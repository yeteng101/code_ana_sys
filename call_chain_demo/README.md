# 函数调用链接口 Demo

这是第一组（代码逆向分析）与第三组之间 JSON 契约的可运行 Demo。第三组提交已经定位好的函数目标，本服务查询内置 CRG fixture，返回调用者、被调用者、回调边、间接调用候选、证据、置信度和覆盖率。

当前 Demo **不查询 PR diff、不判断缺陷、不生成 Patch**，职责边界与《第一组—第三组函数调用链 JSON 接口规范》一致。

## 运行

项目只使用 Python 标准库，不需要安装依赖：

```bash
cd /Users/andye/Documents/ChatGPT/8.18huawei
python3 -m call_chain_demo.server --port 8080
```

健康检查：

```bash
curl http://127.0.0.1:8080/health
```

同步调用（便于联调）：

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  --data-binary @call_chain_demo/examples/redis-request.json \
  http://127.0.0.1:8080/api/v1/call-chains
```

异步调用（贴近正式接口）：

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  --data-binary @call_chain_demo/examples/libuv-request.json \
  http://127.0.0.1:8080/api/v1/analyze

curl http://127.0.0.1:8080/api/v1/runs/<run_id>
```

查询真实 Clang 流水线产物（`demo/graph.json`）：

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  --data-binary @call_chain_demo/examples/clang-request.json \
  http://127.0.0.1:8080/api/v1/call-chains
```

拉取接口契约：

```bash
curl http://127.0.0.1:8080/api/v1/schemas/call-chain-request
curl http://127.0.0.1:8080/api/v1/schemas/call-chain-result
```

## 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| POST | `/api/v1/call-chains` | 同步查询调用链，直接返回完整结果 |
| POST | `/api/v1/analyze` | 异步提交，立即返回 `run_id` |
| GET | `/api/v1/runs/{run_id}` | 查询异步运行结果 |
| GET | `/api/v1/schemas/call-chain-request` | 获取请求 Schema |
| GET | `/api/v1/schemas/call-chain-result` | 获取结果 Schema |

## Demo 数据与真实 Clang 的关系

现在的 `fixtures/redis.json` 与 `fixtures/libuv.json` 模拟 03-callgraph 阶段的 CRG 产物，用于验证接口、路径查询和错误处理。后续接入 Clang 时，只需把 `FixtureGraph.load_for_repository()` 替换为读取 Clang 生成的 `graph.json`，HTTP 请求与返回格式不用改变。

fixture 中的源码行号是演示数据，不能作为真实 libuv/Redis 版本的源码证据；返回体会明确携带这一警告。

真实 Clang 流水线已经在本仓库落地：`clang_pipeline/` 会解析 `demo/sample/` 的 C++ 代码，跑 7 个阶段并把带证据的 `graph.json`、`report.md`、`graph.mmd` 发布到 `demo/`。本服务会把 `demo/graph.json` 适配为 CRG 图，`repository.name=clang-pipeline-demo` 时返回真实 Clang 证据；libuv / Redis fixture 仍保留作为 HTTP 契约回归。

## 测试

```bash
python3 -m unittest discover -s call_chain_demo/tests -v
```

测试覆盖同步/异步接口、幂等、目标解析、正反向调用链、回调过滤、间接调用候选、证据引用、节点/边连续性、置信度和路径安全。
