# Code Reverse Agent

面向 libuv / Redis 的代码逆向分析 Agent 设计 Demo。目标是从固定版本源码中提取模块结构、直接调用链、异步回调链、函数指针候选和编译宏差异，并为每条结论保留源码证据与置信度。

## 当前内容

- `docs/source-analysis.md`：libuv / Redis 源码结构和关键调用链基线。
- `docs/architecture.md`：Subagent 分工、执行协议、证据和验收规范。
- `docs/interfaces.md`：对外 / 对内接口与 JSON 规范总文档（对接其他组先看这里）。
- `schemas/`：接口与流水线的完整 JSON Schema（分析请求、任务结果、证据图、问答、各阶段产物、pipeline 配置）。
- `demo/`：libuv `uv_run`、Redis 客户端请求链的 Demo fixture、调用图 / 问答 / pipeline 示例。
- `demo/sample/`：自包含的 C++ 事件循环样例，Clang 流水线直接分析这个仓库。
- `demo/libuv/`：libuv v1.50.0 真实分析产物（调用图、模块架构、关键链、自然语言分析）。
- `clang_pipeline/`：7 阶段 Clang 流水线（index → macro → callgraph → fptr → async → verify → report）。
- `scripts/run_libuv.sh`：一键 clone libuv v1.50.0、生成 compile_commands 并运行流水线。

# 代码逆向分析 Agent 接口与 JSON 规范

## 1. 对外 JSON 接口

对外接口只定义 JSON 消息，不绑定具体传输方式。调用方提交一个分析任务，服务端返回任务编号；之后可以查询任务状态、调用关系图、中间产物，并对分析结果进行自然语言提问。

### 1.1 提交分析请求

请求 JSON：

```json
{
  "schema_version": "1.0",
  "task_id": "demo-libuv-loop",
  "repository": {
    "url": "https://github.com/libuv/libuv",
    "commit": "8fb9cb919489a48880680a56efecff6a7dfb4504",
    "language": "c"
  },
  "build_profiles": [
    {
      "name": "macos-clang",
      "defines": ["_GNU_SOURCE"],
      "target": "default"
    }
  ],
  "query": {
    "type": "call_chain",
    "entry_symbols": ["uv_run"],
    "depth": 8,
    "include_async": true,
    "include_function_pointers": true
  }
}
```

响应 JSON：

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "task_id": "demo-libuv-loop",
  "status": "queued"
}
```

### 1.2 查询分析结果

请求只需要任务编号：

```json
{
  "run_id": "run_libuv_1.50.0"
}
```

响应 JSON：

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "task_id": "demo-libuv-loop",
  "status": "partial",
  "summary": "uv_run 驱动事件循环，等待就绪事件并分发回调。",
  "findings": [
    {
      "kind": "direct_call",
      "source": "fn:uv_run",
      "target": "fn:uv__io_poll",
      "confidence": 1.0,
      "evidence_ids": ["ev_a3dcf6ec0abb"]
    }
  ],
  "evidence": [
    {
      "id": "ev_a3dcf6ec0abb",
      "kind": "call_site",
      "location": {
        "file": "third_party/libuv/src/unix/core.c",
        "line": 460,
        "snippet": "uv__io_poll(loop, timeout);"
      }
    }
  ],
  "warnings": []
}
```

### 1.3 获取调用关系图

