#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LIBUV_TAG="v1.50.0"
LIBUV_COMMIT="8fb9cb919489a48880680a56efecff6a7dfb4504"
LIBUV_DIR="$ROOT/third_party/libuv"
WORKSPACE="$ROOT/demo/run_libuv_v1.50.0"

mkdir -p third_party
if [ ! -d "$LIBUV_DIR/.git" ]; then
  git clone --depth 1 --branch "$LIBUV_TAG" \
    https://github.com/libuv/libuv.git "$LIBUV_DIR"
fi

cmake -S "$LIBUV_DIR" -B "$LIBUV_DIR/build" \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCMAKE_C_COMPILER=clang \
  -DBUILD_TESTING=OFF \
  -DCMAKE_BUILD_TYPE=Debug

python3 -m clang_pipeline.pipeline \
  --source "$LIBUV_DIR" \
  --workspace "$WORKSPACE" \
  --run-id "run_libuv_${LIBUV_TAG#v}" \
  --profile "libuv-macos-clang" \
  --repository "libuv/libuv" \
  --commit "$LIBUV_COMMIT" \
  --entry "uv_run" \
  --compile-commands "$LIBUV_DIR/build/compile_commands.json" \
  --publish "$ROOT/demo/libuv"
