---
description: "/write Phase 3 — 校验（Alignment + Length + Coverage）"
---

# Phase 3: 校验 (Verification)

> **前置**：Phase 2 写作已完成（所有模块 Phase A/B/C 闭环通过）。

### Step 3.5: 大纲对齐检查表 (Outline Alignment Checklist)

> **强制执行**：所有模块写完后、时长自检前，必须逐项核对以下清单。任何一项未通过则**禁止进入 Step 4**。
> **引用检查表**: `.agent/rules/rule_outline_alignment.md`（O1-O10）

逐项执行 `rule_outline_alignment.md` 中定义的 **O1-O10** 检查（O8 为 `/write` 专用的 `teaching_requirements` 覆盖检查，O9 为模块字数预算达标检查，O10 为人文标签密度检查）。

### Step 3.7: 脉络与密度校验 (Clarity & Density Check)

> **强制执行**：大纲对齐检查通过后、时长自检前，必须完成以下四项质量检查。任何一项 🔴 级未通过则**禁止进入 Step 4**。

#### C1: 骨架还原测试 (Skeleton Recovery)
- 提取所有 H3 + H4 标题，形成标题序列
- 仅阅读标题序列，检查是否能还原 ≥ 80% 的教学叙事逻辑
- 如果标题序列中存在"读了标题仍不知道这一节讲什么"的条目 → ⚠️ 需重写标题（参照 `rule_heading_design.md`）
- **§10 Pinker 新生朗读测试**：对每个 H3/H4 标题执行——大一新生第一次看到这个标题，能在 3 秒内理解本节要讲什么吗？标题本身需要读两遍才能理解 → 标记 `[TITLE_OPAQUE]` 🟡（参照 `narrative_standards_guide.md` §10.4）

#### C2: 段落级信息推进扫描 (IAR Scan)
- 对每个模块的自然段执行 A/S/R 分类（定义见 `rule_content_depth.md` §4.1）
- 计算 IAR 值
- IAR < 0.70 的模块 → 🔴 **禁止提交**，回退修剪冗余段

#### C3: 巨型段落扫描 (Oversized Paragraph Scan)
- 扫描所有 > 350 字的单个自然段（定义见 `script_format/SKILL.md` §5.2）
- 逐一标记并建议拆分点
- 存在 ≥ 2 个巨型段落 → ⚠️ 建议修复

#### C4: 换角度重复检测 (Paraphrase Padding Scan)
- 对每个模块，将所有自然段分别压缩为 1 句话
- 检查是否存在两段压缩后语义重叠 > 80% 的情况
- 标记重复对及建议处理（合并或删除后者）
- 存在 ≥ 2 对重复 → 🔴 **禁止提交**

#### C5: 语义自洽检查 (Semantic Coherence Checkpoint) 🆕

> **按需加载**：加载共享模块 `workflows/_check_semantic_coherence.md`，执行其中的 **Part A（回译压缩）+ Part B（宪法批评链，使用 5 项：C1-C3, C5-C6）+ Part D（图式层经验域阻断）**。
>
> 判定规则：任何 🔴 标记 → 回退重写。2+ 个 🟡 标记 → 建议修订后再继续。

#### C6: 大纲可记忆性检查 (Outline Memorability Gate) 🆕

> **引用维度**: `/memory_optimize` M1.7（v4 新增）
> **理论依据**: Bartlett 重建性记忆——教师从标题链重建课堂逻辑。如果标题链只是并列罗列，教师脱稿时将无法重建论证走向。

1. 提取当前模块所有 H3 标题，检查相邻标题间是否存在**因果/递进/转折**关系（而非仅并列）
   - ≥ 3 个连续 H3 之间只有并列关系 → `[FLAT_OUTLINE]` 🟡
2. 每个 H3 压缩为 ≤ 4 字要旨关键词，串联后检查是否构成逻辑故事
   - 要旨串联无逻辑关联 → `[FRAGMENTED_OUTLINE]` 🟡
3. 角色代入：只看标题列表，能否 30 秒内描述"这堂课讲什么"
   - 标题太抽象 → `[TITLE_OPAQUE]` 🟡

**判定**：
- `[FLAT_OUTLINE]` **或** `[FRAGMENTED_OUTLINE]` 单独出现 → 🟡 建议修改但不阻断
- `[FLAT_OUTLINE]` + `[FRAGMENTED_OUTLINE]` **同时出现** → 🔴 **禁止提交**，标题链既无因果逻辑又无可提取要旨，必须回退重构大纲（参照 `rule_heading_design.md` §4 金字塔逻辑）

