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
