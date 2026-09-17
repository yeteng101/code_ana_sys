#!/usr/bin/env python3
"""Validate curated synchronization annotations; never infer labels from graphs."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/sync-validation.schema.json"
REQUIRED_TYPES = {"mutex_lock", "rwlock", "atomic", "condition_variable",
                  "event_wait", "event_notify", "thread_join", "happens_before"}


def check_dataset(dataset: Path, root: Path = ROOT) -> tuple[dict, list[str]]:
    errors: list[str] = []
    summary = {"samples": 0, "orders": {}, "labels": {}, "relation_types": {}}
    try:
        data = json.loads(dataset.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        errors.extend(f"schema {list(e.absolute_path)}: {e.message}"
                      for e in Draft202012Validator(schema).iter_errors(data))
        if errors:
            return {**summary, "status": "failed", "errors": errors}, errors
        source_root = (root / "third_party/libuv").resolve()
        result = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode or result.stdout.strip() != data["commit"]:
            errors.append("libuv checkout missing or HEAD does not match pinned commit")
        sources = {}
        for name, expected in data["source_files"].items():
            path = (root / name).resolve()
            if not path.is_relative_to(source_root):
                errors.append(f"source outside pinned checkout: {name}")
                continue
            if not path.is_file():
                errors.append(f"missing source: {name}")
                continue
            raw = path.read_bytes().replace(b"\r\n", b"\n")
            if hashlib.sha256(raw).hexdigest() != expected:
                errors.append(f"source hash mismatch: {name}")
            sources[name] = raw.decode("utf-8").splitlines()
        ids = set()
        for sample in data["samples"]:
            sid = sample["id"]
            if sid in ids:
                errors.append(f"duplicate sample ID: {sid}")
            ids.add(sid)
            evidence = {}
            for item in sample["evidence"]:
                eid = item["id"]
                if eid in evidence:
                    errors.append(f"{sid}: duplicate evidence ID: {eid}")
                evidence[eid] = item
                lines = sources.get(item["file"])
                if lines is None:
                    errors.append(f"{sid}: unverified evidence file: {item['file']}")
                elif not 1 <= item["line"] <= len(lines):
                    errors.append(f"{sid}: evidence line out of range")
                elif lines[item["line"] - 1].strip() != item["snippet"].strip():
                    errors.append(f"{sid}: evidence snippet mismatch: {eid}")
            for endpoint in (sample["source"], sample["target"]):
                for eid in endpoint["evidence_ids"]:
                    if eid not in evidence:
                        errors.append(f"{sid}: dangling evidence reference: {eid}")
                if not any(evidence[eid]["snippet"] == endpoint["operation"]
                           for eid in endpoint["evidence_ids"] if eid in evidence):
                    errors.append(f"{sid}: operation missing matching evidence")
            equal = sample["claim_order"] == sample["order"]
            if sample["label"] == "positive" and (not equal or sample["order"] == "unknown"):
                errors.append(f"{sid}: positive label requires a supported known order")
            if sample["label"] == "negative" and equal:
                errors.append(f"{sid}: negative label must reject the claimed order")
            if sample["label"] == "uncertain" and sample["order"] != "unknown":
                errors.append(f"{sid}: uncertain label requires unknown order")
            expected = ("unknown" if sample["order"] == "unknown" else
                        "inconsistent" if sample["label"] == "negative" else "consistent")
            if sample["classification"] != expected:
                errors.append(f"{sid}: inconsistent classification")
        summary = {"dataset_id": data["dataset_id"], "commit": data["commit"],
                   "review": data["review"], "check_scope": "schema_and_source_integrity",
                   "samples": len(data["samples"]),
                   "orders": dict(Counter(s["order"] for s in data["samples"])),
                   "labels": dict(Counter(s["label"] for s in data["samples"])),
                   "relation_types": dict(Counter(s["relation_type"] for s in data["samples"]))}
        if REQUIRED_TYPES - summary["relation_types"].keys():
            errors.append("missing required synchronization primitive coverage")
        if {"happens_before", "concurrent", "unknown"} - summary["orders"].keys():
            errors.append("missing required order coverage")
        if summary["labels"].get("negative", 0) < 3:
            errors.append("at least three negative claims required")
    except (OSError, ValueError) as exc:
        errors.append(f"input error: {exc}")
    return {**summary, "status": "failed" if errors else "verified", "errors": errors}, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=ROOT / "validation/sync-relations/dataset.json")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    summary, errors = check_dataset(args.dataset)
    text = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    print(text, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8", newline="\n")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
