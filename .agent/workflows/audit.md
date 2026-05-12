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

### Q2.5: 真实素材验真 (Real-Asset Authenticity)

> **引用技能**: `.agent/skills/real_asset_scanner/SKILL.md`

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/scan_real_assets.py \
  <课程>/weeks/<周次>/src/
```

检查 VISUAL 块中是否存在"使用 AI 生图替代真实素材"的违规情况：
*   `no_ai_flag = true` 且当前 Asset 仍为 AI 生成图 → 🔴 **Needs Revision**
*   CRITICAL 级且无 `**Source**` 字段 → 🟡 建议补充来源标注
*   扫描引擎自动跳过已有真实素材（GIF/JPG/小尺寸PNG），避免误报

### Q3: 时长估算

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" {WEEK_FILTER}
```

> **口述字数排除项**：Frontmatter / `[VISUAL]` 块 / `[ACTIVITY]` 块 / `[!NOTE]` 导读块 / Markdown 标题行——均不计入口述字数。

> [!NOTE]
> **字数为教师决策域**：Q3 的字数/时长估算仅作为**信息展示**供教师参考。字数偏低（📊）不触发 `Needs Revision`，不构成审计短路条件。Agent **禁止**以字数不足为由自行建议扩写或判定审计失败。仅退化（`[DEGEN]`）、预算溢出（>150%）等质量问题触发非零退出码。

### Q4: 语义自洽检查 (Semantic Coherence Protocol)

> **理论基础**：Self-Enhancement Bias 研究表明，LLM 在审阅自身输出时会在 >50% 的情况下
> 无法识别客观错误。以下协议通过**结构化探针**替代笼统审阅，强制 System 2 深层分析。

Agent 需逐项执行以下检查：

**A: 过渡检查**（保留原有）
*   段落之间是否使用了禁忌过渡（"下面我们来看"/ "接下来介绍"）？
*   是否使用了推荐过渡技巧（悬念反问/听觉桥接/递进对比/回环）？

**B: 反翻译腔**（保留原有）
*   是否存在超过 20 字未断句的长句？
*   是否存在禁忌词（"进行/实现/功能/相关的/在…的情况下"）？

**C: 朗读测试**（保留原有）
*   选取 3 段正文，模拟朗读节奏是否流畅。

**D: 回译压缩测试 (Compression Test)** 🆕
*   **范围**：每个 `> [TEACHING MOMENT]` 块 + 每个模块的结尾总结段
*   **步骤**：
    1. 将目标段压缩为恰好**一句话（≤25 字）**
    2. 检查压缩后的句子是否**自洽**（无逻辑矛盾）且包含**具体命题**
    3. 如果压缩后变成空话（如"可视化很重要"、"这个概念很关键"）→ 原文为填充物，标记 `[HOLLOW_BLOCK]`
    4. 如果压缩时发现**无法调和的矛盾** → 原文存在逻辑断裂，标记 `[LOGIC_BREAK]` 🔴
*   **示例**：原文若同时说"有损压缩"和"无损压平"修饰同一过程 → 压缩时矛盾暴露 → `[LOGIC_BREAK]`

**E: 宪法批评链 (Constitutional Critique)** 🆕
*   **范围**：每个 `> [TEACHING MOMENT]` 块 + `> [STORY TIME]` 块 + 模块首尾段
*   **逐条检查以下 6 条宪法原则**，对每条原则要求 Agent **引用具体违规文本**：

| # | 原则 | 检查方法 | 标记 |
|:---|:---|:---|:---|
| C1 | **反义词共现禁止**：同一句/段中不得同时出现语义矛盾的修饰 | 扫描是否存在"有损+无损"/"极其简洁+极其复杂"等自相矛盾 | `[ANTONYM_CLASH]` 🔴 |
| C2 | **费曼画板**：每个四字以上修饰词组必须能被描述为具体物理画面 | 选取段中最长的修饰短语，尝试描述画面。无法画出 → 违反 | `[UNPAINTABLE]` 🟡 |
| C3 | **Mayer 删除**：删掉该修饰语后信息量是否下降 | 逐个删除修饰语，检查信息损失 | `[SEDUCTIVE_DETAIL]` 🟡 |
| C4 | **压缩命题**：每个核心断言可被压缩为 ≤20 字且无歧义 | 逐句压缩测试 | `[INCOMPRESSIBLE]` 🟡 |
| C5 | **具象化强制**：禁止用抽象概念解释另一个抽象概念 | 检查是否存在"抽象→抽象"解释链 | `[ABSTRACT_LOOP]` 🟡 |
| C6 | **造词检测**：如果一个 ≥4 字的词组不是通用术语，很可能是幻觉造词 | Agent 判断该词组是否为公认的中文词汇或学术术语 | `[NEOLOGISM]` 🔴 |

