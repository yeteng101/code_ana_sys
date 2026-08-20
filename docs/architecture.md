# 代码逆向 Agent：架构与规范

## 1. 设计目标

系统输入一个固定版本的 C/C++ 仓库和编译配置，输出可复核的模块图、调用链、异步链、函数指针候选、宏差异和自然语言解释。

设计约束：可复现、可增量、可审计、允许不确定性、跨平台配置隔离。

## 2. Agent 组织

```text
Orchestrator
  ├─ RepositoryIndexer
  ├─ BuildMacroAnalyzer
  ├─ CallGraphAnalyzer
  ├─ FunctionPointerResolver
  ├─ AsyncEventTracer
  ├─ ArchitectureSynthesizer
  ├─ NaturalLanguageAnalyst
  └─ VerificationAgent
```

### Agent 职责

| Agent | 输入 | 输出 |
|---|---|---|
| RepositoryIndexer | 文件、构建脚本 | 文件/符号/include 索引 |
| BuildMacroAnalyzer | 编译命令、生成脚本 | 配置矩阵、条件可达性 |
| CallGraphAnalyzer | AST/IR、符号索引 | 直接调用图、CFG 摘要 |
| FunctionPointerResolver | 类型、赋值、注册点 | 候选目标和 points-to 证据 |
| AsyncEventTracer | 注册点、队列、线程信息 | 事件注册/触发/回调链 |
| ArchitectureSynthesizer | 各类图 | 模块图、生命周期图、关键路径 |
| NaturalLanguageAnalyst | 图、证据、用户问题 | 带引用的自然语言答案 |
| VerificationAgent | 结果图、源码 | 覆盖率、矛盾、不确定性报告 |

## 3. 执行协议

1. 编排器创建 `analysis_run`，锁定 commit 和 build profile。
2. Indexer 与 BuildMacroAnalyzer 并行运行。
3. 其余 Agent 只读取版本化 artifact，不直接修改别的 Agent 的结果。
4. Synthesizer 合并边；冲突保留双方证据并降低置信度。
5. VerificationAgent 通过后，才允许生成报告和图。

artifact 使用内容哈希寻址，例如 `graph://call-chain/<sha256>`；相同输入可以复用缓存。

## 4. 证据与置信度规范

- `1.0`：源码直接调用或编译器确认的唯一目标。
- `0.8-0.99`：类型、赋值流和控制流共同确认。
- `0.5-0.79`：存在多个候选，但上下文提供了较强约束。
- `<0.5`：启发式推断，只能作为待验证线索。

每条结论必须包含 `file`、`line`、`snippet_hash` 或 AST 节点 ID。跨宏配置的边必须带 `condition`，跨线程/进程的边必须带 `execution_context`。

## 5. 安全与工程规范

- 源码解析在隔离工作目录中进行；构建命令默认禁止网络和任意写入。
- 单个 Agent 有超时、节点数和输出大小上限。
- 失败允许返回部分 artifact，并在 `warnings` 中列出缺失原因。
- Schema 使用语义版本号；新增字段向后兼容，删除或改义必须升主版本。
- 不把模型生成的解释当作事实；事实必须来自 Evidence Graph。

## 6. 验证门禁

- 关键入口链覆盖率 >= 90%。
- 回调注册到执行的映射准确率目标 >= 85%。
- 函数指针候选召回率目标 >= 80%。
- 100% 的报告结论有源码证据。
- 同一 commit、同一 profile 的结果哈希稳定。
