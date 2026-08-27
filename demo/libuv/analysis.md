# 自然语言分析

## 模块架构
仓库由 core、include、src、unix、uv 组成。入口负责初始化运行时、注册回调并驱动主循环；事件循环组件负责等待就绪事件、遍历句柄并分发回调。

## 关键调用链
入口 `uv_run` 的关键路径是：`uv_run -> uv__io_poll`。

## 异步回调链
fd_ready 事件在 third_party/libuv/src/heap-inl.h:222 触发回调，但候选为空，需要进一步分析。

## 函数指针
静态分析发现回调字段存在多个候选：`uv__async_io、uv__cancelled、uv__fs_done、uv__fs_event、uv__fs_work、uv__getaddrinfo_done、uv__getaddrinfo_work、uv__getnameinfo_done、uv__getnameinfo_work、uv__poll_io、uv__queue_done、uv__queue_work、uv__random_done、uv__random_work、uv__server_io、uv__signal_event、uv__stream_io、uv__udp_io`，无法唯一确定目标，置信度为 0.30。

## 复杂宏
本次分析覆盖：ACCESS_ONCE (third_party/libuv/test/benchmark-async-pummel.c:29)、ARRAY_END (third_party/libuv/src/uv-common.h:55)、ARRAY_SIZE (third_party/libuv/src/uv-common.h:54)、EV_OOBAND (third_party/libuv/src/unix/kqueue.c:48)、F_OK (third_party/libuv/include/uv/win.h:659)、INIT (third_party/libuv/src/unix/fs.c:90)、UV_EXTERN (third_party/libuv/include/uv.h:39)。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。

## 结论
验证覆盖率为 79%，报告状态为 not ready；所有结论均引用源码文件、行号和原始代码片段。
