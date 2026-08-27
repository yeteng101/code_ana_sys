from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


FIXTURE_DIR = Path(__file__).with_name("fixtures")
DEMO_GRAPH = Path(__file__).resolve().parents[1] / "demo" / "graph.json"
ANALYZER_CONFIG = {
    "engine": "fixture-crg",
    "path_algorithm": "depth-first",
    "chain_confidence": "minimum-edge",
}


class RequestError(ValueError):
    def __init__(self, code: str, message: str, *, target_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.target_id = target_id

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "retryable": False,
        }
        if self.target_id:
            result["target_id"] = self.target_id
        return result


@dataclass(frozen=True)
class PathResult:
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...]
    complete: bool
    termination_reason: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def make_run_id(request: dict[str, Any]) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = stable_digest(request)[:12]
    return f"run_{stamp}_{suffix}"


def _is_safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_request(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise RequestError("INVALID_REQUEST", "请求体必须是 JSON object")

    for field in ("schema_version", "task_id", "action", "repository", "targets", "analysis"):
        if field not in request:
            raise RequestError("INVALID_REQUEST", f"缺少必填字段: {field}")

    if request["action"] != "get_call_chains":
        raise RequestError("INVALID_REQUEST", "action 必须为 get_call_chains")
    if not isinstance(request["task_id"], str) or not request["task_id"].strip():
        raise RequestError("INVALID_REQUEST", "task_id 必须是非空字符串")

    repository = request["repository"]
    if not isinstance(repository, dict):
        raise RequestError("INVALID_REQUEST", "repository 必须是 object")
    for field in ("provider", "name", "commit_sha"):
        if not isinstance(repository.get(field), str) or not repository[field].strip():
            raise RequestError("INVALID_REQUEST", f"repository.{field} 必须是非空字符串")
    if len(repository["commit_sha"]) < 7:
        raise RequestError("INVALID_REQUEST", "repository.commit_sha 至少为 7 个字符")

    targets = request["targets"]
    if not isinstance(targets, list) or not targets:
        raise RequestError("INVALID_TARGETS", "targets 不能为空")
    seen_target_ids: set[str] = set()
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            raise RequestError("INVALID_TARGETS", f"targets[{index}] 必须是 object")
        for field in ("target_id", "type", "name", "location", "role"):
            if field not in target:
                raise RequestError("INVALID_TARGETS", f"targets[{index}] 缺少字段: {field}")
        target_id = target["target_id"]
        if not isinstance(target_id, str) or not target_id:
            raise RequestError("INVALID_TARGETS", f"targets[{index}].target_id 必须是非空字符串")
        if target_id in seen_target_ids:
            raise RequestError("INVALID_TARGETS", f"target_id 重复: {target_id}")
        seen_target_ids.add(target_id)
        location = target["location"]
        if not isinstance(location, dict) or not isinstance(location.get("file"), str):
            raise RequestError("INVALID_TARGETS", f"targets[{index}].location.file 缺失")
        if not _is_safe_relative_path(location["file"]):
            raise RequestError("INVALID_TARGETS", f"目标路径必须相对仓库根且不能包含 ..: {location['file']}")
        if "line" not in location and "start_line" not in location:
            raise RequestError("INVALID_TARGETS", f"targets[{index}].location 必须提供 line 或 start_line")

    analysis = request["analysis"]
    if not isinstance(analysis, dict):
        raise RequestError("INVALID_REQUEST", "analysis 必须是 object")
    if analysis.get("direction") not in {"forward", "backward", "both"}:
        raise RequestError("INVALID_REQUEST", "analysis.direction 必须是 forward/backward/both")
    for field, default, limit in (("max_depth", 8, 20), ("max_paths_per_target", 20, 100)):
        value = analysis.get(field, default)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise RequestError("INVALID_REQUEST", f"analysis.{field} 必须是正整数")
        if value > limit:
            raise RequestError("INVALID_REQUEST", f"analysis.{field} 超过 Demo 上限 {limit}")

    normalized = copy.deepcopy(request)
    normalized["analysis"].setdefault("max_depth", 8)
    normalized["analysis"].setdefault("max_paths_per_target", 20)
    normalized["analysis"].setdefault("include_callbacks", True)
    normalized["analysis"].setdefault("include_indirect_calls", True)
    normalized["analysis"].setdefault("include_external_calls", False)
    normalized["analysis"].setdefault("build_profile", "default")
    return normalized


class FixtureGraph:
    def __init__(self, payload: dict[str, Any]):
        self.payload = payload
        self.nodes = {node["node_id"]: node for node in payload["nodes"]}
        self.edges = {edge["edge_id"]: edge for edge in payload["edges"]}
        self.evidence = {item["id"]: item for item in payload["evidence"]}
        self.outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for edge in payload["edges"]:
            self.outgoing[edge["source_node_id"]].append(edge)
            self.incoming[edge["target_node_id"]].append(edge)
        for values in (self.outgoing, self.incoming):
            for edge_list in values.values():
                edge_list.sort(key=lambda item: item["edge_id"])

    @classmethod
    def load_for_repository(cls, repository_name: str) -> "FixtureGraph":
        aliases = {
            "redis/redis": "redis.json",
            "libuv/libuv": "libuv.json",
        }
        key = repository_name.lower()
        if key == "clang-pipeline-demo":
            with DEMO_GRAPH.open(encoding="utf-8") as stream:
                payload = _graph_schema_to_fixture(json.load(stream))
            return cls(payload)
        filename = aliases.get(key)
        if not filename:
            raise RequestError("REPOSITORY_NOT_FOUND", f"Demo 没有仓库 {repository_name} 的 CRG fixture")
        with (FIXTURE_DIR / filename).open(encoding="utf-8") as stream:
            return cls(json.load(stream))

    def resolve_target(self, target: dict[str, Any]) -> tuple[str | None, list[str], str]:
        node_id = target.get("node_id")
        if node_id:
            if node_id in self.nodes:
                return node_id, [], "unique"
            return None, [], "unresolved"

        candidates = []
        requested_file = target["location"]["file"]
        requested_signature = target.get("signature")
        for node in self.nodes.values():
            if node["name"] != target["name"] or node["type"] != target["type"]:
                continue
            if requested_file and node["location"]["file"] != requested_file:
                continue
            if requested_signature and node.get("signature") != requested_signature:
                continue
            candidates.append(node["node_id"])
        candidates.sort()
        if len(candidates) == 1:
            return candidates[0], [], "unique"
        if len(candidates) > 1:
            return None, candidates, "multiple_candidates"
        return None, [], "unresolved"

    @staticmethod
    def _edge_allowed(edge: dict[str, Any], analysis: dict[str, Any]) -> bool:
        if edge["type"] == "callback_edge" and not analysis["include_callbacks"]:
            return False
        if edge["type"] == "indirect_call" and not analysis["include_indirect_calls"]:
            return False
        if edge["type"] == "external" and not analysis["include_external_calls"]:
            return False
        return True

    def _walk(
        self,
        root_node_id: str,
        direction: str,
        analysis: dict[str, Any],
    ) -> tuple[list[PathResult], int]:
        max_depth = analysis["max_depth"]
        max_paths = analysis["max_paths_per_target"]
        adjacency = self.outgoing if direction == "forward" else self.incoming
        results: list[PathResult] = []
        truncated = 0

        def visit(current: str, node_path: list[str], edge_path: list[str]) -> None:
            nonlocal truncated
            if len(results) >= max_paths:
                truncated += 1
                return
            if len(edge_path) >= max_depth:
                results.append(PathResult(tuple(node_path), tuple(edge_path), False, "max_depth"))
                truncated += 1
                return

            candidates = [edge for edge in adjacency.get(current, []) if self._edge_allowed(edge, analysis)]
            if not candidates:
                node = self.nodes[current]
                reason = "external_call" if node["type"] == "external" else "leaf"
                results.append(PathResult(tuple(node_path), tuple(edge_path), True, reason))
                return

            progressed = False
            for edge in candidates:
                next_node = edge["target_node_id"] if direction == "forward" else edge["source_node_id"]
                if next_node in node_path:
                    results.append(PathResult(tuple(node_path), tuple(edge_path), False, "cycle"))
                    continue
                progressed = True
                visit(next_node, node_path + [next_node], edge_path + [edge["edge_id"]])
            if not progressed and not results:
                results.append(PathResult(tuple(node_path), tuple(edge_path), True, "leaf"))

        visit(root_node_id, [root_node_id], [])
        return results, truncated

    def query_paths(
        self,
        root_node_id: str,
        analysis: dict[str, Any],
    ) -> tuple[list[tuple[str, PathResult]], int]:
        directions = [analysis["direction"]]
        if analysis["direction"] == "both":
            directions = ["backward", "forward"]
        paths: list[tuple[str, PathResult]] = []
        truncated = 0
        for direction in directions:
            found, count = self._walk(root_node_id, direction, analysis)
            paths.extend((direction, item) for item in found)
            truncated += count
        return paths, truncated


def _graph_schema_to_fixture(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = []
    for node in graph.get("nodes", []):
        node_type = {
            "function": "function",
            "callback": "callback",
            "event_source": "event_source",
            "module": "module",
            "external": "external",
        }.get(node.get("kind"), node.get("kind", "function"))
        nodes.append(
            {
                "node_id": node["id"],
                "type": node_type,
                "name": node["name"],
                "qualified_name": node["id"].removeprefix("fn:").removeprefix("cb:"),
                "signature": node.get("signature"),
                "location": {"file": node["file"], "line": node["line"]},
                "evidence_ids": [],
            }
        )
    edges = []
    for edge in graph.get("edges", []):
        context = edge.get("execution_context")
        execution_context = {
            "process": None,
            "thread": None,
            "event_loop": context if isinstance(context, str) else None,
            "async_boundary": edge.get("kind") in {"callback_edge", "indirect_call"},
        }
        edges.append(
            {
                "edge_id": edge["id"],
                "source_node_id": edge["source"],
                "target_node_id": edge["target"],
                "type": edge.get("kind", "direct_call"),
                "call_site": edge.get("call_site") or {"file": "", "line": 1},
                "condition": edge.get("condition"),
                "execution_context": execution_context,
                "confidence": edge["confidence"],
                "evidence_ids": edge.get("evidence_ids", []),
                "candidate_node_ids": [],
            }
        )
    return {
        "schema_version": graph.get("schema_version", "1.0"),
        "run_id": graph.get("run_id", ""),
        "graph_snapshot_id": "clang-pipeline-demo-v1",
        "nodes": nodes,
        "edges": edges,
        "evidence": graph.get("evidence", []),
    }


def _chain_from_path(
    graph: FixtureGraph,
    target: dict[str, Any],
    root_node_id: str,
    query_direction: str,
    path: PathResult,
    index: int,
) -> dict[str, Any]:
    node_ids = list(path.node_ids)
    edge_ids = list(path.edge_ids)
    if query_direction == "backward":
        node_ids.reverse()
        edge_ids.reverse()

    nodes = [copy.deepcopy(graph.nodes[node_id]) for node_id in node_ids]
    edges = [copy.deepcopy(graph.edges[edge_id]) for edge_id in edge_ids]
    edge_confidences = [edge["confidence"] for edge in edges]
    evidence_ids: list[str] = []
    for edge in edges:
        for evidence_id in edge["evidence_ids"]:
            if evidence_id not in evidence_ids:
                evidence_ids.append(evidence_id)
    if not evidence_ids:
        declaration_ids = graph.nodes[root_node_id].get("evidence_ids", [])
        evidence_ids.extend(declaration_ids)

    candidate_ids: list[str] = []
    resolution_status = "unique"
    for edge in edges:
        candidates = edge.get("candidate_node_ids", [])
        if candidates:
            resolution_status = "multiple_candidates" if len(candidates) > 1 else "unique"
            for candidate in candidates:
                if candidate not in candidate_ids:
                    candidate_ids.append(candidate)

    complete = path.complete
    termination_reason = path.termination_reason
    if resolution_status == "multiple_candidates":
        complete = False
        termination_reason = "unresolved_indirect_call"

    return {
        "id": f"finding_{target['target_id']}_{index:03d}",
        "kind": "call_chain",
        "target_id": target["target_id"],
        "root_node_id": root_node_id,
        "direction": "caller_to_callee",
        "query_direction": query_direction,
        "nodes": nodes,
        "edges": edges,
        "complete": complete,
        "termination_reason": termination_reason,
        "resolution": {
            "status": resolution_status,
            "candidate_node_ids": candidate_ids,
        },
        "confidence": min(edge_confidences, default=1.0),
        "evidence_ids": evidence_ids,
    }


def analyze_call_chains(raw_request: Any, *, run_id: str | None = None) -> dict[str, Any]:
    request = validate_request(raw_request)
    run_id = run_id or make_run_id(request)
    graph = FixtureGraph.load_for_repository(request["repository"]["name"])
    analysis = request["analysis"]

    findings: list[dict[str, Any]] = []
    unresolved_targets: list[dict[str, Any]] = []
    resolved_total = 0
    truncated_total = 0
    chain_index = 1

    for target in request["targets"]:
        node_id, candidates, status = graph.resolve_target(target)
        if not node_id:
            unresolved_targets.append(
                {
                    "target_id": target["target_id"],
                    "reason": "目标节点存在歧义" if status == "multiple_candidates" else "目标节点未找到",
                    "candidate_node_ids": candidates,
                }
            )
            continue
        resolved_total += 1
        paths, truncated = graph.query_paths(node_id, analysis)
        truncated_total += truncated
        for query_direction, path in paths:
            findings.append(_chain_from_path(graph, target, node_id, query_direction, path, chain_index))
            chain_index += 1

    used_evidence_ids = {
        evidence_id
        for finding in findings
        for evidence_id in finding["evidence_ids"]
    }
    for finding in findings:
        for node in finding["nodes"]:
            used_evidence_ids.update(node.get("evidence_ids", []))
    evidence = [copy.deepcopy(item) for evidence_id, item in graph.evidence.items() if evidence_id in used_evidence_ids]
    evidence.sort(key=lambda item: item["id"])

    unresolved_indirect = sum(
        1 for finding in findings if finding["resolution"]["status"] != "unique"
    )
    roots_total = len(request["targets"])
    coverage_complete = (
        resolved_total == roots_total
        and truncated_total == 0
        and unresolved_indirect == 0
        and all(item["complete"] for item in findings)
    )
    if graph.payload["graph_snapshot_id"] == "clang-pipeline-demo-v1":
        warnings = [
            "调用图来自 clang_pipeline 的 Clang AST 产物，证据行号来自 demo/sample 真实源码。"
        ]
    else:
        warnings = [
            "Demo 使用内置 CRG fixture 验证接口；替换为 Clang 产物后才能作为真实源码分析结论。"
        ]
    if unresolved_targets:
        warnings.append(f"有 {len(unresolved_targets)} 个目标未解析")
    if unresolved_indirect:
        warnings.append(f"有 {unresolved_indirect} 条链包含多个间接调用候选")

    status = "succeeded"
    if resolved_total == 0:
        status = "failed"
    elif not coverage_complete:
        status = "partial"
    errors = [
        {
            "code": "TARGET_NOT_FOUND",
            "message": item["reason"],
            "retryable": False,
            "target_id": item["target_id"],
        }
        for item in unresolved_targets
    ]

    context_config = {
        **ANALYZER_CONFIG,
        "fixture": graph.payload["graph_snapshot_id"],
        "build_profile": analysis["build_profile"],
    }
    result = {
        "schema_version": "1.0",
        "run_id": run_id,
        "task_id": request["task_id"],
        "status": status,
        "generated_at": utc_now(),
        "analysis_context": {
            "repository": request["repository"]["name"],
            "commit_sha": request["repository"]["commit_sha"],
            "graph_snapshot_id": request["repository"].get("graph_snapshot_id", graph.payload["graph_snapshot_id"]),
            "build_profile": analysis["build_profile"],
            "analyzer": {
                "name": "code-reverse-agent-demo",
                "version": "0.1.0",
                "config_sha256": stable_digest(context_config),
            },
        },
        "target_resolution": {
            "requested_total": roots_total,
            "resolved_total": resolved_total,
            "unresolved_targets": unresolved_targets,
        },
        "findings": findings,
        "evidence": evidence,
        "coverage": {
            "complete": coverage_complete,
            "roots_total": roots_total,
            "roots_analyzed": resolved_total,
            "targets_total": roots_total,
            "targets_analyzed": resolved_total,
            "truncated_chains": truncated_total,
            "unresolved_indirect_calls": unresolved_indirect,
            "skipped_files": [],
            **({"reason": "存在未解析目标、间接调用或被截断的链"} if not coverage_complete else {}),
        },
        "warnings": warnings,
        "errors": errors,
    }
    validate_result(result)
    return result


def validate_result(result: dict[str, Any]) -> None:
    evidence_ids = {item["id"] for item in result["evidence"]}
    if len(evidence_ids) != len(result["evidence"]):
        raise AssertionError("evidence id 必须唯一")
    finding_ids: set[str] = set()
    known_nodes: dict[str, dict[str, Any]] = {}
    known_edges: dict[str, dict[str, Any]] = {}

    for finding in result["findings"]:
        if finding["id"] in finding_ids:
            raise AssertionError(f"finding id 重复: {finding['id']}")
        finding_ids.add(finding["id"])
        nodes = finding["nodes"]
        edges = finding["edges"]
        if len(nodes) != len(edges) + 1:
            raise AssertionError(f"{finding['id']}: nodes 数量必须等于 edges + 1")
        for node in nodes:
            previous = known_nodes.setdefault(node["node_id"], node)
            if previous != node:
                raise AssertionError(f"同一 node_id 的定义不一致: {node['node_id']}")
            file_path = node["location"]["file"]
            if not _is_safe_relative_path(file_path):
                raise AssertionError(f"节点包含非法路径: {file_path}")
            if not set(node.get("evidence_ids", [])).issubset(evidence_ids):
                raise AssertionError(f"{node['node_id']}: 引用了不存在的 evidence")
        for index, edge in enumerate(edges):
            if edge["source_node_id"] != nodes[index]["node_id"]:
                raise AssertionError(f"{edge['edge_id']}: source_node_id 与路径不一致")
            if edge["target_node_id"] != nodes[index + 1]["node_id"]:
                raise AssertionError(f"{edge['edge_id']}: target_node_id 与路径不一致")
            previous = known_edges.setdefault(edge["edge_id"], edge)
            if previous != edge:
                raise AssertionError(f"同一 edge_id 的定义不一致: {edge['edge_id']}")
            if not set(edge["evidence_ids"]).issubset(evidence_ids):
                raise AssertionError(f"{edge['edge_id']}: 引用了不存在的 evidence")
            if not _is_safe_relative_path(edge["call_site"]["file"]):
                raise AssertionError(f"边包含非法路径: {edge['call_site']['file']}")
            if finding["confidence"] > edge["confidence"]:
                raise AssertionError(f"{finding['id']}: 链置信度高于边置信度")
        if not set(finding["evidence_ids"]).issubset(evidence_ids):
            raise AssertionError(f"{finding['id']}: 引用了不存在的 evidence")
        if not finding["complete"] and not finding.get("termination_reason"):
            raise AssertionError(f"{finding['id']}: 非完整链缺少 termination_reason")


def summarize_findings(result: dict[str, Any]) -> Iterable[str]:
    for finding in result["findings"]:
        names = " -> ".join(node["name"] for node in finding["nodes"])
        yield f"{finding['query_direction']}: {names} ({finding['confidence']:.2f})"
