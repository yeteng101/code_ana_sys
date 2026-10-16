#!/usr/bin/env python3
"""Check every project registered in validation/projects.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validation_projects import ROOT, check_registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail if any project remains in a pending/incomplete review state",
    )
    args = parser.parse_args()
    try:
        result = check_registry(root=ROOT)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    incomplete = [
        project
        for project in result["projects"]
        if project.get("project_status") in {"not_started", "candidates_collected", "in_review"}
        or project.get("human_review") != "confirmed"
    ]
    return 1 if result["status"] == "failed" or (args.strict and incomplete) else 0


if __name__ == "__main__":
    raise SystemExit(main())
