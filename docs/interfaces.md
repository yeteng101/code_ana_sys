# 代码逆向 Agent：接口与 JSON 规范

版本：1.0（2026-08-26）  
适用对象：本组（实现方）与所有需要对接的协作组（调用方 / 提供方）  
分析后端：Clang（LibTooling + PPCallbacks），目标仓库：libuv / Redis（C/C++）

> 本文档是对外/对内接口的唯一事实来源；`schemas/` 目录下的 JSON Schema 文件是格式的机器可读定义，以 Schema 为准。

## 0. 我们提供什么

一句话：**别人给我一个"仓库 + commit + 想分析的函数或问题"，我还给他"带源码证据的调用链、异步回调链、函数指针候选、宏差异和自然语言解释"。**

本项目是一个独立的代码逆向分析 Subagent：

- 对外：通过 HTTP API 提供服务，其他组直接调用；
- 对内：7 个分析阶段用 JSON 文件接力，**没有 Orchestrator 统一调度**，由极简 pipeline driver 按顺序执行；
- 所有中间结果与最终结果都是 JSON，格式由 `schemas/` 下的 JSON Schema 约束。

## 1. 接口全景

```text
外部调用方 / 其他协作组
        │  HTTP /api/v1（JSON）
        ▼
┌─────────────────────────────────┐
│   代码逆向分析 Subagent（本项目）   │
│  ┌────── 对内文件管道（JSON）──────┐ │
│  │ 01-index → 02-macro →        │ │
│  │ 03-callgraph → 04-fptr →     │ │
│  │ 05-async → 06-verify →       │ │
│  │ 07-report                    │ │
│  └──────────────────────────────┘ │
└─────────────────────────────────┘
```

## 2. 分析技术栈（Clang）

| 阶段 | 用到的 Clang 能力 | 产物 |
|---|---|---|
| 编译数据库 | CMake `CMAKE_EXPORT_COMPILE_COMMANDS=ON` / Bear | `compile_commands.json` |
| 源码索引 | `clang::tooling` + RecursiveASTVisitor | `01-index/symbols.json` |
| 宏分析 | `PPCallbacks`（宏定义 / 展开 / 条件编译） | `02-macro/macros.json` |
| 调用图 | `ASTMatcher` 匹配 CallExpr | `03-callgraph/callgraph.json` |
| 函数指针 | AST + 类型约束 + 赋值流（疑难场景可选 SVF） | `04-fptr/fptr-candidates.json` |
| 异步链 | 注册点 / 事件源 / 回调字段匹配 | `05-async/async-chains.json` |
| 验证 | 对源码重查 + 交叉验证 | `06-verify/verification.json` |

原则：**Clang 负责"事实"，模型只负责"解释"**；任何进入报告的结论必须挂上 Clang 产出的证据。

## 3. 对外接口（HTTP REST）

### 3.1 通用约定

- Base URL：`http://<host>:<port>/api/v1`（Demo 默认 `http://127.0.0.1:8080/api/v1`）
- 请求 / 响应体：`application/json`（`graph` 端点可用 `format` 参数返回 `text/plain` 的 Mermaid / DOT）
- 时间格式：ISO 8601 UTC，如 `2026-08-26T08:00:00Z`
- 认证：Demo 阶段可选 `Authorization: Bearer <token>`；正式接入由部署方提供
- 幂等：`POST /analyze` 携带 `task_id`，同一 `task_id` 重复提交返回同一 `run_id`
- 版本：URL 路径 `/v1` 为不兼容大版本；消息内 `schema_version` 为字段级小版本

### 3.2 端点清单

| 方法 | 路径 | 作用 | 响应 Schema |
|---|---|---|---|
| POST | `/analyze` | 提交分析任务 | `run-accepted.schema.json` |
| GET | `/runs/{run_id}` | 查询任务状态与摘要 | `run-result.schema.json` |
| GET | `/runs/{run_id}/graph` | 获取调用关系 / 证据图 | `graph.schema.json` |
| GET | `/runs/{run_id}/artifacts` | 获取中间产物清单 | `artifacts.schema.json` |
| POST | `/runs/{run_id}/questions` | 自然语言提问 | `question.schema.json` |
| GET | `/schemas/{name}` | 拉取 JSON Schema（供对接） | 对应 Schema 文件 |

### 3.3 端点详情

