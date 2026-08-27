# Code Reverse Agent

面向 libuv / Redis 的代码逆向分析 Agent 设计 Demo。目标是从固定版本源码中提取模块结构、直接调用链、异步回调链、函数指针候选和编译宏差异，并为每条结论保留源码证据与置信度。

## 当前内容

- `docs/source-analysis.md`：libuv / Redis 源码结构和关键调用链基线。
- `docs/architecture.md`：Subagent 分工、执行协议、证据和验收规范。
- `docs/interfaces.md`：对外 / 对内接口与 JSON 规范总文档（对接其他组先看这里）。
- `schemas/`：接口与流水线的完整 JSON Schema（分析请求、任务结果、证据图、问答、各阶段产物、pipeline 配置）。
- `demo/`：libuv `uv_run`、Redis 客户端请求链的 Demo fixture、调用图 / 问答 / pipeline 示例。
- `demo/sample/`：自包含的 C++ 事件循环样例，Clang 流水线直接分析这个仓库。
- `clang_pipeline/`：7 阶段 Clang 流水线（index → macro → callgraph → fptr → async → verify → report）。
- `Code-Reverse-Agent-汇报.pptx`：面向初学者的汇报 PPT。
- `scripts/build_ppt.js`：技术版 PPT 生成脚本。
- `scripts/build_beginner_ppt.js`：初学者版 PPT 生成脚本。

## Demo

当前 Demo 用 Clang 真正解析 `demo/sample/` 里的 C++ 代码，跑完 7 个流水线阶段，产出模块架构、关键调用链、自然语言分析、带源码证据的调用图、函数指针候选、异步回调和验证报告。生成的产物在 `demo/run_clang_demo/`，报告与图同步发布到 `demo/`。

```text
app_main -> loop_run -> wait_for_events
app_main -> loop_register  (callback registration)
dispatch_once --CALL_WATCHER--> Watcher::callback -> on_readable / on_writable / on_once
```

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

1. 把 `compile_commands.json` 从 demo 样例换成固定 commit 的 libuv / Redis 编译数据库。
2. 用 `clang_pipeline/stage_runner.py` 的同一契约替换各阶段实现，加入 GitHub Actions 回归验证。
3. `demo/graph.json` 已接入 `call_chain_demo`（`repository.name=clang-pipeline-demo`）；下一步把 libuv / Redis fixture 也替换为真实 compile_commands 产物。

## 许可证

本仓库目前只包含设计文档、Schema、Demo fixture 和生成脚本；分析的第三方源码应在后续下载时遵守其原始许可证并保留版权声明。
