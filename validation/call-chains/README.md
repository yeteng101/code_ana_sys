# 调用链正负样本标注 v1

这是调用链验证集的 v1.1 人工标注，目标是先约束“调用链结果”这件事，而不是等所有
分析阶段完成后再补标注。

## 标注口径

一条样本的 `claim` 包含：

```text
source  起点符号 ID
target  终点符号 ID
kind    direct_call / callback_edge / indirect_call
```

标签规则：

| label | 含义 |
|---|---|
| `positive` | 图里存在同 source、target、kind 的边 |
| `negative` | 图里不存在同 source、target、kind 的边 |
| `uncertain` | 需要继续查源码或构建其他 profile 才能确认 |

特别注意：

- `source -> target` 存在，但 `kind` 不对，仍然是 negative。
- 回调字段匹配到多个候选函数时，`resolution=multiple_candidates`，不能被当成唯一目标。
- 只有“同 source、同 target、同 kind”三件事都一致，才算正样本。

## 文件

```text
validation/call-chains/dataset.json
validation/call-chains/README.md
schemas/call-chain-validation.schema.json
```

`dataset.json` 的每个样本包含：

```json
{
  "id": "cc_pos_0001",
  "graph": "demo/libuv/graph.json",
  "claim": {
    "source": "fn:uv_run",
    "target": "fn:uv__io_poll",
    "kind": "direct_call"
  },
  "label": "positive",
  "expected_exists": true,
  "resolution": "unique",
  "candidate_targets": [],
  "evidence": [
    {
      "file": "third_party/libuv/src/unix/core.c",
      "line": 460,
      "snippet": "uv__io_poll(loop, timeout);"
    }
  ],
  "tags": ["libuv", "direct_call"],
  "notes": "uv_run 明确直接调用 uv__io_poll"
}
```

## 样本清单与验证目的

下表覆盖当前全部调用链样本。`说明` 解释该样本专门验证什么，`证据` 是第一条源码证据。

