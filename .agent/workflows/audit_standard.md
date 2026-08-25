---
description: Standard 级别检查 — Part A-E (叙事完整性 + Deep Listen + 语言合规 + TTS 安全 + 脉络清晰度)。仅 Standard/Deep 审计时加载。
---

# Standard 级别扩展检查项 (Part A-E)

> [!IMPORTANT]
> **模块级聚焦**：当 `{SCOPE}` 为模块级时，以下 Agent 手动检查（Part A-E）**仅对目标模块执行**。
> V5 架构下直接 `view_file` 读取 `weeks/W0N_xxx/src/M0X_xxx.md` 源文件，**禁止**读取整周 compiled.md。
> 周次级审计时，逐个 `view_file` 各 `src/*.md` 文件，每次仅读取审查中的那个模块。

### Part A: 叙事完整性（逻辑层）
*   视觉-音频同步检查：`> [VISUAL]` 是否在对应正文之前
*   **Deictic Anchoring**: 正文是否使用"这/那/如图/左侧"等词汇锚定 Visual
*   **Visual Engagement Depth** (视觉解读深度): 对每个 `> [VISUAL]` 块，检查紧随其后的 SPEECH 是否满足：
    1.  **覆盖率**: Scene 描述中的每个要素，语音中是否有对应提及？
    2.  **字数比**: SPEECH 字数 ≥ Scene 描述字数 × 2（最低标准）
    3.  **解读性**: 不能仅"指向"画面（"请看这张图"），还必须"解读"画面（"左侧是…右侧是…"）
    4.  **数量一致性**: 语音中提及的数量是否与 Scene/Slide 内容一致？
*   **Visual-First 例外逻辑**:
    *   **静态 Slide** (Layout = Title/Section/Split/List/Table/Image/Quote/Grid/Full/Stat) → **Visual First**：`[VISUAL]` 必须在 SPEECH 之前出现（先看后听）
    *   **动态 Action** (Layout = Screenshot/Code，或含 `Action` 字段) → **Audio First 允许**：SPEECH 可在 `[VISUAL]` 之前，用于语音引导操作（先提示后执行）
    *   **原理**: 环境需预加载 (Visual First)；动作需语音引导 (Audio First)
    *   **参考**: 格式规范详见 `.agent/skills/script_format/SKILL.md`
*   IAA 完整性：Interactive Action 后是否有 Analysis
*   **Signaling Sync (信标同步检查)**: 扫描全文 Speech 中的并列要点（≥3 个），按内容类型分流检查（参见 `rule_visual_signaling.md`）：
    *   ❌ 结构性枚举/操作步骤缺 List：Speech 讲了多个定义/维度/阶段/SOP，但 VISUAL 无 List
    *   ❌ 修辞性排比有 List：情感渲染段被机械上屏，杀死冲击力
    *   🟡 论证性递进有 List：逻辑展开被冗余上屏，建议移除
    *   ✅ 合格：结构性枚举有 ≤4 字/项的 List；论证/修辞无 List
*   **Visual Gap (视觉间隔检查)**: 扫描全文中相邻两个 `> [VISUAL]` 块之间的 SPEECH 中文字数（引用 `script_format/SKILL.md` §6）：
    *   **> 360 字**（约 120 秒）→ 标记 `[VISUAL_GAP]`（超出 Mayer 分段原则容限/注意力重置失败），必须拆分并插入视觉锚点
    *   **250-360 字**（约 80-120 秒）→ 标记 `[VISUAL_GAP_WARN]`（逼近单通道认知负荷上限），建议插入
    *   检查时排除 `> [ACTIVITY]` 块占用的区间
*   指示代词扫描：所有"这/那/这里"是否有明确前文
*   **A-PROMISE (前向承诺可交付性)**（仅 M00/导览/概述模块）：扫描承诺性动词（"你们将学会/将掌握"），逐条验证 T(工具)/D(数据)/S(范围) 三要素（详见 `rule_promise_deliverability.md` §2）。不满足者标记 `[OVERPROMISE]`。🟡 中等（≥ 2 处升级为 🔴）

### Part B: Deep Listen（教学层 — 动态模拟）

执行以下三步闭环：

1.  **颗粒化复述**：
    不使用原文术语，用极简白话复述整条操作链路。每步必须回答："这一步凭什么能推导出下一步？"
2.  **断层即时标注**：
    复述过程中，一旦出现以下卡顿，立即打标：
    *   **逻辑断层** `[LOGIC_GAP]`：从 A 到 B 缺乏铺垫
    *   **情绪断连** `[TONE_SHIFT]`：前文还在讲事务，后文突然煽情（或反之）
