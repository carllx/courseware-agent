# Plugin 规格指南

## 概述

Plugin 是 Antigravity IDE 的**顶层打包单元**，可将 Skill、Rule、MCP 服务器、Hook、Subagent 聚合为一个可分发的整体。最小化的 Plugin 仅需一个 `plugin.json` 文件。

---

## plugin.json 格式

```json
{
  "name": "my-plugin"
}
```

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---:|:---|
| `name` | string | 否 | 插件标识符，缺省时使用**目录名**作为名称 |

> [!NOTE]
> `plugin.json` 是 Plugin 的唯一必需文件。即使内容为空对象 `{}`，该文件也必须存在以标识目录为 Plugin。

---

## 目录结构

```
<plugin-name>/
├── plugin.json       # 必需 — 标识符
├── mcp_config.json   # 可选 — MCP 服务器定义（见 mcp_config_spec.md）
├── hooks.json        # 可选 — 生命周期钩子（见 hooks_spec.md）
├── skills/           # 可选 — 技能目录，结构同独立 Skill
├── rules/            # 可选 — 规则目录，结构同独立 Rule
├── agents/           # 可选 — 预定义 Subagent（见 subagent_spec.md）
└── sidecars/         # 可选 — 后台进程（见 sidecars_spec.md）
```

---

## 安装路径

| 级别 | 路径 | 优先级 |
|:---|:---|:---:|
| 工作区级 | `<workspace>/.agents/plugins/<name>/` | 高 |
| 全局级（IDE） | `~/.gemini/config/plugins/<name>/` | 中 |
| 全局级（CLI） | `~/.gemini/antigravity-cli/plugins/<name>/` | 低 |

> [!IMPORTANT]
> 工作区级 Plugin 优先于全局级。同名 Plugin 在多级别共存时，高优先级会遮蔽低优先级的同名资源。

---

## Plugin vs 独立 Skill 决策表

| 判断维度 | 选择 Plugin | 选择独立 Skill |
|:---|:---|:---|
| 需要捆绑 MCP 服务器 | ✅ | ❌ |
| 需要 Hook 拦截能力 | ✅ | ❌ |
| 需要预定义 Subagent | ✅ | ❌ |
| 仅含一套指令 + 脚本 | ❌ | ✅ |
| 需要跨 IDE 兼容 | ❌（Plugin 为 Antigravity 专有） | ✅（Skill 遵循开放标准） |
| 面向团队分发 | ✅ | 按需 |
| 包含后台 Sidecar 进程 | ✅ | ❌ |

> [!TIP]
> **经验法则**：如果你的扩展**仅**是一份 SKILL.md + scripts/，请保持独立 Skill 形态。只有当需要 MCP / Hook / Sidecar 等 Plugin 专属机制时，才将其包装为 Plugin。

---

## 常见陷阱

| 陷阱 | 说明 |
|:---|:---|
| 缺少 `plugin.json` | 目录不会被识别为 Plugin，其子资源不会被加载 |
| `name` 含大写或空格 | 推荐使用 kebab-case（如 `my-plugin`） |
| 嵌套 Plugin | Plugin 目录内不应再包含另一个 Plugin |
| 全局 Plugin 写入工作区文件 | 全局 Plugin 无权访问工作区文件系统，应使用持久数据目录 |

---

## 质量检查表

| # | 检查项 | 标准 |
|:--|:---|:---|
| P1 | `plugin.json` 存在 | 文件存在且为合法 JSON |
| P2 | 子目录命名 | `skills/`、`rules/`、`agents/` 等使用标准名称 |
| P3 | 内部 Skill 规范 | `skills/` 下每个子目录含合法 `SKILL.md` |
| P4 | 无冗余文件 | 不含 `.DS_Store`、`node_modules/` 等非必要文件 |
| P5 | 路径正确性 | 安装在三个合法路径之一，无路径拼写错误 |
