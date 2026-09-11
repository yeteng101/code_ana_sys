# 周会汇报（2026-09-10）

> 本周主题：把代码逆向分析系统从“能跑流水线”推进到“能自然语言分析、能写入图数据库、能自动回归”的完整闭环。
>
> 外部接口文档：[docs/external-interfaces.md](docs/external-interfaces.md)
>
> 调用链验证集：[validation/call-chains/README.md](validation/call-chains/README.md)

## 一、本周目标

围绕 C/C++ 代码逆向分析，完成四件事：

1. 用 Clang 真正解析源码，产出带证据的调用图和关键调用链。
2. 把分析能力包装成大模型可以调用的工具层。
3. 让自然语言输入仓库路径后，自动完成分析并回答代码问题。
4. 把调用图写入 Neo4j，并接入 GitHub Actions 自动回归。

## 二、本周完成内容

### 1. Clang 七阶段分析流水线

已完成并跑通以下阶段：

```text
源码索引
  → 宏分析
  → 调用图
  → 函数指针分析
  → 异步回调链
  → 证据验证
  → 报告与架构图
```

每个阶段通过 JSON 文件接力，上一阶段输出作为下一阶段输入，不依赖中心化 Orchestrator。

真实 libuv v1.50.0 分析结果：

| 指标 | 结果 |
|---|---:|
| 函数/回调节点 | 633 |
| 调用边 | 1481 |
| 源码证据 | 1543 |
| 验证覆盖率 | 79.37% |
| 当前状态 | partial |

样例工程 `demo/sample` 已做到完整通过，覆盖直接调用、函数指针、异步回调和证据片段。

### 2. 自然语言驱动的仓库分析

新增了“问题中包含仓库路径，自动先分析再回答”的能力。

示例：

```bash
python3 -m clang_pipeline.cli ask \
  --question "请分析仓库 /path/to/libuv，uv_run 调用了谁？" \
  --backend claude-code
```

执行过程：

1. 从自然语言中识别仓库路径。
2. 自动查找 `compile_commands.json`，找不到时生成通用编译数据库。
3. 自动运行七阶段流水线。
4. 生成 Agent 上下文。
5. 调用 Claude Code / OpenAI 回答。
6. 输出 JSON 结果、分析工作目录和证据链。

如果只想查询已有产物，不重新分析，可以加：

```bash
python3 -m clang_pipeline.cli ask \
  --question "uv_run 调用了谁？" \
  --workspace demo/libuv \
  --no-auto-analyze \
  --backend claude-code
```

### 3. Agent 工具层与 MCP

项目向大模型暴露以下工具：

```text
analyze_repo
get_call_graph
get_key_chains
get_architecture
get_evidence
get_source_snippet
get_macro_analysis
read_analysis_report
```

已完成三种接入方式：

| 接入方式 | 用途 |
|---|---|
| Claude Code CLI | 本地直接调用 Claude Code 分析 |
| MCP stdio 服务 | 让 Claude Code 调用我们的代码分析工具 |
| HTTP JSON 服务 | 给外部程序或后续网页调用 |

Claude Code 注册我们自己的 MCP：

```bash
claude mcp add code-reverse-agent \
  -s user \
  -e CRA_WORKSPACE=/Users/andye/Documents/ChatGPT/8.18huawei/demo/libuv \
  -e CRA_REPO_ROOT=/Users/andye/Documents/ChatGPT/8.18huawei \
  -e PYTHONPATH=/Users/andye/Documents/ChatGPT/8.18huawei \
  -- python3 -m clang_pipeline.mcp_server
```

### 4. Neo4j 图数据库

调用图现在可以写入 Neo4j 5.26。

本次采用“调用边重实体”模型：

```text
CodeNode      源码函数或回调节点
CallEdge      一条调用边的重实体
Evidence      源码证据

CodeNode -[:HAS_CALL_EDGE]-> CallEdge
CallEdge -[:CALL_TARGET]-> CodeNode
CallEdge -[:HAS_EVIDENCE]-> Evidence
```

这样每条调用边都能直接关联多条源码证据，不会出现“关系再连关系”的非法图模型。

GitHub Actions 真实 Neo4j 容器回查结果：

| 指标 | 写入 | 回查 |
|---|---:|---:|
| CodeNode | 633 | 633 |
| CallEdge | 1481 | 1481 |
| Evidence | 1543 | 1543 |
| 带证据的调用边 | 1481 | 1481 |

本地启动 Neo4j：

```bash
bash scripts/start_neo4j.sh
```

写入并回查：

```bash
python3 scripts/verify_neo4j.py \
  --workspace demo/libuv \
  --run-id run_libuv_1.50.0
```

### 5. GitHub Actions 自动回归

新增工作流：

```text
.github/workflows/regression.yml
```

每次 push 或 pull request 自动执行：

- 样例 Clang 七阶段流水线
- Agent 工具层测试
- MCP stdio 协议测试
- HTTP JSON 接口测试
- Neo4j 写入与回查

