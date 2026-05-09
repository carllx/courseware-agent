---
description: 以目标受众（DMA 学生）视角审查逐字稿的认知对齐与信噪比，执行宏观-微观分阶段审查，输出深度诊断清单 + 修复建议稿。
---

# /review 工作流 — 教学体验审查

> **输入**: 课程名 + 周次 + 模块文件路径（或 `--all` 处理整周全部模块）
> **输出**: L1 诊断清单（artifact）+ L2 修复建议稿（artifact）
>
> **核心哲学**: 逐字稿不仅要"合规"（`/audit` 的职责），更要"可理解"——确保内容穿透了专家与学生之间的认知鸿沟。
> **理论基础**: Shulman PCK（教学内容知识） + Mayer 一致性原则 + Sweller 冗余效应 + Plain Language 原则

## 参数

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| `--dry-run` | 仅输出 L1 诊断清单，不生成 L2 修复建议 | 否（默认双层产出） |
| `--focus <维度>` | 仅执行指定维度的检查，逗号分隔 | 全部（R1-R7） |
| `--all` | 处理整周全部模块 | 否（默认单模块） |

**可用的 `--focus` 维度**:
- `coherence` — R1 Mayer 一致性扫描
- `saturation` — R2 论证模式饱和度
- `skeleton` — R3 骨架逻辑审查
- `pck` — R4 Shulman PCK 三层诊断
- `plain` — R5 Plain Language 精简
- `inflation` — R5b LLM 隐性膨胀检测
- `fact` — R6 SME 事实快检

**示例**:
```
/review 交互产品开发 W02 M03
/review 交互产品开发 W02 --all --dry-run
/review 交互产品开发 W02 M03 --focus coherence,saturation
```

## 与现有工作流的协作关系

```
/write Phase 3 → /review（教学体验审查）→ /audit（全面质量门）
                           ↓
              /memory_optimize（记忆逻辑专项，可选）
```

| 工作流 | 职责边界 | 侧重 |
|:---|:---|:---|
| `/audit` | 全面质量门（格式/TTS/OBE/字数/叙事） | **合规性** |
| `/review` | 教学体验审查（知识漏洞/冗余/不对称/简练化） | **可理解性** |
| `/memory_optimize` | 记忆逻辑专项（标题/冷热/锚词/过渡） | **可记忆性** |

> [!IMPORTANT]
> `/review` 的输出深度应对标 analysis_review_correction.md 的分析粒度——逐段标注问题类型、提供理论依据、给出正反示例。

---

## Phase A — 宏观审查（先结构后细节）

> **编辑层级**：发展编辑 (Developmental Editing) — 先解决结构问题，避免在后续被删除的段落上浪费微观打磨的精力。
> **强制排序**：Phase A 全部完成后才可进入 Phase B。

### Step 1: 教学目标锚定

1. 读取目标模块的 frontmatter `objectives` 字段
2. 读取 `course.yaml` 中对应周次的 `calendar[].lessons[].steps` 和 `teaching_requirements`
3. 建立本模块的**教学目标清单**（≤ 5 条），作为后续所有判断的基准

> 此步骤的输出是一张简洁的目标表，后续所有"是否支撑教学目标"的判断都以此为锚。

### Step 2: Mayer 一致性扫描 (R1)

> **引用规则**: `rule_coherence_audit.md` §1

对每个人文标签块（`[DID YOU KNOW]`/`[CASE STUDY]`/`[STORY TIME]`）及 >200 字的扩展段落，执行 Mayer 三问：

1. 这段内容是否**直接支撑** Step 1 中列出的教学目标？
2. 删除它后，核心概念的理解度是否会**实质性下降**？
3. 它是否引入了**教学目标清单未包含的新子概念**？

→ 标记 `[SEDUCTIVE_DETAIL_BLOCK]` / `[SCOPE_CREEP]` / `[REMOVABLE]`

### Step 3: 论证模式饱和度检测 (R2)

> **引用规则**: `rule_script_clarity.md` §2.7

1. 提取本模块所有案例/论证段落的**论证骨架**（A-vs-B / BEFORE-AFTER / DEFINITION-EXAMPLE / PAIN-REVEAL）
2. 统计同一骨架类型出现的次数
3. **≥ 3 次** → 标记 `[PATTERN_SATURATION]`
4. 标注哪 2 个案例最具教学冲击力（建议保留完整展开），其余建议压缩/删除

### Step 4: 骨架逻辑审查 (R3)

> **引用规则**: `rule_heading_design.md` §4 + `rule_script_clarity.md` §1

1. 提取所有 H3+H4 标题链
2. **因果链测试**：检查相邻 H3 标题之间是否存在因果/递进/转折关系（而非仅并列）
   - ≥ 3 个连续 H3 只有并列关系 → `[FLAT_OUTLINE]`
3. **四字要旨测试**：每个 H3 压缩为 ≤ 4 字要旨关键词，检查串联后是否构成逻辑故事
   - 要旨串联只是碎片 → `[FRAGMENTED_OUTLINE]`
