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