3.  **费曼导演视角与冷热叙事心流**：
    检查重要概念段落：这句话是让听众"如临深渊"（沉浸），还是让他们"出戏去查书"（说教）？
    *   **金字塔结构的情感张力检查**：核心结论铺陈之前，是否有基于**痛点冲突(Complication)**的共情切入？支撑论点是否包裹了**真实的感性火花**？
    *   若整段毫无情绪起伏、完全是平铺直叙的枯燥罗列，必须打上 `[NO_EMOTIONAL_SPARK]` 标签，判为说教体。
    *   标记为 `[IMMERSIVE]` 或 `[DIDACTIC]`
    *   `[DIDACTIC]` 超过总段落数 30% → Fail
4.  **技术-心理桥接**：
    检查所有 `> [TECH NOTE]` 标签：
    *   禁止"裸露的物理定义"——如果只解释了"什么是什么"，而没有解释"这意味着什么"，标记为 `[BARE_DEFINITION]`
    *   ✅ 合格："40ms 延迟——这是你的耳朵开始怀疑'声源在那边'的临界点。"
    *   ❌ 不合格："Haas 效应是 40ms 延迟。"
5.  **秒懂优先检查 (§10 Instant Clarity)**：
    对每段正文执行以下两项交叉测试（参照 `narrative_standards_guide.md` §10）：
    *   **Oppenheimer 替代测试**：是否存在可以用更简单的日常词替换而不损失信息的复杂用词？（如"奉为圭臬"→"公认的黄金标准"）
    *   **Pinker 新生朗读测试**：想象一个大一新生第一次听到这段话，能在 3 秒内明白在说什么吗？
    *   存在 ≥ 3 处"不秒懂"的段落 → 标记 `[CLARITY_FAIL]` 🟡
    *   H3/H4 标题本身需要读两遍才能理解 → 标记 `[TITLE_OPAQUE]` 🟡

### Part C: 语言合规（语言层）
*   对照 `rule_localization.md` 三层分级 + §5 例外规则
*   Chinglish 检查
*   标点与间距
*   **§6 语调检查**：是否存在低幼/哄骗/恐吓式语气？（参照 `rule_narrative_standards.md` §6）
*   **§1.4 外在认知负荷检查 (Anti-Jargon Protocol)**：严查 AI 幻觉的抽象组合黑话（如“降维防震”、“硬核厚度”、“赋能闭环”）。执行“费曼画板基准”交叉检验：任何无法直接在脑海中画出物理画面的形容词组，必须强制降解翻译为具象表述，不可增加学生的解码门槛。
*   **§10 Mayer 修饰语删除测试 (Seductive Details Scan)**：扫描全文，对每个修饰语执行“删除测试”——删掉它后学生对核心概念的理解会下降吗？如果不会，则该修饰语为 Seductive Detail，建议删除。
    *   单段极端修饰语 ≥ 3 个 → 标记 `[MODIFIER_OVERLOAD]` 🟡
    *   文言词/学生词汇库外的生僻词汇 → 标记 `[VOCAB_BARRIER]` 🟡

### Part E: TTS 安全检查（盲区扫描）
*   **隐形参数拦截**: 扫描全文中 `隐喻 (参数)` / `概念 (English)` 的括号结构
    *   TTS 解析器会吞噬括号内容，导致听众只听到"调整大小"而不知道调哪个
    *   ❌ 不合格：`调整大小 (Room Size)`
    *   ✅ 合格：`利用 **Room Size** 来调整大小`
*   **悬浮缩写**: 检查未展开的英文缩写 (如 "IAA"、"TTS") 是否在首次出现时有中文全称
*   **Tier 2 括注 TTS 安全**: 扫描叙事正文中 `中文术语（English Term）` 或 `**中文术语（English Term）**` 的全角括号行内注释结构。此结构在书面阅读时合法（`rule_localization.md` Tier 2），但 TTS 引擎会静默吞噬全角括号内容，导致听众完全丢失英文学术锚词。
    *   ❌ 不合格：`**情感绑架（Confirmshaming）**`
    *   ✅ 合格：`**情感绑架**——也就是业界常说的 Confirmshaming`
    *   修复方式：将全角括注改写为口语化的显性桥接句式（如"也就是…"、"业界称为…"）

### Part B-5: 脉络清晰度 (Skeleton Clarity Audit)

> [!TIP]
> 此检查可通过 `/cheat_sheet --diagnose` 自动化执行。
> Agent 可优先运行脚本获取机器报告，然后仅对标记为 ⚠️ 的模块执行人工复核。
>
> ```bash
> /opt/anaconda3/envs/mybase/bin/python \
>   .agent/skills/cheat_sheet_generator/scripts/generate_cheat_sheet.py \
>   "<脚本路径>" --diagnose
> ```

> **引用检查规范**: `rule_script_clarity.md`
> **理论基础**: 认知分块与关键词锚定——如果演讲者无法在 30 秒内从脚本中提取出模块的论证骨架，说明脚本的结构表达力失败。