4. **角色代入测试**：想象一位教师只看标题列表，能否在 30 秒内描述"这堂课讲什么"
   - 标题太抽象 → `[TITLE_OPAQUE]`

---

## Phase B — 微观审查（结构稳定后执行）

> **编辑层级**：行编辑 (Line Editing) — 在 Phase A 确认结构无重大问题后，聚焦句段层面的认知对齐与简练化。

### Step 5: Shulman PCK 三层诊断 (R4)

> **引用规则**: `rule_prerequisite_awareness.md` §1-§3.4

逐段扫描，检查三个层面的知识不对称：

**5a. 术语层**（已有规则覆盖，此处复用）：
- 标记所有 L3 未铺垫术语 → `[PREREQUISITE_GAP]`
- 检查 30 字内连续 ≥ 3 个 L3 术语 → `[VOCAB_OVERLOAD]`

**5b. 逻辑层**（新增维度）：
- 检查所有理论框架过渡处是否有显式因果桥 → 缺失者标记 `[LOGIC_LEAP]`
- 检查"断言式理论关系"（仅用类比代替推理）→ `[LOGIC_LEAP]`

**5c. 图式层**（新增维度）：
- 对每个类比/隐喻执行"受众经验匹配测试"（参照 §3.4 经验域表）
- 使用 DMA 学生低概率经验域的类比 → `[SCHEMA_MISMATCH]`

### Step 6: Plain Language 精简 (R5)

> **引用规则**: `rule_script_clarity.md` §2.5 修辞通胀 + `audit_standard.md` Part C §10

对每段执行两种删除测试：

1. **整段删除测试**：删除此段后本模块的信息完整性是否受损？
   - 不受损 → 标记 `[TRIM_CANDIDATE]` 🟡
2. **句级压缩测试**：此句能否用 ≤ 50% 的字数表达相同信息？
   - 能 → 标记 `[COMPRESS_CANDIDATE]` 🟢
3. **复用现有检测**：`[RHETORIC_INFLATION]`、`[MODIFIER_OVERLOAD]`

### Step 6a: LLM 隐性膨胀检测 (R5b)

> **引用规则**: `rule_script_clarity.md` §2.8

对每个 `##` 模块执行以下专项扫描，识别能穿透 IAR 检测的 LLM 特有隐蔽膨胀：

1. **压缩比测试**：随机抽取 3-5 段，压缩为最少字数等效表述
   - 压缩比 < 0.4 的段落 ≥ 2 → `[STEALTH_INFLATION]` 🟡
   - 压缩比 < 0.3 的段落 ≥ 1 → `[STEALTH_INFLATION]` 🔴
2. **七子模式逐项扫描**：

| 子模式 | 快速检测方法 | 标记 |
|:---|:---|:---|
| P1 结论展开冗余 | 金句后的段落是否仅重述结论 | `[CONCLUSION_ECHO]` |
| P2 三段式信封 | `###` 块首尾是否有空转预告/总结 | `[ENVELOPE_PADDING]` |
| P3 修辞能量过载 | 同一段极端程度词 ≥ 3 | `[ENERGY_OVERLOAD]` |
| P4 对称强迫症 | 两案例结构对称但信息量不对称 | `[SYMMETRY_BLOAT]` |
| P5 定义回声 | 同一定义被 ≥ 3 次用不同措辞重述 | `[DEFINITION_ECHO]` |
| P6 脚手架残留 | 段首存在对读者无贡献的铺垫句 | `[SCAFFOLD_RESIDUE]` |
| P7 叙事过度戏剧化 | 情景设置字数 > 论证字数 | `[DRAMATIZATION_BLOAT]` |

3. **L2 修复建议中必须提供**：原文 → 压缩版的正反对比示例

### Step 6b: SME 事实快检 (R6)

> **引用规则**: `rule_factual_grounding.md` §1

对模块中的关键事实声明执行快速核查：

1. 理论归因是否准确（如"Kenneth Craik 在 1943 年提出"）
2. 技术细节是否正确（如"Bang-Bang Control 是恒温器的实际工作原理"）
3. 案例时效性是否过期（如"微信删除机制是否仍然不可恢复"）
4. 不确定者标记 `[FACT_CHECK_NEEDED]` 🟡

---

## Phase C — 产出

### L1: 诊断清单

输出为 Markdown artifact，格式如下：

