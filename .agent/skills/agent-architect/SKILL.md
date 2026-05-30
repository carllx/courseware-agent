---
name: agent-architect
description: 创建、编辑和管理 Antigravity IDE 的七大扩展机制——Rule（被动约束）、Workflow（主动命令）、Skill（领域能力包）、Plugin（多扩展打包）、Hook（工具调用拦截）、Sidecar（后台持久进程）、Subagent Definition（预定义子代理）。当用户要求新增规则、创建工作流命令、构建新技能、创建插件、配置 Hook/Sidecar/MCP、定义子代理、修改现有扩展配置、或需要理解 .agent/ 目录体系时触发。也适用于：扩展机制审查、批量重构 frontmatter、迁移旧规则/技能到新项目。
---

# Agent Architect

创建和管理 Antigravity IDE 工作区的七大扩展机制的统一引擎。

## 扩展机制诊断路由

收到扩展需求时，按以下决策树判定输出形态：

```
用户需求是什么？
  ├─ 被动约束（安全底线/代码风格/格式规范/审查前置检查……）
  │     → 🛡️ Rule Path — 输出 .agent/rules/rule_xxx.md
  ├─ 可复用的多步命令（部署/审计/导出/生成……）
  │     → ⚡ Workflow Path — 输出 .agent/workflows/xxx.md
  ├─ 复杂领域知识包（含脚本/资产/渐进式披露/多文件……）
  │     → 🧩 Skill Path — 输出 .agent/skills/xxx/ 目录
  ├─ 多扩展打包分发（含 MCP/Hooks/多 Skill/跨团队共享……）
  │     → 📦 Plugin Path — 输出 .agents/plugins/xxx/ 目录
  ├─ 工具调用前/后自动执行自定义脚本
  │     → 🪝 Hook Path — 输出 hooks.json 配置
  ├─ 后台持久进程（监控/定时任务/事件反应……）
  │     → 🔄 Sidecar Path — 输出 sidecar.json 配置
  └─ 预定义可复用的专业子代理
        → 🤖 Subagent Path — 输出 agents/ 目录
```

**灰色地带判定**：
- 如果约束逻辑超过 150 行或需要脚本辅助 → 升级为 Skill
- 如果工作流只有单一检查步骤 → 降级为 Rule（`model_decision` 触发）
- 如果用户说"帮我创建一个 `/xxx` 命令" → Workflow Path
- 如果需要将 Skill + Rule + Hook 组合分发 → 升级为 Plugin
- 如果需要持久后台运行而非一次性命令 → Sidecar（非 Workflow）

---

## §1 Rule 创建（被动约束）

### 1.1 需求分析

确认以下信息：
1. **约束什么行为**：这条规则要禁止/强制/引导什么操作？
2. **触发频率**：每次都需要？特定文件？特定操作？偶尔参考？
3. **与现有规则的关系**：是否可以合并？是否冲突？

**必须先扫描** `.agent/rules/` 下现有规则列表（仅读 frontmatter，不读 body），检查是否已有类似约束。

### 1.2 选择触发模式

```
需要对每个请求都生效？
  ├─ 是 → always (慎用！持续占用上下文。`always_on` 亦可，两者等效)
  └─ 否 → 与特定文件类型绑定？
            ├─ 是 → glob → 填写 globs 字段
            └─ 否 → 模型能从 description 判断相关性？
                      ├─ 是 → model_decision
                      └─ 否 → manual
```

### 1.2.1 跨工具兼容分流

Antigravity 支持**三层互补**的规则定义机制（v1.20.3+ 引入 AGENTS.md 支持，v1.21.6 强化）：

```
该规则的适用范围？
  ├─ 团队使用多种 AI IDE（Cursor / Claude Code / Copilot…）
  │     → 写入 AGENTS.md（跨工具基础层，纯 Markdown）
  ├─ 仅 Antigravity 需要，且需覆盖 AGENTS.md 中的通用规则
  │     → 写入 GEMINI.md（Antigravity 专属覆盖层）
  └─ 需要基于文件路径精准触发（glob / model_decision）
        → 写入 .agent/rules/rule_xxx.md（带 YAML Frontmatter）
```

