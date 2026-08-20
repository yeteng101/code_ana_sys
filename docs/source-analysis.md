# libuv / Redis 源码结构剖析

本文是逆向分析 Agent 的事实基线。分析必须记录仓库 URL、commit、编译器、编译参数和目标平台；没有这些信息的结论只能标为 `unreproducible`。

## 1. libuv（1.x）

### 1.1 目录与职责

| 区域 | 典型路径 | 责任 |
|---|---|---|
| 公共 API | `include/uv.h`, `include/uv/unix.h`, `include/uv/win.h` | 类型、句柄、请求、回调签名和 ABI |
| 公共实现 | `src/uv-common.c`, `src/uv-data-getter-setters.c` | 平台无关的句柄/请求辅助逻辑 |
| Unix 核心 | `src/unix/core.c`, `src/unix/loop.c` | loop 生命周期、阶段调度、时间和 pending 队列 |
| Unix I/O | `src/unix/poll.c`, `src/unix/linux-core.c`, `src/unix/proctitle.c` | watcher、poll backend 和 Unix 细节 |
| Unix 子系统 | `src/unix/async.c`, `fs.c`, `process.c`, `signal.c`, `stream.c`, `tcp.c`, `udp.c` | 各类 handle/request 的实现 |
| Windows | `src/win/*` | IOCP、Windows handle、进程和网络实现 |
| 构建/生成 | `CMakeLists.txt`, `configure.ac`, `src/*.h.in` | 平台探测、宏和生成头文件 |
| 测试 | `test/`, `test/benchmark/` | 行为、生命周期和平台差异的可执行证据 |

### 1.2 主事件循环调用链

典型 Unix 配置下，入口链为：

```text
uv_run
  -> uv__run_pending
  -> uv__run_idle
  -> uv__run_prepare
  -> uv__io_poll
       -> backend poll（epoll/kqueue/event ports）
       -> watcher.callback
  -> uv__run_check
  -> uv__run_closing_handles
```

`uv_run` 的循环条件由 active handles、active requests、stop flag 和 loop mode 共同决定。`uv__io_poll` 不是最终业务回调；它把就绪事件映射回 `uv__io_t` 的 watcher，再由具体 handle 的 read/write/connect 回调推进状态机。

### 1.3 Handle/Request 生命周期

```text
uv_*_init -> uv_*_start -> uv__io_start/queue_work
           -> poll 或 worker 完成
           -> 用户 callback
           -> uv_*_stop / uv_cancel
           -> uv_close -> close callback
```

必须分别建模：

- handle 的引用计数和 `uv_ref`/`uv_unref` 对 loop 可运行性的影响；
- request 在提交、完成、取消和释放之间的状态；
- threadpool 完成后如何通过 async/idle/pending 队列回到 loop 线程；
- `uv_close` 的延迟关闭语义，不能把调用点误认为 close callback。

### 1.4 难点与分析规则

- **回调表**：`uv_stream_t`、`uv_fs_t` 等结构中保存 callback，需记录声明、赋值、触发三个位置。
- **函数指针**：先按完整函数类型过滤，再用赋值流、对象类型、注册 API 和控制流缩小候选；无法确定时输出候选集合。
- **异步边**：注册点到执行点使用 `callback_edge`，并附带事件源、线程和队列信息，不能伪装成普通 `call`。
- **平台宏**：Unix/Windows 使用不同实现；`UV__*` 和 configure 生成宏必须作为配置维度进入图索引。
- **生成代码**：分析输入同时保留原始模板和生成文件，并记录生成命令。

## 2. Redis（7.x）

### 2.1 目录与职责

| 区域 | 典型路径 | 责任 |
|---|---|---|
| 服务器核心 | `src/server.c`, `src/server.h` | 初始化、配置、周期任务、主循环 |
| 事件抽象 | `src/ae.c`, `src/ae.h`, `src/ae_epoll.c`, `src/ae_kqueue.c`, `src/ae_select.c` | file/time events 与平台 backend |
| 网络与协议 | `src/networking.c`, `src/connection.c`, `src/connhelpers.c` | socket、读写回调、RESP 解析、客户端状态 |
| 命令与数据 | `src/commands.c`, `src/commands/*.json`, `src/object.c`, `src/t_*.c` | 命令表生成、对象和数据结构实现 |
| 持久化/复制 | `src/rdb.c`, `src/aof.c`, `src/replication.c` | RDB、AOF、复制状态机 |
| 后台任务 | `src/bio.c` 及固定 commit 中的相关后台任务文件 | 后台 I/O 和异步任务 |
| 模块与扩展 | `src/module.c`, `src/module*.c` | Module API、模块命令和回调 |
| 集群/哨兵 | `src/cluster.c`, `src/sentinel.c` | 分布式状态和网络事件 |
| 构建/生成/测试 | `Makefile`, `src/Makefile`, `utils/`, `tests/` | 命令表生成、平台探测、集成测试 |

路径名必须以固定 commit 的实际文件清单为准；表中的 `bio_*` 仅表示需要在索引阶段解析的后台任务相关文件，不应由 Agent 猜测文件名。

### 2.2 客户端请求主链

```text
aeMain
  -> aeProcessEvents
  -> aeApiPoll（epoll/kqueue/select）
  -> readQueryFromClient
  -> processInputBuffer
  -> processCommand
  -> command implementation
  -> addReply / prepareClientToWrite
  -> sendReplyToClient
```

连接建立链通常为：

```text
acceptTcpHandler
  -> connCreateAcceptedSocket
  -> connectionAccept
  -> createClient
  -> aeCreateFileEvent(readQueryFromClient)
```

### 2.3 Redis 特有难点

- 命令表可能由 `src/commands/*.json` 生成，必须把生成输入和生成输出建立 provenance。
- file event、time event、客户端状态机和后台线程同时存在，异步图需要区分事件循环线程与 BIO/IO 线程。
- Module API 引入外部函数指针和用户代码，边界外目标标记为 `external_module`。
- epoll/kqueue/select 是互斥配置；同一逻辑事件应通过 `implementation_of` 边连接到平台实现。
- fork、持久化和复制路径会产生跨进程或状态机边，不能只依赖单一静态调用图。

## 3. 统一事实模型

分析结果分为四类节点：`function`、`callback`、`event_source`、`build_configuration`；边分为 `direct_call`、`callback_edge`、`registers`、`completes`、`implementation_of`、`data_flow` 和 `external`。

每条边必须包含源码位置、配置条件、推导方法和置信度。自然语言报告、Mermaid 图和 JSON 查询结果都只能从这个 Evidence Graph 派生。
