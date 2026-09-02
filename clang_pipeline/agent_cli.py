from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .agent import AgentContext, run_agent


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
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    ctx = AgentContext(
        workspace,
        repo_root=Path(args.repo_root).resolve(),
        run_id=_run_id_from_workspace(workspace),
    )
    try:
        result: dict[str, Any] = run_agent(
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


if __name__ == "__main__":
    main()
