---
trigger: glob
description: 当 Agent 撰写、插入或修改 [ACTIVITY] Type: Quiz 块时，强制执行随堂练习设计方法论约束——Haladyna MCQ 设计法则、情境化遮盖测试、判断题防线、Testing Effect 反馈增强。
globs:
  - "**/src/M*.md"
  - "**/practices/*.yaml"
---

# 规则：随堂练习设计方法论 (Quiz Item Design Methodology)

## TL;DR

Quiz 的灵魂不是"出题"，而是"诊断 + 纠错"。本规则提供**设计方法论**（怎么出好题），格式合规由 `script-format §4.1` 管控，审计检查由 `audit_standard Part Q` 管控。核心三要素：题干必须通过遮盖测试（§3）、反馈必须锚定逐字稿（§5）、记忆层级限比例（§6）。

> **SSOT**：本文件为 Quiz **设计方法论**的唯一定义点。
> 格式规范 → `script-format §4.1`；审计检查项 → `audit_standard Part Q`；超星导出 → `chaoxing-quiz §2`。

---

## §1 定位声明与管辖边界

本规则**仅管控**"怎样设计出高质量的 Quiz 题目"，不重复定义以下已有约束：

| 约束内容 | 管辖方 | 本规则的姿态 |
|---|---|---|
| Quiz 块格式（Q/Options/Answer/Explain 字段） | `script-format §4.1` | **引用，不重定义** |
| 连续 ≥3000 字必须插入 ACTIVITY | `script-format §5.1 第二层` | **引用，不重定义** |
| Quiz 优先策略（优先于 QA） | `write_phase2_compose.md` | **引用，不重定义** |
| Quiz 块完整性审计（字段齐全性） | `audit_standard Part Q` | **引用，不重定义** |
| 超星题库格式与导出协议 | `chaoxing-quiz §2` | **引用，不重定义** |

---

## §2 Haladyna MCQ 设计法则（精选）

> **理论来源**：Haladyna, T. M., Downing, S. M., & Rodriguez, M. C. (2002). *A review of multiple-choice item-writing guidelines for classroom assessment*. Applied Measurement in Education, 15(3), 309-333.

从 31 条黄金法则中提取 8 条与课堂随堂练习最相关的高共识规则：

### 2.1 题干设计

| # | 法则 | Agent 行为约束 |
|---|---|---|
| H1 | **聚焦单一概念** | 每道题只测试**一个**知识点，禁止在单题中串联多个独立概念 |
| H2 | **题干自包含** | 题干必须呈现一个完整的、可独立理解的问题或情境，不依赖选项才能理解 |
| H3 | **禁止否定题干** | 禁止使用"以下哪项**不**正确"、"**不**属于"等否定措辞（测的是阅读理解而非专业知识） |
| H4 | **禁止照搬逐字稿原文** | 题干和选项的措辞必须进行**语义重构**（paraphrase），不得直接复制逐字稿的原始句子 |

### 2.2 选项设计

| # | 法则 | Agent 行为约束 |
|---|---|---|
| H5 | **混淆项必须可信** | 每个错误选项必须是基于真实学生常见误解（misconception）设计的，不得使用明显荒谬的"凑数选项" |
| H6 | **选项等长等格式** | 所有选项的长度和语法结构应大致一致，避免正确答案因"最长/最详细"而暴露 |
| H7 | **禁止"以上皆是/以上皆非"** | 此类选项消耗短期记忆且诊断价值为零 |
| H8 | **选项随机排序** | 正确答案不得集中在某个固定位置（如总是 C） |

---

## §3 情境化设计与遮盖测试

> **理论基础**：布鲁姆认知分类法 — Application / Evaluation 层级。
> **核心目标**：测试"能否用知识解决问题"，而非"能否复述定义"。

### 3.1 情境微剧本要求

每道 Quiz 的题干**必须**包含一个**微型场景**——一个具体的人物在具体的情境中做了具体的事。

**正确示例**：
> 小明买了一台戴森吸尘器，并在朋友圈发了开箱照片。根据 JTBD，他发朋友圈属于什么需求？

**禁止示例**：
> 关于 JTBD 理论，以下哪项正确？

### 3.2 遮盖测试（Cover Test）— 3 条物理规则

"遮盖测试"的操作定义：**遮住所有选项后，仅凭题干，读者能否清楚知道这道题在问什么？** 通过以下 3 条可机械执行的规则来保障：

| # | 物理规则 | 判定标准 |
|---|---|---|
| CT-1 | 题干必须是**完整的问句或情境描述 + 具体追问** | 题干字数 ≥ 25 字 |
| CT-2 | **禁止空壳题干模板** | 禁止使用：`以下哪项正确`、`关于 X 的说法正确/错误的是`、`下列不属于 X 的是` |
| CT-3 | 题干必须包含 **≥1 个具体实体** | 至少包含一个：人名、产品名、品牌名、场景名词、事件名称 |

---

## §4 判断题设计约束

> **风险背景**：判断题的猜对概率为 50%（远高于四选一的 25%），形成性诊断价值极低。同时，Butler & Roediger (2008) 的 Testing Effect 研究表明，错误项在学生记忆中会留下**错误印记（misinformation effect）**，判断题尤甚。

### 4.1 判断题使用限制

