---
trigger: model_decision
description: 当准备调用 generate_image 为课程生成视觉资产时，必须先读取 visual_system.yaml 并按 Prompt 组装协议构建指令。
---

# 规则：视觉资产生成协议 (Visual Asset Generation Protocol)

**生效范围**: 当 Agent 需要调用 `generate_image` 工具为课程创建视觉资产（PPT 配图、信息图、图标等）时。

## 1. 核心原则

> **设计系统是唯一的视觉权威。任何生成的图片都必须像是从同一本品牌手册中裁出来的。**

## 2. 强制前置步骤 (Pre-flight)

在调用 `generate_image` **之前**，Agent 必须：

1.  **读取** 目标课程的 `course.yaml`。
2.  **定位** `agent.standards` 字段 → 读取对应的 `visual_system.yaml`。
3.  **提取** 以下高保真层级 Tokens：
    *   `style.prompt_variants[Layout]` — 当前 Layout 的 AI 视觉提示指引模板
    *   `style.prompt_templates.base_en` — 该主题全局的基础英文生成后缀
    *   `palette.bg_base` / `palette.primary` 等 — 主要色值约束
    *   各主题特异性内部指导 (如 `generation_guide`) — 必须作为内部推导(thinking) 的法则，严禁照搬输出，严禁越权新建规则文件。
4.  **隔离校验**：如果当前对话中已为**另一门课程**加载过不同的 `visual_system.yaml`，Agent 必须在内部推理中**显式确认主题切换**（输出 `[THEME SWITCH: 从 <旧主题> 切换到 <新主题>]`），并清除上一课程的 Prompt 模板缓存。禁止在未确认切换的情况下复用前一课程的色板或风格词。

> [!CAUTION]
> 未完成上述步骤直接调用 `generate_image` 属于**违规操作**。

## 3. Prompt 组装协议

最终 Prompt 必须按以下的“模块化”架构进行拼装，并在第二步进行**场景路由分流**：

```
[Scene 描述（核心要求：不仅仅翻译物理画面，必须强制加入 `[Emotional/Psychological Tension]` 层。提取脚本上下文中潜藏的痛点、焦虑或顿悟，翻译为视觉张力形容词，例如：'overwhelming, feeling of suffocation, sterile, high contrast tension, breathing room' 等，以确保生成资产具有受众共鸣的氧气感和情绪张力）],
[Keywords 认知锚点注入（强制）：从 [VISUAL] 块的 Keywords 字段（若有）和紧邻的后续 Speech 段落中提取 3-5 个最具辨识度的名词/实体/品牌名，翻译为英文名词短语后嵌入场景描述中。这些关键词是教师回忆逐字稿的核心线索，必须在画面中以可辨识的具象物件形式呈现。示例：「纸质账本」→ vintage ledger book, 「小红书瀑布流」→ smartphone showing scrolling feed, 「水泵」→ cast-iron water pump],
[上下文文化适配：根据脚本主题的文化/时代背景，选择匹配的影像风格。如脚本讲当代科技，使用 "contemporary product photography"；如脚本讲中国历史，使用 "Chinese historical illustration"。禁止对所有场景无脑套用同一年代的影像风格。具体路由规则见 visual_system.yaml 的 generation_guide.context_routing 节。],
[路由条件分流（基于 `[VISUAL].RenderMode` 字段，缺省按 visual_system.yaml 的 pedagogical_routing 规则自动判定）：
  - **路由 A (主题风格)**：`RenderMode` 为 `themed` → 附加 `style.prompt_variants.Layout` + `style.prompt_templates.base_en`。
  - **路由 B (纯几何)**：`RenderMode` 为 `pure` → 强制忽略所有 Layout 变体，唯一附加 `style.prompt_templates.pure_geometry_en`。
  - **路由 C (真实素材)**：`RenderMode` 为 `real` → 不调用 `generate_image`，由 `/source_images` 或 `/source_videos` 工作流处理。
  - **路由 D (教学信息图)**：`RenderMode` 为 `pedagogical` → 附加 `style.prompt_variants.Pedagogical_Layout` + `style.prompt_templates.pedagogical_en`。走 pedagogical 管线时，画面中**必须**包含 1-3 个标志性可辨识物件（iconic recognizable objects）作为认知锚点，**不受** §6.6 具象禁令约束。],
color palette constraint: [bg_base, primary 等实际色阶强制要求].
[若明确要求存在图中文字: All visible text must be cleanly rendered in Simplified Chinese. 否则完全省略此句]
[尺寸后缀（根据脚本上下文环境如 --ar 16:9）]
without: [路由 A → suffix_negative；路由 B → suffix_negative_pure；路由 D → suffix_negative_pedagogical]
```

