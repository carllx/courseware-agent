# YAML Frontmatter 格式规范

## 基本结构

所有 `.agent/rules/*.md` 文件**必须**以 YAML frontmatter 开头：

```yaml
---
trigger: <触发模式>
description: <自然语言描述，用于模型判定和列表展示>
# 仅 glob 模式需要：
globs:
  - "<glob 模式 1>"
  - "<glob 模式 2>"
---
```

## 字段规范

### `trigger`（必需）

| 值 | 说明 |
|:---|:---|
| `always` | 每次对话都注入 |
| `model_decision` | 模型自主判断是否注入 |
| `glob` | 文件路径匹配时注入 |
| `manual` | `@rule_name` 显式引用时注入 |

### `description`（必需）

**质量要求**：

```
✅ 好的 description:
"当修改 course.yaml 的 objectives.mappings 或新增课程时，
 必须校验观测点命名与人培支撑矩阵的合规性。"

❌ 差的 description:
"课程工具配置规范"
```

撰写原则：
1. **说明触发条件**：「当 X 时」或「在 Y 场景下」
2. **说明核心行为**：「必须做 A」或「禁止 B」
3. **控制长度**：1-2 句话，≤ 100 字
4. **对 `model_decision` 尤其重要**：模型仅靠此字段判断是否激活

### `globs`（仅 `glob` 模式必需）

> [!CAUTION]
> **字段名必须是 `globs`（复数 + 列表格式）**。使用 `glob`（单数字符串）会导致匹配失效，规则永远不会被触发！

```yaml
# ✅ 正确
globs:
  - "*/weeks/*/src/*.md"

# ❌ 错误 — 字段名单数，且非列表格式
glob: "*/weeks/*/src/*.md"

# ❌ 错误 — 虽然字段名正确，但值不是列表
globs: "*/weeks/*/src/*.md"
```

---

## Glob 模式语法速查表

所有路径**相对于工作区根目录**匹配。

### 基础通配符

| 符号 | 含义 | 示例 | 匹配 | 不匹配 |
|:---:|:---|:---|:---|:---|
| `*` | 匹配**单层**内任意字符（不跨 `/`） | `*.md` | `README.md` | `src/README.md` |
| `**` | 匹配**任意深度**的路径段（含零层） | `**/*.md` | `README.md`、`a/b/c.md` | — |
| `?` | 匹配**恰好 1 个**字符 | `file?.txt` | `file1.txt` | `file10.txt` |

### 字符集与范围

| 符号 | 含义 | 示例 | 匹配 |
|:---:|:---|:---|:---|
| `[abc]` | 匹配 a、b 或 c | `[Rr]eadme.md` | `Readme.md`、`readme.md` |
| `[0-9]` | 匹配数字范围 | `W0[1-9]_*.md` | `W01_Intro.md` |
| `[!abc]` | **否定**——不匹配 a、b、c | `[!.]*.md` | `readme.md` 但不匹配 `.hidden.md` |

### 花括号展开

| 符号 | 含义 | 示例 | 等价于 |
|:---:|:---|:---|:---|
| `{a,b}` | 匹配 a **或** b | `*.{ts,tsx}` | `*.ts` 和 `*.tsx` |
| `{yaml,yml}` | 多扩展名 | `**/*.{yaml,yml}` | 所有 yaml/yml 文件 |

### 目录锚定

| 模式 | 含义 |
|:---|:---|
| `*/weeks/*/src/*.md` | 工作区根下**一级子目录**的 scripts/ 下的 .md |
| `**/weeks/*/src/*.md` | **任意深度**的 scripts/ 下的 .md |
| `src/**/*.js` | src/ 及其所有子目录下的 .js |

---

## 防御性 Glob 设计

> [!CAUTION]
> 以下三条策略旨在防止规则**静默失效**——即目录结构变更或脏文件出现时，Agent 不报错但不再执行约束。

### 策略 1：优先 `**/` 替代 `*/`

`*/` 仅匹配**恰好一层**子目录。一旦课程结构从 `课程名/practices/` 变为 `分类/课程名/practices/`，规则将静默失效。

```yaml
# ❌ 脆弱 — 目录层级变更后静默失效
globs:
  - "*/practices/*.yaml"

# ✅ 抗变更 — 任意嵌套深度都能锚定
globs:
  - "**/practices/*.yaml"
```

**例外**：仅当你**确信且有意**将匹配限定在恰好一层时才使用 `*/`，并在注释中说明理由。

### 策略 2：用字符集 `[0-9]` 收敛匹配范围

对有规范命名约定的文件（如 `W01_practice.yaml`），使用字符集约束避免匹配草稿、备份或临时文件。

```yaml
# ❌ 过度泛化 — draft.yaml、template.yaml 也会触发
globs:
  - "**/practices/*.yaml"

# ✅ 精确锁定 — 仅匹配 W01_*.yaml ~ W99_*.yaml
globs:
  - "**/practices/W[0-9][0-9]*.yaml"
```

### 策略 3：组合运用

```yaml
# 最佳实践：深度弹性 + 命名约束
globs:
  - "**/practices/W[0-9][0-9]*.yaml"  # 实践配置（精确）
  - "**/weeks/W[0-9][0-9]*/src/*.md"       # 课程脚本（精确）
```

## 约束

- 每个 .md 文件总大小 ≤ **12,000 字符**
- frontmatter 中**不使用** `name` 字段（那是 Skills 的字段）
- `description` 是**字符串**，不是列表
- `globs` 是**列表**（YAML array），不是字符串
- glob 路径相对于**工作区根目录**解析，不是相对于 `.agent/rules/` 目录

