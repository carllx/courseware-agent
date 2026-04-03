---
name: script-format
description: 定义课程逐字稿的格式规范与标签体系。当 Agent 执行 /write 工作流撰写脚本时，自动参照本规范。依赖 rule_narrative_standards.md 和 rule_localization.md。
---

# 技能：脚本格式规范 (Script Format)

## TL;DR (预检阶段专用，≤ 150 字)

脚本格式核心：Visual-First 双轨（先 VISUAL 后 Speech）→ 知识标签（技术层+人文层）→ ACTIVITY 块。Slide 内联定义于 `> [VISUAL]` 块（Slide/Layout/Scene 三必填）。视觉密度底线: 每模块 Slide ≥ ⌈讲授净分钟÷3⌉，连续 >360 字无 VISUAL 禁止。人文标签密度: 每模块口头型标签 ≥ ⌈字数预算÷2000⌉。完整规范见下文各节。

## 描述

定义课程逐字稿的**格式标准**：包括 Visual-First 双轨结构、知识标签体系、`[VISUAL]` 块字段规范、`[ACTIVITY]` 块规范和质量检查清单。

> [!IMPORTANT]
> 本文件是格式规范的**唯一真相源 (SSoT)**。
> `/write` 工作流负责编排（何时做），本文件负责规范（怎么做）。
> `/audit` 工作流基于本文件中的规则进行审计。

---

## 1. Visual-First 双轨结构

1.  **Define**: 先定义 `> [VISUAL]` 块。
2.  **Anchor**: 后续 Speech 必须通过**指示性词汇** (如"如图"、"左侧") 锚定画面内容 (See `rule_narrative_standards.md`).
3.  **Bullet Sync (要点同步)**: 当 Speech 中出现**结构化要点**（≥3 个并列项、阶段划分、评分/考核/任务说明等），紧邻的 `> [VISUAL]` 块**必须**包含 `**List**` 字段，将关键要点同步显示在 PPT 上。严禁出现"讲了但 PPT 上看不到"的信息断层。
4.  **Intent Alignment (意图对齐)**: `[VISUAL].Scene` 的描述必须与其后续 Speech 段落共享同一个**认知意图**（而非表层实体名词）。在抽象风格系统（如 Dada/Bauhaus）下，Scene 使用隐喻/情绪/张力来表达此意图；在具象风格系统下，Scene 可直接引用 Speech 中的实体对象。
    - 写作时的自检问句：「如果学生同时看到这张图、听到这段话，他们能否感受到**同一种情绪或认知张力**？」
    - 若答案为否，必须调整 Scene 或 Speech 之一使两者对齐。
    - **不可能三角警示**：在抽象风格系统下，严禁为了对齐而违反 `rule_visual_generation.md` §6.6（具象禁令）。正确做法是提取 Speech 中案例的**心理学内核**（如"被信息淹没的焦虑"、"新旧断裂的冲击"），将其映射为抽象视觉张力。

---

## 2. 知识标签体系

标签服务于**知识面的规范化**——确保课程触及技术深度与人文广度。

**技术层**:
*   `> [TECH NOTE]` — 技术原理、参数说明
*   `> [WARNING]` — 操作风险、常见错误
*   `> [DID YOU KNOW]` — 冷知识、科普趣闻

**人文层** (触发深度 Web 调研):
*   `> [STORY TIME]` — 比喻、寓言、经典故事
*   `> [PHILOSOPHY]` — 哲学思辨、认知科学
*   `> [CASE STUDY]` — 行业案例、历史事件、文化现象
*   `> [LIFE CONNECT]` — 日常生活、地域文化、流行文化

**教学层**:
*   `> [TEACHING MOMENT]` — 核心教学金句、顿悟时刻

**静默层** (不朗读):
*   `> [VISUAL]` — 画面描述 + Slide 内联定义
*   `> [PACING]` — 节奏控制（留白/加速）

### 人文层标签调研指引

1.  **Term Check**: 先使用 `librarian` 技能查阅教材定义，确保术语准确性。
2.  **Deep Dive**: 当使用人文层标签时，Agent **必须**激活 `narrative_archaeologist` skill 执行深度调研。
3.  详细的搜索策略、三轮搜索协议、调研备忘录格式和质量过滤标准见该 Skill 文档。

### 知识标签 + Slide 引用关联

知识标签自身**不是** `[VISUAL]`，但可以紧跟一个 `[VISUAL]` 块：

