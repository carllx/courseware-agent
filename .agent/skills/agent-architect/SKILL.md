---
name: agent-architect
description: 创建、编辑和管理 Antigravity IDE 的三大扩展机制——Rule（被动约束）、Workflow（主动命令）、Skill（领域能力包）。当用户要求新增规则、创建工作流命令、构建新技能、修改现有扩展配置、或需要理解 .agent/ 目录体系时触发。也适用于：扩展机制审查、批量重构 frontmatter、迁移旧规则/技能到新项目。
---

# Agent Architect

创建和管理 Antigravity IDE 工作区的三大扩展机制的统一引擎。

## 三元诊断路由

收到扩展需求时，按以下决策树判定输出形态：

```
用户需求是什么？
  ├─ 被动约束（安全底线/代码风格/格式规范/审查前置检查……）
  │     → 🛡️ Rule Path — 输出 .agent/rules/rule_xxx.md
  ├─ 可复用的多步命令（部署/审计/导出/生成……）
  │     → ⚡ Workflow Path — 输出 .agent/workflows/xxx.md
  └─ 复杂领域知识包（含脚本/资产/渐进式披露/多文件……）
        → 🧩 Skill Path — 输出 .agent/skills/xxx/ 目录
```

**灰色地带判定**：
- 如果约束逻辑超过 150 行或需要脚本辅助 → 升级为 Skill
- 如果工作流只有单一检查步骤 → 降级为 Rule（`model_decision` 触发）
- 如果用户说"帮我创建一个 `/xxx` 命令" → Workflow Path

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
  ├─ 是 → always (慎用！持续占用上下文)
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

> **AGENTS.md 嵌套作用域**：AGENTS.md 可放置在子目录中，更深层的文件覆盖更浅层的指令。适用于 monorepo 或多课程工作区——每个子目录可携带针对性规则。

> **AGENTS.md 格式约束**：写入 AGENTS.md 的内容必须使用纯 Markdown，**禁止使用 Antigravity 独有的 Frontmatter 字段**（如 `trigger`、`globs`），否则其他 IDE 无法解析。需要精准触发的规则应沉淀至 `.agent/rules/`。

> Frontmatter 各字段规范 + Glob 防御性设计：见 [rule_frontmatter_spec.md](references/rule_frontmatter_spec.md)
> 可复用模板库：见 [rule_templates.md](references/rule_templates.md)

### 1.3 Rule Frontmatter 格式

```yaml
---
trigger: <always|model_decision|glob|manual>
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

Workflow 是可复用的多步任务模板，用户通过 `/命令名` 触发。存放于 `.agent/workflows/xxx.md`。

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

---

## §3 Skill 创建（领域能力包）

### 3.1 创建流程

根据复杂度选择对应模式：

#### 快速模式（代理自生成）

适用于快速原型化——用户在聊天中描述需求，代理直接生成 SKILL.md 及附属资源：

1. 用户描述技能目标（如"为我生成一个关于 Three.js + Vite 的技能"）
2. 代理创建 `.agent/skills/<skill-name>/` 目录
3. 代理生成 SKILL.md（含 frontmatter + 指令 body）
4. 代理按需生成 scripts/references/assets
5. 用户审查并迭代

> 此模式适合：新技术探索、个人项目、技能原型验证。

#### 工程模式（结构化创建）

适用于团队共享的高质量技能——需要完整的规划与验证：

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
---
```

**必需字段**：`name`（kebab-case，≤ 64 字符）+ `description`（≤ 1024 字符）。
**硬性约束**：`name` 的值**必须与其父目录名一致**（如 `my-skill/SKILL.md` 中必须写 `name: my-skill`），否则校验工具会报错。
**禁止字段**：Skill 的 frontmatter 中禁止使用 `trigger`/`globs`（那是 Rule 的字段）。

### 3.3 目录结构与存放位置

#### 全局技能 vs 项目技能

Antigravity 支持两个层级的技能目录，解决不同的复用需求：

| 层级 | 路径 | 适用场景 | 示例 |
|:---|:---|:---|:---|
| **全局** | `~/.gemini/skills/<skill-name>/` | 跨项目通用的框架/语言规范 | TypeScript 规范、React 最佳实践 |
| **项目** | `.agent/skills/<skill-name>/` | 当前项目专属的库/SDK/业务逻辑 | 内部 UI 组件库、特定 API 用法 |

> **选择原则**：如果一个技能适用于你使用的框架和语言（与项目无关），放全局目录；如果它针对当前应用或后端的特定库、SDK 及框架，放项目级目录。项目级技能会随代码仓库分发给团队成员，实现**分布式知识共享**。

#### 单个技能的内部结构

```
skill-name/
├── SKILL.md          # 必需 — 指令与指南
├── scripts/          # 可选 — 可执行脚本
├── references/       # 可选 — 按需加载的参考文档
└── assets/           # 可选 — 输出资产（模板/图片/字体）
```

### 3.4 懒加载机制与 Token 预算

**核心问题——上下文膨胀 (Context Bloat)**：将过多代码或文档塞入上下文窗口会浪费 Token 并降低模型理解能力。技能的设计哲学是**懒加载 (Lazy Loading)**——代理仅在判定技能与当前任务相关时才读取其内容，不相关的技能不占用任何上下文预算。

**三级渐进式加载系统**（实现懒加载的具体机制）：
1. **元数据** (name + description) — 始终在上下文中，代理据此判断是否需要读取该技能 (~100 词 = ~25 Token)
2. **SKILL.md body** — 技能触发后才加载 (500 行 = ~4K Token)
3. **Bundled resources** — 仅在 SKILL.md 指令引导下按需加载 (单次建议 < 8K Token)

**Token 估算**：英文 `字符数 / 4`；中文 `字符数 / 2`。

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
| S6 | 存放层级 | 全局技能放 `~/.gemini/skills/`，项目技能放 `.agent/skills/`，不可混放 |

### 3.6 开放技能生态（参考信息）

技能是一个开放标准。当用户明确要求查找或复用现有技能时，可参考以下资源：

| 资源 | 用途 |
|:---|:---|
| [agentskills.io](https://agentskills.io) | 官方规范文档（本文件规范基于此，最后验证：2026-04-15） |
| [skills.sh](https://skills.sh) | 社区技能目录，`npx skills add <owner/repo>` 安装 |
| [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills) | Google 官方技能仓库 |

> 注意：不要在每次创建技能时主动抓取这些资源（成本高、收益低）。仅在用户显式请求"查找现有技能"或"参考官方规范"时才访问。

---

## §4 通用禁止行为

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

---

## $5 Knowledge Items 协作

Antigravity 内置持久化知识系统（Knowledge Items, KI），由后台 Knowledge Subagent 从对话中自动提取。

**agent-architect 创建的扩展如何与 KI 交互**：

1. **KI 不是手动放文件就自动索引的**。存储路径 `~/.gemini/antigravity/knowledge/` 由系统管理。
2. **工作区 `.agent/knowledge/`**（如存在）是用户自管理的参考资料目录，不会被自动索引到 KI 系统。
3. **提升 KI 捕获率的编写策略**：
   - Rule/Skill 的 `description` 应包含明确的领域关键词
   - 在 Walkthrough 制品中标注关键架构决策，KI Subagent 更容易提取
4. **查询 KI**：Agent 在对话开始时收到 KI 摘要列表，可通过 `view_file` 读取 KI 制品

> 详细指南：见 [knowledge_items_guide.md](references/knowledge_items_guide.md)
