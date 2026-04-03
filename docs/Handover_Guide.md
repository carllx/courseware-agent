# 2025-2026-2 学期课程备课交接文档 v1.0

## 1. 项目概况
本项目 (`/Users/yamlam/Downloads/2025-2026-2 课程`) 是基于 **Agent 驱动的多课程备课框架** 的工作区。核心目标是将内容创作与格式工程解耦，利用 `/Users/yamlam/Downloads/教务材料` (TMA) 工具链自动生成教学大纲、进度表和教案。

## 2. 环境与工具链
### 2.1 关键路径
- **工作区根目录**: `/Users/yamlam/Downloads/2025-2026-2 课程`
- **工具链目录**: `/Users/yamlam/Downloads/教务材料`
- **Python 环境**: `/opt/anaconda3/envs/mybase` (必须使用此环境以确保依赖正确)

### 2.2 核心命令
所有生成命令需在 **工具链目录** (`教务材料`) 下执行：

```bash
cd /Users/yamlam/Downloads/教务材料

# 生成特定课程的所有文档 (大纲、进度表、教案)
python scripts/generate.py --course "交互产品开发"
python scripts/generate.py --course "信息可视化"
```

## 3. 课程状态与行动指南

### A. [无需行动] 实习指导 (Internship Guidance)
- **状态**: 🟢 活跃 (Active)
- **类型**: Project
- **配置**: `实习指导/course.yaml`
- **注意**: 该课程使用非标准 Schema，与通用生成器不兼容。

### B. [已修正] 信息可视化 (Information Visualization)
- **状态**: ⚠️ 配置就绪 (复杂排课)
- **代码**: `CNFU003847`
- **学时**: 40学时 (2.0学分)
- **班级结构**:
    1. **影视班**: 1-8周 (5节/周)
    2. **游戏班**: 10-18周 (分段排课)
- **已知限制**: `course.yaml` 的 `calendar` 结构性字段（week/topic/hours）可由 `sync_syllabus.py` 从脚本 frontmatter 同步。但教案索引字段（`supported_objectives`/`task`/`lessons`/`steps`）和大纲渲染字段（`teaching_requirements`/`focus`/`difficulty`/`ideology`/`teaching_method`）是**直接在 `course.yaml` 维护**的，不经过 frontmatter（ADR 007/008）。
- **objectives 状态**: ✅ 知识/能力/素质 各 3 条，使用 `mappings` 数组格式（ADR 010）。

### C. [已修正] 交互产品开发 (Interaction Product Development)
- **状态**: 🟢 配置就绪
- **代码**: `CNFU002572`
- **学时**: 60学时 (3.0学分)
- **进度**: 1-15周 (周三 2-5节)
- **特殊模式**: 本课程无逐字稿 (`scripts/W*.md`)，所有 calendar 数据直接在 `course.yaml` 维护（ADR 008 正式化的"无脚本课程模式"）。
- **objectives 状态**: ✅ 知识/能力/素质 各 3 条，使用 `mappings` 数组格式（ADR 010）。

## 4. 实验文档处理
> [!NOTE]
> **自动化就绪（2026-02-24）**：两门课程 `course.yaml → experiments` 字段已完全对齐 TMA Schema，`04_Experiment_Generator` 可直接驱动生成。

### 当前实验类型分布（对齐 Spec §1.2，满足 ≥ 3 种要求）

| 课程 | 实验1 | 实验2 | 实验3 | 实验4 | 认定表 |
|------|------|------|------|------|:-----:|
| 信息可视化 | 验证性 | 设计性 | 综合性 | 综合性 | 3份 |
| 交互产品开发 | 验证性 | 综合性 | 设计性 | 综合性 | 3份 |

### 生成命令（待 TMA 开发完成后）
```bash
cd /Users/yamlam/Downloads/教务材料
python scripts/gen_experiment_xml.py --course "信息可视化"
python scripts/gen_experiment_xml.py --course "交互产品开发"
```

### 信息可视化双班说明（ADR 012）
- **教案**：一门课一份教案（8周统一备课），不分班
- **进度表**：以班为单位各出一份（影视班 W1-8 / 游戏班 W10-18）
- **假期吸收**：W16 端午节进度表跳过日期行，`official_weeks` 不扣减（影视班 8 / 游戏班 9）
    - ⚠️ **偏移映射已修复（2026-02-24）**：`content_map` 构建时自动跳过 `excluded_weeks` + 节假日，calendar 内容顺延。游戏班 W16 显示"节假日停课"，W17-W18 从 calendar[6-7] 正确填充。
