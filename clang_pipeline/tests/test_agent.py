from __future__ import annotations

import unittest
from pathlib import Path

from clang_pipeline.agent import AgentContext, execute_tool, fallback_answer
from clang_pipeline.agent_context import build_agent_context, write_agent_context


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "demo" / "libuv"


@unittest.skipUnless((WORKSPACE / "graph.json").exists(), "demo/libuv artifacts required")
class AgentToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = AgentContext(WORKSPACE, repo_root=ROOT)

    def test_call_graph_tool(self) -> None:
        result = execute_tool(self.ctx, "get_call_graph", {"entry": "uv_run", "depth": 2})
        self.assertIn("fn:uv_run", result)
        self.assertIn("fn:uv__io_poll", result)

    def test_key_chains_and_architecture(self) -> None:
        chains = execute_tool(self.ctx, "get_key_chains", {})
        self.assertIn("uv_run", chains)
        architecture = execute_tool(self.ctx, "get_architecture", {})
        self.assertIn("unix", architecture)

    def test_evidence_and_source(self) -> None:
        evidence = execute_tool(
            self.ctx,
            "get_evidence",
            {"evidence_ids": ["ev_a3dcf6ec0abb"]},
        )
        self.assertIn("uv__io_poll(loop, timeout);", evidence)
        source = execute_tool(
            self.ctx,
            "get_source_snippet",
            {"file": "third_party/libuv/src/unix/core.c", "line": 460},
        )
        self.assertIn("uv__io_poll(loop, timeout);", source)

    def test_fallback_without_api_key(self) -> None:
        result = fallback_answer("uv_run 调用了谁？", self.ctx)
        self.assertEqual("partial", result["status"])
        self.assertIn("规则模板", result["answer"])

    def test_agent_context_file(self) -> None:
        payload = build_agent_context(
            self.ctx,
            "uv_run 调用了谁？",
            focus=["uv_run"],
        )
        self.assertIn("artifact_paths", payload)
        self.assertTrue(payload["artifact_paths"]["graph"])
        path = write_agent_context(self.ctx, "uv_run 调用了谁？", focus=["uv_run"])
        self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