| ID | 断言 | 标签 | 验证目的 | 证据 |
|---|---|---|---|---|
| `cc_pos_sample_001` | `fn:demo::app_main -> fn:demo::loop_run` / `direct_call` | `positive` | app_main 直接调用 loop_run | `demo/sample/app.cpp:29` |
| `cc_pos_sample_002` | `fn:demo::loop_run -> fn:demo::wait_for_events` / `direct_call` | `positive` | 事件循环主循环直接等待事件 | `demo/sample/event_loop.cpp:47` |
| `cc_pos_sample_003` | `fn:demo::loop_run -> fn:demo::run_ready_watchers` / `direct_call` | `positive` | 事件返回后进入 watcher 分发 | `demo/sample/event_loop.cpp:48` |
| `cc_pos_sample_004` | `fn:demo::run_ready_watchers -> fn:demo::dispatch_once` / `direct_call` | `positive` | watcher 就绪后直接调用分发函数 | `demo/sample/event_loop.cpp:26` |
| `cc_pos_sample_005` | `fn:demo::dispatch_once -> cb:Watcher::callback` / `callback_edge` | `positive` | CALL_WATCHER 宏通过结构体字段触发回调，候选目标不唯一 | `demo/sample/event_loop.cpp:19` |
| `cc_pos_sample_006` | `cb:Watcher::callback -> fn:demo::on_readable` / `callback_edge` | `positive` | 注册点证明 on_readable 是候选，但不应声称这是唯一目标 | `demo/sample/app.cpp:26` |
| `cc_pos_libuv_001` | `fn:uv_run -> fn:uv__io_poll` / `direct_call` | `positive` | uv_run 的事件轮询入口 | `third_party/libuv/src/unix/core.c:460` |
| `cc_pos_libuv_002` | `fn:uv_run -> fn:uv__run_timers` / `direct_call` | `positive` | uv_run 的定时器阶段 | `third_party/libuv/src/unix/core.c:442` |
| `cc_pos_libuv_003` | `fn:uv__run_timers -> fn:uv_timer_again` / `direct_call` | `positive` | 重复定时器的重新挂载 | `third_party/libuv/src/timer.c:192` |
| `cc_pos_libuv_004` | `fn:uv__io_poll -> cb:uv__io_s::cb` / `callback_edge` | `positive` | 回调字段 w->cb 的目标集合需要结合赋值流继续收敛 | `third_party/libuv/src/unix/kqueue.c:379` |
| `cc_neg_sample_001` | `fn:demo::dispatch_once -> fn:demo::on_readable` / `direct_call` | `negative` | 真实关系是经过 Watcher::callback 的 callback_edge，不是 direct_call | `demo/sample/event_loop.cpp:19` |
| `cc_neg_sample_002` | `fn:demo::loop_run -> fn:demo::on_once` / `direct_call` | `negative` | loop_run 只负责事件循环，不直接调用 on_once | `demo/sample/app.cpp:28` |
| `cc_neg_libuv_001` | `fn:uv_run -> fn:uv__queue_remove` / `direct_call` | `negative` | uv_run 只能经 uv__run_timers 间接到达 uv__queue_remove | `third_party/libuv/src/timer.c:188` |
| `cc_neg_libuv_002` | `fn:uv__run_timers -> fn:uv__io_poll` / `direct_call` | `negative` | uv__run_timers 不直接调用 uv__io_poll | `third_party/libuv/src/timer.c:192` |
| `cc_neg_libuv_003` | `fn:uv_run -> fn:uv__io_poll` / `callback_edge` | `negative` | source/target 存在，但正确 kind 是 direct_call，不是 callback_edge | `third_party/libuv/src/unix/core.c:460` |
| `cc_neg_sample_003` | `cb:Watcher::callback -> fn:demo::on_once` / `direct_call` | `negative` | 真实注册关系通过 callback_edge 表达，不是 direct_call | `demo/sample/app.cpp:28` |
| `cc_pos_libuv_005` | `fn:uv_run -> fn:uv__loop_alive` / `direct_call` | `positive` | uv_run 在循环开始前检查 loop 是否还活着 | `third_party/libuv/src/unix/core.c:432` |
| `cc_pos_libuv_006` | `fn:uv_run -> fn:uv__update_time` / `direct_call` | `positive` | uv_run 在循环开头更新时间 | `third_party/libuv/src/unix/core.c:434` |
| `cc_pos_libuv_007` | `fn:uv_run -> fn:uv__run_pending` / `direct_call` | `positive` | uv_run 执行 pending 阶段 | `third_party/libuv/src/unix/core.c:450` |
| `cc_pos_libuv_008` | `fn:uv_run -> fn:uv__run_idle` / `direct_call` | `positive` | uv_run 执行 idle 阶段 | `third_party/libuv/src/unix/core.c:451` |
| `cc_pos_libuv_009` | `fn:uv_run -> fn:uv__run_prepare` / `direct_call` | `positive` | uv_run 执行 prepare 阶段 | `third_party/libuv/src/unix/core.c:452` |
| `cc_pos_libuv_010` | `fn:uv_run -> fn:uv__backend_timeout` / `direct_call` | `positive` | uv_run 计算 backend timeout | `third_party/libuv/src/unix/core.c:456` |
| `cc_pos_libuv_011` | `fn:uv_run -> fn:uv__run_check` / `direct_call` | `positive` | uv_run 执行 check 阶段 | `third_party/libuv/src/unix/core.c:474` |
| `cc_pos_libuv_012` | `fn:uv_run -> fn:uv__run_closing_handles` / `direct_call` | `positive` | uv_run 执行 closing handles 阶段 | `third_party/libuv/src/unix/core.c:475` |
| `cc_pos_libuv_013` | `fn:uv_run -> fn:uv__queue_empty` / `direct_call` | `positive` | uv_run 判断 pending queue 是否为空 | `third_party/libuv/src/unix/core.c:447` |
| `cc_pos_libuv_014` | `fn:uv__io_poll -> fn:uv__update_time` / `direct_call` | `positive` | uv__io_poll 在进入 poll 前更新时间 | `third_party/libuv/src/unix/kqueue.c:306` |
| `cc_pos_libuv_015` | `fn:uv__io_poll -> fn:uv__queue_remove` / `direct_call` | `positive` | uv__io_poll 从 watcher queue 移除已注册项 | `third_party/libuv/src/unix/kqueue.c:194` |
| `cc_pos_libuv_016` | `fn:uv__io_poll -> fn:uv__queue_head` / `direct_call` | `positive` | uv__io_poll 读取 watcher queue 头部 | `third_party/libuv/src/unix/kqueue.c:193` |
| `cc_neg_libuv_004` | `fn:uv_run -> fn:uv__run_timers` / `callback_edge` | `negative` | uv_run 到 uv__run_timers 是 direct_call；source/target 相同但 kind 错误，仍为 negative | `third_party/libuv/src/unix/core.c:442` |
| `cc_neg_libuv_005` | `fn:uv_run -> fn:uv__io_poll` / `indirect_call` | `negative` | uv_run 到 uv__io_poll 是直接调用，不是 indirect_call | `third_party/libuv/src/unix/core.c:460` |
| `cc_neg_libuv_006` | `fn:uv_run -> fn:uv__run_prepare` / `callback_edge` | `negative` | uv_run 到 uv__run_prepare 是直接调用，不是 callback_edge | `third_party/libuv/src/unix/core.c:452` |
| `cc_neg_libuv_007` | `fn:uv_run -> fn:uv__kqueue_delete` / `direct_call` | `negative` | uv_run 不直接调用后续 poll 内部的 kqueue 删除逻辑 | `third_party/libuv/src/unix/core.c:460` |
| `cc_neg_libuv_008` | `fn:uv__io_poll -> fn:uv__run_check` / `direct_call` | `negative` | uv__run_check 是 uv_run 的阶段调用，不是 uv__io_poll 的直接调用 | `third_party/libuv/src/unix/core.c:474` |
| `cc_neg_libuv_009` | `fn:uv__io_poll -> fn:uv__run_pending` / `direct_call` | `negative` | uv__run_pending 是 uv_run 的阶段调用，不是 uv__io_poll 的直接调用 | `third_party/libuv/src/unix/core.c:465` |
| `cc_neg_libuv_010` | `fn:uv__update_time -> fn:uv_run` / `direct_call` | `negative` | 方向错误：真实关系是 uv_run -> uv__update_time | `third_party/libuv/src/unix/core.c:434` |
| `cc_neg_libuv_011` | `fn:uv__run_timers -> fn:uv__update_time` / `direct_call` | `negative` | 两者是 uv_run 的不同阶段，不存在 uv__run_timers -> uv__update_time 的直接调用 | `third_party/libuv/src/unix/core.c:478` |

