# 调用链正负样本标注 v1

这是验证集的第一批人工标注，目标是先约束“调用链结果”这件事，而不是等所有
分析阶段完成后再补标注。

## 标注口径

一条样本的 `claim` 包含：

```text
source  起点符号 ID
target  终点符号 ID
kind    direct_call / callback_edge / indirect_call
```

标签规则：

| label | 含义 |
|---|---|
| `positive` | 图里存在同 source、target、kind 的边 |
| `negative` | 图里不存在同 source、target、kind 的边 |
| `uncertain` | 需要继续查源码或构建其他 profile 才能确认 |

特别注意：

- `source -> target` 存在，但 `kind` 不对，仍然是 negative。
- 回调字段匹配到多个候选函数时，`resolution=multiple_candidates`，不能被当成唯一目标。
- 只有“同 source、同 target、同 kind”三件事都一致，才算正样本。

## 文件

```text
validation/call-chains/dataset.json
validation/call-chains/README.md
schemas/call-chain-validation.schema.json
```

`dataset.json` 的每个样本包含：

```json
{
  "id": "cc_pos_0001",
  "graph": "demo/libuv/graph.json",
  "claim": {
    "source": "fn:uv_run",
    "target": "fn:uv__io_poll",
    "kind": "direct_call"
  },
  "label": "positive",
  "expected_exists": true,
  "resolution": "unique",
  "candidate_targets": [],
  "evidence": [
    {
      "file": "third_party/libuv/src/unix/core.c",
      "line": 460,
      "snippet": "uv__io_poll(loop, timeout);"
    }
  ],
  "tags": ["libuv", "direct_call"],
  "notes": "uv_run 明确直接调用 uv__io_poll"
}
```

## 校验

```bash
python3 scripts/check_call_chain_validation.py \
  --dataset validation/call-chains/dataset.json \
  --graph demo/graph.json \
  --graph demo/libuv/graph.json
```

校验器会检查：

1. 样本 ID 是否唯一；
2. `label` 和 `expected_exists` 是否一致；
3. `positive` 样本的 `source/target/kind` 是否真的存在于图；
4. `negative` 样本是否确实不存在同 kind 的边；
5. 如果源码文件在当前仓库可见，evidence 的文件、行号和原文片段是否匹配。

## 当前覆盖范围

- demo 小样例：直接调用、回调字段、回调候选
- libuv v1.50.0：`uv_run` 直接调用、定时器链、事件回调字段
- 负样本：错误 kind、把回调注册误判成直接调用、把间接到达误判成直接调用

下一批应扩展到：

- 更多 libuv profile（epoll / kqueue / select）
- 宏展开后的条件边
- 函数指针赋值流
- 跨线程和异步边界
- Redis 的调用链正负样本
