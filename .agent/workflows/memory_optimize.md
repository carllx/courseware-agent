---
description: 对指定逐字稿模块执行记忆逻辑专项优化（要旨可提取性 + 逻辑可重建性 + 冷热节律 + 视觉分流 + 段落呼吸），输出诊断报告并可选执行修复。
---

# /memory_optimize 工作流

> **输入**: 课程名 + 周次 + 模块文件路径（或 `--all` 处理整周全部模块）
> **输出**: 记忆逻辑诊断报告（Markdown artifact）+ 可选的修复执行
>
> **理论基础**: `docs/RESEARCH_SPEECH_MEMORIZATION.md` v3 — 逻辑重建范式
> **核心哲学**: 逐字稿不是枷锁，而是脚手架。教师记住的是逻辑链条，词语临场重建。

## 参数

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| `--dry-run` | 仅输出诊断报告，不执行修复 | 否（默认诊断+修复） |
| `--focus <维度>` | 仅执行指定维度的检查，逗号分隔 | 全部（M1-M6） |
| `--all` | 处理整周全部模块 | 否（默认单模块） |

**可用的 `--focus` 维度**:
- `heading` — M1 标题记忆锚点
- `rhythm` — M2 冷热叙事心流
- `transition` — M3 过渡焊接质量
- `checkpoint` — M4 Rosenshine 理解检查点
- `paragraph` — M5 段落物理负荷
- `anchor` — M6 锚词故事线

**示例**:
```
/memory_optimize 交互产品开发 W03 M03 --dry-run
/memory_optimize 交互产品开发 W03 --all --focus heading,rhythm
```

## 与现有工作流的协作关系

```
/write → /audit --quick → 需要记忆逻辑专项优化？
                              ├─ 是 → /memory_optimize
                              └─ 否 → /audit --standard
/memory_optimize → /cheat_sheet（验证修复后的骨架健康度）
```

| 工作流 | 职责边界 |
|:---|:---|
| `/audit` | 全面质量门（Q1-Q10 + Part A-E），只诊断不修复 |
| `/cheat_sheet --diagnose` | IAR 诊断 + 骨架健康，被本工作流 Phase 1 调用 |
| `/memory_optimize` | **专注记忆逻辑的诊断+修复**，复用上两者的自动化输出 |

---

## Phase 1: 自动化诊断（机器扫描）

> 本阶段零人工判断，全部由脚本完成。
> 理据：LLM 不会算字数（`rule_content_depth.md` 明确警告），量化检查必须由脚本执行。

### Step 1.1: 字数/视觉密度/退化检测

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" --week <N> --module-breakdown
```

**关注指标**：
- `[VISUAL_GAP]`：连续 >360 字无视觉切换（注意力重置失败）
- `[VISUAL_DENSITY_LOW]`：模块 Slide 数 < ⌈讲授净分钟数 ÷ 3⌉
- `[DEGEN]`：四字格密度/修饰语过载的段落级退化

### Step 1.2: IAR 段落推进 + 骨架链 + 视觉对齐诊断

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/generate_cheat_sheet.py \
  "<脚本路径>" --diagnose
```

**关注指标**：
- `[PADDING]`：冗余段 >1/块
- `[STAGNATION]`：连续支撑段 >2
- `[SKELETON_DEAD_LOOP]`：标题语义重叠
- `[FRAGMENTED_LOGIC]`：锚词串联无逻辑关联

### Step 1.3: Signaling Sync + Text 覆盖率

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_visual_text_sync.py \
  --course "<课程>" --week <N>