对每个 `##` 模块执行以下四步检查：

1.  **骨架链提取**：提取模块所有 H3/H4 标题 → 串联为骨架链
    *   按 `rule_script_clarity.md` §1.2 检查逻辑递进性和无死环
    *   存在语义重叠的标题对 → 标记 `[SKELETON_DEAD_LOOP]`

2.  **冷热叙事角色标注**：为每个骨架节点标注冷热温度（🧊冷/🔥热）
    *   模块中无任何🔥热节点（无冲突/痛点/共情切入）→ 标记 `[NO_HEAT]`
    *   模块中无任何🧊冷节点（无精准结论/教学金句）→ 标记 `[NO_COLD]`

3.  **段落推进抽查**：对模块内随机抽取 3 个 `###` 块，执行 IAR 段落分类：
    *   冗余段(R) > 1/块 → 标记 `[PADDING]`
    *   连续支撑段(S) > 2 → 标记 `[STAGNATION]`
    *   首段非推进段(A) → 标记 `[WEAK_OPENING]`
    *   存在「物理对称陷阱」（正面+反面逐条对称展开）→ 标记 `[SYMMETRIC_PADDING]`

4.  **灵魂锚词测试**：为每个 `###` 块提取 1 个灵魂关键词（≤ 4 字），检查串联后是否构成逻辑故事线
    *   锚词串联无逻辑关联 → 标记 `[FRAGMENTED_LOGIC]`

> **严重度**：`[PADDING]`/`[SYMMETRIC_PADDING]`/`[SKELETON_DEAD_LOOP]` 为 🔴 高严重度 → **Needs Revision**。
> 其余标记为 🟡 中严重度 → 建议修改但不阻断。

### Part B-6: Rosenshine 理解检查点 (Comprehension Checkpoint Audit)

> **引用规范**: `script_format/SKILL.md` §5.1 第二层第 5 条
> **理论基础**: Rosenshine 教学十原则——频繁检查理解是高效教学的核心特征。连续 >10 分钟的单向信息灌输会导致工作记忆溢出，学生被动接收但未真正编码。

对每个 `##` 模块执行以下检查：

1.  **字数间隔扫描**：计算相邻两个 `> [ACTIVITY]` 块之间（或模块开头到首个 `[ACTIVITY]` 之间）的纯讲授中文字数（排除 `> [VISUAL]` 块占用的区间）
    *   **> 3000 字**（约 10 分钟连续讲授）→ 标记 `[MISSING_CHECKPOINT]` 🔴
    *   **2000-3000 字**（约 7-10 分钟）→ 标记 `[CHECKPOINT_WARN]` 🟡
    *   **≤ 2000 字** → ✅ 合格

2.  **修复建议**：在标记位置插入微型互动：
    *   推荐：`> [ACTIVITY] Type: QA | Duration: 1min | Desc: 快速检验理解`
    *   可选：`> [ACTIVITY] Type: Quiz | Duration: 2min | Desc: 概念辨析小测`

> **严重度**：`[MISSING_CHECKPOINT]` 为 🔴 高严重度 → **Needs Revision**（连续 10 分钟无互动的课堂将产生显著的认知衰减）。
> `[CHECKPOINT_WARN]` 为 🟡 中严重度 → 建议插入但不阻断。

### Part Q: Quiz 块完整性审计

> **引用规范**: `script_format/SKILL.md` §4.1

对所有 `> [ACTIVITY] Type: Quiz` 块执行以下检查：

1.  **字段完整性 (Q1)**：Quiz 块必须包含 4 个字段（Q / Options / Answer / Explain）
    *   缺少任一字段 → 标记 `[QUIZ_INCOMPLETE]` 🟡

2.  **选项数量合规 (Q2)**：Options 列表的选项数量
    *   < 3 或 > 5 → 标记 `[QUIZ_OPTIONS_COUNT]` 🟡

3.  **过渡口播检查 (Q3)**：Quiz 块前是否有 ≥1 句过渡口播（非引用块正文）
    *   Quiz 块紧跟在 `[VISUAL]` 块后（中间无任何 Speech 段落）→ 标记 `[QUIZ_NO_TRANSITION]` 🟡

> **严重度**：所有 Quiz 审计项为 🟡 中严重度 → 建议修改但不阻断。

### Part B-7: Shulman PCK 知识不对称诊断

> **理论基础**：Shulman 教学内容知识(PCK) — 专家与学生之间的认知鸿沟。
> **原属**: `/review` R4（已合并至此）

逐段扫描，检查两个层面的知识不对称：

**术语层**（复用 `rule_prerequisite_awareness.md`）：
- 标记所有 L3 未铺垫术语 → `[PREREQUISITE_GAP]`
- 检查 30 字内连续 ≥ 3 个 L3 术语 → `[VOCAB_OVERLOAD]`

