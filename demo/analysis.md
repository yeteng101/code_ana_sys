# 自然语言分析

## 模块架构
样例由 app (应用回调)、event_loop (事件循环) 组成。应用入口负责初始化事件循环、注册回调并启动轮询；事件循环组件负责等待就绪事件、遍历 watcher 并分发回调。

## 关键调用链
入口 `app_main` 的关键路径是：`app_main -> loop_run -> run_ready_watchers -> dispatch_once -> Watcher::callback -> on_readable`。

## 异步回调链
fd_ready 事件在 demo/sample/event_loop.cpp:19 触发回调，候选为 on_once、on_readable、on_writable

## 函数指针
静态分析发现回调字段存在多个候选：`on_once、on_readable、on_writable`，无法唯一确定目标，置信度为 0.60。

## 复杂宏
本次分析覆盖：CALL_WATCHER (demo/sample/event_loop.cpp:3)、LOOP_BACKEND (demo/sample/event_loop.h:9)。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。

## 结论
验证覆盖率为 100%，报告状态为 ready；所有结论均引用源码文件、行号和原始代码片段。
