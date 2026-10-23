from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .clang_ast import read_json


VISUALIZATION_FILENAME = "visualization.html"
MAX_MODULE_NODES = 8
MAX_CALL_NODES = 220
MAX_CALL_EDGES = 1600
MAX_EXTERNAL_CALLS = 80


def _optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return read_json(path)


def _artifact(workspace: Path, *names: str) -> Path:
    for name in names:
        path = workspace / name
        if path.exists():
            return path
    return workspace / names[-1]


def _component_for_file(file: str) -> str:
    parts = Path(file).parts
    if not parts:
        return "core"
    parent = parts[-2] if len(parts) >= 2 else parts[-1]
    if len(parts) >= 3 and parent in {"src", "include"}:
        platform = parts[-3]
        if platform in {
            "unix",
            "win",
            "winapi",
            "darwin",
            "linux",
            "generic",
            "aix",
            "os390",
            "qnx",
            "sunos",
        }:
            return platform
    return parent or "core"


def _component_for_node(node: dict[str, Any]) -> str:
    if node.get("kind") == "external_function":
        return "external"
    return _component_for_file(node.get("file", ""))


def _component_names(architecture: dict[str, Any]) -> dict[str, str]:
    return {
        component.get("id", ""): component.get("name")
        or component.get("id", "")
        for component in architecture.get("components", [])
    }


def _build_component_index(
    nodes: list[dict[str, Any]],
    architecture: dict[str, Any],
) -> tuple[dict[str, str], dict[str, str]]:
    names = _component_names(architecture)
    by_node: dict[str, str] = {}
    symbol_to_component: dict[str, str] = {}
    for component in architecture.get("components", []):
        component_id = component.get("id", "")
        names.setdefault(component_id, component_id)
        for symbol in component.get("symbols", []):
            symbol_to_component[str(symbol.get("id", ""))] = component_id
    for node in nodes:
        node_id = str(node.get("id", ""))
        component_id = symbol_to_component.get(node_id)
        if not component_id:
            component_id = _component_for_node(node)
            names.setdefault(component_id, component_id)
        by_node[node_id] = component_id
    return by_node, names


def _prepare_calls(
    graph: dict[str, Any],
    by_node: dict[str, str],
) -> list[dict[str, Any]]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_by_id = {node["id"]: node for node in nodes}
    degree: Counter[str] = Counter()
    for edge in edges:
        degree[str(edge.get("source", ""))] += 1
        degree[str(edge.get("target", ""))] += 1

    selected = {
        node_id
        for node_id, _ in degree.most_common(MAX_CALL_NODES)
    }
    external_ids = {
        node["id"]
        for node in nodes
        if node.get("kind") == "external_function"
    }
    selected.update(list(external_ids)[:MAX_EXTERNAL_CALLS])

    selected_edges = []
    for edge in edges:
        if edge.get("source") in selected or edge.get("target") in selected:
            selected_edges.append(edge)
            if len(selected_edges) >= MAX_CALL_EDGES:
                break

    calls = []
    for edge in selected_edges:
        source = node_by_id.get(edge.get("source"), {})
        target = node_by_id.get(edge.get("target"), {})
        site = edge.get("call_site") or {}
        snippet = str(site.get("snippet") or "")
        calls.append(
            {
                "id": str(edge.get("id", "")),
                "source": str(source.get("name") or edge.get("source", "")),
                "target": str(target.get("name") or edge.get("target", "")),
                "source_component": by_node.get(str(edge.get("source", "")), "core"),
                "target_component": by_node.get(str(edge.get("target", "")), "core"),
                "kind": str(edge.get("kind", "direct_call")),
                "file": str(site.get("file", "")),
                "line": int(site.get("line", 0)),
                "snippet": snippet[:180],
                "confidence": edge.get("confidence", 0.0),
            }
        )
    calls.sort(
        key=lambda item: (
            item["source_component"],
            item["source"],
            item["target"],
            item["file"],
            item["line"],
        )
    )
    return calls


