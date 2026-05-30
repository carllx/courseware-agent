# 🔗 Handoff：Bridge 已完全修复，附使用指南

> **来源**: `eddddda7` (myskills / Ruflo Bridge 调试)
> **目标**: `/Users/yamlam/Downloads/2025-2026-2 课程`
> **时间**: 2026-05-26T16:20 CST

---

## ✅ 验证结论：Bridge 代码已完全正确

经过完整的参数矩阵测试，所有三个修复均已生效：

```
正确参数 {type: "researcher", name: "revise-agent"}: ✅ 成功
缺少 type: ❌ Zod 校验拒绝 (type: Required)  ← 你遇到的就是这个
缺少 name: ❌ Zod 校验拒绝
中文名: ❌ 上游拒绝 (agentId 不允许中文)
```

## 🔴 你遇到的 `type: Required` 的原因

**不是 Bridge 的 bug，而是 Antigravity 在解析你的自然语言指令时没有正确构造参数。**

你输入的指令：
```
mcp ruflo_agent_spawn /revise 《信息可视化》 weeks/W04_AI_D3_Basics/src/
```

Antigravity 需要将其解析为：
```json
{
  "type": "researcher",
  "name": "revise-w04-agent"
}
```

但它可能解析为了不含 `type` 的格式，导致 Zod 校验报 `type: Required`。

---

## 📋 正确的使用方式

### 方式 1：明确指定参数（推荐）

告诉 Agent：

> 请调用 ruflo_agent_spawn，参数为 type="researcher"，name="revise-w04"

### 方式 2：让 Agent 自己构造

> 请创建一个 Ruflo researcher agent，命名为 revise-w04，用来审查 W04_AI_D3_Basics 目录

### ⚠️ 注意事项

1. **`name` 只能用英文** — 不能用中文、空格或特殊字符。允许的字符：`a-z A-Z 0-9 _ - . :`
2. **`type` 必须是以下之一**: `coder`, `researcher`, `analyst`, `architect`, `reviewer`, `custom`
3. **Antigravity 重启后第一次调用可能慢 3-5 秒**（Bridge 需要连接上游 Ruflo）

---

## 📌 关于 /revise 工作流

对方 Agent 的建议是正确的：**`/revise` 是 Antigravity 原生工作流，不需要通过 Ruflo Bridge 启动**。

Ruflo Agent 适合的场景是：
- 需要**跨会话持久化记忆**（ruflo_memory_store/search）
- 需要**多 Agent 集群协调**（ruflo_swarm_init）
- 需要**成本追踪**和**学习模式积累**

对于一次性的 `/revise` 审查任务，直接用 Antigravity 的原生 subagent 更高效。

## 🛠️ 建议 Skills

- **`handoff`** — 如有新问题继续回报
