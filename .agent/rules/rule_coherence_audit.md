---
trigger: model_decision
description: 当编写或审查逐字稿时，强制执行 Mayer 一致性原则——识别并标记超出教学目标边界的诱惑性细节和模块级冗余块。仅在审计/深度审查时按需加载。
---

# 规则：Mayer 一致性审查协议 (Coherence Audit Protocol)

> **核心原则**：「有趣不等于有用。」——每个案例、每段扩展讨论、每个知识框（DID YOU KNOW），都必须对本模块的学习目标做出**直接贡献**。否则它就是一个诱惑性细节（Seductive Detail），无论多么精彩，都在消耗学生有限的工作记忆。
>
> **理论基础**：Mayer 一致性原则（Coherence Principle）——"People learn better when extraneous words, images, and sounds are excluded rather than included." 诱惑性细节之所以危险，正因为它们看起来不像冗余。

## TL;DR

对每个 `[DID YOU KNOW]`、`[CASE STUDY]`、`[STORY TIME]` 块以及 >200 字的扩展段落执行 Mayer 三问。不直接支撑教学目标 → `[SEDUCTIVE_DETAIL_BLOCK]`；删除后不损失理解 → `[REMOVABLE]`；引入未声明的新子概念 → `[SCOPE_CREEP]`。

---

## §1 模块级一致性检查（Mayer 三问）

### 1.1 适用范围

对以下内容**逐块**执行 Mayer 三问：
- 所有 `> [DID YOU KNOW]` 块
- 所有 `> [CASE STUDY]` 块
- 所有 `> [STORY TIME]` 块
- 任何 > 200 字的非标签扩展讨论段落（如 Vision Pro 扩展、历史背景叙述等）

### 1.2 三问判定矩阵

| # | 问题 | 判定 | 标记 |
|:---:|:---|:---|:---|
| Q1 | 这段内容是否**直接支撑**本模块声明的学习目标（参照 frontmatter `objectives`）？ | 否 → 疑似诱惑性细节 | `[SEDUCTIVE_DETAIL_BLOCK]` 🟡 |
| Q2 | 删除它后，核心概念的理解度是否会**实质性下降**？ | 否 → 确认为可移除 | `[REMOVABLE]` 🟢 |
| Q3 | 它是否引入了**本模块未声明的新子概念**（检查 `course.yaml` steps）？ | 是 → 超出目标边界 | `[SCOPE_CREEP]` 🔴 |

> [!WARNING]
> **冗余效应边界条件**：Q1 判定时必须区分**真冗余**与**伪冗余/互补**：
> - **真冗余**：文字和图形各自都能独立传达完整含义 → 删除文字版本（Sweller 冗余效应成立）
> - **伪冗余/互补**：图形对新手无法独立理解，需文字解读配合（如 Munzner 有效性排序图 + 口语讲解）→ Mayer 多媒体原则（有益），非冗余效应。保留。
>
> **判定方法**：遮住文字只看图，新手能否独立理解 ≥ 80%？能 → 真冗余；不能 → 互补，豁免 Q1。

### 1.3 判定组合与严重度

| 标记组合 | 综合严重度 | 说明 |
|:---|:---:|:---|
| `[SCOPE_CREEP]` | 🔴 高 | 引入了教学大纲未规划的新概念，必须处置 |
| `[SEDUCTIVE_DETAIL_BLOCK]` + `[REMOVABLE]` | 🟡 中 | 有趣但非必要，强烈建议移除或降级 |
| 仅 `[SEDUCTIVE_DETAIL_BLOCK]`（删除会损失理解度） | 🟢 低 | 保留但压缩 |

---

## §1.4 可取困难豁免通道 (Desirable Difficulty Exemption)

> **→ SSOT**: `rule_cognitive_efficiency.md` §1（DD-1/DD-2/DD-3 校验矩阵）+ §2（Paas 公式）。当 §1.2 Mayer 三问标记某块为可删除时，加载该规则执行二次校验，通过则重分类为 `[GERMANE_LOAD]`。

---

## §2 处置策略

| 标记 | 处置方式 |
|:---|:---|
| `[SEDUCTIVE_DETAIL_BLOCK]` + `[REMOVABLE]`（未通过 §1.4） | **删除**或**降级**为脚注/课后延伸/`<!-- EXTENDED_READING: ... -->` 注释 |
| `[SCOPE_CREEP]` | **迁移**到对应周次的模块中；或**转化为课程预告**（使用 `rule_prerequisite_awareness.md` §1.2 策略 A 日常语言替代） |
| 仅 `[SEDUCTIVE_DETAIL_BLOCK]`（删除会损失理解度） | **保留**，但压缩为 **≤ 3 句**的精要版本，删除所有非核心细节 |
| `[GERMANE_LOAD]`（通过 §1.4 豁免） | **保留**，不压缩。审计报告标注 `[DD-EXEMPT]` |

---

## §3 写作时自检

在 `/write` Phase 2 每完成一个 `##` 模块后，对本模块所有人文标签块执行 Mayer 三问：

> _"如果我把这段完全删掉，学生对本模块核心概念的理解会下降吗？如果答案是'不会，但会少了一些趣味'——这就是诱惑性细节。"_

---

## §4 禁止行为

- ❌ 在单个 `##` 模块中引入 ≥ 2 个模块教学目标未涉及的独立子概念（触发 `[SCOPE_CREEP]`）
- ❌ 以"丰富度"或"有趣"为由保留与教学目标无直接因果关系的大段扩展（> 200 字）
- ❌ 将 `[DID YOU KNOW]` 块作为知识炫技的容器——该标签的功能是"惊喜感 + 记忆锚点"，不是"百科全书补丁"

---

## §5 与现有规则的关系

| 本规则条款 | 互补的现有规则 | 关系 |
|:---|:---|:---|
| §1 模块级一致性 | `rule_content_depth.md` §4.1 IAR | IAR 在段落级检测冗余段（R）；本规则在标签块/模块级检测目标越界 |
| §1 诱惑性细节 | `audit_standard.md` Part C §10 Mayer 修饰语删除测试 | 现有 §10 在**句级**执行修饰语删除测试；本规则在**块级**执行整段价值判定 |
| §1.4 可取困难豁免 | `rule_cognitive_efficiency.md` §1 二次校验 | 本规则 §1.4 为纯指针；完整 DD 校验矩阵与 Paas 公式 SSOT 在该规则 |
| §2 SCOPE_CREEP | `rule_outline_alignment.md` O1 steps 结构覆盖 | O1 检查"大纲该有的是否有"（缺失检测）；本规则检查"大纲没说的是否多了"（溢出检测） |
| §3 写作时自检 | `rule_script_clarity.md` §2 一段一事 | 一段一事在段落职能层面检查；本规则在教学目标对齐层面检查 |
