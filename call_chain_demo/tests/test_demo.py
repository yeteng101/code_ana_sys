from __future__ import annotations

import json
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from call_chain_demo.engine import RequestError, analyze_call_chains, validate_request, validate_result
from call_chain_demo.server import DemoHandler, RUNS, TASKS


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "call_chain_demo" / "examples"


def load_example(name: str) -> dict:
    with (EXAMPLES / name).open(encoding="utf-8") as stream:
        return json.load(stream)


class EngineTests(unittest.TestCase):
    def test_redis_both_directions_and_candidates(self) -> None:
        result = analyze_call_chains(load_example("redis-request.json"))
        validate_result(result)

        self.assertEqual("partial", result["status"])
        self.assertEqual(1, result["target_resolution"]["resolved_total"])
        backward = [item for item in result["findings"] if item["query_direction"] == "backward"]
        forward = [item for item in result["findings"] if item["query_direction"] == "forward"]
        self.assertEqual(1, len(backward))
        self.assertEqual("aeMain", backward[0]["nodes"][0]["name"])
        self.assertEqual("processCommand", backward[0]["nodes"][-1]["name"])
        self.assertEqual(2, len(forward))
        self.assertTrue(all(item["resolution"]["status"] == "multiple_candidates" for item in forward))
        self.assertTrue(all(item["confidence"] == 0.65 for item in forward))
        self.assertFalse(result["coverage"]["complete"])

    def test_libuv_callback_edges(self) -> None:
        result = analyze_call_chains(load_example("libuv-request.json"))
        callback_edges = [
            edge
            for finding in result["findings"]
            for edge in finding["edges"]
            if edge["type"] == "callback_edge"
        ]
        self.assertEqual(2, len(callback_edges))
        self.assertTrue(all(edge["execution_context"]["async_boundary"] for edge in callback_edges))

    def test_callback_filter_stops_before_dispatch(self) -> None:
        request = load_example("redis-request.json")
        request["analysis"]["include_callbacks"] = False
        result = analyze_call_chains(request)
        self.assertFalse(any(
            edge["type"] == "callback_edge"
            for finding in result["findings"]
            for edge in finding["edges"]
        ))

    def test_target_can_resolve_without_node_id(self) -> None:
        request = load_example("redis-request.json")
        del request["targets"][0]["node_id"]
        result = analyze_call_chains(request)
        self.assertEqual(1, result["target_resolution"]["resolved_total"])

    def test_empty_targets_are_rejected(self) -> None:
        request = load_example("redis-request.json")
        request["targets"] = []
        with self.assertRaisesRegex(RequestError, "targets 不能为空"):
            validate_request(request)

    def test_unsafe_paths_are_rejected(self) -> None:
        request = load_example("redis-request.json")
        request["targets"][0]["location"]["file"] = "../outside.c"
        with self.assertRaisesRegex(RequestError, "不能包含"):
            validate_request(request)

    def test_clang_pipeline_graph_snapshot(self) -> None:
        result = analyze_call_chains(load_example("clang-request.json"))
        validate_result(result)
        self.assertIn("clang-pipeline-demo-v1", result["analysis_context"]["graph_snapshot_id"])
        node_ids = {
            node["node_id"]
            for finding in result["findings"]
            for node in finding["nodes"]
        }
        self.assertIn("fn:demo::loop_run", node_ids)
        self.assertIn("fn:demo::dispatch_once", node_ids)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        RUNS.clear()
        TASKS.clear()
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request_json(self, method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=2) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)

    def test_health_and_schema(self) -> None:
        status, body = self.request_json("GET", "/health")
        self.assertEqual(200, status)
        self.assertEqual("ok", body["status"])
        status, body = self.request_json("GET", "/api/v1/schemas/call-chain-request")
        self.assertEqual(200, status)
        self.assertEqual("CallChainRequest", body["title"])

    def test_sync_endpoint(self) -> None:
        status, body = self.request_json("POST", "/api/v1/call-chains", load_example("redis-request.json"))
        self.assertEqual(200, status)
        self.assertEqual("task_redis_chain_001", body["task_id"])
        self.assertGreaterEqual(len(body["findings"]), 3)

    def test_async_endpoint_and_idempotency(self) -> None:
        request = load_example("libuv-request.json")
        status, accepted = self.request_json("POST", "/api/v1/analyze", request)
        self.assertEqual(202, status)
        run_id = accepted["run_id"]
        result = accepted
        for _ in range(30):
            _, result = self.request_json("GET", f"/api/v1/runs/{run_id}")
            if result["status"] not in {"queued", "running"}:
                break
            time.sleep(0.01)
        self.assertIn(result["status"], {"succeeded", "partial"})

        status, repeated = self.request_json("POST", "/api/v1/analyze", request)
        self.assertEqual(200, status)
        self.assertEqual(run_id, repeated["run_id"])

    def test_invalid_request_is_structured(self) -> None:
        request = load_example("redis-request.json")
        request["targets"] = []
        status, body = self.request_json("POST", "/api/v1/call-chains", request)
        self.assertEqual(400, status)
        self.assertEqual("INVALID_TARGETS", body["errors"][0]["code"])


if __name__ == "__main__":
    unittest.main()