- **节次出入**：忽略（W14-W18 节次差异不影响教案内容）

## 5. 常见问题
- **报错 `Config not found`**: 检查 `course.yaml` 路径。
- **日期计算错误**: 检查 `course.yaml` 中的 `semester_config.start_date` (本学期应为 `2026-03-02`)。
- **假日未生效**: 假日数据从 `semester_calendar.yaml` 加载，代码中无硬编码（ADR 014）。若假日跳过不生效，检查 `00_Data_Context/semester_calendar.yaml` 是否已更新当前学期的假日列表。
- **报错 `'exams' is undefined`**: `course.yaml` 缺少 `exams` 节点。即使是考查课也必须填写此字段，否则 Jinja 模板渲染会报错。
- **评分项命名被退回**: `normal_items.name` 必须使用 `章节测试N` 或 `命题测试N` 格式（无括号），`desc` 需关联对应实验并注明考核要求。详见 ADR 005。
- **大纲"三、课程内容和教学要求"表格为空**: `course.yaml` 的 `calendar` 条目需补全 `teaching_requirements`、`focus`、`difficulty`、`ideology`、`teaching_method` 五个字段。缺省时生成器仅渲染空白占位标签。详见 ADR 006。
- **`teaching_requirements` 是 dict 而非 string**: 必须为文本字符串（以"通过本章学习"开头），不得使用结构化 dict。若误用会导致大纲渲染静默失败。详见 ADR 008。
- **`objectives` 使用旧 flat 格式**: `course_schema.py` 的 `ObjectiveItem` 已移除旧版 flat 字段（`requirement`/`point`/`support_level`），Pydantic 会直接拒绝含这些字段的数据。必须使用 `mappings: [{requirement, point, support_level}]` 数组格式。详见 ADR 010 & ADR 014。
- **教案首页课程目标表残缺**: 教案首页模板按知识/能力/素质三维度生成目标表，官方标准每维度 ≥ 3 条。若 `objectives` 每维度仅 1 条，表格行数不足，显示残缺。需在 `course.yaml` 中为每维度补充至 ≥ 3 条目标。详见 ADR 010。
- **`supported_objectives` 引用了不存在的目标编号**: 如 `calendar` 中出现 `知识2` 但 `objectives.knowledge` 仅定义了 `index: 1`，会导致教案生成器引用失败。执行 `/audit Part F5` 检查双向引用一致性。详见 ADR 010。
- **`experiments[].type` 枚举不合规**: 合法值仅限 `验证性`、`综合性`、`设计性`、`演示性`（含「性」后缀）。`创新`、`研究`、`验证`、`设计` 等均为不合规值，会导致 TMA 生成器类型匹配失败（认定表不触发）。详见 ADR 011。
- **实验类型种类不足**: 同一课程的 4 个实验必须涵盖 ≥ 3 种不同 type，满足教务「不低于 3 种」要求。推荐：实验1 验证性、实验2/3 设计性+综合性各一、实验4 综合性。详见 ADR 011。
- **`group_size` / `requirement` 缺失**: 这两个字段在 TMA Schema 中为必填，缺失时实验指导书「项目一览表」的每组人数和开出要求两列将为空白。详见 ADR 011。
- **`assessment_methods` 缺少 `final_item`**: 凡有 `final_score_ratio > 0` 的课程，必须同时在 `assessment_methods` 中填写 `final_item`（期末考核说明），不可仅有 `normal_items`。详见 ADR 011。
- **认定表触发条件**: 仅 `type` 为 `综合性` 或 `设计性` 的实验生成认定表；`验证性` 和 `演示性` 实验无需认定（标准答案可判定质量，无需专家审查）。详见 Spec_Experiment.md §4.2。
- **进度表末尾周为空**: 当 `excluded_weeks` 或节假日位于 `week_range` 中间时，旧版偏移映射使用简单 `offset + ci` 会"吃掉"一个 calendar 条目导致末尾周空行。已修复为自动跳过停课周映射（ADR 013 / ISSUE-009）。
- **`_deprecated/` 目录**: 已于 2026-02-24 清除（ADR 014）。废弃代码由 Git 历史归档，禁止重建此目录。
- **Jinja/docxtpl 相关报错**: 项目已完全迁移到纯 XML 操作方案（`docx_engine.py`），不再使用 `docxtpl` 或 Jinja 模板。若遇到相关报错，说明引用了过时代码路径。详见 ADR 004（历史记录）& ADR 014。


