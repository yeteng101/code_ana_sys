from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from .clang_ast import stable_digest, utc_now


ACQUIRE_TARGETS = frozenset(
    {
        "uv__malloc",
        "uv__strdup",
        "uv__strndup",
        "malloc",
        "calloc",
        "realloc",
        "uv__calloc",
        "uv__realloc",
        "uv__reallocf",
        "open",
        "uv__open_cloexec",
        "uv__make_pipe",
        "uv__fs_open",
        "uv__stream_open",
        "dlopen",
        "scandir",
        "getaddrinfo",
        "uv_getaddrinfo",
        "uv__fs_opendir",
        "zmalloc",
        "zcalloc",
        "zrealloc",
        "ztrymalloc",
        "ztrycalloc",
        "ztryrealloc",
        "sdsnew",
        "sdsnewlen",
        "sdsempty",
        "sdsdup",
    }
)

RELEASE_TARGETS = frozenset(
    {
        "uv__free",
        "free",
        "close",
        "uv__close",
        "uv__close_nocancel",
        "uv__close_nocheckstdio",
        "uv__fs_close",
        "uv__fs_closedir",
        "uv__fs_scandir_cleanup",
        "uv__fs_scandir_free",
        "uv_fs_req_cleanup",
        "dlclose",
        "uv_freeaddrinfo",
        "freeaddrinfo",
        "closedir",
        "zfree",
        "sdsfree",
        "sdsfreesplitres",
    }
)

MEMORY_TARGETS = frozenset(
    {
        "uv__malloc",
        "uv__strdup",
        "uv__strndup",
        "malloc",
        "calloc",
        "realloc",
        "uv__calloc",
        "uv__realloc",
        "uv__reallocf",
        "uv__free",
        "free",
        "scandir",
        "getaddrinfo",
        "uv_freeaddrinfo",
        "freeaddrinfo",
        "zmalloc",
        "zcalloc",
        "zrealloc",
        "ztrymalloc",
        "ztrycalloc",
        "ztryrealloc",
        "zfree",
        "sdsnew",
        "sdsnewlen",
        "sdsempty",
        "sdsdup",
        "sdsfree",
        "sdsfreesplitres",
    }
)

FILE_DESCRIPTOR_TARGETS = frozenset(
    {
        "open",
        "close",
        "uv__open_cloexec",
        "uv__make_pipe",
        "uv__fs_open",
        "uv__stream_open",
        "uv__close",
        "uv__close_nocancel",
        "uv__close_nocheckstdio",
        "uv__fs_close",
        "uv__fs_closedir",
        "uv__fs_opendir",
        "uv__stream_close",
        "closedir",
    }
)

HANDLE_TARGETS = frozenset({"dlopen", "dlclose"})

SOURCE_RESOURCE_IDS = {
    "uv__fs_open": "rf_libuv_fs_fd_v1",
    "uv__fs_close": "rf_libuv_fs_fd_v1",
    "uv__getpwuid_r": "rf_libuv_getpwuid_buf_v1",
    "uv__async_start": "rf_libuv_async_fd_v1",
    "uv__async_stop": "rf_libuv_async_fd_v1",
    "uv_freeaddrinfo": "rf_libuv_getaddrinfo_v1",
    "uv__fs_scandir": "rf_libuv_scandir_entries_v1",
    "uv__fs_scandir_cleanup": "rf_libuv_scandir_entries_v1",
    "uv_dlopen": "rf_libuv_dlopen_handle_v1",
    "uv_dlclose": "rf_libuv_dlopen_handle_v1",
}

TARGET_RESOURCE_IDS = {
    "uv__fs_close": "rf_libuv_fs_fd_v1",
    "uv__fs_opendir": "rf_libuv_fs_fd_v1",
    "uv__fs_scandir_cleanup": "rf_libuv_scandir_entries_v1",
    "uv__fs_scandir_free": "rf_libuv_scandir_entries_v1",
    "dlclose": "rf_libuv_dlopen_handle_v1",
    "dlopen": "rf_libuv_dlopen_handle_v1",
    "scandir": "rf_libuv_scandir_entries_v1",
    "getaddrinfo": "rf_libuv_getaddrinfo_v1",
    "uv_freeaddrinfo": "rf_libuv_getaddrinfo_v1",
    "freeaddrinfo": "rf_libuv_getaddrinfo_v1",
}

RESOURCE_TYPES = {
    "rf_libuv_fs_fd_v1": "file_descriptor",
    "rf_libuv_getpwuid_buf_v1": "memory",
    "rf_libuv_async_fd_v1": "file_descriptor",
    "rf_libuv_getaddrinfo_v1": "memory",
    "rf_libuv_scandir_entries_v1": "memory",
    "rf_libuv_dlopen_handle_v1": "handle",
}

