from __future__ import annotations

import json
import tempfile
import unittest
from argparse import Namespace
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from clang_pipeline.cli import command_repo
from clang_pipeline.repo_agent import repository_identity, run_repo_analysis


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "clang_pipeline" / "tests" / "fixtures"
SAMPLE = ROOT / "demo" / "sample"


class RepoAgentTests(unittest.TestCase):
    def test_repo_cli_validation_project_wiring(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bundle"
            result = {
                "status": "succeeded",
                "repository": "fixture/repo",
                "commit": "f" * 40,
                "build_profile": "repository-auto",
                "source_dir": str(Path(tmp) / "source"),
                "output_dir": str(output),
                "pipeline_status": {},
            }
            args = Namespace(
                repo_url="https://example.com/fixture/repo.git",
                output=output,
                branch="",
                commit="",
                work_root="",
                entry=[],
                profile="",
                no_archive=True,
                validation_project="fixture",
                validation_name="Fixture",
                validation_repository="fixture/repo",
                validation_source_root="",
                validation_limit=50,
            )
            with patch("clang_pipeline.cli.run_repo_analysis", return_value=result) as analyze, \
                    patch("clang_pipeline.cli.scaffold_project", return_value={"status": "not_started"}) as scaffold, \
                    patch("clang_pipeline.cli.collect_candidates", return_value={"total_candidates": 0}) as collect, \
                    patch("sys.stdout", new=StringIO()):
                command_repo(args)
            analyze.assert_called_once()
            scaffold.assert_called_once_with(
                project_id="fixture",
                name="Fixture",
                repository="fixture/repo",
                repository_url="https://example.com/fixture/repo.git",
                commit="f" * 40,
                build_profile="repository-auto",
            )
            collect.assert_called_once_with(
                project_id="fixture",
                predictions_dir=output / "external",
                limit=50,
                source_root=result["source_dir"],
            )

    def test_repository_identity_keeps_owner_and_repo(self) -> None:
        self.assertEqual(
            repository_identity("https://github.com/libuv/libuv.git"),
            "libuv/libuv",
        )
        self.assertEqual(
            repository_identity("git@github.com:redis/redis.git"),
            "redis/redis",
        )
        self.assertEqual(
            repository_identity("/Users/andye/Documents/ChatGPT/8.18huawei/demo/sample"),
            "sample",
        )

    def test_file_url_produces_complete_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bundle"
            log_file = Path(tmp) / "runtime.log"
            log_file.write_text(
                "function=open_and_close event=started\n",
                encoding="utf-8",
            )
            result = run_repo_analysis(
                FIXTURE.resolve().as_uri(),
                output_dir=output,
                archive=True,
                log_paths=[log_file],
            )

            self.assertEqual("succeeded", result["status"])
            self.assertTrue(Path(result["source_dir"]).is_dir())
            self.assertTrue(result["build_profile"])
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["repository_url"], FIXTURE.resolve().as_uri())
            self.assertIn("visualization.html", manifest["outputs"].values())
            self.assertIn("external/call-chains.json", manifest["outputs"].values())
            self.assertIn("external/resource-flow.json", manifest["outputs"].values())
            self.assertIn("external/sync-relations.json", manifest["outputs"].values())
            self.assertIn("external/knowledge-graph.json", manifest["outputs"].values())

            for path in (
                "visualization.html",
                "graph.json",
                "report.md",
                "external/call-chains.json",
                "external/resource-flow.json",
                "external/sync-relations.json",
                "external/knowledge-graph.json",
                "knowledge/build-profile.json",
                "knowledge/log-facts.json",
                "knowledge/knowledge-graph.json",
            ):
                self.assertTrue((output / path).exists(), path)
            self.assertTrue(Path(result["archive"]).exists())

            calls = json.loads((output / "external/call-chains.json").read_text())
            resources = json.loads(
                (output / "external/resource-flow.json").read_text()
            )
            sync = json.loads(
                (output / "external/sync-relations.json").read_text()
            )
            knowledge = json.loads(
                (output / "external/knowledge-graph.json").read_text()
            )
            self.assertTrue(calls["items"])
            self.assertTrue(resources["items"])
            self.assertTrue(sync["items"])
            self.assertGreater(knowledge["summary"]["log_events"], 0)
            for document in (calls, resources, sync):
                self.assertNotIn(
                    result["source_dir"],
                    json.dumps(document),
                )
            self.assertNotIn(
                result["source_dir"],
                (output / "visualization.html").read_text(encoding="utf-8"),
            )

    def test_cpp_repository_uses_the_same_url_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cpp-bundle"
            result = run_repo_analysis(
                SAMPLE.resolve().as_uri(),
                output_dir=output,
                archive=False,
            )
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual("succeeded", result["status"])
            self.assertGreater(manifest["summary"]["nodes"], 0)
            self.assertGreater(manifest["summary"]["call_items"], 0)
            self.assertTrue((output / "visualization.html").exists())


if __name__ == "__main__":
    unittest.main()