#### 3.3.1 POST /api/v1/analyze —— 提交分析

请求体（`analysis-request.schema.json`）：

```json
{
  "schema_version": "1.0",
  "task_id": "demo-libuv-loop",
  "repository": {
    "url": "https://github.com/libuv/libuv",
    "commit": "f5b9d8a1",
    "language": "c"
  },
  "build_profiles": [
    {"name": "linux-debug", "defines": ["_GNU_SOURCE"], "target": "default", "compiler": "clang"}
  ],
  "query": {
    "type": "call_chain",
    "entry_symbols": ["uv_run"],
    "depth": 8,
    "include_async": true,
    "include_function_pointers": true
  },
  "webhook_url": "http://other-team.example.com/callback"
}
```

成功响应 `202 Accepted`（`run-accepted.schema.json`）：

```json
{
  "schema_version": "1.0",
  "run_id": "run_20260826_demo_libuv",
  "task_id": "demo-libuv-loop",
  "status": "queued",
  "links": {
    "status": "http://127.0.0.1:8080/api/v1/runs/run_20260826_demo_libuv",
    "graph": "http://127.0.0.1:8080/api/v1/runs/run_20260826_demo_libuv/graph",
    "artifacts": "http://127.0.0.1:8080/api/v1/runs/run_20260826_demo_libuv/artifacts"
  }
}
```

#### 3.3.2 GET /api/v1/runs/{run_id} —— 查状态与结果

响应（`run-result.schema.json`）：

```json
{
  "schema_version": "1.0",
  "run_id": "run_20260826_demo_libuv",
  "task_id": "demo-libuv-loop",
  "status": "succeeded",
  "summary": "uv_run 在 Unix 事件循环中依次执行 pending/prepare/io_poll 等阶段；io_poll 就绪后通过 watcher 回调派发事件。",
  "findings": [
    {"kind": "direct_call", "source": "uv_run", "target": "uv__io_poll", "condition": "linux-debug", "confidence": 0.99, "evidence_ids": ["ev_2"]}
  ],
  "stats": {
    "started_at": "2026-08-26T08:00:00Z",
    "finished_at": "2026-08-26T08:01:00Z",
    "duration_ms": 60000,
    "nodes": 4,
    "edges": 3
  },
  "artifacts": [],
  "warnings": []
}
```

`status` 取值：`queued`（排队中）/ `running`（运行中）/ `succeeded`（成功）/ `partial`（部分成功）/ `failed`（失败）。

#### 3.3.3 GET /api/v1/runs/{run_id}/graph —— 拿图

Query 参数：

| 参数 | 取值 | 默认 | 说明 |
|---|---|---|---|
| format | json / mermaid / dot / svg | json | 输出格式；非 json 返回 text/plain |
| depth | 1-20 | 不限 | 从关注点向外扩展的层数 |
| focus | 节点 id 列表 | 全部 | 只看与这些节点相关的子图 |
| node_types | function,callback,event_source,... | 全部 | 按节点类型过滤 |

JSON 响应为 `graph.schema.json`：`nodes`（函数 / 回调 / 事件源）+ `edges`（调用 / 回调 / 注册 / 实现）+ `evidence`（每条边与节点挂的证据）。

#### 3.3.4 GET /api/v1/runs/{run_id}/artifacts —— 中间产物

返回各阶段产物清单（名称、Schema、sha256、下载 URL），方便协作组拿原始分析数据自行加工。

#### 3.3.5 POST /api/v1/runs/{run_id}/questions —— 自然语言提问

请求：

```json
{"question": "uv_async_send 之后回调在哪个线程执行？", "focus": ["uv_async_send"], "max_paths": 5}
```

响应（`question.schema.json`）：

```json
{
  "run_id": "run_20260826_demo_libuv",
  "question": "uv_async_send 之后回调在哪个线程执行？",
  "answer": "uv_async_send 会向 loop 的唤醒管道写入字节；事件循环线程在 poll 阶段收到事件后执行 uv__async_io，并从队列取出注册的回调逐一调用。",
  "confidence": 0.85,
  "evidence_chain": [
    {"id": "ev_10", "kind": "call_site", "location": {"file": "src/unix/async.c", "line": 1, "snippet": "uv__async_io(loop, w, events);"}, "role": "supports"}
  ],
  "paths": [{"source": "uv_async_send", "target": "async_cb", "edge_ids": ["e10", "e11"]}],
  "disclaimer": "回调触发时机部分为推断，建议结合运行时日志验证。"
}
```

