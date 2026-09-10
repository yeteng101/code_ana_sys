#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from clang_pipeline.agent import AgentContext
from clang_pipeline.agent_runner import ask_question


def main() -> int:
    parser = argparse.ArgumentParser(
        description="验证 OPENAI_API_KEY、Agent 工具调用和 JSON 输出闭环"
    )
    parser.add_argument("--workspace", default="demo/libuv")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--run-id", default="run_libuv_1.50.0")
    parser.add_argument("--question", default="uv_run 调用了谁？")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL") or "gpt-5")
    parser.add_argument("--max-steps", type=int, default=6)
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY", "").strip():
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "缺少 OPENAI_API_KEY",
                    "next_step": (
                        "export OPENAI_API_KEY='sk-...' && "
                        "python3 scripts/verify_openai.py"
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    ctx = AgentContext(
        Path(args.workspace).resolve(),
        repo_root=Path(args.repo_root).resolve(),
        run_id=args.run_id,
    )
    try:
        result = ask_question(
            args.question,
            ctx,
            backend="openai",
            max_steps=args.max_steps,
            model=args.model,
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "backend": "openai",
                    "error": {"message": str(exc)},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    checks = [
        {"name": "status_succeeded", "passed": result.get("status") == "succeeded"},
        {"name": "answer_nonempty", "passed": bool(str(result.get("answer", "")).strip())},
        {"name": "tool_called", "passed": bool(result.get("tool_calls"))},
    ]
    status = "verified" if all(item["passed"] for item in checks) else "failed"
    print(
        json.dumps(
            {
                "status": status,
                "backend": "openai",
                "model": args.model,
                "checks": checks,
                "result": result,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if status == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