调用图是完整 JSON 图：

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "nodes": [
    {
      "id": "fn:uv_run",
      "kind": "function",
      "name": "uv_run",
      "file": "third_party/libuv/src/unix/core.c",
      "line": 427
    }
  ],
  "edges": [
    {
      "id": "e_874df4524df0",
      "source": "fn:uv_run",
      "target": "fn:uv__io_poll",
      "kind": "direct_call",
      "call_site": {
        "file": "third_party/libuv/src/unix/core.c",
        "line": 460,
        "snippet": "uv__io_poll(loop, timeout);"
      },
      "confidence": 1.0,
      "evidence_ids": ["ev_a3dcf6ec0abb"]
    }
  ],
  "evidence": []
}
```

### 1.4 自然语言提问

请求 JSON：

```json
{
  "question": "uv_async_send 之后回调在什么时候执行？",
  "focus": ["uv_async_send"],
  "max_paths": 5
}
```

响应 JSON：

```json
{
  "run_id": "run_libuv_1.50.0",
  "question": "uv_async_send 之后回调在什么时候执行？",
  "answer": "uv_async_send 会唤醒事件循环，事件循环线程在 poll 阶段处理后执行注册的回调。",
  "confidence": 0.85,
  "evidence_chain": [
    {
      "id": "ev_10",
      "kind": "call_site",
      "location": {
        "file": "third_party/libuv/src/unix/async.c",
        "line": 170,
        "snippet": "uv__async_io(loop, w, events);"
      }
    }
  ]
}
```

## 2. 对内 JSON 接口

对内接口不使用 HTTP，而是 JSON 文件管道：上一阶段把结果写成 JSON 文件，下一阶段读取。

```text
workspace/{run_id}/
├── compile_commands.json
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


1. **源码索引**

   它读取用户指定的仓库和 `commit`，把代码里所有的函数定义、文件路径、行号信息扫出来，生成一份清单。

2. **编译宏分析**

   它基于上一份清单和编译选项，把代码里所有宏展开的结果和条件编译分支全部提取出来——这对我们处理跨平台代码非常关键。

3. **构建调用图**

   它汇总索引和宏展开的结果，生成一张初步的调用图。图中的边会标注调用的类型，是直接调用、宏展开还是函数指针调用。

4. **处理函数指针**

   它结合调用图和抽象语法树，找出所有函数指针的赋值位置和调用位置，列出每个指针可能指向哪些函数，并给出概率。

5. **处理异步事件**

   它基于前面的调用图和函数指针结果，把“注册回调—事件触发—回调执行”这条完整的异步链串起来。这是我们处理 libuv 这类异步库的核心环节。

6. **验证**

   它汇总前面所有结果，做最终校验，给每条调用链附上证据和置信度，生成最终的验证报告。

| 阶段 | 输入 | 输出 | 内容 |
|---|---|---|---|
| 01-index | compile_commands.json | symbols.json | 函数、字段、类型索引 |
| 02-macro | compile_commands.json | macros.json | 宏定义、展开、条件编译 |
| 03-callgraph | symbols + macros | callgraph.json | 调用图节点和边 |
| 04-fptr | callgraph | fptr-candidates.json | 函数指针候选 |
| 05-async | callgraph + fptr | async-chains.json | 注册、触发、回调链 |
| 06-verify | 以上全部 | verification.json | 证据核查、覆盖率 |
| 07-report | verification | report/graph/analysis | 对外交付物 |



阶段执行顺序由 `pipeline.json` 定义：

```json
{
  "pipeline_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "stages": [
    {
      "name": "01-index",
      "order": 1,
      "command": ["python3", "-m", "clang_pipeline.stage_runner", "01-index", "--workspace", "{workspace}"],
      "inputs": ["compile_commands.json"],
      "outputs": ["01-index/symbols.json"]
    }
  ]
}
```

每个阶段只读自己的输入，只写自己的输出，不修改其他阶段的文件。

## 3. JSON 规范

所有阶段产物都带统一信封：

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "stage": "03-callgraph",
  "status": "succeeded",
  "generated_at": "2026-08-27T08:00:00Z",
  "inputs": [],
  "findings": [],
  "evidence": [],
  "warnings": []
}
```

证据必须能回到源码：

```json
{
  "id": "ev_a3dcf6ec0abb",
  "kind": "call_site",
  "location": {
    "file": "third_party/libuv/src/unix/core.c",
    "line": 460,
    "snippet": "uv__io_poll(loop, timeout);"
  },
  "role": "supports",
  "build_profile": "macos-clang"
}
```

置信度语义：

- `1.0`：源码直接调用，目标唯一。
- `0.8 - 0.99`：类型、赋值流和控制流共同确认。
- `0.5 - 0.79`：存在多个候选，但上下文有较强约束。
- `<0.5`：启发式推断，只能作为待验证线索。


## Agent 工具层设计思路



不要把 7 个阶段直接拆成 7 个大模型工具，而是：

> 7 阶段流水线继续保持内部实现不变，外面包一层大模型能调用的高层工具。

```text
大模型 Agent
   │
   ▼