> **官方优先级链**：System Rules（不可变）> `GEMINI.md` > `AGENTS.md` > `.agent/rules/`。三者互补而非互斥。

> **GEMINI.md 双层作用域**：全局级 `~/.gemini/GEMINI.md` 应用于所有工作区；工作区级 `<workspace>/GEMINI.md` 仅对当前项目生效，可覆盖全局设置。

> **AGENTS.md 嵌套作用域**：AGENTS.md 可放置在子目录中，更深层的文件覆盖更浅层的指令。适用于 monorepo 或多课程工作区——每个子目录可携带针对性规则。

> **AGENTS.md 模块化导入**：AGENTS.md / GEMINI.md 支持 `@/path/to/file.md` 语法导入其他指令文件，避免单文件过大。建议保持每个文件 100-300 行。

> **AGENTS.md 格式约束**：写入 AGENTS.md 的内容必须使用纯 Markdown，**禁止使用 Antigravity 独有的 Frontmatter 字段**（如 `trigger`、`globs`），否则其他 IDE 无法解析。需要精准触发的规则应沉淀至 `.agent/rules/`。

> Frontmatter 各字段规范 + Glob 防御性设计：见 [rule_frontmatter_spec.md](references/rule_frontmatter_spec.md)
> 可复用模板库：见 [rule_templates.md](references/rule_templates.md)

### 1.3 Rule Frontmatter 格式

```yaml
---
trigger: <always|always_on|model_decision|glob|manual>
description: 当<触发条件>时，<核心行为>。
# 仅 glob 模式需要：
globs:
  - "**/<pattern>"
---
```

**禁止字段**：Rule 的 frontmatter 中禁止使用 `name`（那是 Skill 的字段）。

### 1.4 Glob 陷阱速查

| 陷阱 | 错误写法 | 正确写法 |
|:---|:---|:---|
| 字段名单数 | `glob: "*.md"` | `globs:\n  - "*.md"` |
| 值非列表 | `globs: "*.md"` | `globs:\n  - "*.md"` |
| `*` 不跨目录 | `"*.md"` 期望匹配子目录 | `"**/*.md"` |
| 路径基准错误 | 相对于 rules/ 目录 | 相对于**工作区根目录** |
| `*/` 脆弱 | `"*/practices/*.yaml"` | `"**/practices/*.yaml"` |
| 过度泛化 | `"**/practices/*.yaml"` | `"**/practices/W[0-9][0-9]*.yaml"` |

### 1.5 Rule Body 结构

从 [rule_templates.md](references/rule_templates.md) 选择对应模板：

1. **标题**: `# 规则：<中文名> (<English Name>)`
2. **TL;DR** (glob 规则推荐): 2-3 行核心速记
3. **核心原则**: 1 句话 blockquote
4. **规则条目**: `§N` 编号分节
5. **禁止行为**: `❌` 前缀清单
6. **验证方法** (可选): 命令或检查表

### 1.6 Rule 质量检查

| # | 检查项 | 标准 |
|:--|:---|:---|
| Q1 | 文件大小 | ≤ 12,000 字符（≥ 80% 时发出预警） |
| Q2 | Frontmatter 合法性 | `trigger` 值为 4 种之一；`description` 非空且 ≤ 100 字；含触发条件 |
| Q3 | Glob 字段名 | `trigger: glob` 时字段名必须是 **`globs`**（复数），值必须是 **YAML 列表** |
| Q4 | Glob 模式有效性 | 无语法错误；路径相对于工作区根；`*` 与 `**` 使用正确 |
| Q5 | 命名规范 | 文件名 `rule_<功能域>.md`，全小写 + 下划线 |
| Q6 | 无冲突 | 不与现有规则矛盾或重复 |
| Q7 | 语言 | 标题中英对照，正文简体中文 |
| Q8 | 可操作性 | 每条规则是具体、可执行的，非模糊建议 |
| Q9 | 防御性 Glob | `*/` 已评估可否用 `**/` 替代；通配符范围已收敛 |
| Q10 | Token 预算 | `always` 规则：字符数 / 4 估算 Token，> 2000 Token 时预警并考虑降级 |

