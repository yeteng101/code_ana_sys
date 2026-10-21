from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .clang_ast import evidence_id, stable_digest, utc_now


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
    assignment = ASSIGNMENT_PATTERN.search(text)
    if assignment:
        expression = _simple_expression(assignment.group("lhs"))
        if expression:
            return expression
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


ASSIGNMENT_PATTERN = re.compile(
    r"(?P<lhs>[A-Za-z_]\w*(?:(?:->|\.)[A-Za-z_]\w*|\[[^\]]+\])*)"
    r"\s*=\s*(?P<rhs>[^;]+);"
)
RETURN_PATTERN = re.compile(r"^\s*return\s+(?P<expr>[^;]+);")


def _simple_expression(value: str) -> str | None:
    cleaned = re.sub(r"^[\s(&*]+|[\s)]+$", "", value.strip())
    match = re.fullmatch(
        r"[A-Za-z_]\w*(?:(?:->|\.)[A-Za-z_]\w*|\[[^\]]+\])*",
        cleaned,
    )
    return match.group(0) if match else None


def _resolve_source_path(source_root: Path, file: str) -> Path:
    path = Path(file)
    if path.is_absolute():
        return path
    candidates = [source_root / path, Path.cwd() / path]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


def _function_ranges(
    graph: dict[str, Any],
    source_root: Path | None,
) -> dict[tuple[str, str], tuple[int, int]]:
    by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph.get("nodes", []):
        if node.get("kind") != "function":
            continue
        file = str(node.get("file") or "")
        line = int(node.get("line") or 0)
        if not file or line <= 0:
            continue
        by_file[file].append(node)
    ranges: dict[tuple[str, str], tuple[int, int]] = {}
    for file, nodes in by_file.items():
        path = _resolve_source_path(
            source_root or Path.cwd(),
            file,
        )
        try:
            line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            line_count = 0
        nodes.sort(key=lambda item: int(item["line"]))
        for index, node in enumerate(nodes):
            start = int(node["line"])
            end = (
                int(nodes[index + 1]["line"]) - 1
                if index + 1 < len(nodes)
                else line_count
            )
            ranges[(file, str(node["name"]))] = (start, max(start, end))
    return ranges


def _scan_source_facts(
    graph: dict[str, Any],
    source_root: Path,
) -> dict[str, Any]:
    facts: dict[str, Any] = {
        "assignments": [],
        "returns": [],
        "evidence": {},
    }
    ranges = _function_ranges(graph, source_root)
    file_cache: dict[str, list[str]] = {}
    for (file, function), (start, end) in ranges.items():
        path = _resolve_source_path(source_root, file)
        if file not in file_cache:
            try:
                file_cache[file] = path.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
            except OSError:
                continue
        lines = file_cache[file]
        for line in range(start, min(end, len(lines)) + 1):
            snippet = lines[line - 1].strip()
            assignment = ASSIGNMENT_PATTERN.search(snippet)
            if assignment:
                lhs = _simple_expression(assignment.group("lhs"))
                rhs = assignment.group("rhs").strip()
                if lhs:
                    evidence = evidence_id("assignment", file, line, lhs)
                    facts["assignments"].append(
                        {
                            "function": function,
                            "file": file,
                            "line": line,
                            "lhs": lhs,
                            "rhs": rhs,
                            "snippet": snippet,
                            "evidence_id": evidence,
                        }
                    )
                    facts["evidence"].setdefault(
                        evidence,
                        {
                            "id": evidence,
                            "kind": "assignment",
                            "location": {"file": file, "line": line, "snippet": snippet},
                            "role": "supports",
                        },
                    )
            returned = RETURN_PATTERN.match(snippet)
            if returned:
                expression = _simple_expression(returned.group("expr"))
                if expression:
                    evidence = evidence_id(
                        "control_flow", file, line, f"return:{expression}"
                    )
                    facts["returns"].append(
                        {
                            "function": function,
                            "file": file,
                            "line": line,
                            "expression": expression,
                            "snippet": snippet,
                            "evidence_id": evidence,
                        }
                    )
                    facts["evidence"].setdefault(
                        evidence,
                        {
                            "id": evidence,
                            "kind": "control_flow",
                            "location": {"file": file, "line": line, "snippet": snippet},
                            "role": "supports",
                        },
                    )
    return facts