```

**关注指标**：
- Signaling 缺失（结构性枚举/操作步骤无 List）（🔴）
- 修辞性排比有 List（🔴）
- 冗余效应风险（论证性递进有 List）（🟡）
- Text 覆盖率 < 50%（🟡）
- Heading 空洞（🟡）

---

## Phase 2: Agent 深度检查（LLM 判断）

> 本阶段为不可自动化的语义级检查。
> Agent 需 `view_file` 读取目标模块脚本，按指定维度逐项执行。
> 若使用 `--focus` 参数，仅执行指定维度。

### M1: 标题记忆锚点

> **引用规则**: `rule_heading_design.md`
> **理论依据**: 断言-证据设计 (Alley & Garner) — H3 断言标题是教师图式重建的要旨锚点

逐项检查：
1. H3 是否为「四字定性：完整断言陈述句」结构
2. H4 冒号前是否为「动词/动宾结构」（≤ 5 字）
3. 同级 H4 释义字数差是否 ≤ 2 字（理想），≤ 4 字（容忍）
4. H3 排列是否遵循叙事递进（SCQA 金字塔推荐）
5. **碎片测试**：只读全部 H3+H4 标题，能否还原 80% 叙事主线
6. **要旨提取测试** (v3 新增)：每个 H3 标题能否被压缩为一句 ≤15 字的要旨？如果需要读正文才能理解标题含义 → `[TITLE_OPAQUE]`
7. **大纲逻辑可记忆性测试** (v4 新增)：

   > **理论依据**：Bartlett 重建性记忆——人类不记忆原文，而是记忆一个可用于重建原文的**逻辑图式**。标题链就是这个图式的骨架。如果标题链只是并列罗列，教师的记忆负荷等同于背诵一串无关联的清单。

   - **M1.7a 因果链测试**：提取所有 H3 标题，检查相邻标题之间是否存在**因果/递进/转折**关系（而非仅仅并列）。如果 ≥ 3 个连续 H3 之间只有并列关系 → `[FLAT_OUTLINE]` 🟡
   - **M1.7b 四字要旨测试**：每个 H3 标题能否被压缩为 ≤ 4 字的要旨关键词？这些关键词串联后是否构成一个**有逻辑的故事**（如"裂痕→病根→翻译→武器"）？如果要旨串联后只是一堆碎片 → `[FRAGMENTED_OUTLINE]` 🟡
   - **M1.7c 角色代入测试**：想象一位教师只看标题列表，能否在 30 秒内向同事描述"这堂课讲什么"？如果标题太抽象/太模糊导致无法口头复述 → `[TITLE_OPAQUE]`（复用现有标签）

   > **判定**：`[FLAT_OUTLINE]` + `[FRAGMENTED_OUTLINE]` 同时出现 → 🔴 高严重度（标题链既无因果逻辑又无可提取的要旨，教师将无法脱稿），必须在修复计划中优先处理。

### M2: 冷热叙事心流

> **引用规则**: `rule_script_clarity.md` §4 + `audit_standard.md` Part B-5
> **理论依据**: Von Restorff 效应 — 冷热切换点是最强的记忆分界线

逐项检查：
1. 提取骨架链，为每节点标注 🧊冷/🔥热
2. 模块无🔥热节点（无冲突/痛点/共情切入）→ `[NO_HEAT]`
3. 模块无🧊冷节点（无精准结论/教学金句）→ `[NO_COLD]`
4. 整段毫无情绪起伏、平铺直叙的枯燥罗列 → `[NO_EMOTIONAL_SPARK]`
5. 冷热切换点是否与段落边界对齐（§4.1 冷热边界即段落边界）
6. **记忆精度分层** (v3 新增)：`[TEACHING MOMENT]` 是否为精炼金句（需逐字精度）？`[STORY TIME]`/`[CASE STUDY]` 是否为要旨框架式（允许临场发挥）？如果人文标签段落写得像需要背诵的课文 → `[VERBATIM_TRAP]`
7. **论证多样性检查** (v4 新增)：

   > **理论依据**：Kalyuga 专长反转效应——相同论证结构的连续出现使教师记忆时产生"串台"（干扰效应），无法区分哪个案例对应哪个知识点。多样化的论证模式（对比型/故事型/数据型/定义型/过程型）为记忆提供差异化的编码线索。

   - **M2.7a 论证模式标注**：提取每个 H3 块使用的主要论证模式（参照 `rule_script_clarity.md` §2.7.1 骨架类型）
   - **M2.7b 多样性检测**：如果 ≥ 3 个连续 H3 块使用完全相同的论证模式 → `[MONOTONE_ARGUMENT]` 🟡
   - **M2.7c 与 §4.3 的协同**：`rule_script_clarity.md` §4.3 禁止连续 3 个 `###` 结构完全相同（形式层面）；本维度在论证模式层面（语义层面）执行同等检查
   - **修复建议**：建议至少每隔 2 个 H3 块切换一次论证模式（如：对比型→故事型→数据型），为教师记忆提供「认知路标」

### M3: 过渡焊接质量

> **引用规则**: `narrative_standards_guide.md` §3
> **理论依据**: 重建性记忆 (Bartlett) — 逻辑衔接清晰度决定教师图式能否正确重建内容

逐项检查：
1. 是否使用禁忌过渡（"下面我们来看"/"接下来介绍"/"让我们继续学习"）→ `[BANNED_TRANSITION]`
2. 是否使用推荐过渡技巧（悬念反问/听觉桥接/递进对比/回环/时间跳切/感官切换）
3. **逻辑因果链检查** (v3 新增)：相邻 H3 块之间的过渡段是否显式表达了因果/递进/转折关系？如果两个模块之间只有机械的时间顺序而无逻辑关系 → `[LOGIC_BRIDGE_MISSING]`

### M4: Rosenshine 理解检查点

> **引用规则**: `audit_standard.md` Part B-6
> **理论依据**: Rosenshine 教学十原则 — 连续 >10 分钟单向灌输导致工作记忆溢出

逐项检查：
1. 计算相邻 `[ACTIVITY]` 之间的纯讲授字数（排除 VISUAL/PACING 块）
2. **>3000 字**（约 10 分钟）→ `[MISSING_CHECKPOINT]` 🔴
3. **2000-3000 字**（约 7-10 分钟）→ `[CHECKPOINT_WARN]` 🟡
4. **≤2000 字** → ✅ 合格

