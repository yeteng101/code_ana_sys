from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .clang_ast import evidence_id, stable_digest, utc_now


LOCK_ACQUIRE = {
    "uv_mutex_lock": ("acquire", "mutex_lock"),
    "uv_rwlock_rdlock": ("acquire", "rwlock"),
    "uv_rwlock_wrlock": ("acquire", "rwlock"),
    "uv_sem_wait": ("acquire", "mutex_lock"),
    "pthread_mutex_lock": ("acquire", "mutex_lock"),
    "pthread_rwlock_rdlock": ("acquire", "rwlock"),
    "pthread_rwlock_wrlock": ("acquire", "rwlock"),
}

LOCK_RELEASE = {
    "uv_mutex_unlock": ("release", "mutex_lock"),
    "uv_rwlock_unlock": ("release", "rwlock"),
    "uv_rwlock_rdunlock": ("release", "rwlock"),
    "uv_rwlock_wrunlock": ("release", "rwlock"),
    "uv_sem_post": ("release", "mutex_lock"),
    "pthread_mutex_unlock": ("release", "mutex_lock"),
    "pthread_rwlock_unlock": ("release", "rwlock"),
}

CONDITION_WAIT = {
    "uv_cond_wait": ("wait", "condition_variable"),
    "pthread_cond_wait": ("wait", "condition_variable"),
}

CONDITION_NOTIFY = {
    "uv_cond_signal": ("notify", "condition_variable"),
    "uv_cond_broadcast": ("notify", "condition_variable"),
    "pthread_cond_signal": ("notify", "condition_variable"),
    "pthread_cond_broadcast": ("notify", "condition_variable"),
}

THREAD_RULES = {
    "uv_thread_create": ("create", "thread_join"),
    "uv_thread_create_ex": ("create", "thread_join"),
    "uv_thread_join": ("join", "thread_join"),
    "pthread_create": ("create", "thread_join"),
    "pthread_join": ("join", "thread_join"),
}

EVENT_RULES = {
    "uv_async_send": ("notify", "event_notify"),
    "uv__async_io": ("wait", "event_wait"),
    "uv__async_send": ("notify", "event_notify"),
    "eventfd": ("wait", "event_wait"),
    "poll": ("wait", "event_wait"),
    "kevent": ("wait", "event_wait"),
    "epoll_wait": ("wait", "event_wait"),
}

SEQUENCE_TARGETS = {
    "listAddNodeTail",
    "listDelNode",
    "listFirst",
    "listEmpty",
    "setIOPendingCount",
    "getIOPendingCount",
    "zfree",
    "writeToClient",
    "readQueryFromClient",
    "freeClientAsync",
    "pthread_join",
    "_serverLog",
    "uv__queue_insert_tail",
    "uv__queue_move",
    "uv__queue_head",
    "uv__queue_remove",
    "uv__work_submit",
    "uv__fs_done",
}

QUEUE_PRODUCERS = {
    "listAddNodeTail",
    "uv__queue_insert_tail",
    "uv__queue_move",
    "setIOPendingCount",
    "uv_async_send",
}

QUEUE_CONSUMERS = {
    "listFirst",
    "listDelNode",
    "listEmpty",
    "getIOPendingCount",
    "uv__queue_head",
    "uv__queue_remove",
}

ATOMIC_RELEASE_TOKENS = (
    "memory_order_release",
    "atomic_store_explicit",
    "atomic_store(",
    "atomic_exchange_explicit",
    "atomic_exchange(",
    "atomic_fetch_add_explicit",
    "atomic_fetch_sub_explicit",
    "atomicIncr",
    "atomicDecr",
    "atomicSetWithSync",
    "__atomic_store",
)

ATOMIC_ACQUIRE_TOKENS = (
    "memory_order_acquire",
    "atomic_load_explicit",
    "atomic_load(",
    "atomicGetWithSync",
    "__atomic_load",
)

ATOMIC_RELAXED_TOKENS = (
    "memory_order_relaxed",
    "atomicGet(",
    "atomicSet(",
)

QUEUE_RESOURCE_TOKENS = (
    "queue",
    "wq",
    "jobs",
    "pending",
    "reply",
    "watcher",
    "ready",
)

