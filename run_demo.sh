#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m clang_pipeline.pipeline \
  --source demo/sample \
  --workspace demo/run_clang_demo \
  --run-id run_20260827_clang_demo \
  --publish demo

python3 -m unittest discover -s clang_pipeline/tests -v
