# Claude Code 接入教程

## 1. 两种接入方式

### 方式 A：项目直接调用 Claude Code

```bash
cd /Users/andye/Documents/ChatGPT/8.18huawei

python3 -m clang_pipeline.cli ask \
  --question "uv_run 调用了哪些函数？" \
  --workspace demo/libuv \
  --backend claude-code
```

适用场景：

- 已有分析产物。
- 希望返回 JSON 答案。
- 希望固定 Claude Code 作为回答模型。

### 方式 B：Claude Code 通过 MCP 调用分析工具

注册 MCP：

```bash
claude mcp add code-reverse-agent \
  -s user \
  -e CRA_WORKSPACE=/Users/andye/Documents/ChatGPT/8.18huawei/demo/libuv \
  -e CRA_REPO_ROOT=/Users/andye/Documents/ChatGPT/8.18huawei \
  -e PYTHONPATH=/Users/andye/Documents/ChatGPT/8.18huawei \
  -- python3 -m clang_pipeline.mcp_server
```

检查：

```bash
claude mcp list
```

## 2. 在 Claude Code 中提问

示例：

```text
使用 code-reverse-agent 的 get_call_graph，
查看 uv_run 两层以内的调用图。
```

仓库 URL 分析：

```text
使用 code-reverse-agent 的 analyze_repo，
分析 https://github.com/example/project.git，
输出到 /tmp/project-analysis。
```

分析完成后继续询问：

```text
读取 /tmp/project-analysis/manifest.json，
总结调用链、资源流和同步关系结果。
```

## 3. 当前 MCP 工具

```text
analyze_repo
get_call_graph
get_key_chains
get_architecture
get_knowledge_graph
get_evidence
get_source_snippet
get_macro_analysis
get_visualization
read_analysis_report
```

## 4. 常见问题

### 为什么 MCP Server 启动后没有输出？

`python3 -m clang_pipeline.mcp_server` 是 stdio MCP 服务，会等待 Claude Code
通过 stdin 发送 JSON-RPC。不要单独在终端运行，应由 Claude Code 自动启动。

### 如何删除或更新 MCP？

```bash
claude mcp remove code-reverse-agent
```

然后重新执行 `claude mcp add ...`。

### 如何指定其他 workspace？

修改：

```bash
CRA_WORKSPACE=/path/to/workspace
CRA_RUN_ID=run_id
```

### 如何验证 MCP 工具列表？

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cli","version":"1"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | python3 -m clang_pipeline.mcp_server
```

## 5. Agent 调用链

```text
用户问题
  -> Claude Code 规划
  -> MCP tools/list
  -> analyze_repo / get_call_graph / get_evidence
  -> 工具返回 JSON
  -> Claude Code 读取结果
  -> 继续调用其他工具
  -> 最终回答
```
