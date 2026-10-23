from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .clang_ast import stable_digest, utc_now


DIAGNOSTIC_PATTERN = re.compile(
    r"^(?P<file>.+?):(?P<line>\d+):(?:(?P<column>\d+):)?\s*"
    r"(?P<severity>fatal error|error|warning|note):\s*(?P<message>.*)$"
)
STACK_PATTERN = re.compile(
    r"(?:#\d+\s+)?(?:0x[0-9a-fA-F]+\s+in\s+)?"
    r"(?P<function>[A-Za-z_~][\w:~.-]*)?\s*"
    r"(?P<file>(?:/|\./)?[^\s:()]+):(?P<line>\d+)"
)
FUNCTION_FIELD_PATTERN = re.compile(r"\bfunction=([A-Za-z_~][\w:~.-]*)")
EVENT_FIELD_PATTERN = re.compile(r"\bevent=([A-Za-z_][\w.-]*)")


def _relative_file(value: str, source_root: Path) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(source_root.resolve()).as_posix()
        except ValueError:
            return path.as_posix()
    return path.as_posix()


def parse_log_file(
    path: str | Path,
    *,
    source_root: str | Path,
    origin: str = "log",
) -> list[dict[str, Any]]:
    log_path = Path(path).resolve()
    root = Path(source_root).resolve()
    events = []
    for line_number, raw in enumerate(
        log_path.read_text(encoding="utf-8", errors="replace").splitlines(),
        start=1,
    ):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("{"):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                item = None
            if isinstance(item, dict):
                file = str(item.get("file") or "")
                event = {
                    "id": "log_" + stable_digest([log_path.as_posix(), line_number, item])[:12],
                    "kind": "structured_log_event",
                    "origin": origin,
                    "log_file": log_path.name,
                    "log_line": line_number,
                    "timestamp": str(item.get("timestamp") or ""),
                    "severity": str(item.get("severity") or item.get("level") or "info"),
                    "message": str(item.get("message") or line),
                    "function": str(item.get("function") or ""),
                    "event": str(item.get("event") or ""),
                    "file": _relative_file(file, root) if file else "",
                    "line": int(item.get("line") or 0),
                    "raw": raw,
                }
                events.append(event)
                continue
        diagnostic = DIAGNOSTIC_PATTERN.match(line)
        if diagnostic:
            events.append(
                {
                    "id": "diag_" + stable_digest([log_path.as_posix(), line_number])[:12],
                    "kind": "compiler_diagnostic",
                    "origin": origin,
                    "log_file": log_path.name,
                    "log_line": line_number,
                    "severity": diagnostic.group("severity"),
                    "message": diagnostic.group("message"),
                    "function": "",
                    "event": "diagnostic",
                    "file": _relative_file(diagnostic.group("file"), root),
                    "line": int(diagnostic.group("line")),
                    "column": int(diagnostic.group("column") or 0),
                    "raw": raw,
                }
            )
            continue
        stack = STACK_PATTERN.search(line)
        if stack:
            events.append(
                {
                    "id": "stack_" + stable_digest([log_path.as_posix(), line_number])[:12],
                    "kind": "stack_frame",
                    "origin": origin,
                    "log_file": log_path.name,
                    "log_line": line_number,
                    "severity": "error",
                    "message": line,
                    "function": stack.group("function") or "",
                    "event": "stack_frame",
                    "file": _relative_file(stack.group("file"), root),
                    "line": int(stack.group("line")),
                    "raw": raw,
                }
            )
            continue
        function = FUNCTION_FIELD_PATTERN.search(line)
        event_name = EVENT_FIELD_PATTERN.search(line)
        if function or event_name:
            events.append(
                {
                    "id": "log_" + stable_digest([log_path.as_posix(), line_number])[:12],
                    "kind": "log_event",
                    "origin": origin,
                    "log_file": log_path.name,
                    "log_line": line_number,
                    "severity": "info",
                    "message": line,
                    "function": function.group(1) if function else "",
                    "event": event_name.group(1) if event_name else "",
                    "file": "",
                    "line": 0,
                    "raw": raw,
                }
            )
    return events


def collect_log_facts(
    paths: list[str | Path],
    *,
    source_root: str | Path,
) -> dict[str, Any]:
    root = Path(source_root).resolve()
    files = []
    events = []
    for value in paths:
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            continue
        origin = "compiler" if path.suffix in {".err", ".diag"} or "compile" in path.name else "runtime"
        file_events = parse_log_file(path, source_root=root, origin=origin)
        files.append({"path": str(path), "events": len(file_events)})
        events.extend(file_events)
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "source_root": str(root),
        "files": files,
        "events": events,
    }
