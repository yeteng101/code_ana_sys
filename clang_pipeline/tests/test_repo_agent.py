from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from clang_pipeline.repo_agent import run_repo_analysis


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "clang_pipeline" / "tests" / "fixtures"


class RepoAgentTests(unittest.TestCase):
    def test_file_url_produces_complete_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bundle"
            result = run_repo_analysis(
                FIXTURE.resolve().as_uri(),
                output_dir=output,
                archive=True,
            )

            self.assertEqual("succeeded", result["status"])
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["repository_url"], FIXTURE.resolve().as_uri())
            self.assertIn("visualization.html", manifest["outputs"].values())
            self.assertIn("external/call-chains.json", manifest["outputs"].values())
            self.assertIn("external/resource-flow.json", manifest["outputs"].values())
            self.assertIn("external/sync-relations.json", manifest["outputs"].values())

            for path in (
                "visualization.html",
                "graph.json",
                "report.md",
                "external/call-chains.json",
                "external/resource-flow.json",
                "external/sync-relations.json",
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
            self.assertTrue(calls["items"])
            self.assertTrue(resources["items"])
            self.assertTrue(sync["items"])


if __name__ == "__main__":
    unittest.main()
