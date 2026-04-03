---
description: "/write Phase 1 — 备料（Pre-flight + 知识准备）"
---

# Phase 1: 备料 (Preparation)

> **前置**：本文件是 `/write` 工作流的第一阶段。完成后加载 `write_phase2_compose.md` 进入写作阶段。

### Step 0: 环境预检 (Pre-flight Check)
在开始撰写脚本前，**强制要求**运行一次知识库健康度检查，确保没有断链或孤立的知识笔记。只有全绿通过才可进入下一步。

```bash
# 从 Workspace 根目录运行：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_knowledge.py \
  --course "<课程名>"

# Draft 模块追踪（如已存在脚本）：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/check_draft_status.py \
  --course "<课程名>"
```

### Step 0.5: 搜索预算声明 (Search Budget)

> **ADR-028**：在写作前明确各阶段网络请求（search_web/read_url）上限，防止 Token 雪崩。
> 具体预算标准与公式，请参考 `.agent/rules/rule_content_depth.md` 的 `§1.3 搜索预算` 节。
> 当任一预算耗尽时，将未完成调研记录到 `tracking.md`，不阻塞写作流程。

### Step 1: 定位课程
运行 `extract_week.py --week N` 提取目标周的教学信息（替代加载全量 `course.yaml`，ADR-021 Phase 1）：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  《课程》/extract_week.py --week N
```

输出包含本周 calendar、对应 objectives 子集和课程元信息（~2-5KB）。

### Step 2: 加载上下文
*   **结构**: `<课程>/weeks/_archive/00_structure_map.md`
*   **知识入口**: `<课程>/knowledge/knowledge_hub.yaml`（仅加载此文件，不直接加载 `index.json`）
*   **风格**: `<课程>/styles/`（通过 `course.yaml` 的 `agent.style` 定位）
*   **前序脚本**: 加载最近 1 份 **`status: audited`** 的脚本作为风格基线。
    - 若无 `audited` 脚本，回退到 `status: done` 的脚本
    - 若连 `done` 的也没有（冷启动），使用 `script_format/benchmark_sample.md` 标杆样本
    - 仅加载前序脚本中**任意 1 个模块的代表性片段**（~300 字），不加载全文
    - 代表性片段选取标准：优先选含 ≥ 2 个人文标签的模块段落

> [!IMPORTANT]
> **冷启动降级**：当课程无已完成脚本时（如写 W01），Agent 必须加载 `script_format/benchmark_sample.md` 标杆样本作为**人文密度基线锚点**，代替前序脚本。该样本展示了每 ~170 字一个人文锚点的目标密度。

*   **规则与技能**: 按需加载（遵循 Progressive Disclosure 原则）。
    - **知识检索阶段** (Step 2.3-2.5)：加载 `rule_content_depth.md`、`librarian`、`narrative_archaeologist`
    - **写作阶段** (Step 3)：加载 `script_format`、`rule_narrative_standards.md`、`rule_localization.md`、`rule_content_depth.md`
    - 不得在任务开始时一次性加载全部规则和技能

> [!CAUTION]
> **Frontmatter 边界 (ADR 007)**：写作过程中严禁在 frontmatter 中添加教案索引字段（`supported_objectives`/`task`/`steps`）。这些字段的 SSOT 在 `course.yaml`，非脚本的职责范围。Frontmatter 仅含：`week`/`topic`/`title`/`hours`/`objectives`/`created`/`status`。

### Step 2.1: 实践联动扫描 (Practice & Experiment Linkage)

> **目的**：将实践教学规划 (`experiment_planning.md` + `W0X_practice.yaml`) 与每周脚本写作系统性关联，实现正向传导。

**若该周 `hours_practice > 0`：**

1. **宏观扫描（实验/项目）**：
    - 定位 `<课程>/practices/experiment_planning.md`（或 `project_brief.md`）中的当前周次区间。
    - 提取【实验目标】、【交付物产出】、【工具链】与【AI 边界】作为该周脚本的硬性上下文。
    - **硬约束**：课后 `task` 的数据源必须与规划一致；若实验规定禁用 AI，脚本中严禁出现相关操作引导。

2. **微观扫描（每周 Practice YAML）**：
    - 读取 `<课程>/practices/W0X_practice.yaml` (若缺失则标记 `[WARN] 建议先执行 /design_practice`，不阻塞)。
    - 抓取 `theory_prerequisites` 和 `theory_link` 以校验本周讲授模块是否覆盖核心前置概念。
    - 抓取 `upstream_dependencies` 确保跨周实践数据链条完整。

3. **输出联动备忘录**：
    - 提取上述约束，生成简短的 `<!-- PRACTICE_LINKAGE: ... -->` 块并在工作记忆中保留，保证写作时不会偏离实践主线。

### Step 2.2: 字数预算分解 (Word Budget Breakdown)

> **ADR 020 强制**：LLM 单轮输出 Token 上限无法覆盖长课时脚本的全文需求。必须在写作前将目标拆解为模块级字数预算，以支持分段生成。
> **ADR-028 前移**：本步骤从原 Step 2.8 前移至此，确保后续 Step 2.3 的知识检索门限（K-0/K-2）可安全引用模块字数预算。

基于 `extract_week.py --week N` 输出中的 `calendar.lessons[].steps[]` 时长配置，为脚本每个模块计算目标字数：

1. **读取教案 `steps` 配置**（导入/讲授/实践/小结的 `minutes` 分配）
2. **计算各阶段讲授净时长**：模块分配 minutes - 该模块预设 ACTIVITY 时长
3. **按语速常量换算目标字数**：讲授净时长 x 语速常量（默认 180 字/分钟；单课程试点可通过 `--speed-override N` 覆盖）
4. **输出字数预算表**，作为后续步骤的硬性约束

**字数预算表标注格式**（写入脚本骨架中）：

```markdown
## 模块 1：主题名 (约 25 分钟)
<!-- BUDGET: 4500 chars | SLIDES: ≥13 | STATUS: pending -->

