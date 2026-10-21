from __future__ import annotations

import json
import unittest
from pathlib import Path

from clang_pipeline.resource_flow import analyze_resource_flow
from clang_pipeline.sync_flow import analyze_sync_relations


ROOT = Path(__file__).resolve().parents[2]
LIBUV_GRAPH = ROOT / "demo" / "libuv" / "graph.json"
REDIS_GRAPH = ROOT / "demo" / "redis" / "graph.json"


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

    def test_cross_function_queue_atomic_and_thread_join_relations(self) -> None:
        graph = {
            "run_id": "sync-enhancement-test",
            "meta": {"repository": "fixture/repo", "commit": "a" * 40},
            "nodes": [
                {"id": "fn:producer", "kind": "function", "name": "producer"},
                {"id": "fn:consumer", "kind": "function", "name": "consumer"},
                {"id": "fn:main", "kind": "function", "name": "main"},
                {"id": "fn:listAddNodeTail", "kind": "external_function", "name": "listAddNodeTail"},
                {"id": "fn:listFirst", "kind": "external_function", "name": "listFirst"},
                {"id": "fn:atomic_store_explicit", "kind": "external_function", "name": "atomic_store_explicit"},
                {"id": "fn:atomic_load_explicit", "kind": "external_function", "name": "atomic_load_explicit"},
                {"id": "fn:pthread_create", "kind": "external_function", "name": "pthread_create"},
                {"id": "fn:pthread_join", "kind": "external_function", "name": "pthread_join"},
            ],
            "edges": [
                {
                    "id": "queue-producer",
                    "source": "fn:producer",
                    "target": "fn:listAddNodeTail",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/queue.c",
                        "line": 10,
                        "snippet": "listAddNodeTail(queue, item);",
                    },
                    "evidence_ids": ["ev-queue-producer"],
                },
                {
                    "id": "queue-consumer",
                    "source": "fn:consumer",
                    "target": "fn:listFirst",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/queue.c",
                        "line": 20,
                        "snippet": "item = listFirst(queue);",
                    },
                    "evidence_ids": ["ev-queue-consumer"],
                },
                {
                    "id": "atomic-release",
                    "source": "fn:producer",
                    "target": "fn:atomic_store_explicit",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/atomic.c",
                        "line": 12,
                        "snippet": "atomic_store_explicit(&ready, 1, memory_order_release);",
                    },
                    "evidence_ids": ["ev-atomic-release"],
                },
                {
                    "id": "atomic-acquire",
                    "source": "fn:consumer",
                    "target": "fn:atomic_load_explicit",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/atomic.c",
                        "line": 22,
                        "snippet": "value = atomic_load_explicit(&ready, memory_order_acquire);",
                    },
                    "evidence_ids": ["ev-atomic-acquire"],
                },
                {
                    "id": "thread-create",
                    "source": "fn:main",
                    "target": "fn:pthread_create",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/thread.c",
                        "line": 5,
                        "snippet": "pthread_create(&worker, NULL, run, NULL);",
                    },
                    "evidence_ids": ["ev-thread-create"],
                },
                {
                    "id": "thread-join",
                    "source": "fn:main",
                    "target": "fn:pthread_join",
                    "kind": "direct_call",
                    "call_site": {
                        "file": "src/thread.c",
                        "line": 30,
                        "snippet": "pthread_join(worker, NULL);",
                    },
                    "evidence_ids": ["ev-thread-join"],
                },
            ],
            "evidence": [
                {"id": "ev-queue-producer", "file": "src/queue.c", "line": 10},
                {"id": "ev-queue-consumer", "file": "src/queue.c", "line": 20},
                {"id": "ev-atomic-release", "file": "src/atomic.c", "line": 12},
                {"id": "ev-atomic-acquire", "file": "src/atomic.c", "line": 22},
                {"id": "ev-thread-create", "file": "src/thread.c", "line": 5},
                {"id": "ev-thread-join", "file": "src/thread.c", "line": 30},
            ],
        }
        result = analyze_sync_relations(graph)
        relations = result["items"]
        self.assertTrue(any(
            "cross-function queue publication queue" in str(item.get("condition"))
            for item in relations
        ))
        self.assertTrue(any(
            item["relation_type"] == "atomic"
            and item["source"]["function"] == "producer"
            and item["target"]["function"] == "consumer"
            and item["order"] == "happens_before"
            for item in relations
        ))
        self.assertTrue(any(
            item["relation_type"] == "thread_join"
            and "thread handle worker" in str(item.get("condition"))
            for item in relations
        ))

    @unittest.skipUnless(REDIS_GRAPH.exists(), "demo/redis graph required")
    def test_redis_program_order_relations_are_emitted(self) -> None:
        graph = json.loads(REDIS_GRAPH.read_text(encoding="utf-8"))
        result = analyze_sync_relations(graph)
        endpoints = {
            (
                item["source"]["function"],
                item["source"]["line"],
                item["target"]["function"],
                item["target"]["line"],
                item["order"],
            )
            for item in result["items"]
        }
        self.assertTrue(
            {
                ("bioSubmitJob", 155, "bioSubmitJob", 156, "happens_before"),
                ("bioSubmitJob", 156, "bioSubmitJob", 158, "happens_before"),
                ("bioDrainWorker", 317, "bioDrainWorker", 319, "happens_before"),
                ("IOThreadMain", 4192, "IOThreadMain", 4193, "happens_before"),
            }
            <= endpoints
        )
        self.assertTrue(
            any(
                "cross-function queue publication" in str(item.get("condition"))
                and item["source"]["function"] == "bioSubmitJob"
                and item["target"]["function"] == "bioProcessBackgroundJobs"
                for item in result["items"]
            )
        )
        source_result = analyze_sync_relations(graph, source_root=ROOT)
        self.assertTrue(
            any(
                item["relation_type"] == "atomic"
                and item["source"]["function"] == "setIOPendingCount"
                and item["target"]["function"] == "getIOPendingCount"
                for item in source_result["items"]
            )
        )


if __name__ == "__main__":
    unittest.main()
