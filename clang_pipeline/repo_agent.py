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
from .visualization import write_visualization


def repository_label(url: str) -> str:
    parsed = urlparse(url)
    path = Path(unquote(parsed.path)).name
    name = re.sub(r"\.git$", "", path)
    return slugify_repository(Path(name)) or "repository"


def repository_identity(url: str) -> str:
    parsed = urlparse(url)
    raw_path = parsed.path
    if parsed.scheme == "":
        if ":" not in raw_path:
            return repository_label(url)
        raw_path = raw_path.split(":", 1)[1]
    path = unquote(raw_path).strip("/")
    if parsed.scheme in {"http", "https", "ssh", "git", ""} and path:
        path = re.sub(r"\.git$", "", path)
        parts = [part for part in path.split("/") if part]
        if len(parts) >= 2:
            return "/".join(parts[-2:])
        if len(parts) == 1:
            return parts[0]
    return repository_label(url)


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
    log_path: Path | None = None,
) -> list[dict[str, Any]]:
    def write_log(text: str) -> None:
        if log_path is None:
            return
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(text.rstrip() + "\n")

    existing = discover_compile_commands(repo)
    if existing:
        write_log(f"using existing compile commands: {existing}")
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
            write_log("\n".join(
                part for part in (completed.stdout, completed.stderr) if part
            ))
            return list(read_json(build_dir / "compile_commands.json"))
        write_log(
            "cmake configure failed; falling back to generic compile commands\n"
            + completed.stdout
            + completed.stderr
        )

    write_log("no compile_commands.json found; generated generic compile commands")
    return generic_compile_commands(repo)


def _relativize_json_paths(value: Any, source_root: Path) -> Any:
    root = source_root.resolve()
    if isinstance(value, dict):
        return {
            key: _relativize_json_paths(item, source_root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_relativize_json_paths(item, source_root) for item in value]
    if isinstance(value, str) and Path(value).is_absolute():
        try:
            resolved = Path(value).resolve()
        except OSError:
            return value
        if resolved.is_relative_to(root):
            return resolved.relative_to(root).as_posix()
    return value


def relativize_artifact_paths(output_dir: Path, source_root: Path) -> None:
    paths = [output_dir / name for name in (
        "graph.json",
        "architecture.json",
        "key-chains.json",
        "run-result.json",
    )]
    paths.extend((output_dir / "external").glob("*.json"))
    paths.extend((output_dir / "knowledge").glob("*.json"))
    for path in paths:
        if not path.is_file():
            continue
        write_json(path, _relativize_json_paths(read_json(path), source_root))
    root_text = str(source_root.resolve())
    for name in ("report.md", "analysis.md"):
        path = output_dir / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(
            text.replace(root_text + "/", "").replace(root_text, ""),
            encoding="utf-8",
        )


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
    knowledge_source = workspace / "external" / "knowledge-graph.json"
    if knowledge_source.exists():
        shutil.copyfile(knowledge_source, external_dir / "knowledge-graph.json")
    knowledge_dir = output_dir / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    for name in ("build-profile.json", "log-facts.json", "knowledge-graph.json"):
        source = workspace / "10-knowledge" / name
        if source.exists():
            shutil.copyfile(source, knowledge_dir / name)
    logs_dir = output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_sources = (
        sorted((workspace / "logs").glob("*"))
        if (workspace / "logs").exists()
        else []
    )
    for source in log_sources:
        if source.is_file():
            shutil.copyfile(source, logs_dir / source.name)
    _write_call_chains(workspace, output_dir)

    graph = read_json(workspace / "07-report" / "graph.json")
    resource_flow = read_json(external_dir / "resource-flow.json")
    sync_relations = read_json(external_dir / "sync-relations.json")
    call_chains = read_json(external_dir / "call-chains.json")
    knowledge_graph = (
        read_json(external_dir / "knowledge-graph.json")
        if (external_dir / "knowledge-graph.json").exists()
        else {}
    )
    manifest = {
        "schema_version": "1.0",
        "run_id": run_id,
        "repository": graph.get("meta", {}).get("repository", repository_label(repository_url)),
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
            "knowledge_entities": len(knowledge_graph.get("entities", [])),
            "knowledge_relations": len(knowledge_graph.get("relations", [])),
        },
        "outputs": {
            "visualization": "visualization.html",
            "call_chains": "external/call-chains.json",
            "resource_flow": "external/resource-flow.json",
            "sync_relations": "external/sync-relations.json",
            "knowledge_graph": "external/knowledge-graph.json",
            "logs": "logs",
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
    log_paths: list[str | Path] | None = None,
    optimized_ir: bool = False,
) -> dict[str, Any]:
    repo, resolved_commit, label = checkout_repository(
        repository_url,
        branch=branch,
        commit=commit,
        work_root=work_root,
    )
    run_id = f"run_{label}_{int(time.time())}"
    repository = repository_identity(repository_url)
    target_output = Path(output_dir).expanduser().resolve()
    target_workspace = target_output / "workspace"
    profile = build_profile or "repository-auto"
    logs_dir = target_workspace / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    for index, value in enumerate(log_paths or []):
        path = Path(value).expanduser().resolve()
        if path.is_file():
            shutil.copyfile(path, logs_dir / f"{index:02d}_{path.name}")
    compile_units = build_compile_commands(
        repo,
        log_path=logs_dir / "build.log",
    )

    outcome = run_pipeline(
        source_root=repo,
        workspace=target_workspace,
        run_id=run_id,
        build_profile=profile,
        compile_commands=compile_units,
        publish_dir=target_output,
        commit=resolved_commit,
        entry_symbols=entry_symbols,
        repository=repository,
        optimized_ir=optimized_ir,
    )
    bundle = bundle_artifacts(
        target_workspace,
        target_output,
        repository_url=repository_url,
        commit=resolved_commit,
        run_id=run_id,
        build_profile=profile,
    )
    relativize_artifact_paths(target_output, repo)
    write_visualization(
        target_output,
        graph=read_json(target_output / "graph.json"),
        resource_flow=read_json(target_output / "external" / "resource-flow.json"),
        sync_relations=read_json(target_output / "external" / "sync-relations.json"),
        output=target_output / "visualization.html",
    )
    archive_path = ""
    if archive:
        archive_path = str(target_output) + ".zip"
        shutil.make_archive(str(target_output), "zip", target_output)

    return {
        "status": "succeeded",
        "repository_url": repository_url,
        "repository": repository,
        "repository_label": label,
        "commit": resolved_commit,
        "run_id": run_id,
        "build_profile": profile,
        "source_dir": str(repo),
        "workspace": str(target_workspace),
        "output_dir": str(bundle),
        "archive": archive_path,
        "outputs": read_json(bundle / "manifest.json")["outputs"],
        "pipeline_status": {
            item["stage"]: item.get("status")
            for item in outcome.get("results", [])
        },
    }
