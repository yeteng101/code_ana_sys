#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_graph_edges(paths: list[Path]) -> set[tuple[str, str, str]]:
    edges: set[tuple[str, str, str]] = set()
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for edge in data.get("edges", []):
            edges.add((edge.get("source", ""), edge.get("target", ""), edge.get("kind", "")))
    return edges


def normalize(text: str) -> str:
    return " ".join(text.split())


def check_dataset(dataset: Path, graphs: list[Path]) -> tuple[dict, list[str]]:
    data = json.loads(dataset.read_text(encoding="utf-8"))
    edge_set = load_graph_edges(graphs)
    errors: list[str] = []
    ids: set[str] = set()
    samples = data.get("samples", [])
    for sample in samples:
        sample_id = sample.get("id", "<missing>")
        if sample_id in ids:
            errors.append(f"{sample_id}: 重复 ID")
        ids.add(sample_id)
        label = sample.get("label")
        expected = sample.get("expected_exists")
        if (label == "positive") != bool(expected):
            errors.append(f"{sample_id}: label={label} 与 expected_exists={expected} 不一致")
        claim = sample.get("claim") or {}
        key = (claim.get("source", ""), claim.get("target", ""), claim.get("kind", ""))
        exists = key in edge_set
        if exists != bool(expected):
            errors.append(
                f"{sample_id}: 图校验不一致，expected_exists={expected}, actual_exists={exists}, "
                f"claim={key}"
            )
        for evidence in sample.get("evidence", []):
            source = ROOT / evidence["file"]
            if not source.exists():
                continue
            lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
            line = int(evidence["line"])
            if not 1 <= line <= len(lines):
                errors.append(f"{sample_id}: evidence 行号越界 {evidence['file']}:{line}")
            elif normalize(lines[line - 1]) != normalize(evidence["snippet"]):
                errors.append(
                    f"{sample_id}: evidence 片段不匹配 {evidence['file']}:{line}"
                )

    summary = {
        "dataset": str(dataset),
        "graphs": [str(path) for path in graphs],
        "samples": len(samples),
        "positive": sum(1 for item in samples if item.get("label") == "positive"),
        "negative": sum(1 for item in samples if item.get("label") == "negative"),
        "uncertain": sum(1 for item in samples if item.get("label") == "uncertain"),
        "errors": errors,
        "status": "verified" if not errors else "failed",
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验调用链验证集正负样本")
    parser.add_argument("--dataset", default="validation/call-chains/dataset.json")
    parser.add_argument("--graph", action="append", default=[])
    args = parser.parse_args()
    dataset = (ROOT / args.dataset).resolve() if not Path(args.dataset).is_absolute() else Path(args.dataset)
    graph_paths = [
        (ROOT / item).resolve() if not Path(item).is_absolute() else Path(item)
        for item in args.graph
    ]
    summary, errors = check_dataset(dataset, graph_paths)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
