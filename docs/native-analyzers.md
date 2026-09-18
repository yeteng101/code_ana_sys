# 原生分析器：资源流和同步关系

本项目原来的七阶段流水线原生输出调用图、函数指针和异步链。资源流和同步关系
现在新增了两个**原生提取器**：

```text
clang_pipeline/resource_flow.py
clang_pipeline/sync_flow.py
```

它们不读取 validation ground truth，也不使用 reviewed annotations；输入是
Clang 产物形成的 `graph.json`，输出标记为 `origin=analyzer`。

## 运行

在已有 workspace 上运行：

```bash
python3 -m clang_pipeline.cli native \
  --workspace demo/libuv
```

也可以显式指定调用图：

```bash
python3 -m clang_pipeline.cli native \
  --workspace demo/libuv \
  --graph demo/libuv/graph.json
```

输出：

```text
<workspace>/08-resource-flow/resource-flow.json
<workspace>/09-sync-relations/sync-relations.json
<workspace>/external/resource-flow.json
<workspace>/external/sync-relations.json
```

## 资源流分析器

第一版是规则和调用图驱动的可解释实现：

- 从 graph edge 的 `call_site` 提取 API、函数、文件、行号和 snippet；
- 把 `malloc/free`、`open/close`、`uv__make_pipe/uv__close`、
  `dlopen/dlclose`、`scandir/cleanup`、`getaddrinfo/freeaddrinfo`
  映射为 acquire/release；
- 按 resource key、函数和资源族配对操作；
- 每个事实都必须带 graph 中原有的 evidence id；
- 没有配对到的操作输出 `complete=false` 和
  `release_not_found` / `acquire_not_found`，不直接写 `memory_leak=true`。

当前局限：

```text
只做调用图可见的直接资源操作
不做完整指针别名、CFG 和错误路径求解
跨函数的资源对象依赖规则和表达式 key
不把不完整路径直接判为最终泄漏
```

## 同步关系分析器

第一版从 graph edge 提取：

```text
mutex_lock / unlock
rwlock rdlock / wrlock / unlock
condition wait / signal / broadcast
thread create / join
event wait / notify
```

明确配对：

- 同一函数、同一资源 key 的 lock -> unlock；
- 同一资源 key 的 condition notify -> wait；
- graph 中同时存在的 event notify/wait 作为低置信度关系；
- 每条关系带 source/target 文件、行号、snippet、confidence 和 evidence_ids。

当前局限：

```text
跨线程 happens-before 仍是启发式
不解析 reads-from、锁顺序环和数据竞争的最终结论
unknown 不会被伪装成 concurrent 或 happens_before
```

## 和外部 JSON 的关系

`cli native` 会产生两类 JSON：

```text
08-resource-flow/resource-flow.json
09-sync-relations/sync-relations.json
```

同时把外部接口契约版本写到：

```text
external/resource-flow.json
external/sync-relations.json
```

这两份文件的 `origin` 必须是：

```text
analyzer
```

人工标注仍然只能放在 reviewed 目录，不能替代原生预测。
