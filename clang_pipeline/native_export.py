from __future__ import annotations

from pathlib import Path
from typing import Any

from .clang_ast import read_json, write_json
from .compiler_facts import extract_build_profile, optimized_ir_facts
from .knowledge_graph import build_knowledge_graph
from .log_facts import collect_log_facts
from .resource_flow import analyze_resource_flow
from .sync_flow import analyze_sync_relations
from .visualization import write_visualization


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
    request_path = workspace_path / "request.json"
    source_root = None
    if request_path.exists():
        source_root = read_json(request_path).get("source_root")
    request = read_json(request_path) if request_path.exists() else {}
    resource_flow = analyze_resource_flow(graph, source_root=source_root)
    sync_relations = analyze_sync_relations(graph, source_root=source_root)
    compile_commands_path = workspace_path / "compile_commands.json"
    compile_commands = (
        list(read_json(compile_commands_path))
        if compile_commands_path.exists()
        else []
    )
    build_profile = extract_build_profile(
        compile_commands,
        source_root or request.get("repo_root") or Path.cwd(),
    )
    request_log_paths = [Path(item) for item in request.get("log_paths", [])]
    log_paths = request_log_paths or (
        sorted((workspace_path / "logs").glob("*"))
        if (workspace_path / "logs").exists()
        else []
    )
    log_facts = collect_log_facts(
        log_paths,
        source_root=source_root or request.get("repo_root") or Path.cwd(),
    )
    optimized_ir = (
        optimized_ir_facts(
            compile_commands,
            graph,
            source_root or request.get("repo_root") or Path.cwd(),
        )
        if request.get("optimized_ir")
        else {}
    )
    knowledge_graph = build_knowledge_graph(
        graph,
        resource_flow,
        sync_relations,
        build_profile=build_profile,
        optimized_ir=optimized_ir,
        log_facts=log_facts,
    )

    resource_path = workspace_path / "08-resource-flow" / "resource-flow.json"
    sync_path = workspace_path / "09-sync-relations" / "sync-relations.json"
    external_resource = workspace_path / "external" / "resource-flow.json"
    external_sync = workspace_path / "external" / "sync-relations.json"
    write_json(resource_path, resource_flow)
    write_json(sync_path, sync_relations)
    write_json(external_resource, resource_flow)
    write_json(external_sync, sync_relations)
    knowledge_dir = workspace_path / "10-knowledge"
    write_json(knowledge_dir / "build-profile.json", build_profile)
    write_json(knowledge_dir / "log-facts.json", log_facts)
    write_json(knowledge_dir / "knowledge-graph.json", knowledge_graph)
    write_json(workspace_path / "external" / "knowledge-graph.json", knowledge_graph)
    visualization_path = write_visualization(
        workspace_path,
        graph,
        resource_flow=resource_flow,
        sync_relations=sync_relations,
        knowledge_graph=knowledge_graph,
    )
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
            "knowledge_graph": str(workspace_path / "external" / "knowledge-graph.json"),
        },
        "knowledge_graph": {
            "status": "succeeded",
            "entities": knowledge_graph["summary"]["entities"],
            "relations": knowledge_graph["summary"]["relations"],
            "path": str(knowledge_dir / "knowledge-graph.json"),
        },
        "visualization": str(visualization_path),
    }
