from __future__ import annotations

import json
import os
from typing import Any

from .agent import SYSTEM_PROMPT, AgentContext, run_agent
from .agent_context import write_agent_context
from .claude_code_bridge import claude_code_available, run_claude_code
from .llm_bridge import llm_enabled


ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence_ids": {"type": "array", "items": {"type": "string"}},
        "disclaimer": {"type": "string"},
    },
    "required": ["answer", "confidence", "evidence_ids"],
}


def resolve_backend(value: str) -> str:
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


def ask_question(
    question: str,
    ctx: AgentContext,
    *,
    backend: str = "auto",
    max_steps: int = 6,
    model: str | None = None,
    focus: list[str] | None = None,
) -> dict[str, Any]:
    backend = resolve_backend(backend)
    if backend == "claude-code":
        return _ask_claude_code(question, ctx, model=model, focus=focus)
    return _ask_openai(question, ctx, max_steps=max_steps, model=model)


def _ask_openai(
    question: str,
    ctx: AgentContext,
    *,
    max_steps: int,
    model: str | None,
) -> dict[str, Any]:
    result = run_agent(
        question,
        ctx,
        max_steps=max_steps,
        model=model,
    )
    result["backend"] = "openai"
    return result


def _ask_claude_code(
    question: str,
    ctx: AgentContext,
    *,
    model: str | None,
    focus: list[str] | None,
) -> dict[str, Any]:
    context_path = write_agent_context(ctx, question, focus=focus)
    prompt = (
        f"请先读取上下文文件 {context_path}，再回答下面的问题。\n"
        f"上下文文件里包含 artifact_paths，如需要可继续读取对应产物。\n\n"
        f"问题：{question}"
    )
    payload = run_claude_code(
        prompt,
        system_prompt=SYSTEM_PROMPT,
        model=model,
        cwd=ctx.repo_root,
        json_schema=ANSWER_SCHEMA,
        add_dirs=[ctx.workspace],
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
        "question": question,
        "answer": parsed.get("answer", str(payload)),
        "confidence": float(parsed.get("confidence", 0.5)),
        "evidence_chain": evidence_chain,
        "paths": parsed.get("paths", []),
        "disclaimer": parsed.get("disclaimer", ""),
        "tool_calls": [
            {
                "tool": "claude-code",
                "status": "ok",
                "arguments": {"context_file": str(context_path)},
            }
        ],
        "status": "succeeded",
        "backend": "claude-code",
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
