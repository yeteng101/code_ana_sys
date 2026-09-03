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

    def _run(self, statements: list[tuple[str, dict[str, Any]]]) -> None:
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
                        "MATCH (r:CALLS {run_id:$run_id, id:$edge_id}) "
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
