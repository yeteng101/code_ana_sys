#!/usr/bin/env python3
"""Normalize checked-in annotations; this command never reads analyzer predictions."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.benchmark import ROOT, read, write
from scripts.export_validation import OP_KIND


def sync_cases(data):
    cases = []
    for s in data["samples"]:
        ev = {e["id"]: e for e in s["evidence"]}
        a = ev[s["source"]["evidence_ids"][0]]
        b = ev[s["target"]["evidence_ids"][0]]
        identity = [s["source"]["function"], s["target"]["function"], a["file"], a["line"], b["file"], b["line"], s["condition"]]
        base = {"id": s["id"], "category": "sync_relation", "identity": identity,
                "kind": s["order"], "expected_exists": True, "evidence": s["evidence"],
                "notes": s["reason"], "condition": s["condition"]}
        cases.append(base)
        if s["claim_order"] != s["order"]:
            cases.append({**base, "id": s["id"] + "_rejected_claim", "kind": s["claim_order"], "expected_exists": False})
    return cases


def prepare():
    review = {"human_review": "pending", "method": "existing annotations plus AI source review",
              "limitation": "Legacy libuv call labels were selected against the same graph; regression scores are not independent accuracy estimates."}
    libuv = {"schema_version": "1.0", "dataset_id": "libuv-baseline-v1", "review": review,
             "repository": "libuv/libuv", "commit": "8fb9cb919489a48880680a56efecff6a7dfb4504", "cases": []}
    for s in read(ROOT / "validation/call-chains/dataset.json")["samples"]:
        if s["graph"] != "demo/libuv/graph.json":
            continue
        c = s["claim"]
        libuv["cases"].append({"id": s["id"], "category": "call_chain", "identity": [c["source"], c["target"]],
                               "kind": c["kind"], "expected_exists": s["expected_exists"], "evidence": s["evidence"],
                               "notes": s.get("notes", "")})
    for resource in read(ROOT / "validation/resource-flow/dataset.json")["resources"]:
        if resource.get("repository") != "libuv/libuv":
            continue
        for op in resource["operations"]:
            loc = op["location"]
            libuv["cases"].append({"id": resource["id"] + "_" + op["operation_id"], "category": "resource_flow",
                                   "identity": [resource["id"], op["function"], loc["file"], loc["line"]],
                                   "kind": OP_KIND[op["kind"]], "expected_exists": True, "evidence": [loc],
                                   "notes": "Operation fact, not a final defect classification."})
    libuv["cases"] += sync_cases(read(ROOT / "validation/sync-relations/dataset.json"))
    write(ROOT / "validation/benchmarks/libuv/ground-truth.json", libuv)
    redis_calls = read(ROOT / "validation/redis/call-chains.json")
    redis = {"schema_version": "1.0", "dataset_id": "redis-7.2.4-baseline-v1",
             "repository": "redis/redis", "commit": redis_calls["commit"],
             "review": redis_calls["review"], "cases": redis_calls["cases"] + sync_cases(read(ROOT / "validation/redis/sync-relations.json"))}
    write(ROOT / "validation/benchmarks/redis/ground-truth.json", redis)


if __name__ == "__main__":
    prepare()