def _module_graph(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    by_node: dict[str, str],
    names: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    node_counts: Counter[str] = Counter(by_node.values())
    selected_ids = {
        component_id
        for component_id, _ in node_counts.most_common(MAX_MODULE_NODES)
    }
    module_nodes = [
        {
            "id": component_id,
            "name": names.get(component_id, component_id),
            "value": node_counts[component_id],
        }
        for component_id in sorted(
            selected_ids,
            key=lambda item: (-node_counts[item], item),
        )
    ]

    edge_counts: Counter[tuple[str, str]] = Counter()
    for edge in edges:
        source = by_node.get(str(edge.get("source", "")), "")
        target = by_node.get(str(edge.get("target", "")), "")
        if (
            source
            and target
            and source in selected_ids
            and target in selected_ids
            and source != target
        ):
            edge_counts[(source, target)] += 1

    module_edges = [
        {
            "source": source,
            "target": target,
            "value": count,
        }
        for (source, target), count in edge_counts.most_common()
    ]
    return module_nodes, module_edges


def _stable_number(value: str) -> int:
    digest = 0
    for char in value:
        digest = ((digest * 131) + ord(char)) & 0xFFFFFFFF
    return digest


def _full_graph(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    by_node: dict[str, str],
    names: dict[str, str],
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        grouped[by_node.get(str(node.get("id", "")), "core")].append(node)

    component_ids = sorted(
        grouped,
        key=lambda item: (-len(grouped[item]), item),
    )
    center_by_component: dict[str, tuple[float, float]] = {}
    if len(component_ids) <= 10:
        for index, component_id in enumerate(component_ids):
            angle = -3.141592653589793 / 2 + (
                index / max(1, len(component_ids))
            ) * 2 * 3.141592653589793
            center_by_component[component_id] = (
                1000 + 700.0 * math.cos(angle),
                560 + 360.0 * math.sin(angle),
            )
    else:
        columns = int((len(component_ids) - 1) ** 0.5) + 1
        for index, component_id in enumerate(component_ids):
            row, column = divmod(index, columns)
            center_by_component[component_id] = (
                220.0 + column * 420.0,
                220.0 + row * 340.0,
            )

    node_records = []
    for component_id in component_ids:
        center_x, center_y = center_by_component[component_id]
        group = grouped[component_id]
        group_radius = min(
            260.0,
            46.0 + (len(group) ** 0.5) * 14.0,
        )
        for index, node in enumerate(sorted(group, key=lambda item: str(item.get("id", "")))):
            angle = (index * 2.399963229728653) % (2 * 3.141592653589793)
            radius = group_radius * ((index % 17) / 17 + 0.35)
            jitter = _stable_number(str(node.get("id", ""))) % 31 - 15
            node_records.append(
                {
                    "id": str(node.get("id", "")),
                    "name": str(node.get("name") or node.get("id", "")),
                    "kind": str(node.get("kind") or "unknown"),
                    "component": component_id,
                    "x": center_x + radius * math.cos(angle) + jitter,
                    "y": center_y + radius * math.sin(angle) + jitter,
                }
            )

    node_by_id = {item["id"]: item for item in node_records}
    edge_records = []
    for edge in edges:
        if edge.get("source") in node_by_id and edge.get("target") in node_by_id:
            edge_records.append(
                {
                    "source": str(edge.get("source", "")),
                    "target": str(edge.get("target", "")),
                    "kind": str(edge.get("kind", "direct_call")),
                }
            )

    return {
        "nodes": node_records,
        "edges": edge_records,
        "components": [
            {
                "id": component_id,
                "name": names.get(component_id, component_id),
                "count": len(grouped[component_id]),
            }
            for component_id in component_ids
        ],
    }


def _prepare_data(
    graph: dict[str, Any],
    resource_flow: dict[str, Any],
    sync_relations: dict[str, Any],
    architecture: dict[str, Any],
    key_chains: dict[str, Any],
    run_result: dict[str, Any],
    verification: dict[str, Any],
    analysis_text: str,
    knowledge_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    by_node, component_names = _build_component_index(nodes, architecture)
    module_nodes, module_edges = _module_graph(
        nodes,
        edges,
        by_node,
        component_names,
    )
    full_graph = _full_graph(
        nodes,
        edges,
        by_node,
        component_names,
    )

    resource_types = Counter(
        str(item.get("resource_type") or "other")
        for item in resource_flow.get("items", [])
    )
    sync_types = Counter(
        str(item.get("relation_type") or "unknown")
        for item in sync_relations.get("items", [])
    )
    coverage = (verification.get("coverage") or {}).get("coverage_rate")
    knowledge_graph = knowledge_graph or {}
    knowledge_entities = knowledge_graph.get("entities", [])
    knowledge_relations = knowledge_graph.get("relations", [])

    return {
        "run_id": str(graph.get("run_id", "")),
        "repository": str((graph.get("meta") or {}).get("repository", "")),
        "commit": str((graph.get("meta") or {}).get("commit", "")),
        "build_profile": str((graph.get("meta") or {}).get("build_profile", "")),
        "metrics": {
            "nodes": len(nodes),
            "edges": len(edges),
            "evidence": len(graph.get("evidence", [])),
            "external": sum(
                node.get("kind") == "external_function" for node in nodes
            ),
            "coverage": round(float(coverage), 4) if coverage is not None else None,
            "resource_items": len(resource_flow.get("items", [])),
            "sync_items": len(sync_relations.get("items", [])),
            "knowledge_entities": len(knowledge_entities),
            "knowledge_relations": len(knowledge_relations),
        },
        "node_kinds": dict(
            Counter(
                str(node.get("kind") or "unknown")
                for node in nodes
            ).most_common()
        ),
        "edge_kinds": dict(
            Counter(
                str(edge.get("kind") or "unknown")
                for edge in edges
            ).most_common()
        ),
        "modules": module_nodes,
        "module_edges": module_edges,
        "full_graph": full_graph,
        "calls": _prepare_calls(graph, by_node),
        "key_chains": key_chains.get("paths", [])[:12],
        "resource_flow": {
            "status": resource_flow.get("status", "not_available"),
            "types": dict(resource_types.most_common()),
        },
        "sync_relations": {
            "status": sync_relations.get("status", "not_available"),
            "types": dict(sync_types.most_common()),
        },
        "knowledge": {
            "summary": knowledge_graph.get("summary", {}),
            "entities": knowledge_entities[:1200],
            "relations": knowledge_relations[:1800],
        },
        "analysis": analysis_text[:6000],
        "summary": str(
            (run_result.get("summary") or "").strip()
            or (graph.get("meta") or {}).get("summary", "")
        ),
    }


def _render_html(data: dict[str, Any]) -> str:
    payload = json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    return TEMPLATE.replace("__VIS_DATA__", payload)


def write_visualization(
    workspace: str | Path,
    graph: dict[str, Any] | None = None,
    *,
    resource_flow: dict[str, Any] | None = None,
    sync_relations: dict[str, Any] | None = None,
    knowledge_graph: dict[str, Any] | None = None,
    output: str | Path | None = None,
) -> Path:
    workspace_path = Path(workspace).resolve()
    graph = graph or _optional_json(_artifact(workspace_path, "07-report/graph.json", "graph.json"))
    resource_flow = resource_flow or _optional_json(
        _artifact(
            workspace_path,
            "08-resource-flow/resource-flow.json",
            "external/resource-flow.json",
            "resource-flow.json",
        )
    )
    sync_relations = sync_relations or _optional_json(
        _artifact(
            workspace_path,
            "09-sync-relations/sync-relations.json",
            "external/sync-relations.json",
            "sync-relations.json",
        )
    )
    knowledge_graph = knowledge_graph or _optional_json(
        _artifact(
            workspace_path,
            "external/knowledge-graph.json",
            "knowledge-graph.json",
            "10-knowledge/knowledge-graph.json",
        )
    )
    architecture = _optional_json(
        _artifact(
            workspace_path,
            "07-report/architecture.json",
            "architecture.json",
        )
    )
    key_chains = _optional_json(
        _artifact(
            workspace_path,
            "07-report/key-chains.json",
            "key-chains.json",
        )
    )
    run_result = _optional_json(
        _artifact(
            workspace_path,
            "07-report/run-result.json",
            "run-result.json",
        )
    )
    verification = _optional_json(
        _artifact(
            workspace_path,
            "06-verify/verification.json",
            "verification.json",
        )
    )
    analysis_path = _artifact(
        workspace_path,
        "07-report/analysis.md",
        "analysis.md",
    )
    analysis_text = (
        analysis_path.read_text(encoding="utf-8")
        if analysis_path.exists()
        else ""
    )
    data = _prepare_data(
        graph,
        resource_flow,
        sync_relations,
        architecture,
        key_chains,
        run_result,
        verification,
        analysis_text,
        knowledge_graph,
    )
    report_dir = workspace_path / "07-report"
    target = Path(output).resolve() if output else (
        report_dir / VISUALIZATION_FILENAME
        if report_dir.exists()
        else workspace_path / VISUALIZATION_FILENAME
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_render_html(data), encoding="utf-8")
    return target


TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Code Reverse Analysis</title>
  <style>
    :root {
      color-scheme: light dark;
      --bg: #f4f6f8;
      --surface: #ffffff;
      --surface-2: #e9eef3;
      --text: #18202a;
      --muted: #66727f;
      --border: #d7dee6;
      --accent: #2f6fed;
      --accent-soft: #dfe9ff;
      --green: #1f8a5b;
      --red: #c23b46;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #10151c;
        --surface: #171d26;
        --surface-2: #202936;
        --text: #e8edf3;
        --muted: #a3adba;
        --border: #303b49;
        --accent: #6f9dff;
        --accent-soft: #233a62;
        --green: #55b98a;
        --red: #e5727c;
      }
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    header {
      padding: 22px 28px 16px;
      border-bottom: 1px solid var(--border);
    }
    h1 {
      margin: 0 0 8px;
      font-size: 22px;
      font-weight: 600;
    }
    .meta {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
      overflow-wrap: anywhere;
    }
    main {
      padding: 18px 28px 30px;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }
    .stat {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      min-height: 68px;
    }
    .stat-label {
      color: var(--muted);
      font-size: 12px;
    }
    .stat-value {
      margin-top: 7px;
      font-size: 22px;
      font-weight: 600;
      font-variant-numeric: tabular-nums;
    }
    .tabs {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }
    .tab {
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      border-radius: 6px;
      padding: 7px 12px;
      font: inherit;
      cursor: pointer;
    }
    .tab.active {
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
    }
    .panel { display: none; }
    .panel.active { display: block; }
    .section-title {
      margin: 0 0 10px;
      font-size: 16px;
      font-weight: 600;
    }
    .graph-shell {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px;
      min-height: 330px;
    }
    svg { display: block; width: 100%; height: auto; }
    .module-node {
      cursor: pointer;
      stroke: var(--accent);
      stroke-width: 1.5;
      fill: var(--surface-2);
    }
    .module-node.selected {
      fill: var(--accent-soft);
      stroke-width: 3;
    }
    .module-label {
      fill: var(--text);
      font-size: 12px;
      text-anchor: middle;
    }
    .module-edge {
      stroke: var(--muted);
      stroke-opacity: 0.42;
      fill: none;
    }
    .overview-detail {
      min-height: 22px;
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
    }
    .graph-toolbar {
      display: flex;
      gap: 8px;
      align-items: end;
      margin-bottom: 10px;
    }
    .graph-toolbar label {
      flex: 1;
    }
    .graph-zoom {
      width: 36px;
      height: 36px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      font-size: 20px;
      cursor: pointer;
    }
    .graph-canvas-shell {
      position: relative;
      height: 650px;
      min-height: 480px;
      overflow: hidden;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
    }
    #full-graph-canvas {
      display: block;
      width: 100%;
      height: 100%;
      cursor: grab;
      touch-action: none;
    }
    #full-graph-canvas.dragging {
      cursor: grabbing;
    }
    .graph-detail {
      min-height: 24px;
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      overflow-wrap: anywhere;
    }
    .graph-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin: 10px 0 0 2px;
      color: var(--muted);
      font-size: 12px;
    }
    .graph-legend span {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent);
    }
    .module-list {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 10px;
    }
    .module-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
    }
    .module-name {
      margin-bottom: 7px;
      font-weight: 600;
    }
    .module-bar {
      height: 6px;
      background: var(--surface-2);
      border-radius: 999px;
      overflow: hidden;
      margin: 8px 0;
    }
    .module-bar span {
      display: block;
      height: 100%;
      background: var(--accent);
    }
    .module-meta {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
      overflow-wrap: anywhere;
    }
    .toolbar {
      display: flex;
      gap: 10px;
      align-items: end;
      margin-bottom: 10px;
    }
    .toolbar label {
      display: flex;
      flex-direction: column;
      gap: 5px;
      flex: 1;
      color: var(--muted);
      font-size: 12px;
    }
    input {
      width: 100%;
      min-height: 36px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 0 10px;
      font: inherit;
    }
    select {
      width: 100%;
      min-height: 36px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 0 10px;
      font: inherit;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th, td {
      padding: 9px 8px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }
    th {
      color: var(--muted);
      font-weight: 500;
    }
    td.code {
      max-width: 380px;
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
    }
    .call-count {
      color: var(--muted);
      margin-bottom: 8px;
      font-size: 12px;
    }
    .finding-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
    }
    .finding-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 13px;
    }
    .finding-card h3 {
      margin: 0 0 8px;
      font-size: 14px;
    }
    .tag-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .tag {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 4px 8px;
      color: var(--muted);
      font-size: 12px;
    }
    .path-list {
      margin: 0;
      padding: 0;
      list-style: none;
    }
    .path-list li {
      padding: 8px 0;
      border-bottom: 1px solid var(--border);
      line-height: 1.5;
      overflow-wrap: anywhere;
    }
    @media (max-width: 600px) {
      header, main { padding-left: 14px; padding-right: 14px; }
      .toolbar { display: block; }
      th:nth-child(2), td:nth-child(2) { display: none; }
    }
  </style>