---

## §2 Workflow 创建（主动命令）

### 2.1 Workflow 概述

Workflow 是可复用的多步任务模板，用户通过 `/命令名` 触发。

**存放位置**（双级）：
| 级别 | 路径 | 说明 |
|:---|:---|:---|
| 工作区级 | `.agent/workflows/xxx.md` | 仅当前项目可用 |
| 全局级 | `~/.gemini/antigravity/global_workflows/xxx.md` | 所有工作区可用 |

> 详细格式规范：见 [workflow_spec.md](references/workflow_spec.md)

### 2.2 Workflow Frontmatter 格式

```yaml
---
description: <一句话说明该命令做什么>
---
```

仅需 `description` 字段。

### 2.3 Workflow Body 结构

```markdown
---
description: 将脚本导出为指定格式
---

## 前置条件
- 确认已有目标脚本文件

## 步骤
1. 读取目标脚本
2. 执行转换逻辑
// turbo
3. 输出结果文件
```

**自动化注解**：
- `// turbo` — 仅该步骤自动运行（无需用户确认）
- `// turbo-all` — 文件中任意位置出现一次，所有步骤自动运行

### 2.4 Workflow 质量检查

| # | 检查项 | 标准 |
|:--|:---|:---|
| W1 | Frontmatter | 必须含 `description` 字段 |
| W2 | 命名规范 | 文件名即命令名，全小写，用下划线 |
| W3 | 步骤明确性 | 每步有明确的动作动词和预期产物 |
| W4 | 幂等性 | 重复执行不应产生副作用 |
| W5 | 权限相容性 | 含 `// turbo` 的步骤所调用的命令，应在文档注释中提示用户将其加入 IDE Agent Permissions 的 **Allow List**，否则 `Request Review` 策略下自动执行会被拦截 |

---

## §3 Skill 创建（领域能力包）

### 3.1 创建流程

1. **理解需求** — 收集具体使用场景和示例
2. **规划资源** — 识别需要哪些 scripts/references/assets
3. **初始化** — 运行 `scripts/init_agent_extension.py <skill-name> --path <dir> --type skill`
4. **实现资源** — 编写脚本、参考文档、资产文件
5. **编写 SKILL.md** — 遵循渐进式披露原则
6. **打包验证** — 运行 `scripts/package_skill.py`

### 3.2 Skill Frontmatter 格式

```yaml
---
name: <kebab-case 名称>
description: <说明做什么 + 何时触发，中文撰写>
# 可选（实验性）——限制该 Skill 可调用的工具：
allowed-tools: Read Grep Glob Bash
---
```

**必需字段**：`name`（kebab-case，≤ 64 字符）+ `description`（≤ 1024 字符）。
**可选字段**：`allowed-tools`（实验性）——空格分隔的工具白名单，限制该 Skill 激活时 Agent 可调用的工具范围。
**禁止字段**：Skill 的 frontmatter 中禁止使用 `trigger`/`globs`（那是 Rule 的字段）。

> [!WARNING]
> **`allowed-tools` 安全边界**：`allowed-tools` 是安全隔离的**一个层次**，但**不替代沙箱和参数验证**。不同运行时（IDE vs CLI）对其实现严格度可能不同。最佳实践：研究型 Skill 应限制为只读工具（`Read Grep Glob`）。

### 3.3 目录结构与安装位置

Skill 可放置在三个位置（优先级由高到低）：

