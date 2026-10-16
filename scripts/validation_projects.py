#!/usr/bin/env python3
"""Reusable operations for repository-specific validation projects.

The evaluation code is repository-independent. A validation project stores the
repository pin, analyzer candidates, the human review table, and the reviewed
ground truth for one C/C++ repository.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "validation" / "projects.json"

PROJECT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
CATEGORY_FILES = {
    "call_chain": "call-chains.json",
    "resource_flow": "resource-flow.json",
    "sync_relation": "sync-relations.json",
}
DECISIONS = {
    "": "",
    "Pending": "",
    "Confirmed": "confirmed",
    "Confirmed with condition": "confirmed",
    "Rejected": "rejected",
    "Needs fix": "",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def normalize_project_id(project_id: str) -> str:
    if not PROJECT_ID_RE.fullmatch(project_id):
        raise ValueError(
            "project id must match [a-z0-9][a-z0-9._-]{0,63}; "
            f"received {project_id!r}"
        )
    return project_id


def load_registry(registry_path: Path | None = None) -> dict[str, Any]:
    path = Path(registry_path or REGISTRY_PATH)
    data = read_json(path)
    if data.get("schema_version") != "1.0" or not isinstance(data.get("projects"), list):
        raise ValueError(f"invalid validation project registry: {path}")
    return data


def save_registry(
    registry: dict[str, Any],
    registry_path: Path | None = None,
) -> None:
    write_json(Path(registry_path or REGISTRY_PATH), registry)


def project_entry(
    project_id: str,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    for project in registry["projects"]:
        if project.get("id") == project_id:
            return project
    raise KeyError(f"validation project is not registered: {project_id}")


def project_dir(
    project_id: str,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> Path:
    entry = project_entry(project_id, registry_path)
    path = entry.get("paths", {}).get("project")
    if not path:
        return root / "validation" / "datasets" / project_id
    path = Path(path)
    return path if path.is_absolute() else root / path


def _relative_project_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _entry_path(root: Path, value: str) -> str:
    path = Path(value)
    return value if path.is_absolute() else _relative_project_path(root / path, root)


def _project_entry(
    *,
    project_id: str,
    name: str,
    repository: str,
    repository_url: str,
    commit: str,
    build_profile: str,
    output: Path,
    root: Path,
) -> dict[str, Any]:
    return {
        "id": project_id,
        "name": name or project_id,
        "repository": repository,
        "repository_url": repository_url,
        "commit": commit,
        "build_profile": build_profile,
        "status": "not_started",
        "human_review": "pending",
        "paths": {
            "project": _entry_path(root, str(output)),
            "manifest": _entry_path(root, str(output / "manifest.json")),
            "source_manifest": _entry_path(root, str(output / "source-manifest.json")),
            "ground_truth": _entry_path(root, str(output / "ground-truth.json")),
            "candidates": _entry_path(root, str(output / "candidates.json")),
            "gold_additions": _entry_path(root, str(output / "gold-additions.json")),
            "review_table": _entry_path(root, str(output / "review-table.csv")),
        },
        "results": _entry_path(root, str(root / "validation" / "results" / project_id)),
    }


def scaffold_project(
    *,
    project_id: str,
    name: str,
    repository: str,
    repository_url: str,
    commit: str = "",
    build_profile: str = "repository-auto",
    source_root: str = "",
    output_dir: str | Path | None = None,
    root: Path = ROOT,
    registry_path: Path | None = None,
    template_path: Path | None = None,
) -> dict[str, Any]:
    project_id = normalize_project_id(project_id)
    output = (
        Path(output_dir).expanduser().resolve()
        if output_dir
        else root / "validation" / "datasets" / project_id
    )
    if output.exists():
        raise FileExistsError(f"validation project already exists: {output}")
    template = Path(template_path or root / "validation" / "templates" / "new-project")
    shutil.copytree(template, output)

    source_root = source_root or f"third_party/{project_id}"
    manifest = {
        "schema_version": "1.0",
        "project_id": project_id,
        "name": name or project_id,
        "repository": repository,
        "repository_url": repository_url,
        "commit": commit,
        "build_profile": build_profile,
        "source_root": source_root,
        "status": "not_started",
        "human_review": "pending",
        "created_at": utc_now(),
        "artifacts": {
            "candidates": "candidates.json",
            "review_table": "review-table.csv",
            "ground_truth": "ground-truth.json",
            "gold_additions": "gold-additions.json",
            "source_manifest": "source-manifest.json",
        },
    }
    source_manifest = {
        "schema_version": "1.0",
        "commit": commit,
        "sha256_lf": {},
    }
    ground_truth = {
        "schema_version": "1.0",
        "dataset_id": f"{project_id}-validation-v1",
        "repository": repository,
        "commit": commit,
        "review": {
            "method": "human_review_of_analyzer_candidates",
            "human_review": "pending",
        },
        "cases": [],
    }
    candidates = {
        "schema_version": "1.0",
        "project_id": project_id,
        "repository": repository,
        "commit": commit,
        "generated_at": utc_now(),
        "facts": [],
    }
    additions = {"schema_version": "1.0", "cases": []}
    write_json(output / "manifest.json", manifest)
    write_json(output / "source-manifest.json", source_manifest)
    write_json(output / "ground-truth.json", ground_truth)
    write_json(output / "candidates.json", candidates)
    write_json(output / "gold-additions.json", additions)
    write_csv(
        output / "review-table.csv",
        [],
        [
            "category",
            "candidate_id",
            "source",
            "target",
            "type",
            "evidence",
            "analyzer_status",
            "confidence",
            "decision",
            "notes",
        ],
    )

    registry = load_registry(registry_path)
    entry = _project_entry(
        project_id=project_id,
        name=name,
        repository=repository,
        repository_url=repository_url,
        commit=commit,
        build_profile=build_profile,
        output=output,
        root=root,
    )
    registry["projects"] = [p for p in registry["projects"] if p.get("id") != project_id]
    registry["projects"].append(entry)
    save_registry(registry, registry_path)
    return {
        "project_id": project_id,
        "project_dir": str(output),
        "review_table": str(output / "review-table.csv"),
        "ground_truth": str(output / "ground-truth.json"),
        "status": "not_started",
    }


def _anchor_value(evidence: dict[str, Any]) -> dict[str, Any]:
    value = evidence.get("location", evidence)
    return {
        "file": str(value.get("file", "")),
        "line": value.get("line"),
        "snippet": str(value.get("snippet", "")),
    }


def _merge_facts(
    facts: list[dict[str, Any]],
    category: str,
    identity: list[Any],
    kind: str,
    *,
    status: str,
    confidence: float,
    evidence: list[dict[str, Any]],
    metadata: dict[str, Any] | None = None,
) -> None:
    key = (category, tuple(identity), kind)
    for fact in facts:
        if (fact["category"], tuple(fact["identity"]), fact["kind"]) == key:
            for item in evidence:
                anchor = _anchor_value(item)
                if anchor not in fact["evidence"]:
                    fact["evidence"].append(anchor)
            if status == "confirmed" or fact["status"] == "unconfirmed":
                fact["status"] = status
            fact["confidence"] = max(fact["confidence"], float(confidence or 0.0))
            return
    facts.append(
        {
            "category": category,
            "identity": list(identity),
            "kind": kind,
            "status": status,
            "confidence": float(confidence or 0.0),
            "evidence": [_anchor_value(item) for item in evidence],
            "metadata": metadata or {},
        }
    )


def _symbol(node: dict[str, Any]) -> str:
    return str(node.get("symbol") or node.get("id") or node.get("name") or "")


def _relativize_file(
    file: str,
    source_root: Path | None,
    configured_root: str | None = None,
) -> tuple[str, str]:
    raw = str(file)
    if not raw:
        return raw, "missing file"
    if configured_root:
        prefix = str(configured_root).replace("\\", "/").rstrip("/")
        if prefix and raw.replace("\\", "/").startswith(prefix + "/"):
            raw = raw[len(prefix) + 1 :]
    path = Path(raw)
    if source_root is None or not source_root.exists():
        return raw, ""
    source_root = source_root.resolve()
    try:
        candidate = path.resolve()
        if candidate.is_relative_to(source_root):
            return candidate.relative_to(source_root).as_posix(), ""
    except OSError:
        pass
    direct = source_root / path
    if direct.is_file():
        return path.as_posix(), ""
    matches = list(source_root.rglob(path.name))
    if len(matches) == 1:
        return matches[0].relative_to(source_root).as_posix(), "relativized by unique basename"
    return raw, "unable to map evidence file to configured source root"


def collect_candidates(
    *,
    project_id: str,
    predictions_dir: str | Path,
    limit: int = 100,
    source_root: str | Path | None = None,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    entry = project_entry(project_id, registry_path)
    project = project_dir(project_id, root, registry_path)
    manifest = read_json(project / "manifest.json")
    predictions = Path(predictions_dir)
    configured_root = source_root or manifest.get("source_root")
    source_root_path = (
        Path(configured_root).resolve()
        if configured_root
        and (Path(configured_root).is_absolute() or (root / str(configured_root)).exists())
        else None
    )
    warnings: list[str] = []
    facts: list[dict[str, Any]] = []
    sources: set[tuple[str, str]] = set()

    for category, filename in CATEGORY_FILES.items():
        path = predictions / filename
        if not path.is_file():
            warnings.append(f"missing prediction file: {path}")
            continue
        doc = read_json(path)
        if doc.get("result_type") != category:
            warnings.append(f"prediction result_type mismatch for {filename}")
        source = doc.get("source", {})
        sources.add((str(source.get("repository", "")), str(source.get("commit", ""))))
        evidence = {str(item.get("id", "")): item for item in doc.get("evidence", [])}
        if category == "call_chain":
            for item in doc.get("items", []):
                nodes = {str(node.get("id", "")): node for node in item.get("nodes", [])}
                for edge in item.get("edges", []):
                    source_id = str(edge.get("source", ""))
                    target_id = str(edge.get("target", ""))
                    anchors = []
                    for evidence_id in edge.get("evidence_ids", []):
                        item_evidence = evidence.get(str(evidence_id))
                        if item_evidence is not None:
                            anchors.append(item_evidence)
                    if not anchors:
                        warnings.append(f"edge without evidence: {edge.get('id')}")
                        continue
                    _merge_facts(
                        facts,
                        "call_chain",
                        [_symbol(nodes.get(source_id, {"id": source_id})),
                         _symbol(nodes.get(target_id, {"id": target_id}))],
                        str(edge.get("kind", "")),
                        status=str(edge.get("status", item.get("status", "unconfirmed"))),
                        confidence=edge.get("confidence", item.get("confidence", 0.0)),
                        evidence=anchors,
                    )
        elif category == "resource_flow":
            for item in doc.get("items", []):
                resource_id = str(item.get("resource", ""))
                for operation in item.get("operations", []):
                    anchors = [
                        evidence[str(evidence_id)]
                        for evidence_id in operation.get("evidence_ids", [])
                        if str(evidence_id) in evidence
                    ]
                    if not anchors:
                        warnings.append(f"resource operation without evidence: {operation.get('id')}")
                        continue
                    operation_file, file_warning = _relativize_file(
                        operation.get("file", ""),
                        source_root_path,
                        configured_root=configured_root,
                    )
                    if file_warning:
                        warnings.append(
                            f"{operation.get('id')}: {file_warning}: "
                            f"{operation.get('file')}"
                        )
                    _merge_facts(
                        facts,
                        "resource_flow",
                        [
                            resource_id,
                            str(operation.get("function", "")),
                            operation_file,
                            operation.get("line"),
                        ],
                        str(operation.get("kind", "")),
                        status=str(operation.get("status", item.get("status", "unconfirmed"))),
                        confidence=operation.get("confidence", item.get("confidence", 0.0)),
                        evidence=anchors,
                    )
        else:
            for item in doc.get("items", []):
                source_endpoint = item.get("source", {})
                target_endpoint = item.get("target", {})
                anchors = [
                    evidence[str(evidence_id)]
                    for evidence_id in item.get("evidence_ids", [])
                    if str(evidence_id) in evidence
                ]
                if not anchors:
                    warnings.append(f"sync relation without evidence: {item.get('id')}")
                    continue
                source_file, source_warning = _relativize_file(
                    source_endpoint.get("file", ""),
                    source_root_path,
                    configured_root=configured_root,
                )
                target_file, target_warning = _relativize_file(
                    target_endpoint.get("file", ""),
                    source_root_path,
                    configured_root=configured_root,
                )
                if source_warning:
                    warnings.append(f"{item.get('id')}: {source_warning}: {source_endpoint.get('file')}")
                if target_warning:
                    warnings.append(f"{item.get('id')}: {target_warning}: {target_endpoint.get('file')}")
                _merge_facts(
                    facts,
                    "sync_relation",
                    [
                        str(source_endpoint.get("function", "")),
                        str(target_endpoint.get("function", "")),
                        source_file,
                        source_endpoint.get("line"),
                        target_file,
                        target_endpoint.get("line"),
                    ],
                    str(item.get("order", "")),
                    status=str(item.get("status", "unconfirmed")),
                    confidence=item.get("confidence", 0.0),
                    evidence=anchors,
                    metadata={"condition": item.get("condition", "")},
                )

    facts.sort(key=lambda fact: (fact["category"], str(fact["identity"]), fact["kind"]))
    for repository, commit in sorted(sources):
        if not repository and not commit:
            continue
        if repository != manifest.get("repository") or (
            manifest.get("commit") and commit != manifest.get("commit")
        ):
            warnings.append(
                "prediction source does not match validation project: "
                f"prediction={repository}@{commit}, project="
                f"{manifest.get('repository')}@{manifest.get('commit')}"
            )
    kept: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for fact in facts:
        category = fact["category"]
        if limit and counts.get(category, 0) >= limit:
            continue
        counts[category] = counts.get(category, 0) + 1
        prefix = {"call_chain": "cc", "resource_flow": "rf", "sync_relation": "sync"}[category]
        digest = hashlib.sha1(
            json.dumps(
                [category, fact["identity"], fact["kind"]],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()[:12]
        fact["id"] = f"{prefix}_{digest}"
        for anchor in fact["evidence"]:
            file, warning = _relativize_file(
                anchor["file"],
                source_root_path,
                configured_root=configured_root,
            )
            anchor["file"] = file
            if warning:
                warnings.append(f"{fact['id']}: {warning}: {anchor['file']}")
        kept.append(fact)

    total = {category: sum(1 for item in facts if item["category"] == category)
             for category in CATEGORY_FILES}
    candidates = {
        "schema_version": "1.0",
        "project_id": project_id,
        "repository": manifest.get("repository", ""),
        "commit": manifest.get("commit", ""),
        "generated_at": utc_now(),
        "prediction_sources": sorted(
            {"repository": repository, "commit": commit} for repository, commit in sources
        ),
        "limit_per_category": limit or None,
        "truncated": any(total.get(category, 0) > counts.get(category, 0) for category in total),
        "facts": kept,
    }
    rows = []
    for fact in kept:
        identity = fact["identity"]
        if fact["category"] == "call_chain":
            source, target = str(identity[0]), str(identity[1])
        elif fact["category"] == "resource_flow":
            source = str(identity[0])
            target = f"{identity[1]}@{identity[2]}:{identity[3]}"
        else:
            source, target = str(identity[0]), str(identity[1])
        evidence_cells = [
            f"{anchor['file']}:{anchor['line']}"
            for anchor in fact["evidence"]
        ]
        if len(evidence_cells) > 3:
            evidence_cells = evidence_cells[:3] + [
                f"+{len(evidence_cells) - 3} more"
            ]
        rows.append(
            {
                "category": fact["category"],
                "candidate_id": fact["id"],
                "source": source,
                "target": target,
                "type": fact["kind"],
                "evidence": "; ".join(evidence_cells),
                "analyzer_status": fact["status"],
                "confidence": f"{fact['confidence']:.2f}",
                "decision": "Pending",
                "notes": "",
            }
        )
    write_json(project / "candidates.json", candidates)
    write_csv(
        project / "review-table.csv",
        rows,
        [
            "category",
            "candidate_id",
            "source",
            "target",
            "type",
            "evidence",
            "analyzer_status",
            "confidence",
            "decision",
            "notes",
        ],
    )
    manifest["status"] = "candidates_collected"
    manifest["human_review"] = "pending"
    write_json(project / "manifest.json", manifest)
    entry["status"] = "candidates_collected"
    entry["human_review"] = "pending"
    registry = load_registry(registry_path)
    for index, registered in enumerate(registry["projects"]):
        if registered.get("id") == project_id:
            registry["projects"][index] = entry
            break
    save_registry(registry, registry_path)
    return {
        "project_id": project_id,
        "candidates": {category: counts.get(category, 0) for category in CATEGORY_FILES},
        "total_candidates": len(kept),
        "truncated": candidates["truncated"],
        "review_table": str(project / "review-table.csv"),
        "warnings": warnings,
    }


def _normalize_decision(decision: str) -> str:
    normalized = DECISIONS.get(decision.strip())
    if normalized is None:
        raise ValueError(
            f"unsupported decision {decision!r}; expected Confirmed, "
            "Confirmed with condition, Rejected, Needs fix, or Pending"
        )
    return normalized


def _case_from_fact(
    fact: dict[str, Any],
    *,
    expected_exists: bool,
    notes: str,
) -> dict[str, Any]:
    evidence = []
    for anchor in fact["evidence"]:
        evidence_id = (
            f"{fact['id']}_ev_{len(evidence) + 1}"
        )
        if not anchor.get("file") or not anchor.get("line") or not anchor.get("snippet"):
            raise ValueError(f"candidate {fact['id']} has incomplete evidence")
        evidence.append({**anchor, "id": evidence_id})
    condition = fact.get("metadata", {}).get("condition", "")
    case = {
        "id": fact["id"],
        "category": fact["category"],
        "identity": fact["identity"],
        "kind": fact["kind"],
        "expected_exists": expected_exists,
        "evidence": evidence,
        "notes": notes,
    }
    if condition:
        case["condition"] = condition
    return case


def build_ground_truth(
    *,
    project_id: str,
    review_table: str | Path | None = None,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    entry = project_entry(project_id, registry_path)
    project = project_dir(project_id, root, registry_path)
    manifest = read_json(project / "manifest.json")
    candidates = read_json(project / "candidates.json")
    table_path = Path(review_table or project / "review-table.csv")
    rows = read_csv(table_path)
    decisions: dict[str, str] = {}
    notes: dict[str, str] = {}
    for row in rows:
        candidate_id = row.get("candidate_id", "").strip()
        if not candidate_id:
            continue
        decision = _normalize_decision(row.get("decision", ""))
        if candidate_id in decisions and decisions[candidate_id] != decision:
            raise ValueError(f"conflicting review decisions for {candidate_id}")
        decisions[candidate_id] = decision
        notes[candidate_id] = row.get("notes", "").strip()

    cases: list[dict[str, Any]] = []
    reviewed_count = 0
    for fact in candidates.get("facts", []):
        decision = decisions.get(fact["id"], "")
        if decision in {"", "Needs fix"}:
            continue
        reviewed_count += 1
        cases.append(
            _case_from_fact(
                fact,
                expected_exists=decision == "confirmed",
                notes=notes.get(fact["id"], ""),
            )
        )
    additions = read_json(project / "gold-additions.json")
    for case in additions.get("cases", []):
        if case.get("id") in {item["id"] for item in cases}:
            raise ValueError(f"gold addition duplicates candidate case: {case.get('id')}")
        cases.append(case)
    if not cases:
        raise ValueError("review table contains no Confirmed or Rejected decision")
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("ground truth contains duplicate case IDs")

    pending = sum(
        1
        for fact in candidates.get("facts", [])
        if decisions.get(fact["id"], "") in {"", "Needs fix"}
    )
    human_review = "confirmed" if pending == 0 else "partial"
    ground_truth = {
        "schema_version": "1.0",
        "dataset_id": f"{project_id}-validation-v1",
        "repository": manifest.get("repository", ""),
        "commit": manifest.get("commit", ""),
        "review": {
            "method": "human_review_of_analyzer_candidates",
            "human_review": human_review,
            "review_table": (
                table_path.resolve().relative_to(project.resolve()).as_posix()
                if table_path.resolve().is_relative_to(project.resolve())
                else table_path.name
            ),
            "reviewed_candidates": reviewed_count,
            "pending_candidates": pending,
        },
        "cases": cases,
    }
    write_json(project / "ground-truth.json", ground_truth)
    manifest["status"] = "ready" if human_review == "confirmed" else "in_review"
    manifest["human_review"] = human_review
    write_json(project / "manifest.json", manifest)
    entry["status"] = manifest["status"]
    entry["human_review"] = human_review
    registry = load_registry(registry_path)
    for index, registered in enumerate(registry["projects"]):
        if registered.get("id") == project_id:
            registry["projects"][index] = entry
            break
    save_registry(registry, registry_path)
    return {
        "project_id": project_id,
        "ground_truth": str(project / "ground-truth.json"),
        "cases": len(cases),
        "reviewed_candidates": reviewed_count,
        "pending_candidates": pending,
        "human_review": human_review,
        "status": manifest["status"],
    }


def _resolve_source_root(manifest: dict[str, Any], root: Path) -> Path | None:
    value = manifest.get("source_root")
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path if path.exists() else None
    return root / path if (root / path).exists() else None


def pin_validation_sources(
    *,
    project_id: str,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    project = project_dir(project_id, root, registry_path)
    manifest = read_json(project / "manifest.json")
    source_root = _resolve_source_root(manifest, root)
    if source_root is None:
        raise FileNotFoundError(
            f"configured source root is unavailable: {manifest.get('source_root')}"
        )
    files: set[Path] = set()
    for filename in ("candidates.json", "ground-truth.json", "gold-additions.json"):
        data = read_json(project / filename)
        candidates = data.get("facts", []) if filename == "candidates.json" else data.get("cases", [])
        for fact in candidates:
            for evidence in fact.get("evidence", []):
                file = str(evidence.get("file", ""))
                path = source_root / file
                if path.is_file():
                    files.add(path.resolve())
    hashes: dict[str, str] = {}
    for path in sorted(files):
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        hashes[path.relative_to(source_root.resolve()).as_posix()] = hashlib.sha256(raw).hexdigest()
    source_manifest = {
        "schema_version": "1.0",
        "commit": manifest.get("commit", ""),
        "sha256_lf": hashes,
    }
    write_json(project / "source-manifest.json", source_manifest)
    return {
        "project_id": project_id,
        "source_root": str(source_root),
        "source_files": len(hashes),
        "source_manifest": str(project / "source-manifest.json"),
    }


def _validate_ready_truth(truth: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    if truth.get("schema_version") != "1.0" or not isinstance(truth.get("cases"), list):
        return ["invalid ground-truth envelope"]
    if not truth["cases"]:
        return []
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema is required to validate ready ground truth"]
    schema = read_json(root / "schemas" / "validation-benchmark.schema.json")
    errors.extend(
        f"ground-truth schema {list(error.absolute_path)}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(truth)
    )
    commit = str(truth.get("commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append("ready ground truth requires a 40-character git commit")
    return errors


def _evidence_source_errors(
    cases: list[dict[str, Any]],
    source_root: Path | None,
    root: Path,
) -> list[str]:
    errors: list[str] = []
    cache: dict[str, list[str]] = {}
    for case in cases:
        for evidence in case.get("evidence", []):
            file = str(evidence.get("file", ""))
            line = evidence.get("line")
            snippet = str(evidence.get("snippet", ""))
            candidates = []
            if source_root is not None:
                candidates.append(source_root / file)
            candidates.append(root / file)
            path = next((item for item in candidates if item.is_file()), None)
            if path is None:
                errors.append(f"{case.get('id')}: missing evidence source: {file}")
                continue
            if file not in cache:
                cache[file] = path.read_text(encoding="utf-8", errors="replace").splitlines()
            lines = cache[file]
            if not isinstance(line, int) or not 1 <= line <= len(lines):
                errors.append(f"{case.get('id')}: evidence line out of range: {file}:{line}")
            elif " ".join(lines[line - 1].split()) != " ".join(snippet.split()):
                errors.append(f"{case.get('id')}: evidence snippet mismatch: {file}:{line}")
    return errors


def check_project(
    *,
    project_id: str,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    entry = project_entry(project_id, registry_path)
    errors: list[str] = []
    warnings: list[str] = []
    project = project_dir(project_id, root, registry_path)
    manifest = read_json(project / "manifest.json")
    if manifest.get("project_id") != project_id:
        errors.append("manifest project_id does not match registry")
    for key in (
        "schema_version",
        "project_id",
        "repository",
        "repository_url",
        "source_root",
        "status",
        "human_review",
    ):
        if not manifest.get(key):
            errors.append(f"manifest is missing {key}")
    source_manifest = read_json(project / "source-manifest.json")
    if source_manifest.get("commit") != manifest.get("commit"):
        errors.append("source-manifest commit differs from manifest")
    ground_truth = read_json(project / "ground-truth.json")
    if not ground_truth.get("cases"):
        warnings.append("ground truth is empty; human review has not produced Gold yet")
    else:
        errors.extend(_validate_ready_truth(ground_truth, root))
        source_root = _resolve_source_root(manifest, root)
        if source_root is not None and (source_root / ".git").exists():
            git = subprocess.run(
                ["git", "-C", str(source_root), "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
            )
            if git.returncode or git.stdout.strip() != manifest.get("commit"):
                errors.append("source checkout HEAD does not match manifest commit")
        errors.extend(
            _evidence_source_errors(ground_truth["cases"], source_root, root)
        )
        hashes = source_manifest.get("sha256_lf", {})
        if hashes and source_root is not None:
            for file, expected in hashes.items():
                path = source_root / file
                if not path.is_file():
                    errors.append(f"missing hashed source: {file}")
                    continue
                raw = path.read_bytes().replace(b"\r\n", b"\n")
                if hashlib.sha256(raw).hexdigest() != expected:
                    errors.append(f"source hash mismatch: {file}")
        elif hashes and source_root is None:
            errors.append("source hashes cannot be verified because source root is unavailable")
        elif not hashes:
            warnings.append("source hashes are not pinned")
    if manifest.get("human_review") == "confirmed" and not ground_truth.get("cases"):
        errors.append("manifest claims human review confirmed but ground truth is empty")
    if manifest.get("status") == "ready" and (
        manifest.get("human_review") != "confirmed" or not ground_truth.get("cases")
    ):
        errors.append("project is marked ready without confirmed non-empty Gold")
    return {
        "project_id": project_id,
        "name": entry.get("name", project_id),
        "status": "failed" if errors else "passed",
        "project_status": manifest.get("status", "unknown"),
        "human_review": manifest.get("human_review", "pending"),
        "cases": len(ground_truth.get("cases", [])),
        "errors": errors,
        "warnings": warnings,
    }


def check_legacy_project(entry: dict[str, Any], root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    paths = [
        value
        for value in entry.get("datasets", {}).values()
        if isinstance(value, str)
    ]
    if not paths:
        errors.append("legacy project has no dataset paths")
    counts: dict[str, int] = {}
    for value in paths:
        path = Path(value)
        if not path.is_absolute():
            path = root / path
        if not path.is_file():
            errors.append(f"missing dataset: {value}")
            continue
        try:
            data = read_json(path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid dataset JSON {value}: {exc}")
            continue
        count = len(data.get("samples", data.get("resources", data.get("cases", []))))
        counts[path.name] = count
    results = entry.get("results")
    if results and not (Path(results) if Path(results).is_absolute() else root / results).exists():
        warnings.append(f"results directory is not available: {results}")
    warnings.append("legacy project is pending human review unless all pending labels are resolved")
    return {
        "project_id": entry.get("id", "<missing>"),
        "name": entry.get("name", entry.get("id", "<missing>")),
        "status": "failed" if errors else "passed",
        "project_status": entry.get("status", "legacy_pending_review"),
        "human_review": entry.get("human_review", "pending"),
        "cases": sum(counts.values()),
        "errors": errors,
        "warnings": warnings,
    }


def check_registry(
    *,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    ids = [project.get("id") for project in registry["projects"]]
    errors: list[str] = []
    if any(not item for item in ids):
        errors.append("project entry is missing an id")
    if len(ids) != len(set(ids)):
        errors.append("duplicate project id in registry")
    reports = []
    for project in registry["projects"]:
        project_id = project.get("id")
        if not project_id:
            reports.append(
                {
                    "project_id": "<missing>",
                    "status": "failed",
                    "errors": ["missing project id"],
                    "warnings": [],
                }
            )
            continue
        try:
            if project.get("paths", {}).get("project"):
                reports.append(check_project(project_id=project_id, root=root, registry_path=registry_path))
            else:
                reports.append(check_legacy_project(project, root))
        except (OSError, ValueError, KeyError, AttributeError, TypeError) as exc:
            reports.append(
                {
                    "project_id": project_id,
                    "status": "failed",
                    "errors": [str(exc)],
                    "warnings": [],
                }
            )
    project_errors = [error for report in reports for error in report.get("errors", [])]
    return {
        "schema_version": "1.0",
        "registry": str(Path(registry_path or REGISTRY_PATH)),
        "projects": reports,
        "errors": errors + project_errors,
        "status": "failed" if errors or project_errors else "passed",
    }
