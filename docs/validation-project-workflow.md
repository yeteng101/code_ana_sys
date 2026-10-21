# 新仓库验证项目工作流

## 1. 设计边界

验证框架、评测器、打分规则和 JSON 导出是通用能力；每个新 C/C++ 仓库都必须
建立自己的 repository-specific Gold。不能把 libuv/Redis 的 Gold 直接作为
另一个仓库的标准答案。

```text
仓库 URL
  -> 检出并固定 commit
  -> 七阶段分析 + 原生资源流/同步关系分析
  -> external JSON 分析结果
  -> 收集 candidate facts
  -> 人工复核 review-table.csv
  -> 构建 Gold
  -> 固定源码 SHA-256
  -> 注册校验
  -> 通用评测
  -> report.json / report.md
```

分析器结果始终是 candidate，不能自动变成 Gold。`Confirmed` 表示分析器
候选正确，`Rejected` 表示该 identity/kind 是错误预测并成为负样本。
分析器没有输出的漏检事实需要人工加入 `gold-additions.json`，否则新项目
无法可靠测量 recall。

## 2. 初始化新项目

先把目标源码固定到仓库内：

```bash
git clone https://github.com/example/project.git third_party/project
git -C third_party/project checkout <40-character-commit>
```

创建验证项目并登记到 `validation/projects.json`：

```bash
python3 scripts/scaffold_validation_project.py \
  --project-id project \
  --name "Example Project" \
  --repository example/project \
  --repository-url https://github.com/example/project.git \
  --commit "$(git -C third_party/project rev-parse HEAD)" \
  --build-profile repository-auto \
  --source-root third_party/project
```

生成位置：

```text
validation/datasets/project/
├── manifest.json
├── source-manifest.json
├── candidates.json
├── gold-additions.json
├── ground-truth.json
├── review-table.csv
└── review-checklists/
```

## 3. 运行 URL Subagent

```bash
python3 -m clang_pipeline.cli repo \
  --repo-url https://github.com/example/project.git \
  --commit "$(git -C third_party/project rev-parse HEAD)" \
  --output artifacts/project-analysis \
  --no-archive
```

可以把前两步合并成一次运行：

```bash
python3 -m clang_pipeline.cli repo \
  --repo-url https://github.com/example/project.git \
  --commit "$(git -C third_party/project rev-parse HEAD)" \
  --output artifacts/project-analysis \
  --no-archive \
  --validation-project project \
  --validation-repository example/project
```

这样会先初始化 `validation/datasets/project/`，再从本次分析结果收集
`review-table.csv`；Gold 仍必须人工复核，不会自动生成。

三个用于评测的外部结果位于：

```text
artifacts/project-analysis/external/call-chains.json
artifacts/project-analysis/external/resource-flow.json
artifacts/project-analysis/external/sync-relations.json
```

URL Subagent 在打包时会把这些 JSON 中的源码路径转换成仓库相对路径，
因此重跑后 evidence identity 仍然稳定，可以用于后续评测。

## 4. 收集人工复核候选

```bash
python3 scripts/collect_validation_candidates.py \
  --project-id project \
  --predictions artifacts/project-analysis/external \
  --source-root third_party/project \
  --limit 100
```

`--limit 0` 表示不截断。默认每类最多 100 条，避免单次人工复核表过大。
候选事实不会自动进入 Gold；`manifest.status` 会停留在
`candidates_collected`。

打开复核表：

```bash
open validation/datasets/project/review-table.csv
```

复核时填写 `decision` 和 `notes`：

```text
Pending
Confirmed
Confirmed with condition
Rejected
Needs fix
```

每条结论都要回到源码检查 `evidence` 的 file/line/snippet。

## 5. 补充人工 Gold

分析器漏掉的事实写入 `validation/datasets/project/gold-additions.json`。
每条使用统一 case 格式：

```json
{
  "id": "manual_sync_missed_001",
  "category": "sync_relation",
  "identity": ["producer", "consumer", "src/queue.c", 41, "src/queue.c", 87],
  "kind": "happens_before",
  "expected_exists": true,
  "evidence": [
    {"file": "src/queue.c", "line": 41, "snippet": "pthread_mutex_unlock(&q->lock);"},
    {"file": "src/queue.c", "line": 87, "snippet": "pthread_mutex_lock(&q->lock);"}
  ],
  "notes": "人工从源码补充的跨线程发布关系"
}
```

调用链 identity 为 `[source_symbol, target_symbol]`；资源流为
`[resource_id, function, file, line]`；同步关系为两端 function、file、
line 共六个值。

## 6. 构建 Gold

```bash
python3 scripts/build_validation_ground_truth.py \
  --project-id project
```

脚本读取 CSV 的 decision：

```text
Confirmed / Confirmed with condition -> expected_exists = true
Rejected                              -> expected_exists = false
Pending / Needs fix                   -> 不进入 Gold
```

所有候选都处理完时 `human_review=confirmed`，否则为 `partial`。

## 7. 固定源码

```bash
python3 scripts/pin_validation_project.py \
  --project-id project
```

脚本收集全部 evidence 文件并写入 LF-normalized SHA-256：

```text
validation/datasets/project/source-manifest.json
```

## 8. 校验和评测

```bash
python3 scripts/check_validation_projects.py \
  --report validation/results/project/project-check.json
```

```bash
python3 scripts/run_validation_project.py \
  --project-id project \
  --ground-truth validation/datasets/project/ground-truth.json \
  --predictions artifacts/project-analysis/external \
  --output validation/results/project/baseline \
  --min-call-recall 0.90 \
  --min-resource-recall 0.60 \
  --min-sync-recall 0.20 \
  --max-fp 0
```

该命令同时生成 `report.json`、`report.md` 和 `gate.json`。任一阈值不满足时
返回非零退出码，可直接作为 CI 门禁。最终人工验收阶段增加：

```text
--strict-review
```

它会要求 `review.human_review=confirmed`，否则 CI 失败。

打开报告：

```bash
cat validation/results/project/baseline/report.md
cat validation/results/project/baseline/gate.json
```

## 9. 状态含义

| 状态 | 含义 |
|---|---|
| `not_started` | 只有项目骨架 |
| `candidates_collected` | 已有候选，等待人工复核 |
| `in_review` | 已有 Gold，但仍有 pending/needs-fix |
| `ready` | 候选已全部处理，Gold 非空，可评测 |

`check_validation_projects.py --strict` 会在仍有 pending 时失败，可作为
CI 质量门禁。