| 级别 | 路径 | 说明 |
|:---|:---|:---|
| Plugin 级 | `~/.gemini/config/plugins/<pluginName>/skills/<skill>/` | 跟随 Plugin 分发 |
| 工作区级 | `<workspace>/.agents/skills/<skill>/`（新标准）<br>`<workspace>/.agent/skills/<skill>/`（传统兼容） | 仅当前项目 |
| 全局级 | `~/.gemini/antigravity/skills/<skill>/` | 所有工作区 |

> **`.agent/` vs `.agents/` 迁移**：2026 年初起 `.agents/`（复数）成为跨工具标准目录名。IDE 仍向后兼容 `.agent/`（单数），本项目当前使用传统路径。迁移时仅需重命名目录，无需修改文件内容。新项目建议直接使用 `.agents/`。

```
skill-name/
├── SKILL.md          # 必需 — 指令与指南
├── scripts/          # 可选 — 可执行脚本
├── references/       # 可选 — 按需加载的参考文档
└── assets/           # 可选 — 输出资产（模板/图片/字体）
```

> **互操作性**：Antigravity 遵循 Agent Skills 开放标准，Skill 可跨 Claude Code、Cursor、GitHub Copilot 等 IDE 使用。编写时避免依赖 Antigravity 独有 API，以保持可移植性。

### 3.4 渐进式披露与 Token 预算

三级加载系统，节省上下文：
1. **元数据** (name + description) -- 始终在上下文中 (~100 词 = ~25 Token)
2. **SKILL.md body** -- 技能触发后加载 (500 行 = ~4K Token)
3. **Bundled resources** -- 按需加载 (单次建议 < 8K Token)

**Token 估算**：英文 `字符数 / 4`；中文 `字符数 / 2`。

> [!IMPORTANT]
> **MCP 工具的隐性 Token 开销**：Eager-loaded 的 MCP 工具 schema 在会话开始时自动注入 context，每个工具约消耗 200-500 Token。拥有 50+ 工具的 MCP 服务器可能吞噬 10K+ Token。设计 Plugin 时应优先使用 Lazy 加载策略，或将工具按需分组。

**关键原则**：
- SKILL.md body ≤ 500 行，超出时拆分到 references/
- 引用文件避免深层嵌套——所有 reference 从 SKILL.md 直接链接
- 超过 100 行的 reference 文件，顶部加目录（TOC）

> 设计模式参考：见 [skill_design_patterns.md](references/skill_design_patterns.md)

### 3.5 Skill 质量检查

| # | 检查项 | 标准 |
|:--|:---|:---|
| S1 | Frontmatter | `name` kebab-case，`description` 非空中文 |
| S2 | SKILL.md 体量 | ≤ 500 行 |
| S3 | 脚本测试 | scripts/ 下的脚本必须实际运行通过 |
| S4 | 无冗余文件 | 删除 README.md / CHANGELOG.md 等辅助文件 |
| S5 | 资源引用 | 所有 references 从 SKILL.md 有明确链接和加载时机说明 |

---

## §4 通用禁止行为

### 4.1 Rule / Workflow / Skill（经典三元）

