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

from clang_pipeline.agent import AgentContext
from clang_pipeline.graph_store import Neo4jGraphStore, store_graph_json


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
    payload = {
        "status": verification["status"],
        "run_id": args.run_id,
        "written": counts,
        "verification": verification,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if verification["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
