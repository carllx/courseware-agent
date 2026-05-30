---
name: script-format
description: 定义课程逐字稿的格式规范与标签体系（含三层松耦合叙事约束体系、Mayer/Rosenshine 实证原则、教师分级赋能策略）。当 Agent 执行 /write 工作流撰写脚本时，自动参照本规范。依赖 rule_narrative_standards.md 和 rule_localization.md。
---

# 技能：脚本格式规范 (Script Format)

## TL;DR (预检阶段专用，≤ 150 字)

脚本格式核心：Visual-First 双轨（先 VISUAL 后 Speech）→ 知识标签（技术层+人文层）→ ACTIVITY 块。Slide 内联定义于 `> [VISUAL]` 块（Slide/Layout/Scene 三必填）。叙事约束: §5.1 三层松耦合体系（叙事启动层推荐/认知传递层强制/实证丰化层推荐），Rosenshine 检查点: 连续>3000字纯讲授必须插入 ACTIVITY。视觉密度底线: 每模块 Slide ≥ ⌈讲授净分钟÷3⌉，连续 >360 字无 VISUAL 禁止。人文标签密度: 每模块口头型标签 ≥ ⌈字数预算÷2000⌉。完整规范见下文各节。

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
3.  **Signaling Sync (信标同步)**: 当 Speech 中出现 ≥3 个并列要点时，按**内容类型分流**决定是否在 `> [VISUAL]` 块中显示 `**List**` 字段（详见 `rule_visual_signaling.md`）：
    - **结构性枚举**（定义/框架/分类/SOP/评分标准）→ **必须**有 List，每项 ≤4 字
    - **操作性步骤**（SOP/实践指引）→ **必须**有 List，可保留完整步骤编号
    - **论证性递进**（首先…其次…的逻辑展开）→ **禁止**有 List（口述已充分传递，上屏触发冗余效应）
    - **修辞性排比**（情感渲染/类比/排比句式）→ **绝对禁止** List（文字化杀死冲击力）
4.  **Intent Alignment (意图对齐)**: `[VISUAL].Scene` 的描述必须与其后续 Speech 段落共享同一个**认知意图**（而非表层实体名词）。在抽象风格系统（如 Dada/Bauhaus）下，Scene 使用隐喻/情绪/张力来表达此意图；在具象风格系统下，Scene 可直接引用 Speech 中的实体对象。
    - 写作时的自检问句：「如果学生同时看到这张图、听到这段话，他们能否感受到与此概念匹配的**与此概念匹配的真实感受——一个具体的生活切片或行业痛点**？」
    - 若答案为否，必须调整 Scene 或 Speech 之一使两者对齐。重点在于捕捉讲者内心的共鸣与受众需要的精神氧气（解脱感、震撼感、焦虑感）。
    - **信息优先原则**：当信息对齐与抽象风格系统冲突时，**信息对齐优先**。Agent 应将 Slide 的 `RenderMode` 自动判定为 `pedagogical`（见 `visual_system.yaml` 的 `pedagogical_routing` 规则），使用教学信息图路线生成包含具象认知锚点的图片。仅当 Slide 纯粹承载氛围/情绪过渡功能（无具体名词、无结构化论点）时，才保留 `themed` 模式走抽象风格路线。
    - **遗留兼容**：在 `RenderMode=themed` 模式下，仍然遵循 `rule_visual_generation.md` §6.6 的具象禁令，使用心理学内核的隐喻映射。
5.  **Progressive Sequence (渐进式披露/多帧连击)**: 严禁为了“少写一个块”而将含有 SCQA 完整逻辑的内容堆叠在单张排版上（如同时抛出痛点、发问与底层 3 个支撑点）。对于核心知识节点的高潮引入，必须使用**多帧视觉切花序列**替代信息堆叠：
    - ① **(悬念/冲突)**：使用 `Layout: Full` 极简放大充满张力的痛点切片 + 留白 `**(Pause: 3s)**`。
    - ② **(焦点发问)**：紧接使用 `Layout: Center` 提出直指灵魂的反问。
    - ③ **(结构解答)**：最后进入 `Layout: Grid` 或 `Split` 层层解构金字塔的论点。