#### C7: 叙事拓扑校验 (Narrative Topology Check) 🆕

> **引用规则**: `rule_narrative_topology.md`
> **理论依据**: 中观结构层防线——微观段落质量和宏观标题骨架之间的章节排列、块归属和母题频率检查。

1. **C7.1 概念依赖链**：提取各 H3 的引入集/依赖集，构建 DAG，校验章节顺序是否违反拓扑排序
   - 旁支章节切断主线 → `[MAINLINE_BREAK]` 🟡
   - 引用概念在后文才定义 → `[DEPENDENCY_VIOLATION]` 🔴
2. **C7.2 块级归属**：扫描所有 WARNING/QA/TEACHING MOMENT 块，校验其引用概念是否在当前或相邻 H3 内定义
   - 块出现在定义源 ≥2 个 H3 之后 → `[MISPLACED_BLOCK]` 🔴
3. **C7.3 母题频率**：提取模块中反复出现的抽象论点，统计完整论证次数
   - 同一母题 ≥3 次完整展开 → `[THEME_SATURATION]` 🟡；≥5 次 → 🔴

**判定**：任一 🔴 → 阻断提交，回退修复。

### Step 3.8: 视觉与文字同步对齐 (Visual-Text Sync)


> **强制执行**：在完成所有的文本修改后、时长自检前执行，确保 Slide 的视觉文字与修改后的演讲内容严格对齐。引用规则：`RESEARCH_SPEECH_MEMORIZATION.md`。

- 运行 `validate_visual_text_sync.py` 检查当前编写的模块：
  ```bash
  /opt/anaconda3/envs/mybase/bin/python \
    .agent/scripts/validation/validate_visual_text_sync.py \
    --course "<课程名>" --week <周次>
  ```
- **修复 Signaling Sync (🔴 必须)**: 按内容类型分流修复：
  - 结构性枚举/操作步骤缺 List → 补充 ≤4 字/项的关键词 List
  - 修辞性排比有 List → 移除 List 字段（文字化杀死冲击力）
  - 论证性递进有 List → 建议移除（🟡 非阻断）
- **优化 Text 字段 (🟡 建议)**: 审查 `Text 字段缺失` 的报告，为缺少 Text 的 VISUAL 块补全核心论断（而非泛化标题），提升 Slide 文字作为记忆锚点的效能。

### Step 3.9: 真实素材需求扫描 (Real-Asset Sourcing Check)

> **引用技能**: `.agent/skills/real_asset_scanner/SKILL.md`

扫描当前编写模块的 `[VISUAL]` 块，识别需要真实网络素材替代 AI 生图的位置：

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/scan_real_assets.py \
  <课程>/weeks/<周次>/src/
```

**处理规则**：
- `no_ai_flag = true` 的 CRITICAL 项 → 🔴 **必须**标注 `**Source**: TBD (需真实档案)` 并记录到 `sourcing_checklist.yaml`
- 其他 CRITICAL 项 → 🟡 建议替换但不阻断提交
- ENHANCE / OPTIONAL 项 → 记录但不阻断

> [!TIP]
> 扫描引擎会自动跳过已有真实素材（GIF/JPG/小尺寸 PNG 等），避免对已完成的素材发出误报。

### Step 3.92: 教材图覆盖率校验 (Textbook Visual Coverage Check)

> **关联规则**: `rule_textbook_sourcing.md`  |  **关联工作流**: `/sync_textbook_visuals`

1. 检查当前课程的 `knowledge/textbook/` 目录是否存在且包含至少一本教材。若不存在 → 跳过此步骤。
2. 统计本单元脚本中：
   - 引用 `textbook/` 路径的 `[VISUAL]` 块数量 (A)
   - 含 `[TEXTBOOK-REF]` 标签的 `[VISUAL]` 块数量 (B)
   - 总 `[VISUAL]` 块数量 (C)
   - **教材图覆盖率** = max(A, B) / C
3. 定位教材中与本单元理论概念相关的章节数量 (D)

**判定规则**：

| 条件 | 判定 | 处理 |
|:---|:---|:---|
| D > 0 且覆盖率 = 0% | ⚠️ **教材图零覆盖** | 强烈建议执行 `/sync_textbook_visuals`。不阻断提交，但在报告中高亮显示 |
| D > 0 且覆盖率 < 15% | 🟡 **教材图覆盖不足** | 建议审查是否有遗漏的教材图匹配 |
| D = 0 或覆盖率 ≥ 15% | ✅ 通过 | 无需处理 |

> [!NOTE]
> 此步骤为**建议性检查**（🟡），不阻断提交流程。目的是确保教材图不被系统性遗漏。

### Step 3.95: 概念注册回写 (Concept Registry Writeback)

> **ADR 043 增量维护协议**：`<课程>/concept_registry.yaml` 是 `theory_link.concept_id` 的 SSOT，应在 `/write` 过程中增量补充。

**执行流程**：

1. **扫描新写模块**：从当前周次所有 `src/M0X_*.md` 中提取所有 `theory_link` 相关内容（概念名称、首次引入位置）
2. **比对注册表**：读取 `<课程>/concept_registry.yaml`，检查新写模块引入的核心概念是否已有对应 `id`
3. **自动追加**：对于不存在的概念，以 `snake_case` 生成 `id`，追加到 `concepts:` 列表末尾，标注 `first_introduced: W0X`
4. **通知用户**：列出新增的概念 ID 清单

> [!IMPORTANT]
> 此步骤不删除或修改已有概念——仅追加。概念 ID 的重命名/删除应通过 `/update_guidance` §G4 执行。

### Step 4: 时长自检（必须执行，不得跳过）

从**课程目录**下运行时长验证器（注意路径为相对课程目录的上级 `.agent`）：

```bash
# 从 Workspace 根目录运行：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_script_length.py \
  --course "<课程名>"
