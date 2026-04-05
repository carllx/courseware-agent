---
description: 审查脚本与课程配置的质量（分级审计：快速/标准/深度）
---

# /audit 工作流 (通用版)

> **输入**: 课程名 + 脚本文件路径或教学单元 ID
> **输出**: 审计报告

## 审计级别

| 级别 | 命令 | 执行范围 | 典型场景 |
|:---|:---|:---|:---|
| **Quick** | `/audit --quick` | 自动化验证 + 规范合规 + 视觉完整 + 时长估算 + 大纲一致性 | 写完一篇脚本后的快速自检 |
| **Standard** (默认) | `/audit` | Quick + 叙事质量 + 语言合规 + TTS 安全 | 常规脚本审查 |
| **Deep** | `/audit --deep` | Standard + 知识面覆盖率 + OBE 对齐 + course.yaml 结构校验 | 里程碑节点的全量审计 |

### 输入模式

| 模式 | 输入文件 | 限制 | 说明 |
|:---|:---|:---|:---|
| **Full** (默认) | `weeks/*/src/*.md` | 无 | 完整审计 |
| **Speech-Only** | `.txt` (TTS 导出) | 仅 Standard 级别的 Part B + C + E | 仅审查语言流 |

**Speech-Only 模式约定**：
*   `.txt` 必须由 `validate_script_length.py --dump-text`（**不加** `--blind-mode`）导出，以保留 `[SLIDE #N: ID]` 溯源标记
*   `--blind-mode` 导出的纯净文本**禁止**用于审计（无法溯源）
*   报告中所有问题标注必须引用 `[SLIDE #N]` 锚点，格式：`→ 源文件：Sxx_Name.md，Slide ID: Sxx_xxx`

---

## 执行步骤

### Step 0: 范围解析（必须首先执行）

解析用户指定的审计范围，确定过滤变量：

| 用户输入 | `{SCOPE}` | `{WEEK_FILTER}` | `{MODULE_FILTER}` | 说明 |
|:---|:---|:---|:---|:---|
| `/audit --course "X"` | 课程级 | _(空)_ | _(空)_ | 全课程全量审计 |
| `/audit --course "X" --week 1` | 周次级 | `--week 1` | _(空)_ | 仅审 W01 全部模块 |
| `/audit --course "X" --week 1 --module "视觉系统"` | 模块级 | `--week 1` | `--module "视觉系统"` | 仅审 W01 的指定模块 |

**后续所有脚本命令**必须在 `--course` 后追加 `{WEEK_FILTER}`。Agent 手动检查步骤仅读取目标范围的脚本内容。

> [!IMPORTANT]
> **V5 架构聚焦规则**：当 `{SCOPE}` 为模块级时，Agent 手动检查（Q4/Q6/Part A-E）应**直接读取 `weeks/W0N_xxx/src/M0X_xxx.md` 源文件**，而非 compiled.md，以避免加载整周全部模块的文本浪费上下文。

### Step 1: 定位文件与模式判断
运行 `extract_week.py --week N` 提取目标周的教学信息（Quick/Standard 级别替代加载全量 `course.yaml`，ADR-021 Phase 1）：

```bash
/opt/anaconda3/envs/mybase/bin/python 《课程》/extract_week.py --week N
```

找到目标脚本。
*   若输入为 `.md` → **Full 模式**
*   若输入为 `.txt` → **Speech-Only 模式**（跳过 Step 2、Part A、Part D）

### Step 2: 自动化验证 (Pre-Flight)

> **周次/模块级审计时**：`validate_project.py` 自动跳过全局验证器（syllabus/knowledge）。

```bash
# 从 Workspace 根目录运行：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_project.py \
  --course "<课程>" {WEEK_FILTER}

# Draft 模块追踪：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/check_draft_status.py \
  --course "<课程>" {WEEK_FILTER}
```

---

## Quick 级别检查项

> **Quick = 原 `/validate_script` 的全部检查。** 写完脚本后的第一道质量门。

### Q1: 规范合规性检查

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_spec.py \
  --course "<课程>" {WEEK_FILTER}