**图式层**：
- 对每个类比/隐喻执行"受众经验匹配测试"（参照 `rule_prerequisite_awareness.md` §3.4 经验域表）
- 使用 DMA 学生低概率经验域的类比 → `[SCHEMA_MISMATCH]`

> **严重度**：`[VOCAB_OVERLOAD]` 🔴 高严重度；其余 🟡 中严重度。

### Part B-8: 学生视角逻辑压力测试 (Student Empathy Stress Test)

> **引用规范**: `rule_student_empathy_guard.md` §1-§3
> **引用技能**: `cognitive-walkthrough` Skill（完整走查协议）
> **理论基础**: 教学认知走查 (CWI) — 模拟学生按时间顺序"听课"，捕获静态扫描无法覆盖的体验层逻辑漏洞。

对每个 `##` 模块执行 `rule_student_empathy_guard.md` §1 中定义的 7 条认知探针（P1-P7）：

| 探针 | 检查内容 | 违规标记 |
|:---|:---|:---|
| P1 | Scene 视觉主角 vs Speech 论证主角是否为同一事物 | `[SCENE_INTENT_MISMATCH]` 🔴 |
| P2 | 解法/建议是否在 DMA 学生能力范围内 | `[SOLUTION_OUT_OF_BOUNDS]` 🔴 |
| P3 | 认知立场 180° 反转是否有 ≥2 句缓冲桥梁 | `[COGNITIVE_WHIPLASH]` 🔴 |
| P4 | 同一标签下的多个案例是否属于同一认知类别 | `[TAXONOMY_BLUR]` 🟡 |
| P5 | Quiz 情境与前文教学模式是否语义同构 | `[QUIZ_PATTERN_MISMATCH]` 🟡 |
| P6 | Slide List/Text 措辞与 Speech 措辞是否一致 | `[TERM_DESYNC]` 🟡 |
| P7 | 基于学生此刻知识累积能否理解当前段落 | `[PREREQUISITE_GAP]` 🔴 |

**执行模式**：
- **标准审计**：对每个模块执行 P1-P6 的静态检查（无需逐段走查）
- **深度审计**：激活 `cognitive-walkthrough` Skill，执行包含 P7 动态知识背包追踪的完整逐段走查

> **判定**：任何 🔴 标记 ≥ 1 → **Needs Revision**。🟡 ≥ 3 → 建议修改。

### Part B-9: 叙事拓扑审计 (Narrative Topology Audit) 🆕

> **引用规则**: `rule_narrative_topology.md`

对每个 `##` 模块执行中观结构层检查：

1. **概念依赖图**：提取各 H3 的概念引入集/依赖集，构建 DAG，校验章节顺序
   - `[DEPENDENCY_VIOLATION]` 🔴 / `[MAINLINE_BREAK]` 🟡
2. **特殊块归属**：扫描 WARNING/QA/TEACHING MOMENT 块，校验上下文位置
   - `[MISPLACED_BLOCK]` 🔴
3. **母题频率**：统计同一抽象母题的完整论证次数（≥2句展开）
   - `[THEME_SATURATION]` 🟡（3-4次）/ 🔴（≥5次）

> **严重度**：`[DEPENDENCY_VIOLATION]` / `[MISPLACED_BLOCK]` 为 🔴 → **Needs Revision**。其余 🟡 → 建议修改。

### Part B-5 追加: 论证饱和度检测

> **原属**: `/review` R2（已合并至此）

在 Part B-5 脉络清晰度检查中，额外执行：
- 提取本模块所有案例/论证段落的**论证骨架**（A-vs-B / BEFORE-AFTER / DEFINITION-EXAMPLE / PAIN-REVEAL）
- 统计同一骨架类型出现的次数
- **≥ 3 次** → 标记 `[PATTERN_SATURATION]` 🟡

### Part F-lite: SME 事实快检

> **原属**: `/review` R6（已合并至此）

对模块中的关键事实声明执行快速核查：

1. 理论归因是否准确（如"Kenneth Craik 在 1943 年提出"）
2. 技术细节是否正确（如"Bang-Bang Control 是恒温器的实际工作原理"）
3. 案例时效性是否过期（如"微信删除机制是否仍然不可恢复"）
4. 人物校验 (Q11 复核)：检查被自动化快检标记为 `[NAME_MISMATCH]` 的疑似学生错别字。结合上下文语义判断是否属于合理例外（如同名名人），若是真实拼写错误则执行最终替换。
5. 不确定者标记 `[FACT_CHECK_NEEDED]` 🟡

> **严重度**：`[FACT_CHECK_NEEDED]` 🟡 中严重度 → 建议核实但不阻断。