Neo4j 回查结果会作为 `neo4j-verification` artifact 上传，可在 GitHub Actions 运行页面下载。

### 6. 任务看板同步

当前 Kanb 看板已建立 9 个任务：

- libuv 真实流水线：已完成
- Agent / HTTP / MCP 框架：已完成
- GitHub Actions 回归：已完成
- Neo4j 端到端验证：已完成
- 毕业实习报告：已完成
- libuv 覆盖率提升到 90%：待办
- Redis 真实仓库分析：待办
- Claude Code MCP 端到端提问：待办
- OpenAI API Key 端到端验证：进行中

## 三、关键产物在哪里

### 1. 分析产物

```text
demo/libuv/graph.json          调用图
demo/libuv/architecture.json   模块架构
demo/libuv/key-chains.json     关键调用链
demo/libuv/analysis.md         自然语言分析报告
demo/libuv/run-result.json     统一运行结果
```

### 2. 完整七阶段产物

```text
demo/run_libuv_v1.50.0/
├── 01-index/symbols.json
├── 02-macro/macros.json
├── 03-callgraph/callgraph.json
├── 04-fptr/fptr-candidates.json
├── 05-async/async-chains.json
├── 06-verify/verification.json
└── 07-report/
```

### 3. Neo4j 数据库产物

Neo4j 的真实数据库文件在 Docker 容器数据卷里，不在 Git 仓库中。仓库里保存的是“源图”和“可验证结果”：

```text
demo/libuv/graph.json
  写入 Neo4j 的源调用图

GitHub Actions artifact: neo4j-verification
  Neo4j 写入后回查得到的验证 JSON
```

如果需要重新导出 Neo4j 中的数据，可以执行 Cypher：

```cypher
MATCH (n:CodeNode {run_id: 'run_libuv_1.50.0'})
RETURN n.id, n.name, n.kind
LIMIT 50;
```

```cypher
MATCH (a:CodeNode {run_id: 'run_libuv_1.50.0'})
      -[r:CALLS {run_id: 'run_libuv_1.50.0'}]->(b)
RETURN a.name, r.kind, b.name, r.confidence
LIMIT 50;
```

## 四、本周遇到的问题与解决

### 问题 1：Neo4j 不能把关系直接连到关系

最初设计为：

```text
CALLS -> HAS_EVIDENCE -> Evidence
```

但 Neo4j 属性图里，关系只能连接节点，不能连接其他关系。CI 真容器运行后暴露了问题，最后改成 `CallEdge` 节点重实体模型，调用边和证据现在都能被正确回查。

### 问题 2：本机 Docker daemon 不可用

本机无法稳定启动 Neo4j 容器，因此把真实 Neo4j 验证放入 GitHub Actions：

- 使用 `neo4j:5.26` service container
- 写入真实的 1481 条调用边
- 回查节点、边、证据和 `uv_run` 出边
- 上传验证 artifact

这样不依赖本机 Docker，也能保证回归结果可复现。

### 问题 3：CI 缺少 libuv 源码

CI 首次运行时 Agent 测试找不到 `third_party/libuv/src/unix/core.c`，因为源码目录被 `.gitignore` 排除了。工作流已增加固定版本 libuv 源码 checkout，测试恢复通过。

## 五、周会现场可以演示什么

推荐演示顺序：

1. 打开 Kanb 看板，展示本周任务状态和依赖关系。
2. 运行自然语言分析：

```bash
python3 -m clang_pipeline.cli ask \
  --question "请分析仓库 /Users/andye/Documents/ChatGPT/8.18huawei/demo/sample，loop_run 调用了谁？" \
  --backend claude-code
```

3. 展示 `demo/libuv/graph.json` 和 `key-chains.json`。
4. 打开 GitHub Actions Regression 页面，展示：
   - Python/Clang 回归通过
   - MCP 协议通过
   - Neo4j 真容器回查通过
   - `neo4j-verification` artifact 可下载
5. 展示 Claude Code 通过 MCP 调用 `get_call_graph` 或 `get_key_chains`。

### 验证集当前进度

调用链正负样本第一版已完成：

```text
validation/call-chains/dataset.json
```

当前包含：

| 类型 | 数量 |
|---|---:|
| 正样本 | 22 |
| 负样本 | 14 |
| 合计 | 36 |

校验命令：

```bash
python3 scripts/check_call_chain_validation.py \
  --dataset validation/call-chains/dataset.json \
  --graph demo/graph.json \
  --graph demo/libuv/graph.json
```

当前校验结果：

```text
status: verified
positive: 10
negative: 6
errors: 0
```

资源流样本第一版也已完成：

```text
validation/resource-flow/dataset.json
```

| 类型 | 数量 |
|---|---:|
| no_leak | 7 |
| leak | 1 |
| double_free | 1 |
| use_after_free | 1 |
| uncertain | 0 |
| 合计 | 10 |

资源流校验命令：

```bash
python3 scripts/check_resource_flow_validation.py \
  --dataset validation/resource-flow/dataset.json
```

## 六、下周计划

