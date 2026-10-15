from __future__ import annotations

import json
import unittest
from pathlib import Path

from clang_pipeline.resource_flow import analyze_resource_flow
from clang_pipeline.sync_flow import analyze_sync_relations


ROOT = Path(__file__).resolve().parents[2]
LIBUV_GRAPH = ROOT / "demo" / "libuv" / "graph.json"


@unittest.skipUnless(LIBUV_GRAPH.exists(), "demo/libuv graph required")
class NativeAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = json.loads(LIBUV_GRAPH.read_text(encoding="utf-8"))

    def test_resource_flow_has_native_operations_and_evidence(self) -> None:
        result = analyze_resource_flow(self.graph)
        self.assertEqual("resource_flow", result["result_type"])
        self.assertEqual("analyzer", result["source"]["origin"])
        self.assertTrue(result["items"])
        for item in result["items"]:
            self.assertTrue(item["evidence_ids"])
            self.assertEqual("unconfirmed", item["status"])
            for operation in item["operations"]:
                self.assertTrue(operation["evidence_ids"])
                self.assertIn("status", operation)
                self.assertIsInstance(operation["confidence"], (int, float))

    def test_resource_flow_uses_exact_apis_and_stable_resource_ids(self) -> None:
        graph = {
            "run_id": "resource-exact-test",
            "meta": {
                "repository": "example/repo",
                "commit": "a" * 40,
            },
            "nodes": [
                {"id": "fn:uv__getpwuid_r", "kind": "function", "name": "uv__getpwuid_r"},
                {"id": "fn:uv__malloc", "kind": "function", "name": "uv__malloc"},
                {"id": "fn:uv__free", "kind": "function", "name": "uv__free"},
                {"id": "fn:uv__free_client", "kind": "function", "name": "uv__free_client"},
                {"id": "fn:uv__open_context", "kind": "function", "name": "uv__open_context"},
            ],
            "edges": [
                {
                    "id": "acquire",
                    "source": "fn:uv__getpwuid_r",
                    "target": "fn:uv__malloc",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/core.c",
                        "line": 10,
                        "snippet": "buf = uv__malloc(bufsize);",
                    },
                    "evidence_ids": ["ev-acquire"],
                },
                {
                    "id": "release",
                    "source": "fn:uv__getpwuid_r",
                    "target": "fn:uv__free",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/core.c",
                        "line": 20,
                        "snippet": "uv__free(buf);",
                    },
                    "evidence_ids": ["ev-release"],
                },
                {
                    "id": "false-release",
                    "source": "fn:uv__getpwuid_r",
                    "target": "fn:uv__free_client",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/core.c",
                        "line": 30,
                        "snippet": "uv__free_client(client);",
                    },
                    "evidence_ids": ["ev-false-release"],
                },
                {
                    "id": "false-acquire",
                    "source": "fn:uv__getpwuid_r",
                    "target": "fn:uv__open_context",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/core.c",
                        "line": 40,
                        "snippet": "uv__open_context(ctx);",
                    },
                    "evidence_ids": ["ev-false-acquire"],
                },
            ],
            "evidence": [
                {"id": "ev-acquire", "file": "src/core.c", "line": 10},
                {"id": "ev-release", "file": "src/core.c", "line": 20},
                {"id": "ev-false-release", "file": "src/core.c", "line": 30},
                {"id": "ev-false-acquire", "file": "src/core.c", "line": 40},
            ],
        }
        result = analyze_resource_flow(graph)
        self.assertEqual(1, len(result["items"]))
        item = result["items"][0]
        self.assertEqual("rf_libuv_getpwuid_buf_v1", item["resource"])
        self.assertEqual("buf", item["resource_expression"])
        self.assertEqual({"acquire", "release"}, {
            operation["kind"] for operation in item["operations"]
        })

    def test_sync_relations_have_native_relations_and_evidence(self) -> None:
        result = analyze_sync_relations(self.graph)
        self.assertEqual("sync_relation", result["result_type"])
        self.assertEqual("analyzer", result["source"]["origin"])
        self.assertTrue(result["items"])
        relation_types = {item["relation_type"] for item in result["items"]}
        self.assertIn("mutex_lock", relation_types)
        for item in result["items"]:
            self.assertEqual("unconfirmed", item["status"])
            self.assertTrue(item["evidence_ids"])
            self.assertIn(item["order"], {"happens_before", "happens_after", "concurrent", "unknown"})


if __name__ == "__main__":
    unittest.main()