工具层（Tool Layer）
├── analyze_repo
├── get_call_graph
├── get_key_chains
├── get_architecture
├── get_evidence
└── get_source_snippet
   │
   ▼
现有 7 阶段流水线
   │
   ▼
Evidence Graph
```
Schema 统一放在 `schemas/` 目录：

```text
common.schema.json          共享定义
analysis-request.schema.json 分析请求
run-result.schema.json       任务结果
graph.schema.json            调用关系图
symbols.schema.json          01-index
macros.schema.json           02-macro
fptr-candidates.schema.json  04-fptr
async-chains.schema.json     05-async
verification.schema.json     06-verify
pipeline.schema.json         pipeline 配置
```

总结：对外是 JSON 消息，对内是 JSON 文件接力，所有结论都必须带源码证据。


运行：

```bash
cd /Users/andye/Documents/ChatGPT/8.18huawei
```

```bash
python3 -m clang_pipeline.pipeline \
  --source demo/sample \
  --workspace demo/run_clang_demo \
  --run-id run_20260827_clang_demo \
  --publish demo
```

也可以从任何目录直接跑一键脚本（脚本会自动进入仓库根目录）：

```bash
bash /Users/andye/Documents/ChatGPT/8.18huawei/run_demo.sh
```

跑 libuv：

```bash
bash scripts/run_libuv.sh
```

libuv 产物发布到 `demo/libuv/`：`graph.json`、`report.md`、`architecture.json`、`key-chains.json`、`analysis.md`。

验证：

```bash
python3 -m unittest discover -s clang_pipeline/tests -v
```

交付物：`demo/graph.json`（调用关系图）、`demo/architecture.json`（模块架构）、`demo/key-chains.json`（关键调用链）、`demo/analysis.md`（自然语言分析）、`demo/report.md`（完整报告）。

## 其他电脑直接运行

仓库只依赖 Python 标准库，不需要 `pip install`。换一台电脑运行时，只需要：

1. Python 3.9+：macOS 自带 `/usr/bin/python3`；Linux 可用 `apt install python3`。
2. Clang：macOS 执行 `xcode-select --install`；Ubuntu/Debian 执行 `sudo apt install clang`；Fedora 执行 `sudo dnf install clang`。
3. 克隆并运行：

```bash
git clone https://github.com/yeteng101/code_ana_sys.git
cd code_ana_sys
bash run_demo.sh
```

`run_demo.sh` 会自动检查 `python3` 和 `clang++`，缺少时给出安装提示。Windows 建议使用 WSL 2 或安装 LLVM 后从命令行运行。

接口约定：分析请求见 `schemas/analysis-request.schema.json`，任务状态见 `run-result.schema.json`，调用关系图见 `graph.schema.json`，内部流水线见 `pipeline.schema.json`。

## 下一步

1. libuv v1.50.0 已用 CMake 生成真实 compile_commands 并跑通流水线；下一步固定 Redis 编译数据库。
2. 用 `clang_pipeline/stage_runner.py` 的同一契约替换各阶段实现，加入 GitHub Actions 回归验证。
3. `demo/graph.json` 已接入 `call_chain_demo`（`repository.name=clang-pipeline-demo`）；下一步把 libuv / Redis fixture 也替换为真实 compile_commands 产物。

## 许可证

本仓库目前只包含设计文档、Schema、Demo fixture 和生成脚本；分析的第三方源码应在后续下载时遵守其原始许可证并保留版权声明。
