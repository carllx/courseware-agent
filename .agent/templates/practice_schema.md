# Practice YAML 规范说明（通用模板）

> 适用于所有课程的每周实践步骤设计文档模板。每个 `W0X_practice.yaml` 遵循此结构。
> 路径：`<课程>/practices/W0X_practice.yaml`
> **本文件为通用模板 (SSOT)**，位于 `.agent/templates/practice_schema.md`。
> **Schema Version: 3.1** (2026-04-13, ADR 043 + 超星集成)
> `/new_course` 工作流 Step 2.5 会在新课程 `practices/_schema.md` 创建精简引用文件，指向本模板。

## 必填字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `week` | int | 周次编号 |
| `title` | str | 本周实践主题名称 |
| `experiment_link` | `list[int]` | 关联的实验 ID 列表（绑定 `course.yaml.experiments[].id`），无实验关联时留空或 `[]` |
| `total_minutes` | int | 实践总时长（分钟），必须 = `course.yaml` 的 `hours_practice × 45` |
| `theory_prerequisites` | list[str] | 本周实践依赖的核心理论知识点 |
| `phases` | list[Phase] | 实践各阶段 |
| `homework` | Homework | 课后作业规格 |

## Phase 对象

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | str | ✅ | 阶段编号 (P1, P2, ...) |
| `name` | str | ✅ | 阶段名称 |
| `minutes` | int | ✅ | 时长（分钟） |
| `type` | enum | ✅ | `workshop` / `practice` / `critique` / `demo` / `discussion` / `warmup` / `qa` |
| `description` | str | ✅ | 任务描述 |
| `tools` | list[str] | ✅ | 使用的工具（须属于 `course.yaml` 声明的工具子集） |
| `steps` | list[str] | ❌ | 具体步骤分解 |
| `deliverables` | list[str] | ✅ | 本阶段交付物（禁止为空） |
| `theory_link` | object/str | ⚠️ 条件必填 | **理论回链**（详见下方升级说明） |
| `upstream_dependencies`| list[Dependency]| ❌ | **跨阶段/跨周 DAG 依赖**（详见下方升级说明） |
| `materials` | list[Material] | ❌ | 素材定义列表（详见下方 Material 对象） |

### theory_link — 结构化理论回链（CA 构建性对齐）

> 借鉴 Biggs 构建性对齐理论：每个教学活动 (TLA) 必须显式回链到预期学习成果 (ILO)。

**条件必填规则**：当 Phase `type ∈ {workshop, practice, critique}` 时**必填**。`warmup` / `demo` / `qa` / `discussion` 类型免填。

**唯一合法格式（结构化对象）**：

```yaml
theory_link:
  concept_id: "preattentive_processing"    # 必须匹配 <课程>/concept_registry.yaml concepts[].id
  course_objective: "知识1"                 # 可选，匹配 course.yaml supported_objectives[]
  description: "前注意处理与视觉弹出效应"    # 人类可读补充说明（可选）
```

> [!CAUTION]
> **纯字符串格式已废弃 (v3.0)**：`/audit_deep` Part H 会标记为 `[CA_LEGACY_FORMAT]` 错误。所有 theory_link 必须使用结构化对象格式，`concept_id` 引用独立的 `<课程>/concept_registry.yaml`（非 course.yaml 内嵌）。

### upstream_dependencies — 跨周 DAG 依赖声明

> 借鉴有向无环图 (DAG) 建模：显式声明跨阶段/跨周次的数据流依赖。

```yaml
upstream_dependencies:
  - source: "W03.P1"          # 源节点：周次.Phase_ID
    artifact: "tidy_csv"      # 依赖的具体产出物标识
    required: true             # 硬依赖(true) / 软依赖(false)
```

当实践步骤的 `description` 或 `steps` 中引用了其他周次的产出物但 `upstream_dependencies` 为空时，`/audit_deep` Part H 会标记 `[UPSTREAM_IMPLICIT]` 警告。

## Material 对象

每个 material 通过 `type` 字段区分素材类型，不同 type 拥有各自专属字段。

### 通用字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | enum | ✅ | 素材类型枚举（见下表） |
| `title` | str | ✅ | 素材标题 |

### Material Type 枚举

| `type` | 用途 | 特有字段 |
|---|---|---|
| `poll` | 投票/表决活动 | `rounds[]`（含 `stimulus`, `options`, `answer`, `reveal`） |
| `quiz` | 限时测试题 | `questions`, `time_limit_sec`, `chaoxing_export` |
| `critique_card` | 找茬/评审卡 | `image`, `context`, `known_issues[]`, `rubric` |
| `tutorial_steps` | 工具操作指南 | `steps[]`（含 `screenshot`, `instruction`, `data_file`） |
| `dataset` | 数据集素材 | `file`, `format`, `rows`, `columns`, `schema`, `preview` |
| `code_template` | 代码模板/残缺代码 | `file`, `language`, `scaffold_zones[]` |
| `case_study` | 案例展示 | `images[]`, `context`, `discussion_prompts` |
| `comparison` | 对比材料 | `items[]`（A/B 对比图组，含 `label`, `image`, `description`） |