PAIR_RULES = {
    # target function suffix -> expected release function suffix
    "uv__malloc": "uv__free",
    "uv__strdup": "uv__free",
    "uv__strndup": "uv__free",
    "malloc": "free",
    "calloc": "free",
    "realloc": "free",
    "open": "close",
    "uv__fs_open": "uv__fs_close",
    "uv__open_cloexec": "uv__close",
    "uv__make_pipe": "uv__close",
    "uv__stream_open": "uv__stream_close",
    "uv__fs_opendir": "uv__fs_closedir",
    "dlopen": "dlclose",
    "scandir": "uv__fs_scandir_cleanup",
    "getaddrinfo": "uv_freeaddrinfo",
    "uv_getaddrinfo": "uv_freeaddrinfo",
    "zmalloc": "zfree",
    "zcalloc": "zfree",
    "zrealloc": "zfree",
    "ztrymalloc": "zfree",
    "ztrycalloc": "zfree",
    "ztryrealloc": "zfree",
    "sdsnew": "sdsfree",
    "sdsnewlen": "sdsfree",
    "sdsempty": "sdsfree",
    "sdsdup": "sdsfree",
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


def _classify(target: str) -> str | None:
    if target in RELEASE_TARGETS:
        return "release"
    if target in ACQUIRE_TARGETS:
        return "acquire"
    return None


def _resource_type(resource_id: str, target: str, source: str) -> str:
    if resource_id in RESOURCE_TYPES:
        return RESOURCE_TYPES[resource_id]
    if target in HANDLE_TARGETS:
        return "handle"
    if target in MEMORY_TARGETS:
        return "memory"
    if target in FILE_DESCRIPTOR_TARGETS or source in {
        "uv__async_start",
        "uv__async_stop",
        "uv_fs_open",
        "uv__fs_close",
    }:
        return "file_descriptor"
    if source in {"uv_dlopen", "uv_dlclose", "uv__getaddrinfo_work", "uv__fs_scandir"}:
        return RESOURCE_TYPES[SOURCE_RESOURCE_IDS[source]]
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


def _resource_identity(source: str, target: str, expression: str) -> tuple[str, str]:
    if target in TARGET_RESOURCE_IDS:
        resource_id = TARGET_RESOURCE_IDS[target]
    elif target in MEMORY_TARGETS and source != "uv__getpwuid_r":
        resource_id = None
    else:
        resource_id = SOURCE_RESOURCE_IDS.get(source)
    return resource_id or expression, expression


def _operation(edge: dict[str, Any], graph: dict[str, Any], kind: str) -> dict[str, Any]:
    site = edge.get("call_site") or {}
    target = _node_name(graph, str(edge.get("target", "")))
    source = _node_name(graph, str(edge.get("source", "")))
    snippet = str(site.get("snippet") or "")
    resource, resource_expression = _resource_identity(
        source,
        target,
        _resource_key(snippet, target),
    )
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
        "_resource_id": resource,
        "_resource_expression": resource_expression,
        "_resource_type": _resource_type(resource, target, source),
        "_edge_id": edge.get("id", ""),
    }


def _pair_key(source: str, target: str) -> str:
    if source in SOURCE_PAIR_RULES:
        return f"family:{SOURCE_PAIR_RULES[source]}"
    if target in PAIR_RULES:
        return f"family:{PAIR_RULES[target]}"
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
        kind = _classify(target)
        if kind:
            operations.append(_operation(edge, graph, kind))

    grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        cross_function = operation["_resource_id"] != operation["_resource_expression"]
        grouped[
            (
                operation["_pair_key"],
                operation["_resource_id"],
                operation["_resource_expression"],
                "" if cross_function else operation["function"],
            )
        ].append(operation)

    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    referenced_evidence: set[str] = set()
    for (pair_key, resource_id, resource_expression, function), group in sorted(
        grouped.items()
    ):
        group.sort(key=lambda item: (item["file"], item["line"]))
        acquires = [item for item in group if item["kind"] == "acquire"]
        releases = [item for item in group if item["kind"] == "release"]
        selected: list[dict[str, Any]] = []
        if acquires:
            selected.append(acquires[0])
        if releases:
            selected.append(releases[-1] if acquires else releases[0])
        if not selected:
            continue
        selected.sort(key=lambda item: (item["file"], item["line"]))
        complete = bool(acquires and releases)
        termination = (
            "release_found"
            if complete
            else "release_not_found"
            if acquires
            else "acquire_not_found"
        )

        for operation in selected:
            referenced_evidence.update(operation["evidence_ids"])
        public_operations = [_public_operation(item) for item in selected]
        item_id = "rf_" + stable_digest(
            [
                pair_key,
                resource_id,
                resource_expression,
                function,
                public_operations,
            ]
        )[:12]
        items.append(
            {
                "id": item_id,
                "status": "unconfirmed",
                "resource": resource_id,
                "resource_expression": resource_expression,
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
                f"{item_id}: visible graph has {termination} for "
                f"{function}:{resource_id}[{resource_expression}]"
            )

    if len(warnings) > 50:
        warnings = warnings[:50] + [
            f"{len(warnings) - 50} additional unresolved resource paths omitted"
        ]
    status = "succeeded" if items and not warnings else ("partial" if items else "not_available")
    generated_at = str((graph.get("meta") or {}).get("generated_at") or utc_now())
    return {
        "schema_version": "1.0",
        "run_id": str(graph.get("run_id", "")),
        "result_type": "resource_flow",
        "status": status,
        "generated_at": generated_at,
        "source": {
            **dict(graph.get("meta") or {}),
            "origin": "analyzer",
            "provider": "native_resource_flow_v1",
        },
        "items": items,
        "evidence": _evidence_map(graph, referenced_evidence),
        "warnings": warnings,
    }
