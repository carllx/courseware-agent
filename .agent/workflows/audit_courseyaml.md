---
description: 深度审计 — Part F (course.yaml 合规性检查 F1-F16)。仅在 /audit --deep 且审计范围含 course.yaml 时加载。
---

# /audit Deep 级别 — Part F: course.yaml 合规性检查

> **加载条件**：仅当执行 `/audit --deep` 且审计范围包含 course.yaml 或需要全量校验时加载。
> **注意**：Part F 需要加载 `course.yaml` 全文（跨周引用校验），不使用 `extract_week.py`。

---

*   **F1: `content` 编号前缀与 `chapter_title` 合规性**
    *   `calendar[].content` 每行必须自带编号前缀（如 `1.1`、`2.3`），WYSIWYG 模式下文本即最终大纲输出
    *   `calendar[].chapter_title` 必须存在且格式为 `"第X章 {topic}"`
    *   含实验内容的周次须挂载 `exp_id`
    *   范围：工作区内所有课程的 `course.yaml`
*   **F2: `lessons[].steps` 5 阶段完整性**（另见 F14 stage 分钟归属校验）
    *   首周允许省略 `复习`，常规周必须包含 `复习/导入/讲授/实践/小结` 全部 5 阶段，末周可灵活裁剪
    *   同一 stage 不应连续出现两次（如连续两个 `导入`），应合并或重新分类
    *   检查方法：逐周提取 `steps[].stage` 值集合，对比约束表
*   **F3: ADR 008 类型约束校验**
    *   `teaching_requirements` → `str` 或 `dict`（dict 格式：`{knowledge, ability, quality, method}` 供教案分维度展示，大纲生成器自动扁平化）
    *   `supported_objectives` → `list[str]`
    *   `focus` / `difficulty` / `ideology` / `teaching_method` → `str`
    *   `lessons` → `list[dict]`
*   **F4: objectives 数量与 mappings 格式（ADR 010）**
    *   每个维度（`knowledge` / `ability` / `quality`）条目数 ≥ 3
    *   每条目标使用 `mappings` 数组格式，**禁止**使用旧 flat 格式（`requirement/point/support_level` 顶层字段）
    *   每条 `desc` 内容不可与同维度其他条目笼统重复，需有独立教学聚焦点
*   **F5: `supported_objectives` 引用完整性（ADR 010）**
    *   **无悬空引用**：`calendar[].supported_objectives` 中的引用（如 `知识2`）必须在 `objectives` 中有对应编号
    *   **无孤儿目标**：`objectives` 中每条目标至少被一个 CalendarWeek 的 `supported_objectives` 引用；若有孤儿目标，标记警告但不 Fail（允许存在但不教学的预留目标）
    *   检查时同步生成引用覆盖率报告：`知识N/能力N/素质N` 各被引用的周次列表
*   **F6: `experiments[].type` 枚举合法性（ADR 011 / 实验新规）**
    *   合法值仅限 `设计性` 和 `综合性`。不再允许验证性、演示性等其他类型。
    *   检查方法：遍历 `experiments[].type`，比对白名单 `["设计性", "综合性"]`。
*   **F8: `group_size` 和 `requirement` 字段存在性（ADR 011）**
    *   `experiments[]` 每项的 `group_size` 和 `requirement` 必须存在且非空
*   **F9: `final_item` 必填性（ADR 011）**
    *   当 `final_score_ratio > 0` 时，`assessment_methods` 必须含 `final_item`
*   **F10: `exams` 类型枚举（ADR 011）**
    *   `exams.final_exam[].sections[].questions[].type` 必须使用标准枚举值（`验证性`/`综合性`/`设计性`/`演示性`）
*   **F11: 多班 `classes[]` 合规性检查（ADR 012）**
    *   多班课程（`classes[]` 长度 > 1）时，每个班级必须声明 `week_range` 和 `official_weeks`
    *   `excluded_weeks` 中的周次必须在 `week_range` 范围内
    *   `hours` 节点应含 `per_class: true` 以消除学时歧义
    *   不应存在无消费者的冗余字段（如 `session_time_overrides`、`schedule_segments`），除非生成器确实需要读取
