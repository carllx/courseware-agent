---
trigger: glob
description: 当编辑脚本或知识库文档时，强制执行 SSOT 职责边界，防止 Slide 定义、课程结构等信息越界。
globs:
  - "**/weeks/*/src/*.md"
  - "**/weeks/*/package.yaml"
  - "**/knowledge/**"
---

# 规则：文档职责边界协议 (Document Boundary Protocol)

**生效范围**: 所有课程的内容文档。

## 1. 核心原则 (SSOT)

> **每种信息只能在一个地方定义，其他地方只能引用。**

> **消费者导向 (ADR 007)**：决定数据归属时，必须先分析「谁消费这些数据」。如果数据的消费者不在该文件的主要处理链路上（如教案字段对脚本写作工作流无用），该数据不应存储在此文件中，以避免 Agent 处理时的 Token 浪费。

## 2. 通用职责划分

| 文档 | 唯一职责 | 允许引用 | 禁止包含 |
|:---|:---|:---|:---|
| `scripts/00_structure_map.md` | 课程结构、时间轴、教学节奏 | Slide ID | ❌ 视觉设计、Slide 定义 |
| `scripts/Sxx_*.md` / `scripts/Wxx_*.md` | 逐字稿、演示动作、**Slide 内联定义** | Asset 路径 | ❌ 课程结构、❌ 教案索引字段 |
| `course.yaml` calendar[] | 教案索引字段 SSOT：`supported_objectives`(list)、`task`(str)、`lessons[].steps`；大纲字段：`teaching_requirements`(str\|dict, ADR 008)、`focus`/`difficulty`/`ideology`/`teaching_method`(str) | frontmatter 结构数据 | ❌ 逐字稿内容 |
| `practices/experiment_planning.md` | 实验任务详情层（目标/工具/交付物/周次等） | - | ❌ 定义成绩权重、实验名称（SSOT 在 course.yaml） |
| `knowledge/` | 教材、术语、教纲 | - | ❌ 课程结构、视觉设计 |

> **⚠️ 关键变更**: `visuals/slide_database.md` 已取消。所有 Slide 定义的 SSOT 是 Script 文件中的 `> [VISUAL]` 块。

## 3. Slide 定义规范

Slide 使用 `> [VISUAL]` 块内联定义在 Script 中：

```markdown
> [VISUAL]
> *   **Slide**: `S01_Timeline_Matrix`
> *   **Layout**: `Diagram`
> *   **Scene**: 三阶段实习时间轴与关键任务对比图
```

**必填字段**: `Slide`（ID）、`Layout`（排版类型）、`Scene`（画面描述）
**推荐字段**: `Asset`（资产文件相对路径）、`Text`（画面主要文字）
**可选字段**: `Caption`（副标题/图注）、`List`（列表数据）、`Lang`（画面文字语言，默认 `zh-CN`）

## 4. 实验教学外键关联规范 (Experiment Keys)

> **核心原则**：所有实践活动必须能够严格回溯到 `course.yaml` 中定义的顶级实验。执行链条为：**`course.yaml` (最高权重，定义参数) -> `practices/experiment_planning.md` (定义细则) -> `scripts/` 内的 `[ACTIVITY]` (通过 `experiment_id` 强制投射关联)**。

在使用 `> [ACTIVITY]` 块定义实验操作或实训时，**强制**包含 `experiment_id` 字典，以标明此操作隶属其宏观主线架构。

```markdown
> [ACTIVITY]
> *   **Type**: `Practice`
> *   **Duration**: `15min`
> *   **experiment_id**: `2`   ← 强制外键关联
> *   **Desc**: 实验详情描述...
```

## 5. 引用规范

### Slide 引用（知识标签中引用同脚本内已定义的 Slide）
```markdown
✅ 正确: 在知识标签后紧跟 > [VISUAL] 块
❌ 错误: 在知识标签中直接写视觉设计描述
```

### 资产引用
```markdown
✅ 正确: > **Asset**: `S02_Phase1_Purify/S02_NoisePrint_cap.png`
❌ 错误: 加载 `../../some/hard/coded/path.wav`
```

## 6. 禁止行为

1. ❌ 在结构文档 (`00_structure_map.md`) 中写 Slide 定义
2. ❌ 在同一脚本中重复定义相同 Slide ID
3. ❌ 在脚本中硬编码绝对资产路径
4. ❌ 维护独立的 `slide_database.md` 文件（已废弃）
5. ❌ 在 `practices/` 中重复定义在 `course.yaml` 中已有字段的副本（如计分比例）
6. ❌ 在脚本 frontmatter 中存储教案索引字段（`supported_objectives`/`task`/`steps`），这些字段的 SSOT 在 `course.yaml`（ADR 007）

## 7. 评分体系 SSOT 规范 (Assessment Naming Convention)

> **核心原则 (ADR 005)**：`course.yaml` 中的评分项命名与描述必须符合教务审查规范。

### 7.1 `assessment_methods.normal_items`

- **`name`**：格式为 `章节测试N` 或 `命题测试N`。❌ 禁止使用 `实验N（实验名称）` 格式（含括号、内嵌实验名称）。
- **`desc`**：必须以 `对应实验N「实验名称」。考核要求：` 开头，先声明外键关联，再给出具体考核指标。

### 7.2 `exams`

- `exams` 节点为**必填**。即使是考查课也必须填写，否则 Jinja 模板渲染会报错 `'exams' is undefined`。
- `exams.final_exam[].sections[].questions[].content` 同样遵循 `对应实验N「...」。考核要求：` 的描述结构。

