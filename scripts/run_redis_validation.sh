#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
redis_commit=d2c8a4b91e8c0e6aefd1f5bc0bf582cddbe046b7
if [ ! -d third_party/redis/.git ]; then
  git clone --depth 1 --branch 7.2.4 https://github.com/redis/redis.git third_party/redis
fi
test "$(git -C third_party/redis rev-parse HEAD)" = "$redis_commit"
mkdir -p demo/redis
bear --output "$PWD/demo/redis/compile_commands.full.json" -- \
  make -C third_party/redis -j2 CC=/usr/bin/clang MALLOC=libc OPTIMIZATION=-O0 BUILD_TLS=no
python - <<'PY'
import json
from pathlib import Path
full = json.loads(Path('demo/redis/compile_commands.full.json').read_text())
scope = {'ae.c', 'bio.c', 'lazyfree.c', 'networking.c', 't_string.c', 'db.c', 'adlist.c', 'dict.c'}
selected = [x for x in full if Path(x['file']).name in scope and '/src/' in x['file']
            and '-cc1' not in x.get('arguments', [])]
assert {Path(x['file']).name for x in selected} == scope
for unit in selected:
    # Preserve captured flags while making relative source/include paths resolvable.
    unit['arguments'][0] = 'clang'
    args = unit['arguments']
    for i, arg in enumerate(args):
        if arg.endswith('.c') and not arg.startswith('-'):
            args[i] = str((Path(unit['directory']) / arg).resolve())
        elif arg.startswith('-I') and len(arg) > 2:
            args[i] = '-I' + str((Path(unit['directory']) / arg[2:]).resolve())
    unit['arguments'][1:1] = ['-working-directory', unit['directory']]
Path('demo/redis/compile_commands.json').write_text(json.dumps(selected, indent=2)+'\n')
Path('demo/redis/build-provenance.json').write_text(json.dumps({
    'repository': 'redis/redis', 'commit': 'd2c8a4b91e8c0e6aefd1f5bc0bf582cddbe046b7',
    'build': 'make CC=/usr/bin/clang MALLOC=libc OPTIMIZATION=-O0 BUILD_TLS=no',
    'capture': 'bear', 'full_translation_units': len(full), 'analyzed_translation_units': len(selected),
    'scope': sorted(scope), 'scope_note': 'Full Redis build, eight selected real translation units analyzed; not whole-program coverage.'
}, indent=2)+'\n')
PY
python -m clang_pipeline.pipeline --source third_party/redis \
  --workspace demo/run_redis_validation --run-id redis-7.2.4-validation \
  --profile redis-linux-clang --repository redis/redis --commit "$redis_commit" \
  --entry processInputBuffer --entry bioProcessBackgroundJobs --entry aeProcessEvents \
  --compile-commands demo/redis/compile_commands.json --publish demo/redis
cp demo/run_redis_validation/06-verify/verification.json demo/redis/verification.json