| # | 约束 | 说明 |
|---|---|---|
| TF-1 | **占比限制** | 单次 Quiz 活动中，判断题占比 **≤ 20%**（如 5 题中最多 1 题为判断） |
| TF-2 | **必须附修正解析** | 判断为"错"的题目，`Explain` 字段必须写明**正确的陈述是什么**，而非仅说"该说法是错误的" |
| TF-3 | **禁止绝对词** | 题干中禁止使用"总是"、"绝不"、"所有"、"全部"等绝对量词（这些词是判断题的"送分线索"） |
| TF-4 | **单一命题** | 每道判断题只能包含一个可独立判定的命题，禁止复合句 |

---

## §5 Testing Effect 与反馈增强

> **理论来源**：
> - Butler, A. C., & Roediger, H. L. (2008). *Feedback enhances the positive effects and reduces the negative effects of multiple-choice testing*. Memory & Cognition, 36, 604-616.
> - Butler, A. C., Karpicke, J. D., & Roediger, H. L. (2008). *Correcting a metacognitive error: Feedback increases retention of low-confidence correct responses*. JEPLMC, 34, 918-928.
>
> **核心发现**：多选测试本身就能增强记忆（Testing Effect），但**只有附带反馈时**才能消除错误选项的负面印记。没有反馈的测试比不测试更糟。

### 5.1 反馈设计约束

| # | 约束 | 说明 |
|---|---|---|
| FB-1 | **`Explain` 字段推荐填写** | 虽然 `script-format §4.1` 将 Explain 标记为"推荐"，但本规则**强烈建议**每道 Quiz 都附带反馈，理由见 Butler (2008) |
| FB-2 | **双向解释** | 反馈不仅要说明正确答案**为何对**，还必须说明**至少一个**错误选项为何错（纠正最常见的 misconception） |
| FB-3 | **锚定逐字稿** | 反馈中必须提及逐字稿中的具体论述点（如"参见本节关于 JTBD 三维解绑的分析"），帮助学生**定位回溯** |

---

## §6 认知负荷守则 (CLT)

> **理论来源**：Sweller, J., Ayres, P., & Kalyuga, S. (2011). *Cognitive Load Theory*. Springer.

### 6.1 与记忆层级的兼容约束

> [!IMPORTANT]
> 本规则**不全面禁止**记忆层级（Recall）的测试。
> `chaoxing-quiz §2.3` 的题型矩阵包含填空题（术语回忆强化），属于合法的记忆层级题型。
> 本规则的约束是：**记忆层级题目的占比 ≤ 20%**，推荐 ≥ 60% 的题目达到 Application 或 Evaluation 层级。

| 布鲁姆层级 | 推荐占比 | 对应题型 |
|---|---|---|
| Remember (记忆) | ≤ 20% | 填空题、简单判断题 |
| Understand (理解) | ≤ 20% | 概念辨析选择题 |
| Apply / Evaluate (应用/评估) | **≥ 60%** | 情境选择题、案例分析 |

### 6.2 降低外在认知负荷

| # | 约束 | 说明 |
|---|---|---|
| CL-1 | **选项精简** | 选项数量 3-5 个（已由 `script-format §4.1` 定义，此处引用） |
| CL-2 | **题干避免冗余信息** | 题干中不得包含与答题无关的装饰性背景描述（Mayer 连贯性原则） |
| CL-3 | **单题单屏** | 在 H5 渲染中，一道 Quiz 不应与其他 ACTIVITY 在同一视口内堆叠 |

---

## §7 协作规则引用表

| 关联组件 | 文件路径 | 分工边界 |
|---|---|---|
| **script-format §4.1** | `.agent/skills/script_format/SKILL.md` | 管控 Quiz 块的**格式**（字段定义、书写规则、选项数量） |
| **script-format §5.1** | 同上 | 管控**何时插入** Quiz（3000 字检查点、Rosenshine 原则） |
| **write_phase2_compose** | `.agent/workflows/write_phase2_compose.md` | 管控写作时的 **Quiz 优先策略** |
| **chaoxing-quiz §2** | `.agent/skills/chaoxing_quiz/SKILL.md` | 管控**超星导出**格式与知识点提取协议 |
| **audit_standard Part Q** | `.agent/workflows/audit_standard.md` | 管控 Quiz 块的**审计检查**（字段完整性、过渡口播） |
| **本规则** | `.agent/rules/rule_quiz_design.md` | 管控 Quiz 题目的**设计方法论**（题干质量、选项可信度、反馈深度） |

---

## 禁止行为

- ❌ 出"以下哪项正确"/"关于 X 的说法错误的是"等**空壳题干**
- ❌ 使用"以上皆是"/"以上皆非"选项
- ❌ 错误选项明显荒谬，一看就是凑数
- ❌ 正确答案永远是最长、最详细的那个选项
- ❌ 逐字照搬逐字稿原文作为题干或选项
- ❌ Quiz 不附任何反馈（`Explain` 为空），让错误选项的记忆印记无法消除
- ❌ 整场 Quiz 全是填空/判断等纯记忆题（记忆层级 > 20%）
- ❌ 判断题使用"总是"、"绝不"等绝对词（送分线索）
- ❌ 重新定义 `script-format §4.1` 已管控的格式约束（如选项数量、字段必填性）
