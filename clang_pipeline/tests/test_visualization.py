from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from clang_pipeline.visualization import write_visualization


class VisualizationTests(unittest.TestCase):
    def test_writes_repository_independent_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            (workspace / "07-report").mkdir()
            graph = {
                "run_id": "generic-run",
                "meta": {
                    "repository": "example/alpha-beta",
                    "commit": "a" * 40,
                    "build_profile": "generic",
                },
                "nodes": [
                    {
                        "id": "fn:alpha",
                        "name": "alpha",
                        "kind": "function",
                        "file": "project/alpha.c",
                    },
                    {
                        "id": "fn:beta",
                        "name": "beta",
                        "kind": "function",
                        "file": "project/beta.c",
                    },
                ],
                "edges": [
                    {
                        "id": "edge-alpha-beta",
                        "source": "fn:alpha",
                        "target": "fn:beta",
                        "kind": "direct_call",
                        "call_site": {
                            "file": "project/alpha.c",
                            "line": 7,
                            "snippet": "beta();",
                        },
                        "confidence": 1.0,
                    }
                ],
                "evidence": [],
            }
            path = write_visualization(
                workspace,
                graph,
                resource_flow={
                    "status": "partial",
                    "items": [{"resource_type": "memory"}],
                },
                sync_relations={
                    "status": "succeeded",
                    "items": [{"relation_type": "mutex_lock"}],
                },
            )
            text = path.read_text(encoding="utf-8")
            self.assertIn("alpha", text)
            self.assertIn("beta", text)
            self.assertIn("Module Graph", text)
            self.assertIn("Full Call Graph", text)
            self.assertIn("Calls", text)
            self.assertNotIn("uv_run", text)
            payload_start = text.index('<script id="viz-data"')
            payload_end = text.index("</script>", payload_start)
            payload_text = text[
                text.index(">", payload_start) + 1 : payload_end
            ]
            payload = json.loads(payload_text)
            self.assertEqual(payload["metrics"]["nodes"], 2)
            self.assertEqual(payload["metrics"]["edges"], 1)
            self.assertEqual(len(payload["full_graph"]["nodes"]), 2)
            self.assertEqual(len(payload["full_graph"]["edges"]), 1)


if __name__ == "__main__":
    unittest.main()
