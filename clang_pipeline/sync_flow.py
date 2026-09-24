from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from .clang_ast import stable_digest, utc_now


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
    for token in ("worker", "main", "submitter", "event", "loop", "thread"):
        if token in lowered:
            return token
    return None


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
    }


def _location(operation: dict[str, Any]) -> dict[str, Any]:
    return {
        "function": operation["function"],
        "thread": operation["thread"],
        "file": operation["file"],
        "line": operation["line"],
        "snippet": operation["snippet"],
        "held_locks": [],
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


def analyze_sync_relations(graph: dict[str, Any]) -> dict[str, Any]:
    """Extract first-pass synchronization relations from a Clang graph.

    The extractor is deliberately conservative: lock pairs found in the same
    function are emitted as happens-before relations. Cross-function condition
    and event pairs are emitted with unknown or low-confidence order unless
    there is a shared resource key and a visible notification/wait pair.
    """

    operations = [
        operation
        for edge in graph.get("edges", [])
        if (operation := _sync_operation(edge, graph)) is not None
    ]
    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    referenced: set[str] = set()

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
        "evidence": _evidence_map(graph, referenced),
        "warnings": warnings,
    }