---

## 2. 知识标签体系

标签服务于**知识面的规范化**——确保课程触及技术深度与人文广度。

**技术层**:
*   `> [TECH NOTE]` — 技术原理、参数说明
*   `> [WARNING]` — 操作风险、常见错误
*   `> [DID YOU KNOW]` — 冷知识、科普趣闻

**人文层** (触发深度 Web 调研。**核心规则**：这些标签所承载的内容必须是学生听完后能一句话复述给室友的**真实案例或行业痛点**，写作时需寻找具体的生活切片进行交织，不要使用干瘪枯燥的背景，也不要用华丽的修辞替代真实故事):
*   `> [STORY TIME]` — 比喻、寓言、经典故事
*   `> [PHILOSOPHY]` — 哲学思辨、认知科学
*   `> [CASE STUDY]` — 行业案例、历史事件、文化现象
*   `> [LIFE CONNECT]` — 日常生活、地域文化、流行文化

**教学层**:
*   `> [TEACHING MOMENT]` — 核心教学金句、顿悟时刻

**静默层** (不朗读):
*   `> [VISUAL]` — 画面描述 + Slide 内联定义


### 人文层标签调研指引

1.  **Term Check**: 先使用 `librarian` 技能查阅教材定义，确保术语准确性。
2.  **Deep Dive**: 当使用人文层标签时，Agent **必须**激活 `narrative_archaeologist` skill 执行深度调研。
3.  详细的搜索策略、三轮搜索协议、调研备忘录格式和质量过滤标准见该 Skill 文档。

### 知识标签 + Slide 引用关联

知识标签自身**不是** `[VISUAL]`，但可以紧跟一个 `[VISUAL]` 块。详见 [visual_block_examples.md](references/visual_block_examples.md)。

---

## 3. `[VISUAL]` 块规范

所有 Slide 直接在 Script 的 `> [VISUAL]` 块中定义。**不再使用集中式 `slide_database.md`**。

> [!WARNING]
> **防 Markdown 块粘连红线 (Anti-Adhesion Rule)**
> 当 `> [VISUAL]` 或 `> [ACTIVITY]` 紧跟在另一个引用块（如 `> [CASE STUDY]`）之后或被其包裹时，**必须在两个块之间使用真正的空行（完全空白，不能有 `>`）进行断开！**

### 字段规范

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `Slide` | ✅ | Slide 标题（中文），兼作模块内唯一标识 |
| `Layout` | ✅ / 可推断 | PPT 排版类型。当下方关联了代码块/Mermaid/表格时可省略，解析器自动推断（见下文） |
| `Scene` | ✅ | 画面的中文描述 |
| `Text` | 可选 | Slide 标题文字 |
| `List` | 可选 | 列表内容。**单行**用 `/` 分隔；**多行**每项以 `> - 项目` 格式（必须保留 `>` 前缀）。**Comparison** 用 `label: items` 冒号键值对，**严禁缩进嵌套子列表** |
| `Action` | 可选 | 画面中的操作动作 |
| `Asset` | 可选 | 推荐 MD 图片语法 `![预览](路径)`，引擎自动剥壳提取纯路径。**注意：当 `[VISUAL]` 块下方跟随关联的纯文本资产时，引擎提取的 `assetContent` 优先级高于图片路径，原图片将被忽略。** |
| `Asset N` | 可选 | 多图编号后缀（`Asset 1`, `Asset 2`, ...），归入 `assets[]` |
| `Resource` | 可选 | 辅助参考图片路径，归入 `assets[]` |
| `AI_Prompt` | 可选 | AI 文生图 Prompt |
| `Source` | **条件必填** | 枚举：`Textbook`/`AI_Gen`/`Code`/`External`/`Video`/`Manual`。非 AI 真实素材时强制必填 |
| `Duration` | **条件必填** | 视频时长，格式 `XmXXs`。Asset 指向 `.mp4`/`.webm` 时强制必填 |
| `TimeCategory` | **条件必填** | `lecture`（≤30s）/ `activity`（>30s）/ `explore`。Duration 存在时强制必填 |
| `Search` | 可选 | 网络搜索关键词 |
| `Caption` | 可选 | 注释/引用文字 |
| `Keywords` | 推荐 | 3-5 个英文关键名词，作为 AI 文生图认知锚点 |
| `RenderMode` | 可选 | `themed`/`pedagogical`/`pure`/`real`，缺省由 `visual_system.yaml` 自动判定 |
| `assetContent` | 引擎推断 | 纯文本视觉资产内容。当 `[VISUAL]` 块下方**紧跟**（允许 ≤1 行空行间距）Markdown 代码块或表格时，引擎会自动吞并将其作为内嵌资产。 |
| `assetType` | 引擎推断 | 纯文本视觉资产类型（如 `mermaid`, `javascript`, `table` 等）。 |