## 模块 2：主题名 (约 20 分钟 + 30 分钟 ACTIVITY)
<!-- BUDGET: 3600 chars | SLIDES: ≥10 | STATUS: pending -->
```

**视觉预算**（与字数预算同步生成）：

基于 `script_format/SKILL.md` §6.2 的公式，为每个模块计算最低 Slide 数量：

*   **建议值** = `⌈讲授净分钟数 ÷ 2⌉`
*   **底线值** = `⌈讲授净分钟数 ÷ 3⌉`（写入 `<!-- SLIDES: ≥N -->` 注释）
*   讲授净分钟数 = 模块总分钟数 - ACTIVITY 分钟数

> [!IMPORTANT]
> **时间格式规范**：模块 `##` 标题中的时间标注**推荐**使用中文格式 `(约 X 分钟)`，也接受英文格式 `(X min)` / `(X minutes)`。验证器 `validate_script_length.py --module-breakdown` 已兼容上述所有格式。同一份脚本内应保持格式统一。

> [!CAUTION]
> 禁止跳过本步骤直接进入 Step 2.3。没有字数预算的知识检索无法正确触发门限规则。

### Step 2.3: 知识枢纽扫描 (Knowledge Hub Scan)

> [!CAUTION]
> **上下文隔离策略（条件强制）**：当满足以下**任一条件**时，Step 2.3-2.5 的知识检索
> **必须**委托给 `browser_subagent` 或独立 Agent 调用：
> 1. 本单元模块数 ≥ 4
> 2. 本单元总字数预算 ≥ 12,000 字
> 3. 主 Agent 上下文已超过会话总量的 30%（由 Agent 自行估算）
>
> SubAgent 应仅返回**素材预算表**（Step 2.8 格式），主 Agent 据此进入 Step 3 写作。
> 不满足上述条件时，隔离仍为**推荐**但非强制。

激活 `librarian` skill（遵循 `rule_content_depth.md` §1 知识饱和度门限），执行：

**[K-0 颗粒度预检]** —— **在执行 Layer 1 匹配前，先判断本单元知识颗粒度是否充分：**
*   读取本单元在 `00_structure_map.md` 中的 Hub 标签数量
*   若本单元存在任何 **模块字数预算 ≥ 2500 字** 的模块 **且** 该模块的 Hub 标签数 ≤ 1，则**禁止直接写作**，必须先：
    1.  将「核心理论节点」列中的每个独立认知目标逐一列出
    2.  为每个认知目标在 Hub 中检查或新建专属条目（若无则建 `note` 并更新 Hub）
    3.  确认单元 Hub 标签数 ≥ 单元核心理论节点数后，方可继续

1.  **Hub 已在 Step 2 加载** — 直接读取内存中的 `knowledge_hub.yaml` 条目
2.  **匹配本单元知识点** — 对照当前单元**每个独立认知目标**，按 `tags` 和 `summary` 找命中条目（**每个目标独立匹配，不可用一条 summary 统括多目标**）
3.  **按需深挖**（遵循 `rule_content_depth.md` §1.1 饱和度底线）：
    - 模块字数预算 ≥ 1500 字：**强制执行 Layer 2**（`search_knowledge.py`），不可仅用 summary 写作
    - 模块字数预算 < 1500 字且 `summary` 已足够 → 直接用于写作，跳过 Layer 2/3
    - 需要原文/数据 / 需要具体案例 → 执行 `search_knowledge.py` 精确定位段落
