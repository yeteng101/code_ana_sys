#!/usr/bin/env python3
"""Export analyzer facts or explicitly identified reviewed annotations."""
import argparse
import copy
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validation.benchmark import FILES, read, validate_external, write


def envelope(category, run_id, source, origin):
    return {"schema_version": "1.0", "run_id": run_id, "result_type": category,
            "status": "partial" if category == "call_chain" else "not_available",
            "source": source, "origin": origin, "items": [], "evidence": [], "warnings": []}


def export_graph(graph, verification=None):
    docs = {k: envelope(k, graph["run_id"], graph.get("meta", {}), "analyzer") for k in FILES}
    doc = docs["call_chain"]
    evidence = {e["id"]: e for e in graph["evidence"]}
    nodes = {n["id"]: n for n in graph["nodes"]}
    verdicts = {}
    for check in (verification or {}).get("checks", []):
        edge_id = check.get("claim", "").split(": ", 1)[0]
        verdicts[edge_id] = {"confirmed": "confirmed", "refuted": "refuted"}.get(check.get("result"), "unconfirmed")
    for edge in graph["edges"]:
        e = copy.deepcopy(edge)
        if not e.get("evidence_ids") or any(x not in evidence for x in e["evidence_ids"]):
            raise ValueError(f"edge {e['id']} lacks resolvable evidence")
        e["status"] = verdicts.get(e["id"], "unconfirmed")
        item = {"id": e["id"], "entry": e["source"], "direction": "caller_to_callee",
                "nodes": [nodes[x] for x in dict.fromkeys([e["source"], e["target"]])], "edges": [e],
                "confidence": e["confidence"], "evidence_ids": e["evidence_ids"], "status": e["status"]}
        doc["items"].append(item)
    doc["evidence"] = graph["evidence"]
    doc["warnings"].append("Absent per-edge verification remains unconfirmed; confidence is not a verification verdict.")
    for k in ("resource_flow", "sync_relation"):
        docs[k]["warnings"].append("Current seven-stage analyzer has no native extractor for this result type. Ground truth is not substituted.")
    return docs


OP_KIND = {"acquire": "acquire", "use": "hold", "retain": "hold", "release": "release",
           "drop_ref": "release", "transfer": "transfer", "borrow": "hold", "escape": "transfer", "invalidate": "release"}


def reviewed_resources(dataset, doc):
    doc["origin"] = "reviewed_annotations_not_analyzer_predictions"
    doc["status"] = "partial"
    doc["warnings"] = ["Operation facts only; defect classifications are not exported. Review metadata is preserved."]
    for resource in dataset["resources"]:
        if resource.get("repository") != "libuv/libuv":
            continue
        operations = []
        for op in resource["operations"]:
            operations.append({"kind": OP_KIND[op["kind"]], "original_kind": op["kind"],
                               "function": op["function"], **op["location"], "evidence_ids": op["evidence_ids"],
                               "confidence": resource["confidence"], "status": "unconfirmed"})
        family = resource["family"]
        doc["items"].append({"id": resource["id"], "resource": resource["id"],
                             "resource_type": family if family in {"file_descriptor", "memory", "lock", "connection", "handle", "reference"} else "other",
                             "operations": operations, "owner": resource.get("ownership_model"), "thread": None,
                             "confidence": resource["confidence"], "status": "unconfirmed",
                             "evidence_ids": [e["id"] for e in resource["evidence"]],
                             "review": resource.get("ground_truth", {}).get("review", "unspecified")})
        doc["evidence"].extend(resource["evidence"])


def reviewed_sync(dataset, doc):
    doc["origin"] = "reviewed_annotations_not_analyzer_predictions"
    doc["status"] = "partial"
    doc["review"] = dataset["review"]
    doc["warnings"] = ["Source-reviewed conditions must accompany each relation; human review is pending."]
    for s in dataset["samples"]:
        endpoints = []
        ev = {e["id"]: e for e in s["evidence"]}
        for k in ("source", "target"):
            endpoint = copy.deepcopy(s[k])
            endpoint.update({x: ev[endpoint["evidence_ids"][0]][x] for x in ("file", "line", "snippet")})
            endpoints.append(endpoint)
        doc["items"].append({"id": s["id"], "relation_type": s["relation_type"],
                             "source": endpoints[0], "target": endpoints[1], "order": s["order"],
                             "condition": s["condition"], "execution_context": {"source_thread": s["source"]["thread"], "target_thread": s["target"]["thread"]},
                             "confidence": s["confidence"], "status": "unconfirmed",
                             "evidence_ids": list(ev)})
        doc["evidence"].extend(s["evidence"])


def save(docs, output):
    for category, doc in docs.items():
        validate_external(doc, category)
        write(Path(output) / (FILES[category] + ".json"), doc)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--graph", type=Path, required=True)
    p.add_argument("--verification", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--reviewed-resources", type=Path)
    p.add_argument("--reviewed-sync", type=Path)
    a = p.parse_args()
    docs = export_graph(read(a.graph), read(a.verification) if a.verification else None)
    if a.reviewed_resources:
        reviewed_resources(read(a.reviewed_resources), docs["resource_flow"])
    if a.reviewed_sync:
        reviewed_sync(read(a.reviewed_sync), docs["sync_relation"])
    save(docs, a.output)
    print(f"Validated three external JSON files: {a.output}")


if __name__ == "__main__":
    main()