> [!TIP]
> **Scene 描述应使用英文**：中文 Token 效率约为英文的 1/3。将 `[VISUAL].Scene` 翻译为英文可节省约 30-50% 的输入 Token。若确实需要控制图表标签等特定文字的语言，才按需加入英文的 text_directive 语句。

### 否定词 (Negative Prompt)
默认拒绝混入任何不必要的数据。
**优先使用正面描述**：用正面语言描述期望场景（如 "a clean empty desk typography" 而非 "without clutter text"），若系统给出明确拒绝倾向，则通过 `without:` 参数加挂在末尾。

> [!CAUTION]
> 绝对禁止将 `[VISUAL]` 块中的完整中文字符（如 `包含文本 "..."`、标题、详细图文对照）喂给生图工具。产生的必须是纯净图形资产！如果需要图中有字，说明应当使用 PPT 的文本框排版，而不是烧死在图片像素里。
> **极其关键**：除非特定的 Infographic 绝对需要显示标签内容，否则默认在 `without:` 后附加 **`text, typography, letters, words, characters, numbers`** 以杜绝模型生成“简体中文”文字幻觉。

## 4. 语言约束

| 元素 | 语言要求 | 说明 |
|:---|:---|:---|
| **画面中的标题/标签** | **简体中文** | 默认。除非 `[VISUAL].Lang` 字段明确指定其他语言。 |
| **数据（电话、日期）** | **与脚本一致** | 必须从脚本正文中提取真实数据，严禁编造。 |
| **品牌名/软件术语** | 英文可保留 | 属于 Tier 3 软件锚点，参见 `rule_localization.md`。 |

## 5. 质量检查

质量检查采用**分级策略**，减少推理 Token 消耗：

**Tier A — 逐张检查**（含文字渲染或复杂布局的 Slide）：
1.  使用 `view_file` 查看图片。
2.  确认色调与当前课程 `visual_system.yaml` 的 `palette` 一致（参照 `bg_base` 与 `primary` 色值）。
3.  确认画面文字语言符合 `[VISUAL].Lang` 字段指定（默认中文）。
4.  如不合格，最多重试 **2 次**。

**Tier B — 批量信任**（纯背景/氛围图，Layout 为 `Title`、`Image`）：
1.  先完成全部 Tier B 图片的生成。
2.  最后统一 `view_file` 抽检 **1-2 张**代表性图片。
3.  如抽检发现系统性色调偏差，则对全批重新生成。

## 6. 禁止行为

1.  ❌ 不读取 `visual_system.yaml` 就调用 `generate_image`
2.  ❌ 使用纯英文 Prompt 生成面向中文课程的资产
3.  ❌ 在图片中编造脚本中不存在的数据（电话号码、姓名等）
4.  ❌ 忽略设计系统的色彩约束，使用默认/随机配色
5.  ❌ **将幻灯片中待排版的具体解说文字（如标题、要点列表）硬编码写入图片 Prompt 中**，这是严重的资产污染行为。
6.  ❌ **生搬硬套的具象描摹 (Superficial Skinning)**（**仅限 `RenderMode=themed`**）：在使用抽象风格系统（如包豪斯、康定斯基等）且 RenderMode 为 `themed` 时，禁止用抽象元素去拼凑具体的实体物件。应提取其心理学内核，并用与之呼应的抽象元素进行非客观的形体映射。**但在 `RenderMode=pedagogical` 模式下，此禁令不适用**——教学信息图模式明确要求包含 1-3 个标志性可辨识物件（iconic recognizable objects）作为教师回忆逐字稿的认知锚点。