IDENTIFIER_PATTERN = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
IGNORED_IDENTIFIERS = {
    "if",
    "else",
    "while",
    "for",
    "return",
    "sizeof",
    "NULL",
    "true",
    "false",
}


def _tail(value: str) -> str:
    value = value.split(":")[-1]
    return value.rsplit("::", 1)[-1]


def _node_name(graph: dict[str, Any], node_id: str) -> str:
    for node in graph.get("nodes", []):
        if node.get("id") == node_id:
            return str(node.get("name") or _tail(node_id))
    return _tail(node_id)


def _resource_key(snippet: str, fallback: str) -> str:
    text = snippet.strip()
    arguments = re.search(r"\(([^()]*)\)", text)
    if arguments:
        first = arguments.group(1).split(",", 1)[0].strip()
        if first:
            return first.lstrip("&*").strip()
    assignment = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", text)
    if assignment:
        return assignment.group(1)
    return fallback


def _thread_hint(function: str) -> str | None:
    lowered = function.lower()
    for token in ("submit", "post", "producer", "enqueue"):
        if token in lowered:
            return "producer"
    for token in ("worker", "process", "iothread", "threadmain"):
        if token in lowered:
            return "worker"
    for token in ("main", "event", "loop"):
        if token in lowered:
            return token
    return None


def _identifiers(text: str) -> set[str]:
    return {
        match.group(0)
        for match in IDENTIFIER_PATTERN.finditer(text)
        if match.group(0) not in IGNORED_IDENTIFIERS
    }


def _sequence_operation(
    edge: dict[str, Any],
    graph: dict[str, Any],
) -> dict[str, Any] | None:
    target = _node_name(graph, str(edge.get("target", "")))
    if target not in SEQUENCE_TARGETS and edge.get("kind") != "callback_edge":
        return None
    source = _node_name(graph, str(edge.get("source", "")))
    site = edge.get("call_site") or {}
    snippet = str(site.get("snippet") or "")
    return {
        "operation_id": "program_op_" + str(edge.get("id", ""))[-10:],
        "kind": "program_order",
        "relation_type": "happens_before",
        "api": target,
        "function": source,
        "thread": _thread_hint(source),
        "resource": _resource_key(snippet, target),
        "file": site.get("file", ""),
        "line": int(site.get("line", 0)),
        "snippet": snippet,
        "evidence_ids": list(edge.get("evidence_ids", [])),
        "_edge_id": edge.get("id", ""),
        "_identifiers": _identifiers(snippet),
    }


def _atomic_operation(
    edge: dict[str, Any],
    graph: dict[str, Any],
) -> dict[str, Any] | None:
    site = edge.get("call_site") or {}
    snippet = str(site.get("snippet") or "")
    classification = _classify_atomic_snippet(snippet)
    if classification is None:
        return None
    kind, semantics = classification
    target = _node_name(graph, str(edge.get("target", "")))
    source = _node_name(graph, str(edge.get("source", "")))
    return {
        "operation_id": "atomic_op_" + str(edge.get("id", ""))[-10:],
        "kind": kind,
        "relation_type": "atomic",
        "semantics": semantics,
        "access": _atomic_access(snippet),
        "api": target,
        "function": source,
        "thread": _thread_hint(source),
        "resource": _resource_key(snippet, target),
        "file": site.get("file", ""),
        "line": int(site.get("line", 0)),
        "snippet": snippet,
        "evidence_ids": list(edge.get("evidence_ids", [])),
        "_edge_id": edge.get("id", ""),
        "_identifiers": _identifiers(snippet),
    }


def _classify_atomic_snippet(snippet: str) -> tuple[str, str] | None:
    lowered = snippet.lower()
    if "atomic" not in lowered and "memory_order_" not in lowered and "__atomic" not in lowered:
        return None
    relaxed_only = (
        "memory_order_relaxed" in lowered
        or bool(re.search(r"\b(atomicIncr|atomicDecr|atomicGet|atomicSet)\s*\(", snippet))
    )
    if relaxed_only:
        kind, semantics = "relaxed", "relaxed"
    elif any(token.lower() in lowered for token in ATOMIC_RELEASE_TOKENS):
        kind, semantics = "release", "release"
    elif any(token.lower() in lowered for token in ATOMIC_ACQUIRE_TOKENS):
        kind, semantics = "acquire", "acquire"
    elif any(token.lower() in lowered for token in ATOMIC_RELAXED_TOKENS):
        kind, semantics = "relaxed", "relaxed"
    else:
        return None
    return kind, semantics