### 视频型 Asset 规范

视频 Asset **必须直接指向 `.mp4`/`.webm` 文件**，引擎通过扩展名判断 Slide 类型。详细格式示例与禁止行为清单见 [visual_block_examples.md](references/visual_block_examples.md)。


### Layout 排版类型 (语义预设版)

> 详见项目规范 [VISUAL_LAYOUT_SPEC.md](../../../../docs/VISUAL_LAYOUT_SPEC.md) 和 [layouts_v2.md](./layouts_v2.md)。

为保持写作直觉，作者在编写 `[VISUAL]` 块时，可直接使用以下 12 种**语义别名**，底层引擎会自动将他们派发到正确的三层正交架构组件中：

| 基础空间 | 可用的教学场景 (语义推断) |
|:---|:---|
| **`Center`** (居中视觉) | `CTA` (行动号召), `Agenda` (大纲目录) |
| **`Split`** (常规双栏) | `Quote` (金句引言), `Workshop` (操作工坊模式) |
| **`Grid`** (多格矩阵) | `Comparison` (方案/红绿对比阵列。**建构法则：**作为引入新法则的破冰工具，先呈现“坏设计 vs 更坏设计”，激发学生内心的疑问与判断，**不要过早闭合结论**) |
| **`Full`** (沉浸满屏) | `Screenshot` (带设备外壳截图), `Poll` (互动轮询) |
| **`Flow`** (节点流线) | - |
| **`Code`** | 代码块展示。配合下方关联 Markdown 代码块使用 |
| **`Diagram`** | Mermaid 图表（架构/流程/类图等）。配合关联 Mermaid 代码块使用 |
| **`Table`** | Markdown 表格展示。配合关联 Markdown 表格使用 |

> **自动推断逻辑**：如果作者在 `[VISUAL]` 块中未显式指定 `**Layout**`，但其下方紧跟了纯文字视觉资产（代码块/Mermaid/表格），解析器会根据代码块语言或表格格式自动推断并应用 `Code`、`Diagram` 或 `Table` 排版类型。

> ⚠️ 警告：原有的部分伪布局（`Title`, `Timeline`, `Card`, `Table`, `List` 等）不代表排版骨架，**已全数废弃并被 Validation Suite 拦截**。如果是纯文字列表，请使用 `List` 字段；**如果内容是纯文本资产（代码块、表格、Mermaid），绝对禁止捏造 `Code` 等伪字段！**必须将原生 Markdown 代码块脱离引用（无 `>` 前缀）直接挂载到 `[VISUAL]` 块的紧下方，引擎会自动吞并并推算组件。

---

## 4. `[ACTIVITY]` 块规范

`lecture` / `workshop` 模式下强制执行：

- 每 **60-90 分钟**的讲授内容后必须插入至少 **1 个** `> [ACTIVITY]` 块
- 活动总时长须与理论讲授时长之和符合课程的计划学时

### 字段规范

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `Type` | ✅ | 活动类型：`Practice` / `Discussion` / `Workshop` / `Quiz` / `QA` / `Demo` / `Warm-up` (强烈鼓励每穿行完一段高能理论后，插入 1 分钟量级的极微小 `QA` 心跳校验，避免长时单向说教导致心流断裂) |
| `Duration` | ✅ | 时长，如 `30min` |
| `Desc` | ✅ | 活动名称或简述 |

