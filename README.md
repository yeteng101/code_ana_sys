# Code Reverse Agent

面向 libuv / Redis 的代码逆向分析 Agent 设计 Demo。目标是从固定版本源码中提取模块结构、直接调用链、异步回调链、函数指针候选和编译宏差异，并为每条结论保留源码证据与置信度。

## 当前内容

- `docs/source-analysis.md`：libuv / Redis 源码结构和关键调用链基线。
- `docs/architecture.md`：Subagent 分工、执行协议、证据和验收规范。
- `schemas/`：分析请求与 Agent 结果 JSON Schema。
- `demo/`：libuv `uv_run`、Redis 客户端请求链的 Demo fixture 和 Mermaid 报告。
- `Code-Reverse-Agent-汇报.pptx`：面向初学者的汇报 PPT。
- `scripts/build_ppt.js`：技术版 PPT 生成脚本。
- `scripts/build_beginner_ppt.js`：初学者版 PPT 生成脚本。

## Demo

当前 Demo 用人工复核的 fixture 验证接口和报告格式。`demo/*.json` 中的证据行号是占位值，接入固定 commit 的源码索引器后必须替换为精确行号。

```text
libuv: uv_run -> uv__io_poll -> watcher.callback
Redis: aeMain -> aeApiPoll -> readQueryFromClient -> processCommand
```

## 下一步

1. 固定 libuv / Redis commit 和编译配置。
2. 接入 AST/IR、compile database 和宏配置分析。
3. 用真实源码证据替换 fixture，并加入 GitHub Actions 回归验证。

## 许可证

本仓库目前只包含设计文档、Schema、Demo fixture 和生成脚本；分析的第三方源码应在后续下载时遵守其原始许可证并保留版权声明。
