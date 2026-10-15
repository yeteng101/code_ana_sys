# libuv / Redis 首轮基准对比

| 项目 | libuv v1.50.0 | Redis 7.2.4 |
|---|---:|---:|
| 调用正/负标注 | 16 / 11 | 110 / 10 |
| 调用 TP / FP / FN | 16 / 0 / 0 | 103 / 0 / 7 |
| 候选 precision | 100% | 100% |
| 候选 recall | 100% | 93.64% |
| 候选 F1 | 100% | 96.71% |
| TP 证据命中率 | 100% | 100% |
| 同步关系标注 | 32 | 22 |
| 同步 recall | 0% | 0% |
| 资源操作标注 | 17 confirmed | 未标注 |
| 资源操作 recall | 64.71% | N/A |

这些是**标注范围内**的结果。libuv 原调用标签与预测图同源，Redis 是本轮独立源码
标注；样本组成不同，不能把上表解释成 libuv 比 Redis 更容易分析或总体准确率差异。
FP=0 仅表示所列负例/identity 未命中误报，其余未标注输出没有完整真值。
Redis 1342 条去重预测位于标注范围之外，未计入 precision。

libuv 资源流已排除 20 个 `pending` 资源候选，只使用 confirmed /
confirmed-with-condition 的 17 条操作作为当前 Gold。历史表中的 62 条不应继续作为
新 baseline 的分母。

重新生成调用图后，libuv 发布图为 894 节点 / 2845 边，Redis 为 745 节点 /
2262 边。当前 06-verify coverage 分别为 libuv 1664/2823=58.94%、Redis
1822/2254=80.83%。这是内部启发式验证覆盖，不是上述 recall；新增 external/builtin
调用边目前仍未全部通过“目标名必须出现在单行 snippet”的验证规则。

## Redis 误差分解

Redis 原生 Makefile 完整构建成功，Bear 捕获 244 条编译记录，8 个选定 translation
units 完成 7 阶段分析。重新生成的发布图包含 55 个 external function 节点，
包括 `pthread_*`、`poll`、`close`、`strerror` 等系统调用。
真实构建及分析运行：
https://github.com/kuangami2/code_ana_sys/actions/runs/35050453666

当前 7 条调用 FN 以 `report.json` 的逐条列表为准，主要两类：

1. 编译器 builtin 替换：`memset`、`sigemptyset`、`sigaddset` 在 AST 中成为
   `__builtin_*` 或宏 helper，预测名称与人工 Gold 名称不同。
2. 宏展开验证拒绝：`serverLog` 展开为 `_serverLog`，Linux 线程命名宏展开为
   `pthread_setname_np`。当前直接调用验证规则检查目标名是否出现在原始单行 snippet，
   宏调用行与目标名不同，可能被标记 refuted。

评测将 refuted 从正向预测排除，故存在图中的宏边也可能形成 FN。
未确认比例 5.54% 是全部去重、非 refuted 候选的比例，不是漏报比例。

Redis 现在有 8 条原生同步预测，但条件、端点和 identity 尚未匹配 22 条人工 Gold；
没有把人工标注当作预测。Redis 资源流有 132 条预测但没有真值，资源指标保持 N/A。

## 原生分析器复核（2026-09-18）

本轮将 `codex/agent-llm-framework` 的 `resource_flow.py` 和 `sync_flow.py`
接入 `export_validation.py --native` 后重新导出并评测：

| 项目 | 原生预测数量 | baseline 结果变化 |
|---|---:|---|
| libuv resource_flow | 237 条 item / 238 条 evidence | 11 TP / 6 FN，227 条 unlabelled predictions |
| libuv sync_relation | 36 条 relation / 67 条 evidence | 仍为 0 TP / 32 FN，36 条 unlabelled predictions |
| Redis resource_flow | 132 条 item / 132 条 evidence | 无真值，保持 N/A |
| Redis sync_relation | 8 条 relation / 15 条 evidence | 仍为 0 TP / 22 FN，8 条 unlabelled predictions |

这说明“分析器已经能输出 JSON”和“分析器输出能直接匹配当前人工 identity”是两件事。
当前阻塞点是资源 resource ID、同步 condition/顺序的 identity 对齐，而不是导出文件缺失。
后续应优先统一 analyzer 的资源/关系命名约定，再由人工复核确认 Ground Truth。

## 资源流身份收口（2026-10-15）

资源流分析器不再使用 API 名称子串匹配。libuv 六个已确认资源族映射到稳定资源 ID，
例如 `uv__getpwuid_r -> rf_libuv_getpwuid_buf_v1`；原始调用表达式保留在
`resource_expression` 中。Redis 增加 `zmalloc/zrealloc/zfree` 和 `sdsnew/sdsfree`
基础分配器配对，同时不再把名字包含 `free/open/close` 的高层函数误当资源操作。

当前 libuv confirmed Gold 上资源流为 11 TP / 6 FN，precision 100%、recall 64.71%。
剩余 FN 是 5 条 transfer 和 async 平台条件位置差异；下一步需要 assignment/return
数据流、平台分支归一化和所有权 transfer。

## 调用图刷新（2026-10-15）

已重新运行 libuv 与 Redis 七阶段流水线，external function 节点分别增加到 216 和
55 个。外部节点的逻辑 symbol 统一为 `fn:<name>`，内部随机 ID 仅保留为图节点 ID，
因此 Redis 调用链 baseline 从 75 TP 恢复到 103 TP，recall 提升到 93.64%。

完整结果在两个 `baseline/report.json` 和 `report.md`；新增标准答案人工复核 pending。
