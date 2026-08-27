# Clang 7 阶段流水线 Demo

本目录的 Clang 7 阶段 Demo 不再使用占位 fixture。`demo/sample/` 是一个自包含的 C++ 事件循环样例，`clang_pipeline/` 调用 Clang 的 `-ast-dump=json` 和 `-E -dM` 真正解析源码，按 7 个阶段接力产出 JSON。`libuv-result.json` / `redis-result.json` 仍是旧 HTTP 契约样例，不作为真实分析结论。

## 样例

```text
app_main
  -> loop_init
  -> loop_register(&loop, 0, on_readable)
  -> loop_register(&loop, 1, on_writable)
  -> loop_register(&loop, 2, on_once)
  -> loop_run
       -> wait_for_events
       -> run_ready_watchers
            -> dispatch_once
                 -> Watcher::callback (CALL_WATCHER)
                      -> on_readable / on_writable / on_once
```

`CALL_WATCHER` 是函数式宏；Clang 的 AST 展开记录让调用边挂上 `macro_stack: ["CALL_WATCHER"]`。

## 运行

```bash
cd /Users/andye/Documents/ChatGPT/8.18huawei
python3 -m clang_pipeline.pipeline \
  --source demo/sample \
  --workspace demo/run_clang_demo \
  --run-id run_20260827_clang_demo \
  --publish demo
```

从任何目录运行一键脚本：

```bash
bash /Users/andye/Documents/ChatGPT/8.18huawei/run_demo.sh
```

运行后：

- `demo/run_clang_demo/01-index/symbols.json`：Clang AST 索引
- `demo/run_clang_demo/02-macro/macros.json`：宏定义、展开和条件编译
- `demo/run_clang_demo/03-callgraph/callgraph.json`：带证据的调用图
- `demo/run_clang_demo/04-fptr/fptr-candidates.json`：函数指针候选
- `demo/run_clang_demo/05-async/async-chains.json`：异步回调链
- `demo/run_clang_demo/06-verify/verification.json`：交叉验证
- `demo/run_clang_demo/07-report/`：报告、图、模块架构、关键链、自然语言分析
- `demo/report.md`、`demo/graph.json`、`demo/graph.mmd`、`demo/run-result.json`、`demo/architecture.json`、`demo/key-chains.json`、`demo/analysis.md`：发布的交付物

07-report 现在包含四类逆向分析结论：

- 模块架构：按文件把函数归入 `event_loop` / `app` 组件，并输出组件依赖。
- 关键调用链：从 `app_main` 出发提取到事件循环和回调候选的完整路径。
- 自然语言分析：用证据图生成专家式解释，覆盖架构、关键路径、异步回调、函数指针和宏。
- 调用关系图：Mermaid 按模块分组，直接调用用实线，宏/回调触发用虚线。

HTTP 联调也可以直接命中真实图：`call_chain_demo/examples/clang-request.json` 会以 `repository.name=clang-pipeline-demo` 请求 `POST /api/v1/call-chains`，服务端读取 `demo/graph.json` 返回带证据的调用链。

## 验证

```bash
python3 -m unittest discover -s clang_pipeline/tests -v
python3 -m unittest discover -s call_chain_demo/tests -v
```

每条调用边都带 `evidence`：文件、行号、原始代码片段。函数指针无法唯一解析时输出候选集合和 `0.6` 置信度，不猜测唯一目标。
