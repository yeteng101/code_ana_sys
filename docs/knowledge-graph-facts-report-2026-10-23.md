# 知识图谱、编译器事实与日志实时提取报告

## 1. 知识图谱

知识图谱把源码分析、资源流、同步关系、构建配置和运行观测统一表示为“实体 + 关系 + 证据”。

主要实体：

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

与函数调用图的区别是：调用图只回答“谁调用谁”，知识图谱还可以回答“哪个函数使用资源、参与同步、在什么优化配置下编译、是否命中运行日志”。

当前输出：

```text
knowledge/build-profile.json
knowledge/log-facts.json
knowledge/knowledge-graph.json
external/knowledge-graph.json
```

## 2. 编译器事实提取

从 `compile_commands.json` 提取：

```text
优化级别：-O0 / -O1 / -O2 / -O3 / -Os / -Oz
语言标准：-std=...
宏定义：-D...
头文件路径：-I...
target triple
sanitizer / LTO / debug / fast-math
```

启用 `--optimized-ir` 后，还会生成优化后的 LLVM IR，提取 call/invoke 事实，并与 AST 调用比较：

```text
inlined_or_eliminated
introduced_by_optimization
```

LLVM 中的 C++ mangled 名称通过 `c++filt -n` 归一化，避免同一个函数被误判成“消失”和“新增”。

## 3. 日志事实与分析时导入

支持：

```text
file:line:column: warning/error: message
堆栈帧 file:line
JSON Lines
function=name event=name
```

URL Subagent 可以通过 `--log` 导入构建或运行日志，生成 `log-facts.json`，并把日志事件关联到函数。

## 4. 日志实时提取

分析完成后可运行：

```bash
python3 scripts/watch_log_facts.py \
  --workspace artifacts/project/workspace \
  --log /var/log/project/runtime.log \
  --interval 1
```

Watcher 首次读取现有内容，之后只处理追加行；有新事件时增量写入：

```text
10-knowledge/log-facts.json
10-knowledge/log-events.jsonl
10-knowledge/knowledge-graph.json
external/knowledge-graph.json
```

使用 `--once` 可执行一次增量提取，适合 CI 或外部调度；使用 `--no-refresh` 可只提取日志、不刷新图。

## 5. 准确率提升

### 5.1 指标口径

- `TP`：标准答案中存在，系统也找到。
- `FN`：标准答案中存在，系统漏掉。
- `FP`：系统输出，但标准答案否定或类型/顺序错误。
- **Precision（精确率）**：系统找到的结果中有多少是对的。
- **Recall（召回率）**：标准答案中的正例有多少被找到了。
- **F1**：Precision 和 Recall 的调和平均，综合反映“找得对”和“找得全”。

计算公式：

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 × Precision × Recall / (Precision + Recall)
          = 2 × TP / (2 × TP + FP + FN)
```

这里的“准确率”统一指 **Precision**，不是全仓库所有预测的普通 Accuracy。当前 precision 只在已标注 identity 范围内计算，未标注预测不计入 FP。

### 5.2 当前结果

| 项目 / 类型 | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| libuv 资源流 | 11 | 0 | 6 | 100% | 64.71% | 78.57% |
| Redis 调用链 | 103 | 0 | 7 | 100% | 93.64% | 96.71% |
| libuv 同步关系 | 4 | 0 | 28 | 100% | 12.50% | 22.22% |
| Redis 同步关系 | 9 | 0 | 13 | 100% | 40.91% | 58.06% |

计算示例：

```text
libuv 资源流 Recall = 11 / (11 + 6) = 64.71%
libuv 资源流 F1      = 22 / (22 + 0 + 6) = 78.57%

Redis 调用链 Recall  = 103 / (103 + 7) = 93.64%
Redis 调用链 F1      = 206 / (206 + 0 + 7) = 96.71%

Redis 同步 Recall    = 9 / (9 + 13) = 40.91%
Redis 同步 F1        = 18 / (18 + 0 + 13) = 58.06%
```

当前 Precision 均为 100% 的原因是已标注 identity 内没有命中 FP；这不等价于整个仓库所有未标注预测都是正确的。

提升来源：

- 恢复 external function 节点，避免调用链提前截断。
- 使用稳定资源 ID 和精确 API 匹配。
- 增加跨函数队列、atomic release/acquire、thread join 和程序顺序。
- 增加资源赋值、返回、别名和跨函数所有权 transfer。
- 修复 builtin 名称、宏展开调用点和平台条件。
- 使用固定 commit、source hash、evidence 和统一评测 identity。
- 使用 `report.json/report.md/gate.json` 质量门禁防止指标回退。

注意：这些是标注范围内结果，FP=0 不等于全仓库 precision 已完成；大量未标注预测未计入 precision，人工 Gold 仍需确认。

## 6. 当前状态

```text
URL -> 检出 -> 构建探测 -> 七阶段分析
-> 调用图 / 资源流 / 同步关系
-> 编译器事实 + LLVM IR 事实
-> 批量/实时日志事实
-> 知识图谱
-> Knowledge 可视化 + Agent/MCP + Neo4j
-> candidate -> 人工复核 -> Gold -> CI 门禁
```

代码和报告已经可复现；人工复核仍是 `pending`。
