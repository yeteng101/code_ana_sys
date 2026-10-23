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


def parse_log_line(
    raw: str,
    *,
    log_path: str | Path,
    line_number: int,
    source_root: str | Path,
    origin: str = "log",
) -> dict[str, Any] | None:
    path = Path(log_path).resolve()
    root = Path(source_root).resolve()
    line = raw.strip()
    if not line:
        return None
    if line.startswith("{"):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            item = None
        if isinstance(item, dict):
            file = str(item.get("file") or "")
            return {
                "id": "log_" + stable_digest([path.as_posix(), line_number, item])[:12],
                "kind": "structured_log_event",
                "origin": origin,
                "log_file": path.name,
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
    diagnostic = DIAGNOSTIC_PATTERN.match(line)
    if diagnostic:
        return {
            "id": "diag_" + stable_digest([path.as_posix(), line_number])[:12],
            "kind": "compiler_diagnostic",
            "origin": origin,
            "log_file": path.name,
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
    stack = STACK_PATTERN.search(line)
    if stack:
        return {
            "id": "stack_" + stable_digest([path.as_posix(), line_number])[:12],
            "kind": "stack_frame",
            "origin": origin,
            "log_file": path.name,
            "log_line": line_number,
            "severity": "error",
            "message": line,
            "function": stack.group("function") or "",
            "event": "stack_frame",
            "file": _relative_file(stack.group("file"), root),
            "line": int(stack.group("line")),
            "raw": raw,
        }
    function = FUNCTION_FIELD_PATTERN.search(line)
    event_name = EVENT_FIELD_PATTERN.search(line)
    if function or event_name:
        return {
            "id": "log_" + stable_digest([path.as_posix(), line_number])[:12],
            "kind": "log_event",
            "origin": origin,
            "log_file": path.name,
            "log_line": line_number,
            "severity": "info",
            "message": line,
            "function": function.group(1) if function else "",
            "event": event_name.group(1) if event_name else "",
            "file": "",
            "line": 0,
            "raw": raw,
        }
    return None


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
        event = parse_log_line(
            raw,
            log_path=log_path,
            line_number=line_number,
            source_root=root,
            origin=origin,
        )
        if event:
            events.append(event)
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


class RealtimeLogExtractor:
    """Incrementally read appended log lines without re-reading old content."""

    def __init__(
        self,
        paths: list[str | Path],
        *,
        source_root: str | Path,
    ) -> None:
        self.source_root = Path(source_root).resolve()
        self.paths = [Path(value).expanduser().resolve() for value in paths]
        self.offsets = {path: 0 for path in self.paths}
        self.partial = {path: "" for path in self.paths}
        self.line_numbers = {path: 0 for path in self.paths}

    def poll(self) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for path in self.paths:
            if not path.is_file():
                continue
            with path.open("rb") as stream:
                stream.seek(self.offsets[path])
                chunk = stream.read()
                end = stream.tell()
            if not chunk:
                continue
            text = chunk.decode("utf-8", errors="replace")
            text = self.partial[path] + text
            complete = text.splitlines(keepends=True)
            if complete and not complete[-1].endswith(("\n", "\r")):
                self.partial[path] = complete.pop()
                end -= len(self.partial[path].encode("utf-8"))
            else:
                self.partial[path] = ""
            for raw in complete:
                self.line_numbers[path] += 1
                event = parse_log_line(
                    raw.rstrip("\r\n"),
                    log_path=path,
                    line_number=self.line_numbers[path],
                    source_root=self.source_root,
                    origin="realtime_log",
                )
                if event:
                    events.append(event)
            self.offsets[path] = end
        return events
