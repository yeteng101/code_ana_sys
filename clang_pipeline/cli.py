from __future__ import annotations

import argparse
import json
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .agent import AGENT_TOOLS, AgentContext
from .agent_context import write_agent_context
from .agent_runner import ask_question
from .agent_server import AgentHandler
from .clang_ast import read_json
from .graph_store import store_graph_json
from .pipeline import DEFAULT_SOURCE, DEFAULT_WORKSPACE, run_pipeline


ROOT = Path(__file__).resolve().parents[1]


def command_analyze(args: argparse.Namespace) -> None:
    compile_commands = None
    if args.compile_commands:
        compile_commands = list(read_json(Path(args.compile_commands).resolve()))
    outcome = run_pipeline(
        source_root=Path(args.source).resolve(),
        workspace=Path(args.workspace).resolve(),
        run_id=args.run_id,
        build_profile=args.profile,
        defines=args.define,
        publish_dir=Path(args.publish) if args.publish else None,
        compile_commands=compile_commands,
        repository=args.repository,
        commit=args.commit,
        entry_symbols=args.entry or None,
    )
    print(json.dumps(outcome, ensure_ascii=False, indent=2))


def command_ask(args: argparse.Namespace) -> None:
    ctx = AgentContext(
        Path(args.workspace).resolve(),
        repo_root=Path(args.repo_root).resolve(),
        run_id=args.run_id,
    )
    result = ask_question(
        args.question,
        ctx,
        backend=args.backend,
        max_steps=args.max_steps,
        model=args.model,
        focus=args.focus or None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def command_context(args: argparse.Namespace) -> None:
    ctx = AgentContext(
        Path(args.workspace).resolve(),
        repo_root=Path(args.repo_root).resolve(),
        run_id=args.run_id,
    )
    path = write_agent_context(
        ctx,
        args.question or "analyze",
        focus=args.focus or None,
    )
    print(json.dumps({"context_file": str(path)}, ensure_ascii=False, indent=2))


def command_server(args: argparse.Namespace) -> None:
    server = ThreadingHTTPServer((args.host, args.port), AgentHandler)
    print(f"Agent Server: http://{args.host}:{args.port}")
    print("POST /api/v1/agent/ask")
    print("GET  /api/v1/agent/tools")
    print("GET  /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def command_tools(args: argparse.Namespace) -> None:
    print(json.dumps({"tools": AGENT_TOOLS}, ensure_ascii=False, indent=2))


def command_graphdb(args: argparse.Namespace) -> None:
    ctx = AgentContext(
        Path(args.workspace).resolve(),
        repo_root=Path(args.repo_root or ROOT).resolve(),
        run_id=args.run_id,
    )
    graph = ctx.load_graph()
    counts = store_graph_json(
        graph,
        args.run_id,
        uri=args.uri or None,
        user=args.user or None,
        password=args.password or None,
    )
    print(
        json.dumps(
            {"status": "succeeded", "run_id": args.run_id, **counts},
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="code-reverse-agent",
        description="完整代码逆向分析：Clang 流水线 + Agent + Claude Code/OpenAI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="运行 7 阶段流水线并生成 JSON 产物")
    analyze.add_argument("--source", default=DEFAULT_SOURCE)
    analyze.add_argument("--workspace", default=DEFAULT_WORKSPACE)
    analyze.add_argument("--run-id", required=True)
    analyze.add_argument("--profile", default="demo-poll")
    analyze.add_argument("--define", action="append", default=[])
    analyze.add_argument("--publish", default="")
    analyze.add_argument("--compile-commands", default="")
    analyze.add_argument("--repository", default="local-cpp-demo")
    analyze.add_argument("--commit", default="local")
    analyze.add_argument("--entry", action="append", default=[])
    analyze.set_defaults(func=command_analyze)

    ask = subparsers.add_parser("ask", help="自然语言提问并输出 JSON")
    ask.add_argument("--question", required=True)
    ask.add_argument("--workspace", default="demo/libuv")
    ask.add_argument("--repo-root", default=str(ROOT))
    ask.add_argument("--run-id", default="run_libuv_1.50.0")
    ask.add_argument("--backend", choices=["auto", "openai", "claude-code"], default="auto")
    ask.add_argument("--max-steps", type=int, default=6)
    ask.add_argument("--model", default=None)
    ask.add_argument("--focus", action="append", default=[])
    ask.set_defaults(func=command_ask)

    context = subparsers.add_parser("context", help="生成 Agent 上下文 JSON")
    context.add_argument("--question", default="")
    context.add_argument("--workspace", default="demo/libuv")
    context.add_argument("--repo-root", default=str(ROOT))
    context.add_argument("--run-id", default="run_libuv_1.50.0")
    context.add_argument("--focus", action="append", default=[])
    context.set_defaults(func=command_context)

    server = subparsers.add_parser("server", help="启动外部 JSON 接口服务")
    server.add_argument("--host", default="127.0.0.1")
    server.add_argument("--port", type=int, default=8090)
    server.set_defaults(func=command_server)

    tools = subparsers.add_parser("tools", help="列出大模型可调用工具")
    tools.set_defaults(func=command_tools)

    graphdb = subparsers.add_parser("graphdb", help="把调用图写入 Neo4j")
    graphdb.add_argument("--workspace", default="demo/libuv")
    graphdb.add_argument("--repo-root", default=str(ROOT))
    graphdb.add_argument("--run-id", default="run_libuv_1.50.0")
    graphdb.add_argument("--uri", default="")
    graphdb.add_argument("--user", default="")
    graphdb.add_argument("--password", default="")
    graphdb.set_defaults(func=command_graphdb)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
