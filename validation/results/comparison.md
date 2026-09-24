# libuv / Redis 首轮基准对比

| 项目 | libuv v1.50.0 | Redis 7.2.4 |
|---|---:|---:|
| 调用正/负标注 | 16 / 11 | 110 / 10 |
| 调用 TP / FP / FN | 16 / 0 / 0 | 75 / 0 / 35 |
| 候选 precision | 100% | 100% |
| 候选 recall | 100% | 68.18% |
| 候选 F1 | 100% | 81.08% |
| TP 证据命中率 | 100% | 100% |
| 同步关系标注 | 32 | 22 |
| 同步 recall | 0% | 0% |
| 资源操作标注 | 62 | 未标注 |
| 资源操作 recall | 0% | N/A |

这些是**标注范围内**的结果。libuv 原调用标签与预测图同源，Redis 是本轮独立源码
标注；样本组成不同，不能把上表解释成 libuv 比 Redis 更容易分析或总体准确率差异。
FP=0 仅表示所列负例/identity 未命中误报，其余未标注输出没有完整真值。
Redis 1276 条去重预测位于标注范围之外，未计入 precision。

libuv 历史 verification coverage 为 1158/1459=79.37%，Redis 本次
06-verify 为 1638/1856=88.25%；二者都是内部启发式验证覆盖，**不是上述 recall**。
报告阶段添加边后，发布图分别为 1481 和 1864 边，分母不同。

## Redis 误差分解

Redis 原生 Makefile 完整构建成功，Bear 捕获 244 条编译记录，8 个选定 translation
units 完成 7 阶段分析。发布图 682 节点 / 1864 边（1773 direct_call / 91 callback_edge）。
真实构建及分析运行：
https://github.com/kuangami2/code_ana_sys/actions/runs/35050453666

35 条 FN 以 `report.json` 的逐条列表为准，主要两类：

1. 系统库调用：pthread_mutex/cond/create/join、poll、close、memset、strerror 等。
   当前 Clang 源码根目录过滤不收集系统头文件声明，随后解析调用目标依赖已索引符号，
   这些外部目标缺失导致边未导出。修复应补外部符号表示，不能从标准答案回灌边。
2. 宏展开验证拒绝：`serverLog` 展开为 `_serverLog`，Linux 线程命名宏展开为
   `pthread_setname_np`。当前直接调用验证规则检查目标名是否出现在原始单行 snippet，
   宏调用行与目标名不同，可能被标记 refuted。标签同时要求调用点和宏定义作为证据。

评测将 refuted 从正向预测排除，故存在图中的宏边也可能形成 FN；
报告 `confirmed_only` 对 Redis 得到相同 75 个 TP，不把拒绝的边算已确认。
图中 373 条重复语义调用合并计数，不能靠重复调用点提高召回率。
未确认比例 5.92% 是全部去重、非 refuted 候选的比例，不是漏报比例。

22 条同步 FN 来自分析器没有原生同步结果输出。没有把调用关系转换成 happens-before，
也没有将人工/AI标注集当作预测。Redis 没有新增资源流真值，资源指标保持 N/A。

## 原生分析器复核（2026-09-18）

本轮将 `codex/agent-llm-framework` 的 `resource_flow.py` 和 `sync_flow.py`
接入 `export_validation.py --native` 后重新导出并评测：

| 项目 | 原生预测数量 | baseline 结果变化 |
|---|---:|---|
| libuv resource_flow | 256 条 item / 348 条 evidence | 仍为 0 TP / 62 FN，257 条 unlabelled predictions |
| libuv sync_relation | 32 条 relation / 61 条 evidence | 仍为 0 TP / 32 FN，32 条 unlabelled predictions |
| Redis resource_flow | 原生提取已运行，但无真值 | N/A |
| Redis sync_relation | 原生提取已运行，但 identity/condition 未匹配 | 仍为 0 TP / 22 FN |

这说明“分析器已经能输出 JSON”和“分析器输出能直接匹配当前人工 identity”是两件事。
当前阻塞点是资源 resource ID、同步 condition/顺序的 identity 对齐，而不是导出文件缺失。
后续应优先统一 analyzer 的资源/关系命名约定，再由人工复核确认 Ground Truth。

完整结果在两个 `baseline/report.json` 和 `report.md`；新增标准答案人工复核 pending。
