# Redis 7.2.4 基准标注

固定 commit `d2c8a4b91e8c0e6aefd1f5bc0bf582cddbe046b7`。

- `call-chains.json`：110 条正例、10 条负例，共 120 条调用关系标注。
  覆盖 adlist、ae、bio、lazyfree；按函数 source/target/type 去重，不靠重复行凑数。
- `sync-relations.json`：22 条同步关系，含 19 条 happens_before、1 条 concurrent、
  2 条 unknown。覆盖后台队列、条件变量、join、I/O 线程批次、原子发布与 relaxed 反例。
- `../benchmarks/redis/ground-truth.json`：统一评测格式，145 条命题
  （120 调用命题、22 关系答案、3 条被拒绝的同步先后命题）。

标注来源为固定真实源码，候选收集后逐项审查函数与宏语义，未从分析器图复制。
AI 源码审查完成，human_review=pending；这不是人工 Gold 验收记录。
调用负例检查直接命名调用不应误标 callback_edge。宏 serverLog 映射为
_serverLog；Linux redis_set_thread_title 映射为 pthread_setname_np，均带两处证据。

同步 condition 是必要前提：同一 worker/对象、成功获取/释放、明确 reads-from、
对应批次等不可省略。held_locks 表示操作成功完成时持有的锁，condition wait
阻塞期间释放锁；concurrent 表示允许无先后顺序，不断言实际同时执行或发生竞态。

真实编译由 `scripts/run_redis_validation.sh` 在 Linux 中运行 Redis 原生 Makefile，
Bear 捕获全部编译命令，再分析 8 个真实 translation units。选定范围和编译参数见
`demo/redis/build-provenance.json`，完整编译数据库保留 CI 运行时的绝对路径；
在其他机器重现时重新执行构建脚本，不直接复用这些绝对路径。

使用同一评测器和外部 schema，具体命令、指标定义与跨项目局限见
[`../benchmarks/README.md`](../benchmarks/README.md)。
