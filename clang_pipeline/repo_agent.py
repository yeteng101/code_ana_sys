from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from .clang_ast import read_json, utc_now, write_json
from .nl_repo import discover_compile_commands, slugify_repository
from .pipeline import run_pipeline


def repository_label(url: str) -> str:
    parsed = urlparse(url)
    path = Path(unquote(parsed.path)).name
    name = re.sub(r"\.git$", "", path)
    return slugify_repository(Path(name)) or "repository"


def _git(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed.stdout.strip()


def checkout_repository(
    repository_url: str,
    *,
    branch: str | None = None,
    commit: str | None = None,
    work_root: str | Path | None = None,
) -> tuple[Path, str, str]:
    parsed = urlparse(repository_url)
    root = Path(work_root or Path(tempfile.gettempdir()) / "code-reverse-subagent").resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = root / f"{repository_label(repository_url)}_{int(time.time())}"
    target.mkdir(parents=True, exist_ok=False)

    if parsed.scheme in {"", "file"}:
        source = Path(unquote(parsed.path or repository_url)).expanduser().resolve()
        if not source.exists():
            raise ValueError(f"仓库路径不存在: {source}")
        if source.is_dir():
            shutil.copytree(
                source,
                target,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "build"),
            )
        else:
            raise ValueError(f"仓库 URL 不是目录: {repository_url}")
        resolved_commit = "local"
    else:
        clone_args = ["clone", "--depth", "1"]
        if branch:
            clone_args += ["--branch", branch]
        clone_args += [repository_url, str(target)]
        _git(clone_args, root)
        if commit:
            _git(["checkout", commit], target)
        resolved_commit = _git(["rev-parse", "HEAD"], target)

    return target, resolved_commit, repository_label(repository_url)


def generic_compile_commands(repo: Path) -> list[dict[str, Any]]:
    commands: list[dict[str, Any]] = []
    suffixes = (".c", ".cc", ".cpp", ".cxx")
    for path in sorted(repo.rglob("*")):
        if path.suffix not in suffixes:
            continue
        compiler = "clang++" if path.suffix != ".c" else "clang"
        standard = "-std=c11" if path.suffix == ".c" else "-std=c++17"
        commands.append(
            {
                "directory": str(repo),
                "file": str(path),
                "arguments": [compiler, standard, "-I", str(repo), str(path)],
                "compiler": compiler,
                "defines": [],
            }
        )
    return commands


def _write_call_chains(
    workspace: Path,
    output_dir: Path,
) -> Path:
    graph = read_json(workspace / "07-report" / "graph.json")
    nodes = {node["id"]: node for node in graph.get("nodes", [])}
    evidence = {item["id"]: item for item in graph.get("evidence", [])}
    items = []
    warnings = []
    for edge in graph.get("edges", []):
        if not edge.get("evidence_ids") or any(
            item not in evidence for item in edge["evidence_ids"]
        ):
            warnings.append(f"{edge.get('id', 'unknown')}: evidence 不完整")
            continue
        exported = dict(edge)
        exported["status"] = "unconfirmed"
        items.append(
            {
                "id": str(edge.get("id", "")),
                "entry": str(edge.get("source", "")),
                "direction": "caller_to_callee",
                "nodes": [
                    nodes[edge["source"]],
                    nodes[edge["target"]],
                ],
                "edges": [exported],
                "confidence": edge.get("confidence", 0.0),
                "evidence_ids": list(edge.get("evidence_ids", [])),
                "status": "unconfirmed",
            }
        )
    doc = {
        "schema_version": "1.0",
        "run_id": str(graph.get("run_id", "")),
        "result_type": "call_chain",
        "status": "partial",
        "source": graph.get("meta", {}),
        "origin": "analyzer",
        "items": items,
        "evidence": graph.get("evidence", []),
        "warnings": warnings,
    }
    target = output_dir / "external" / "call-chains.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    write_json(target, doc)
    return target


