from __future__ import annotations

from pathlib import Path
from typing import Any

from .clang_ast import read_json, write_json
from .resource_flow import analyze_resource_flow
from .sync_flow import analyze_sync_relations


def run_native_export(
    workspace: str | Path,
    graph_path: str | Path | None = None,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    source_graph = (
        Path(graph_path).resolve()
        if graph_path
        else workspace_path / "graph.json"
    )
    if not source_graph.exists():
        source_graph = workspace_path / "07-report" / "graph.json"
    graph = read_json(source_graph)
    resource_flow = analyze_resource_flow(graph)
    sync_relations = analyze_sync_relations(graph)

    resource_path = workspace_path / "08-resource-flow" / "resource-flow.json"
    sync_path = workspace_path / "09-sync-relations" / "sync-relations.json"
    external_resource = workspace_path / "external" / "resource-flow.json"
    external_sync = workspace_path / "external" / "sync-relations.json"
    write_json(resource_path, resource_flow)
    write_json(sync_path, sync_relations)
    write_json(external_resource, resource_flow)
    write_json(external_sync, sync_relations)
    return {
        "status": "succeeded",
        "run_id": str(graph.get("run_id", "")),
        "graph": str(source_graph),
        "resource_flow": {
            "status": resource_flow["status"],
            "items": len(resource_flow["items"]),
            "path": str(resource_path),
        },
        "sync_relations": {
            "status": sync_relations["status"],
            "items": len(sync_relations["items"]),
            "path": str(sync_path),
        },
        "external": {
            "resource_flow": str(external_resource),
            "sync_relations": str(external_sync),
        },
    }