def _alias_sets(facts: dict[str, Any]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = defaultdict(dict)

    def find(mapping: dict[str, str], value: str) -> str:
        mapping.setdefault(value, value)
        if mapping[value] != value:
            mapping[value] = find(mapping, mapping[value])
        return mapping[value]

    def union(mapping: dict[str, str], left: str, right: str) -> None:
        left_root, right_root = find(mapping, left), find(mapping, right)
        if left_root != right_root:
            mapping[max(left_root, right_root)] = min(left_root, right_root)

    for assignment in facts.get("assignments", []):
        rhs = assignment["rhs"]
        if "(" in rhs:
            continue
        right = _simple_expression(rhs)
        if right:
            mapping = result[assignment["function"]]
            union(mapping, assignment["lhs"], right)
    return {function: dict(mapping) for function, mapping in result.items()}


def _canonical_expression(
    function: str,
    expression: str,
    aliases: dict[str, dict[str, str]],
) -> str:
    mapping = aliases.get(function, {})
    if expression not in mapping:
        return expression
    value = expression
    while mapping.get(value, value) != value:
        value = mapping[value]
    return value


def _assignment_chain(
    function: str,
    expression: str,
    facts: dict[str, Any],
    aliases: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    canonical = _canonical_expression(function, expression, aliases)
    chain = []
    for assignment in facts.get("assignments", []):
        if assignment["function"] != function:
            continue
        rhs = _simple_expression(assignment["rhs"])
        if canonical not in {
            _canonical_expression(function, assignment["lhs"], aliases),
            _canonical_expression(function, rhs or "", aliases),
        }:
            continue
        chain.append(
            {
                "file": assignment["file"],
                "line": assignment["line"],
                "lhs": assignment["lhs"],
                "rhs": assignment["rhs"],
                "evidence_id": assignment["evidence_id"],
            }
        )
    return chain


def _returning_resource_summaries(
    operations: list[dict[str, Any]],
    facts: dict[str, Any],
    aliases: dict[str, dict[str, str]],
) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    returns_by_function: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in facts.get("returns", []):
        returns_by_function[item["function"]].append(item)
    for operation in operations:
        if operation["kind"] != "acquire":
            continue
        function = operation["function"]
        expression = operation["_resource_expression"]
        canonical = _canonical_expression(function, expression, aliases)
        visible_return = operation["snippet"].lstrip().startswith("return ")
        returned = any(
            _canonical_expression(function, item["expression"], aliases) == canonical
            for item in returns_by_function.get(function, [])
        )
        if visible_return or returned:
            summaries.setdefault(function, operation)
    return summaries


def _cross_function_transfers(
    graph: dict[str, Any],
    operations: list[dict[str, Any]],
    facts: dict[str, Any],
    aliases: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    summaries = _returning_resource_summaries(operations, facts, aliases)
    if not summaries:
        return []
    node_names = {
        str(node.get("id")): str(node.get("name") or _tail(str(node.get("id"))))
        for node in graph.get("nodes", [])
    }
    transfers: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if edge.get("kind") != "direct_call":
            continue
        target_name = node_names.get(str(edge.get("target", "")), "")
        summary = summaries.get(target_name)
        if summary is None:
            continue
        source = node_names.get(str(edge.get("source", "")), _tail(str(edge.get("source", ""))))
        site = edge.get("call_site") or {}
        snippet = str(site.get("snippet") or "")
        target_pattern = re.escape(target_name)
        assignment = re.search(
            rf"(?P<lhs>[A-Za-z_]\w*(?:(?:->|\.)[A-Za-z_]\w*|\[[^\]]+\])*)"
            rf"\s*=\s*{target_pattern}\s*\(",
            snippet,
        )
        if assignment:
            expression = assignment.group("lhs")
        elif re.search(rf"\breturn\s+{target_pattern}\s*\(", snippet):
            expression = f"{target_name}()"
        else:
            continue
        function = source
        stable_resource = summary["_resource_id"]
        if not stable_resource.startswith("rf_"):
            stable_resource = "rf_flow_" + stable_digest(
                [summary["_pair_key"], target_name]
            )[:12]
        transfers.append(
            {
                "operation_id": "transfer_" + str(edge.get("id", ""))[-10:],
                "kind": "transfer",
                "api": target_name,
                "function": function,
                "file": site.get("file", ""),
                "line": int(site.get("line", 0)),
                "snippet": snippet,
                "evidence_ids": list(edge.get("evidence_ids", [])),
                "status": "unconfirmed",
                "confidence": 0.7,
                "from_function": target_name,
                "assignment_chain": _assignment_chain(
                    function, expression, facts, aliases
                ),
                "_pair_key": summary["_pair_key"],
                "_resource_id": stable_resource,
                "_resource_expression": expression,
                "_resource_type": summary["_resource_type"],
                "_edge_id": edge.get("id", ""),
            }
        )
    return transfers


def _public_operation(operation: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in operation.items() if not key.startswith("_")}


def _evidence_map(graph: dict[str, Any], evidence_ids: set[str]) -> list[dict[str, Any]]:
    result = []
    for item in graph.get("evidence", []):
        if item.get("id") in evidence_ids:
            result.append(item)
    return sorted(result, key=lambda item: str(item.get("id", "")))


def analyze_resource_flow(
    graph: dict[str, Any],
    *,
    source_root: str | Path | None = None,
) -> dict[str, Any]:
    """Extract resource operations from a Clang-produced evidence graph.

    The first native version is intentionally rule based. It does not claim
    that an unpaired operation is a leak; it emits an incomplete path with a
    termination reason and leaves the final judgement to the consumer.
    """

    root = Path(source_root).resolve() if source_root is not None else None
    facts = (
        _scan_source_facts(graph, root)
        if root is not None
        else {"assignments": [], "returns": [], "evidence": {}}
    )
    aliases = _alias_sets(facts)
    operations: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        target = _node_name(graph, str(edge.get("target", "")))
        source = _node_name(graph, str(edge.get("source", "")))
        kind = _classify(target)
        if kind:
            operations.append(_operation(edge, graph, kind))

    transfers = _cross_function_transfers(graph, operations, facts, aliases)
    operations.extend(transfers)
    transfer_ids = {
        item["_pair_key"]: item["_resource_id"]
        for item in transfers
    }
    for operation in operations:
        operation["_canonical_expression"] = _canonical_expression(
            operation["function"],
            operation["_resource_expression"],
            aliases,
        )
        if (
            operation["kind"] != "transfer"
            and operation["_pair_key"] in transfer_ids
            and not operation["_resource_id"].startswith("rf_")
        ):
            operation["_resource_id"] = transfer_ids[operation["_pair_key"]]
        operation["assignment_chain"] = _assignment_chain(
            operation["function"],
            operation["_resource_expression"],
            facts,
            aliases,
        )

    grouped: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        cross_function = operation["_pair_key"] in transfer_ids
        grouped[
            (
                operation["_pair_key"],
                operation["_resource_id"],
                "" if cross_function else operation["_canonical_expression"],
                "" if cross_function else operation["function"],
            )
        ].append(operation)

    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    referenced_evidence: set[str] = set()
    used_fact_ids: set[str] = set()
    for (pair_key, resource_id, resource_expression, function), group in sorted(
        grouped.items()
    ):
        group.sort(key=lambda item: (item["file"], item["line"]))
        acquires = [item for item in group if item["kind"] == "acquire"]
        releases = [item for item in group if item["kind"] == "release"]
        group_transfers = [item for item in group if item["kind"] == "transfer"]
        selected: list[dict[str, Any]] = []
        if acquires:
            selected.append(acquires[0])
        selected.extend(group_transfers)
        if releases:
            selected.append(releases[-1] if acquires else releases[0])
        if not selected:
            continue
        selected.sort(key=lambda item: (item["file"], item["line"]))
        complete = bool(acquires and releases)
        cross_function = bool(group_transfers)
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
        data_flow = [
            fact
            for item in public_operations
            for fact in item.get("assignment_chain", [])
        ]
        used_fact_ids.update(fact["evidence_id"] for fact in data_flow)
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
                "resource_expression": (
                    group_transfers[0]["_resource_expression"]
                    if group_transfers
                    else resource_expression
                ),
                "resource_type": selected[0]["_resource_type"],
                "operations": public_operations,
                "owner": function,
                "thread": None,
                "ownership_model": (
                    "cross_function_transfer"
                    if cross_function
                    else "visible_acquire_release"
                    if complete
                    else "unresolved_from_visible_graph"
                ),
                "data_flow": data_flow,
                "assignment_chain": data_flow,
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

    fact_evidence = {
        evidence_id_value: item
        for evidence_id_value, item in facts.get("evidence", {}).items()
        if evidence_id_value in used_fact_ids
    }
    combined_evidence = {
        **fact_evidence,
        **{
            item["id"]: item
            for item in _evidence_map(graph, referenced_evidence)
        },
    }

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
        "evidence": sorted(combined_evidence.values(), key=lambda item: item["id"]),
        "warnings": warnings,
    }