def _atomic_access(snippet: str) -> str:
    lowered = snippet.lower()
    if any(
        token in lowered
        for token in (
            "atomic_load",
            "atomicget",
            "__atomic_load",
            "atomicgetwithsync",
        )
    ):
        return "read"
    return "write"


def _sync_operation(edge: dict[str, Any], graph: dict[str, Any]) -> dict[str, Any] | None:
    target = _node_name(graph, str(edge.get("target", "")))
    source = _node_name(graph, str(edge.get("source", "")))
    rules = (
        LOCK_ACQUIRE.get(target)
        or LOCK_RELEASE.get(target)
        or CONDITION_WAIT.get(target)
        or CONDITION_NOTIFY.get(target)
        or THREAD_RULES.get(target)
        or EVENT_RULES.get(target)
    )
    if rules is None:
        return None
    kind, relation_type = rules
    site = edge.get("call_site") or {}
    snippet = str(site.get("snippet") or "")
    return {
        "operation_id": "sync_op_" + str(edge.get("id", ""))[-10:],
        "kind": kind,
        "relation_type": relation_type,
        "api": target,
        "function": source,
        "thread": _thread_hint(source),
        "resource": _resource_key(snippet, target),
        "file": site.get("file", ""),
        "line": int(site.get("line", 0)),
        "snippet": snippet,
        "evidence_ids": list(edge.get("evidence_ids", [])),
        "_edge_id": edge.get("id", ""),
        "_identifiers": _identifiers(snippet),
    }


def _location(operation: dict[str, Any]) -> dict[str, Any]:
    return {
        "function": operation["function"],
        "thread": operation["thread"],
        "file": operation["file"],
        "line": operation["line"],
        "snippet": operation["snippet"],
        "held_locks": list(operation.get("held_locks", [])),
        "evidence_ids": operation["evidence_ids"],
    }


def _make_relation(
    source: dict[str, Any],
    target: dict[str, Any],
    *,
    order: str,
    confidence: float,
    condition: str | None,
) -> dict[str, Any]:
    relation_id = "sync_" + stable_digest(
        [
            source["relation_type"],
            source["operation_id"],
            target["operation_id"],
            order,
        ]
    )[:12]
    return {
        "id": relation_id,
        "status": "unconfirmed",
        "relation_type": source["relation_type"],
        "source": _location(source),
        "target": _location(target),
        "order": order,
        "condition": condition,
        "execution_context": {
            "process": "target-repository",
            "source_thread": source.get("thread"),
            "target_thread": target.get("thread"),
            "event_loop": None,
        },
        "confidence": confidence,
        "evidence_ids": list(
            dict.fromkeys(source["evidence_ids"] + target["evidence_ids"])
        ),
        "origin": "analyzer",
    }


def _public_operation(operation: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in operation.items() if not key.startswith("_")}


def _evidence_map(graph: dict[str, Any], evidence_ids: set[str]) -> list[dict[str, Any]]:
    result = []
    for item in graph.get("evidence", []):
        if item.get("id") in evidence_ids:
            result.append(item)
    return sorted(result, key=lambda item: str(item.get("id", "")))


def _resolve_source_path(source_root: Path, file: str) -> Path:
    path = Path(file)
    if path.is_absolute():
        return path
    for candidate in (source_root / path, Path.cwd() / path):
        if candidate.is_file():
            return candidate
    return source_root / path


