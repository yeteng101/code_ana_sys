# Demo 验证

本 Demo 先用固定的、人工复核过的期望结果验证接口和报告格式；接入真实 AST/编译数据库后，将这些 fixture 替换为分析器 artifact。

## 用例 1：libuv 事件循环

问题：`uv_run` 如何驱动一次 Unix I/O 事件循环？

期望链：

```text
uv_run -> uv__run_pending -> uv__run_prepare -> uv__io_poll
       -> watcher callback -> uv__run_check -> uv__run_closing_handles
```

## 用例 2：Redis 客户端请求

问题：Redis 如何从 socket 事件进入命令执行？

期望链：

```text
aeMain -> aeProcessEvents -> aeApiPoll -> readQueryFromClient
       -> processInputBuffer -> processCommand -> command implementation
```

## 验证规则

1. 每条边必须有源码文件和行号证据。
2. `watcher callback` 和 `readQueryFromClient` 使用 `callback_edge`，不能标为普通直接调用。
3. epoll/kqueue/select 的实现边必须带 build profile 条件。
4. 函数指针无法唯一解析时输出候选集合和低置信度，而不是猜测唯一目标。
5. 同一输入重复运行时，结果中的节点和边排序稳定。

样例请求见 `libuv-request.json`，样例结果见 `libuv-result.json` 与 `redis-result.json`。
