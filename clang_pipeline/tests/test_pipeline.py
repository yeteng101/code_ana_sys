from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from clang_pipeline.pipeline import run_pipeline
from clang_pipeline.resource_flow import analyze_resource_flow


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "demo" / "sample"
EXTERNAL_FIXTURE = ROOT / "clang_pipeline" / "tests" / "fixtures"


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
            visualization = (
                workspace / "07-report" / "visualization.html"
            ).read_text(encoding="utf-8")
            self.assertIn("event_loop", visualization)
            self.assertIn("app", visualization)
            self.assertTrue(
                (workspace / "08-resource-flow" / "resource-flow.json").exists()
            )
            self.assertTrue(
                (workspace / "09-sync-relations" / "sync-relations.json").exists()
            )
            self.assertTrue((workspace / "external" / "resource-flow.json").exists())
            self.assertTrue(
                (workspace / "external" / "sync-relations.json").exists()
            )
            native = outcome["native"]
            self.assertEqual("succeeded", native["status"])
            self.assertIn("resource_flow", native)
            self.assertIn("sync_relations", native)
            self.assertIn("visualization", native)

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

    def test_external_function_calls_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            run_pipeline(
                source_root=EXTERNAL_FIXTURE,
                workspace=workspace,
                run_id="run_test_external_flow",
                build_profile="external-flow",
                publish_dir=None,
            )

            graph = json.loads(
                (workspace / "07-report" / "graph.json").read_text()
            )
            node_names = {
                node["id"]: node.get("name", node["id"])
                for node in graph["nodes"]
            }
            target_names = {
                node_names[edge["target"]]
                for edge in graph["edges"]
                if edge.get("target")
            }
            self.assertTrue(
                {
                    "open",
                    "close",
                    "getaddrinfo",
                    "freeaddrinfo",
                    "pthread_mutex_lock",
                    "pthread_cond_wait",
                    "pthread_mutex_unlock",
                }
                <= target_names
            )
            self.assertGreaterEqual(
                sum(
                    node.get("kind") == "external_function"
                    for node in graph["nodes"]
                ),
                7,
            )

            resource_flow = json.loads(
                (
                    workspace
                    / "08-resource-flow"
                    / "resource-flow.json"
                ).read_text()
            )
            resource_facts = {
                (
                    operation.get("api"),
                    operation.get("function"),
                    operation.get("kind"),
                )
                for item in resource_flow["items"]
                for operation in item["operations"]
            }
            self.assertTrue(
                {
                    ("open", "open_and_close", "acquire"),
                    ("close", "open_and_close", "release"),
                    ("getaddrinfo", "resolve_host", "acquire"),
                    ("freeaddrinfo", "resolve_host", "release"),
                }
                <= resource_facts
            )

            sync_relations = json.loads(
                (
                    workspace
                    / "09-sync-relations"
                    / "sync-relations.json"
                ).read_text()
            )
            self.assertTrue(sync_relations["items"])
            self.assertIn(
                "mutex_lock",
                {item["relation_type"] for item in sync_relations["items"]},
            )
            visualization = (
                workspace / "07-report" / "visualization.html"
            ).read_text(encoding="utf-8")
            self.assertIn("pthread_mutex_lock", visualization)
            self.assertIn("open", visualization)

    def test_macro_builtin_and_platform_conditions_are_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            run_pipeline(
                source_root=EXTERNAL_FIXTURE.parent,
                workspace=workspace,
                run_id="run_test_macro_builtin",
                build_profile="fixture-platform",
                defines=["PLATFORM_TEST"],
                publish_dir=None,
            )

            graph = json.loads(
                (workspace / "07-report" / "graph.json").read_text()
            )
            node_names = {node["id"]: node["name"] for node in graph["nodes"]}
            edges = [
                (node_names[edge["source"]], node_names[edge["target"]], edge)
                for edge in graph["edges"]
            ]
            memset_edges = [
                edge for source, target, edge in edges
                if source == "clear_buffer" and target == "memset"
            ]
            self.assertEqual(1, len(memset_edges))
            self.assertIn("ZERO_BUFFER", str(memset_edges[0].get("condition")))

            poll_edges = [
                edge for source, target, edge in edges
                if source == "wait_platform" and target == "poll"
            ]
            self.assertEqual(1, len(poll_edges))
            self.assertIn("PLATFORM_TEST", str(poll_edges[0].get("condition")))
            verification = json.loads(
                (workspace / "06-verify" / "verification.json").read_text()
            )
            self.assertTrue(
                any(item.get("method") == "macro_expansion" for item in verification["checks"])
            )

    def test_resource_assignment_alias_and_cross_function_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            run_pipeline(
                source_root=EXTERNAL_FIXTURE.parent,
                workspace=workspace,
                run_id="run_test_resource_ownership",
                build_profile="fixture-resource",
                publish_dir=None,
            )
            graph = json.loads(
                (workspace / "07-report" / "graph.json").read_text()
            )
            result = analyze_resource_flow(
                graph,
                source_root=EXTERNAL_FIXTURE.parent,
            )
            transfers = [
                item
                for item in result["items"]
                if item["ownership_model"] == "cross_function_transfer"
            ]
            self.assertTrue(transfers)
            self.assertTrue(any(
                operation["kind"] == "transfer"
                for item in transfers
                for operation in item["operations"]
            ))
            self.assertTrue(any(
                item.get("data_flow")
                for item in transfers
            ))

    def test_pipeline_logs_flow_into_knowledge_graph(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            log = root / "runtime.log"
            log.write_text(
                "function=app_main event=startup\n",
                encoding="utf-8",
            )
            run_pipeline(
                source_root=SAMPLE,
                workspace=workspace,
                run_id="run_test_pipeline_log",
                build_profile="demo-poll",
                publish_dir=None,
                log_paths=[log],
            )
            facts = json.loads(
                (workspace / "10-knowledge" / "log-facts.json").read_text()
            )
            knowledge = json.loads(
                (workspace / "10-knowledge" / "knowledge-graph.json").read_text()
            )
            self.assertEqual(1, len(facts["events"]))
            self.assertGreater(knowledge["summary"]["log_events"], 0)


if __name__ == "__main__":
    unittest.main()
