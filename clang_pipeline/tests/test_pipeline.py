from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from clang_pipeline.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "demo" / "sample"


@unittest.skipUnless(shutil.which("clang++"), "clang++ is required")
class ClangPipelineTests(unittest.TestCase):
    def test_seven_stages_produce_evidence_graph(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            outcome = run_pipeline(
                source_root=SAMPLE,
                workspace=workspace,
                run_id="run_test_clang_demo",
                build_profile="demo-poll",
                publish_dir=None,
            )
            self.assertEqual(len(outcome["results"]), 7)

            symbols = json.loads((workspace / "01-index" / "symbols.json").read_text())
            symbol_ids = {item["id"] for item in symbols["symbols"]}
            self.assertIn("fn:demo::app_main", symbol_ids)
            self.assertIn("fn:demo::loop_run", symbol_ids)
            self.assertIn("field:Watcher::callback", symbol_ids)

            graph = json.loads((workspace / "03-callgraph" / "callgraph.json").read_text())
            edge_keys = {
                (item["source"], item["target"], item["kind"]) for item in graph["edges"]
            }
            self.assertIn(
                ("fn:demo::app_main", "fn:demo::loop_run", "direct_call"),
                edge_keys,
            )
            self.assertIn(
                ("fn:demo::loop_run", "fn:demo::wait_for_events", "direct_call"),
                edge_keys,
            )
            self.assertIn(
                ("fn:demo::dispatch_once", "cb:Watcher::callback", "indirect_call"),
                edge_keys,
            )
            self.assertTrue(graph["evidence"])
            self.assertTrue(
                all(
                    item["location"].get("snippet")
                    for item in graph["evidence"]
                    if item["location"].get("file", "").startswith("demo/sample/")
                )
            )

            fptr = json.loads((workspace / "04-fptr" / "fptr-candidates.json").read_text())
            target_names = {
                target["name"]
                for candidate in fptr["candidates"]
                for target in candidate["candidate_targets"]
            }
            self.assertEqual(
                {"on_once", "on_readable", "on_writable"},
                target_names,
            )

            async_result = json.loads(
                (workspace / "05-async" / "async-chains.json").read_text()
            )
            self.assertEqual(1, len(async_result["chains"]))
            self.assertTrue(
                {"on_once", "on_readable", "on_writable"}
                <= {
                    callback["name"]
                    for chain in async_result["chains"]
                    for callback in chain["callbacks"]
                }
            )

            verification = json.loads(
                (workspace / "06-verify" / "verification.json").read_text()
            )
            self.assertTrue(verification["report_ready"])
            self.assertGreaterEqual(verification["coverage"]["coverage_rate"], 0.9)

            self.assertTrue((workspace / "07-report" / "report.md").exists())
            self.assertTrue((workspace / "07-report" / "graph.json").exists())
            self.assertTrue((workspace / "07-report" / "graph.mmd").exists())
            self.assertTrue((workspace / "07-report" / "architecture.json").exists())
            self.assertTrue((workspace / "07-report" / "key-chains.json").exists())
            self.assertTrue((workspace / "07-report" / "analysis.md").exists())

            architecture = json.loads(
                (workspace / "07-report" / "architecture.json").read_text()
            )
            component_ids = {item["id"] for item in architecture["components"]}
            self.assertIn("event_loop", component_ids)
            self.assertIn("app", component_ids)

            analysis = (workspace / "07-report" / "analysis.md").read_text()
            self.assertIn("CALL_WATCHER", analysis)
            self.assertIn("on_readable", analysis)
            self.assertIn("异步回调链", analysis)


if __name__ == "__main__":
    unittest.main()