```

**时长门限（硬性约束）**：

| 检查项 | 标准 | 不合格处理 |
|:---|:---|:---|
| 预估总时长 ≥ 课程计划时长 x 80% | 如 5 小时课 → 预估需 ≥ 240 分钟 | **禁止提交，必须回到 Step 3 补充** |
| ACTIVITY 总时长 > 0 | `lecture`/`workshop` 模式强制要求 | 补充 `[ACTIVITY]` 块后重新验证 |
| **模块字数偏低** | 📊 仅供教师参考 | Agent 仅报告现状，不触发自动修复。教师可选择标记 `<!-- SHORT_MODULE: logical_complete -->` 或要求补充 |
| 模块字数 60%-80% | 📊 仅供教师参考 | 同上 |

> **ℹ️ 分片架构提示**：验证器现在支持 `--file` 参数直传文件路径。对 `weeks/` 架构，`--course` 模式会自动编译分片脚本并使用 `_compiled.md`。

> **⚠️ 理论+实践混合模式**：当 `course.yaml` 中同时定义了 `hours_theory` 和 `hours_practice` 时，验证逻辑应为“讲授时长 + 活动时长 ≈ 计划总课时”，而非纯用 80% 塞进公式。典型的 4 课时“理论 2h + 实践 2h”单元，预估总时长在 150-200 分钟即合格。

**模块级预算对标**（**强制执行**，不可跳过）：

```bash
# 从 Workspace 根目录运行：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_script_length.py \
  --course "<课程名>" --module-breakdown
```

### Step 5: 知识面覆盖率检查

```bash
# 检查标签分布（兼容分片架构：搜索 src/ 和 _compiled.md）
echo "=== 知识标签分布 ==="
# 分片架构
grep -roP '> \[([A-Z ]+?)(?::.*?)?\]' "<课程>/weeks/"*"/src/" 2>/dev/null | sort | uniq -c | sort -rn
# 或使用编译产物
grep -oP '> \[([A-Z ]+?)(?::.*?)?\]' "<课程>/weeks/"*/".build/compiled.md" 2>/dev/null | sort | uniq -c | sort -rn

echo "=== VISUAL 块完整性 ==="
grep -rc '> \[VISUAL\]' "<课程>/weeks/"*"/src/" 2>/dev/null || \
grep -c '> \[VISUAL\]' "<课程>/weeks/"*/".build/compiled.md" 2>/dev/null

echo "=== 知识节点标签一致性 ==="
# 提取脚本中的知识节点标签，检查是否在 Hub 中存在
grep -roP '\*\*知识节点\*\*: `([^`]+)`' "<课程>/weeks/" 2>/dev/null | \
  sed 's/.*`\(.*\)`.*/\1/' | while read tag; do
    if grep -q "$tag" "<课程>/knowledge/knowledge_hub.yaml"; then
      echo "✅ $tag"
    else
      echo "❌ $tag — 未在 Hub 中找到，请检查或新建条目"
    fi
  done
```

### Step 6: 收尾 (Epilogue)

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）+ E2（ADR 检查）+ E3（链接验证）。