*   **F12: 生成器输出完整性抽检（ADR 013）**
    *   对含 `excluded_weeks` 或节假日影响的课程，运行 `generate.py` 后抽检进度表末尾行是否有内容（防止偏移映射回归）
    *   验证教案生成数量 = `len(calendar)` 减去被 `excluded_weeks` 命中且存在于 calendar 中的周数
    *   方法：运行生成命令后用 `python-docx` 读取进度表，检查每行 W{N} 的教学内容列是否为空
*   **F13: 实验编号命名合规性（ADR 017）**
    *   `weeks/W*/src/*.md` 正文和 `course.yaml` 的 `content`/`task`/`summary` 字段中，实验引用必须使用 `实验N(ExpN)` 格式
    *   Frontmatter `tags`、Slide 标识符（如 `S07_Exp3_WrapUp`）、`exp_id` 注释行中允许保留裸 `Exp[n]`
    *   检查方法：`grep -P '\bExp[1-4]\b'` 扫描正文，排除 frontmatter 和技术标识符上下文

*   **F14: 教学环节 `stage` 分类校验（MSG-012 / L1 写入校验）**（另见 F2 stage 种类完整性）
    *   **分类归属表**：
        | 归属 | stage 关键词 |
        |:----:|:----------:|
        | 理论学时 | 复习、导入、讲授、演示 |
        | 实践学时 | 实践、练习、训练、总结、小结 |
    *   **C-1**: W1（`calendar[0]`）的 steps 中不得出现 `stage: 复习`（首次课无先前内容可复习）
    *   **C-2**: 每周 steps 的理论/实践 stage 分钟折算学时（÷ `minutes_per_period`）与 `hours_theory`/`hours_practice` 偏差 > 0.5h → `[WARN]`，> 1h → `[CRITICAL]`
    *   **C-3**: `hours_theory=0` 的纯实践周，理论 stage 总分钟 > 30min → `[WARN]`
    *   **C-4**: `∑steps[].minutes` 与 `(hours_theory + hours_practice) × minutes_per_period` 偏差 > 15% → `[WARN]`，> 1 课时 → `[CRITICAL]`
    *   检查方法：**优先**运行 `python scripts/validate_steps.py`（课程端本地校验），或运行教务端 `audit_course_data.py --root .`；严格模式加 `--strict` 查看所有偏差
    *   **触发时机**：任何对 `calendar[].lessons[].steps` 的写入或修改后

*   **F15: 目标覆盖密度预警（知识链防御 — 根因4）**
    *   遍历 `objectives` 中每条目标（如 `知识1`…`素质3`），统计其在 `calendar[].supported_objectives` 中被引用的**周次数**
    *   引用次数 = 1 → 标记 `[OBJ_THIN_COVER]` ⚠️，附带该目标 ID 与唯一支撑周次
    *   引用次数 = 0 → 已有 F5 覆盖（孤儿目标），此处不重复
    *   输出格式：生成**目标覆盖密度矩阵**（目标 ID × 被引用周次列表），附在审计报告末尾
    *   **原理**：仅 1 周独撑的目标极度脆弱——该周脚本一旦删减模块，目标将彻底脱链

*   **F16: 知识库条目核销（知识链防御 — 根因1）**
    *   遍历 `knowledge_hub.yaml` 所有条目 ID，检查是否在任意 `weeks/W*/src/*.md` 中被引用（搜索范围：`核心理论库` 行 + `[TECH NOTE]`/`[CASE STUDY]` 正文中的 `` `条目ID` `` 反引号引用）
    *   未被任何脚本引用 → 标记 `[HUB_ORPHAN]` ⚠️，附带条目 ID、类型与摘要
    *   **与 F5 的区别**：F5 检查 `supported_objectives` 引用完整性（目标 → 周次），F16 检查知识库条目引用完整性（条目 → 脚本）
    *   **原理**：入库但未入链的条目意味着知识库索引与教学实践脱节——要么是遗漏引用，要么应从 hub 移除

*   **F17: 实验数量与排布硬性约束（实验新规）**
    *   本检查依赖 `hours.practice` (实践学时) 和 `experiments` 数组。
    *   **40实践学时课程**：`experiments` 长度必须恰好为 3。排布必须为：Exp1(设计性), Exp2(设计性), Exp3(综合性)。
    *   **60实践学时课程**：`experiments` 长度必须恰好为 4。排布必须为：Exp1(设计性), Exp2(设计性), Exp3(设计性), Exp4(综合性)。
    *   **类型兜底检查**：不论实践学时，`综合性` 实验必须有且只有一个，且必须是数组的最后一个元素。
