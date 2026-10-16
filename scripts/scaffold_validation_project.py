#!/usr/bin/env python3
"""Create a repository-specific validation project from the shared template."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validation_projects import ROOT, scaffold_project


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--name", default="")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--commit", default="")
    parser.add_argument("--build-profile", default="repository-auto")
    parser.add_argument("--source-root", default="")
    parser.add_argument(
        "--output",
        type=Path,
        help="defaults to validation/datasets/<project-id>",
    )
    args = parser.parse_args()
    try:
        result = scaffold_project(
            project_id=args.project_id,
            name=args.name,
            repository=args.repository,
            repository_url=args.repository_url,
            commit=args.commit,
            build_profile=args.build_profile,
            source_root=args.source_root,
            output_dir=args.output,
            root=ROOT,
        )
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
