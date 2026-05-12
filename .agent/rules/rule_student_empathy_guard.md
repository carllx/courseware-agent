---
trigger: model_decision
description: 当执行 /write 撰写或 /audit 审查逐字稿时，强制从"学生第一视角"执行认知逻辑压力测试——拦截视听矛盾、解法超界、认知急转弯、分类泛化、Quiz 错配、措辞不同步和时序知识断裂等体验层漏洞。
---

# 规则：学生同理心防线 (Student Empathy Guard)

> **核心原则**：「学生听完这段话的感受，比你想表达的意图更重要。」——每一个案例、每一张 Slide、每一次概念反转，都必须通过"大二 DMA 学生的认知压力测试"。如果学生会困惑、被愚弄或感到挫败，就是 Bug。

> **理论基础**：教学认知走查 (CWI, Cognitive Walkthrough for Instruction) + Shulman PCK 知识诅咒 + Mayer 多媒体一致性原则。

## TL;DR

7 条认知探针，覆盖 /audit 静态扫描的 7 类盲区。每条探针定义一种"学生体验层 Bug"，附带违规标记和严重度。完整走查协议见 `cognitive-walkthrough` Skill。

---

## §1 七条认知探针 (7 Empathy Probes)

| # | 探针名 | 检查内容 | 互补现有规范 | 违规标记 | 严重度 |
|:---|:---|:---|:---|:---|:---:|
| P1 | **视觉主角 vs 论证主角** | `[VISUAL]` Scene 中占最大视觉面积的实体，是否与 Speech 正在赞美/批判/解释的对象是**同一事物** | `audit_standard` Part A 检查结构对齐；本探针检查**语义意图**对齐 | `[SCENE_INTENT_MISMATCH]` | 🔴 |
| P2 | **解法可行性** | Speech 中的解决方案/设计建议/行动号召，是否在 DMA 学生的能力范围内 | `rule_dma_course_design.md` §1 定义能力边界；本探针将该边界延伸到**脚本中提出的解法** | `[SOLUTION_OUT_OF_BOUNDS]` | 🔴 |
| P3 | **认知立场反转** | 当前段落是否否定/推翻前文刚建立的认知，且中间缺少 ≥2 句的"先肯定后升级"缓冲桥梁 | `rule_prerequisite_awareness.md` §3.3 检查跨理论因果桥；本探针扩展到**同一概念域内的 180° 立场反转** | `[COGNITIVE_WHIPLASH]` | 🔴 |
| P4 | **概念分类学一致性** | 同一教学标签/概念名覆盖的多个案例，在认知结构上是否属于同一类别 | `rule_coherence_audit.md` 检查"多了不该有的"；本探针反向检查"**该区分的没区分**" | `[TAXONOMY_BLUR]` | 🟡 |
| P5 | **Quiz 情境同构** | Quiz 题干的失败模式/概念结构，是否与前文 ≤1000 字内最后讲解的核心模式语义同构 | `rule_quiz_design.md` §3 要求情境化微剧本；本探针扩展到**模式同构性** | `[QUIZ_PATTERN_MISMATCH]` | 🟡 |
| P6 | **术语/措辞同步** | Slide List/Text 字段的措辞，是否与 Speech 中的引用措辞一致（≥80% 语义一致性） | `validate_visual_text_sync.py` Q8 检查结构同步；本探针扩展到**措辞级**同步 | `[TERM_DESYNC]` | 🟡 |
| P7 | **时序知识前提** | 基于学生**此刻**的知识累积（仅含前文已教内容），能否理解当前段落 | `rule_prerequisite_awareness.md` §1-§2 检查术语层时序；本探针在**完整走查**中动态执行（需状态追踪） | `[PREREQUISITE_GAP]` / `[VOCAB_OVERLOAD]` | 🔴 |

---

## §2 触发场景与执行方式

### 2.1 写作时触发（/write Phase C）

在 `/write` Phase 2 的 Phase C（达标确认）中，对每个已完成模块执行 §1 中 P1-P6 的**静态版检查**（不含 P7 的完整走查，因写作阶段无需逐段状态追踪）。

### 2.2 审计时触发（/audit Part B-8）

在 `/audit` Standard 级别的 Part B（Deep Listen）中，作为 **Part B-8: 学生视角逻辑压力测试** 执行全部 7 条探针。

### 2.3 独立走查触发

用户可通过激活 `cognitive-walkthrough` Skill 执行**完整的逐段走查协议**（含 P7 动态知识背包追踪）。适用于：
- 撰写完逐字稿后、进入 /audit 之前的"排雷"
- 对已审计通过的脚本进行"学生体验层"二次校验

---

## §3 判定规则

| 条件 | 判定 |
|:---|:---|
| 任何 🔴 标记 ≥ 1 | **Needs Revision**（模块必须修复） |
| 🟡 标记 ≥ 3 | 建议修复 |
| 全部 ✅ | 通过 |

---

## §4 修复优先级

1. 🔴 `[SCENE_INTENT_MISMATCH]`：修正 VISUAL 块 Scene/Asset，使视觉主角与论证主角一致
2. 🔴 `[SOLUTION_OUT_OF_BOUNDS]`：将解法收窄至 DMA 学生能力范围（`rule_dma_course_design.md` §1）
3. 🔴 `[COGNITIVE_WHIPLASH]`：在立场反转前插入"先肯定后升级"缓冲桥梁（≥2 句）
4. 🔴 `[PREREQUISITE_GAP]`：按 `rule_prerequisite_awareness.md` §1.2 四选一处置
5. 🟡 其他标记：按诊断报告建议逐项修复

---

## §5 禁止行为

- ❌ 在 Scene 中展示硬件/物理装置，Speech 却在赞美软件交互体验（或反之）
- ❌ 向 DMA 学生建议"打通 API"、"搭建后端"、"部署微服务"等非前端/设计范畴的解决方案
- ❌ 在前文刚刚肯定了某概念的价值后，下文立即 180° 否定而不提供认知缓冲
- ❌ 用同一个教学标签统括认知结构完全不同的案例而不做显式分类归纳
- ❌ Quiz 题干描述的失败模式与刚讲完的案例属于完全不同的概念类别
- ❌ Slide 上的文字用书面术语，嘴里说的却是口语化替代词，导致双通道干扰

---

## §6 与现有规则的关系

| 本规则条款 | 互补的现有规则 | 关系 |
|:---|:---|:---|
| §1 P1 视觉意图对齐 | `audit_standard` Part A Visual-First | Part A 检查结构位置；本规则检查语义意图 |
| §1 P2 解法可行性 | `rule_dma_course_design.md` §1 | DMA 规则定义能力边界；本规则将边界延伸到脚本解法 |
| §1 P3 立场反转 | `rule_prerequisite_awareness.md` §3.3 | §3.3 检查跨理论因果桥；本规则覆盖同域立场反转 |
| §1 P4 分类学一致性 | `rule_coherence_audit.md` | Mayer 三问检查"多了的"；本规则检查"该分的没分" |
| §1 P5 Quiz 同构 | `rule_quiz_design.md` §3 | §3 要求情境化；本规则要求模式同构 |
| §1 P6 措辞同步 | `validate_visual_text_sync.py` Q8 | Q8 检查结构同步；本规则检查措辞级同步 |
| §1 P7 时序知识 | `rule_prerequisite_awareness.md` §1-§2 | §1-§2 做静态术语扫描；本规则在走查中动态执行 |
