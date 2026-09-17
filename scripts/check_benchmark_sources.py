#!/usr/bin/env python3
"""Check pinned source hashes and every benchmark evidence anchor."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jsonschema import Draft202012Validator
from validation.benchmark import ROOT, anchor, key, read, write


def check(truth, manifest, root=ROOT):
    Draft202012Validator(read(ROOT / "schemas/validation-benchmark.schema.json")).validate(truth)
    errors = []
    prefix = "third_party/" + truth["repository"].split("/")[-1]
    pin = subprocess.run(["git", "-C", str(root / prefix), "rev-parse", "HEAD"], capture_output=True, text=True)
    if pin.returncode or pin.stdout.strip() != truth["commit"]:
        errors.append("source checkout does not match pinned commit")
    if manifest["commit"] != truth["commit"]:
        errors.append("manifest pin mismatch")
    cache = {}
    for file, expected in manifest["sha256_lf"].items():
        p = (root / file).resolve()
        if not p.is_relative_to((root / prefix).resolve()) or not p.is_file():
            errors.append(f"invalid source path: {file}")
            continue
        raw = p.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(raw).hexdigest() != expected:
            errors.append(f"source hash mismatch: {file}")
        cache[file] = raw.decode("utf-8").splitlines()
    keys, ids = set(), set()
    for c in truth["cases"]:
        if c["id"] in ids or key(c) in keys:
            errors.append(f"duplicate case: {c['id']}")
        ids.add(c["id"])
        keys.add(key(c))
        for e in c["evidence"]:
            file, line, snippet = anchor(e)
            lines = cache.get(file, [])
            if not 1 <= line <= len(lines) or " ".join(lines[line-1].split()) != snippet:
                errors.append(f"bad evidence: {c['id']} {file}:{line}")
    return {"dataset_id": truth["dataset_id"], "cases": len(ids), "status": "failed" if errors else "verified", "errors": errors}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--benchmark", type=Path, required=True)
    a = p.parse_args()
    report = check(read(a.benchmark / "ground-truth.json"), read(a.benchmark / "source-manifest.json"))
    write(a.benchmark / "source-check.json", report)
    print(report)
    return bool(report["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
