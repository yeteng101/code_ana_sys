# 验证集标注规范 v1

统一评测、libuv/Redis baseline 与三类外部 JSON：
[`benchmarks/README.md`](benchmarks/README.md)。

新仓库验证项目从骨架到 Gold 的完整流程：
[`../docs/validation-project-workflow.md`](../docs/validation-project-workflow.md)。

人工复核步骤和 Excel 复核表：
[`MANUAL_REVIEW_GUIDE.md`](MANUAL_REVIEW_GUIDE.md)。

同步关系样本已补齐：[`sync-relations/README.md`](sync-relations/README.md)。
包含固定 libuv v1.50.0 源码上的 32 条关系（26 正例、6 反例），
区分 happens_before / concurrent / unknown，并提供独立 schema、证据校验和 CI。
标注为 AI 源码审查，人工复核状态单独记录，不冒充人工确认。

本目录的标注规范部分参照《第一组返回结果与通信接口规范 v2》，但验证集只负责
记录可复核的事实和人工确认的 ground truth，不把验证集标签直接当作对外接口结论。

## 通用框架与仓库专用 Gold

评测器、schema、证据规则和脚本可以复用到任何 C/C++ 仓库；libuv/Redis 的
`ground-truth.json` 只属于各自固定 commit。迁移到新仓库时：

```text
复用：分析器、JSON 导出、打分器、注册校验、source hash 规则
重建：仓库 pin、candidate 复核、Gold、负样本和人工漏检补充
禁止：把 libuv/Redis Gold 当作新仓库的标准答案
```

新项目目录统一放在 `validation/datasets/<project-id>/`，并在
`validation/projects.json` 注册。分析结果先成为 candidate；只有人工
`Confirmed` / `Rejected` 或 `gold-additions.json` 才进入 Gold。

## 三类结果

| 类型 | 验证目标 | 验证集标签 | 对外接口禁止直接写 |
|---|---|---|---|
| 调用链 | source、target、edge kind 是否正确 | positive / negative / uncertain | 不返回最终缺陷结论 |
| 资源流 | acquire、use、transfer、release 和逃逸路径是否完整 | no_leak / leak / double_free / use_after_free / uncertain | 不直接写 `memory_leak=true` |
| 同步关系 | 共享访问、held_locks、happens-before 是否正确 | consistent / inconsistent / unknown | 不直接写 `deadlock=true` 或 `race=true` |

## 调用链

正样本必须同时满足：

```text
same source
same target
same kind
```

正负样本统一记录：

```text
claim.source
claim.target
claim.kind
evidence.file / line / snippet
resolution
```

## 资源流

资源流先记录操作事实：

```text
acquire
use
retain
release
drop_ref
transfer
borrow
escape
invalidate
```

泄漏由“路径事实”表达，例如：

```text
error_return 路径存在 acquire
当前路径没有找到 release
termination_reason = release_not_found
```

验证集可以标 `ground_truth.classification=leak`，但对外接口仍只返回操作、路径、
覆盖率和证据，由第三组结合 PR diff 做最终缺陷判断。

## 同步关系

同步关系必须同时记录：

- 共享对象的读写访问；
- 访问所在线程或事件循环；
- 访问时持有的锁；
- 锁的 acquire/release 位置；
- 锁顺序边；
- 回调和异步边界。

验证集不把“没有锁”直接标成竞态。`inconsistent` 只表示人工确认的不同步事实，
是否构成最终缺陷由专项 Agent 判断。
