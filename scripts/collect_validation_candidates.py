#!/usr/bin/env python3
"""Turn URL-Subagent external JSON files into a human review candidate table."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validation_projects import ROOT, collect_candidates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="maximum candidates per category; 0 keeps every candidate",
    )
    parser.add_argument(
        "--source-root",
        help="analyzed repository checkout used to relativize evidence paths",
    )
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit cannot be negative")
    try:
        result = collect_candidates(
            project_id=args.project_id,
            predictions_dir=args.predictions,
            limit=args.limit,
            source_root=args.source_root,
            root=ROOT,
        )
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
