from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

from .clang_ast import read_json
from .pipeline import run_pipeline


SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp"}


def _is_repository(path: Path) -> bool:
    if not path.is_dir():
        return False
    if (path / "compile_commands.json").exists():
        return True
    for suffix in SOURCE_SUFFIXES:
        try:
            if next(path.rglob(f"*{suffix}"), None) is not None:
                return True
        except OSError:
            continue
    return False


def _raw_path_candidates(question: str, cwd: Path) -> list[Path]:
    candidates: list[Path] = []
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', question)
    for left, right in quoted:
        raw = left or right
        if raw and (raw.startswith(("/", "~", "./", "../"))):
            candidates.append(Path(raw))
    for match in re.finditer(
        r"(?<![\w])((?:/|~|\./|\.\./)[^\s，。；、,;:：)）}\]]+)",
        question,
    ):
        raw = match.group(1).rstrip("\"'")
        if raw:
            candidates.append(Path(raw))
    result: list[Path] = []
    for candidate in candidates:
        candidate = candidate.expanduser()
        if not candidate.is_absolute():
            candidate = cwd / candidate
        try:
            candidate = candidate.resolve()
        except OSError:
            continue
        if candidate not in result:
            result.append(candidate)
    return result


def _path_candidates(question: str, cwd: Path) -> list[Path]:
    return [
        candidate
        for candidate in _raw_path_candidates(question, cwd)
        if _is_repository(candidate)
    ]


def extract_repo_path(
    question: str,
    *,
    explicit: str | Path | None = None,
    cwd: str | Path | None = None,
    strict: bool = False,
) -> Path | None:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_absolute():
            path = Path(cwd or Path.cwd()) / path
        path = path.resolve()
        if _is_repository(path):
            return path
        if strict:
            raise ValueError(f"路径不是可分析的源码仓库: {path}")
        return None
    root = Path(cwd or Path.cwd()).resolve()
    for path in _path_candidates(question, root):
        return path
    if strict:
        raw = _raw_path_candidates(question, root)
        if raw:
            raise ValueError(f"问题中的路径不存在或不是源码仓库: {raw[0]}")
    return None


def discover_compile_commands(repo: Path) -> Path | None:
    direct = [
        repo / "compile_commands.json",
        repo / "build" / "compile_commands.json",
    ]
    for candidate in direct:
        if candidate.is_file():
            return candidate.expanduser().resolve()
    try:
        matches = sorted(repo.rglob("compile_commands.json"), key=lambda item: str(item))
    except OSError:
        return None
    return matches[0].expanduser().resolve() if matches else None


def slugify_repository(repo: Path) -> str:
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", repo.name).strip("_")
    return name or "repository"


def default_workspace(repo: Path, *, cwd: str | Path | None = None) -> Path:
    root = Path(cwd or Path.cwd()).resolve()
    return root / "demo" / f"run_{slugify_repository(repo)}"


def default_run_id(repo: Path) -> str:
    stamp = time.strftime("%Y%m%d_%H%M%S")
    return f"run_{slugify_repository(repo)}_{stamp}"


def analyze_repository(
    repo: str | Path,
    *,
    workspace: str | Path | None = None,
    run_id: str | None = None,
    compile_commands: str | Path | None = None,
    publish_dir: str | Path | None = None,
    build_profile: str = "default",
    repository: str | None = None,
    commit: str = "local",
    entry_symbols: list[str] | None = None,
) -> dict[str, Any]:
    repo_path = Path(repo).expanduser().resolve()
    if not _is_repository(repo_path):
        raise ValueError(f"不是可分析的源码仓库: {repo_path}")

    compile_path = (
        Path(compile_commands).expanduser().resolve()
        if compile_commands
        else discover_compile_commands(repo_path)
    )
    compile_units = list(read_json(compile_path)) if compile_path else None
    target_workspace = (
        Path(workspace).expanduser().resolve()
        if workspace
        else default_workspace(repo_path).resolve()
    )
    target_run_id = run_id or default_run_id(repo_path)
    outcome = run_pipeline(
        source_root=repo_path,
        workspace=target_workspace,
        run_id=target_run_id,
        build_profile=build_profile,
        compile_commands=compile_units,
        publish_dir=Path(publish_dir).expanduser().resolve() if publish_dir else None,
        repository=repository or repo_path.name,
        commit=commit,
        entry_symbols=entry_symbols,
    )
    return {
        "repository": str(repo_path),
        "workspace": str(target_workspace),
        "run_id": target_run_id,
        "compile_commands": str(compile_path) if compile_path else "",
        "pipeline": outcome,
    }


def analyze_from_question(
    question: str,
    *,
    source: str | Path | None = None,
    workspace: str | Path | None = None,
    run_id: str | None = None,
    compile_commands: str | Path | None = None,
    publish_dir: str | Path | None = None,
    build_profile: str = "default",
    repository: str | None = None,
    commit: str = "local",
    entry_symbols: list[str] | None = None,
    strict: bool = False,
) -> dict[str, Any] | None:
    repo = extract_repo_path(question, explicit=source, strict=strict)
    if repo is None:
        return None
    return analyze_repository(
        repo,
        workspace=workspace,
        run_id=run_id,
        compile_commands=compile_commands,
        publish_dir=publish_dir,
        build_profile=build_profile,
        repository=repository,
        commit=commit,
        entry_symbols=entry_symbols,
    )


def prepare_question_context(
    question: str,
    *,
    source: str | Path | None = None,
    workspace: str | Path | None = None,
    run_id: str | None = None,
    compile_commands: str | Path | None = None,
    publish_dir: str | Path | None = None,
    build_profile: str = "default",
    auto_analyze: bool = True,
) -> tuple[Path, str, dict[str, Any] | None]:
    analysis = (
        analyze_from_question(
            question,
            source=source,
            workspace=workspace,
            run_id=run_id,
            compile_commands=compile_commands,
            publish_dir=publish_dir,
            build_profile=build_profile,
            strict=True,
        )
        if auto_analyze
        else None
    )
    if analysis is not None:
        return (
            Path(analysis["workspace"]).resolve(),
            str(analysis["run_id"]),
            analysis,
        )
    target_workspace = (
        Path(workspace).expanduser().resolve()
        if workspace
        else (Path.cwd() / "demo" / "libuv").resolve()
    )
    return target_workspace, run_id or "run_libuv_1.50.0", None