**修复建议模板**（标记位置插入）：
- 推荐：`> [ACTIVITY] Type: QA | Duration: 1min | Desc: 快速检验理解`
- 可选：`> [ACTIVITY] Type: Quiz | Duration: 2min | Desc: 概念辨析小测`

### M5: 段落物理负荷

> **引用规则**: `script_format/SKILL.md` §5.2
> **理论依据**: 模糊痕迹理论 (FTT) — 段落过长则要旨被淹没，教师无法提取逻辑骨架

逐项检查：
1. **超长单段**：论证段 >250 字 / 叙事段 >350 字 → `[PARAGRAPH_OVERLONG]`
2. **连续长段堆叠**：≥3 个 >200 字段无短段（<80字）穿插 → `[RHYTHM_MONOTONE]`
3. **强制断段触发器检查**（任一成立必须断段）：
   - 逻辑转折（但/然而/不过/问题在于）
   - 视角切换（用户→开发者，现象→原因）
   - 时间跳切（从一个时代/事件跳到另一个）
   - 字数超限（当前段已超过 250 字且非叙事段）
4. **修辞通胀检测** (v3 强化)：段落中是否存在可删除而不损失信息量的文学修饰？过多修饰会抑制教师的生成性加工（Wittrock），使脚本变成需要背诵的枷锁 → `[RHETORIC_INFLATION]`

### M6: 锚词故事线

> **引用规则**: `narrative_standards_guide.md` §9.3
> **理论依据**: 线索依赖记忆 (Cue-dependent Memory) — 关键词就像拉绳子的线头

逐项检查：
1. 每个 H3 块提取灵魂锚词（≤4 字）
2. 锚词串联后是否构成逻辑连贯的故事线
3. 锚词串联无逻辑关联 → `[FRAGMENTED_LOGIC]`
4. **要旨可提取性测试** (v3 新增)：每段是否有且仅有一个 `**加粗**` 的核心概念？连续 >3 段无加粗 → `[ANCHOR_GAP]`

---

## Phase 3: 生成修复计划 + 执行

> 若使用 `--dry-run`，仅输出诊断报告，跳过本阶段。
> 诊断报告输出为 Markdown artifact，供其他模型或后续会话继续执行修复。

### Step 3.1: 生成结构化修复计划

基于 Phase 1/2 的诊断结果，生成 `implementation_plan.md` artifact，包含：

| 修复类型 | 具体内容 |
|:---|:---|
| **标题重构表** | 违规标题原版 → 建议重写版本（含四字定性+断言句） |
| **冷热节点注入** | 缺失🔥热节点的位置 → 建议插入的情感火花类型 |
| **视觉插桩点** | `[VISUAL_GAP]` 位置 → 建议的 Layout + Scene 方向 |
| **段落呼吸重组** | 超长段拆分点（引用 §5.2 四触发器）→ 具体行号 |
| **过渡焊接修复** | 禁忌过渡 → 替换为推荐过渡技巧 |
| **ACTIVITY 插入** | `[MISSING_CHECKPOINT]` 位置 → 推荐的微互动块 |
| **修辞精简** | `[RHETORIC_INFLATION]` 段落 → 压缩后的要旨版本 |
| **逐字陷阱解除** | `[VERBATIM_TRAP]` 段落 → 改写为要旨框架式 |

### Step 3.2: 等待用户确认

> [!IMPORTANT]
> 修复计划必须等待用户明确确认后才能执行。
> 用户可选择：全部接受 / 部分接受 / 拒绝并调整。

### Step 3.3: 执行修复

使用 `multi_replace_file_content` 工具将确认的修改应用到脚本文件。

### Step 3.4: 验证修复效果

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/generate_cheat_sheet.py \
  "<修复后的脚本路径>" --diagnose
```

对比修复前后的诊断报告，确认所有 🔴 标记已清除。

---

## 诊断报告输出格式

```markdown
# 记忆逻辑诊断报告

## 基本信息
- **课程**: {课程名}
- **周次**: W{N}
- **模块**: {模块名}
- **诊断时间**: {时间}

## Phase 1 自动化扫描结果
（粘贴脚本输出的关键指标）

## Phase 2 深度检查结果

### M1 标题记忆锚点 {🔴/🟡/🟢}
（列出违规项 + 建议重写）

### M2 冷热叙事心流 {🔴/🟡/🟢}
（骨架链 + 温度标注 + 问题标记）

### M3 过渡焊接质量 {🔴/🟡/🟢}
（禁忌过渡列表 + 逻辑桥接缺失）

### M4 Rosenshine 检查点 {🔴/🟡/🟢}
（字数间隔统计 + 建议插入位置）

### M5 段落物理负荷 {🔴/🟡/🟢}
（超长段列表 + 断段触发点）

### M6 锚词故事线 {🔴/🟡/🟢}
（锚词串联 + 逻辑连贯性判定）

## 综合结论
- **总评**: Pass / Needs Revision
- **🔴 必修项**: N 项
- **🟡 建议项**: N 项
```
