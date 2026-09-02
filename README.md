# Code Reverse Agent

一个完整可运行的代码逆向分析项目：

```text
C/C++ 源码
   → Clang/libclang 解析
   → 7 阶段 JSON 流水线
   → Evidence Graph
   → Agent 上下文
   → Claude Code / OpenAI
   → 自然语言 JSON 回答
```

## 环境要求

- Python 3.9+
- Clang / clang++
- macOS：`xcode-select --install`
- Ubuntu/Debian：`sudo apt install clang`
- 可选：Claude Code（`claude`）
- 可选：OpenAI API Key

项目使用 Python 标准库，不需要 `pip install`。

## 目录结构

```text
clang_pipeline/
├── pipeline.py            流水线驱动
├── stage_runner.py        单阶段执行入口
├── stages.py              7 个阶段实现
├── libclang_extract.py    用 libclang 提取紧凑 AST
├── agent.py               Agent 工具层 + OpenAI 循环
├── agent_context.py       生成小体积 Agent 上下文 JSON
├── agent_runner.py        统一自然语言入口
├── agent_cli.py           CLI，JSON 输出到 stdout
├── agent_server.py        HTTP JSON 服务
├── claude_code_bridge.py  调用 Claude Code CLI
├── cli.py                 统一命令行
└── llm_bridge.py          OpenAI API 桥接

demo/
├── sample/                自包含 C++ 样例
├── libuv/                 真实 libuv v1.50.0 分析产物
└── run_clang_demo/        样例运行工作目录

schemas/                   JSON Schema
scripts/run_libuv.sh       一键跑 libuv
```

## 快速开始

### 1. 跑样例流水线

```bash
cd /path/to/code_ana_sys

python3 -m clang_pipeline.cli analyze \
  --source demo/sample \
  --workspace demo/run_clang_demo \
  --run-id run_sample_demo \
  --publish demo
```

或者一键脚本：

```bash
bash run_demo.sh
```

### 2. 跑真实 libuv

```bash
bash scripts/run_libuv.sh
```

脚本会：

1. clone libuv v1.50.0
2. 用 CMake 生成真实 `compile_commands.json`
3. 跑完整 7 阶段流水线
4. 发布产物到 `demo/libuv/`

### 3. 用 Claude Code 提问

本机 Claude Code 命令是 `claude`，不是 `cc`：

```bash
claude --version
```

提问：

```bash
python3 -m clang_pipeline.agent_cli \
  --question "uv_run 调用了谁？" \
  --workspace demo/libuv \
  --backend claude-code
```

stdout 输出 JSON：

```json
{
  "run_id": "run_libuv_1.50.0",
  "question": "uv_run 调用了谁？",
  "answer": "uv_run 会调用 uv__io_poll 等待就绪事件...",
  "confidence": 0.9,
  "evidence_chain": [],
  "status": "succeeded"
}
```

### 4. 用 OpenAI 提问

```bash
export OPENAI_API_KEY=sk-你的key
export OPENAI_MODEL=gpt-5

python3 -m clang_pipeline.agent_cli \
  --question "uv_run 调用了谁？" \
  --workspace demo/libuv \
  --backend openai
```

### 5. 自动选择后端

```bash
python3 -m clang_pipeline.agent_cli \
  --question "uv_async_send 之后回调怎么触发？" \
  --workspace demo/libuv \
  --backend auto
```

`auto` 优先级：

```text
claude-code（本机有 claude）
→ openai（有 OPENAI_API_KEY）
→ 规则模板 fallback
```

## 统一 CLI

```bash
# 运行流水线
python3 -m clang_pipeline.cli analyze \
  --source demo/sample \
  --workspace demo/run_clang_demo \
  --run-id run_sample_demo

# 自然语言提问
python3 -m clang_pipeline.cli ask \
  --question "uv_run 调用了谁？" \
  --workspace demo/libuv \
  --backend claude-code

# 只生成 Agent 上下文
python3 -m clang_pipeline.cli context \
  --question "uv_run 调用了谁？" \
  --workspace demo/libuv

# 列出大模型工具
python3 -m clang_pipeline.cli tools

# 启动外部服务
python3 -m clang_pipeline.cli server --port 8090
```

## Agent 上下文

不会把大 JSON 塞进 prompt，而是生成小体积 `agent-context.json`：

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "question": "uv_run 调用了谁？",
  "key_chains": [],
  "evidence": [],
  "artifact_paths": {
    "graph": ".../graph.json",
    "architecture": ".../architecture.json"
  }
}
```

Claude Code 先读小上下文，再按需读取大产物。

## 外部 JSON 服务

```bash
python3 -m clang_pipeline.cli server --port 8090
```

接口：

```text
GET  /health
GET  /api/v1/agent/tools
POST /api/v1/agent/ask
```

提问：

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "uv_run 调用了谁？",
    "workspace": "demo/libuv",
    "backend": "claude-code"
  }' \
  http://127.0.0.1:8090/api/v1/agent/ask
```

## 产物说明

| 产物 | 内容 |
|---|---|
| `01-index/symbols.json` | 函数、字段、类型索引 |
| `02-macro/macros.json` | 宏定义、展开、条件编译 |
| `03-callgraph/callgraph.json` | 调用图 |
| `04-fptr/fptr-candidates.json` | 函数指针候选 |
| `05-async/async-chains.json` | 异步回调链 |
| `06-verify/verification.json` | 验证与覆盖率 |
| `07-report/graph.json` | 最终调用图 |
| `07-report/architecture.json` | 模块架构 |
| `07-report/key-chains.json` | 关键调用链 |
| `07-report/analysis.md` | 自然语言分析 |

所有结论都带证据：

```json
{
  "id": "ev_a3dcf6ec0abb",
  "kind": "call_site",
  "location": {
    "file": "third_party/libuv/src/unix/core.c",
    "line": 460,
    "snippet": "uv__io_poll(loop, timeout);"
  }
}
```

## 测试

```bash
python3 -m unittest discover -s clang_pipeline/tests -v
python3 -m unittest discover -s call_chain_demo/tests -v
```

## Claude Code 注意

macOS 上：

```text
cc      = Apple Clang 编译器
claude  = Claude Code
```

代码默认调用 `claude`。如果需要自定义：

```bash
export CLAUDE_CODE_BIN=/path/to/claude
```

## 常见问题

### 没有 API Key 会怎样？

不会崩溃，返回规则模板结果：

```json
{
  "status": "partial",
  "answer": "当前未配置大模型 API Key..."
}
```

### libuv 的 workspace 不在 Git 里？

`demo/run_libuv_v1.50.0/` 是运行产物，被 `.gitignore` 排除。需要重新生成：

```bash
bash scripts/run_libuv.sh
```

### 想把分析接到自己仓库？

1. 生成该仓库的 `compile_commands.json`
2. 调用：

```bash
python3 -m clang_pipeline.cli analyze \
  --source /path/to/repo \
  --workspace /path/to/workspace \
  --run-id run_my_repo \
  --compile-commands /path/to/compile_commands.json
```
