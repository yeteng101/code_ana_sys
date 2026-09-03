from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from .llm_bridge import DEFAULT_MODEL, api_key, llm_enabled


CHAT_URL = "https://api.openai.com/v1/chat/completions"
MAX_TOOL_RESULT_CHARS = 20000


class AgentToolError(RuntimeError):
    pass


class AgentContext:
    def __init__(
        self,
        workspace: Path | str,
        *,
        repo_root: Path | str | None = None,
        run_id: str = "run_libuv_1.50.0",
    ) -> None:
        self.workspace = Path(workspace)
        self.repo_root = Path(repo_root or Path.cwd())
        self.run_id = run_id

    def _find_artifact(self, *names: str) -> Path | None:
        for name in names:
            path = self.workspace / name
            if path.exists():
                return path
        return None

    def load_json(self, *names: str) -> dict[str, Any]:
        path = self._find_artifact(*names)
        if path is None:
            raise AgentToolError(f"找不到产物: {names[0]}")
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)

    def load_graph(self) -> dict[str, Any]:
        return self.load_json(
            "07-report/graph.json",
            "graph.json",
            "03-callgraph/callgraph.json",
        )

    def load_key_chains(self) -> dict[str, Any]:
        return self.load_json("07-report/key-chains.json", "key-chains.json")

    def load_architecture(self) -> dict[str, Any]:
        return self.load_json("07-report/architecture.json", "architecture.json")

    def load_macros(self) -> dict[str, Any] | None:
        path = self._find_artifact("02-macro/macros.json", "macros.json")
        if path is None:
            return None
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)

    def read_analysis(self) -> str:
        path = self._find_artifact("07-report/analysis.md", "analysis.md")
        if path is None:
            return ""
        return path.read_text(encoding="utf-8")

    def source_snippet(self, file: str, line: int, radius: int = 3) -> str:
        path = Path(file)
        if not path.is_absolute():
            path = self.repo_root / file
        if not path.exists():
            raise AgentToolError(f"源码不存在: {file}")
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not 1 <= line <= len(lines):
            raise AgentToolError(f"行号越界: {file}:{line}")
        start = max(1, line - radius)
        end = min(len(lines), line + radius)
        numbered = [f"{i}: {lines[i - 1]}" for i in range(start, end + 1)]
        return "\n".join(numbered)


