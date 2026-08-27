from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .clang_ast import read_json, relpath, utc_now, write_json


DEFAULT_SOURCE = "demo/sample"
DEFAULT_WORKSPACE = "demo/run_clang_demo"


def build_request(
    run_id: str,
    source_root: Path,
    build_profile: str,
    repository: str = "local-cpp-demo",
    commit: str = "local",
    entry_symbols: list[str] | None = None,
) -> dict[str, Any]:
    request = {
        "schema_version": "1.0",
        "run_id": run_id,
        "task_id": "clang-pipeline-demo",
        "repo_root": str(Path.cwd().resolve()),
        "source_root": str(source_root.resolve()),
        "repository": repository,
        "commit": commit,
        "build_profile": build_profile,
        "started_at": utc_now(),
    }
    if entry_symbols:
        request["entry_symbols"] = entry_symbols
    return request


def build_compile_commands(
    source_root: Path,
    build_profile: str,
    defines: list[str],
    compiler: str = "clang++",
) -> list[dict[str, Any]]:
    root = Path.cwd().resolve()
    include_dir = relpath(root, str(source_root))
    commands: list[dict[str, Any]] = []
    files = sorted(source_root.rglob("*.cpp")) + sorted(source_root.rglob("*.cc"))
    headers = sorted(source_root.rglob("*.h")) + sorted(source_root.rglob("*.hpp"))
    for path in files + headers:
        file = relpath(root, str(path))
        arguments = [compiler, "-std=c++17", "-I", include_dir]
        if path.suffix in {".h", ".hpp"}:
            arguments += ["-x", "c++"]
        arguments += [f"-D{define}" for define in defines]
        arguments.append(file)
        commands.append(
            {
                "directory": str(root),
                "file": file,
                "arguments": arguments,
                "build_profile": build_profile,
                "compiler": compiler,
                "defines": defines,
            }
        )
    return commands


def build_pipeline_config(
    run_id: str,
    workspace_root: str,
) -> dict[str, Any]:
    def command(stage: str, inputs: list[str], outputs: list[str]) -> dict[str, Any]:
        return {
            "name": stage,
            "order": int(stage[:2]),
            "command": [
                "python3",
                "-m",
                "clang_pipeline.stage_runner",
                stage,
                "--workspace",
                "{workspace}",
            ],
            "inputs": inputs,
            "outputs": outputs,
        }

    return {
        "pipeline_version": "1.0",
        "run_id": run_id,
        "workspace_root": workspace_root,
        "stages": [
            command(
                "01-index",
                ["compile_commands.json"],
                ["01-index/symbols.json", "01-index/ast/*.ast.json"],
            ),
            command(
                "02-macro",
                ["compile_commands.json", "01-index/symbols.json"],
                ["02-macro/macros.json"],
            ),
            command(
                "03-callgraph",
                ["01-index/symbols.json", "02-macro/macros.json"],
                ["03-callgraph/callgraph.json"],
            ),
            command(
                "04-fptr",
                ["03-callgraph/callgraph.json"],
                ["04-fptr/fptr-candidates.json"],
            ),
            command(
                "05-async",
                ["03-callgraph/callgraph.json", "04-fptr/fptr-candidates.json"],
                ["05-async/async-chains.json"],
            ),
            command(
                "06-verify",
                [
                    "01-index/symbols.json",
                    "02-macro/macros.json",
                    "03-callgraph/callgraph.json",
                    "04-fptr/fptr-candidates.json",
                    "05-async/async-chains.json",
                ],
                ["06-verify/verification.json"],
            ),
            command(
                "07-report",
                ["06-verify/verification.json"],
                [
                    "07-report/report.md",
                    "07-report/graph.json",
                    "07-report/graph.mmd",
                    "07-report/run-result.json",
                    "07-report/architecture.json",
                    "07-report/key-chains.json",
                    "07-report/analysis.md",
                ],
            ),
        ],
    }


def run_pipeline(
    *,
    source_root: Path,
    workspace: Path,
    run_id: str,
    build_profile: str = "demo-poll",
    defines: list[str] | None = None,
    publish_dir: Path | None = None,
    compile_commands: list[dict[str, Any]] | None = None,
    repository: str = "local-cpp-demo",
    commit: str = "local",
    entry_symbols: list[str] | None = None,
) -> dict[str, Any]:
    workspace.mkdir(parents=True, exist_ok=True)
    request = build_request(
        run_id,
        source_root,
        build_profile,
        repository=repository,
        commit=commit,
        entry_symbols=entry_symbols,
    )
    write_json(workspace / "request.json", request)
    write_json(
        workspace / "compile_commands.json",
        compile_commands
        or build_compile_commands(source_root, build_profile, defines or []),
    )
    try:
        workspace_label = workspace.relative_to(Path.cwd()).as_posix()
    except ValueError:
        workspace_label = str(workspace)
    pipeline_config = build_pipeline_config(run_id, workspace_label)
    write_json(workspace / "pipeline.json", pipeline_config)

    results = []
    for stage in pipeline_config["stages"]:
        command = [str(item).replace("{workspace}", str(workspace)) for item in stage["command"]]
        completed = subprocess.run(
            command,
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            timeout=1200,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Stage {stage['name']} failed: {completed.stderr.strip() or completed.stdout.strip()}"
            )
        try:
            summary = json.loads(completed.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            summary = {"stage": stage["name"], "status": "unknown"}
        results.append(summary)

    if publish_dir is not None:
        report_dir = workspace / "07-report"
        publish_dir.mkdir(parents=True, exist_ok=True)
        sources = [
            report_dir / name
            for name in (
                "report.md",
                "graph.json",
                "graph.mmd",
                "run-result.json",
                "architecture.json",
                "key-chains.json",
                "analysis.md",
            )
        ]
        sources.append(workspace / "pipeline.json")
        for source in sources:
            if source.exists():
                shutil.copyfile(source, publish_dir / source.name)

    return {
        "run_id": run_id,
        "workspace": str(workspace),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the 7-stage Clang pipeline")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--profile", default="demo-poll")
    parser.add_argument("--define", action="append", default=[])
    parser.add_argument("--publish", default="demo")
    parser.add_argument("--compile-commands", default="")
    parser.add_argument("--repository", default="local-cpp-demo")
    parser.add_argument("--commit", default="local")
    parser.add_argument("--entry", action="append", default=[])
    args = parser.parse_args()

    run_id = args.run_id or f"run_{__import__('datetime').datetime.now().strftime('%Y%m%d')}_clang_demo"
    compile_commands = None
    if args.compile_commands:
        compile_commands = list(read_json(Path(args.compile_commands).resolve()))
    outcome = run_pipeline(
        source_root=Path(args.source).resolve(),
        workspace=Path(args.workspace).resolve(),
        run_id=run_id,
        build_profile=args.profile,
        defines=args.define,
        publish_dir=Path(args.publish) if args.publish else None,
        compile_commands=compile_commands,
        repository=args.repository,
        commit=args.commit,
        entry_symbols=args.entry or None,
    )
    print(json.dumps(outcome, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