*   **判定**：任何 🔴 标记 → **Needs Revision**。2 个以上 🟡 标记 → 建议修订。

### Q5: 大纲一致性验证 (Outline Consistency)

> **引用检查表**: `.agent/rules/rule_outline_alignment.md`

Agent 需对照 `extract_week.py --week N` 输出的 `calendar` 条目，逐项执行 `rule_outline_alignment.md` 中定义的 O1-O7 + O9 + O10 检查（O9 为模块字数预算达标，ADR 020；O10 为人文标签密度）。

> 任何 🔴 高严重度项未通过 → 报告结论为 **Needs Revision**。

> [!IMPORTANT]
> **素材补充引导**：当模块填充率 < 60% 时，审计报告应建议补充真实素材（教材提取/网络调研），而非强制扩写。
> 若模块逻辑已完整，可接受 `<!-- SHORT_MODULE: logical_complete -->` 标记。
> 素材补充级别判定详见 `rules/rule_content_depth.md` §3。

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

与 Q3 共享 `--module-breakdown` 输出。检查末列 `[DEGEN]` 标记（引用 `rule_narrative_standards.md` §7.4）。
任何模块存在 🔴 退化 → **Needs Revision (文本退化)**，短路后续 Standard/Deep 检查。

### Q8: 视觉-文字对齐 (Visual-Text Sync)

> **理论**: Visual-First 双轨记忆（`docs/RESEARCH_SPEECH_MEMORIZATION.md`）

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_visual_text_sync.py \
  --course "<课程>" {WEEK_FILTER}
```

检查：Signaling Sync（🔴 结构枚举缺 List / 修辞排比有 List）、Text 覆盖率（🟡 建议 ≥ 50%）、Heading 空洞（🟡）。
Q8 自动化结果可直接用于 Standard Part A 的 Signaling Sync 人工复核。

### Q9: 锚词密度 (Anchor Coverage for Cloak Mode)

由 `/cheat_sheet --diagnose` 自动输出。`**加粗**` 文字是 H5 Cloak 模式的数据源。

| 检查项 | 标准 | 严重度 |
|:---|:---|:---|
| 锚词覆盖率 ≥ 60% | 含加粗段落 / 总段落 | `[ANCHOR_DENSITY_LOW]` 🟡 |
| 最大无锚词间隔 ≤ 3 段 | 连续无加粗段落数 | `[ANCHOR_GAP]` 🟡 |

### Q10: 视觉记忆锚点 (Visual Memory Anchoring)

由 `/cheat_sheet --diagnose` 自动输出。Scene/Layout/Text 三维绑定检查。

| 检查项 | 标准 | 严重度 |
|:---|:---|:---|
| [V1] Scene 有效率 ≥ 90% | Scene ≥ 10 字 | `[SCENE_EMPTY]` 🟡 |
| [V2] Text 覆盖率 ≥ 50% | 含 Text 的 VISUAL 占比 | `[TEXT_LOW]` 🟡 |
| [V3] Layout 一致性 | Grid/Comparison 须含 List | `[LAYOUT_MISMATCH]` 🟡 |

---


## Standard 级别检查项 (Quick + 以下)

> **按需加载**：执行 Standard 或 Deep 级别审计时，加载以下文件获取详细检查项：
> - `workflows/audit_standard.md` — Part A (叙事完整性) + Part B (Deep Listen) + Part C (语言合规) + Part E (TTS 安全) + Part B-5 (脉络清晰度)
> - `workflows/audit_practice.md` — Part P (Practice 冒烟检查)：**仅当目标周次存在 `practice.yaml` 时加载**（ADR 043 R-10）

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
