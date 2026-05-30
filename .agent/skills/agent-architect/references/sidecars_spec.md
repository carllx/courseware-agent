# Sidecars 规格指南

## 概述

Sidecar 是 Antigravity IDE 的**后台常驻进程**，与主 Agent 会话并行运行。典型用途包括：文件监听、持续编译、本地服务器、数据同步等需要长时间运行的任务。

---

## sidecar.json 格式

```json
{
  "name": "file-watcher",
  "command": "node",
  "args": ["./watcher.js"],
  "env": {
    "WATCH_DIR": "${workspaceFolder}"
  },
  "restartOnCrash": true,
  "maxRestarts": 5
}
```

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---:|:---|
| `name` | string | ✅ | Sidecar 标识符（kebab-case） |
| `command` | string | ✅ | 启动命令 |
| `args` | string[] | 否 | 命令参数列表 |
| `env` | object | 否 | 环境变量；支持 `${workspaceFolder}` 插值 |
| `restartOnCrash` | boolean | 否 | 崩溃后自动重启，默认 `true` |
| `maxRestarts` | number | 否 | 最大重启次数，默认 5 |

---

## 发现路径

| 级别 | 路径 |
|:---|:---|
| 全局级 | `~/.gemini/config/sidecars/<name>/sidecar.json` |
| Plugin 级 | `~/.gemini/config/plugins/<pluginName>/sidecars/<name>/sidecar.json` |

> [!NOTE]
> Sidecar 目前仅支持全局级和 Plugin 级部署，不支持工作区级。

---

## 生命周期管理

```
IDE 启动 → 扫描 sidecar.json → 启动进程
                                   ↓
                              进程运行中 ←─── 崩溃重启（受 maxRestarts 限制）
                                   ↓
                           IDE 退出 → 终止进程
```

- **自动启动**：IDE 启动时自动发现并启动所有已注册 Sidecar
- **崩溃重启**：`restartOnCrash: true` 时，进程异常退出后自动重启
- **重启上限**：超过 `maxRestarts` 次后停止重启，记录错误日志
- **优雅关闭**：IDE 退出时发送 `SIGTERM`，等待 10s 后强制 `SIGKILL`

---

## 与主 Agent 通信：agentapi CLI

Sidecar 通过 `agentapi` 命令行工具与主 Agent 交互：

```bash
# 向主 Agent 发送消息
agentapi send-message "文件变更检测：src/index.ts 已更新"

# 读取 Agent 状态
agentapi get-status

# 向 Agent 会话注入上下文
agentapi inject-context "当前编译状态：成功"
```

> [!IMPORTANT]
> `agentapi` 仅在 Sidecar 进程的环境中可用，不可在普通终端中调用。

---

## 持久数据目录

每个 Sidecar 拥有独立的持久数据目录：

```
~/.gemini/antigravity/sidecar_data/<sidecarId>/
```

- 数据在 IDE 重启后保留
- `<sidecarId>` 由 `name` 字段自动生成
- 通过环境变量 `SIDECAR_DATA_DIR` 访问

---

## Sidecar vs Subagent vs Background Task 决策表

| 判断维度 | Sidecar | Subagent | Background Task |
|:---|:---|:---|:---|
| 运行时长 | 持续运行（伴随 IDE 生命周期） | 单次任务后退出 | 单次任务后退出 |
| 并发模型 | 独立进程 | Agent 上下文分支 | 当前会话的后台命令 |
| 通信方式 | agentapi CLI | send_message | stdin/stdout |
| 典型用途 | 文件监听、本地服务器 | 研究、浏览器操作 | 编译、测试 |
| 状态持久化 | ✅ 有专用数据目录 | ❌ 任务完成即销毁 | ❌ 任务完成即销毁 |
| 崩溃恢复 | ✅ 自动重启 | ❌ 需手动重试 | ❌ 需手动重试 |

> [!TIP]
> **经验法则**：需要「一直在跑」的进程 → Sidecar；需要「跑一次就完」的任务 → Subagent 或 Background Task。

---

## 常见陷阱

| 陷阱 | 说明 |
|:---|:---|
| 忘记处理 `SIGTERM` | Sidecar 应监听 `SIGTERM` 并优雅退出，否则可能丢失数据 |
| 日志无限增长 | 建议在 Sidecar 内实现日志轮转 |
| 端口冲突 | 多个 Sidecar 监听同一端口时会启动失败 |

---

## 质量检查表

| # | 检查项 | 标准 |
|:--|:---|:---|
| SC1 | JSON 合法性 | `sidecar.json` 可被 `jq .` 解析，必需字段齐全 |
| SC2 | 命令可用性 | `command` 指向的程序在系统 PATH 中存在 |
| SC3 | 信号处理 | 进程正确处理 `SIGTERM`，10s 内可优雅退出 |
