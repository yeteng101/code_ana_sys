#!/usr/bin/env python3
"""Recreate published benchmark exports/reports and verify source evidence."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main():
    run("scripts/prepare_validation_truth.py")
    for project in ("libuv", "redis"):
        run("scripts/check_benchmark_sources.py", "--benchmark", f"validation/benchmarks/{project}")
        args = ["scripts/export_validation.py", "--graph", f"demo/{project}/graph.json",
                "--output", f"validation/results/{project}/predictions"]
        if project == "redis":
            args += ["--verification", "demo/redis/verification.json"]
        run(*args)
        run("scripts/evaluate_validation.py", "--ground-truth", f"validation/benchmarks/{project}/ground-truth.json",
            "--predictions", f"validation/results/{project}/predictions", "--output", f"validation/results/{project}/baseline")
    run("scripts/export_validation.py", "--graph", "demo/libuv/graph.json",
        "--reviewed-resources", "validation/resource-flow/dataset.json",
        "--reviewed-sync", "validation/sync-relations/dataset.json", "--output", "validation/results/libuv/reviewed")


if __name__ == "__main__":
    main()