- ❌ 创建 `always` 触发的规则而不确认用户知晓其上下文开销
- ❌ 在 `description` 中使用模糊语句如「通用规范」
- ❌ 创建超过 150 行的单条规则（应拆分或升级为 Skill）
- ❌ 在 Rule frontmatter 中使用 `name` 字段
- ❌ 在 Skill frontmatter 中使用 `trigger`/`globs` 字段
- ❌ 未扫描现有 Rules/Skills 就创建新的（可能导致重复或冲突）
- ❌ 使用 `glob:` (单数字符串) 代替 `globs:` (复数列表)
- ❌ 在 glob 模式中用 `*` 期望跨目录匹配（应使用 `**`）
- ❌ 假设 glob 路径相对于 `.agent/rules/` 目录（实际相对于**工作区根**）
- ❌ 生成全英文模板或注释（必须遵循用户语言协议：简体中文）
- ❌ 声称存在"魔法目录"可自动排除上下文（如 `/context/parked/`）——该机制不存在
- ❌ 在 Workflow 中对破坏性命令（`rm -rf`、`git push --force`）使用 `// turbo`
- ❌ 在写入 `AGENTS.md` 的内容中使用 Antigravity 独有的 Frontmatter 字段（`trigger`/`globs` 等）——其他 AI IDE 无法解析，应沉淀至 `.agent/rules/`
- ❌ 在 `.agent/scripts/` 或 Skill `scripts/` 中创建可直接覆写逐字稿正文的 Python 脚本（`open(path, 'w').write()` 模式写入 `src/M*.md`）——参照 `rule_security_governance.md` §6.1
- ❌ 在 Workflow 中用 `// turbo` 标注任何调用 Python 脚本覆写逐字稿内容的步骤

### 4.2 Plugin / Hook / Sidecar / Subagent / MCP（2.0 扩展）

- ❌ 创建 Plugin 但缺少 `plugin.json` 标识文件
- ❌ 在 Plugin 的 `rules/` 目录中写入带 Antigravity 独有 frontmatter 的规则——Plugin 规则应兼顾跨工具性
- ❌ 在 Hook 中执行破坏性操作（`rm -rf`、`git push --force`、`drop table`）
- ❌ 创建 Sidecar 但不配置崩溃恢复策略（Antigravity 默认自动重启，但脚本应具备幂等性）
- ❌ 定义 Subagent 的嵌套调用深度超过 10 层
- ❌ 将 API 密钥硬编码到 `mcp_config.json` 的 headers 中（应使用环境变量引用）
- ❌ 使用 Eager 加载策略配置拥有 50+ 工具的 MCP 服务器（将消耗 10K+ Token，应使用 Lazy）
- ❌ 将 Sidecar 和 Subagent 混淆——Sidecar 是持久后台进程，Subagent 是对话级并行代理

---

## §5 Knowledge Items 协作

Antigravity 内置持久化知识系统（Knowledge Items, KI），由后台 Knowledge Subagent 从对话中自动提取。

**agent-architect 创建的扩展如何与 KI 交互**：

1. **KI 不是手动放文件就自动索引的**。存储路径 `~/.gemini/antigravity/knowledge/` 由系统管理。
2. **工作区 `.agent/knowledge/`**（如存在）是用户自管理的参考资料目录，不会被自动索引到 KI 系统。
3. **提升 KI 捕获率的编写策略**：
   - Rule/Skill 的 `description` 应包含明确的领域关键词
   - 在 Walkthrough 制品中标注关键架构决策，KI Subagent 更容易提取
4. **查询 KI**：Agent 在对话开始时收到 KI 摘要列表，可通过 `view_file` 读取 KI 制品

> 详细指南：见 [knowledge_items_guide.md](references/knowledge_items_guide.md)

---

## §6 Plugin 创建（多扩展打包）

Plugin 是 Skill + Rule + MCP + Hook + Subagent 的**命名空间级容器**，用于将多个相关扩展打包分发。

### 6.1 最小 Plugin 结构

```
my-plugin/
├── plugin.json       # 必需 — {"name": "my-plugin"}（name 可选，缺省用目录名）
├── mcp_config.json   # 可选 — MCP 服务器定义
├── hooks.json        # 可选 — 生命周期钩子
├── skills/           # 可选 — 内含多个 Skill 目录
├── rules/            # 可选 — Rule 文件
└── agents/           # 可选 — 预定义 Subagent
```

### 6.2 安装路径

| 级别 | 路径 |
|:---|:---|
| 工作区级 | `<workspace>/.agents/plugins/<name>/` |
| 全局级（IDE） | `~/.gemini/config/plugins/<name>/` |
| 全局级（CLI） | `~/.gemini/antigravity-cli/plugins/<name>/` |