#### 3.3.6 GET /api/v1/schemas/{name} —— 拉取 Schema

其他组可程序化拉取 `schemas/` 下的规范文件做契约校验，例如 `GET /api/v1/schemas/analysis-request`。

### 3.4 统一错误格式

所有非 2xx 响应统一为：

```json
{"error": {"code": "not_found", "message": "run_id 不存在", "details": {}, "run_id": "run_20260826_demo_libuv"}}
```

错误码：`bad_request`、`validation_error`、`unauthorized`、`not_found`、`conflict`、`rate_limited`、`run_failed`、`timeout`、`internal_error`。

### 3.5 异步与回调

分析是异步的：`POST /analyze` 立即返回 `run_id`。完成后调用方可以：

- 轮询 `GET /runs/{run_id}`；或
- 在请求里带 `webhook_url`，服务端在任务完成时向该地址 `POST` 一个 `run-result.schema.json`。

## 4. 对内接口（文件管道，无 Orchestrator）

### 4.1 工作目录约定

```text
workspace/{run_id}/
├── request.json                # 本次分析请求
├── compile_commands.json       # Clang 编译数据库
├── 01-index/symbols.json
├── 02-macro/macros.json
├── 03-callgraph/callgraph.json
├── 04-fptr/fptr-candidates.json
├── 05-async/async-chains.json
├── 06-verify/verification.json
└── 07-report/
    ├── report.md
    ├── graph.json
    ├── graph.mmd
    ├── architecture.json
    ├── key-chains.json
    └── analysis.md
```

### 4.2 阶段接力协议

1. 每个阶段是独立可执行程序，在 `pipeline.json` 中登记命令；
2. 阶段只读上游产物、只写自己的目录，**不修改其他阶段的文件**；
3. 每个产物 JSON 自带信封字段：`schema_version / run_id / stage / status / generated_at / inputs / findings / evidence / artifacts / warnings`（见 `agent-result.schema.json`）；
4. 阶段失败可以输出 `partial` 产物，原因写进 `warnings`；下游是否接受缺失由 `pipeline.json` 的 `optional` 标记决定；
5. 任何两个阶段之间都可以被其他组替换或插入——只要遵守输入输出契约。

### 4.3 阶段契约表

| 阶段 | 输入 | 输出 | 内容 |
|---|---|---|---|
| 01-index | compile_commands.json | symbols.json | 编译单元 + 符号清单（函数 / 变量 / 类型 / 宏 / 回调字段） |
| 02-macro | compile_commands.json, symbols.json | macros.json | 宏展开、条件编译区域、各 profile 激活态 |
| 03-callgraph | symbols.json, macros.json | callgraph.json | 图：节点 = 函数，边 = 调用 / 回调 / 注册 / 实现 |
| 04-fptr | callgraph.json | fptr-candidates.json | 函数指针调用点、赋值点、候选目标 + 概率 |
| 05-async | callgraph.json, fptr-candidates.json | async-chains.json | 事件源 → 注册 → 触发 → 回调 的异步链 |
| 06-verify | 以上全部 | verification.json | 每条链的核查结果、覆盖率、冲突 |
| 07-report | verification.json | report.md / graph.json / graph.mmd / architecture.json / key-chains.json / analysis.md | 报告、模块架构、关键链与自然语言分析（对外呈现） |

### 4.4 pipeline.json（协作组可插拔）

```json
{
  "pipeline_version": "1.0",
  "run_id": "run_20260826_demo_libuv",
  "workspace_root": "workspace/run_20260826_demo_libuv",
  "stages": [
    {"name": "01-index", "order": 1, "command": ["clang-symbol-indexer", "--workspace", "{workspace}"], "inputs": ["compile_commands.json"], "outputs": ["01-index/symbols.json"]}
  ]
}
```

其他组想替换某个分析环节（例如换成自己的宏分析器），只需实现同样的输入 / 输出 JSON 契约，把 `command` 换成自己的可执行文件。

## 5. JSON 统一规范

### 5.1 公共字段

