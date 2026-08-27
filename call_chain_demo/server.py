from __future__ import annotations

import argparse
import json
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .engine import RequestError, analyze_call_chains, make_run_id, utc_now, validate_request


SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
RUNS: dict[str, dict[str, Any]] = {}
TASKS: dict[str, tuple[str, str]] = {}
RUN_LOCK = threading.Lock()


def _request_fingerprint(request: dict[str, Any]) -> str:
    from .engine import stable_digest

    return stable_digest(request)


def submit_async(raw_request: Any) -> tuple[dict[str, Any], bool]:
    request = validate_request(raw_request)
    fingerprint = _request_fingerprint(request)
    task_id = request["task_id"]
    with RUN_LOCK:
        if task_id in TASKS:
            existing_run_id, existing_fingerprint = TASKS[task_id]
            if existing_fingerprint != fingerprint:
                raise RequestError("INVALID_REQUEST", "相同 task_id 已用于不同的请求")
            return RUNS[existing_run_id], False
        run_id = make_run_id(request)
        RUNS[run_id] = {
            "schema_version": "1.0",
            "run_id": run_id,
            "task_id": task_id,
            "status": "running",
            "generated_at": utc_now(),
            "warnings": [],
            "errors": [],
        }
        TASKS[task_id] = (run_id, fingerprint)

    def worker() -> None:
        try:
            result = analyze_call_chains(request, run_id=run_id)
        except Exception as exc:  # The HTTP boundary must always expose a structured result.
            result = {
                "schema_version": "1.0",
                "run_id": run_id,
                "task_id": task_id,
                "status": "failed",
                "generated_at": utc_now(),
                "findings": [],
                "evidence": [],
                "coverage": {
                    "complete": False,
                    "roots_total": len(request["targets"]),
                    "roots_analyzed": 0,
                    "truncated_chains": 0,
                    "unresolved_indirect_calls": 0,
                    "skipped_files": [],
                    "reason": "internal_error",
                },
                "warnings": [],
                "errors": [{"code": "INTERNAL_ERROR", "message": str(exc), "retryable": False}],
            }
        with RUN_LOCK:
            RUNS[run_id] = result

    threading.Thread(target=worker, name=f"analysis-{run_id}", daemon=True).start()
    return RUNS[run_id], True


class DemoHandler(BaseHTTPRequestHandler):
    server_version = "CodeReverseAgentDemo/0.1"

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _read_json(self) -> Any:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise RequestError("INVALID_REQUEST", "Content-Length 非法") from exc
        if length <= 0 or length > 1_000_000:
            raise RequestError("INVALID_REQUEST", "请求体必须为 1 到 1000000 字节")
        try:
            return json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RequestError("INVALID_REQUEST", "请求体不是合法 JSON") from exc

    def _write_request_error(self, error: RequestError) -> None:
        self._write_json(
            HTTPStatus.BAD_REQUEST,
            {"status": "failed", "warnings": [], "errors": [error.as_dict()]},
        )

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = urlparse(self.path).path
        if path == "/health":
            self._write_json(HTTPStatus.OK, {"status": "ok", "service": "code-reverse-agent-demo", "version": "0.1.0"})
            return
        if path.startswith("/api/v1/runs/"):
            run_id = path.removeprefix("/api/v1/runs/")
            with RUN_LOCK:
                result = RUNS.get(run_id)
            if result is None:
                self._write_json(HTTPStatus.NOT_FOUND, {"status": "failed", "warnings": [], "errors": [{"code": "INVALID_REQUEST", "message": "run_id 不存在", "retryable": False}]})
                return
            self._write_json(HTTPStatus.OK, result)
            return
        if path.startswith("/api/v1/schemas/"):
            name = path.removeprefix("/api/v1/schemas/")
            allowed = {"call-chain-request", "call-chain-result"}
            if name not in allowed:
                self._write_json(HTTPStatus.NOT_FOUND, {"status": "failed", "warnings": [], "errors": [{"code": "INVALID_REQUEST", "message": "Schema 不存在", "retryable": False}]})
                return
            with (SCHEMA_DIR / f"{name}.schema.json").open(encoding="utf-8") as stream:
                self._write_json(HTTPStatus.OK, json.load(stream))
            return
        self._write_json(HTTPStatus.NOT_FOUND, {"status": "failed", "warnings": [], "errors": [{"code": "INVALID_REQUEST", "message": "接口不存在", "retryable": False}]})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = urlparse(self.path).path
        try:
            request = self._read_json()
            if path == "/api/v1/call-chains":
                self._write_json(HTTPStatus.OK, analyze_call_chains(request))
                return
            if path == "/api/v1/analyze":
                state, created = submit_async(request)
                status = HTTPStatus.ACCEPTED if created else HTTPStatus.OK
                self._write_json(status, state)
                return
            self._write_json(HTTPStatus.NOT_FOUND, {"status": "failed", "warnings": [], "errors": [{"code": "INVALID_REQUEST", "message": "接口不存在", "retryable": False}]})
        except RequestError as error:
            self._write_request_error(error)

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {self.address_string()} {fmt % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="代码逆向 Agent 调用链 JSON 接口 Demo")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DemoHandler)
    print(f"Code Reverse Agent Demo: http://{args.host}:{args.port}")
    print("POST /api/v1/call-chains  (同步)")
    print("POST /api/v1/analyze      (异步)")
    print("GET  /api/v1/runs/{run_id}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