```
检查：知识标签白名单、VISUAL/ACTIVITY 块完整性、Layout 类型、Slide ID 唯一性、旧格式残留。

### Q2: 视觉素材完整性

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_visuals.py \
  --course "<课程>" {WEEK_FILTER}
```
交叉比对脚本引用与物理文件。

### Q3: 时长估算

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" {WEEK_FILTER}
```

> **口述字数准确性说明**：时长估算器**仅统计口述内容**的中文字数。以下内容已被自动排除：
> - YAML Frontmatter（`---` 之间的元数据）
> - `> [VISUAL]` 块（仅计为 Slide 数 +1，标题/描述文字不计入）
> - `> [ACTIVITY]` 块（单独计为活动时长，不计入口述字数）
> - `> [!NOTE]` 导读块（归类为引用块，不计入口述字数）
> - Markdown 标题行（`##`/`###`）被解析为 HEADER 类型，不计入口述字数

> [!CAUTION]
> **Q3 短路规则（字数优先门控）**：若 Q3 时长估算中**任何模块**存在 ❌（`fill_ratio < 0.8`），
> 则审计立即输出 `Needs Revision (字数未达标)`，**跳过** Q2 视觉完整性、Q6 视觉密度、
> 以及 Epilogue E3 链接验证。字数达标是最高优先级的质量门，视觉完整性不得在字数未达标时消耗审计注意力。

### Q4: 叙事质量抽查 (Agent 手动)

Agent 需对以下项进行人工判断：

**A: 过渡检查**
*   段落之间是否使用了禁忌过渡（"下面我们来看"/ "接下来介绍"）？
*   是否使用了推荐过渡技巧（悬念反问/听觉桥接/递进对比/回环）？

**B: 反翻译腔**
*   是否存在超过 20 字未断句的长句？
*   是否存在禁忌词（"进行/实现/功能/相关的/在…的情况下"）？

**C: 朗读测试**
*   选取 3 段正文，模拟朗读节奏是否流畅。

### Q5: 大纲一致性验证 (Outline Consistency)

> **引用检查表**: `.agent/rules/rule_outline_alignment.md`

Agent 需对照 `extract_week.py --week N` 输出的 `calendar` 条目，逐项执行 `rule_outline_alignment.md` 中定义的 O1-O7 + O9 + O10 检查（O9 为模块字数预算达标，ADR 020；O10 为人文标签密度）。

> 任何 🔴 高严重度项未通过 → 报告结论为 **Needs Revision**。

> [!IMPORTANT]
> **DRP 审计时强制**：当模块填充率 < 80% 时，审计报告必须输出**具体的 DRP 执行指令**，而非仅标记 "Needs Revision"。
> DRP 级别判定详见 `rules/rule_content_depth.md` §3 审计时的 DRP 级别判定表。

### Q6: 视觉密度量化检查

> **引用规范**: `script_format/SKILL.md` §6 视觉密度标准

对每个 `##` 模块统计以下指标：

| 检查项 | 标准 | 不合格处理 |
|:---|:---|:---|
| **模块 Slide 数** ≥ `⌈讲授净分钟数 ÷ 3⌉` | §6.2 硬性底线 | 标记 `[VISUAL_DENSITY_LOW]`，Needs Revision |
| **最大连续口述间隔** ≤ 360 字 | §6.3 禁止事项 | 标记 `[VISUAL_GAP]`，指出位置 |
| **装饰性视觉** = 0 | §6.3 连贯性原则 | 标记 `[DECORATIVE_VISUAL]`，建议替换或删除 |

计算方法：
*   讲授净分钟数 = 模块 `<!-- BUDGET -->` 标注中的字数 ÷ 语速常量（180 字/分钟）
*   Slide 数 = 模块内 `> [VISUAL]` 块的数量
*   连续口述间隔 = 相邻两个 `> [VISUAL]` 块之间的 SPEECH 中文字数

### Q7: 退化检测 (Degeneration Gate)

> **引用规范**: `rule_narrative_standards.md` §7.4 反退化规则

