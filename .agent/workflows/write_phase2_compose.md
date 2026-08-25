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
2. **逐模块分段填充 (Phase alpha/A/B/C)**：对每个模块依次执行以下闭环：
   - **写作目标**：直接写入 `src/M0X_Topic.md`，**不操作** `package.yaml`

   **Phase alpha：骨架锁定（Skeleton Lock）— 在 Phase A 之前强制执行**
   - 仅加载该模块所需的知识素材（控制上下文消耗）
   - Agent 必须先输出一个小于等于 300 字的模块级逻辑骨架，**自检通过后方可进入 Phase A**
   - 骨架格式：
     ```
     模块 X：{主题} ({时长})
     -- 核心论断：{一句话，本模块最终要让学生记住什么？}
     -- 情感入口：{一句话，用什么痛点/冲突切入？}
     -- 金字塔支撑：
        -- 支撑点 1：{概念名} - {一句话结论}
        -- 支撑点 2：{概念名} - {一句话结论}
        -- 支撑点 3：{概念名} - {一句话结论}（如有）
     -- 视觉序列：{Layout 类型序列，如 Full->Split->Grid->Center}
     -- 出口悬念：{一句话，如何过渡到下一模块？}
     ```
   - **骨架自检清单**（全部通过方可进入 Phase A）：
     - [ ] "核心论断"能否被一个非专业人士秒懂？
     - [ ] 从"情感入口"到"核心论断"是否存在清晰的逻辑递进链？（推荐使用 SCQA 或其他叙事弧）
     - [ ] 支撑点之间是否完全独立（MECE）？有无重叠？
     - [ ] 删掉所有支撑点的细节后，仅看骨架能否还原 80% 的教学目标？
     - [ ] 视觉序列是否遵循渐进式披露（Full->Center->Grid/Split）？
     - [ ] **Vibe Coding 护栏**：对于 AI/编程类主题，检查"核心论断"是否将其包装为"Prompt 工程/架构指挥任务"而非"手动语法填空"？
     - [ ] **事实锚定**：每个支撑点计划引用的案例/产品/事件，能否回答 WHO（具体产品名）+ WHEN（年份/版本）+ WHY（底层原因）中的至少两项？若不能，须在进入 Phase A 前先完成调研。（参照 `rule_factual_grounding.md` §1）
     - [ ] **§10 Pinker 新生测试**：逐条朗读骨架中的"核心论断"与"情感入口"——大一新生能在 3 秒内理解吗？若不能，在进入 Phase A 前先用日常白话重写。
   - 骨架以 `<!-- SKELETON: ... -->` 注释保留在脚本文件中，后续 `/audit` 可据此检查正文是否偏离骨架

   **Phase A：主体写作（占目标字数的 ~60%）**
   - **严格围绕 Phase alpha 锁定的骨架展开**，禁止在写作过程中偏离骨架引入骨架中未列出的支撑点
   - **强制前置思考 (Thought Process) - 提取火花与建构防御**：在编写前，必须识别本模块的 "Emotional/Cognitive Resonance Point" (共情火花/核心冲突点)。同时自检：**是否过早给出了答案？** 必须按建构主义法则，设计出"刻意隐瞒结论、先用对比缺陷激发疑问"的引入路径。
   - **§10 秒懂优先约束 (Instant Clarity Brake)**：写作过程中持续执行 `narrative_standards_guide.md` §10——Oppenheimer 替代测试（能用更简单的词就必须换）+ Mayer 删除测试（删掉修饰语后理解不下降就删）。§10 与 §6/§8 的情绪张力要求是**对等权重的对冲关系**：张力是油门，秒懂是刹车，两者必须同时踩。
   - **多帧连击输出 (Progressive Disclosure)**：遵循 `SKILL.md` §1 约定，**严禁将全量 SCQA 逻辑塞入单张排版**。必须依照 悬念(Full) -> 发问(Center) -> 解答(Grid/Split) 等渐进式切花序列。
   - 写入模块的主体叙事结构：多帧序列起手(痛点对比引发猜测) + 阶梯解构金字塔支撑点 + 案例/人文标签 + 微互动熔断 + VISUAL 块
   - **段落结构**：遵循 `script_format/SKILL.md` §5.2 段落物理结构规范，禁止单段超过 350 字
   - **字数目标**：模块预算的 **60%-70%**
   - Phase A 完成后，**立即调用字数中间检查点**：
     ```bash
     # 方式1: 课程级发现（V5 架构会自动编译 lesson.yaml）
     /opt/anaconda3/envs/mybase/bin/python \
       .agent/scripts/validation/validate_script_length.py \
       --course "<课程名>" --week <周次数字> --module "<模块关键词>" --segment-check

     # 方式2: 直传 segment 文件（推荐，精确针对当前文件）
     /opt/anaconda3/envs/mybase/bin/python \
       .agent/scripts/validation/validate_script_length.py \
       --file "<课程>/weeks/<周次>/src/M0X_Topic.md" \
       --module-breakdown --segment-check
     ```
   - 解析返回的 JSON（`cn_count`, `budget`, `fill_ratio`, `deficit`）

   **Phase B：先减后加（目标 100%+）**

   > [!CAUTION]
   > **教师决策权约束**：Phase B 的内容补充仅在教师明确要求时执行。Agent 在首次写作（Phase A）中应以逻辑完整为准，不应以预算缺口为由自行发起 Phase B。
   - **Step B.1 先减**：审视 Phase A 产出中的所有段落，对照 `rule_content_depth.md` §4.1 标记"冗余段 (R)"。删减冗余段后计算净字数。
   - **Step B.2 再算**：deficit = budget - 净字数（非原始字数）
   - **Step B.3 后加**：根据**净缺口**量级有针对性地补充：
     * 缺口 > 1000 字：需要新增一个完整的案例/故事段落 + 对应 VISUAL
     * 缺口 500-1000 字：为现有概念添加正反对照或深度展开
     * 缺口 < 500 字：在原有段落中添加具体细节和因果解释
   - **Step B.4 推进性自检**：每个新增段落必须通过以下自检——
     _"这段话引入了读者此前不知道的什么？"_
     * 答案为"新概念/新证据/新情感冲击" → 标记为推进段 (A)（允许）
     * 答案为"帮助理解已有概念" → 标记为支撑段 (S)（允许，但不可连续 ≥ 2 个）
     * 答案为"换了个说法" → 标记为冗余段 (R)（**禁止写入**）
   - ⚠️ **强制防注水约束 (引自 `rule_narrative_standards.md §8`)**：补充内容严禁使用空洞车轱辘话。必须引入具体痛点，做到"职业现实锚点"与"硬核认知锚点"的双向拉扯。
   - ⚠️ **§10 Mayer 修饰语删除测试**：Phase B 新增段落必须逐段执行——删掉每个修饰语后，学生对核心概念的理解会下降吗？不会则删。单段极端修饰语（极其/绝对/彻底/死死……）不超过 2 个。
   - Phase B 完成后，**再次调用验证器**确认达标

   **Phase C：达标确认**
   - 调用完整的模块验证：
     ```bash
     /opt/anaconda3/envs/mybase/bin/python \
       .agent/scripts/validation/validate_script_length.py \
       --course "<课程名>" --module-breakdown
     ```
   - 仅当该模块逻辑自检通过 **且** Slide 达底线后标记 `done`（字数预算仅作为参考，不作为硬性门禁）
    - **退化自检门 (Degeneration Gate)**：
      * 检查 `--segment-check` 返回的 `is_degenerated` 字段
      * 若 `is_degenerated == true`：禁止标记 `done`，**必须回退到 Phase A 重写退化区域**
      * 退化重写遵循 `rule_narrative_standards.md` §7.4 指南：基于知识点从零重组叙事
    - **费曼画板探针 (Feynman Canvas Probe) — 强制外显版** 🔧：
      * 对当前模块中每个含 `**加粗锚词**` 的段落，提取加粗词组
      * **强制外显**：Agent 必须输出一份 **Clarity Ledger**（清晰度台账），格式如下：

        | # | 加粗锚词 | 白话翻译（≤20字，DMA 学生秒懂版） | 生活类比来源 |
        |:---|:---|:---|:---|
        | 1 | **数据节点** | 你在小红书上点的每一个赞 | 高概率（社交媒体） |
        | 2 | **格式塔冲突** | 你的眼睛被两个矛盾的信号搞懵了 | 高概率（日常体验） |
        | 3 | **二元映射矩阵** | ❌ 无法用20字白话解释 → 回退改写 | — |

      * **Clarity Ledger 判定规则**：
        - 如果某个锚词无法在 20 字内用白话翻译 → 该段正文**必须回退改写**，用日常语言替代该术语
        - "生活类比来源"必须属于 `rule_prerequisite_awareness.md` §3.4 的**高概率经验域**（社交媒体/设计软件/视频剪辑/网购等）
        - **Vibe Coding 术语翻译强制**：如果锚词属于传统编程技术术语（如"DOM操作"、"组件状态"），必须强制翻译为 Vibe/导演视角的类比（如："指挥 AI 移动视觉图层"）。
        - **Clarity Ledger 作为 task.md 的子产物输出，用户可肉眼审阅**
      * **验证**：
        - 如果 >30% 的加粗锚词未通过费曼画板 → 禁止标记 done
      * **理论依据**：将 Agent 的内部判断（不可观测）转化为外部表格产出（可观测），打破 Pinker 知识诅咒 + LLM Self-Enhancement Bias 的循环论证
    - 若教师要求补充且字数偏低，**此时才进入素材补充流程**（但已有精确缺口数据）
   - **视觉密度即时检查**（`script_format/SKILL.md` §6 强制）：
     1. 统计当前模块的 `> [VISUAL]` 块数量
     2. 若 Slide 数 **< `⌈讲授净分钟数 ÷ 3⌉`**（底线值），禁止标记 done，须对照 §6.1 触发规则补充视觉
     3. 扫描是否存在连续 > 360 字无 `[VISUAL]` 的口述段落，若存在须拆分并插入视觉锚点
    - **Scene-Speech 意图对齐检查**（`script_format/SKILL.md` §1.4 强制）：
      1. 对当前模块每个 `> [VISUAL]` 块，提取 `Scene` 的核心**认知意图标签**（如："新旧对比冲击"、"信息过载焦虑"、"知识升维震撼"）
      2. 提取 `[VISUAL]` 块后紧随的首段 Speech 的核心**认知意图标签**
      3. 若两者的意图标签不一致或无法建立隐喻映射关系，标记为「⚠️ Scene-Speech 意图脱节」，要求修正 Scene 使其与 Speech 的心理学内核对齐
      4. 在抽象风格系统下，**不得**通过插入具象实体名词来"修复"对齐——必须通过调整隐喻/情绪/张力来实现
    - **微互动心跳校验 (Micro-Activity Check)**：
      1. 若该模块为纯理论解读，检查是否未含任何 `[ACTIVITY]`。
      2. **Quiz 优先策略**：当连续讲授 ≥ 3000 字（约 10 分钟）时，应优先插入 `Type: Quiz` 的 ACTIVITY 块。对于 Vibe Coding 主题，**严禁考核"这段代码是什么意思"**，必须转化为考核 Prompt 策略，例如："哪一段自然语言 Prompt 能让 AI 生成上述要求的网格布局？" 或 "AI 为什么会把这个组件排版错乱？"。
      3. 当连续讲授 < 3000 字但概念转折明显时，可插入 1 分钟量级的 `Type: QA` 心跳校验（如 `> [ACTIVITY] Type: QA | Duration: 1min | Desc: 灵魂发问`），打破单向说教导致的心流断裂。

    > [!CAUTION]
    > **Quiz 块格式红线**：Quiz 的题干、选项、答案和解析**必须全部写在 `> ` 引用块内部**，严禁将其写在块外作为普通 Markdown 正文。`validate_spec.py` 会自动拦截缺失字段和孤儿题目。
    >
    > **Quiz 块骨架模板**（复制后填写）：
    > ```markdown
    > 好，我们来做一个快速判断。
    >
    > > [ACTIVITY]
    > > *   **Type**: `Quiz`
    > > *   **Duration**: `2min`
    > > *   **Desc**: 概念辨析小测
    > > *   **Q**: 题干（含情境描述 + 问题）
    > > *   **Options**: A. 选项 | B. 选项 | C. 选项 | D. 选项
    > > *   **Answer**: `C`
    > > *   **Explain**: 解析，回溯逐字稿论述
    >
    > 时间到！我看到后台数据……
    > ```

> [!IMPORTANT]
> **Phase A → 中间检查点 → Phase B** 是字数达标的核心机制。禁止跳过中间检查点直接将模块标记为 done。禁止 Agent 自行估算字数——必须依赖外部验证器的精确计数。

**字数不足素材补充协议 (Material Supplement Protocol)**：

> **引用**: `rules/rule_content_depth.md` §3。当模块实际字数 < 预算 60% 时，按 DRP-L1 → L1.5 → L2 逐级补充真实素材。若补充后仍不足，标记 `<!-- SHORT_MODULE: logical_complete -->` 并继续。详见完整定义。

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