AGENT_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "analyze_repo",
            "description": "运行完整 7 阶段 Clang 流水线并生成 JSON 产物。",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "源码目录"},
                    "workspace": {"type": "string", "description": "产物工作目录"},
                    "run_id": {"type": "string"},
                    "compile_commands": {
                        "type": "string",
                        "description": "可选，compile_commands.json 路径",
                    },
                    "build_profile": {"type": "string", "default": "default"},
                },
                "required": ["source", "workspace", "run_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_call_graph",
            "description": "获取调用关系图，可按入口函数和深度过滤。",
            "parameters": {
                "type": "object",
                "properties": {
                    "entry": {"type": "string", "description": "入口函数名，如 uv_run"},
                    "depth": {"type": "integer", "minimum": 1, "maximum": 20},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_key_chains",
            "description": "获取关键调用链。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_architecture",
            "description": "获取模块架构和组件依赖。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_evidence",
            "description": "按 evidence_id 查询源码证据。",
            "parameters": {
                "type": "object",
                "properties": {
                    "evidence_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    }
                },
                "required": ["evidence_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_source_snippet",
            "description": "查看源码文件某一行的上下文。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                },
                "required": ["file", "line"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_macro_analysis",
            "description": "查询宏定义、展开、条件编译和调用点。",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_analysis_report",
            "description": "读取已有的自然语言分析报告。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def _tool_get_call_graph(ctx: AgentContext, args: dict[str, Any]) -> Any:
    graph = ctx.load_graph()
    entry = args.get("entry")
    depth = int(args.get("depth", 5))
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if entry:
        node_ids = {node["id"] for node in nodes if node.get("name") == entry}
        if not node_ids:
            return {"error": f"未找到入口函数 {entry}"}
        reachable = _reachable_subgraph(nodes, edges, node_ids, depth)
        nodes = reachable["nodes"]
        edges = reachable["edges"]
    return {
        "nodes": nodes[:500],
        "edges": edges[:800],
        "evidence": graph.get("evidence", [])[:300],
    }


def _tool_get_key_chains(ctx: AgentContext, args: dict[str, Any]) -> Any:
    return ctx.load_key_chains()


def _tool_get_architecture(ctx: AgentContext, args: dict[str, Any]) -> Any:
    return ctx.load_architecture()


def _tool_get_evidence(ctx: AgentContext, args: dict[str, Any]) -> Any:
    graph = ctx.load_graph()
    evidence_by_id = {item["id"]: item for item in graph.get("evidence", [])}
    ids = args.get("evidence_ids", [])
    return {
        "evidence": [
            evidence_by_id[evidence_id]
            for evidence_id in ids
            if evidence_id in evidence_by_id
        ],
        "missing_ids": [evidence_id for evidence_id in ids if evidence_id not in evidence_by_id],
    }


def _tool_get_source_snippet(ctx: AgentContext, args: dict[str, Any]) -> Any:
    return {
        "file": args["file"],
        "line": int(args["line"]),
        "snippet": ctx.source_snippet(args["file"], int(args["line"])),
    }


def _tool_get_macro_analysis(ctx: AgentContext, args: dict[str, Any]) -> Any:
    macros = ctx.load_macros()
    if macros is None:
        return {"error": "当前产物目录没有 macros.json"}
    name = args.get("name")
    expansions = macros.get("expansions", [])
    if name:
        expansions = [item for item in expansions if item.get("name") == name]
    return {
        "expansions": expansions[:50],
        "conditional_regions": macros.get("conditional_regions", [])[:50],
    }


def _tool_read_analysis_report(ctx: AgentContext, args: dict[str, Any]) -> Any:
    text = ctx.read_analysis()
    return {"analysis": text[:MAX_TOOL_RESULT_CHARS]}


def _tool_analyze_repo(ctx: AgentContext, args: dict[str, Any]) -> Any:
    from .pipeline import run_pipeline

    compile_commands = None
    if args.get("compile_commands"):
        from .clang_ast import read_json

        compile_commands = list(read_json(Path(args["compile_commands"]).resolve()))
    outcome = run_pipeline(
        source_root=Path(args["source"]).resolve(),
        workspace=Path(args["workspace"]).resolve(),
        run_id=str(args["run_id"]),
        build_profile=str(args.get("build_profile") or "default"),
        publish_dir=None,
        compile_commands=compile_commands,
    )
    return {
        "status": "succeeded",
        "run_id": outcome["run_id"],
        "workspace": outcome["workspace"],
    }


TOOL_IMPLEMENTATIONS: dict[str, Callable[[AgentContext, dict[str, Any]], Any]] = {
    "analyze_repo": _tool_analyze_repo,
    "get_call_graph": _tool_get_call_graph,
    "get_key_chains": _tool_get_key_chains,
    "get_architecture": _tool_get_architecture,
    "get_evidence": _tool_get_evidence,
    "get_source_snippet": _tool_get_source_snippet,
    "get_macro_analysis": _tool_get_macro_analysis,
    "read_analysis_report": _tool_read_analysis_report,
}


def _reachable_subgraph(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    entry_ids: set[str],
    depth: int,
) -> dict[str, list[dict[str, Any]]]:
    node_ids = set(entry_ids)
    current = set(entry_ids)
    selected_edges: list[dict[str, Any]] = []
    for _ in range(depth):
        next_nodes: set[str] = set()
        for edge in edges:
            if edge["source"] in current and edge["target"] not in node_ids:
                next_nodes.add(edge["target"])
                selected_edges.append(edge)
        if not next_nodes:
            break
        node_ids.update(next_nodes)
        current = next_nodes
    return {
        "nodes": [node for node in nodes if node["id"] in node_ids],
        "edges": [
            edge for edge in edges if edge["source"] in node_ids and edge["target"] in node_ids
        ],
    }


def execute_tool(ctx: AgentContext, name: str, args: dict[str, Any]) -> str:
    implementation = TOOL_IMPLEMENTATIONS.get(name)
    if implementation is None:
        raise AgentToolError(f"未知工具: {name}")
    try:
        result = implementation(ctx, args)
    except Exception as exc:
        result = {"error": str(exc)}
    text = json.dumps(result, ensure_ascii=False)
    if len(text) > MAX_TOOL_RESULT_CHARS:
        text = text[:MAX_TOOL_RESULT_CHARS] + "\n...truncated"
    return text


def chat_completion(
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": 0.2,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    request = urllib.request.Request(
        CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Agent LLM 请求失败: {exc.code} {detail}") from exc
    try:
        return data["choices"][0]["message"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Agent LLM 返回格式异常: {json.dumps(data, ensure_ascii=False)[:500]}") from exc


SYSTEM_PROMPT = (
    "你是代码逆向分析专家 Agent。你可以调用工具获取调用图、关键链、架构、证据和源码。"
    "所有结论必须基于工具返回的事实，禁止编造源码。"
    "最终必须返回 JSON object，格式为 "
    '{"answer": "...", "confidence": 0.0-1.0, "evidence_ids": [...], "disclaimer": "..."}。'
)


def run_agent(
    question: str,
    ctx: AgentContext,
    *,
    max_steps: int = 6,
    model: str | None = None,
) -> dict[str, Any]:
    if not llm_enabled():
        return fallback_answer(question, ctx)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    trace: list[dict[str, Any]] = []
    for _ in range(max_steps):
        message = chat_completion(messages, tools=AGENT_TOOLS, model=model)
        messages.append(message)
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            return _final_result(message, trace, question, ctx)
        for tool_call in tool_calls[:4]:
            name = tool_call.get("function", {}).get("name", "")
            raw_args = tool_call.get("function", {}).get("arguments", "{}")
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
            try:
                output = execute_tool(ctx, name, args)
                status = "ok"
            except Exception as exc:
                output = json.dumps({"error": str(exc)}, ensure_ascii=False)
                status = "error"
            trace.append({"tool": name, "status": status, "arguments": args})
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.get("id", ""),
                    "content": output,
                }
            )
    return {
        "run_id": ctx.run_id,
        "question": question,
        "answer": "Agent 已达到最大工具调用步数，未能生成最终答案。",
        "confidence": 0.1,
        "evidence_chain": [],
        "disclaimer": "达到 max_steps 限制。",
        "tool_calls": trace,
        "status": "partial",
    }


def _final_result(
    message: dict[str, Any],
    trace: list[dict[str, Any]],
    question: str,
    ctx: AgentContext,
) -> dict[str, Any]:
    content = message.get("content") or "{}"
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {"answer": content, "confidence": 0.5, "evidence_ids": []}
    evidence_ids = parsed.get("evidence_ids", [])
    graph = ctx.load_graph()
    evidence_by_id = {item["id"]: item for item in graph.get("evidence", [])}
    evidence_chain = [
        evidence_by_id[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in evidence_by_id
    ]
    return {
        "run_id": ctx.run_id,
        "question": question,
        "answer": parsed.get("answer", content),
        "confidence": float(parsed.get("confidence", 0.5)),
        "evidence_chain": evidence_chain,
        "paths": parsed.get("paths", []),
        "disclaimer": parsed.get("disclaimer", ""),
        "tool_calls": trace,
        "status": "succeeded",
    }


def fallback_answer(question: str, ctx: AgentContext) -> dict[str, Any]:
    analysis = ctx.read_analysis()
    if analysis:
        answer = f"当前未配置大模型 API Key，以下为规则模板结果。\n\n{analysis[:4000]}"
    else:
        answer = "当前未配置 OPENAI_API_KEY，且没有找到 analysis.md。"
    return {
        "run_id": ctx.run_id,
        "question": question,
        "answer": answer,
        "confidence": 0.3,
        "evidence_chain": [],
        "disclaimer": "规则模板结果，非大模型分析。",
        "tool_calls": [],
        "status": "partial",
    }
