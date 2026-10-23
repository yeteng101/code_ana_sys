# 证据知识图谱

知识图谱把原本分散的静态分析事实、构建事实和观测事实关联起来：

```text
函数 / 模块
  + 调用边与 evidence
  + 资源流
  + 同步关系
  + 编译单元 / 优化参数
  + compiler diagnostics / runtime logs
```

## 产物

URL Subagent 会生成：

```text
external/knowledge-graph.json
external/resource-flow.json
external/sync-relations.json
external/call-chains.json
knowledge/build-profile.json
knowledge/log-facts.json
knowledge/knowledge-graph.json
logs/
```

`knowledge-graph.json` 的主要实体：

```text
code_symbol
build_profile
compile_unit
compiler_optimization
resource
sync_relation
log_event
```

主要关系：

```text
calls
uses_resource
sync_source / sync_target
has_compile_unit
analyzes_symbol
affects_function
references_symbol
```

## 构建事实

从 `compile_commands.json` 提取：

```text
优化级别：-O0 / -O1 / -O2 / -O3 / -Os / -Oz
语言标准：-std=...
宏定义：-D...
头文件路径：-I...
sanitizer / LTO / debug / target
```

启用 LLVM IR 对照：

```bash
python3 -m clang_pipeline.cli repo \
  --repo-url https://github.com/example/project.git \
  --output artifacts/project \
  --optimized-ir
```

该模式会记录：

```text
AST 中存在、优化后调用消失的边 -> inlined_or_eliminated
只在优化后出现的调用 -> introduced_by_optimization
```

IR 是补充事实，不替代 AST 源码边。
LLVM 中的 C++ mangled 名称会通过 `c++filt -n` 归一化到函数名后再与 AST 比较，
避免把同一个 C++ 调用误判为“消失”和“新增”。

## 日志事实

```bash
python3 -m clang_pipeline.cli repo \
  --repo-url https://github.com/example/project.git \
  --output artifacts/project \
  --log build.log \
  --log runtime.log
```

支持：

- `file:line:column: warning/error: message`
- 堆栈帧 `file:line`
- JSON Lines 日志
- `function=name event=name`

日志事件只作为观测事实，不会直接改动 Gold 或自动证明源码缺陷。

## Neo4j

已有的 `graphdb` 命令会同时尝试写入知识图谱实体：

```bash
python3 -m clang_pipeline.cli graphdb \
  --workspace artifacts/project/workspace \
  --run-id run_example \
  --verify
```

知识图谱使用通用的 `KnowledgeEntity` 和 `RELATED` 关系，原有
`CodeNode`、`Evidence`、`CALLS` 保持不变。
