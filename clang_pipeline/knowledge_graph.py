from __future__ import annotations

from typing import Any

from .clang_ast import stable_digest, utc_now


def _entity(
    entity_id: str,
    kind: str,
    name: str,
    *,
    file: str = "",
    line: int = 0,
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": entity_id,
        "kind": kind,
        "name": name,
        "file": file,
        "line": line,
        "properties": properties or {},
    }


def _relation(
    source: str,
    target: str,
    relation_type: str,
    *,
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": "kg_rel_" + stable_digest([source, target, relation_type, properties or {}])[:12],
        "type": relation_type,
        "source": source,
        "target": target,
        "properties": properties or {},
    }


def _nearest_function(
    nodes: list[dict[str, Any]],
    file: str,
    line: int,
) -> dict[str, Any] | None:
    def same_file(left: str, right: str) -> bool:
        return (
            left == right
            or left.endswith("/" + right)
            or right.endswith("/" + left)
        )

    candidates = [
        node
        for node in nodes
        if node.get("kind") == "function"
        and same_file(str(node.get("file") or ""), file)
        and int(node.get("line") or 0) <= line
    ]
    return max(candidates, key=lambda item: int(item.get("line") or 0)) if candidates else None


def build_knowledge_graph(
    graph: dict[str, Any],
    resource_flow: dict[str, Any] | None = None,
    sync_relations: dict[str, Any] | None = None,
    build_profile: dict[str, Any] | None = None,
    optimized_ir: dict[str, Any] | None = None,
    log_facts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    nodes = graph.get("nodes", [])
    entities: dict[str, dict[str, Any]] = {}
    relations: dict[str, dict[str, Any]] = {}
    code_entity = {}
    for node in nodes:
        entity_id = "code:" + str(node.get("id", ""))
        code_entity[str(node.get("id", ""))] = entity_id
        entities[entity_id] = _entity(
            entity_id,
            "code_symbol",
            str(node.get("name") or node.get("id") or ""),
            file=str(node.get("file") or ""),
            line=int(node.get("line") or 0),
            properties={
                "code_id": node.get("id", ""),
                "code_kind": node.get("kind", ""),
                "module": node.get("module", ""),
                "signature": node.get("signature", ""),
            },
        )

    for edge in graph.get("edges", []):
        source = code_entity.get(str(edge.get("source", "")))
        target = code_entity.get(str(edge.get("target", "")))
        if source and target:
            relation = _relation(
                source,
                target,
                "calls",
                properties={
                    "edge_id": edge.get("id", ""),
                    "kind": edge.get("kind", ""),
                    "confidence": edge.get("confidence", 0),
                    "condition": edge.get("condition"),
                    "evidence_ids": edge.get("evidence_ids", []),
                },
            )
            relations[relation["id"]] = relation

    build_id = ""
    if build_profile:
        build_id = "build:" + str(graph.get("run_id", ""))
        entities[build_id] = _entity(
            build_id,
            "build_profile",
            "repository build profile",
            properties=build_profile.get("summary", {}),
        )
        for unit in build_profile.get("units", []):
            unit_id = "build_unit:" + str(unit.get("id", ""))
            entities[unit_id] = _entity(
                unit_id,
                "compile_unit",
                str(unit.get("file") or ""),
                file=str(unit.get("file") or ""),
                properties=unit,
            )
            relation = _relation(build_id, unit_id, "has_compile_unit")
            relations[relation["id"]] = relation
            for node in nodes:
                if node.get("file") == unit.get("file") and node.get("id") in code_entity:
                    relation = _relation(unit_id, code_entity[node["id"]], "analyzes_symbol")
                    relations[relation["id"]] = relation

    if optimized_ir:
        for change in optimized_ir.get("changes", []):
            fact_id = "compiler_fact:" + str(change.get("id", ""))
            entities[fact_id] = _entity(
                fact_id,
                "compiler_optimization",
                str(change.get("kind") or "optimization"),
                properties=change,
            )
            function = next(
                (
                    node
                    for node in nodes
                    if node.get("kind") == "function"
                    and node.get("name") == change.get("function")
                ),
                None,
            )
            if function and function.get("id") in code_entity:
                relation = _relation(fact_id, code_entity[function["id"]], "affects_function")
                relations[relation["id"]] = relation
            if build_id:
                relation = _relation(build_id, fact_id, "produces_compiler_fact")
                relations[relation["id"]] = relation

    resource_entity = {}
    for item in (resource_flow or {}).get("items", []):
        entity_id = "resource:" + str(item.get("id", ""))
        resource_entity[str(item.get("id", ""))] = entity_id
        entities[entity_id] = _entity(
            entity_id,
            "resource",
            str(item.get("resource") or item.get("id") or ""),
            properties={
                "resource_expression": item.get("resource_expression", ""),
                "resource_type": item.get("resource_type", ""),
                "ownership_model": item.get("ownership_model", ""),
                "confidence": item.get("confidence", 0),
                "evidence_ids": item.get("evidence_ids", []),
            },
        )
        for operation in item.get("operations", []):
            function = next(
                (
                    node
                    for node in nodes
                    if node.get("kind") == "function"
                    and node.get("name") == operation.get("function")
                ),
                None,
            )
            if function and function.get("id") in code_entity:
                relation = _relation(
                    code_entity[function["id"]],
                    entity_id,
                    "uses_resource",
                    properties={
                        "operation": operation.get("kind", ""),
                        "file": operation.get("file", ""),
                        "line": operation.get("line", 0),
                    },
                )
                relations[relation["id"]] = relation

    for item in (sync_relations or {}).get("items", []):
        entity_id = "sync:" + str(item.get("id", ""))
        entities[entity_id] = _entity(
            entity_id,
            "sync_relation",
            str(item.get("relation_type") or item.get("id") or ""),
            properties={
                "order": item.get("order", ""),
                "condition": item.get("condition", ""),
                "confidence": item.get("confidence", 0),
                "evidence_ids": item.get("evidence_ids", []),
            },
        )
        for endpoint_name in ("source", "target"):
            endpoint = item.get(endpoint_name) or {}
            function_name = str(endpoint.get("function") or "")
            function = next(
                (
                    node
                    for node in nodes
                    if node.get("kind") == "function" and node.get("name") == function_name
                ),
                None,
            )
            if function and function.get("id") in code_entity:
                relation = _relation(
                    entity_id,
                    code_entity[function["id"]],
                    f"sync_{endpoint_name}",
                    properties={
                        "file": endpoint.get("file", ""),
                        "line": endpoint.get("line", 0),
                    },
                )
                relations[relation["id"]] = relation

    for event in (log_facts or {}).get("events", []):
        event_id = "log:" + str(event.get("id", ""))
        entities[event_id] = _entity(
            event_id,
            "log_event",
            str(event.get("event") or event.get("kind") or "log"),
            file=str(event.get("file") or ""),
            line=int(event.get("line") or 0),
            properties=event,
        )
        function = None
        if event.get("function"):
            function = next(
                (
                    node
                    for node in nodes
                    if node.get("kind") == "function"
                    and node.get("name") == event.get("function")
                ),
                None,
            )
        if function is None and event.get("file") and event.get("line"):
            function = _nearest_function(nodes, event["file"], int(event["line"]))
        if function and function.get("id") in code_entity:
            relation = _relation(event_id, code_entity[function["id"]], "references_symbol")
            relations[relation["id"]] = relation

    return {
        "schema_version": "1.0",
        "run_id": str(graph.get("run_id", "")),
        "generated_at": utc_now(),
        "source": dict(graph.get("meta") or {}),
        "entities": sorted(entities.values(), key=lambda item: item["id"]),
        "relations": sorted(relations.values(), key=lambda item: item["id"]),
        "build_profile": build_profile or {},
        "optimized_ir": optimized_ir or {},
        "logs": log_facts or {},
        "summary": {
            "entities": len(entities),
            "relations": len(relations),
            "resources": len(resource_entity),
            "sync_relations": len((sync_relations or {}).get("items", [])),
            "log_events": len((log_facts or {}).get("events", [])),
            "compiler_changes": len((optimized_ir or {}).get("changes", [])),
        },
    }
