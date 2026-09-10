from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from typing import Any


class GraphStoreError(RuntimeError):
    pass


class Neo4jGraphStore:
    def __init__(
        self,
        *,
        uri: str | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str = "neo4j",
    ) -> None:
        self.uri = (uri or os.environ.get("NEO4J_URI", "http://127.0.0.1:7474")).rstrip("/")
        self.user = user or os.environ.get("NEO4J_USER", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASSWORD", "")
        self.database = database
        if not self.password:
            raise GraphStoreError("缺少 NEO4J_PASSWORD")

    def _run(self, statements: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
        url = f"{self.uri}/db/{self.database}/tx/commit"
        payload = {
            "statements": [
                {"statement": statement, "parameters": parameters}
                for statement, parameters in statements
            ]
        }
        token = base64.b64encode(f"{self.user}:{self.password}".encode("utf-8")).decode("ascii")
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GraphStoreError(f"Neo4j 请求失败: {exc.code} {detail}") from exc
        errors = data.get("errors") or []
        if errors:
            raise GraphStoreError(f"Neo4j 执行失败: {json.dumps(errors, ensure_ascii=False)}")
        return data

    def query(
        self,
        statement: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        data = self._run([(statement, parameters or {})])
        results = data.get("results") or []
        if not results:
            return []
        result = results[0]
        columns = result.get("columns") or []
        rows = result.get("data") or []
        return [
            dict(zip(columns, item.get("row") or []))
            for item in rows
            if isinstance(item, dict)
        ]

    def store_graph(self, graph: dict[str, Any], run_id: str) -> dict[str, int]:
        statements: list[tuple[str, dict[str, Any]]] = []
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        evidence = graph.get("evidence", [])
        for node in nodes:
            statements.append(
                (
                    "MERGE (n:CodeNode {run_id:$run_id, id:$id}) "
                    "SET n.kind=$kind, n.name=$name, n.file=$file, n.line=$line",
                    {
                        "run_id": run_id,
                        "id": node.get("id", ""),
                        "kind": node.get("kind", ""),
                        "name": node.get("name", ""),
                        "file": node.get("file", ""),
                        "line": int(node.get("line", 0)),
                    },
                )
            )
        for item in evidence:
            location = item.get("location") or {}
            statements.append(
                (
                    "MERGE (e:Evidence {run_id:$run_id, id:$id}) "
                    "SET e.kind=$kind, e.file=$file, e.line=$line, e.snippet=$snippet",
                    {
                        "run_id": run_id,
                        "id": item.get("id", ""),
                        "kind": item.get("kind", ""),
                        "file": location.get("file", ""),
                        "line": int(location.get("line", 0)),
                        "snippet": location.get("snippet", ""),
                    },
                )
            )
        for edge in edges:
            call_site = edge.get("call_site") or {}
            statements.append(
                (
                    "MATCH (a:CodeNode {run_id:$run_id, id:$source}) "
                    "MATCH (b:CodeNode {run_id:$run_id, id:$target}) "
                    "MERGE (a)-[r:CALLS {run_id:$run_id, id:$edge_id}]->(b) "
                    "SET r.kind=$kind, r.confidence=$confidence, "
                    "r.file=$file, r.line=$line",
                    {
                        "run_id": run_id,
                        "source": edge.get("source", ""),
                        "target": edge.get("target", ""),
                        "edge_id": edge.get("id", ""),
                        "kind": edge.get("kind", ""),
                        "confidence": float(edge.get("confidence", 0)),
                        "file": call_site.get("file", ""),
                        "line": int(call_site.get("line", 0)),
                    },
                )
            )
            for evidence_id in edge.get("evidence_ids", []):
                statements.append(
                    (
                        "MATCH (:CodeNode {run_id:$run_id})-[r:CALLS {run_id:$run_id, id:$edge_id}]->"
                        "(:CodeNode {run_id:$run_id}) "
                        "MATCH (e:Evidence {run_id:$run_id, id:$evidence_id}) "
                        "MERGE (r)-[:HAS_EVIDENCE]->(e)",
                        {
                            "run_id": run_id,
                            "edge_id": edge.get("id", ""),
                            "evidence_id": evidence_id,
                        },
                    )
                )
        for index in range(0, len(statements), 200):
            self._run(statements[index : index + 200])
        return {
            "nodes": len(nodes),
            "edges": len(edges),
            "evidence": len(evidence),
        }

    def verify_graph(
        self,
        graph: dict[str, Any],
        run_id: str,
    ) -> dict[str, Any]:
        expected = {
            "nodes": len(graph.get("nodes", [])),
            "edges": len(graph.get("edges", [])),
            "evidence": len(graph.get("evidence", [])),
            "edges_with_evidence": sum(
                1 for edge in graph.get("edges", []) if edge.get("evidence_ids")
            ),
        }
        checks: list[dict[str, Any]] = []

        def scalar(name: str, statement: str) -> int:
            rows = self.query(statement, {"run_id": run_id})
            value = int(rows[0].get("count", 0)) if rows else 0
            checks.append(
                {
                    "name": name,
                    "expected": expected.get(name),
                    "actual": value,
                    "passed": value == expected.get(name),
                }
            )
            return value

        actual = {
            "nodes": scalar(
                "nodes",
                "MATCH (n:CodeNode {run_id:$run_id}) RETURN count(n) AS count",
            ),
            "edges": scalar(
                "edges",
                "MATCH (:CodeNode {run_id:$run_id})-[r:CALLS {run_id:$run_id}]->"
                "(:CodeNode {run_id:$run_id}) RETURN count(r) AS count",
            ),
            "evidence": scalar(
                "evidence",
                "MATCH (e:Evidence {run_id:$run_id}) RETURN count(e) AS count",
            ),
            "edges_with_evidence": scalar(
                "edges_with_evidence",
                "MATCH (:CodeNode {run_id:$run_id})-[r:CALLS {run_id:$run_id}]->"
                "(:CodeNode {run_id:$run_id})-[:HAS_EVIDENCE]->"
                "(:Evidence {run_id:$run_id}) RETURN count(DISTINCT r) AS count",
            ),
        }

        entry_rows = self.query(
            "MATCH (a:CodeNode {run_id:$run_id, name:$name})-[r:CALLS {run_id:$run_id}]->"
            "(b:CodeNode) RETURN b.name AS name, b.kind AS kind, r.kind AS edge_kind "
            "ORDER BY b.name LIMIT 20",
            {"run_id": run_id, "name": "uv_run"},
        )
        result = {
            "status": "verified" if all(check["passed"] for check in checks) else "failed",
            "run_id": run_id,
            "expected": expected,
            "actual": actual,
            "checks": checks,
            "sample_uv_run_targets": entry_rows,
        }
        return result


def store_graph_json(
    graph: dict[str, Any],
    run_id: str,
    *,
    uri: str | None = None,
    user: str | None = None,
    password: str | None = None,
) -> dict[str, int]:
    store = Neo4jGraphStore(uri=uri, user=user, password=password)
    return store.store_graph(graph, run_id)


def verify_graph_json(
    graph: dict[str, Any],
    run_id: str,
    *,
    uri: str | None = None,
    user: str | None = None,
    password: str | None = None,
) -> dict[str, Any]:
    store = Neo4jGraphStore(uri=uri, user=user, password=password)
    return store.verify_graph(graph, run_id)
