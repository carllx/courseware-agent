---
description: 深度审计检查项 — Part D (知识面覆盖率) + Part G (OBE 对齐) + Part H (实验联动合规)。仅在 /audit --deep 时加载。
---

# /audit Deep 级别检查项

> **加载条件**：仅当执行 `/audit --deep` 时加载此文件。
> **前置条件**：已完成 `audit.md` 中的 Quick + Standard 级别检查。

---

### Part D: 知识面覆盖率（知识层）
*   **标签多样性**: 人文层标签是否覆盖至少 2 种分类？（非全是 `[CASE STUDY]`）
*   **人文标签密度**：每个讲授模块的口头型人文标签数是否 ≥ `⌈BUDGET ÷ 2000⌉`？低于此值 → 标记 `[HUMANISTIC_DENSITY_LOW]`
*   **调研深度**: 人文标签内容是否有具体来源？（人名/事件/年份 → 可查？）
*   **事实核验**: 对高黏性/高引用频次的外部事实声明（具体数字、死亡人数、罚款金额、实验数据等），抽检 ≥2 条的来源 URL 可访问性和数据一致性。若来源不可达或数据不一致 → 标记为 `[UNVERIFIED_CLAIM]`
*   **知识拓展**: 是否存在"只复述教材"而缺乏外部知识拓展的段落？
*   **锚点绑定**: 每个人文标签是否回归了技术要点？（防止"故事过剩，技术缺失"）
*   **掉书袋拦截**: 人文层标签内容是否需要听众"停下来查百度"才能理解？
    *   **测试**: 如果必须知道"赫拉是谁"才能听懂这段话，就是废话。必须把"知识点"转化为直觉的"体验感"。
*   **教材覆盖率**: 对照本单元关联的教材章节原文，逐段确认脚本是否覆盖了教材中的核心论述。
    特别检查：正反对照结构是否双覆盖？延伸讨论（如 BOX/案例/附注）是否被纳入或有意识地排除？
    *   若发现教材中有 ≥2 个独立论述段落在脚本中完全未提及 → 标记为 `[TEXTBOOK_GAP]`
*   **教材章节引用链检查（知识链防御 — 根因1）**:
    *   从 `knowledge_hub.yaml` 中筛选 `type: textbook` 的全部条目，逐条检查其 `id` 是否出现在任意脚本的 `核心理论库` 行（`> [!INFO]` 块）或 `[TECH NOTE]` 正文中
    *   未被任何脚本引用的教材章节 → 标记 `[TEXTBOOK_UNLINKED]`，附带条目 ID 与摘要
    *   与 `[TEXTBOOK_GAP]` 的区别：GAP 检查教材**内容**是否被脚本覆盖，UNLINKED 检查教材**条目**是否被结构化引用——后者确保知识库索引与教学链路的闭环
*   **案例密度检查（ADR 023）**: 对每个讲授模块，统计独立案例/实验/产品实例数量，与模块字数预算对照：
    *   字数预算 ≥ 3000 字 → 需 ≥ 2 个独立案例
    *   字数预算 ≥ 4500 字 → 需 ≥ 3 个独立案例
    *   不达标 → 标记为 `[CASE_DENSITY_LOW]`

*   **跨学科维度检查（IDC — Interdisciplinary Check）**：
    *   对每个讲授模块（字数预算 ≥ 2500 字），检查是否存在至少 1 个来自**异质学科**的深度桥接素材
    *   "异质学科"定义：与课程主学科（由 `course.yaml` 的 `discipline` 或课程名称推断）不同的学术领域
    *   桥接素材的识别标志：`[PHILOSOPHY]`、`[ART/AESTHETICS]`、跨域 `[CASE STUDY]` 标记、或正文中明确引用异领域理论家/艺术家
    *   不达标 → 标记为 `[IDC_LOW]`，建议激活 `narrative_archaeologist` §1.5 进行补充
    *   **防灌水校验**：标记为跨学科的内容必须包含锚点回归句（绑回技术要点），否则标记为 `[IDC_DECORATIVE]`（装饰性跨学科引用，无实质贡献）

> 当知识面覆盖率不足、案例密度不达标或跨学科维度不足时，建议激活 `narrative_archaeologist` skill 执行补充调研。

---

### Part G: OBE 构建性对齐审查

> 当需要验证脚本与 OBE 框架的对齐时激活。交叉引用 `rule_training_plan_compliance.md` §4。

*   **G1: 构建性对齐三角**
    *   对 `supported_objectives` 中声明的每个目标，验证脚本中是否存在完整的 **目标 → 教学活动 → 评价/任务** 闭环
    *   若某目标无对应教学活动或评价手段 → 标记 `[OBE_MISALIGN]`
*   **G2: Bloom 分类法动词合规**
    *   `course.yaml` 的 `objectives.desc` 禁用动词：了解 / 熟悉 / 理解 / 掌握
    *   `lessons.objectives`（含脚本 frontmatter）属于豁免范围，但建议与 `objectives.desc` 风格统一
*   **G3: 支撑深度匹配**
    *   对本周 `supported_objectives`，判断脚本教学深度是否匹配 `objectives.desc` 中声明的 Bloom 层级
    *   起始周允许"导入/体验"层级，后续周必须逐步深化