```markdown
> [CASE STUDY: 银翼杀手的混响设计]
> 配乐大师 Vangelis 使用 Lexicon 224 创造了"心理上的雨夜"……

> [VISUAL]
> *   **Slide**: `S04_BladeRunner_City`
> *   **Layout**: `Image`
> *   **Scene**: 银翼杀手 (1982) 霓虹雨夜城市全景
> *   **Search**: `Blade Runner 1982 city rain neon cinematography`
```

---

## 3. `[VISUAL]` 块规范

所有 Slide 直接在 Script 的 `> [VISUAL]` 块中定义。**不再使用集中式 `slide_database.md`**。

### 字段规范

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `Slide` | ✅ | Slide 标题（中文），兼作模块内唯一标识 |
| `Layout` | ✅ | PPT 排版类型 |
| `Scene` | ✅ | 画面的中文描述 |
| `Text` | 可选 | Slide 标题文字 |
| `List` | 可选 | 列表内容 |
| `Action` | 可选 | 画面中的操作动作 |
| `Asset` | 可选 | 物理图片核心字段。**推荐直接使用 MD 图片语法**（例：`![预览](../visuals/assets/...)`），IDE 可直接显示内联预览图，底层引擎会自动剥壳静默提取纯路径（零冗余机制）。 |
| `Asset N` | 可选 | 多图时使用编号后缀（`Asset 1`, `Asset 2`, ...），格式同上，全部归入 `assets[]` 数组 |
| `Resource` | 可选 | 辅助参考图片路径，格式同上，归入 `assets[]` 数组 |
| `AI_Prompt` | 可选 | AI 文生图 Prompt |
| `Search` | 可选 | 网络搜索关键词 |
| `Caption` | 可选 | 注释/引用文字 |

> [!TIP]
> **Asset 路径写法容错**：以下写法均会被解析器自动正规化为纯净相对路径：
> - 新架构: `assets/slides/S00.png`（相对于教学周目录）
> - 新架构 MD: `![预览](assets/slides/S00.png)`
> - 旧架构: `visuals/assets/W01/img.png`（相对于课程根目录）
> - 旧架构 MD: `![描述](../visuals/assets/W01/img.png)`
> - 反引号:  `` `visuals/assets/W01/img.png` ``
> - 双引号: `"visuals/assets/W01/img.png"`

### Layout 排版类型

详见 [pptx/layouts.md](../pptx/layouts.md) (Single Source of Truth)。

| Layout | 定义 | 渲染函数 |
|:---|:---|:---|
| `Title` | 封面/开场页 | renderTitle |
| `Section` | 章节过渡页 | renderTitle |
| `Agenda` | 议程/大纲 | renderList |
| `Split` | 双栏（文+图）| renderSplit |
| `Icons` | 图标+文字行 | renderList |
| `Grid` | 2×2/2×3 卡片网格 | renderGrid |
| `Full` | 全屏沉浸/大图叠字 | renderImage |
| `Table` | 精简表格 | renderList |
| `Comparison` | 对比列 | renderGrid |
| `Dashboard` | KPI 仪表盘 | renderGrid |
| `Stat` | 巨型数字聚焦 | renderTitle |
| `Timeline` | 时间线/流程 | renderDiagram |
| `Poll` | 投票/QR 互动 | renderImage |
| `Workshop` | 练习/工坊引导 | renderList |
| `Quote` | 金句卡片 | renderSplit |
| `CTA` | 行动号召/致谢 | renderTitle |
| `Code` | 代码展示 | renderSplit |
| `Diagram` | 流程图/逻辑图 | renderDiagram |
| `Image` | 单张大图+标题 | renderImage |
| `Screenshot` | 软件界面截图 | renderImage |
| `List` | 列表/要点 | renderList |

> ⚠️ `Card`, `Cards`, `Full Screen`, `CodeBlock`, `Triple-Column`, `Quadrant`, `Flow`, `Canvas`, `Chat-Bubble`, `Template-Card`, `Spectrum`, `Text`, `Chart`, `Video` 已弃用。详见 `layouts.md` 弃用别名表。

---

## 4. `[ACTIVITY]` 块规范

`lecture` / `workshop` 模式下强制执行：

- 每 **60-90 分钟**的讲授内容后必须插入至少 **1 个** `> [ACTIVITY]` 块
- 活动总时长须与理论讲授时长之和符合课程的计划学时

### 字段规范

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `Type` | ✅ | 活动类型：`Practice` / `Discussion` / `Workshop` / `Quiz` / `QA` / `Demo` / `Warm-up` |
| `Duration` | ✅ | 时长，如 `30min` |
| `Desc` | ✅ | 活动名称或简述 |

```markdown
> [ACTIVITY]
> *   **Type**: `Practice`
> *   **Duration**: `30min`
> *   **Desc**: 活动名称或简述
> 活动操作说明…
```

