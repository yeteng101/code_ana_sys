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
ground_truth.classification = no_leak / leak / double_free / use_after_free / uncertain
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
| `rf_libuv_getaddrinfo_v1` | addrinfo 所有权转移和释放 | `no_leak` |
| `rf_libuv_scandir_entries_v1` | 目录项数组生命周期 | `no_leak` |
| `rf_libuv_dlopen_handle_v1` | 动态库句柄生命周期 | `no_leak` |
| `rf_synth_leak_error_path_v1` | 错误路径泄漏 | `leak` |
| `rf_synth_ownership_transfer_v1` | 所有权转移 | `no_leak` |
| `rf_synth_double_free_v1` | 重复释放 | `double_free` |
| `rf_synth_use_after_free_v1` | 释放后使用 | `use_after_free` |

前六个来自 libuv 的真实源码，后四个是仓库内固定的合成 fixture，用于精确测试
错误路径漏 release、所有权 escape、double free 和 use-after-free 四类边界。

## 十个样本逐一说明

### 1. `rf_libuv_fs_fd_v1`

来源：libuv 文件系统请求的文件描述符生命周期。

操作序列：

```text
uv__fs_open:372        acquire
uv_fs_open:2028        transfer
uv__fs_close:161       release
```

关键事实：

- `open(...)` 在 `uv__fs_open` 中创建 fd；
- fd 被保存在 `uv_fs_t` 请求结果中；
- 调用方通过 `uv_fs_close` 请求释放；
- acquire 和 release 不在同一个函数里，但它们属于同一条资源生命周期。

验证目标：

```text
不能因为 uv__fs_open 内部没有 close，就误报为泄漏。
```

ground truth：

```text
no_leak
ownership_model = transferred_to_request
```

### 2. `rf_libuv_getpwuid_buf_v1`

来源：libuv 的 `uv__getpwuid_r` 临时 buffer。

操作序列：

```text
uv__getpwuid_r:1274    acquire
uv__getpwuid_r:1322    release
```

关键事实：

- `buf` 在函数内通过 `uv__malloc` 创建；
- 函数返回前通过 `uv__free(buf)` 释放；
- 这个 buffer 不逃逸到调用方。

验证目标：

```text
函数内部的临时资源必须在所有正常返回路径上成对出现。
```

ground truth：

```text
no_leak
ownership_model = local_owner
```

### 3. `rf_libuv_async_fd_v1`

来源：libuv 的 loop 异步唤醒 fd。

操作序列：

```text
uv__async_start:306    acquire
uv__async_start:313    transfer
uv__async_stop:350     release
uv__async_stop:355     release
```

关键事实：

- `uv__make_pipe` 创建唤醒管道；
- 管道 fd 被保存到 `loop->async_wfd`；
- `uv__async_stop` 在 loop 清理时关闭 fd；
- 这里存在平台条件分支，因此 confidence 低于纯直接调用样本。

验证目标：

```text
资源生命周期由更大的对象 loop 托管时，不能按单个函数判断泄漏。
```

ground truth：

```text
no_leak
ownership_model = owned_by_loop
review = confirmed_with_condition
```

### 4. `rf_libuv_getaddrinfo_v1`

来源：libuv 的 DNS 查询结果所有权。

操作序列：

```text
uv__getaddrinfo_work:103    acquire
uv__getaddrinfo_done:134    transfer
uv_freeaddrinfo:222         release
```

关键事实：

- `getaddrinfo` 创建 `addrinfo` 链表；
- 链表通过 callback 交给调用方；
- libuv 提供 `uv_freeaddrinfo` 让调用方释放；
- 资源不是在本函数内部泄漏，而是所有权已经转移。

验证目标：

```text
所有权转移给 caller 时，termination_reason 应该是 owned_by_callee，
不能简单标成 release_not_found。
```

ground truth：

```text
no_leak
ownership_model = transferred_to_callback_caller
```

### 5. `rf_libuv_scandir_entries_v1`

来源：libuv 的目录扫描结果数组。

操作序列：

```text
uv__fs_scandir:585          acquire
uv__fs_scandir:600          transfer
uv__fs_scandir_cleanup:728  release
```

关键事实：