</head>
<body>
  <header>
    <h1 id="viz-title">Code Reverse Analysis</h1>
    <div class="meta" id="viz-meta"></div>
  </header>
  <main>
    <section class="stats" id="viz-stats"></section>
    <nav class="tabs" aria-label="Views">
      <button class="tab active" type="button" data-tab="overview">Overview</button>
      <button class="tab" type="button" data-tab="graph">Graph</button>
      <button class="tab" type="button" data-tab="modules">Modules</button>
      <button class="tab" type="button" data-tab="calls">Calls</button>
      <button class="tab" type="button" data-tab="findings">Findings</button>
      <button class="tab" type="button" data-tab="knowledge">Knowledge</button>
    </nav>
    <section class="panel" id="panel-graph">
      <h2 class="section-title">Full Call Graph</h2>
      <div class="graph-toolbar">
        <label>Node
          <input id="graph-search" type="search" autocomplete="off">
        </label>
        <label>Edge mode
          <select id="graph-edge-mode">
            <option value="module">Module edges</option>
            <option value="all">All edges</option>
            <option value="selected">Selected only</option>
          </select>
        </label>
        <button class="graph-zoom" id="graph-zoom-in" type="button" aria-label="Zoom in">+</button>
        <button class="graph-zoom" id="graph-zoom-out" type="button" aria-label="Zoom out">−</button>
      </div>
      <div class="graph-canvas-shell">
        <canvas id="full-graph-canvas" aria-label="Full call graph"></canvas>
      </div>
      <div class="graph-legend" aria-hidden="true">
        <span><i class="legend-dot" style="background:var(--accent)"></i>Function</span>
        <span><i class="legend-dot" style="background:var(--green)"></i>Callback</span>
        <span><i class="legend-dot" style="background:var(--red)"></i>External</span>
      </div>
      <div class="graph-detail" id="graph-detail"></div>
    </section>
    <section class="panel active" id="panel-overview">
      <h2 class="section-title">Module Graph</h2>
      <div class="graph-shell" id="module-graph"></div>
      <div class="overview-detail" id="overview-detail"></div>
    </section>
    <section class="panel" id="panel-modules">
      <h2 class="section-title">Modules</h2>
      <div class="module-list" id="module-list"></div>
    </section>
    <section class="panel" id="panel-calls">
      <h2 class="section-title">Calls</h2>
      <div class="toolbar">
        <label>Symbol / File
          <input id="call-filter" type="search" autocomplete="off">
        </label>
      </div>
      <div class="call-count" id="call-count"></div>
      <table>
        <thead>
          <tr><th>Source</th><th>Module</th><th>Target</th><th>Kind</th><th>Location</th><th>Code</th></tr>
        </thead>
        <tbody id="call-rows"></tbody>
      </table>
    </section>
    <section class="panel" id="panel-findings">
      <h2 class="section-title">Findings</h2>
      <div class="finding-grid" id="finding-grid"></div>
    </section>
    <section class="panel" id="panel-knowledge">
      <h2 class="section-title">Knowledge Graph</h2>
      <div class="toolbar">
        <label>Entity / File
          <input id="knowledge-filter" type="search" autocomplete="off">
        </label>
        <label>Entity kind
          <select id="knowledge-kind">
            <option value="">All kinds</option>
          </select>
        </label>
      </div>
      <div class="call-count" id="knowledge-count"></div>
      <table>
        <thead>
          <tr><th>Entity</th><th>Kind</th><th>Name</th><th>Location</th><th>Properties</th></tr>
        </thead>
        <tbody id="knowledge-rows"></tbody>
      </table>
      <h3 class="section-title" style="margin-top:20px">Relations</h3>
      <table>
        <thead>
          <tr><th>Type</th><th>Source</th><th>Target</th></tr>
        </thead>
        <tbody id="knowledge-relation-rows"></tbody>
      </table>
    </section>
  </main>
  <script id="viz-data" type="application/json">__VIS_DATA__</script>
  <script>
    (() => {
      const data = JSON.parse(document.getElementById("viz-data").textContent);
      const byId = (id) => document.getElementById(id);

      byId("viz-title").textContent = data.repository || data.run_id || "Code Reverse Analysis";
      const meta = [data.repository, data.commit, data.build_profile, data.run_id]
        .filter(Boolean).join(" · ");
      byId("viz-meta").textContent = meta;

      const metrics = [
        ["Nodes", data.metrics.nodes],
        ["Edges", data.metrics.edges],
        ["External", data.metrics.external],
        ["Evidence", data.metrics.evidence],
        ["Resource", data.metrics.resource_items],
        ["Sync", data.metrics.sync_items],
        ["Knowledge", data.metrics.knowledge_entities || 0],
        ["Coverage", data.metrics.coverage == null ? "N/A" : `${(data.metrics.coverage * 100).toFixed(1)}%`]
      ];
      byId("viz-stats").innerHTML = metrics.map(([label, value]) =>
        `<div class="stat"><div class="stat-label">${label}</div><div class="stat-value">${value}</div></div>`
      ).join("");

      const tabs = [...document.querySelectorAll(".tab")];
      tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
          tabs.forEach((item) => item.classList.remove("active"));
          document.querySelectorAll(".panel").forEach((panel) => panel.classList.remove("active"));
          tab.classList.add("active");
          byId(`panel-${tab.dataset.tab}`).classList.add("active");
          if (tab.dataset.tab === "graph") {
            renderFullGraph();
          }
          if (tab.dataset.tab === "knowledge") {
            renderKnowledge();
          }
        });
      });

      function renderFullGraph() {
        const canvas = byId("full-graph-canvas");
        const ctx = canvas.getContext("2d");
        const shell = canvas.parentElement;
        const nodes = data.full_graph.nodes || [];
        const edges = data.full_graph.edges || [];
        const nodeById = Object.fromEntries(nodes.map((node) => [node.id, node]));
        const edgeTargets = new Map();
        const edgeSources = new Map();
        for (const edge of edges) {
          edgeTargets.set(edge.target, (edgeTargets.get(edge.target) || 0) + 1);
          edgeSources.set(edge.source, (edgeSources.get(edge.source) || 0) + 1);
        }

        let view = { tx: 0, ty: 0, scale: 1 };
        let hoveredId = "";
        let selectedId = "";
        let pointerDown = false;
        let lastPointer = null;
        let moved = false;
        let edgeMode = "module";

        function nodeColor(kind) {
          if (kind === "callback") return getComputedStyle(document.documentElement).getPropertyValue("--green").trim();
          if (kind === "external_function") return getComputedStyle(document.documentElement).getPropertyValue("--red").trim();
          return getComputedStyle(document.documentElement).getPropertyValue("--accent").trim();
        }

        function fitGraph() {
          if (!nodes.length) return;
          const xs = nodes.map((node) => node.x);
          const ys = nodes.map((node) => node.y);
          const minX = Math.min(...xs);
          const maxX = Math.max(...xs);
          const minY = Math.min(...ys);
          const maxY = Math.max(...ys);
          const width = shell.clientWidth || 900;
          const height = shell.clientHeight || 620;
          const padding = 70;
          view.scale = Math.min(
            (width - padding * 2) / Math.max(1, maxX - minX),
            (height - padding * 2) / Math.max(1, maxY - minY)
          );
          view.scale = Math.max(0.08, Math.min(1.5, view.scale));
          view.tx = width / 2 - ((minX + maxX) / 2) * view.scale;
          view.ty = height / 2 - ((minY + maxY) / 2) * view.scale;
        }

        function draw() {
          if (!canvas.parentElement) return;
          const dpr = window.devicePixelRatio || 1;
          const width = shell.clientWidth || 900;
          const height = shell.clientHeight || 620;
          canvas.width = Math.max(1, Math.floor(width * dpr));
          canvas.height = Math.max(1, Math.floor(height * dpr));
          canvas.style.width = `${width}px`;
          canvas.style.height = `${height}px`;
          ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
          ctx.clearRect(0, 0, width, height);

          const text = getComputedStyle(document.documentElement).getPropertyValue("--text").trim();
          const muted = getComputedStyle(document.documentElement).getPropertyValue("--muted").trim();
          const border = getComputedStyle(document.documentElement).getPropertyValue("--border").trim();
          if (view.scale < 0.28) {
            drawAggregated(ctx, width, height, text, muted, border);
            return;
          }
          drawDetailed(ctx, width, height, text, muted, border);
        }

        function visibleEdges() {
          if (edgeMode === "selected") {
            return edges.filter((edge) =>
              edge.source === selectedId ||
              edge.target === selectedId ||
              edge.source === hoveredId ||
              edge.target === hoveredId
            );
          }
          if (edgeMode === "module") {
            return edges.filter((edge) => {
              const a = nodeById[edge.source];
              const b = nodeById[edge.target];
              return a && b && a.component !== b.component;
            });
          }
          return edges;
        }

        function drawDetailed(ctx, width, height, text, muted, border) {
          ctx.save();
          ctx.translate(view.tx, view.ty);
          ctx.scale(view.scale, view.scale);

          ctx.lineWidth = 0.85 / view.scale;
          ctx.strokeStyle = muted;
          ctx.globalAlpha = edgeMode === "all" ? 0.11 : 0.22;
          ctx.beginPath();
          for (const edge of visibleEdges()) {
            const a = nodeById[edge.source];
            const b = nodeById[edge.target];
            if (!a || !b) continue;
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
          }
          ctx.stroke();
          ctx.globalAlpha = 1;

          for (const node of nodes) {
            const radius = (node.id === selectedId ? 6 : node.id === hoveredId ? 5 : 3.2) / view.scale;
            ctx.beginPath();
            ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
            ctx.fillStyle = nodeColor(node.kind);
            ctx.fill();
            if (node.id === selectedId || node.id === hoveredId || view.scale > 0.55) {
              ctx.font = `${Math.max(10, 12 / view.scale)}px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
              ctx.fillStyle = text;
              ctx.textAlign = "center";
              ctx.fillText(node.name, node.x, node.y - radius - 3);
            }
          }
          ctx.restore();
        }

        function drawAggregated(ctx, width, height, text, muted, border) {
          const components = data.full_graph.components || [];
          const centers = new Map();
          for (const node of nodes) {
            const item = centers.get(node.component) || {
              id: node.component,
              x: 0,
              y: 0,
              count: 0,
              name: node.component,
            };
            item.x += node.x;
            item.y += node.y;
            item.count += 1;
            centers.set(node.component, item);
          }
          for (const [id, item] of centers) {
            const info = components.find((component) => component.id === id);
            item.name = info?.name || id;
            item.x /= item.count;
            item.y /= item.count;
          }
          const centerById = new Map([...centers.entries()]);

          ctx.save();
          ctx.translate(view.tx, view.ty);
          ctx.scale(view.scale, view.scale);
          ctx.lineWidth = 0.8 / view.scale;
          ctx.strokeStyle = muted;
          ctx.globalAlpha = 0.28;
          ctx.beginPath();
          for (const edge of data.module_edges || []) {
            const a = centerById.get(edge.source);
            const b = centerById.get(edge.target);
            if (!a || !b) continue;
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
          }
          ctx.stroke();
          ctx.globalAlpha = 1;

          for (const item of centers.values()) {
            const radius = 18 + Math.sqrt(item.count) * 3;
            ctx.beginPath();
            ctx.arc(item.x, item.y, radius, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(127,127,127,0.18)";
            ctx.fill();
            ctx.strokeStyle = border;
            ctx.lineWidth = 1 / view.scale;
            ctx.stroke();
            ctx.font = `${12 / view.scale}px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
            ctx.fillStyle = text;
            ctx.textAlign = "center";
            ctx.fillText(item.name, item.x, item.y - 2);
            ctx.font = `${10 / view.scale}px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
            ctx.fillText(item.count, item.x, item.y + 14);
          }
          ctx.restore();

          for (const component of data.full_graph.components || []) {
            const item = centers.get(component.id);
            if (!item) continue;
            const sx = item.x * view.scale + view.tx;
            const sy = item.y * view.scale + view.ty;
            ctx.font = "11px -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
            ctx.fillStyle = border;
            ctx.textAlign = "left";
            ctx.fillText(`${component.name} (${component.count})`, sx + 12, sy - 12);
          }
        }

        function screenToWorld(x, y) {
          return {
            x: (x - view.tx) / view.scale,
            y: (y - view.ty) / view.scale
          };
        }

        function hitNode(x, y) {
          const world = screenToWorld(x, y);
          let nearest = null;
          let best = Infinity;
          for (const node of nodes) {
            const dx = node.x - world.x;
            const dy = node.y - world.y;
            const distance = dx * dx + dy * dy;
            if (distance < best) {
              best = distance;
              nearest = node;
            }
          }
          return nearest && Math.sqrt(best) <= 10 / view.scale ? nearest : null;
        }

        function centerNode(node) {
          const width = shell.clientWidth || 900;
          const height = shell.clientHeight || 620;
          view.scale = Math.max(view.scale, 0.42);
          view.tx = width / 2 - node.x * view.scale;
          view.ty = height / 2 - node.y * view.scale;
          selectedId = node.id;
          const incoming = edgeSources.get(node.id) || 0;
          const outgoing = edgeTargets.get(node.id) || 0;
          byId("graph-detail").textContent =
            `${node.name} · ${node.kind} · ${node.component} · incoming ${incoming} · outgoing ${outgoing}`;
          draw();
        }

        function zoomAt(x, y, factor) {
          const before = screenToWorld(x, y);
          view.scale = Math.max(0.06, Math.min(2.2, view.scale * factor));
          const after = screenToWorld(x, y);
          view.tx += (after.x - before.x) * view.scale;
          view.ty += (after.y - before.y) * view.scale;
          draw();
        }

        canvas.addEventListener("wheel", (event) => {
          event.preventDefault();
          const rect = canvas.getBoundingClientRect();
          zoomAt(event.clientX - rect.left, event.clientY - rect.top, Math.exp(-event.deltaY * 0.0012));
        }, { passive: false });

        canvas.addEventListener("pointerdown", (event) => {
          pointerDown = true;
          moved = false;
          lastPointer = { x: event.clientX, y: event.clientY };
          canvas.classList.add("dragging");
          canvas.setPointerCapture(event.pointerId);
        });
        canvas.addEventListener("pointermove", (event) => {
          const rect = canvas.getBoundingClientRect();
          const x = event.clientX - rect.left;
          const y = event.clientY - rect.top;
          if (pointerDown && lastPointer) {
            view.tx += event.clientX - lastPointer.x;
            view.ty += event.clientY - lastPointer.y;
            lastPointer = { x: event.clientX, y: event.clientY };
            moved = true;
          } else {
            const node = hitNode(x, y);
            hoveredId = node ? node.id : "";
          }
          draw();
        });
        canvas.addEventListener("pointerup", (event) => {
          pointerDown = false;
          canvas.classList.remove("dragging");
          const rect = canvas.getBoundingClientRect();
          if (!moved) {
            const node = hitNode(event.clientX - rect.left, event.clientY - rect.top);
            if (node) centerNode(node);
          }
        });
        byId("graph-zoom-in").addEventListener("click", () => {
          zoomAt(shell.clientWidth / 2, shell.clientHeight / 2, 1.25);
        });
        byId("graph-zoom-out").addEventListener("click", () => {
          zoomAt(shell.clientWidth / 2, shell.clientHeight / 2, 0.8);
        });
        byId("graph-edge-mode").addEventListener("change", (event) => {
          edgeMode = event.target.value;
          draw();
        });
        byId("graph-search").addEventListener("input", (event) => {
          const term = event.target.value.trim().toLowerCase();
          const node = nodes.find((item) =>
            item.name.toLowerCase().includes(term) || item.id.toLowerCase().includes(term)
          );
          if (node) centerNode(node);
        });
        new ResizeObserver(() => draw()).observe(shell);
        fitGraph();
        draw();
      }

      function renderModules() {
        const max = Math.max(1, ...data.modules.map((item) => item.value));
        byId("module-list").innerHTML = data.modules.map((item) =>
          `<div class="module-card">
             <div class="module-name">${item.name}</div>
             <div class="module-bar"><span style="width:${(item.value / max) * 100}%"></span></div>
             <div class="module-meta">${item.value} nodes</div>
           </div>`
        ).join("");
      }

      function renderModuleGraph() {
        const container = byId("module-graph");
        const width = 760;
        const height = 430;
        const cx = width / 2;
        const cy = height / 2;
        const rx = Math.min(320, width / 2 - 80);
        const ry = Math.min(165, height / 2 - 60);
        const maxValue = Math.max(1, ...data.modules.map((item) => item.value));
        const nodes = data.modules.slice(0, 8);
        const byName = Object.fromEntries(nodes.map((item) => [item.id, item]));
        const nodePositions = nodes.map((item, index) => {
          const angle = -Math.PI / 2 + (index / nodes.length) * Math.PI * 2;
          return {
            x: cx + Math.cos(angle) * rx,
            y: cy + Math.sin(angle) * ry
          };
        });
        const edges = data.module_edges
          .filter((edge) => byName[edge.source] && byName[edge.target])
          .slice(0, 80);
        const edgeMax = Math.max(1, ...edges.map((edge) => edge.value));
        const edgePaths = edges.map((edge) => {
          const a = nodePositions[nodes.findIndex((item) => item.id === edge.source)];
          const b = nodePositions[nodes.findIndex((item) => item.id === edge.target)];
          return `<path class="module-edge" d="M${a.x} ${a.y} L${b.x} ${b.y}"
            stroke-width="${Math.max(1, Math.min(6, Math.log2(edge.value + 1) / Math.log2(edgeMax + 1) * 6))}"
            marker-end="url(#arrow)"><title>${edge.source} → ${edge.target}: ${edge.value}</title></path>`;
        }).join("");
        const nodeMarks = nodes.map((item, index) => {
          const pos = nodePositions[index];
          const radius = 17 + Math.sqrt(item.value / maxValue) * 22;
          return `<g class="module-node" data-id="${item.id}" tabindex="0"
            transform="translate(${pos.x} ${pos.y})">
            <circle r="${radius}"></circle>
            <text class="module-label" y="4">${item.name}</text>
            <text class="module-label" y="18" font-size="10">${item.value}</text>
          </g>`;
        }).join("");
        container.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img"
          aria-label="Module call graph">
          <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--muted)"></path>
          </marker></defs>
          ${edgePaths}
          ${nodeMarks}
        </svg>`;

        container.querySelectorAll(".module-node").forEach((node) => {
          node.addEventListener("click", () => {
            container.querySelectorAll(".module-node").forEach((item) => item.classList.remove("selected"));
            node.classList.add("selected");
            const id = node.dataset.id;
            const outgoing = data.module_edges.filter((edge) => edge.source === id);
            const incoming = data.module_edges.filter((edge) => edge.target === id);
            byId("overview-detail").textContent =
              `${id}: ${outgoing.length} outgoing modules, ${incoming.length} incoming modules`;
          });
          node.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              node.click();
            }
          });
        });
      }

      function renderCalls(filter = "") {
        const term = filter.trim().toLowerCase();
        const rows = term
          ? data.calls.filter((call) =>
              `${call.source} ${call.target} ${call.file} ${call.snippet}`.toLowerCase().includes(term)
            )
          : data.calls;
        byId("call-count").textContent = `${rows.length} / ${data.calls.length} calls`;
        byId("call-rows").innerHTML = rows.slice(0, 250).map((call) =>
          `<tr>
             <td>${call.source}</td>
             <td>${call.source_component}</td>
             <td>${call.target}</td>
             <td>${call.kind}</td>
             <td>${call.file}:${call.line}</td>
             <td class="code">${call.snippet}</td>
           </tr>`
        ).join("");
      }

      function renderFindings() {
        const resourceTags = Object.entries(data.resource_flow.types)
          .map(([name, value]) => `<span class="tag">${name} ${value}</span>`).join("");
        const syncTags = Object.entries(data.sync_relations.types)
          .map(([name, value]) => `<span class="tag">${name} ${value}</span>`).join("");
        const paths = data.key_chains.map((path) =>
          `<li>${path.summary || path.source || path.id}${path.termination_reason ? ` · ${path.termination_reason}` : ""}</li>`
        ).join("");
        byId("finding-grid").innerHTML =
          `<div class="finding-card"><h3>Resource Flow</h3>
             <div class="tag-row">${resourceTags || '<span class="tag">not available</span>'}</div>
           </div>
           <div class="finding-card"><h3>Sync Relations</h3>
             <div class="tag-row">${syncTags || '<span class="tag">not available</span>'}</div>
           </div>
           <div class="finding-card"><h3>Key Chains</h3>
             <ul class="path-list">${paths || "<li>None</li>"}</ul>
           </div>
           <div class="finding-card"><h3>Analysis</h3>
             <div class="module-meta">${data.summary || data.analysis.split("\n").slice(0, 2).join(" ")}</div>
           </div>`;
      }

      function renderKnowledge() {
        const knowledge = data.knowledge || {};
        const entities = knowledge.entities || [];
        const relations = knowledge.relations || [];
        const entityById = Object.fromEntries(entities.map((item) => [item.id, item]));
        const kindSelect = byId("knowledge-kind");
        if (kindSelect.options.length === 1) {
          [...new Set(entities.map((item) => item.kind))].sort().forEach((kind) => {
            const option = document.createElement("option");
            option.value = kind;
            option.textContent = kind;
            kindSelect.appendChild(option);
          });
        }
        const term = byId("knowledge-filter").value.trim().toLowerCase();
        const kind = kindSelect.value;
        const filtered = entities.filter((item) => {
          const haystack = `${item.id} ${item.name} ${item.file} ${item.kind}`.toLowerCase();
          return (!term || haystack.includes(term)) && (!kind || item.kind === kind);
        });
        byId("knowledge-count").textContent =
          `${filtered.length} / ${entities.length} entities · ${relations.length} relations`;
        byId("knowledge-rows").innerHTML = filtered.slice(0, 300).map((item) =>
          `<tr>
             <td class="code">${item.id}</td>
             <td>${item.kind}</td>
             <td>${item.name}</td>
             <td class="code">${item.file || ""}${item.line ? `:${item.line}` : ""}</td>
             <td class="code">${JSON.stringify(item.properties || {}).slice(0, 220)}</td>
           </tr>`
        ).join("");
        byId("knowledge-relation-rows").innerHTML = relations.slice(0, 300).map((item) => {
          const source = entityById[item.source];
          const target = entityById[item.target];
          return `<tr>
            <td>${item.type}</td>
            <td>${source?.name || item.source}</td>
            <td>${target?.name || item.target}</td>
          </tr>`;
        }).join("");
      }

      byId("call-filter").addEventListener("input", (event) => renderCalls(event.target.value));
      byId("knowledge-filter").addEventListener("input", () => renderKnowledge());
      byId("knowledge-kind").addEventListener("change", () => renderKnowledge());
      renderFullGraph();
      renderModules();
      renderModuleGraph();
      renderCalls();
      renderFindings();
      renderKnowledge();
    })();
  </script>
</body>
</html>
"""
