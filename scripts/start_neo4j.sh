#!/usr/bin/env bash
set -euo pipefail

NAME="code-ana-neo4j"
PASSWORD="${NEO4J_PASSWORD:-codeana123}"

if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
  docker start "$NAME"
else
  docker run -d \
    --name "$NAME" \
    -p 7474:7474 \
    -p 7687:7687 \
    -e "NEO4J_AUTH=neo4j/$PASSWORD" \
    neo4j:5.26
fi

echo "Neo4j: http://127.0.0.1:7474"
echo "User: neo4j"
echo "Password: $PASSWORD"

echo "Waiting for Neo4j HTTP endpoint..."
python3 - <<'PY'
import time
import urllib.request

deadline = time.monotonic() + 180
while True:
    try:
        with urllib.request.urlopen("http://127.0.0.1:7474", timeout=2) as response:
            response.read(1)
        print("Neo4j is ready.")
        break
    except Exception:
        if time.monotonic() >= deadline:
            raise SystemExit("Neo4j 启动超时，请检查 docker logs code-ana-neo4j")
        time.sleep(2)
PY