```markdown
> [ACTIVITY]
> *   **Type**: `Practice`
> *   **Duration**: `30min`
> *   **Desc**: 活动名称或简述
> 活动操作说明…
```

### 4.1 Quiz 子类型规范

当 `Type: Quiz` 时，ACTIVITY 块必须包含以下额外字段：

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `Q` | ✅ | 题干文本（单行，情境+问题） |
| `Options` | ✅ | 选项列表，用 ` \| ` 分隔。格式：`A. 文本 \| B. 文本 \| C. 文本 \| D. 文本` |
| `Answer` | ✅ | 正确答案字母（单选：`C`；多选：`A,C`） |
| `Explain` | 推荐 | 答案解析，引导学生回溯讲授内容。应锚定逐字稿中的具体论述 |

**完整示例**：

```markdown
好，我们来做一个快速测验。

> [ACTIVITY]
> *   **Type**: `Quiz`
> *   **Duration**: `2min`
> *   **Desc**: 案例判断：剥离伪需求
> *   **Q**: 小明买了一台戴森吸尘器，并在朋友圈发了开箱照片。根据 JTBD，他发朋友圈属于什么需求？
> *   **Options**: A. 功能性需求 (Functional) | B. 个人情感需求 (Personal) | C. 社会情感需求 (Social)
> *   **Answer**: `C`
> *   **Explain**: 发朋友圈是为了向外界展示生活品质、获得点赞与认同，属于社会情感需求（Social Job），与吸尘器本身吸灰的功能性无关。

时间到！我看到后台数据……
```

**Quiz 块书写规则**：
- Quiz 块**前面必须有 ≥1 句过渡口播**，引导学生进入答题模式（防止 VISUAL + ACTIVITY 堆叠）
- `Duration` 不可省略（审计配速和 H5 活动时长统计依赖此字段）
- 选项数量 ≥ 3 且 ≤ 5
- 所有内容保持在 `> ` 引用块内，TTS 导出和 PPT 渲染自动跳过内部内容
- **PPT 端**：自动渲染为活动指引页（暖色底 + 📝 图标 + Desc 标题），教师看到此页切换超星投屏
- **H5 端**：渲染为交互式测验卡片（题干 + 选项列表 + 折叠答案）

### 4.2 ACTIVITY 块语气规范

`> [ACTIVITY]` 块内部的指导文本**必须使用祈使句 SOP 体**——动词开头、步骤分明、无修辞膨胀。

✅ **正确**：
```markdown
> Step 1: 打开 Figma，新建 Frame (1440×900)
> Step 2: 将参考截图拖入画板
> Step 3: 用矩形工具标注认知摩擦点
> Step 4: 导出标注图，上传至学习通
```

❌ **禁止**：
```markdown
> 现在，让我们一起打开 Figma，开启一段激动人心的设计之旅！
> 准备好了吗？接下来的 5 分钟将彻底改变你对产品设计的理解！
```

**约束清单**：
- 每步以**动词开头**（打开/选择/观察/记录/讨论/对比/标注）
- 禁止使用感叹号（除非引述用户反馈原文）
- 禁止使用"让我们"、"准备好了吗"、"激动人心"、"彻底改变"等叙事张力词
- 每个步骤 ≤ 30 字（一行一指令，不换行）
- 步骤总数 ≤ 6（超过则拆分为子活动或简化）

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

### 5.1 教学表达三层约束体系 (Evidence-Based Narrative Framework)

> **TL;DR**：三层松耦合约束——① 叙事启动层（SCQA 破冰，推荐）→ ② 认知传递层（冷热交替 + 分段 + 视觉锚定 + Rosenshine 检查点，**唯一强制层**）→ ③ 实证丰化层（STAR 结构案例约束，推荐）。约束强度随教师经验递减（Lv.1 全约束 → Lv.3 底线约束）。
>
> 完整规范见 [evidence_based_narrative.md](references/evidence_based_narrative.md)。


### 5.2 段落物理结构 (Paragraph Anatomy)

> **核心原则**：段落是讲者的呼吸单元。段落过长，讲者无法一口气读完；段落过短碎片化，听者无法建构连贯语义。

