# 三类结果统一评测

四项看板交付：统一评测器 `178904939953773531550094`、libuv baseline
`178904939961425020750097`、Redis 基准 `178904939969235275750100`、
外部 JSON `178904939977269613650103`。认领人：630。

## 运行

```sh
python -m pip install -r validation/sync-relations/requirements.txt
python scripts/prepare_validation_truth.py
python scripts/check_benchmark_sources.py --benchmark validation/benchmarks/libuv
python scripts/check_benchmark_sources.py --benchmark validation/benchmarks/redis
python scripts/evaluate_validation.py --ground-truth validation/benchmarks/libuv/ground-truth.json --predictions validation/results/libuv/predictions --output validation/results/libuv/baseline
python scripts/evaluate_validation.py --ground-truth validation/benchmarks/redis/ground-truth.json --predictions validation/results/redis/predictions --output validation/results/redis/baseline
python -m unittest discover -s validation/tests -v
```

一条 evaluate 命令同时输出 `report.json` 与 `report.md`。
校验源码需检出 `third_party/libuv` 的 v1.50.0 和 `third_party/redis` 的 7.2.4；
checker 验证实际 HEAD、固定源码文件哈希、所有证据行与片段，不存在的源码不能跳过。
`prepare_validation_truth.py` 只读取独立标注，不读取预测图。

## 比较单位及指标

| 类型 | identity（不使用随机 finding ID） | kind |
|---|---|---|
| 调用链 | source symbol、target symbol | direct_call / callback_edge 等 |
| 资源流 | resource ID、函数、文件、行号 | acquire / hold / transfer / release 等 |
| 同步关系 | 两端函数、两端文件/行号、必要条件 | happens_before / concurrent / unknown |

资源流 identity 的 resource ID 是调用方统一的资源标识，不是随机输出 finding ID。
调用链符号使用 `fn:name` 等稳定标识；节点映射可通过 `node.symbol` 提供。
必须使用同一 repository 和 commit；平台差异需要在报告解释，不能把 Linux
同步标签声称为 macOS 运行验证。

- TP：存在的预测与正标注完全相符；FN：正标注未被预测。
- FP：预测命中明确负例，或已标注 identity 上的类型/顺序错误；TN：负命题未被预测。
- precision = TP/(TP+FP)，recall = TP/(TP+FN)，F1 = 2TP/(2TP+FP+FN)。
- 边类型准确率：正标注 identity 上，类型匹配的预测比例；错误类型同时计 FP 与 FN。
- 证据命中率：TP 中**全部**要求的 file/line/snippet 锚点都匹配的比例。
- 覆盖率：正标注 identity 中出现预测的比例，不等同于流水线内部 verification coverage。
- 未确认比例：全部去重、非 refuted 预测中 status 非 confirmed 的比例。
- 语义重复预测合并证据后只计一次，重复数量独立报告。随机 ID 不参与评分。
- 未标注 identity 的预测记录为 unlabelled_predictions，不能假定其正确或错误。
- 分母为零返回 JSON null / Markdown N/A；没有预测时 recall 为 0（若存在正例）。

主指标衡量候选事实检出情况，包含 unconfirmed；`confirmed_only` 另报严格确认指标。
refuted 不作为正向预测。unknown 是应明确表达的不确定关系，并不等于缺少整个输出文件。
输入缺文件、schema 错误、重复标注、缺失/悬空证据或版本不符时失败，不能静默当作空预测。
运行成功只表示评测成功执行，**不代表质量门禁通过**。

## 外部 JSON

```sh
python scripts/export_validation.py --graph demo/libuv/graph.json --native --output validation/results/libuv/predictions
python scripts/export_validation.py --graph demo/libuv/graph.json --reviewed-resources validation/resource-flow/dataset.json --reviewed-sync validation/sync-relations/dataset.json --output validation/results/libuv/reviewed
python scripts/export_validation.py --graph demo/redis/graph.json --verification demo/redis/verification.json --native --output validation/results/redis/predictions
```

每次固定输出 `call-chains.json`、`resource-flow.json`、`sync-relations.json`，
通过已有三类 schema，同时检查每个 finding、edge、operation 的 status、confidence、
非空 evidence_ids 及引用完整性。逐边 status 来自 verification.checks；缺失时 unconfirmed。

`predictions/` 严格保留分析器现状：资源流和同步关系已接入 v1 原生分析器，
通过 `--native` 输出真实 predictions；不能再用 Ground Truth 补齐。
当前 libuv 原生输出为资源流 256 项、同步关系 32 项，但旧 baseline 的 identity/condition
仍可能无法匹配，导致报告中出现 `unlabelled_predictions` 和 Recall=0。这个差异应在
后续 identity 对齐和人工复核中处理，不能把 reviewed 标注直接算作预测。
`reviewed/` 用于人工查看已标注的资源操作、同步关系，明确标记
`origin=reviewed_annotations_not_analyzer_predictions`，**不得拿来发布 baseline 分数**。
不导出 ground_truth.classification 的 leak/race 等最终缺陷结论。
现有标注的 use/retain/borrow 映射为 hold，drop_ref/invalidate 映射为 release，
escape 映射为 transfer；original_kind 保留原始细分语义。未知 owner/thread 用 null。

## 可信度与范围

libuv 旧调用集部分与同一张预测图共同构建，只适合回归，不是独立准确率估计。
Redis 调用标注先从固定源码收集候选，再审查直接调用及宏/函数指针边界；没有根据
分析器输出反向生成正确标签。所有新增标注明确为 AI 源码审查、人工复核 pending。
两项目样本构成不同，指标可展示但不能推导系统在两项目上的普遍性能优劣。

Redis 完整构建采用其原生 Makefile 与 Bear 捕获，避免为不提供 CMake 的版本伪造构建描述。
完整编译数据库另存；七阶段分析覆盖 8 个明确列出的真实 translation units，
不是整个 Redis 的全程序覆盖率。命令见 `scripts/run_redis_validation.sh`。
