# libuv 同步关系验证集

对应看板任务 `178904939922139125250091`（630 认领）。基于开发分支
`codex/agent-llm-framework` 的 `a505c4709173c2519a72cea208101258c5ce179f`，
新增 32 条源码审查样本，未从待评测调用图自动复制标签。

## 范围与结果

- libuv v1.50.0，commit `8fb9cb919489a48880680a56efecff6a7dfb4504`。
- Linux/POSIX 静态源码配置，覆盖 `threadpool.c`、`unix/async.c`、
  `unix/thread.c`、`unix/linux.c`，不声称运行过 Windows/macOS 路径。
- 26 条 happens_before，2 条允许并发的 concurrent，4 条证据不足的 unknown。
- 26 正例、6 反例；mutex、rwlock、atomic、condition_variable、
  event_wait、event_notify、thread_join 及程序顺序均有覆盖。
- `check-report.json` 是完整性检查结果，不是分析器 precision/recall，
  也不是运行时并发证明。`review.human_review=pending`：AI 已审查源码，待人工复核。

引用的完整源码文件按 LF 归一化 SHA-256
固定，兼容 Windows Git CRLF 检出；证据正文、行号与引用均需匹配。

## 复现

在仓库根目录运行（已有源码时检查 HEAD，不覆盖已有修改）：

```sh
git clone --depth 1 --branch v1.50.0 https://github.com/libuv/libuv.git third_party/libuv
git -C third_party/libuv rev-parse HEAD
# 必须为 8fb9cb919489a48880680a56efecff6a7dfb4504
python -m pip install -r validation/sync-relations/requirements.txt
python scripts/check_sync_validation.py --report validation/sync-relations/check-report.json
python -m unittest discover -s validation/tests -v
```

校验器执行 `schemas/sync-validation.schema.json` 的 Draft 2020-12 检查，
要求至少 30 条样本及三类 order。缺少源码、版本不符、文件修改、缺失字段、
重复 ID、悬空 evidence 引用、错行、错 snippet、标注自相矛盾均返回非零。
新增的 GitHub Actions `sync-validation` job 执行相同命令并保存报告。

## 标注约定

每条记录的 `source` / `target` 包含函数、线程角色、共享对象、操作、
操作成功完成后的 `held_locks` 和 evidence 引用。等待操作的 held_locks
指成功返回后的状态，不表示阻塞期间仍持锁。跨线程使用同一逻辑对象名称
必须结合 `condition` 中的同一实例、队列项或读写来源约束。

`condition` 是关系成立的必要前提，不能在评测时丢弃。
`claim_order` 是待检验命题，`order` 是源码与同步原语契约支持的答案。

| label | 含义 |
|---|---|
| positive | 证据和前提支持该已知顺序 |
| negative | 命题过强或错误；答案可能是 concurrent，也可能是 unknown |
| uncertain | 尚不能确定命题，答案必须是 unknown（预留） |

`classification=consistent` 表示正命题与条件相符；`inconsistent` 表示
明确拒绝指定方向性顺序的并发反例；`unknown` 表示不能证明命题。
这些标签不代表 data race/deadlock 等最终缺陷结论。
confidence 是对标注判断的信心，unknown 的高 confidence 不表示同步关系已确认。

- happens_before：条件成立时的程序顺序、原语同步或事件因果关系。eventfd
  样本只证明通知被消费的因果顺序；C11 内存发布另由 pending 原子/锁证明。
- concurrent：允许无方向性顺序，不断言某次运行真的同时执行，不等于竞态。
- unknown：缺少实例配对、读写来源或额外同步信息；不能转换成负向 HB 证明。

## 重点复核

1. 001/012：队列发布依赖同一 mutex 释放/获取和同一请求，不是只见函数名即配对。
2. 004：condition signal 不指定 worker；等待采用 while 检查，容许虚假唤醒。
3. 008/031：工作回调和共享读锁允许并发，不能从源码文本先后推出线程先后。
4. 019/023：原子同步要求明确 reads-from / 观察到归零，且遵守 handle 生命周期。
5. 020/026/032：relaxed load、合并通知、失败 trylock 不能单独提供发布证据。
6. 027/028：覆盖 poll 唤醒和分发；不声称任意 send 都产生一次 callback。

人工复核应逐条阅读 evidence 所在完整函数，检查条件、锁状态、平台和
POSIX/C11 原语语义。复核人确认后再变更 review 元数据，不因机器检查通过
自动升级为人工 Gold。资源流、调用链的未完成任务不在本次改动范围内。
