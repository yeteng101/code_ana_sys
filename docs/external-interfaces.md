# 代码逆向分析：两种外部接口用法

本文面向调用方，不描述内部实现细节。外部调用只有两种推荐方式：

1. **Claude Code CLI 自然语言接口**
2. **固定 JSON 文件接口**

JSON 文件接口固定提供三类结果：

- 调用链结果：`call-chains.json`
- 资源流结果：`resource-flow.json`
- 同步关系结果：`sync-relations.json`

## 一、Claude Code CLI 自然语言接口

### 1. 直接分析一个新仓库

问题中直接写仓库路径：

```bash
cd /Users/andye/Documents/ChatGPT/8.18huawei

python3 -m clang_pipeline.cli ask \
  --question "请分析仓库 /path/to/repo，uv_run 调用了谁？" \
  --backend claude-code
```

系统会依次执行：

```text
识别问题中的仓库路径
→ 查找 compile_commands.json
→ 运行 Clang 七阶段流水线
→ 生成 Agent 上下文
→ 调用 Claude Code CLI
→ 输出 JSON
```

输出示例：

```json
{
  "run_id": "run_libuv_20260910_120000",
  "question": "请分析仓库 /path/to/repo，uv_run 调用了谁？",
  "answer": "uv_run 调用 uv__io_poll ...",
  "confidence": 0.9,
  "evidence_chain": [
    {
      "id": "ev_xxx",
      "kind": "call_site",
      "location": {
        "file": "src/unix/core.c",
        "line": 460,
        "snippet": "uv__io_poll(loop, timeout);"
      }
    }
  ],
  "tool_calls": [
    {
      "tool": "claude-code",
      "status": "ok"
    }
  ],
  "status": "succeeded",
  "backend": "claude-code"
}
```

### 2. 只查询已有分析产物

```bash
python3 -m clang_pipeline.cli ask \
  --question "uv_run 调用了谁？" \
  --workspace demo/libuv \
  --no-auto-analyze \
  --backend claude-code
```

### 3. 通过 MCP 调用工具

如果希望 Claude Code 自己调用分析工具，而不是由 Python 外层驱动，可以先注册我们的 MCP：

```bash
claude mcp add code-reverse-agent \
  -s user \
  -e CRA_WORKSPACE=/Users/andye/Documents/ChatGPT/8.18huawei/demo/libuv \
  -e CRA_REPO_ROOT=/Users/andye/Documents/ChatGPT/8.18huawei \
  -e PYTHONPATH=/Users/andye/Documents/ChatGPT/8.18huawei \
  -- python3 -m clang_pipeline.mcp_server
```

然后在 Claude Code 中直接说：

```text
使用 code-reverse-agent 的 get_key_chains，列出 uv_run 的关键调用链
```

## 二、固定 JSON 文件接口

推荐每个 workspace 下固定生成：

```text
workspace/<run_id>/external/
├── call-chains.json
├── resource-flow.json
└── sync-relations.json
```

三个文件使用统一信封：

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "result_type": "call_chain",
  "status": "partial",
  "generated_at": "2026-09-10T12:00:00Z",
  "source": {
    "repository": "libuv/libuv",
    "commit": "8fb9cb919489a48880680a56efecff6a7dfb4504",
    "build_profile": "libuv-macos-clang"
  },
  "items": [],
  "evidence": [],
  "warnings": []
}
```

### 1. 调用链结果 `call-chains.json`

用途：回答“谁调用谁”“入口到目标怎么走”。

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "result_type": "call_chain",
  "status": "succeeded",
  "items": [
    {
      "id": "chain_uv_run_001",
      "entry": "uv_run",
      "direction": "caller_to_callee",
      "nodes": [
        {"id": "fn:uv_run", "name": "uv_run", "kind": "function"},
        {"id": "fn:uv__io_poll", "name": "uv__io_poll", "kind": "function"}
      ],
      "edges": [
        {
          "source": "fn:uv_run",
          "target": "fn:uv__io_poll",
          "kind": "direct_call",
          "confidence": 0.99,
          "evidence_ids": ["ev_xxx"]
        }
      ],
      "confidence": 0.99,
      "evidence_ids": ["ev_xxx"]
    }
  ],
  "evidence": [],
  "warnings": []
}
```

