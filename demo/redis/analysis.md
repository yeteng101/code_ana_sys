# 自然语言分析

## 模块架构
仓库由 core、src 组成。入口负责初始化运行时、注册回调并驱动主循环；事件循环组件负责等待就绪事件、遍历句柄并分发回调。

## 关键调用链
入口 `aeProcessEvents` 的关键路径是：`aeProcessEvents -> aeFileEvent::wfileProc`。

## 异步回调链
fd_ready 事件在 third_party/redis/src/connection.h:243 触发回调，但候选为空，需要进一步分析。

## 函数指针
静态分析发现回调字段存在多个候选：`dupClientReplyValue、freeClientReplyValue、lazyFreeFunctionsCtx、lazyFreeLuaScripts、lazyFreeReplicationBacklogRefMem、lazyFreeTrackingTable、lazyfreeFreeDatabase、lazyfreeFreeObject`，无法唯一确定目标，置信度为 0.30。

## 复杂宏
本次分析覆盖：ACL_DENIED_AUTH (third_party/redis/src/server.h:2891)、ACL_DENIED_CHANNEL (third_party/redis/src/server.h:2892)、ACL_DENIED_CMD (third_party/redis/src/server.h:2889)、ACL_DENIED_KEY (third_party/redis/src/server.h:2890)、ACL_LOG_CTX_LUA (third_party/redis/src/server.h:2896)。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。

## 结论
验证覆盖率为 88%，报告状态为 not ready；所有结论均引用源码文件、行号和原始代码片段。
