#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "缺少 python3，请先安装 Python 3.9+" >&2
  exit 1
fi

if ! command -v clang++ >/dev/null 2>&1; then
  echo "缺少 clang++，请先安装 Clang（macOS: xcode-select --install; Linux: apt install clang）" >&2
  exit 1
fi

python3 -m clang_pipeline.pipeline \
  --source demo/sample \
  --workspace demo/run_clang_demo \
  --run-id run_20260827_clang_demo \
  --publish demo

python3 -m unittest discover -s clang_pipeline/tests -v
