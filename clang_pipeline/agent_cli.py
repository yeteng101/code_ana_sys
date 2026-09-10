from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent import AgentContext
from .agent_runner import ask_question
from .nl_repo import prepare_question_context


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="代码逆向 Agent CLI，结果以 JSON 输出到 stdout"
    )
    parser.add_argument("--question", required=True)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--max-steps", type=int, default=6)
    parser.add_argument("--model", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--source", default=None)
    parser.add_argument("--compile-commands", default=None)
    parser.add_argument(
        "--auto-analyze",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="问题中包含源码仓库路径时，先自动运行七阶段流水线",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "openai", "claude-code"],
        default="auto",
        help="auto 优先 claude-code，其次 openai",
    )
    parser.add_argument("--focus", action="append", default=[])
    args = parser.parse_args()

    workspace, run_id, analysis = prepare_question_context(
        args.question,
        source=args.source,
        workspace=args.workspace,
        run_id=args.run_id,
        compile_commands=args.compile_commands,
        auto_analyze=args.auto_analyze,
    )
    ctx = AgentContext(
        workspace,
        repo_root=Path(args.repo_root).resolve(),
        run_id=run_id,
    )
    try:
        result = ask_question(
            args.question,
            ctx,
            backend=args.backend,
            max_steps=args.max_steps,
            model=args.model,
            focus=args.focus or None,
        )
        if analysis is not None:
            result["analysis"] = analysis
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


if __name__ == "__main__":
    main()