def build_compile_commands(
    repo: Path,
    *,
    configure: bool = True,
) -> list[dict[str, Any]]:
    existing = discover_compile_commands(repo)
    if existing:
        return list(read_json(existing))

    if configure and (repo / "CMakeLists.txt").exists():
        build_dir = repo / "build"
        build_dir.mkdir(exist_ok=True)
        completed = subprocess.run(
            [
                "cmake",
                "-S",
                str(repo),
                "-B",
                str(build_dir),
                "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
                "-DBUILD_TESTING=OFF",
                "-DCMAKE_BUILD_TYPE=Debug",
            ],
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        if completed.returncode == 0 and (build_dir / "compile_commands.json").exists():
            return list(read_json(build_dir / "compile_commands.json"))

    return generic_compile_commands(repo)


def bundle_artifacts(
    workspace: Path,
    output_dir: Path,
    *,
    repository_url: str,
    commit: str,
    run_id: str,
    build_profile: str,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    external_dir = output_dir / "external"
    external_dir.mkdir(parents=True, exist_ok=True)

    for name in (
        "report.md",
        "graph.json",
        "graph.mmd",
        "run-result.json",
        "architecture.json",
        "key-chains.json",
        "analysis.md",
        "visualization.html",
    ):
        source = workspace / "07-report" / name
        if source.exists():
            shutil.copyfile(source, output_dir / name)

    for name in ("resource-flow.json", "sync-relations.json"):
        source = workspace / "external" / name
        if source.exists():
            shutil.copyfile(source, external_dir / name)
    _write_call_chains(workspace, output_dir)

    graph = read_json(workspace / "07-report" / "graph.json")
    resource_flow = read_json(external_dir / "resource-flow.json")
    sync_relations = read_json(external_dir / "sync-relations.json")
    call_chains = read_json(external_dir / "call-chains.json")
    manifest = {
        "schema_version": "1.0",
        "run_id": run_id,
        "repository_url": repository_url,
        "commit": commit,
        "build_profile": build_profile,
        "generated_at": utc_now(),
        "status": "succeeded",
        "summary": {
            "nodes": len(graph.get("nodes", [])),
            "edges": len(graph.get("edges", [])),
            "evidence": len(graph.get("evidence", [])),
            "resource_items": len(resource_flow.get("items", [])),
            "sync_items": len(sync_relations.get("items", [])),
            "call_items": len(call_chains.get("items", [])),
        },
        "outputs": {
            "visualization": "visualization.html",
            "call_chains": "external/call-chains.json",
            "resource_flow": "external/resource-flow.json",
            "sync_relations": "external/sync-relations.json",
            "graph": "graph.json",
            "report": "report.md",
        },
    }
    write_json(output_dir / "manifest.json", manifest)
    return output_dir


def run_repo_analysis(
    repository_url: str,
    *,
    output_dir: str | Path,
    branch: str | None = None,
    commit: str | None = None,
    work_root: str | Path | None = None,
    entry_symbols: list[str] | None = None,
    build_profile: str | None = None,
    archive: bool = True,
) -> dict[str, Any]:
    repo, resolved_commit, label = checkout_repository(
        repository_url,
        branch=branch,
        commit=commit,
        work_root=work_root,
    )
    run_id = f"run_{label}_{int(time.time())}"
    compile_units = build_compile_commands(repo)
    target_output = Path(output_dir).expanduser().resolve()
    target_workspace = target_output / "workspace"
    profile = build_profile or "repository-auto"

    outcome = run_pipeline(
        source_root=repo,
        workspace=target_workspace,
        run_id=run_id,
        build_profile=profile,
        compile_commands=compile_units,
        publish_dir=target_output,
        repository=label,
        commit=resolved_commit,
        entry_symbols=entry_symbols,
    )
    bundle = bundle_artifacts(
        target_workspace,
        target_output,
        repository_url=repository_url,
        commit=resolved_commit,
        run_id=run_id,
        build_profile=profile,
    )
    archive_path = ""
    if archive:
        archive_path = str(target_output) + ".zip"
        shutil.make_archive(str(target_output), "zip", target_output)

    return {
        "status": "succeeded",
        "repository_url": repository_url,
        "repository": label,
        "commit": resolved_commit,
        "run_id": run_id,
        "workspace": str(target_workspace),
        "output_dir": str(bundle),
        "archive": archive_path,
        "outputs": read_json(bundle / "manifest.json")["outputs"],
        "pipeline_status": {
            item["stage"]: item.get("status")
            for item in outcome.get("results", [])
        },
    }
