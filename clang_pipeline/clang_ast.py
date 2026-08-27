from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


class ClangPipelineError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def relpath(root: Path, value: str) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return path.as_posix()
    return path.as_posix()


def snippet_for(root: Path, file: str, line: int) -> str:
    try:
        lines = (root / file).read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    if 1 <= line <= len(lines):
        return lines[line - 1].strip()
    return ""


def evidence_id(kind: str, file: str, line: int, name: str = "") -> str:
    raw = f"{kind}|{file}|{line}|{name}"
    return "ev_" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def make_source_location(root: Path, loc: dict[str, Any], *, with_snippet: bool = True) -> dict[str, Any] | None:
    file = loc.get("file")
    line = loc.get("line")
    if not file or not line:
        return None
    result: dict[str, Any] = {
        "file": relpath(root, file),
        "line": int(line),
    }
    if loc.get("col"):
        result["column"] = int(loc["col"])
    if with_snippet:
        result["snippet"] = snippet_for(root, result["file"], int(line))
    return result


def range_begin(node: dict[str, Any], *, prefer_expansion: bool = True) -> dict[str, Any]:
    begin = (node.get("range") or {}).get("begin") or {}
    if prefer_expansion and isinstance(begin.get("expansionLoc"), dict):
        return begin["expansionLoc"]
    if isinstance(begin.get("spellingLoc"), dict) and not prefer_expansion:
        return begin["spellingLoc"]
    return begin


def _offset_to_line(root: Path, file: str, offset: int) -> int:
    try:
        text = (root / file).read_text(encoding="utf-8")
    except OSError:
        return 0
    return text.count("\n", 0, min(offset, len(text))) + 1


def _loc_with_file(
    root: Path, loc: dict[str, Any], default_file: str | None
) -> dict[str, Any]:
    if not loc:
        return {}
    result = dict(loc)
    if not result.get("file") and default_file:
        result["file"] = default_file
    if not result.get("line") and result.get("offset") and result.get("file"):
        result["line"] = _offset_to_line(root, result["file"], int(result["offset"]))
    return result


def node_location(
    root: Path,
    node: dict[str, Any],
    default_file: str | None = None,
) -> dict[str, Any] | None:
    kind = node.get("kind")
    if kind in {"CallExpr", "MemberExpr", "BinaryOperator", "UnaryOperator"}:
        loc = range_begin(node)
        loc = _loc_with_file(root, loc, default_file)
        if loc.get("file"):
            return make_source_location(root, loc)
    loc = node.get("loc")
    if not loc or not loc.get("file"):
        loc = range_begin(node)
        loc = _loc_with_file(root, loc, default_file)
    if not loc or not loc.get("file"):
        return None
    return make_source_location(root, loc)


def spelling_location(root: Path, node: dict[str, Any]) -> dict[str, Any] | None:
    loc = node.get("loc")
    if loc and loc.get("file"):
        return make_source_location(root, loc)
    loc = range_begin(node, prefer_expansion=False)
    if loc and loc.get("file"):
        return make_source_location(root, loc)
    return None


def iter_nodes(node: dict[str, Any]) -> Iterator[dict[str, Any]]:
    yield node
    for child in node.get("inner", []):
        yield from iter_nodes(child)


def unwrap_expr(node: dict[str, Any] | None) -> dict[str, Any] | None:
    while node and node.get("kind") in {
        "ImplicitCastExpr",
        "CStyleCastExpr",
        "CXXFunctionalCastExpr",
        "FunctionalCastExpr",
        "MaterializeTemporaryExpr",
        "ParenExpr",
        "ExprWithCleanups",
    }:
        children = node.get("inner", [])
        if not children:
            break
        node = children[0]
    return node


def has_body(node: dict[str, Any]) -> bool:
    return any(child.get("kind") == "CompoundStmt" for child in node.get("inner", []))


def is_fptr_qual_type(type_info: Any) -> bool:
    if not isinstance(type_info, dict):
        return False
    qual = str(type_info.get("desugaredQualType") or type_info.get("qualType") or "")
    return "(*" in qual or "*)(" in qual or "std::function" in qual


def run_clang_ast(unit: dict[str, Any], root: Path) -> dict[str, Any]:
    command = list(unit.get("arguments", []))
    command += ["-fsyntax-only", "-Xclang", "-ast-dump=json"]
    completed = subprocess.run(
        command,
        cwd=unit.get("directory") or str(root),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        raise ClangPipelineError(
            f"Clang AST 解析失败: {unit.get('file')}\n{completed.stderr.strip()}"
        )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ClangPipelineError(f"Clang AST JSON 无法解析: {unit.get('file')}") from exc


def run_preprocessor_macros(unit: dict[str, Any], root: Path) -> list[str]:
    command = list(unit.get("arguments", []))
    command += ["-E", "-dM"]
    completed = subprocess.run(
        command,
        cwd=unit.get("directory") or str(root),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0:
        raise ClangPipelineError(
            f"Clang 预处理失败: {unit.get('file')}\n{completed.stderr.strip()}"
        )
    return completed.stdout.splitlines()
