---
description: "/write Phase 2 — 写作（Segment-by-Segment）"
---

# Phase 2: 写作 (Composition)

> **前置**：Phase 1 备料已完成（知识扫描 + 素材预算表就绪）。
> **完成后**：加载 `write_phase3_verify.md` 进入校验阶段。

### Step 3: 分段执行写作 (Module-by-Module Writing)

> **ADR 020 核心协议**：将脚本按 `##` 模块切分，逐模块生成，每模块有字数预算和即时校验。

**遵循 `.agent/skills/script_format/SKILL.md` 全部规范**，包括：
*   Visual-First 双轨结构（§1）
*   知识标签体系（§2）
*   `[VISUAL]` 块字段规范（§3）
*   `[ACTIVITY]` 块规范（§4）
*   字数预算标注规范（§4.5）
*   叙事规范（§5）

**分段写作协议 (Segment-by-Segment Protocol)**：

> [!IMPORTANT]
> **Package 架构 (ADR-023 v5)**：写作目标是 `src/M0X_Topic.md` 独立碎片文件，**不是** `package.yaml`。
> `package.yaml` 仅为索引组装器，包含完整的 frontmatter 和 `segments: [ src/M01_Topic.md, ... ]` 阵列。
> 
> 这样做的核心目的：构建系统通过预编译 `M0X.md` 生成同层级的 `.build/compiled.md` 以实现完美的相对资源路径（`../public/`）绑定。Agent 写作时仅需加载当前 segment (~30KB) 而非全文 (~110KB)，极大降低由于单次输入产生的上下文丢失概率。

1. **骨架生成**：
   - 若 `package.yaml` 尚不存在，先创建该索引文件（frontmatter + `segments:` 列表）
   - 若 `src/` 与 `public/` 目录不存在，创建之
   - 为每个模块创建空的 `src/M0X_Topic.md` 文件骨架（含 `<!-- BUDGET -->` 注释）
2. **逐模块分段填充 (Phase A/B/C)**：对每个模块依次执行以下闭环：
   - **写作目标**：直接写入 `src/M0X_Topic.md`，**不操作** `package.yaml`

   **Phase A：骨架生成（占目标字数的 ~60%）**
   - 仅加载该模块所需的知识素材（控制上下文消耗）
   - 写入模块的主体叙事结构：开场过渡 + 核心概念展开 + 案例/人文标签 + VISUAL 块
   - **字数目标**：模块预算的 **60%-70%**
   - Phase A 完成后，**立即调用字数中间检查点**：
     ```bash
     # 方式1: 课程级发现（V5 架构会自动编译 lesson.yaml）
     /opt/anaconda3/envs/mybase/bin/python \
       .agent/skills/validation_suite/scripts/validate_script_length.py \
       --course "<课程名>" --week <周次数字> --module "<模块关键词>" --segment-check

     # 方式2: 直传 segment 文件（推荐，精确针对当前文件）
     /opt/anaconda3/envs/mybase/bin/python \
       .agent/skills/validation_suite/scripts/validate_script_length.py \
       --file "<课程>/weeks/<周次>/src/M0X_Topic.md" \
       --module-breakdown --segment-check
     ```
   - 解析返回的 JSON（`cn_count`, `budget`, `fill_ratio`, `deficit`）

   **Phase B：精准补足（目标 100%+）**
   - 根据 Phase A 的**精确缺口**（`deficit = budget - cn_count`），有针对性地补充：
     * 缺口 > 1000 字：需要新增一个完整的案例/故事段落 + 对应 VISUAL
     * 缺口 500-1000 字：为现有概念添加正反对照或深度展开
     * 缺口 < 500 字：在原有段落中添加具体细节和因果解释
   - ⚠️ **强制防注水约束 (引自 `rule_narrative_standards.md §8`)**：补充内容严禁使用空洞车轱辘话。必须引入具体痛点，做到“职业现实锚点”与“硬核认知锚点”的双向拉扯。
   - Phase B 完成后，**再次调用验证器**确认达标

   **Phase C：达标确认**
   - 调用完整的模块验证：
     ```bash
     /opt/anaconda3/envs/mybase/bin/python \
       .agent/skills/validation_suite/scripts/validate_script_length.py \
       --course "<课程名>" --module-breakdown
     ```
   - 仅当该模块 `fill_ratio >= 1.0` **且** Slide 达底线后标记 `done`
   - **退化自检门 (Degeneration Gate)**：
     * 检查 `--segment-check` 返回的 `is_degenerated` 字段
     * 若 `is_degenerated == true`：禁止标记 `done`，**必须回退到 Phase A 重写退化区域**
     * 退化重写遵循 `rule_narrative_standards.md` §7.4 指南：基于知识点从零重组叙事
   - 若仍不达标，**此时才进入 DRP 流程**（但已有精确缺口数据）
   - **视觉密度即时检查**（`script_format/SKILL.md` §6 强制）：
     1. 统计当前模块的 `> [VISUAL]` 块数量
     2. 若 Slide 数 **< `⌈讲授净分钟数 ÷ 3⌉`**（底线值），禁止标记 done，须对照 §6.1 触发规则补充视觉
     3. 扫描是否存在连续 > 360 字无 `[VISUAL]` 的口述段落，若存在须拆分并插入视觉锚点
    - **Scene-Speech 意图对齐检查**（`script_format/SKILL.md` §1.4 强制）：
      1. 对当前模块每个 `> [VISUAL]` 块，提取 `Scene` 的核心**认知意图标签**（如："新旧对比冲击"、"信息过载焦虑"、"知识升维震撼"）
      2. 提取 `[VISUAL]` 块后紧随的首段 Speech 的核心**认知意图标签**
      3. 若两者的意图标签不一致或无法建立隐喻映射关系，标记为「⚠️ Scene-Speech 意图脱节」，要求修正 Scene 使其与 Speech 的心理学内核对齐
      4. 在抽象风格系统下，**不得**通过插入具象实体名词来"修复"对齐——必须通过调整隐喻/情绪/张力来实现

