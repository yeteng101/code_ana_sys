#!/usr/bin/env python3
"""Run project checks, generic evaluation, reports, and quality thresholds."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validation.benchmark import FILES, evaluate, markdown, read, write
from scripts.validation_projects import (
    check_legacy_project,
    check_project,
    project_entry,
)


def _metric(report: dict, category: str, key: str) -> float | None:
    return report["categories"][category].get(key)


def build_gate(
    report: dict,
    *,
    min_call_recall: float | None,
    min_resource_recall: float | None,
    min_sync_recall: float | None,
    max_fp: int,
    strict_review: bool,
) -> dict:
    checks = []
    thresholds = {
        "call_chain": min_call_recall,
        "resource_flow": min_resource_recall,
        "sync_relation": min_sync_recall,
    }
    for category, minimum in thresholds.items():
        if minimum is None:
            continue
        actual = _metric(report, category, "recall")
        passed = actual is not None and actual + 1e-12 >= minimum
        checks.append(
            {
                "name": f"{category}.recall",
                "status": "passed" if passed else "failed",
                "actual": actual,
                "minimum": minimum,
            }
        )
    fp_total = sum(int(report["categories"][name].get("fp") or 0) for name in FILES)
    checks.append(
        {
            "name": "false_positives",
            "status": "passed" if fp_total <= max_fp else "failed",
            "actual": fp_total,
            "maximum": max_fp,
        }
    )
    review = report.get("review", {})
    human_review = str(review.get("human_review") or "pending")
    if strict_review:
        checks.append(
            {
                "name": "human_review",
                "status": "passed" if human_review == "confirmed" else "failed",
                "actual": human_review,
                "required": "confirmed",
            }
        )
    else:
        checks.append(
            {
                "name": "human_review",
                "status": "informational",
                "actual": human_review,
            }
        )
    failed = [item for item in checks if item["status"] == "failed"]
    return {
        "schema_version": "1.0",
        "status": "failed" if failed else "passed",
        "human_review": human_review,
        "strict_review": strict_review,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", default="")
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-call-recall", type=float)
    parser.add_argument("--min-resource-recall", type=float)
    parser.add_argument("--min-sync-recall", type=float)
    parser.add_argument("--max-fp", type=int, default=0)
    parser.add_argument(
        "--strict-review",
        action="store_true",
        help="fail unless review.human_review is confirmed",
    )
    args = parser.parse_args()
    for name in ("min_call_recall", "min_resource_recall", "min_sync_recall"):
        value = getattr(args, name)
        if value is not None and not 0 <= value <= 1:
            parser.error(f"--{name.replace('_', '-')} must be between 0 and 1")
    if args.max_fp < 0:
        parser.error("--max-fp cannot be negative")

    truth = read(args.ground_truth)
    documents = {
        category: read(args.predictions / (filename + ".json"))
        for category, filename in FILES.items()
    }
    report = evaluate(truth, documents)
    gate = build_gate(
        report,
        min_call_recall=args.min_call_recall,
        min_resource_recall=args.min_resource_recall,
        min_sync_recall=args.min_sync_recall,
        max_fp=args.max_fp,
        strict_review=args.strict_review,
    )
    if args.project_id:
        root = Path(__file__).resolve().parents[1]
        entry = project_entry(args.project_id)
        project_check = (
            check_project(project_id=args.project_id, root=root)
            if entry.get("paths", {}).get("project")
            else check_legacy_project(entry, root)
        )
        gate["project_check"] = project_check
        if project_check.get("errors"):
            gate["status"] = "failed"
    args.output.mkdir(parents=True, exist_ok=True)
    write(args.output / "report.json", report)
    with (args.output / "report.md").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(markdown(report))
    write(args.output / "gate.json", gate)
    print(
        json.dumps(
            {
                "status": gate["status"],
                "report": str(args.output / "report.md"),
                "gate": str(args.output / "gate.json"),
                "human_review": gate["human_review"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