def _scan_source_atomic_operations(
    graph: dict[str, Any],
    source_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph.get("nodes", []):
        if node.get("kind") != "function":
            continue
        file = str(node.get("file") or "")
        line = int(node.get("line") or 0)
        if file and line > 0:
            by_file[file].append(node)
    operations: list[dict[str, Any]] = []
    evidence: dict[str, dict[str, Any]] = {}
    for file, nodes in by_file.items():
        path = _resolve_source_path(source_root, file)
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        nodes.sort(key=lambda item: int(item["line"]))
        line_functions: dict[int, str] = {}
        for index, node in enumerate(nodes):
            start = int(node["line"])
            end = (
                int(nodes[index + 1]["line"]) - 1
                if index + 1 < len(nodes)
                else len(lines)
            )
            for line_number in range(start, min(end, len(lines)) + 1):
                line_functions[line_number] = str(node.get("name") or "")
        current_function = ""
        current_started = 0
        function_pattern = re.compile(
            r"^\s*(?:[A-Za-z_][\w\s*&:<>]*?)\s+"
            r"([A-Za-z_]\w*)\s*\([^;]*\)\s*\{?"
        )
        for line_number, raw in enumerate(lines, start=1):
            defined = function_pattern.match(raw)
            if defined:
                current_function = defined.group(1)
                current_started = line_number
            function = current_function if current_started else line_functions.get(line_number, "")
            if not function:
                continue
            snippet = raw.strip()
            classification = _classify_atomic_snippet(snippet)
            if classification is None:
                continue
            call = re.search(r"\b([A-Za-z_]\w*)\s*\(", snippet)
            api = call.group(1) if call else "atomic"
            ev_id = evidence_id("call_site", file, line_number, api)
            kind, semantics = classification
            operations.append(
                {
                    "operation_id": "atomic_src_" + stable_digest(
                        [function, file, line_number, snippet]
                    )[:10],
                    "kind": kind,
                    "relation_type": "atomic",
                    "semantics": semantics,
                    "access": _atomic_access(snippet),
                    "api": api,
                    "function": function,
                    "thread": _thread_hint(function),
                    "resource": _resource_key(snippet, api),
                    "file": file,
                    "line": line_number,
                    "snippet": snippet,
                    "evidence_ids": [ev_id],
                    "_edge_id": "source_atomic",
                    "_identifiers": _identifiers(snippet),
                }
            )
            evidence[ev_id] = {
                "id": ev_id,
                "kind": "call_site",
                "location": {
                    "file": file,
                    "line": line_number,
                    "snippet": snippet,
                },
                "role": "supports",
            }
    return operations, evidence


def analyze_sync_relations(
    graph: dict[str, Any],
    *,
    source_root: str | Path | None = None,
) -> dict[str, Any]:
    """Extract first-pass synchronization relations from a Clang graph.

    The extractor is deliberately conservative: lock pairs found in the same
    function are emitted as happens-before relations. Cross-function condition
    and event pairs are emitted with unknown or low-confidence order unless
    there is a shared resource key and a visible notification/wait pair.
    """

    operations = []
    atomic_operations = []
    sequence_operations = []
    for edge in graph.get("edges", []):
        operation = _sync_operation(edge, graph)
        if operation is not None:
            operations.append(operation)
            continue
        atomic_operation = _atomic_operation(edge, graph)
        if atomic_operation is not None:
            atomic_operations.append(atomic_operation)
            continue
        sequence = _sequence_operation(edge, graph)
        if sequence is not None:
            sequence_operations.append(sequence)
    source_evidence: dict[str, dict[str, Any]] = {}
    if source_root is not None:
        scanned_atomic, source_evidence = _scan_source_atomic_operations(
            graph,
            Path(source_root).resolve(),
        )
        existing_atomic = {
            (
                item["function"],
                item["file"],
                item["line"],
                item["api"],
            )
            for item in atomic_operations
        }
        for operation in scanned_atomic:
            key = (
                operation["function"],
                operation["file"],
                operation["line"],
                operation["api"],
            )
            if key not in existing_atomic:
                atomic_operations.append(operation)
    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    referenced: set[str] = set()

    # Track the locks visible at each operation in source order. This is a
    # local program-order approximation; the condition records that boundary.
    lock_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        if operation["relation_type"] in {"mutex_lock", "rwlock"}:
            lock_groups[(operation["function"], operation["resource"])].append(operation)
    for (function, lock_resource), group in lock_groups.items():
        group.sort(key=lambda item: (item["file"], item["line"]))
        active: set[str] = set()
        for operation in group:
            if operation["kind"] == "acquire":
                active.add(lock_resource)
            operation["held_locks"] = sorted(active)
            if operation["kind"] == "release":
                active.discard(lock_resource)

    # Same-function lock pairs are the strongest evidence available in the
    # current graph: lock -> unlock in source order.
    by_function: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        by_function[
            (operation["relation_type"], operation["resource"], operation["function"])
        ].append(operation)
    for (relation_type, resource, function), group in sorted(by_function.items()):
        group.sort(key=lambda item: (item["file"], item["line"]))
        acquires = [
            item
            for item in group
            if item["kind"] in {"acquire", "wait"} and item["relation_type"] == relation_type
        ]
        releases = [
            item
            for item in group
            if item["kind"] == "release" and item["relation_type"] == relation_type
        ]
        for acquire in acquires:
            release = next(
                (item for item in releases if item["line"] >= acquire["line"]),
                None,
            )
            if release is None:
                continue
            relation = _make_relation(
                acquire,
                release,
                order="happens_before",
                confidence=0.85,
                condition=f"same function/resource {function}:{resource}",
            )
            items.append(relation)
            referenced.update(relation["evidence_ids"])

    # Atomic release/acquire pairs are cross-function publication edges when
    # the same atomic object is visible on both sides.
    by_atomic_resource: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in atomic_operations:
        by_atomic_resource[operation["resource"]].append(operation)
    for resource, group in by_atomic_resource.items():
        releases = [
            item for item in group
            if item["kind"] == "release" or item.get("semantics") == "release"
        ]
        acquires = [
            item for item in group
            if item["kind"] == "acquire" or item.get("semantics") == "acquire"
        ]
        for release in releases:
            for acquire in acquires:
                if release["function"] == acquire["function"] and release["line"] >= acquire["line"]:
                    continue
                if release["function"] == acquire["function"]:
                    order, confidence = "happens_before", 0.8
                else:
                    order, confidence = "happens_before", 0.7
                relation = _make_relation(
                    release,
                    acquire,
                    order=order,
                    confidence=confidence,
                    condition=(
                        f"atomic {resource} release/acquire across "
                        f"{release['function']} -> {acquire['function']}"
                    ),
                )
                items.append(relation)
                referenced.update(relation["evidence_ids"])
                break
        relaxed_reads = [
            item
            for item in group
            if item.get("semantics") == "relaxed" and item.get("access") == "read"
        ]
        preferred_reads = [
            item
            for item in relaxed_reads
            if any(
                token in item["function"].lower()
                for token in ("get", "count", "read", "load")
            )
        ]
        if preferred_reads:
            relaxed_reads = preferred_reads
        relaxed_writes = [
            item
            for item in group
            if item.get("semantics") == "relaxed" and item.get("access") == "write"
        ]
        for source in relaxed_writes:
            target = next(
                (
                    item
                    for item in relaxed_reads
                    if item["function"] != source["function"]
                ),
                None,
            )
            if target is None:
                continue
            relation = _make_relation(
                source,
                target,
                order="unknown",
                confidence=0.3,
                condition=(
                    f"atomic relaxed {resource}; no acquire/release "
                    "publication established"
                ),
            )
            items.append(relation)
            referenced.update(relation["evidence_ids"])

    # Thread create/join pairs use the thread handle as the resource key.
    by_thread_handle: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in operations:
        if operation["relation_type"] == "thread_join":
            by_thread_handle[operation["resource"]].append(operation)
    for handle, group in by_thread_handle.items():
        creates = [item for item in group if item["kind"] == "create"]
        joins = [item for item in group if item["kind"] == "join"]
        for create in creates:
            for join in joins:
                relation = _make_relation(
                    create,
                    join,
                    order="happens_before",
                    confidence=0.75,
                    condition=f"thread handle {handle} is joined",
                )
                items.append(relation)
                referenced.update(relation["evidence_ids"])
                break

    # Cross-function queue publication: a producer inserts into a queue and a
    # different function consumes the same visible queue expression.
    queue_operations = [
        item for item in sequence_operations
        if item["api"] in QUEUE_PRODUCERS or item["api"] in QUEUE_CONSUMERS
    ]
    queue_by_resource: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in queue_operations:
        resource = str(operation.get("resource") or "")
        if len(resource) < 2:
            continue
        if (
            resource.isupper()
            or resource in {"i", "j", "job", "count", "keys"}
            or not any(token in resource.lower() for token in QUEUE_RESOURCE_TOKENS)
        ):
            continue
        queue_by_resource[resource].append(operation)
    for resource, group in queue_by_resource.items():
        producers = [item for item in group if item["api"] in QUEUE_PRODUCERS]
        consumers = [item for item in group if item["api"] in QUEUE_CONSUMERS]
        for producer in producers:
            for consumer in consumers:
                if producer["function"] == consumer["function"]:
                    continue
                relation = _make_relation(
                    producer,
                    consumer,
                    order="happens_before",
                    confidence=0.55,
                    condition=(
                        f"cross-function queue publication {resource}: "
                        f"{producer['function']} -> {consumer['function']}"
                    ),
                )
                items.append(relation)
                referenced.update(relation["evidence_ids"])
                break

    # Condition notification -> wait uses the same condition object when the
    # source expression is visible. The order is useful but still heuristic.
    for relation_type in ("condition_variable", "event_notify", "event_wait"):
        waits = [
            item
            for item in operations
            if item["relation_type"] == relation_type and item["kind"] == "wait"
        ]
        notifies = [
            item
            for item in operations
            if item["relation_type"] == relation_type and item["kind"] == "notify"
        ]
        for notify in notifies:
            for wait in waits:
                if notify["resource"] and notify["resource"] == wait["resource"]:
                    relation = _make_relation(
                        notify,
                        wait,
                        order="happens_before",
                        confidence=0.6,
                        condition=(
                            f"visible notification for shared resource "
                            f"{notify['resource']}"
                        ),
                    )
                    items.append(relation)
                    referenced.update(relation["evidence_ids"])
                    break

    # Event-loop wakeup is a native but lower-confidence causal relation when
    # the graph contains both a notify and a wait implementation.
    notify = next(
        (item for item in operations if item["relation_type"] == "event_notify"),
        None,
    )
    wait = next(
        (item for item in operations if item["relation_type"] == "event_wait"),
        None,
    )
    if notify is not None and wait is not None:
        items.append(
            _make_relation(
                notify,
                wait,
                order="unknown",
                confidence=0.4,
                condition="same event loop wakeup must be consumed",
            )
        )
        referenced.update(items[-1]["evidence_ids"])

    # Adjacent same-function facts with a shared variable are a useful
    # program-order approximation until CFG and full alias analysis are added.
    by_function_sequence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in operations + sequence_operations:
        by_function_sequence[operation["function"]].append(operation)
    for function, group in by_function_sequence.items():
        group.sort(key=lambda item: (item["file"], item["line"]))
        for index, source in enumerate(group[:-1]):
            for target in group[index + 1 :]:
                if target["line"] <= source["line"]:
                    continue
                shared = source.get("_identifiers", set()) & target.get(
                    "_identifiers", set()
                )
                if not shared:
                    continue
                relation = _make_relation(
                    source,
                    target,
                    order="happens_before",
                    confidence=0.55,
                    condition=(
                        f"program order {function}:"
                        f"{','.join(sorted(shared)[:5])}"
                    ),
                )
                items.append(relation)
                referenced.update(relation["evidence_ids"])
                break

    # Deduplicate equal relations while retaining all evidence.
    deduped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in items:
        key = (
            str(item["relation_type"]),
            str(item["source"].get("file")) + ":" + str(item["source"].get("line")),
            str(item["target"].get("file")) + ":" + str(item["target"].get("line")),
        )
        if key in deduped:
            deduped[key]["evidence_ids"] = list(
                dict.fromkeys(
                    deduped[key]["evidence_ids"] + item["evidence_ids"]
                )
            )
        else:
            deduped[key] = item
    items = sorted(deduped.values(), key=lambda item: item["id"])

    if not items:
        warnings.append("no synchronization relation matched the native rules")
    status = "succeeded" if items else "not_available"
    generated_at = str((graph.get("meta") or {}).get("generated_at") or utc_now())
    output_evidence = {
        item["id"]: item
        for item in _evidence_map(graph, referenced)
    }
    output_evidence.update(
        {
            evidence_id_value: item
            for evidence_id_value, item in source_evidence.items()
            if evidence_id_value in referenced
        }
    )
    return {
        "schema_version": "1.0",
        "run_id": str(graph.get("run_id", "")),
        "result_type": "sync_relation",
        "status": status,
        "generated_at": generated_at,
        "source": {
            **dict(graph.get("meta") or {}),
            "origin": "analyzer",
            "provider": "native_sync_flow_v1",
        },
        "items": items,
        "evidence": sorted(output_evidence.values(), key=lambda item: item["id"]),
        "warnings": warnings,
    }
