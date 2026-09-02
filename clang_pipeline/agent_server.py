from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .agent import AGENT_TOOLS, AgentContext, run_agent
from .llm_bridge import LLMNotConfigured


ROOT = Path(__file__).resolve().parents[1]


def default_workspace() -> Path:
    candidates = [
        ROOT / "demo" / "libuv",
        ROOT / "demo" / "run_clang_demo",
    ]
    for candidate in candidates:
        if (candidate / "graph.json").exists():
            return candidate
    return candidates[0]


class AgentHandler(BaseHTTPRequestHandler):
    server_version = "CodeReverseAgentServer/0.1"

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _read_json(self) -> Any:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 2_000_000:
            raise ValueError("请求体必须为 1 到 2000000 字节")
        return json.loads(self.rfile.read(length))

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self._write_json(
                HTTPStatus.OK,
                {"status": "ok", "service": "code-reverse-agent", "version": "0.2.0"},
            )
            return
        if path == "/api/v1/agent/tools":
            self._write_json(HTTPStatus.OK, {"tools": AGENT_TOOLS})
            return
        self._write_json(
            HTTPStatus.NOT_FOUND,
            {"status": "failed", "error": {"code": "not_found", "message": "接口不存在"}},
        )

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/v1/agent/ask":
            self._write_json(
                HTTPStatus.NOT_FOUND,
                {"status": "failed", "error": {"code": "not_found", "message": "接口不存在"}},
            )
            return
        try:
            body = self._read_json()
            if not isinstance(body, dict) or not str(body.get("question", "")).strip():
                raise ValueError("question 不能为空")
            workspace = Path(body.get("workspace") or default_workspace()).resolve()
            run_id = str(body.get("run_id") or "run_libuv_1.50.0")
            max_steps = int(body.get("max_steps", 6))
            ctx = AgentContext(
                workspace,
                repo_root=ROOT,
                run_id=run_id,
            )
            result = run_agent(
                str(body["question"]).strip(),
                ctx,
                max_steps=max_steps,
                model=body.get("model"),
            )
            self._write_json(HTTPStatus.OK, result)
        except LLMNotConfigured as exc:
            self._write_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {
                    "status": "failed",
                    "error": {"code": "llm_not_configured", "message": str(exc)},
                },
            )
        except Exception as exc:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"status": "failed", "error": {"code": "bad_request", "message": str(exc)}},
            )

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {self.address_string()} {fmt % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="代码逆向 Agent 外部接口")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), AgentHandler)
    print(f"Agent Server: http://{args.host}:{args.port}")
    print("POST /api/v1/agent/ask  (自然语言提问)")
    print("GET  /api/v1/agent/tools")
    print("GET  /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