当前对应实现：

```text
07-report/key-chains.json
07-report/graph.json
schemas/call-chains.schema.json
```

### 2. 资源流结果 `resource-flow.json`

用途：描述资源从获取、持有、转移到释放的路径。这里的资源包括文件描述符、
内存、锁、连接、句柄和引用计数。

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "result_type": "resource_flow",
  "status": "partial",
  "items": [
    {
      "id": "flow_fd_001",
      "resource": "fd:listener",
      "resource_type": "file_descriptor",
      "operations": [
        {
          "kind": "acquire",
          "file": "src/unix/tcp.c",
          "line": 123,
          "snippet": "int fd = uv__socket(...);",
          "evidence_ids": ["ev_xxx"]
        },
        {
          "kind": "release",
          "file": "src/unix/tcp.c",
          "line": 456,
          "snippet": "uv__close(fd);",
          "evidence_ids": ["ev_yyy"]
        }
      ],
      "owner": "uv_tcp_t",
      "thread": "event_loop",
      "confidence": 0.82,
      "evidence_ids": ["ev_xxx", "ev_yyy"]
    }
  ],
  "evidence": [],
  "warnings": []
}
```

允许的操作类型：

```text
acquire
hold
transfer
wait
release
leak_suspected
use_after_release_suspected
```

对应 schema：

```text
schemas/resource-flow.schema.json
```

> 资源流分析阶段目前还没有接入 Clang 流水线；本文件先固定输出契约，
> 后续用验证集确认规则和标注口径。

### 3. 同步关系结果 `sync-relations.json`

用途：描述线程、事件循环、锁、原子操作和等待/通知之间的顺序关系。

```json
{
  "schema_version": "1.0",
  "run_id": "run_libuv_1.50.0",
  "result_type": "sync_relation",
  "status": "partial",
  "items": [
    {
      "id": "sync_001",
      "relation_type": "mutex_lock",
      "source": {
        "file": "src/unix/thread.c",
        "line": 100,
        "symbol": "uv_mutex_lock"
      },
      "target": {
        "file": "src/unix/thread.c",
        "line": 140,
        "symbol": "uv_mutex_unlock"
      },
      "order": "happens_before",
      "execution_context": {
        "process": "uv",
        "thread": "worker",
        "event_loop": null
      },
      "confidence": 0.8,
      "evidence_ids": ["ev_zzz"]
    }
  ],
  "evidence": [],
  "warnings": []
}
```

允许的关系类型：

```text
mutex_lock
rwlock
atomic
barrier
condition_variable
event_wait
event_notify
thread_join
happens_before
```

对应 schema：

```text
schemas/sync-relations.schema.json
```

> 同步关系分析阶段目前同样没有接入流水线；先固定契约，再由验证集确定
> 哪些同步原语必须识别、哪些只要求候选关系。

## 三、接口选型

| 场景 | 推荐接口 |
|---|---|
| 人直接提问、临时分析 | Claude Code CLI 自然语言 |
| 网页、脚本、CI、第三方系统 | 三个 JSON 文件 |
| Claude Code 自主选择工具 | MCP |
| 结果做回归或证据审核 | JSON 文件 + evidence |

推荐组合：

```text
人提问 → Claude Code CLI
系统集成 → call-chains.json / resource-flow.json / sync-relations.json
质量验证 → evidence_ids + validation dataset
```

## 四、下一步：验证集

验证集不按“结果文件有多少”计数，而按下面三类标注：

1. 调用链：每条边是否为真、方向是否正确、是否遗漏关键边。
2. 资源流：资源获取/转移/释放是否配对，是否存在泄漏或提前释放。
3. 同步关系：锁、原子操作、等待/通知和 happens-before 是否正确。

验证集任务已经布置到 Kanb 看板，优先从 libuv v1.50.0 的真实产物开始。