> **开放枚举**：上述 8 种为核心类型，教师可自定义新 type 并在此文档补充说明。

#### quiz 类型扩展字段（v3.1）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `questions` | int | ✅ | 题目数量 |
| `time_limit_sec` | int | ❌ | 限时秒数（如 180） |
| `chaoxing_export` | str | ❌ | 超星导出文件的相对路径（如 `practices/materials/W01/chaoxing_quiz_w01.txt`）|

> 当 `chaoxing_export` 存在时，`validate_practice.py` 校验该文件物理存在（校验规则 11）。
> 生成协议详见 `chaoxing-quiz` Skill。

## Homework 对象

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` | str | ✅ | 作业标题 |
| `description` | str | ✅ | 作业描述 |
| `deliverables` | list[str] | ✅ | 提交物清单（严禁置空） |
| `experiment_data_link` | str | ❌ | 关联的实验数据集 |
| `materials` | list[Material] | ❌ | 作业所需素材（复用 Material 对象） |

> [!CAUTION]
> **以下字段已废弃 (v3.0, ADR 043)**：
> - ~~`weight`~~ — 成绩权重的 SSOT 在 `course.yaml.assessment_methods`，practices/ 层禁止定义（参见 `rule_document_boundaries.md` §6.5）
> - ~~`scoring_rubric`~~ — 同上，评分标准的权威定义在 `course.yaml`
> - Phase 对象中同样**禁止**出现 `weight` 或 `scoring_rubric` 字段

## 素材文件目录约定

```
<课程>/
└── practices/
    └── materials/       ← 素材物理文件存放根目录（SSOT）
        ├── W01/         ← 按周次组织
        │   ├── *.png/svg    ← 图片素材
        │   └── *.csv/xlsx   ← 数据素材
        ├── W02/
        └── shared/      ← 跨周共享素材
```

- 素材路径在 YAML 中使用 **相对于课程根目录** 的路径（如 `practices/materials/W01/...`）
- **practice_guide.md 中的图片引用**：统一使用 `../../practices/materials/W0X/` 相对路径（从 `weeks/W0X/practice_guide.md` 出发）
- 命名使用小写英文 + 下划线，如 `anscombe_group1_scatter.png`

> [!CAUTION]
> **`weeks/W0X/public/practice/` 路径已废弃**（v3.1.1）。所有 practice 专用素材必须存放在 `practices/materials/W0X/` 中。`public/` 目录仅保留给 H5 课件构建专用资产（slides、textbook 等），practice 图片不得混入。


## 校验规则

1. `sum(phases[].minutes)` = `total_minutes`
2. `total_minutes` = `course.yaml` 对应周的 `hours_practice × 45`
3. `tools[]` ⊂ `course.yaml.resources_url` 声明的工具集
4. `experiment_link` 须为 `list[int]`，每个元素须匹配 `course.yaml.experiments[].id`
5. `materials[].type` 须属于本文档定义的枚举集（含自定义扩展）
6. `materials` 中引用的文件路径须存在于对应的 `weeks/W0X/assets/` 或 `<课程>/practices/materials/` 目录中
7. **theory_link 条件必填**：当 phase `type ∈ {workshop, practice, critique}` 时不得为空
8. **theory_link 引用完整性**：`concept_id` 须存在于 `<课程>/concept_registry.yaml concepts[]`（独立文件，非 course.yaml 内嵌）
9. **upstream_dependencies 一致性**：若 `description/steps` 引用其他周次产出物且 `upstream_dependencies` 为空 → 标记 `[UPSTREAM_IMPLICIT]`
10. **SSOT 越界禁止**：practice.yaml 的 Phase 或 Homework 对象中**不得出现** `weight` 或 `scoring_rubric` 字段（SSOT 在 course.yaml）
11. **quiz 导出文件存在性**：当 `materials[type:quiz].chaoxing_export` 非空时，对应路径的 `.txt` 文件须物理存在于 `<课程>/` 下
12. **下游衍生文档一致性 (practice_guide.md)**：
    - (a) 同目录下须存在 `practice_guide.md`（学生操作指南）
    - (b) 指南中不得出现课程级过时术语（由 `<课程>/stale_terms.yaml` 声明，验证器不硬编码任何特定课程术语）→ 标记 `[GUIDE_STALE_TERM]`
    - (c) `practice.yaml` 的 `theory_prerequisites[]` 中的每个条目须在 `practice_guide.md` 中出现 → 标记 `[GUIDE_PREREQ_DRIFT]`
    - (d) 通过 `theory_link.concept_id` 关联的概念名称（来自注册表）应在指南中提及 → 标记 `[GUIDE_CONCEPT_MISSING]`（信息级）

> [!IMPORTANT]
> **终极闭环产出要求**：所有 YAML 修改生效并生成完材料后，**必须强制**使用 Markdown 为该次实践额外补充渲染并生成用于学生阅读操作的手册方案：`weeks/W0X_Name/practice_guide.md` 或 `<课程>/practices/W0X_Practice_Guide.md`，以此实现真正的双轨交付。
