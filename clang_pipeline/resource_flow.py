from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from .clang_ast import stable_digest, utc_now


ACQUIRE_RULES = (
    "uv__malloc",
    "uv__strdup",
    "uv__strndup",
    "malloc",
    "calloc",
    "realloc",
    "open",
    "uv__open_cloexec",
    "uv__make_pipe",
    "uv__fs_open",
    "uv__stream_open",
    "dlopen",
    "scandir",
    "uv_getaddrinfo",
)

RELEASE_RULES = (
    "uv__free",
    "free",
    "uv__close",
    "uv__close_nocancel",
    "uv__fs_close",
    "uv__fs_scandir_cleanup",
    "uv_fs_req_cleanup",
    "dlclose",
    "uv_freeaddrinfo",
)

PAIR_RULES = {
    # target function suffix -> expected release function suffix
    "uv__malloc": "uv__free",
    "uv__strdup": "uv__free",
    "uv__strndup": "uv__free",
    "malloc": "free",
    "calloc": "free",
    "realloc": "free",
    "uv__fs_open": "uv__fs_close",
    "uv__open_cloexec": "uv__close",
    "uv__make_pipe": "uv__close",
    "uv__stream_open": "uv__stream_close",
    "dlopen": "dlclose",
    "scandir": "uv__fs_scandir_cleanup",
    "uv_getaddrinfo": "uv_freeaddrinfo",
}

SOURCE_PAIR_RULES = {
    "uv__async_start": "uv__async_stop",
    "uv__getpwuid_r": "uv__getpwuid_r",
    "uv_fs_open": "uv_fs_close",
    "uv_dlopen": "uv_dlclose",
    "uv_getaddrinfo": "uv_freeaddrinfo",
    "uv__fs_scandir": "uv__fs_scandir_cleanup",
}


def _tail(value: str) -> str:
    value = value.split(":")[-1]
    return value.rsplit("::", 1)[-1]


def _node_name(graph: dict[str, Any], node_id: str) -> str:
    for node in graph.get("nodes", []):
        if node.get("id") == node_id:
            return str(node.get("name") or _tail(node_id))
    return _tail(node_id)


def _classify(target: str, source: str, snippet: str) -> tuple[str | None, str]:
    text = " ".join((target, source, snippet)).lower()
    if any(rule in text for rule in RELEASE_RULES):
        return "release", _resource_type(target, snippet)
    if any(rule in text for rule in ACQUIRE_RULES):
        return "acquire", _resource_type(target, snippet)
    return None, "other"


def _resource_type(target: str, snippet: str) -> str:
    text = f"{target} {snippet}".lower()
    if any(item in text for item in ("malloc", "free", "strdup", "realloc", "buffer")):
        return "memory"
    if any(item in text for item in ("dlopen", "dlclose", "lib")):
        return "handle"
    if any(
        item in text
        for item in ("open", "close", "make_pipe", "scandir", "eventfd", "fd")
    ):
        return "file_descriptor"
    return "other"


def _resource_key(snippet: str, fallback: str) -> str:
    text = snippet.strip()
    assignment = re.match(r"^([A-Za-z_][A-Za-z0-9_]*(?:->|\.)[A-Za-z0-9_]+|[A-Za-z_][A-Za-z0-9_]*)\s*=", text)
    if assignment:
        return assignment.group(1)
    arguments = re.search(r"\(([^()]*)\)", text)
    if arguments:
        first = arguments.group(1).split(",", 1)[0].strip()
        if first:
            return first.lstrip("&*").strip()
    return fallback


def _operation(edge: dict[str, Any], graph: dict[str, Any], kind: str) -> dict[str, Any]:
    site = edge.get("call_site") or {}
    target = _node_name(graph, str(edge.get("target", "")))
    source = _node_name(graph, str(edge.get("source", "")))
    snippet = str(site.get("snippet") or "")
    return {
        "operation_id": "op_" + str(edge.get("id", ""))[-10:],
        "kind": kind,
        "api": target,
        "function": source,
        "file": site.get("file", ""),
        "line": int(site.get("line", 0)),
        "snippet": snippet,
        "evidence_ids": list(edge.get("evidence_ids", [])),
        "status": "unconfirmed",
        "confidence": 0.75,
        "_pair_key": _pair_key(source, target),
        "_resource_key": _resource_key(snippet, target),
        "_resource_type": _resource_type(target, snippet),
        "_edge_id": edge.get("id", ""),
    }