### 6.3 Plugin vs 独立 Skill 决策

| 需求特征 | 推荐 |
|:---|:---|
| 单一领域知识包 | → Skill |
| 需要 MCP 工具 + Hook 联动 | → Plugin |
| 需要跨团队/跨项目分发 | → Plugin |
| 包含预定义 Subagent | → Plugin |

> 详细规格：见 [plugin_spec.md](references/plugin_spec.md)

---

## §7 Hooks 配置（工具调用拦截）

JSON Hooks 允许在 Agent 的工具调用或模型推理前后自动执行自定义 shell 脚本。

### 7.1 生命周期阶段

| 阶段 | 触发时机 |
|:---|:---|
| `before_tool_call` | 工具调用前拦截 |
| `after_tool_call` | 工具调用后 |
| `before_model_call` | 模型推理前 |
| `after_model_call` | 模型推理后 |
| `on_loop_stop` | Agent 循环停止时 |

### 7.2 配置位置

Hooks 通过 `hooks.json` 配置，可放置于：
- Plugin 目录内（`<plugin>/hooks.json`）
- 全局级（`~/.gemini/config/hooks.json`）

> 详细规格：见 [hooks_spec.md](references/hooks_spec.md)

---

## §8 Sidecars 配置（后台持久进程）

Sidecars 是与主 Agent 并行运行的后台进程，适用于持久监控、定时任务和事件驱动工作流。

### 8.1 核心特性

- **自动生命周期管理**：Antigravity 自动启动、崩溃后自动重启
- **agentapi CLI 通信**：Sidecar 通过 `agentapi`（自动注入 PATH）与主 Agent 交互
- **持久数据存储**：`~/.gemini/antigravity/sidecar_data/<sidecarId>/`

### 8.2 发现路径

| 级别 | 路径 |
|:---|:---|
| 全局级 | `~/.gemini/config/sidecars/` |
| Plugin 级 | `~/.gemini/config/plugins/<pluginName>/sidecars/` |

> 详细规格：见 [sidecars_spec.md](references/sidecars_spec.md)

---

## §9 Subagent 定义（预定义子代理）

除运行时 `define_subagent` 动态创建外，还可在 Plugin 或工作区中**预定义**可复用的 Subagent。

### 9.1 定义位置

| 级别 | 路径 |
|:---|:---|
| Plugin 级 | `<plugin>/agents/` |
| 工作区级 | `<workspace>/.agents/agents/` |

### 9.2 内置 Subagent 类型

| 类型 | 能力 |
|:---|:---|
| `research` | 只读工具，探索代码库 |
| `browser` | 浏览器交互 |
| `self` | 完整克隆父 Agent |

### 9.3 Workspace 隔离模式

| 模式 | 行为 |
|:---|:---|
| `inherit` | 共享父工作区（默认） |
| `branch` | 创建隔离分支 |
| `share` | 共享底层仓库（类似 git worktree） |

> [!WARNING]
> Subagent 嵌套调用深度上限为 **10 层**。超出将被系统拒绝。

> 详细规格：见 [subagent_spec.md](references/subagent_spec.md)

---

## §10 MCP 服务器配置

`mcp_config.json` 用于连接外部工具服务器（Model Context Protocol）。

### 10.1 配置格式

```json
{
  "mcpServers": {
    "server-name": {
      "serverUrl": "https://...",
      "headers": {"x-api-key": "${ENV_VAR}"}
    }
  }
}
```

### 10.2 加载策略

| 策略 | 优点 | 缺点 |
|:---|:---|:---|
| **Eager** | 工具立即可用 | 每个工具 ~200-500 Token |
| **Lazy** | 节省 90%+ Token | 需配置触发关键词 |

> 详细规格：见 [mcp_config_spec.md](references/mcp_config_spec.md)
