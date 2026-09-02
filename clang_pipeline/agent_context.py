from __future__ import annotations

from pathlib import Path
from typing import Any

from .agent import AgentContext
from .clang_ast import write_json


def build_agent_context(
    ctx: AgentContext,
    question: str,
    *,
    focus: list[str] | None = None,
    max_key_chains: int = 10,
    max_evidence: int = 20,
) -> dict[str, Any]:
    graph = ctx.load_graph()
    focus = focus or []
    key_chains: dict[str, Any] = {"paths": []}
    architecture: dict[str, Any] = {"components": []}
    try:
        key_chains = ctx.load_key_chains()
    except Exception:
        pass
    try:
        architecture = ctx.load_architecture()
    except Exception:
        pass

    evidence = graph.get("evidence", [])
    selected_evidence = _select_evidence(evidence, focus, max_evidence)
    paths = key_chains.get("paths", [])[:max_key_chains]

    return {
        "schema_version": "1.0",
        "run_id": ctx.run_id,
        "question": question,
        "focus": focus,
        "summary": ctx.read_analysis()[:4000],
        "key_chains": paths,
        "architecture": architecture.get("components", [])[:20],
        "evidence": selected_evidence,
        "graph_stats": {
            "nodes": len(graph.get("nodes", [])),
            "edges": len(graph.get("edges", [])),
        },
        "artifact_paths": {
            "graph": _artifact_path(ctx.workspace, "07-report/graph.json", "graph.json"),
            "architecture": _artifact_path(
                ctx.workspace, "07-report/architecture.json", "architecture.json"
            ),
            "key_chains": _artifact_path(
                ctx.workspace, "07-report/key-chains.json", "key-chains.json"
            ),
            "analysis": _artifact_path(
                ctx.workspace, "07-report/analysis.md", "analysis.md"
            ),
        },
    }


def _select_evidence(
    evidence: list[dict[str, Any]],
    focus: list[str],
    limit: int,
) -> list[dict[str, Any]]:
    if focus:
        selected = [
            item
            for item in evidence
            if any(
                name in (item.get("location") or {}).get("snippet", "")
                or name in item.get("id", "")
                for name in focus
            )
        ]
        if selected:
            return selected[:limit]
    return evidence[:limit]


def _artifact_path(workspace: Path, *names: str) -> str:
    for name in names:
        path = workspace / name
        if path.exists():
            return str(path)
    return ""


def write_agent_context(
    ctx: AgentContext,
    question: str,
    *,
    focus: list[str] | None = None,
) -> Path:
    payload = build_agent_context(ctx, question, focus=focus)
    target = ctx.workspace / "agent-context.json"
    write_json(target, payload)
    return target