*   **G4: 大纲一致性交叉验证**
    *   引用 `rule_outline_alignment.md` 的 O1-O7 + O9 + O10（与 Quick 级别 Q5 共享同一检查表）

*   **G5: 显式回链强制检查（知识链防御 — 根因3）**
    *   对非首周（W2+）脚本，定位 `[STAGE NOTE: 复习]` 或 `[STAGE NOTE: 复习/导入]` 段落
    *   检查该段落是否包含**目标 ID 锚点**（如"知识目标 2 回链"、"素质目标 2 回链"等显式回链标记）
    *   仅有概念性回顾（如"回顾上周的 Tidy Data"）但无目标 ID 绑定 → 标记 `[BACKLINK_WEAK]` ⚠️
    *   **原理**：OBE 评审要求可追溯的显式锚点，"隐含使用"不等于"显式覆盖"——复习段必须让审查者一眼看到本段回链的是哪个课程目标

*   **G6: 脚本-日历目标交叉校验（知识链防御 — 根因2）**
    *   比对脚本 frontmatter 的 `objectives` 列表与 `course.yaml` 对应周次的 `supported_objectives` 列表
    *   脚本 frontmatter 声明了某目标但 calendar 未标注 → 标记 `[OBJ_UNLABELED]`，建议补标
    *   calendar 标注了某目标但脚本 frontmatter 未声明 → 标记 `[OBJ_PHANTOM]`，可能为虚标
    *   **原理**：`supported_objectives` 依赖人工标注，缺乏从脚本内容反推的校验机制——双向对比消除标注盲区

---

### Part H: 实验联动合规性审查

> **加载条件**：仅当 `<课程>/practices/experiment_planning.md` 存在时执行。
> **目的**：确保每周脚本的实践活动、课后任务和工具链与实验进度规划保持一致。

*   **H1: 实验区间匹配**
    *   根据当前 Week N，确认其落入 `experiment_planning.md` 中哪个实验的「对应周次」区间
    *   若当前周次不在任何实验区间内（如纯理论周），记录 `[EXP_NONE]` 并跳过 H2-H5

*   **H2: 数据流一致性**
    *   若当前实验或前序实验的交付物包含数据集（如 Tidy CSV），检查脚本的实践 ACTIVITY 和课后 `task` 是否引用了该数据来源
    *   若脚本中使用了与实验规划不一致的数据来源（如实验要求用实验1的 Tidy Data，但脚本让学生随意选数据）→ 标记 `[EXP_DATA_MISMATCH]`

*   **H3: 工具链覆盖度**
    *   对照实验规划中声明的工具（如 ECharts / Figma / AI 辅助），检查本周脚本是否对该工具有教学铺垫或操作指导
    *   若实验要求的核心工具在对应周次的脚本中完全未提及 → 标记 `[EXP_TOOL_GAP]`

*   **H4: AI 使用边界合规**
    *   读取实验规划中对 AI 的使用定位（如"AI 辅助生成"或无 AI 要求）
    *   若实验未要求 AI 辅助，但脚本中引入了学生端 AI 操作 → 标记 `[EXP_AI_LEAK]`
    *   若实验明确要求 AI 辅助，但脚本中未给出任何 AI 使用指导 → 标记 `[EXP_AI_MISSING]`

*   **H5: 课后任务-实验交付物对齐**
    *   对照实验规划中的「交付物」清单，检查 `course.yaml` 中对应周次的 `task` 字段是否与实验交付物在范围和格式上一致
    *   若 `task` 要求的产出与实验交付物严重不匹配 → 标记 `[EXP_DELIVERABLE_DRIFT]`

*   **H6: Practice YAML theory_link 覆盖率（CA 构建性对齐）**
    *   统计本周 practice YAML 中 `type ∈ {workshop, practice, critique}` 的 phase 数量
    *   统计其中填写了有效 `theory_link` 的数量（结构化对象或非空字符串均计入）
    *   覆盖率 < 100% → 标记 `[CA_COVERAGE_LOW]`，列出缺失的 phase ID 和名称
    *   若 `theory_link` 为字符串类型（非对象） → 标记 `[CA_LEGACY_FORMAT]`
    *   若 `theory_link.concept_id` 不存在于 `course.yaml.concept_registry[]` → 标记 `[CA_REF_BROKEN]`

*   **H7: upstream_dependencies DAG 一致性**
    *   对所有声明了 `upstream_dependencies` 的 phase，验证 `source` 字段指向的 `W0X.PY` 是否存在于对应周次的 practice YAML 中
    *   验证 `artifact` 字段描述的产出物是否在源 phase 的 `deliverables` 中有对应条目
    *   引用断裂 → 标记 `[UPSTREAM_BROKEN]`
    *   若 `description/steps` 中引用了其他周次产出物但 `upstream_dependencies` 为空 → 标记 `[UPSTREAM_IMPLICIT]`

*   **H8: Practice Guide 生成状态**
    *   检查对应周次的 `practices/W0X_Practice_Guide.md` 是否存在
    *   若存在，检查文件大小是否 > 2KB（骨架阈值）
    *   缺失 → 标记 `[GUIDE_MISSING]`
    *   存在但 ≤ 2KB → 标记 `[GUIDE_SKELETON]`

> 当 Part H 存在 ≥2 项标记时，建议重新审查 `/write Phase 1 Step 2.1b-2.1c` 的联动扫描是否被正确执行。