#### 段落长度标准

| 段落类型 | 建议长度 | 硬性上限 | 说明 |
|:---|:---|:---|:---|
| 概念引入段 | 80-150 字 | 200 字 | 一段一概念，引入即止 |
| 叙事/案例段 | 150-250 字 | 350 字 | 一段一故事弧：起→转→落 |
| 论证支撑段 | 100-200 字 | 250 字 | 一段一证据/一个维度 |
| 过渡段 | 30-60 字 | 80 字 | 独立成段，不附属于前后段 |
| 总结金句段 | 20-50 字 | 80 字 | 精炼到位，适配 `[TEACHING MOMENT]` |

#### 强制断段规则

满足以下**任一条件**即必须断段（插入空行）：

1. 逻辑转折——出现"但/然而/不过/问题在于"
2. 视角切换——从"用户"切到"开发者"，从"现象"切到"原因"
3. 时间跳切——从一个时代/事件跳到另一个
4. 字数超限——当前段落已超过 250 字且非叙事段

#### 禁止行为

*   ❌ 单个自然段超过 350 字（讲者无法一口气读完，必须拆分）
*   ❌ 过渡句嵌入在上一段或下一段的末尾/开头（破坏段落独立性，应独立成段）
*   ❌ 连续 3 个以上长段（>200字）无短段（<80字）穿插（节奏单调，缺乏呼吸感）

---

## 6. 视觉密度标准 (Visual Density Standard)

> **理论基础**：基于双重编码理论（Dual Coding Theory）与 Mayer 多媒体认知理论（CTML），学习者通过视觉+听觉双通道处理信息，纯语音单通道输入会快速达到认知负荷上限。根据 Mayer 分段原则（Segmenting Principle），教学材料必须分解为用户可消化的信息块。视觉材料的切换在课堂中起到了物理“分段”的信号作用，帮助大脑重置注意力（Attention Reset）。每个视觉都必须回答："这张图帮助学生理解了什么？"

### 6.1 视觉切换触发规则

满足以下**任一条件**即应插入新的 `> [VISUAL]` 块：

| 触发条件 | 说明 |
|:---|:---|
| 新概念引入 | 每个独立认知目标/术语首次出现时 |
| 举例/类比 | 使用案例、比喻、类比解释时 |
| 流程/步骤 | 涉及多步骤流程、操作链路时 |
| 数据/对比 | 展示数据、对比分析、正反对照时 |
| 连续叙述超限 | 连续口述 **>120 秒**（约 360 字）无视觉变化时（强制注意力重置，防止认知负荷过载） |

### 6.2 量化参考

| 指标 | 建议范围 | 硬性底线 |
|:---|:---|:---|
| 视觉切换频率 | 45-120 秒/张 | ≤ 120 秒/张 |
| 每张 Slide 文字量 | ≤ 6-10 词（Signaling 级：关键词 ≤4 字/项） | — |
| **模块最低 Slide 数** | `⌈讲授净分钟数 ÷ 2⌉` | `⌈讲授净分钟数 ÷ 3⌉` |

> **公式**：讲授净分钟数 = 模块总分钟数 - ACTIVITY 分钟数。
> 例：25 分钟纯讲授模块 → 建议 ≥ 13 张，底线 ≥ 9 张。
>
> **DRP 联动修正**：当模块被标记为 `<!-- STATUS: blocked -- DRP_EXHAUSTED -->` 时，
> 视觉密度底线的“讲授净分钟数”应基于**实际字数反推的分钟数**（实际字数 ÷ 语速常量）重新计算，
> 而非原始教案预算分钟数。此修正防止 DRP 熔断模块产生大量无内容支撑的占位 Slide。
> 
> **理论注记 (120秒防线)**：根据高等教育教学研究，学生的持续注意力受刺激频率的深刻影响。单张 Slide 停留超过 1-2 分钟（约 180-360 字）后，注意力会逐渐衰减。此时必须通过视觉或互动干预进行“重置”（Micro-interventions），分流处理压力。

### 6.3 标题层级 Slide 分配协议 (Heading-Level Visual Allocation)