4.  **识别知识缺口** → 无命中条目标记为「调研需求」，进入 Step 2.5

> 调研完成并采用后，**必须**调用 `archive_web.py` 存档为 note，hub 自动更新。

**[知识饱和度评估 (Saturation Check)]**

> **引用**: `rules/rule_content_depth.md` §1.1。对每个独立认知目标执行五维评分（定义/案例/人文/正反/跨学科）。
> 饱和度 < 0.6 强制触发 librarian 深挖 + narrative_archaeologist；人文锚点为 0 自动触发 Step 2.5。

### Step 2.4: 教材-脚本对照审查 (Textbook Cross-Check)

在知识枢纽扫描（Step 2.3）完成后、深度调研（Step 2.5）之前，对 Hub 中所有 `type: textbook` 条目执行**反向验证**：

1.  **定位教材原文**：对照本单元的 Hub 标签，找到教材中所有相关章节的原文
2.  **逐段比对**：检查教材原文中每个独立论述段落是否已被 Hub 条目覆盖或已规划写入脚本
3.  **标记遗漏**：将教材中存在但脚本中未覆盖的知识段落标记为「教材覆盖缺口」
4.  **输出缺口清单**：列出所有缺口及预估时长增量，作为 Step 3 写作和 Step 4 时长校验的输入
5.  **产出案例提取清单**（ADR 023 强制）：以下表格形式列出教材中可用于本单元的所有**具体案例/实验/设计启示/design implications**：

    | 来源章节 | 案例/概念名称 | 可用于哪个模块 | 已在 note 中覆盖？ |
    |---|---|---|---|

    此清单是 Step 3 写作和 DRP-L1 的**必要输入**。**未产出此清单禁止进入 Step 3**。

> **⚠️ 正反双覆盖强制规则**：当教材原文中存在「正反对照」结构时（如 Desirable vs Undesirable、成功模式 vs 失败模式、Use vs Misuse），**必须同时覆盖正反两面**，严禁只提取正面。

### Step 2.5: 深度调研 (Knowledge Expansion)

激活 `narrative_archaeologist` skill，处理以下**三类**素材需求：

1.  **知识缺口**：Step 2.3 中 Hub 完全无命中的知识点（原有逻辑）
2.  **人文层空白**：知识饱和度评估中「人文锚点」维度得分为 0 的认知目标
    - 即便教材定义和案例充足，但缺少故事/隐喻/文化类比时，仍需主动调研
    - 优先搜索中国本土案例和学生日常生活中可观察到的现象
3.  **跨学科空白**：知识饱和度评估中「跨学科桥接」维度得分为 0 且模块字数预算 ≥ 2500 字的认知目标
    - 使用 `narrative_archaeologist` **§1.5 跨学科桥接搜索策略**（强制异领域搜索矩阵）
    - 目标：为模块添加至少 1 个来自异质学科的深度桥接素材（哲学根源/艺术映射/认知科学/社会学）
    - **不灌水原则**：跨学科素材必须通过 §4 Quality Gate + 锚点回归，即便搜索无果也不得用同学科素材冒充

**执行流程**（对上述三类素材需求统一执行）：

1.  **分类搜索**: 对知识缺口/人文空白按 Search Playbook (§1) 构造搜索词；对跨学科空白按 **§1.5 跨学科桥接搜索策略**构造搜索词，执行多角度 `search_web`
2.  **深挖验证**: 对最佳候选用 `read_url_content` 深入阅读，按 3-Pass Protocol (§2) 验证
3.  **产出备忘**: 为每个可用素材生成 Research Memo (§3)
4.  **筛选决策**: 按 Quality Gate (§4) 筛选，标记采用/弃用
5.  **存档回写**: 被采用的素材 → `archive_web.py` 存档；未找到的 → 追加 `tracking.md`

> 调研成果直接作为 Step 3 写作的输入素材。

### Step 2.8: 素材预算表 (Material Budget)

> **引用**: `rules/rule_content_depth.md` §1.2。对每个模块评估素材覆盖率。
> 覆盖率低于门限时**禁止进入 Phase 2 写作**，先执行 DRP 补充素材（具体阈值见 `rule_content_depth.md` §1.2 覆盖率判定表）。
> 预算表以 `<!-- MATERIAL_BUDGET: ... -->` 注释写入脚本骨架，确保跨会话可追溯。
