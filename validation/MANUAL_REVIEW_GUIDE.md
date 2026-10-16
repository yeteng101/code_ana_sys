# 验证集人工复核指南

## 1. 复核对象

验证集原始标注位于：

```text
validation/call-chains/dataset.json
validation/resource-flow/dataset.json
validation/sync-relations/dataset.json
validation/redis/call-chains.json
validation/redis/sync-relations.json
```

统一 Excel 复核表：

```text
validation/人工复核表-2026-10-16.xlsx
```

新仓库使用通用 CSV 复核表，不走上面的历史 Excel：

```text
validation/datasets/<project-id>/review-table.csv
```

新仓库初始化、候选收集、复核结论转 Gold 的完整命令见：

```text
docs/validation-project-workflow.md
```

2026-10-16 的 Codex 模拟复核结果见：

```text
validation/reviews/simulated-review-2026-10-16.json
validation/人工复核表-2026-10-16-simulated.xlsx
```

模拟复核只做 evidence 源码检查加分类规则，不冒充人工确认；
原始 `human_review` 仍保持 `pending`。

自动生成的 benchmark 文件不要直接人工修改：

```text
validation/benchmarks/libuv/ground-truth.json
validation/benchmarks/redis/ground-truth.json
```

## 2. 复核状态含义

| 状态 | 含义 |
|---|---|
| Pending | 尚未人工确认 |
| Pending candidate | 自动生成候选，尚未确认 |
| Confirmed | 人工确认正确 |
| Confirmed with condition | 在给定条件下成立 |
| Rejected | 人工确认错误 |
| Needs fix | 需要修改证据或标签 |

## 3. 复核顺序

建议优先级：

```text
1. 同步关系
2. 资源流
3. 调用链
```

原因：同步关系语义最复杂，当前 recall 最低。

## 4. 调用链复核

打开：

```bash
code validation/call-chains/dataset.json
code validation/redis/call-chains.json
```

每条记录确认：

```text
source
target
kind
expected_exists
evidence.file
evidence.line
evidence.snippet
```

然后打开源码：

```bash
nl -ba <source_file> | sed -n '<line-5>,<line+5>p'
```

确认：

- 函数名与源码一致。
- 调用方向正确。
- 调用类型正确。
- 行号和 snippet 完全匹配。

## 5. 资源流复核

打开：

```bash
code validation/resource-flow/dataset.json
```

每个资源确认：

```text
resource.id
operations.kind
operations.api
operations.function
operations.location
ownership_model
paths
ground_truth.classification
ground_truth.review
```

重点检查：

- acquire 是否确实获取资源。
- release 是否释放同一资源实例。
- transfer 是否改变所有权。
- 错误路径是否缺少 release。
- escape 是否可能逃逸到外部。

## 6. 同步关系复核

打开：

```bash
code validation/sync-relations/dataset.json
code validation/redis/sync-relations.json
```

每条记录确认：

```text
source.function
source.thread
source.shared_object
source.held_locks
source.operation
target.function
target.thread
target.shared_object
target.held_locks
target.operation
order
condition
evidence
```

重点检查：

- source 和 target 是否操作同一个共享对象。
- held_locks 是否正确。
- happens_before 是否由锁、原子或程序顺序支持。
- concurrent 是否确实允许并发。
- unknown 是否不应被误判成确定关系。
- condition 是否必要。

## 7. 使用 Excel 记录结论

打开：

```bash
open "validation/人工复核表-2026-10-16.xlsx"
```

使用：

```text
Category 筛选
Project 筛选
Decision 下拉选择
Notes 填写问题
```

结论选项：

```text
Pending
Confirmed
Confirmed with condition
Rejected
Needs fix
```

## 8. 复核完成后的同步

把 Excel 中的 Decision 和 Notes 同步回对应 JSON，然后运行：

```bash
python3 scripts/prepare_validation_truth.py
python3 scripts/reproduce_validation.py
```

检查：

```bash
cat validation/results/libuv/baseline/report.md
cat validation/results/redis/baseline/report.md
```

## 9. 复核完成标准

全部满足后才算验证集 v1 完成：

```text
所有 pending 均已处理
confirmed / rejected 均有记录
evidence 与源码一致
没有悬空 evidence_ids
source hash 校验通过
benchmark 可重复生成
CI 结果可复现
```