> **设计理据**：H5 Slider 同时服务于**教师备课**（叙事弧线定位、讲稿切换锚点）与**学生预习**（概念边界识别）。视觉素材不应按"标题深度"机械分配，而应以**概念独立性 × 媒体侵入强度**为联合判据。

#### 分配规则

| 标题层级 | Slide 策略 | 判定规则 |
|:---|:---|:---|
| **H2（`##`）** | 🔴 **必须有 ≥1 张独立开篇 Slide** | Layout 限 `Full` / `Center` / `Title`，功能是认知重置，宣告新叙事弧开启 |
| **H3（`###`）** | 🟡 **必须有 ≥1 张锚定 Slide** | 第一张 Slide 是教师的"视觉锚点"（看到这张图就知道该讲什么）。后续 Slide 按 §6.1 触发规则追加。**豁免**：纯文字过渡段（<300 字且无独立概念引入）可不设 Slide |
| **H4（`####`）** | 🟢 **按需分配，默认复用上级 Slide** | 仅当 H4 引入独立案例、独立图表或独立对比时新增 Slide；否则沿用所属 H3 的最后一张 Slide |

#### 媒体侵入强度分级

不同媒体类型对学生心智模型的侵入强度（Cognitive Intrusion）不同，视觉权重应按**媒体类型**（而非标题深度）调节：

| 侵入等级 | 媒体类型 | 说明 |
|:---|:---|:---|
| 🔴 **高** | 实录视频（>30s）、真实历史档案照 | 自带"认知重置"效果，即使放在 H4 下也应独立成 Slide |
| 🟡 **中** | AI 概念图、数据可视化、流程图 | 标准锚定素材，遵循标题层级分配 |
| 🟢 **低** | 微图标、排版强调、代码片段 | 不需要独立 Slide，通过 `List`/`Text` 字段内联即可 |

> [!IMPORTANT]
> **叙事边界性**：相邻 H3 的首张 Slide 必须具备**明确的视觉区分度**（不同的 Scene 主题、不同的色调倾向），以确保 slide-dots 导航条的叙事弧线颜色不发生混淆。禁止两个相邻 H3 共享同一张母图的微调变体作为首张 Slide。

### 6.4 禁止事项

*   ❌ 添加与学习目标无关的装饰性图片（Mayer 连贯性原则）
*   ❌ 连续 > 120 秒（约 360 字）无任何 `> [VISUAL]` 切换
*   ❌ 在同一张 Slide 上堆叠 > 10 个文字要点（认知过载）
*   ❌ 相邻 `> [VISUAL]` 块之间叙事文本 < 80 字（视觉堆叠，破坏演讲呼吸节律）
*   ❌ **Markdown 块粘连**：使用 `>` 空行连接 `[CASE STUDY]` 等口述标签块与 `[VISUAL]` / `[ACTIVITY]` 块（必须用纯空行物理切断，否则 H5 引擎会解析崩溃）
*   ❌ **VISUAL 夹带私货**：将正常的讲授词、活动说明等普通段落，错误地包裹在 `> [VISUAL]` 区块内（`[VISUAL]` 是纯配置块，任何非元数据字段的文本都会被 H5 解析器直接丢弃，绝对不可见！）
*   ❌ **List 裸列表项**：`**List**:` 后的多行列表项缺少 `>` 引用前缀（如 `- 项目` 而非 `> - 项目`），会导致 VISUAL 块在该行断裂，后续的 `**Asset**` 图片路径丢失。多行列表的每个 `- item` 行**必须**以 `> - item` 格式书写
*   ❌ **Comparison 嵌套列表**：在 `Layout: Comparison` 的 List 字段中使用缩进嵌套子列表（如 `>   - 二级子项`）。SSG 构建层的 `extract_visual_list()` 会将所有缩进层级拍平为一维数组，导致 H5 端丢失双栏结构信息并触发错误的奇偶分配 fallback。Comparison 必须使用 `label: items` 扁平冒号格式（见 §3 List 字段规范）
*   ❌ **代码块/表格与 VISUAL 间夹杂讲稿**：在 `[VISUAL]` 块与其关联的代码块/表格之间插入讲稿文字。解析器的 Look-Ahead 只容忍 ≤1 行空行，任何非空非代码的文本都会中断关联，导致代码块被误读为普通正文
*   ❌ **代码块资产与图片 Asset 同时指定**：对同一 `[VISUAL]` 块既提供 `**Asset**` 图片路径又在块后跟代码块。解析器会忽略图片路径（代码块优先），造成作者预期与实际渲染不一致
*   ❌ **伪造属性字段裹挟资产**：在 `[VISUAL]` 块中创造不存在的自定义字段（如 `> * **Code**: ` 或 `> * **Diagram**: `）来包裹文本资源。系统根本不支持此类幻觉设定。
*   ❌ **资产代码块嵌套引用 (Quote Entanglement)**：将下挂的 Markdown 纯文本资产（如 ```javascript ... ```）错误地加上 `>` 前缀包裹在引用块内。纯文本资产必须完全脱离大括号引用，紧随块后顶格书写！

