from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from .agent import AGENT_TOOLS, AgentContext, execute_tool


ROOT = Path(__file__).resolve().parents[1]


def _env_path(name: str, default: Path) -> Path:
    return Path(os.environ.get(name, str(default))).resolve()


def _context() -> AgentContext:
    workspace = _env_path("CRA_WORKSPACE", ROOT / "demo" / "libuv")
    repo_root = _env_path("CRA_REPO_ROOT", ROOT)
    return AgentContext(
        workspace,
        repo_root=repo_root,
        run_id=os.environ.get("CRA_RUN_ID", "run_libuv_1.50.0"),
    )


def _mcp_tools() -> list[dict[str, Any]]:
    tools = []
    for tool in AGENT_TOOLS:
        function = tool["function"]
        tools.append(
            {
                "name": function["name"],
                "description": function["description"],
                "inputSchema": function["parameters"],
            }
        )
    return tools


def _respond(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    message_id = message.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "code-reverse-agent", "version": "0.1.0"},
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": message_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": message_id, "result": {"tools": _mcp_tools()}}
    if method == "tools/call":
        params = message.get("params") or {}
        name = params.get("name", "")
        arguments = params.get("arguments") or {}
        try:
            output = execute_tool(_context(), name, arguments)
            result: dict[str, Any] = {
                "content": [{"type": "text", "text": output}],
                "isError": False,
            }
        except Exception as exc:
            result = {
                "content": [{"type": "text", "text": json.dumps({"error": str(exc)}, ensure_ascii=False)}],
                "isError": True,
            }
        return {"jsonrpc": "2.0", "id": message_id, "result": result}
    return {
        "jsonrpc": "2.0",
        "id": message_id,
        "error": {"code": -32601, "message": f"未知方法: {method}"},
    }


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = _respond(message)
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