| 字段 | 类型 | 说明 |
|---|---|---|
| schema_version | string | 语义版本 `MAJOR.MINOR`，破坏性变更升 MAJOR |
| run_id | string | 服务端生成，格式 `run_YYYYMMDD_<slug>` |
| task_id | string | 调用方自定义，用于幂等 |
| status | string | queued / running / succeeded / partial / failed |
| generated_at | string | ISO 8601 UTC |
| inputs / artifacts | array | 产物引用（name / schema / sha256 / url） |
| warnings | array | 非致命问题清单 |
| findings | array | 结论（边 / 链 / 候选目标） |
| evidence | array | 证据（见 5.2） |

### 5.2 Evidence（证据）——最重要

每条结论必须至少挂一条 evidence，否则不允许进入报告。字段：

| 字段 | 说明 |
|---|---|
| id | 证据 ID |
| kind | declaration / call_site / assignment / registration / trigger / macro_expansion / conditional_compilation / type_constraint / control_flow / build_flag |
| location | `{file, line, column?, snippet?, ast_id?}`；file 相对仓库根 |
| role | supports（支持）/ refutes（反驳）/ context（上下文） |
| build_profile | 该证据生效的构建配置 |
| macro_stack | 展开时激活的宏栈（复杂宏分析必须） |

### 5.3 置信度语义

- `1.0`：源码直接调用，或编译器确认的唯一目标
- `0.8-0.99`：类型、赋值流与控制流共同确认
- `0.5-0.79`：存在多个候选，但上下文有较强约束
- `<0.5`：启发式推断，只能作为待验证线索
- 函数指针无法唯一解析时输出候选集合，不猜测唯一目标

### 5.4 Graph（节点与边）

节点类型：`function` / `callback` / `event_source` / `build_configuration` / `module` / `external`  
边类型：`direct_call` / `callback_edge` / `registers` / `completes` / `implementation_of` / `data_flow` / `macro_expansion` / `indirect_call` / `external`  
每条边必带：`call_site`（源码位置）、`condition`（宏 / 平台条件）、`execution_context`（线程 / 进程 / 事件循环）、`confidence`、`evidence_ids`。

### 5.5 编码规则

- 文件路径一律相对仓库根，禁止绝对路径
- `snippet_sha256` 用于内容校验与缓存
- 生成代码必须记录生成命令与来源模板（provenance）
- 未知字段：接收方必须忽略（向前兼容）；新增字段不得改变已有字段的语义

## 6. 与其他组联动场景

| 场景 | 本组角色 | 对方角色 | 使用的接口 |
|---|---|---|---|
| A 调用我们的分析能力 | 提供服务 | 调用方 | HTTP API（3.2） |
| B 对方替换 / 新增分析阶段 | 提供契约 | 实现方 | 内部文件管道 + pipeline.json（4.4） |
| C 我们消费对方的数据 | 调用方 | 提供服务 | 对方 API；本组写 adapter 转成我们的 artifact |

对接检查清单：

1. 先通过 `GET /api/v1/schemas/{name}` 或 `schemas/` 目录拿到契约；
2. 用 `task_id` 做幂等，用 `run_id` 做会话标识；
3. 大任务使用 `webhook_url` 接收完成通知，避免长轮询；
4. 所有结论按 `evidence` 追溯；双方结果不一致时，先比对 commit、build_profile 与 `snippet_sha256`。

## 7. Schema 文件清单

| 文件 | 用途 | 谁使用 |
|---|---|---|
| analysis-request.schema.json | 分析请求 | 调用方 |
| run-accepted.schema.json | 提交任务后立即返回 | 服务端 |
| run-result.schema.json | 任务状态与摘要 | 调用方 |
| graph.schema.json | 调用 / 证据图 | 调用方 |
| question.schema.json | 问答请求 / 响应 | 调用方 |
| artifacts.schema.json | 产物清单 | 调用方 |
| common.schema.json | 共享定义（证据 / 错误 / 状态 / 产物） | 全部 |
| agent-result.schema.json | 阶段产物信封 | 内部阶段 |
| pipeline.schema.json | 流水线配置 | 内部 driver |
| symbols / macros / fptr-candidates / async-chains / verification .schema.json | 各阶段产物 | 内部阶段 |

## 8. 变更记录

- 2026-08-26 v1.0：初版定稿；确定 Clang 分析栈；对外 6 个 HTTP 端点；对内 7 阶段文件管道；证据与置信度规范。
