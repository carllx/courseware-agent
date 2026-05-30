# MCP 服务器配置指南

## 概述

MCP（Model Context Protocol）服务器为 Agent 提供**外部工具能力**。通过 `mcp_config.json` 配置远程 HTTP 服务器或本地命令行工具，Agent 即可调用第三方 API 和系统工具。

---

## mcp_config.json 格式

```json
{
  "mcpServers": {
    "server-name": {
      "serverUrl": "https://mcp.example.com/sse",
      "headers": {
        "x-api-key": "${MCP_API_KEY}"
      },
      "timeout": 30,
      "trustDomain": false
    }
  }
}
```

### 顶层字段

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `mcpServers` | object | 键为服务器名（kebab-case），值为服务器配置 |

### 服务器配置字段

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---:|:---|
| `serverUrl` | string | 二选一 | 远程 HTTP/SSE 端点 URL |
| `command` | string | 二选一 | 本地命令行工具路径 |
| `args` | string[] | 否 | `command` 模式的参数列表 |
| `headers` | object | 否 | HTTP 请求头（仅 `serverUrl` 模式） |
| `env` | object | 否 | 环境变量（仅 `command` 模式） |
| `timeout` | number | 否 | 请求超时秒数，默认 30 |
| `trustDomain` | boolean | 否 | 是否信任该域的 SSL 证书 |

---

## serverUrl vs command 模式

| 维度 | `serverUrl`（远程） | `command`（本地） |
|:---|:---|:---|
| 连接方式 | HTTP/SSE 长连接 | 子进程 stdin/stdout |
| 典型用途 | 云端 API 网关 | 本地 CLI 工具封装 |
| 需要网络 | ✅ | ❌ |
| 延迟 | 较高（网络往返） | 低（本地进程） |
| 认证 | 通过 `headers` 传递 API Key | 通过 `env` 注入凭据 |

```json
// 远程模式
{ "github": { "serverUrl": "https://api.github.com/mcp",
              "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" } } }
// 本地模式
{ "sqlite": { "command": "npx",
              "args": ["-y", "@anthropic/mcp-server-sqlite", "./data.db"] } }
```

---

## Eager vs Lazy 加载

| 模式 | 行为 | Token 开销 | 适用场景 |
|:---|:---|:---|:---|
| **Eager** | 会话开始时加载**全部**工具 schema | 高（每工具 ~200-500 Token） | 高频使用的核心工具 |
| **Lazy** | **按需**加载，触发关键词匹配后才加载 | 低（节省 90%+ Token） | 低频或大型工具集 |

> [!IMPORTANT]
> 一个含 20 个工具的 MCP 服务器，Eager 模式将消耗 **4,000-10,000 Token** 的上下文空间。对于大型工具集，强烈推荐 Lazy 模式。

**Token 估算**：单个工具 schema 约 200-500 Token。10 工具 Eager ≈ 2K-5K Token；20 工具 ≈ 4K-10K Token。

> [!TIP]
> Lazy 模式将开销降至仅 `instructions.md` 大小（通常 < 200 Token）。

### instructions.md 与 Lazy 触发

Lazy 模式下，每个 MCP 服务器目录可包含 `instructions.md`，内含**触发关键词**和最佳实践。IDE 据此判断何时按需加载工具 schema：

```
<serverName>/
├── <toolName>.json    # 工具 schema
└── instructions.md    # 触发关键词 + 调用规范
```

---

## 放置路径

| 位置 | 路径 | 说明 |
|:---|:---|:---|
| Plugin 内 | `<plugin-dir>/mcp_config.json` | 随 Plugin 分发 |
| 全局级 | `~/.gemini/config/mcp.json` | 所有工作区共享 |
| 工作区级 | `<workspace>/.agents/mcp.json` | 仅当前工作区生效 |

> [!NOTE]
> 多级别配置会**合并**（不覆盖）。同名服务器在多级别定义时，工作区级优先。

---

## 安全提醒

> [!CAUTION]
> API 密钥和敏感头信息的管理注意事项：

- ❌ 禁止将明文 API Key 提交到 Git 仓库
- ✅ 使用环境变量插值：`"x-api-key": "${MCP_API_KEY}"`
- ✅ 将密钥存储在 `.env` 文件中并加入 `.gitignore`
- ✅ 团队协作时使用密钥管理服务（如 1Password CLI、Vault）
- ⚠️ `trustDomain: true` 会跳过 SSL 验证——仅用于本地开发环境

---

## 常见陷阱

| 陷阱 | 说明 |
|:---|:---|
| `serverUrl` 和 `command` 同时指定 | 两者互斥，只能选其一 |
| 忘记环境变量插值语法 | 必须使用 `${VAR_NAME}` 格式，非 `$VAR_NAME` |
| Eager 加载过多工具 | 上下文被工具 schema 占满，影响 Agent 推理质量 |
| 本地 MCP 服务器未安装 | `command` 指向的程序需事先安装到 PATH 中 |