### 新增样本重点

- `cc_pos_libuv_005` 到 `cc_pos_libuv_016`：覆盖 `uv_run` 的主要阶段调用和 `uv__io_poll` 的内部直接调用。
- `cc_neg_libuv_004` 到 `cc_neg_libuv_006`：source/target 真实存在但 edge kind 写错，测试 kind 精确性。
- `cc_neg_libuv_007` 到 `cc_neg_libuv_009`：把跨阶段或深层实现误判成直接调用，测试间接到达不能当直接边。
- `cc_neg_libuv_010` 到 `cc_neg_libuv_011`：方向或阶段关系错误，测试调用链方向必须从源码事实出发。

当前数据集规模：

```text
36 条样本
22 条 positive
14 条 negative
0 条 uncertain
```

## 校验

```bash
python3 scripts/check_call_chain_validation.py \
  --dataset validation/call-chains/dataset.json \
  --graph demo/graph.json \
  --graph demo/libuv/graph.json
```

校验器会检查：

1. 样本 ID 是否唯一；
2. `label` 和 `expected_exists` 是否一致；
3. `positive` 样本的 `source/target/kind` 是否真的存在于图；
4. `negative` 样本是否确实不存在同 kind 的边；
5. 如果源码文件在当前仓库可见，evidence 的文件、行号和原文片段是否匹配。

## 当前覆盖范围

- demo 小样例：直接调用、回调字段、回调候选
- libuv v1.50.0：`uv_run` 主要阶段、`uv__io_poll` 内部调用、定时器链、事件回调字段
- 负样本：错误 kind、把回调注册误判成直接调用、把间接到达误判成直接调用
- 边界样本：错误 kind、反向调用、跨阶段误判、深层实现误判

下一批应扩展到：

- 更多 libuv profile（epoll / kqueue / select）
- 宏展开后的条件边
- 函数指针赋值流
- 跨线程和异步边界
- Redis 的调用链正负样本