def _pair_key(source: str, target: str) -> str:
    if source in SOURCE_PAIR_RULES:
        return f"source:{source}"
    if target in PAIR_RULES:
        return f"target:{target}"
    return f"single:{source}:{target}"


def _public_operation(operation: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in operation.items() if not key.startswith("_")}


def _evidence_map(graph: dict[str, Any], evidence_ids: set[str]) -> list[dict[str, Any]]:
    result = []
    for item in graph.get("evidence", []):
        if item.get("id") in evidence_ids:
            result.append(item)
    return sorted(result, key=lambda item: str(item.get("id", "")))


def analyze_resource_flow(graph: dict[str, Any]) -> dict[str, Any]:
    """Extract resource operations from a Clang-produced evidence graph.

    The first native version is intentionally rule based. It does not claim
    that an unpaired operation is a leak; it emits an incomplete path with a
    termination reason and leaves the final judgement to the consumer.
    """

    operations: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        target = _node_name(graph, str(edge.get("target", "")))
        source = _node_name(graph, str(edge.get("source", "")))
        snippet = str((edge.get("call_site") or {}).get("snippet") or "")
        kind, _ = _classify(target, source, snippet)
        if kind:
            operations.append(_operation(edge, graph, kind))

    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        grouped[
            (
                operation["_pair_key"],
                operation["function"],
                operation["_resource_key"],
            )
        ].append(operation)

    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    referenced_evidence: set[str] = set()
    for (pair_key, function, resource_key), group in sorted(grouped.items()):
        group.sort(key=lambda item: (item["file"], item["line"]))
        acquires = [item for item in group if item["kind"] == "acquire"]
        releases = [item for item in group if item["kind"] == "release"]
        selected: list[dict[str, Any]] = []
        if acquires and releases:
            selected = [acquires[0], releases[-1]]
            complete = True
            termination = "release_found"
        elif acquires:
            selected = [acquires[0]]
            complete = False
            termination = "release_not_found"
        elif releases:
            selected = [releases[0]]
            complete = False
            termination = "acquire_not_found"
        else:
            continue

        for operation in selected:
            referenced_evidence.update(operation["evidence_ids"])
        public_operations = [_public_operation(item) for item in selected]
        item_id = "rf_" + stable_digest(
            [pair_key, function, resource_key, public_operations]
        )[:12]
        items.append(
            {
                "id": item_id,
                "status": "unconfirmed",
                "resource": resource_key,
                "resource_type": selected[0]["_resource_type"],
                "operations": public_operations,
                "owner": function,
                "thread": None,
                "ownership_model": (
                    "visible_acquire_release"
                    if complete
                    else "unresolved_from_visible_graph"
                ),
                "paths": [
                    {
                        "path_id": item_id + "_path",
                        "condition": "visible_graph_path",
                        "operations": [
                            item["operation_id"] for item in public_operations
                        ],
                        "complete": complete,
                        "termination_reason": termination,
                        "evidence_ids": [
                            evidence_id
                            for item in public_operations
                            for evidence_id in item["evidence_ids"]
                        ],
                    }
                ],
                "confidence": 0.8 if complete else 0.35,
                "evidence_ids": [
                    evidence_id
                    for item in public_operations
                    for evidence_id in item["evidence_ids"]
                ],
                "origin": "analyzer",
            }
        )
        if not complete:
            warnings.append(
                f"{item_id}: visible graph has {termination} for {function}:{resource_key}"
            )

    if len(warnings) > 50:
        warnings = warnings[:50] + [
            f"{len(warnings) - 50} additional unresolved resource paths omitted"
        ]
    status = "succeeded" if items and not warnings else ("partial" if items else "not_available")
    return {
        "schema_version": "1.0",
        "run_id": str(graph.get("run_id", "")),
        "result_type": "resource_flow",
        "status": status,
        "generated_at": utc_now(),
        "source": {
            **dict(graph.get("meta") or {}),
            "origin": "analyzer",
            "provider": "native_resource_flow_v1",
        },
        "items": items,
        "evidence": _evidence_map(graph, referenced_evidence),
        "warnings": warnings,
    }
