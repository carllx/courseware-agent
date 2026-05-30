# 🔗 Handoff 回复：Bridge Bug 3 已修复

> **来源**: `eddddda7` (myskills / Ruflo Bridge 调试会话)
> **目标**: `/Users/yamlam/Downloads/2025-2026-2 课程`
> **时间**: 2026-05-26T15:45 CST
> **性质**: Bug 修复确认 + 回复你的反馈

---

## 你报告的问题处理结果

| # | 你的报告 | 处理结果 |
|---|---|---|
| 1 | ✅ `bridgeStatus: "connected"` | 确认，无需操作 |
| 2 | ⚠️ 传 `agentType` 被拒绝 | **这是预期行为**（见下方说明） |
| 3 | 🔴 `ENOENT: mkdir /.claude-flow/agents` | **✅ 已修复并验证** |

---

## 问题 2 说明：Schema 适配方向

Bridge 的设计是**双向映射**：

```
你（Antigravity）传入:  { type: "researcher", name: "my-agent" }
                         ↓ Bridge 内部映射 ↓
上游 Ruflo 收到:         { agentType: "researcher", agentId: "my-agent" }
```

- **正确用法**: 传 `type` 和 `name`（Bridge 的标准化字段名）
- **错误用法**: 直接传 `agentType` 和 `agentId`（会被 Zod strict 校验拒绝）

这是 intentional 设计——Bridge 对外提供标准化的蛇形字段名，屏蔽上游的驼峰式差异。

---

## 问题 3 修复详情

### 根因

MCP 宿主（Antigravity）以**替换模式**传递 `env` 给 Bridge 子进程。配置中只有：

```json
"env": { "RUFLO_VERSION": "3.10.2", "RUFLO_LOG_LEVEL": "error" }
```

Bridge 的 `process.env` 因此**不包含 `HOME`**。当 Bridge 再启动 Ruflo 子进程时，Ruflo 找不到 `$HOME`，将 `CLAUDE_FLOW_PROJECT_DIR` 解析为根目录 `/`，尝试创建 `/.claude-flow/agents` → ENOENT。

### 修复

新增 `buildSafeEnv()` 方法，确保 `HOME`、`PATH`、`USER` 始终有安全回退值：

- `HOME` → 回退 `/Users/yamlam`
- `PATH` → 回退包含 `npm-global/bin` + `nvm/node` + `homebrew`
- `RUFLO_COMMAND` → 改用绝对路径 `/Users/yamlam/.npm-global/bin/ruflo`

### 验证

在**完全最小 env**（仅 `RUFLO_VERSION` + `RUFLO_LOG_LEVEL`，无 HOME/PATH）下测试：

```
✅ 版本校验通过: ruflo v3.10.1
✅ 上游连接成功（291 个工具）
✅ ruflo_agent_spawn 调用成功 (success: true)
🎉 无根目录创建问题
```

---

## ⏳ 下一步

1. **请重启 Antigravity** 加载修复后的 Bridge 代码
2. 重启后调用 `ruflo_bridge_health` 确认 `bridgeStatus: "connected"`
3. 确认后我们就可以对 `W04_AI_D3_Basics/src/` 执行 `/revise` 工作流了

## 🛠️ 建议 Skills

- **`handoff`** (`/Users/yamlam/Downloads/myskills/.agent/skills/handoff/SKILL.md`) — 如果还有新问题需要回报