---

## 7. 质量检查清单

> 此清单为**唯一定义处**。`/write` 和 `/audit` 均引用此清单。

- [ ] 技术参数是否与知识库一致？
- [ ] 所有 `[VISUAL]` 块是否包含必填字段 (Slide, Layout, Scene)？
- [ ] 知识面覆盖：每个 `##` 讲授模块的口头型人文标签数 ≥ `⌈模块讲授字数预算 ÷ 2000⌉`？（最低 1 个/模块）
- [ ] 是否包含留白标记？
- [ ] 语言是否遵循 `rule_localization.md` 和 `rule_narrative_standards.md`？
- [ ] **Visual Anchoring**: 正文是否包含指向画面的指示性词汇？
- [ ] **Signaling Sync**: Speech 中的并列要点是否按内容类型分流正确处理？结构性枚举有 List（≤4 字/项）？论证性递进无 List？修辞性排比绝对无 List？（参见 `rule_visual_signaling.md`）
- [ ] `[ACTIVITY]` 总时长 > 0（`lecture`/`workshop` 模式强制）？
- [ ] **Rosenshine Checkpoint**: 是否存在连续 > 3000 字（约 10 分钟）纯讲授（无 `[ACTIVITY]`）的区间？（§5.1 第二层 Rosenshine 理解检查点）
- [ ] **Visual Density**: 每个模块的 Slide 数是否 ≥ `⌈讲授净分钟数 ÷ 3⌉`？（§6.2 硬性底线）
- [ ] **Visual Gap**: 是否存在连续 > 360 字（约 120 秒）无 `[VISUAL]` 的口述段落？（§6.4 禁止事项）
- [ ] **Visual Stacking**: 是否存在相邻 `[VISUAL]` 块间距 < 80 字的堆叠违规？（§6.4）
- [ ] **Media Duration**: 所有 Asset 指向 `.mp4`/`.webm` 的 `[VISUAL]` 块是否均包含 `Duration` 和 `TimeCategory` 字段？（§3 条件必填）
- [ ] **Heading-Level Allocation**: 每个 H2 (`##`) 是否有 ≥1 张开篇 Slide？每个 H3 (`###`) 是否有 ≥1 张锚定 Slide（<300 字纯过渡段豁免）？（§6.3 分配协议）
- [ ] **Narrative Boundary**: 相邻 H3 的首张 Slide 是否具备明确的视觉区分度（不同 Scene 主题/色调）？（§6.3 叙事边界性）
- [ ] **Cognitive Anchor Recall (三词回溯测试)**: 对每张 AI 生成的 Slide 图片执行回溯测试——看着图片，能否在 3 秒内说出 ≥3 个与逐字稿内容相关的关键词？若不能，说明图片缺少认知锚点，需调整 Scene/Keywords 后重新生成。（仅适用于 `RenderMode=pedagogical` 的 Slide）
- [ ] **Instant Clarity (§10)**: 是否存在可用更简单日常词替换而不损失信息的复杂用词？（Oppenheimer 替代测试）是否存在单段 ≥ 3 个极端修饰语？（Mayer 修饰语密度上限）H3/H4 标题是否秒懂？（Pinker 新生朗读测试）
- [ ] **Pure Text Asset Association**: 带有代码块/Mermaid/表格的 `[VISUAL]` 块是否正确关联？`assetType` 是否与实际内容匹配？（§3 纯文字视觉资产）
- [ ] **Dying Metaphor (§10.6)**: 是否存在 Dying 级隐喻/四字成语堆砌？（Orwell 自检：读到它时大脑是否自动生成画面？如果没有就是 Dying，用白话重说）
- [ ] **结构性装饰语密度**: `validate_script_length.py` 是否报告 `[DEGEN]` 段落级结构性退化？（四字格密度 ≥5/百字、「的」字链 ≥2 处、或窗口极端修饰 ≥3）如有，须修复对应窗口

