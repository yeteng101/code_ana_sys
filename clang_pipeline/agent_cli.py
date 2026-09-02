from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .agent import SYSTEM_PROMPT, AgentContext, run_agent
from .claude_code_bridge import claude_code_available, run_claude_code
from .llm_bridge import llm_enabled


ROOT = Path(__file__).resolve().parents[1]


def _run_id_from_workspace(workspace: Path) -> str:
    name = workspace.name
    return name if name.startswith("run_") else "run_cli_agent"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="代码逆向 Agent CLI，结果以 JSON 输出到 stdout"
    )
    parser.add_argument("--question", required=True)
    parser.add_argument("--workspace", default="demo/libuv")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--max-steps", type=int, default=6)
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--backend",
        choices=["auto", "openai", "claude-code"],
        default="auto",
        help="auto 优先 claude-code，其次 openai",
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    ctx = AgentContext(
        workspace,
        repo_root=Path(args.repo_root).resolve(),
        run_id=_run_id_from_workspace(workspace),
    )
    try:
        backend = _resolve_backend(args.backend)
        if backend == "claude-code":
            result = _run_claude_backend(args, ctx)
        else:
            result = run_agent(
                args.question,
                ctx,
                max_steps=args.max_steps,
                model=args.model,
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "question": args.question,
                    "error": {"message": str(exc)},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1) from exc


def _resolve_backend(value: str) -> str:
    if value != "auto":
        return value
    provider = os.environ.get("AGENT_LLM_PROVIDER", "").strip()
    if provider in {"openai", "claude-code"}:
        return provider
    if claude_code_available():
        return "claude-code"
    if llm_enabled():
        return "openai"
    return "openai"


def _run_claude_backend(args: argparse.Namespace, ctx: AgentContext) -> dict[str, Any]:
    analysis = ctx.read_analysis()
    prompt = args.question
    if analysis:
        prompt = (
            f"{args.question}\n\n"
            f"请基于以下已有分析产物回答。\n\n{analysis[:8000]}"
        )
    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "evidence_ids": {"type": "array", "items": {"type": "string"}},
            "disclaimer": {"type": "string"},
        },
        "required": ["answer", "confidence", "evidence_ids"],
    }
    payload = run_claude_code(
        prompt,
        system_prompt=SYSTEM_PROMPT,
        model=args.model,
        cwd=args.repo_root,
        json_schema=schema,
    )
    content = payload.get("result")
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"answer": content, "confidence": 0.5, "evidence_ids": []}
    elif isinstance(content, dict):
        parsed = content
    else:
        parsed = payload
    evidence_chain = _evidence_chain(ctx, parsed.get("evidence_ids", []))
    return {
        "run_id": ctx.run_id,
        "question": args.question,
        "answer": parsed.get("answer", str(payload)),
        "confidence": float(parsed.get("confidence", 0.5)),
        "evidence_chain": evidence_chain,
        "paths": parsed.get("paths", []),
        "disclaimer": parsed.get("disclaimer", ""),
        "tool_calls": [{"tool": "claude-code", "status": "ok"}],
        "status": "succeeded",
    }


def _evidence_chain(ctx: AgentContext, evidence_ids: list[str]) -> list[dict[str, Any]]:
    try:
        graph = ctx.load_graph()
    except Exception:
        return []
    evidence_by_id = {item["id"]: item for item in graph.get("evidence", [])}
    return [
        evidence_by_id[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in evidence_by_id
    ]


if __name__ == "__main__":
    main()