- `scandir` 分配目录项数组；
- 数组地址保存到 `req->ptr`；
- `uv_fs_req_cleanup` 会调用 `uv__fs_scandir_cleanup`；
- 清理函数会释放数组本身以及各个目录项。

验证目标：

```text
资源由 request 托管时，要看 request cleanup，而不是只看创建函数。
```

ground truth：

```text
no_leak
ownership_model = owned_by_fs_request
```

### 6. `rf_libuv_dlopen_handle_v1`

来源：libuv 的动态库句柄。

操作序列：

```text
uv_dlopen:36     acquire
uv_dlclose:47    release
```

关键事实：

- `dlopen` 返回动态库 handle；
- handle 存入 `uv_lib_t`；
- `uv_dlclose` 调用 `dlclose` 释放 handle；
- 同时释放 `lib->errmsg`。

验证目标：

```text
跨函数存储的资源要识别“存入对象”和“对象销毁时释放”两个阶段。
```

ground truth：

```text
no_leak
ownership_model = stored_in_uv_lib_t
```

### 7. `rf_synth_leak_error_path_v1`

来源：仓库内合成 fixture。

文件：

```text
validation/resource-flow/fixtures/leak_error_path.c
```

操作序列：

```text
line 4   acquire
line 8   error_return（没有 release）
line 9   release（normal_return）
```

关键事实：

- `fail=true` 时直接 `return -1`；
- 该错误路径没有 `free(buf)`；
- 正常路径才会执行 `free(buf)`。

接口期望：

```text
error_return 路径：
  acquire 存在
  release 不存在
  complete = false
  termination_reason = release_not_found
```

ground truth：

```text
leak
```

验证目标：

```text
不能只检查函数里是否存在 free，必须按路径检查错误分支。
```

### 8. `rf_synth_ownership_transfer_v1`

来源：仓库内合成 fixture。

文件：

```text
validation/resource-flow/fixtures/ownership_transfer.c
```

操作序列：

```text
line 4   acquire
line 7   escape（return buf）
```

关键事实：

- 当前函数内没有 `free`；
- 但是指针通过 return 交给调用方；
- caller 获得所有权后负责释放。

接口期望：

```text
termination_reason = resource_escaped
```

ground truth：

```text
no_leak
```

验证目标：

```text
“本函数没有 release”不等于“资源泄漏”。
escape / transfer 必须先于 leak 判断。
```

### 9. `rf_synth_double_free_v1`

来源：仓库内合成 fixture。

文件：

```text
validation/resource-flow/fixtures/double_free.c
```

操作序列：

```text
line 4   acquire
line 7   release
line 8   release
```

关键事实：

- 同一个 `buf` 被连续释放两次；
- 这是释放次数异常，不是缺少释放；
- 资源流必须保留两次 release 操作，不能只记录一个布尔值。

接口期望：

```text
release_operations = [line 7, line 8]
termination_reason = double_release_observed
```

ground truth：

```text
double_free
```

验证目标：

```text
区分 leak 和 double free；两者不是同一个错误类型。
```

### 10. `rf_synth_use_after_free_v1`

来源：仓库内合成 fixture。

文件：

```text
validation/resource-flow/fixtures/use_after_free.c
```

操作序列：

```text
line 4   acquire
line 7   release
line 8   use
```

关键事实：

- `buf` 在 line 7 被释放；
- line 8 仍然写入 `buf[0]`；
- 错误来自操作顺序，而不是缺少 release。

接口期望：

```text
operations = [acquire, release, use]
termination_reason = use_after_release_observed
```

ground truth：

```text
use_after_free
```

验证目标：

```text
资源流不仅要记录操作集合，还必须保留操作顺序。
```

## 容易混淆的四个判断

| 现象 | 不能直接判断 | 正确做法 |
|---|---|---|
| 本函数没有 release | leak | 先看 transfer / escape / caller ownership |
| 出现了两次 release | leak | 标为 double_free |
| release 之后还有 use | leak | 标为 use_after_free |
| 错误路径没有 release | 一定是缺陷 | 先看是否有其他错误处理路径或 caller 释放 |

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
6. `double_free` 样本必须至少出现两次 release；
7. `use_after_free` 样本必须出现 release 后的 use；
8. 源码存在时，evidence 的文件、行号和 snippet 是否匹配。
