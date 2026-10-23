#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from clang_pipeline.agent import AgentContext, AgentToolError
from clang_pipeline.graph_store import (
    Neo4jGraphStore,
    store_graph_json,
    store_knowledge_graph_json,
)


def wait_for_neo4j(store: Neo4jGraphStore, timeout: int = 180) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            store.query("RETURN 1 AS ok")
            return
        except Exception:
            if time.monotonic() >= deadline:
                raise
            time.sleep(2)


def main() -> int:
    parser = argparse.ArgumentParser(description="写入并回查 Neo4j 调用图")
    parser.add_argument("--workspace", default="demo/libuv")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--run-id", default="run_libuv_1.50.0")
    parser.add_argument("--uri", default="")
    parser.add_argument("--user", default="")
    parser.add_argument("--password", default="")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    ctx = AgentContext(
        Path(args.workspace).resolve(),
        repo_root=Path(args.repo_root).resolve(),
        run_id=args.run_id,
    )
    graph = ctx.load_graph()
    store = Neo4jGraphStore(
        uri=args.uri or None,
        user=args.user or None,
        password=args.password or None,
    )
    wait_for_neo4j(store, timeout=args.timeout)
    counts = store_graph_json(
        graph,
        args.run_id,
        uri=args.uri or None,
        user=args.user or None,
        password=args.password or None,
    )
    verification = store.verify_graph(graph, args.run_id)
    knowledge_verification = None
    knowledge_counts = None
    try:
        knowledge = ctx.load_knowledge_graph()
    except AgentToolError:
        knowledge = None
    if knowledge is not None:
        knowledge_counts = store_knowledge_graph_json(
            knowledge,
            args.run_id,
            uri=args.uri or None,
            user=args.user or None,
            password=args.password or None,
        )
        knowledge_verification = store.verify_knowledge_graph(knowledge, args.run_id)
    payload = {
        "status": (
            "verified"
            if verification["status"] == "verified"
            and (
                knowledge_verification is None
                or knowledge_verification.get("status") in {"verified", "not_available"}
            )
            else "failed"
        ),
        "run_id": args.run_id,
        "written": counts,
        "verification": verification,
        "knowledge_written": knowledge_counts,
        "knowledge_verification": knowledge_verification,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
