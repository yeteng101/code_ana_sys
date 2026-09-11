#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str) -> str:
    return " ".join(text.split())


def check_dataset(dataset: Path) -> tuple[dict, list[str]]:
    data = json.loads(dataset.read_text(encoding="utf-8"))
    errors: list[str] = []
    resources = data.get("resources", [])
    ids: set[str] = set()
    classifications = {"no_leak": 0, "leak": 0, "uncertain": 0}
    for resource in resources:
        resource_id = resource.get("id", "<missing>")
        if resource_id in ids:
            errors.append(f"{resource_id}: 重复 resource ID")
        ids.add(resource_id)
        classification = resource.get("ground_truth", {}).get("classification")
        if classification in classifications:
            classifications[classification] += 1
        operations = resource.get("operations", [])
        operation_ids = [item.get("operation_id", "") for item in operations]
        if len(operation_ids) != len(set(operation_ids)):
            errors.append(f"{resource_id}: operation_id 重复")
        evidence_ids = {
            item.get("id")
            for item in resource.get("evidence", [])
            if item.get("id")
        }
        for operation in operations:
            for evidence_id in operation.get("evidence_ids", []):
                if evidence_id not in evidence_ids:
                    errors.append(
                        f"{resource_id}: operation {operation.get('operation_id')} "
                        f"引用不存在的 evidence {evidence_id}"
                    )
            location = operation.get("location", {})
            source = ROOT / location.get("file", "")
            if source.exists():
                lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
                line = int(location.get("line", 0))
                if not 1 <= line <= len(lines):
                    errors.append(f"{resource_id}: operation 行号越界 {location}")
                elif normalize(lines[line - 1]) != normalize(location.get("snippet", "")):
                    errors.append(
                        f"{resource_id}: operation snippet 不匹配 {location.get('file')}:{line}"
                    )
        for path in resource.get("paths", []):
            for operation_id in path.get("operations", []):
                if operation_id not in operation_ids:
                    errors.append(
                        f"{resource_id}: path {path.get('path_id')} 引用不存在的 operation {operation_id}"
                    )
            for evidence_id in path.get("evidence_ids", []):
                if evidence_id not in evidence_ids:
                    errors.append(
                        f"{resource_id}: path {path.get('path_id')} 引用不存在的 evidence {evidence_id}"
                    )
        if classification == "leak":
            has_missing_release = any(
                path.get("complete") is False
                and path.get("termination_reason") == "release_not_found"
                for path in resource.get("paths", [])
            )
            if not has_missing_release:
                errors.append(f"{resource_id}: leak 样本缺少 release_not_found 路径")

    return {
        "dataset": str(dataset),
        "resources": len(resources),
        "no_leak": classifications["no_leak"],
        "leak": classifications["leak"],
        "uncertain": classifications["uncertain"],
        "errors": errors,
        "status": "verified" if not errors else "failed",
    }, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验资源流和泄漏标注数据集")
    parser.add_argument("--dataset", default="validation/resource-flow/dataset.json")
    args = parser.parse_args()
    dataset = (
        Path(args.dataset)
        if Path(args.dataset).is_absolute()
        else (ROOT / args.dataset).resolve()
    )
    summary, errors = check_dataset(dataset)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
