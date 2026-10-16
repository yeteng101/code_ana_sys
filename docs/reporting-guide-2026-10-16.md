# 汇报与答辩指南

## 1. 一句话项目介绍

输入 C/C++ 仓库 URL，自动完成调用图、调用链、资源流、同步关系、JSON 文件和
可视化页面的代码逆向分析 Subagent。

## 2. 汇报主线

```text
问题
→ Clang 事实提取
→ Agent 工具调用
→ 三类分析结果
→ 统一验证集
→ 新仓库 candidate / Gold 工作流
→ 可视化
→ 仓库 URL 业务闭环
```

## 3. 当前核心指标

| 指标 | 当前值 |
|---|---:|
| libuv 资源流 recall | 64.71% |
| libuv 资源流 F1 | 78.57% |
| Redis 调用链 recall | 93.64% |
| Redis 调用链 F1 | 96.71% |
| libuv 同步关系 recall | 12.50% |
| Redis 同步关系 recall | 31.82% |
| 当前 FP | 0 |

## 4. 可现场演示

```bash
python3 -m clang_pipeline.cli repo \
  --repo-url file:///Users/andye/Documents/ChatGPT/8.18huawei/clang_pipeline/tests/fixtures \
  --output /tmp/demo-analysis \
  --no-archive
```

```bash
open /tmp/demo-analysis/visualization.html
```

## 5. 可能被追问的问题

### recall 为什么提升？

重新生成调用图，恢复系统调用；资源流统一稳定 ID；同步关系增加程序顺序事实。

### precision 100% 是否意味着完成？

不是。当前只在已标注样本上计算 precision，大量 unlabelled prediction 未计入。

### 同步关系为什么仍较低？

跨线程队列、原子变量、CFG、reads-from、held-locks 尚未完整实现。

### 这是否只支持 libuv/Redis？

不是。Subagent 和可视化是仓库无关的。除 libuv/Redis 外，已用独立 C 和 C++
示例仓库验证同一个 URL 入口，均生成调用图、资源流、同步关系 JSON 和可视化。

### 验证集是否防止数据泄漏？

是。Gold 只用于评测，分析器不读取 Gold 作为预测。

### 这次模拟复核能当作人工复核吗？

不能。模拟复核完成了 356 行的 evidence 源码检查，并生成独立 reviewed Gold，
但它仍是 `method=simulated_manual_review_by_codex`，官方
`human_review=pending`。汇报时应明确这是 AI 辅助预审，最终需人工抽检确认。

### 验证集能否直接迁移到新仓库？

评测框架和流程可以复用，libuv/Redis 的 Gold 不能复用。每个仓库需要固定
commit、重新收集 candidate、人工确认/拒绝，并补充分析器漏检的 Gold。

### Agent 体现在哪里？

MCP 工具层、AgentContext、工具执行循环、Claude Code/OpenAI 后端和仓库 URL 闭环。

### 为什么 Clang 负责事实，LLM 只负责解释？

防止模型编造代码事实，所有结论必须挂 evidence。

### 结果是否可复现？

固定 commit、源码 hash、evidence 和构建 profile，CI 可重复生成评测结果。

### 新仓库从 URL 到 Gold 的命令是什么？

完整命令和文件状态在
[`validation-project-workflow.md`](validation-project-workflow.md)：

```text
scaffold_validation_project
-> collect_validation_candidates
-> 人工 review-table.csv
-> build_validation_ground_truth
-> pin_validation_project
-> check_validation_projects
-> evaluate_validation
```

## 6. 汇报结尾

当前系统已经完成从仓库输入到结果输出的闭环，验证集能够衡量调用链、资源流和
同步关系的准确率。同一个入口已经能迁移到新的 C/C++ 仓库。下一阶段重点是
同步关系、资源流深层语义、人工复核和 CI 门禁。
