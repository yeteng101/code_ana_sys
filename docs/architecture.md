# 代码逆向 Agent：架构与规范（v2 · 无 Orchestrator）

版本：2.0（2026-08-26）  
本文与 [interfaces.md](./interfaces.md) 和 `schemas/` 目录保持一致，是架构的唯一事实来源。

## 1. 设计目标

系统输入一个固定 commit 的 C/C++ 仓库（libuv / Redis）和构建配置，用 Clang 解析源码，输出可复核的模块图、调用链、异步回调链、函数指针候选、宏差异和自然语言解释。

设计约束：可复现、可增量、可审计、允许不确定性、跨平台配置隔离、**没有 Orchestrator 统一管理**。

## 2. 总体架构

```text
外部调用方 / 协作组
        │  HTTP /api/v1（JSON，见 interfaces.md §3）
        ▼
┌───────────────────────────────────────┐
│ 接口层  6 个 HTTP 端点                  │
├───────────────────────────────────────┤
│ 驱动层  pipeline driver               │
│         读 pipeline.json，按 order 启动 │
├───────────────────────────────────────┤
│ 分析层  7 个阶段，JSON 文件接力          │
│ 01-index → 02-macro → 03-callgraph    │
│   → 04-fptr → 05-async → 06-verify    │
│   → 07-report                         │
└───────────────────────────────────────┘
```

三层职责：

| 层 | 职责 | 关键文件 |
|---|---|---|
| 接口层 | 接单（analyze）、交付（status / graph / artifacts / questions） | interfaces.md §3 |
| 驱动层 | 按 `pipeline.json` 顺序执行命令、检查产物；**不做调度决策** | `pipeline.schema.json` |
| 分析层 | 7 个独立阶段，各自读 JSON、写 JSON | `schemas/*` 阶段产物 |

没有 Orchestrator 的含义：不存在一个中央 Agent 来分配任务、合并结果、决定优先级。阶段之间靠**文件契约**衔接，靠 `pipeline.json` 登记顺序，靠 pipeline driver 顺序执行。

## 3. 分析层：7 个阶段

每个阶段是独立可执行程序，工作目录布局见 interfaces.md §4.1。产物信封统一为 `agent-result.schema.json`。

| 阶段 | Clang 能力 | 输入 | 输出 | 内容 | Schema |
|---|---|---|---|---|---|
| 01-index | RecursiveASTVisitor | compile_commands.json | symbols.json | 编译单元 + 符号（函数/变量/类型/宏/回调字段）清单 | symbols.schema.json |
| 02-macro | PPCallbacks | compile_commands.json, symbols.json | macros.json | 宏定义/展开、条件编译区域、各 profile 激活态 | macros.schema.json |
| 03-callgraph | ASTMatcher（CallExpr） | symbols.json, macros.json | callgraph.json | 图：节点 = 函数/回调/事件源，边 = 调用/回调/注册/实现 | graph.schema.json |
| 04-fptr | AST + 类型约束 + 赋值流（疑难可加 SVF） | callgraph.json | fptr-candidates.json | 函数指针调用点、赋值点、候选目标 + 概率 | fptr-candidates.schema.json |
| 05-async | 注册点 / 事件源 / 回调字段匹配 | callgraph.json, fptr-candidates.json | async-chains.json | 事件源 → 注册 → 触发 → 回调的异步链 | async-chains.schema.json |
| 06-verify | 源码重查 + 交叉验证 | 以上全部 | verification.json | 每条链核查结果、覆盖率、冲突 | verification.schema.json |
| 07-report | 报告 / 图生成（可接 LLM 解释） | verification.json | report.md / graph.json / graph.mmd / architecture.json / key-chains.json / analysis.md | 对外交付物 | — |

合成（模块图、关键路径）与自然语言解释不再设独立 Agent，合并进 07-report：**模型只解释 Evidence Graph 里已有的东西，不许编造源码事实**。

## 4. 执行协议（无 Orchestrator 版本）

1. 请求进入接口层 → 创建 `run_id`，锁定 commit 与 build profile，生成 `request.json` 与 `compile_commands.json`。
2. pipeline driver 读 `pipeline.json`，按 `order` 顺序执行各阶段命令。
3. 每个阶段只读 `inputs` 列出的产物、只写 `outputs` 对应目录，**不修改其他阶段的文件**。
4. 阶段失败可输出 `partial` 产物，原因写进 `warnings`；`optional: true` 的阶段失败时下游可继续。
5. 任何阶段都可以被协作组替换或插入，只要输入输出 JSON 契约一致（见 interfaces.md §4.4）。
6. 06-verify 通过（覆盖率达标、无未解决冲突）后，才允许 07-report 生成报告和图。
7. 产物用 `sha256` 校验；内容哈希寻址（如 `graph://call-chain/<sha256>`），相同输入可复用缓存。

## 5. 证据与置信度规范

所有结论必须挂 Evidence Graph：一条 finding 通过 `evidence_ids` 引用 evidence，evidence 必须含 `file`、`line` 等源码锚点（字段定义见 `common.schema.json`）。

置信度语义：

- `1.0`：源码直接调用或编译器确认的唯一目标。
- `0.8-0.99`：类型、赋值流和控制流共同确认。
- `0.5-0.79`：存在多个候选，但上下文提供了较强约束。
- `<0.5`：启发式推断，只能作为待验证线索。

跨宏配置的边必须带 `condition`，跨线程/进程的边必须带 `execution_context`，函数指针无法唯一解析时输出候选集合而不是猜测唯一目标。

## 6. 安全与工程规范

- 源码解析在隔离工作目录中进行；构建命令默认禁止网络和任意写入。
- 单个阶段有超时、节点数和输出大小上限。
- 失败允许返回部分 artifact，并在 `warnings` 中列出缺失原因。
- Schema 使用语义版本号；新增字段向后兼容，删除或改义必须升主版本。
- 不把模型生成的解释当作事实；事实必须来自 Evidence Graph。

## 7. 验证门禁

- 关键入口链覆盖率 >= 90%。
- 回调注册到执行的映射准确率目标 >= 85%。
- 函数指针候选召回率目标 >= 80%。
- 100% 的报告结论有源码证据。
- 同一 commit、同一 profile 的结果哈希稳定。

## 8. 文档与 Schema 索引

- `docs/interfaces.md`：对外 6 个 HTTP 端点、对内文件管道、JSON 统一规范、协作组联动方式。
- `schemas/common.schema.json`：共享定义（schema_version、run_id、source_location、evidence、finding、error、artifact_ref）。
- 对外 API：`analysis-request`、`run-accepted`、`run-result`、`graph`、`question`、`artifacts`。
- 对内流水线：`pipeline`、`agent-result`、`symbols`、`macros`、`fptr-candidates`、`async-chains`、`verification`。

## 9. 与 v1 的差异

| 项 | v1（旧） | v2（当前） |
|---|---|---|
| 调度 | Orchestrator 统一管理 | pipeline driver + `pipeline.json` 顺序执行 |
| 内部通信 | 编排消息 | JSON 文件管道（上一阶段写、下一阶段读） |
| Agent 划分 | 8 个 Agent（含独立 Synthesizer / NL Analyst） | 7 个阶段，合成与解释合并进 07-report |
| 证据模型 | 描述性规范 | `common.schema.json` 机器可校验字段 |
| 图与产物 | `graph://` 抽象引用 | 完整 Graph JSON + sha256 校验 |
