# Workflow 格式规范

## 概述

Workflow 是可复用的多步任务模板，存放于 `.agent/workflows/` 目录下。用户通过 `/文件名`（不含 `.md` 后缀）触发。

---

## Frontmatter 结构

```yaml
---
description: <一句话说明该命令做什么>
---
```

唯一必需字段：`description`。

**示例：**

```yaml
---
description: 将脚本导出为 TTS 纯文本、审阅 Word 文档或词汇表
---
```

---

## Body 结构

正文使用标准 Markdown，按步骤编号组织：

```markdown
---
description: 审查脚本与课程配置的质量
---

## 前置条件
- 确认目标课程目录存在
- 确认 course.yaml 已配置

## 参数
- `--deep` — 执行深度审计（含 OBE 对齐和知识面覆盖率）
- `--quick` — 仅执行快速检查

## 步骤

1. 读取目标课程的 course.yaml
2. 扫描 scripts/ 目录下所有脚本文件
// turbo
3. 运行字段合规性检查
4. 生成审计报告
```

---

## 自动化注解

| 注解 | 位置 | 效果 |
|:---|:---|:---|
| `// turbo` | 某步骤的上一行 | 仅该步骤自动运行（`SafeToAutoRun: true`） |
| `// turbo-all` | 文件中任意位置 | 所有命令行步骤自动运行 |

**注意**：`// turbo` 仅适用于涉及 `run_command` 工具的步骤。

---

## 命名约定

| 事项 | 规范 |
|:---|:---|
| 文件名 | 全小写，下划线分隔，`.md` 后缀 |
| 触发命令 | `/文件名`（自动去除 `.md`）|
| 示例 | `audit.md` → 用户输入 `/audit` 触发 |

---

## 终端策略与 turbo 的关系

Antigravity IDE 支持配置 **Allow List / Deny List** 终端策略，控制 Agent 可自动运行的命令范围。

**`// turbo` 注解与终端策略的交互**：
- `// turbo` 将步骤的 `SafeToAutoRun` 设为 `true`
- 但如果命令不在 IDE 的 Allow List 中，仍需用户确认
- 反之，即使命令在 Allow List 中，没有 `// turbo` 注解的步骤默认仍需确认

**安全红线**：
- 禁止对破坏性命令使用 `// turbo`：`rm -rf`、`git push --force`、`drop table` 等
- 即使用户要求，也应在 Workflow 中标注警告注释而非直接 turbo

---

## 与其他机制的关系

| 场景 | 选择 |
|:---|:---|
| 被动约束，每次/条件自动注入 | → **Rule** |
| 主动命令，`/xxx` 触发 | → **Workflow** |
| 含脚本/资产的复杂领域包 | → **Skill** |

**Workflow 可以引用 Rule 和 Skill**——在步骤中 `@rule_name` 或调用 Skill 的脚本，但 Workflow 本身是轻量的编排层。
