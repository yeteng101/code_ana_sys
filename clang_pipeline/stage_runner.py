from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import stages


STAGE_FUNCTIONS = {
    "01-index": stages.stage01_index,
    "02-macro": stages.stage02_macro,
    "03-callgraph": stages.stage03_callgraph,
    "04-fptr": stages.stage04_fptr,
    "05-async": stages.stage05_async,
    "06-verify": stages.stage06_verify,
    "07-report": stages.stage07_report,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one Clang pipeline stage")
    parser.add_argument("stage", choices=sorted(STAGE_FUNCTIONS))
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    result = STAGE_FUNCTIONS[args.stage](workspace)
    print(
        json.dumps(
            {
                "stage": args.stage,
                "status": result.get("status", "succeeded"),
                "workspace": str(workspace),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
