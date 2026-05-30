# 预定义 Subagent 规格指南

## 概述

预定义 Subagent 允许在 Plugin 或工作区中声明**可复用的子代理**，每个 Subagent 拥有独立的系统提示词、工具权限和可选的模型配置。主 Agent 通过 `send_message` 与 Subagent 协作。

---

## agents/ 目录结构

Subagent 定义文件可放置在两个位置：

| 位置 | 路径 |
|:---|:---|
| Plugin 内 | `<plugin-dir>/agents/<agent-name>.md` |
| 工作区级 | `<workspace>/.agents/agents/<agent-name>.md` |

每个 `.md` 文件定义一个 Subagent，文件名即 Subagent 标识符。

```
agents/
├── researcher.md       # 研究型 Subagent
├── code-reviewer.md    # 代码审查 Subagent
└── translator.md       # 翻译 Subagent
```

---

## 定义文件格式

```yaml
---
name: researcher
description: 只读研究代理，负责信息收集和分析
model: gemini-2.5-pro
allowed-tools:
  - search_web
  - read_url_content
  - view_file
  - grep_search
workspace-mode: inherit
---

# Researcher Subagent

你是一名专业研究员。你的职责是：
1. 根据主 Agent 的指令搜索和收集信息
2. 将研究结果整理为结构化摘要
3. 通过 send_message 将结果返回给调用者

## 约束
- 仅执行只读操作，不修改任何文件
- 每次研究结果必须标注信息来源
```

### Frontmatter 字段

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---:|:---|
| `name` | string | ✅ | 标识符，kebab-case |
| `description` | string | ✅ | 一句话说明用途，供主 Agent 选择时参考 |
| `model` | string | 否 | 指定模型；缺省时继承主 Agent 的模型 |
| `allowed-tools` | string[] | 否 | 工具白名单；缺省时继承主 Agent 的全部工具 |
| `workspace-mode` | string | 否 | 工作区隔离模式（见下文），默认 `inherit` |

---

## Workspace 隔离模式

| 模式 | 行为 | 适用场景 |
|:---|:---|:---|
| `inherit` | 与主 Agent **共享**同一工作区视图（默认） | 常规协作任务 |
| `branch` | 在**隔离的 Git 分支**中工作，修改不影响主分支 | 实验性代码变更、重构探索 |
| `share` | 共享仓库但**独立工作目录** | 并行编辑不同文件集 |

> [!WARNING]
> `branch` 模式下，Subagent 的修改需要**显式合并**才能生效。任务完成后未合并的分支可能成为孤立分支。

---

## 嵌套深度限制

Subagent 可以继续调用其他 Subagent，形成嵌套链：

```
主 Agent → Subagent A → Subagent B → Subagent C → ...
```

> [!CAUTION]
> 当前嵌套深度**硬上限为 10 层**。超过限制时，`send_message` 调用将失败。实践中建议嵌套不超过 **3 层**，以控制延迟和上下文膨胀。

---

## 内置 Subagent 类型

Antigravity 提供以下预定义 Subagent 类型，无需手动配置即可使用：

| 类型 | 说明 | 工具权限 |
|:---|:---|:---|
| `research` | 只读研究代理 | 搜索、阅读、Grep 等只读工具 |
| `browser` | 浏览器交互代理 | Chrome DevTools MCP 工具集 |
| `self` | 主 Agent 的**完整克隆** | 继承全部工具和上下文 |

> [!TIP]
> `self` 类型适合将大任务**分治并行**——多个克隆同时处理不同子问题。但每个克隆消耗独立的 Token 配额。

---

## 安全继承

Subagent 的权限遵循**递减继承**原则：

1. 子代理的工具集 **≤** 父代理的工具集（只能缩减，不能扩展）
2. 文件系统访问范围继承自父代理的工作区配置
3. 终端策略（Allow List / Deny List）从父代理继承
4. API 密钥和 MCP 连接从父代理环境继承

---

## 常见陷阱

| 陷阱 | 说明 |
|:---|:---|
| 定义文件缺少 `description` | 主 Agent 无法判断何时调用该 Subagent |
| `allowed-tools` 为空列表 | 等同于**无任何工具**，Subagent 只能纯文本回复 |
| 嵌套过深导致超时 | 每层嵌套增加延迟，3 层以上需评估总时长 |
| `branch` 模式未合并 | 实验结果滞留在孤立分支中 |

---

## 质量检查表

| # | 检查项 | 标准 |
|:--|:---|:---|
| SA1 | Frontmatter 完整 | `name` + `description` 必须存在且非空 |
| SA2 | 工具权限最小化 | `allowed-tools` 仅列出该 Subagent 实际需要的工具 |
| SA3 | 系统提示词明确 | Body 中有清晰的角色定义、任务范围和输出格式要求 |
