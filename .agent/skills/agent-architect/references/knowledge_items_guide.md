# Knowledge Items (KI) 指南

## 概述

Knowledge Items 是 Antigravity IDE 的持久化记忆系统。后台 Knowledge Subagent 自动从对话中提取关键信息，生成结构化的 KI 条目。

## 存储层级

| 层级 | 路径 | 管理者 | 自动索引 |
|:---|:---|:---|:---:|
| 全局 KI | `~/.gemini/antigravity/knowledge/` | 系统（Knowledge Subagent） | 是 |
| 工作区参考 | `.agent/knowledge/` | 用户手动 | 否 |

> **注意**：往 `.agent/knowledge/` 放文件不会被 KI 系统自动索引。该目录仅作为 Agent 的参考资料来源。

## KI 结构

每个 KI 由系统自动生成，包含：
- `metadata.json` — 标题、摘要、时间戳、原始来源引用
- `artifacts/` — 相关文档、代码示例、用户指令记录

## 与 Agent Architect 的交互

### 创建 Rule/Skill/Workflow 时

1. **先查 KI**：开始任何创建工作前，检查 KI 摘要列表中是否已有相关主题
2. **写高质量 description**：包含明确领域关键词，帮助 KI Subagent 未来关联
3. **在 Walkthrough 中标注关键决策**：例如"为什么选择 `glob` 而非 `model_decision`"

### 迁移到新项目时

KI 是全局的（存在用户主目录下），跨项目共享。但 `.agent/` 目录下的文件需要手动迁移。`init_agent_extension.py` 可以辅助在新项目中重建 Rule/Workflow/Skill 骨架。

## 常见误区

| 误区 | 真相 |
|:---|:---|
| "把文件放到 `.agent/knowledge/` 就会被自动索引" | 不会。KI 由 Knowledge Subagent 从对话中提取 |
| "KI = 用户手写的笔记" | KI 是系统自动生成的结构化知识，不是用户笔记 |
| "`/context/parked/` 可以停放无关文件" | 该路径不存在，Antigravity 无此机制 |