Q7 与 Q3 共享同一命令输出——`--module-breakdown` 模式中的 `[DEGEN]` 标记：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" {WEEK_FILTER} --module-breakdown
```

检查输出末列是否存在 `[DEGEN]` 标记。任何模块存在 🔴 退化 → **Needs Revision (文本退化)**，短路后续 Standard/Deep 检查。

---

## Standard 级别检查项 (Quick + 以下)

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
*   **Bullet Sync (要点同步检查)**: 扫描全文 Speech 中的结构化要点（≥3 个并列项、编号列表、阶段划分、考核/评分/任务说明），检查其紧邻的 `> [VISUAL]` 块是否包含 `**List**` 字段将要点同步展示在 PPT 上。
    *   ❌ 不合格：Speech 讲了 4 个阶段，但 VISUAL 块只有氛围 Scene，无 List
    *   ✅ 合格：Speech 讲了 4 个阶段，VISUAL 块的 List 逐条对应
*   **Visual Gap (视觉间隔检查)**: 扫描全文中相邻两个 `> [VISUAL]` 块之间的 SPEECH 中文字数（引用 `script_format/SKILL.md` §6）：
    *   **> 360 字**（约 120 秒）→ 标记 `[VISUAL_GAP]`，必须拆分并插入视觉锚点
    *   **250-360 字**（约 80-120 秒）→ 标记 `[VISUAL_GAP_WARN]`，建议插入
    *   检查时排除 `> [ACTIVITY]` 块占用的区间
*   指示代词扫描：所有"这/那/这里"是否有明确前文

### Part B: Deep Listen（教学层 — 动态模拟）

执行以下三步闭环：

1.  **颗粒化复述**：
    不使用原文术语，用极简白话复述整条操作链路。每步必须回答："这一步凭什么能推导出下一步？"
2.  **断层即时标注**：
    复述过程中，一旦出现以下卡顿，立即打标：
    *   **逻辑断层** `[LOGIC_GAP]`：从 A 到 B 缺乏铺垫
    *   **情绪断连** `[TONE_SHIFT]`：前文还在讲事务，后文突然煽情（或反之）
3.  **费曼导演视角与 SCQA 心流**：
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

### Part C: 语言合规（语言层）
*   对照 `rule_localization.md` 三层分级 + §5 例外规则
*   Chinglish 检查
*   标点与间距
*   **§6 语调检查**：是否存在低幼/哄骗/恐吓式语气？（参照 `rule_narrative_standards.md` §6）

### Part E: TTS 安全检查（盲区扫描）
*   **隐形参数拦截**: 扫描全文中 `隐喻 (参数)` / `概念 (English)` 的括号结构
    *   TTS 解析器会吞噬括号内容，导致听众只听到"调整大小"而不知道调哪个
    *   ❌ 不合格：`调整大小 (Room Size)`
    *   ✅ 合格：`利用 **Room Size** 来调整大小`
*   **悬浮缩写**: 检查未展开的英文缩写 (如 "IAA"、"TTS") 是否在首次出现时有中文全称

---

## Deep 级别检查项 (Standard + 以下)

> **按需加载**：执行 Deep 级别审计时，根据审计范围加载以下文件：
> 1. `workflows/audit_deep.md` — Part D (知识面覆盖率) + Part G (OBE 对齐)：**所有 Deep 审计必须加载**
> 2. `workflows/audit_courseyaml.md` — Part F (course.yaml 合规性 F1-F16)：**仅当审计范围包含 course.yaml 时加载**

---

### 跨项目边界检查 (Post-Audit)

> 审计报告产出后、执行修复前，按 `/mailbox_out` 工作流判定修复项归属。

- 🟢 **课程端项**（course.yaml 数据/脚本/知识库）→ 直接修复
- 🔵 **教务端项**（生成器 bug/模板格式/Schema/Spec/审计规则）→ 编写 MSG 投递邮箱，**不得**直接修改教务端文件
- 🟡 **双端协同项**（Schema 新字段 + 数据填充）→ 课程端先完成数据准备，再发 MSG 给教务端

**Conclusion**: Pass / Fail / Needs Revision

### Epilogue: 收尾

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）+ E2（ADR 检查）。
