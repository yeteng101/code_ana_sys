# 资源流样本与泄漏标注 v1

本目录按《第一组返回结果与通信接口规范 v2》的资源流约定构建，重点区分：

```text
接口应该返回什么事实
验证集人工标注的 ground truth 是什么
```

接口不直接返回：

```text
memory_leak = true
```

接口只返回操作、路径、所有权、覆盖率和证据。验证集可以额外标注：

```text
ground_truth.classification = no_leak / leak / uncertain
```

## 标注规则

### no_leak

满足任一条件：

- 同一路径存在 acquire 和 release；
- 资源通过 `transfer` 或 `escape` 交给调用方；
- 资源所有权仍由更大的生命周期对象持有，例如 loop 或 request。

### leak

必须同时满足：

- 某条路径存在 acquire；
- 同一路径没有找到 release、transfer 或 escape；
- 路径标记为 `complete=false`；
- `termination_reason` 为 `release_not_found`。

### uncertain

平台条件、回调候选或调用图不完整，导致无法确认是否会被其他路径释放。

## 当前样本

| ID | 类型 | ground truth |
|---|---|---|
| `rf_libuv_fs_fd_v1` | 文件描述符生命周期 | `no_leak` |
| `rf_libuv_getpwuid_buf_v1` | 堆内存生命周期 | `no_leak` |
| `rf_libuv_async_fd_v1` | loop 异步唤醒 fd | `no_leak` |
| `rf_synth_leak_error_path_v1` | 错误路径泄漏 | `leak` |
| `rf_synth_ownership_transfer_v1` | 所有权转移 | `no_leak` |

前三个来自 libuv 的真实源码，后两个是仓库内固定的合成 fixture，用于精确测试
“错误路径漏 release”和“所有权 escape 不是泄漏”这两个边界。

## 校验

```bash
python3 scripts/check_resource_flow_validation.py \
  --dataset validation/resource-flow/dataset.json
```

校验器会检查：

1. resource ID 是否唯一；
2. operation ID 是否在同一资源内唯一；
3. path 引用的 operation 是否存在；
4. evidence_ids 是否都能在资源 evidence 中找到；
5. `leak` 样本必须存在 `release_not_found` 路径；
6. 源码存在时，evidence 的文件、行号和 snippet 是否匹配。
