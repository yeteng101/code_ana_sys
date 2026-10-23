#!/usr/bin/env python3
"""Tail logs, append extracted facts, and refresh the evidence knowledge graph."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clang_pipeline.clang_ast import read_json, utc_now, write_json
from clang_pipeline.knowledge_graph import build_knowledge_graph
from clang_pipeline.log_facts import RealtimeLogExtractor
from clang_pipeline.visualization import write_visualization


def _refresh_graph(workspace: Path, log_facts: dict) -> dict:
    graph_path = workspace / "07-report" / "graph.json"
    if not graph_path.exists():
        return {}
    graph = read_json(graph_path)
    resource_path = workspace / "external" / "resource-flow.json"
    sync_path = workspace / "external" / "sync-relations.json"
    resource_flow = read_json(resource_path) if resource_path.exists() else {"items": []}
    sync_relations = read_json(sync_path) if sync_path.exists() else {"items": []}
    build_path = workspace / "10-knowledge" / "build-profile.json"
    build_profile = read_json(build_path) if build_path.exists() else {}
    old_kg_path = workspace / "10-knowledge" / "knowledge-graph.json"
    old_kg = read_json(old_kg_path) if old_kg_path.exists() else {}
    knowledge = build_knowledge_graph(
        graph,
        resource_flow,
        sync_relations,
        build_profile=build_profile,
        optimized_ir=old_kg.get("optimized_ir", {}),
        log_facts=log_facts,
    )
    write_json(workspace / "10-knowledge" / "knowledge-graph.json", knowledge)
    write_json(workspace / "external" / "knowledge-graph.json", knowledge)
    write_visualization(
        workspace,
        graph,
        resource_flow=resource_flow,
        sync_relations=sync_relations,
        knowledge_graph=knowledge,
    )
    return knowledge


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--log", action="append", required=True)
    parser.add_argument("--source-root", default="")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--no-refresh", action="store_true")
    parser.add_argument("--events-jsonl", type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    request_path = workspace / "request.json"
    request = read_json(request_path) if request_path.exists() else {}
    source_root = Path(
        args.source_root or request.get("source_root") or workspace
    ).resolve()
    log_paths = [Path(value).expanduser().resolve() for value in args.log]
    extractor = RealtimeLogExtractor(log_paths, source_root=source_root)
    log_facts_path = workspace / "10-knowledge" / "log-facts.json"
    existing = read_json(log_facts_path) if log_facts_path.exists() else {}
    events = list(existing.get("events", []))
    seen = {str(item.get("id")) for item in events}
    jsonl_path = args.events_jsonl or workspace / "10-knowledge" / "log-events.jsonl"
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    last_result: dict = {}
    while True:
        new_events = extractor.poll()
        if new_events:
            with jsonl_path.open("a", encoding="utf-8", newline="\n") as stream:
                for event in new_events:
                    if event["id"] in seen:
                        continue
                    seen.add(event["id"])
                    events.append(event)
                    stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            log_facts = {
                "schema_version": "1.0",
                "generated_at": utc_now(),
                "source_root": str(source_root),
                "files": [
                    {
                        "path": str(path),
                        "events": sum(
                            item.get("log_file") == path.name for item in events
                        ),
                    }
                    for path in log_paths
                ],
                "events": events,
            }
            write_json(log_facts_path, log_facts)
            knowledge = {} if args.no_refresh else _refresh_graph(workspace, log_facts)
            last_result = {
                "status": "updated",
                "new_events": len(new_events),
                "total_events": len(events),
                "log_facts": str(log_facts_path),
                "knowledge_graph": str(
                    workspace / "10-knowledge" / "knowledge-graph.json"
                )
                if knowledge
                else "",
            }
        else:
            last_result = {
                "status": "idle",
                "new_events": 0,
                "total_events": len(events),
                "log_facts": str(log_facts_path),
            }
        if args.once:
            print(json.dumps(last_result, ensure_ascii=False, indent=2))
            return 0
        if new_events:
            print(json.dumps(last_result, ensure_ascii=False))
        time.sleep(max(args.interval, 0.1))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
