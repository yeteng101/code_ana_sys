#!/usr/bin/env python3
"""Build standard Gold cases from reviewed analyzer candidates and manual additions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validation_projects import ROOT, build_ground_truth


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--review-table", type=Path)
    args = parser.parse_args()
    try:
        result = build_ground_truth(
            project_id=args.project_id,
            review_table=args.review_table,
            root=ROOT,
        )
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