```markdown
# 教学体验审查诊断清单

## 基本信息
- **课程**: {课程名}
- **周次**: W{N}
- **模块**: {模块名}
- **审查时间**: {时间}
- **教学目标锚定**:
  1. {目标1}
  2. {目标2}
  ...

## Phase A 宏观审查结果

### R1 Mayer 一致性 {🔴/🟡/🟢}
| 位置（行号） | 内容摘要 | 标记 | 理由 | 严重度 |
|:---|:---|:---|:---|:---:|
| L87-88 | Kenneth Craik 历史背景 | [SEDUCTIVE_DETAIL_BLOCK] | 不直接支撑"三种模型博弈"的学习目标 | 🟡 |

### R2 论证饱和度 {🔴/🟡/🟢}
| 骨架类型 | 出现次数 | 涉及案例 | 建议保留 | 建议压缩/删除 |
|:---|:---:|:---|:---|:---|

### R3 骨架逻辑 {🔴/🟡/🟢}
- **H3 标题链**: ...
- **要旨故事线**: ...
- **问题标记**: ...

## Phase B 微观审查结果

### R4 Shulman PCK 三层诊断 {🔴/🟡/🟢}
#### 术语层
（逐条列出）
#### 逻辑层
（逐条列出，含正反示例）
#### 图式层
（逐条列出）

### R5 Plain Language 精简 {🔴/🟡/🟢}
（列出 TRIM_CANDIDATE 和 COMPRESS_CANDIDATE）

### R5b LLM 隐性膨胀 {🔴/🟡/🟢}
| 位置（行号） | 子模式 | 原文摘要 | 压缩版 | 压缩比 |
|:---|:---|:---|:---|:---:|
（逐条列出，附正反对比示例）

### R6 SME 事实快检 {🔴/🟡/🟢}
（列出 FACT_CHECK_NEEDED 项）

## 综合结论
- **总评**: Pass / Needs Revision
- **🔴 必修项**: N 项
- **🟡 建议项**: N 项
- **预估修复工作量**: 小/中/大
```

### L2: 修复建议稿

> 仅对 🔴 高严重度问题提供**完整重写文本**；🟡 中等问题提供**修改方向 + 简短示例**。

输出格式：

```markdown
# 教学体验审查修复建议

## 🔴 必修项

### 修复 1: [LOGIC_LEAP] Norman→Cooper 逻辑桥缺失 (L45-46)

**原文**:
> 如果说 Norman 的鸿沟理论是诊断症状的听诊器，那么 Cooper 的模型论就是揭示病因的解剖刀。

**问题**: 用类比替代了因果推理。学生不知道"为什么鸿沟是症状而模型是病根"。

**建议重写**:
> Norman 告诉我们"血流在哪断了"——用户卡在了执行或评估环节。但**为什么会断**？
> Cooper 追问了一个更深层的问题：造成这些断裂的根源，是工程师构建的系统和用户脑中的世界
> 根本就不在同一个频道上。鸿沟是表面裂缝，模型错位才是地基问题。

---

## 🟡 建议项

### 建议 1: [PATTERN_SATURATION] "用户X vs 机器Y" 模式重复5次

**修改方向**: 保留微信案例(L59-62)和恒温器案例(L143-154)完整展开，
将电影放映案例(L99-100)压缩为一句话引用，将微信删除案例(L251-254)
改用不同的论证骨架（如 PAIN-REVEAL 型）。
```

---

## 与 Phase 3 写作门禁的集成

> [!IMPORTANT]
> `/review` 的 R3（骨架逻辑审查）中的 **大纲可记忆性检查** 作为 `/write` Phase 3 的**强制门禁**集成：
> - Phase 3 Step 3.7 新增 **C6: 大纲可记忆性检查**
> - `[FLAT_OUTLINE]` 或 `[FRAGMENTED_OUTLINE]` → 🟡 建议修改但不阻断
> - `[FLAT_OUTLINE]` + `[FRAGMENTED_OUTLINE]` 同时出现 → 🔴 禁止提交

---

## Phase D — 物理修复执行（L2 建议 → 代码修改）

> **编辑层级**：执行编辑 (Copy Editing + Physical Refactor)
> **前置条件**：Phase C 的 L1/L2 报告已生成

### Step 7: 自动修复（仅限 🔴 必修项）

对 L2 报告中每个 🔴 必修项，Agent 必须：

1. **定位**：找到原文的精确行号范围
2. **修改**：直接调用 `replace_file_content` 或 `multi_replace_file_content` 执行物理修改
3. **校验**：修改后立即运行 `validate_spec.py` 确认无新增错误

**修复范围限定**：

| 问题级别 | 处理方式 |
|:---|:---|
| 🔴 必修 | Agent 自动执行修复 |
| 🟡 建议 | 列入修复建议清单，**不自动修改**，交由用户人工决定 |
| ℹ️ 参考 | 仅在报告中记录，不做任何处理 |

> [!WARNING]
> Phase D 修复**不得**改变模块的教学逻辑或删除有效内容。修复行为限于：
> - 删除占位符残留
> - 修正 Bold 标记空格
> - 压缩跨模块重复案例为回指句
> - 修正 VISUAL 字段顺序
> - 替换修辞黑名单词组

### Step 8: 修复验证

修复完成后执行回归验证：

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_spec.py \
  --course "<课程名>" --week <周次>
```

### Step 9: 修复报告

产出修复摘要，格式：

```markdown
## Phase D 修复报告

- **修复日期**: YYYY-MM-DD
- **修复范围**: <课程> W<N>
- **自动修复项**: X 个 🔴
- **跳过项**: Y 个 🟡 (待用户决定)
- **回归验证**: ✅ validate_spec.py 通过 / ❌ 新增 N 个错误
```