> [!IMPORTANT]
> **Phase A → 中间检查点 → Phase B** 是字数达标的核心机制。禁止跳过中间检查点直接将模块标记为 done。禁止 Agent 自行估算字数——必须依赖外部验证器的精确计数。

**字数不足回退协议 (Deficit Recovery Protocol — DRP)**：

> **引用**: `rules/rule_content_depth.md` §3。当模块实际字数 < 预算 80% 时，按 DRP-L1 → L1.5 → L2 → L3 逐级执行，严禁跳级。详见完整定义。

3. **上下文管理**：已完成模块以**结构化记忆 Slot**（而非全文或 1 行摘要）保留在上下文中：
   ```
   M{N}: topic={主题} | tail="{末尾2行Speech}" | metaphor={核心意象}
         | hook="{过渡悬念}" | tags={ST:N CS:N PH:N LC:N} | chars={实际字数}
   ```
   - `tail`：供下一模块**过渡焊接**使用（`rule_narrative_standards.md` §3）
   - `metaphor`/`hook`：供**回环**和**悬念反问**技巧使用
   - 写每个新模块前，**必须先读取前一模块 Slot 的 `tail` 和 `hook`**，据此生成过渡句

**上下文分层策略**（控制每轮输入 Token）：

| 层级 | 内容 | 估算 Token |
|:---|:---|:---|
| Layer 0 (常驻) | `extract_week.py` 提取的本周元数据 + 字数预算表 | ~400-600 |
| Layer 1 (当前) | 当前模块的知识素材 | ~3,000-5,000 |
| Layer 2 (Slot) | 已完成模块的结构化记忆 Slot | ~800-2,000 |
| Layer 3 (风格) | 前序脚本的代表性片段（~300 字） | ~500 |

**知识标签内容来源规则**：
*   优先使用教材原文中的案例/故事（已经过 Step 2.3 深挖获取）
*   仅当教材中**完全缺失**人文素材时，才强制触发 Step 2.5 调研
*   调研中发现的 Search 关键词可直接用于 `[VISUAL]` 块的 `Search` 字段

**实验引用命名约定（ADR 017）**：
*   脚本正文中引用实验时，统一使用 `实验N(ExpN)` 格式（如 `实验3(Exp3)`）
*   Frontmatter `tags`、Slide 标识符等技术上下文中保留 `Exp[n]` 原样

**分片编译验证（每个模块定稿后执行）**：

当一个 segment 文件写入/修改完成后，立即执行编译验证确保可合并：
```bash
/opt/anaconda3/envs/mybase/bin/python engines/dumptext.py \
  <课程>/weeks/<周次>/package.yaml
```
- 验证编译无报错（✅ Compilation complete）
- 验证产物 `.build/compiled.md` 包含新写入的内容
- 若编译失败，检查 `package.yaml` 中 `segments` 阵列里的路径是否与实际文件名一致