| 优先级 | 任务 | 目标 |
|---|---|---|
| P0 | 提升 libuv 验证覆盖率 | 79.4% → 90% |
| P0 | Redis 固定 commit 真实分析 | 跑通 CMake + compile_commands |
| P1 | Claude Code MCP 全链路 | 自然语言提问 → 工具调用 → JSON 答案 |
| P1 | OpenAI Key 端到端 | 配置 secret 后跑真实模型验证 |
| P2 | 导出 Neo4j 查询结果 | 生成节点/边/证据 CSV 或 JSON |

## 七、风险和待确认

- libuv 仍有约 20.6% 调用边无法唯一确认，主要来自函数指针和平台条件编译。
- Redis 目前仍是 fixture，不能算真实仓库分析结果。
- OpenAI 真实调用需要先在 GitHub 仓库配置 `OPENAI_API_KEY` secret。
- Neo4j 数据默认在容器卷中；如果要作为汇报附件，需要额外导出节点/边 JSON 或 CSV。

## 八、相关链接

- GitHub 分支：<https://github.com/yeteng101/code_ana_sys/tree/codex/agent-llm-framework>
- GitHub Actions：<https://github.com/yeteng101/code_ana_sys/actions/workflows/regression.yml>
- Kanb 看板：<https://workflow.yeteng.xin>
- 项目原 README：从下一节开始保留

---

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

GitHub Actions 会在 push 和 pull request 时自动执行：

- 样例 Clang 七阶段流水线回归
- Agent 工具与 MCP stdio 协议回归
- `call_chain_demo` 的 JSON/HTTP 回归
- Neo4j 写入、回查节点/边/证据数量和 `uv_run` 出边

OpenAI 真实调用只在手动触发 `workflow_dispatch` 且仓库配置了
`OPENAI_API_KEY` secret 时执行，避免普通提交产生 API 成本。

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

## Claude Code 通过 MCP 调用工具层

本项目提供 MCP 工具服务，Claude Code 可以直接调用我们的工具：

```bash
export CRA_WORKSPACE=/path/to/code_ana_sys/demo/libuv
export CRA_REPO_ROOT=/path/to/code_ana_sys

claude mcp add code-reverse-agent \
  -- python3 -m clang_pipeline.mcp_server
```

Claude Code 中会看到这些工具：

```text
analyze_repo
get_call_graph
get_key_chains
get_architecture
get_evidence
get_source_snippet
get_macro_analysis
read_analysis_report
```

也可以手动测试 MCP 服务：

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_key_chains","arguments":{}}}' \
  | python3 -m clang_pipeline.mcp_server
```

## 调用图存入图数据库

启动 Neo4j：

```bash
bash scripts/start_neo4j.sh
```

设置连接参数：

```bash
export NEO4J_URI=http://127.0.0.1:7474
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=codeana123
```

写入调用图：

```bash
python3 -m clang_pipeline.cli graphdb \
  --workspace demo/libuv \
  --run-id run_libuv_1.50.0 \
  --verify
```

Neo4j 中会创建：

```text
CodeNode   函数 / 回调节点
Evidence   源码证据
CALLS      调用关系
CallEdge    调用边的重实体，保存 kind/confidence/evidence_ids
HAS_CALL_EDGE  CodeNode 到 CallEdge
CALL_TARGET    CallEdge 到目标 CodeNode
HAS_EVIDENCE   CallEdge 到 Evidence
```

也可以直接运行端到端校验脚本。它会等待 Neo4j 就绪，写入调用图，然后回查
`CodeNode`、`CALLS`、`Evidence`、`HAS_EVIDENCE` 数量，并抽样验证
`uv_run` 的出边：

```bash
python3 scripts/verify_neo4j.py \
  --workspace demo/libuv \
  --run-id run_libuv_1.50.0
```

如果 Neo4j 不在本机默认端口，传入：

```bash
python3 scripts/verify_neo4j.py \
  --uri http://127.0.0.1:7474 \
  --user neo4j \
  --password codeana123
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

### 怎么验证 OpenAI API Key 端到端可用？

先设置 Key 和模型：

```bash
export OPENAI_API_KEY='sk-...'
export OPENAI_MODEL='gpt-5'
```

然后执行：

```bash
python3 scripts/verify_openai.py --workspace demo/libuv
```

脚本检查三件事：

1. `OPENAI_API_KEY` 是否存在；
2. 模型是否能通过 Agent 调用 `get_call_graph` 等工具；
3. 最终是否返回 `status=succeeded` 的 JSON 答案。

如果没有 Key，脚本会返回 `status=skipped` 并打印下一步命令，不会伪造成功。

### libuv 的 workspace 不在 Git 里？

`demo/run_libuv_v1.50.0/` 是运行产物，被 `.gitignore` 排除。需要重新生成：

```bash
bash scripts/run_libuv.sh
```

### Neo4j 镜像下载慢？

`scripts/start_neo4j.sh` 会拉取 `neo4j:5.26`，首次可能需要较长时间；也可以使用已有 Neo4j，设置 `NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD` 后直接执行 `cli graphdb`。

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