---

## 8. 标杆密度样本 (Benchmark Density Sample)

> **用途**：当课程无已完成脚本时（冷启动场景），Agent 必须将标杆样本作为**人文密度基线锚点**，代替前序脚本参考。
>
> **标杆样本已拆出为独立文件**：[benchmark_sample.md](benchmark_sample.md)。冷启动时仅加载该文件（~45 行），不必加载本 SKILL.md 全文。

---

## 9. 参考资源索引 (Reference Index)

以下参考文件按需加载，不随 SKILL.md 主体自动加载：

| 文件 | 加载时机 | 内容 |
|:---|:---|:---|
| [evidence_based_narrative.md](references/evidence_based_narrative.md) | 撰写/审计模块叙事结构时 | 三层松耦合约束体系完整规范（SCQA/认知传递/STAR）+ 教师分级赋能策略 |
| [visual_density_standard.md](references/visual_density_standard.md) | 审计视觉密度、分配 Slide 时 | 视觉切换触发规则、量化参考、标题层级分配协议、禁止事项 |
| [visual_block_examples.md](references/visual_block_examples.md) | 编写 VISUAL 块、处理视频 Asset 时 | 知识标签+Slide 关联示例、视频型 Asset 正确格式与禁止行为 |
| [LAYOUT_STORYBOOK.md](references/LAYOUT_STORYBOOK.md) | 需要 Layout 排版的详细视觉参考时 | Layout 类型的 Storybook 可视化样例集 |
| [narrative_standards_guide.md](references/narrative_standards_guide.md) | 审阅词句、深度 Audit 重构、不确定语调时 | 反翻译腔、韵律、过渡焊接、脉络透明度、§10 秒懂优先协议 |
| [instant_clarity_research.md](references/instant_clarity_research.md) | 执行 §10 遇边界判定、优化 validate_script_length.py、需要学术引用支持决策时 | Oppenheimer/Paivio/Mayer/Pinker 四框架的原始论文、实验结论、LLM 华丽偏差研究 |
| [speech_memorization_research.md](references/speech_memorization_research.md) | 需要理解脉络可视化和逻辑重建理论基础时 | 七大记忆方法体系、冷热标签映射、骨架卡片理论、v3 逻辑重建范式 |
| [teacher_cheat_sheet.md](references/teacher_cheat_sheet.md) | Lv.1 新手教师备课、`/write` 工作流首次使用时 | 三层分级填空式备课脚手架（§5.1 教师分级赋能策略配套工具） |
| [argument_saturation.md](references/argument_saturation.md) | 审计段落论证饱和度时 | 论证饱和判定模型与阈值 |
| [llm_inflation_patterns.md](references/llm_inflation_patterns.md) | 检测/修复 LLM 生成文本膨胀时 | LLM 常见注水模式识别与修复策略 |
| [rhetoric_patterns.md](references/rhetoric_patterns.md) | 审计修辞手法合规性时 | 修辞模式分类与使用边界 |
| [schema_asymmetry.md](references/schema_asymmetry.md) | 评估学生认知图式差异时 | 图式不对称分析模型 |
| [benchmark_sample.md](benchmark_sample.md) | 冷启动、无前序脚本时 | 人文密度基线锚点 |

> **关联规则**：`rule_script_clarity.md`（脉络清晰度与反注水统一防线）在写作和审计时由 glob 自动触发。
