#!/usr/bin/env python3
"""Pin LF-normalized SHA-256 hashes for every validation evidence source."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validation_projects import ROOT, pin_validation_sources


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    args = parser.parse_args()
    try:
        result = pin_validation_sources(project_id=args.project_id, root=ROOT)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