### 4.5 字数预算标注规范 (ADR 020)

> `/write` Step 2.8 生成的字数预算，以 HTML 注释形式嵌入脚本骨架。

**格式**：
```markdown
<!-- BUDGET: 4500 chars | STATUS: pending -->
<!-- BUDGET: 3600 chars | STATUS: done -->
```

**规则**：
- `BUDGET` 值为该模块的目标中文讲授字数（基于教案 `steps[].minutes` x 语速常量）
- `STATUS` 在分段写作过程中由 Agent 维护：`pending` → `done`
- 此注释**不影响** PPT/TTS 导出（被解析器自动忽略）
- 脚本完成后可保留或删除，不影响任何下游流程

---

## 5. 叙事规范

*   将枯燥的技术定义转化为生动的比喻。
*   每 3 分钟设计一个留白 `**(Pause: 3s)**`。
*   遵循 `rule_narrative_standards.md`（过渡焊接、韵律句法、反翻译腔）。
*   遵循 `rule_localization.md` 语言协议。

---

## 6. 视觉密度标准 (Visual Density Standard)

> **理论基础**：Mayer 多媒体学习认知理论（CTML）指出学习者通过视觉+听觉双通道处理信息，但每通道容量有限。视觉材料应以**概念切换为驱动**，而非按时间均匀分配。每个视觉都必须回答："这张图帮助学生理解了什么？"

### 6.1 视觉切换触发规则

满足以下**任一条件**即应插入新的 `> [VISUAL]` 块：

| 触发条件 | 说明 |
|:---|:---|
| 新概念引入 | 每个独立认知目标/术语首次出现时 |
| 举例/类比 | 使用案例、比喻、类比解释时 |
| 流程/步骤 | 涉及多步骤流程、操作链路时 |
| 数据/对比 | 展示数据、对比分析、正反对照时 |
| 连续叙述超限 | 连续口述 **>120 秒**（约 360 字）无视觉变化时 |

### 6.2 量化参考

| 指标 | 建议范围 | 硬性底线 |
|:---|:---|:---|
| 视觉切换频率 | 45-120 秒/张 | ≤ 120 秒/张 |
| 每张 Slide 文字量 | ≤ 6-10 词 | — |
| **模块最低 Slide 数** | `⌈讲授净分钟数 ÷ 2⌉` | `⌈讲授净分钟数 ÷ 3⌉` |

> **公式**：讲授净分钟数 = 模块总分钟数 - ACTIVITY 分钟数。
> 例：25 分钟纯讲授模块 → 建议 ≥ 13 张，底线 ≥ 9 张。

### 6.3 禁止事项

*   ❌ 添加与学习目标无关的装饰性图片（Mayer 连贯性原则）
*   ❌ 连续 > 120 秒（约 360 字）无任何 `> [VISUAL]` 切换
*   ❌ 在同一张 Slide 上堆叠 > 10 个文字要点（认知过载）

---

## 7. 质量检查清单

> 此清单为**唯一定义处**。`/write` 和 `/audit` 均引用此清单。

- [ ] 技术参数是否与知识库一致？
- [ ] 所有 `[VISUAL]` 块是否包含必填字段 (Slide, Layout, Scene)？
- [ ] 知识面覆盖：每个 `##` 讲授模块的口头型人文标签数 ≥ `⌈模块讲授字数预算 ÷ 2000⌉`？（最低 1 个/模块）
- [ ] 是否包含留白标记？
- [ ] 语言是否遵循 `rule_localization.md` 和 `rule_narrative_standards.md`？
- [ ] **Visual Anchoring**: 正文是否包含指向画面的指示性词汇？
- [ ] **Bullet Sync**: Speech 中的结构化要点（≥3 并列项）是否在 `[VISUAL]` 的 `**List**` 中同步？
- [ ] `[ACTIVITY]` 总时长 > 0（`lecture`/`workshop` 模式强制）？
- [ ] **Visual Density**: 每个模块的 Slide 数是否 ≥ `⌈讲授净分钟数 ÷ 3⌉`？（§6.2 硬性底线）
- [ ] **Visual Gap**: 是否存在连续 > 360 字（约 120 秒）无 `[VISUAL]` 的口述段落？（§6.3 禁止事项）

---

## 8. 标杆密度样本 (Benchmark Density Sample)

> **用途**：当课程无已完成脚本时（冷启动场景），Agent 必须将标杆样本作为**人文密度基线锚点**，代替前序脚本参考。
>
> **标杆样本已拆出为独立文件**：[benchmark_sample.md](benchmark_sample.md)。冷启动时仅加载该文件（~45 行），不必加载本 SKILL.md 全文。
