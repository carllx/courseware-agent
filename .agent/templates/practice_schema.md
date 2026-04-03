# Practice YAML 规范说明（通用模板）

> 适用于所有课程的每周实践步骤设计文档模板。每个 `W0X_practice.yaml` 遵循此结构。
> 路径：`<课程>/practices/W0X_practice.yaml`
> **本文件为通用模板**，位于 `.agent/templates/practice_schema.md`。
> `/new_course` 工作流 Step 2.5 会自动复制到新课程的 `practices/_schema.md`。

## 必填字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `week` | int | 周次编号 |
| `title` | str | 本周实践主题名称 |
| `experiment_link` | str | 关联的实验名称（对应 `experiment_planning.md` 划定的周次/阶段），无实验关联时留空 |
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

**推荐格式（结构化对象）**：

```yaml
theory_link:
  concept_id: "preattentive_processing"    # 必须匹配 course.yaml concept_registry[].id
  course_objective: "知识1"                 # 必须匹配 course.yaml supported_objectives[]
  description: "前注意处理与视觉弹出效应"    # 人类可读补充说明（可选）
```

**向后兼容格式（纯字符串）**：

```yaml
theory_link: "前注意处理 (Pre-attentive Processing)"
```

> [!WARNING]
> 纯字符串格式仍可解析，但 `/audit_deep` Part H 会标记为 `[CA_LEGACY_FORMAT]` 警告，建议升级为结构化格式。

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
| `quiz` | 限时测试题 | `questions[]`, `time_limit_sec`, `scoring` |
| `critique_card` | 找茬/评审卡 | `image`, `context`, `known_issues[]`, `rubric` |
| `tutorial_steps` | 工具操作指南 | `steps[]`（含 `screenshot`, `instruction`, `data_file`） |
| `dataset` | 数据集素材 | `file`, `format`, `rows`, `columns`, `schema`, `preview` |
| `code_template` | 代码模板/残缺代码 | `file`, `language`, `scaffold_zones[]` |
| `case_study` | 案例展示 | `images[]`, `context`, `discussion_prompts` |
| `comparison` | 对比材料 | `items[]`（A/B 对比图组，含 `label`, `image`, `description`） |

> **开放枚举**：上述 8 种为核心类型，教师可自定义新 type 并在此文档补充说明。

## Homework 对象

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` | str | ✅ | 作业标题 |
| `description` | str | ✅ | 作业描述 |
| `deliverables` | list[str] | ✅ | 提交物清单（严禁置空） |
| `weight` | str | ✅ | 成绩占比标记（如 30% / 期末部分） |
| `scoring_rubric` | dict | ❌ | 结构化评分量表/判分维度 |
| `experiment_data_link` | str | ❌ | 关联的实验数据集 |
| `materials` | list[Material] | ❌ | 作业所需素材（复用 Material 对象） |

## 素材文件目录约定

```
<课程>/
└── practices/
    └── materials/       ← 素材物理文件存放根目录
        ├── W01/         ← 按周次组织
        │   ├── *.png/svg    ← 图片素材
        │   └── *.csv/xlsx   ← 数据素材
        ├── W02/
        └── shared/      ← 跨周共享素材
```

- 素材路径在 YAML 中使用 **相对于教学周目录** 的路径（如 `assets/practice/...`）或 **相对于课程根目录** 的路径（如 `practices/materials/W01/...`）
- 命名使用小写英文 + 下划线，如 `anscombe_group1_scatter.png`

## 校验规则

1. `sum(phases[].minutes)` = `total_minutes`
2. `total_minutes` = `course.yaml` 对应周的 `hours_practice × 45`
3. `tools[]` ⊂ `course.yaml.resources_url` 声明的工具集
4. `experiment_link` 须准确映射由 `experiment_planning.md` 划定的周次/阶段，跨周实验须在对应周次声明。
5. `materials[].type` 须属于本文档定义的枚举集（含自定义扩展）
6. `materials` 中引用的文件路径须存在于对应的 `weeks/W0X/assets/` 或 `<课程>/practices/materials/` 目录中
7. **theory_link 条件必填**：当 phase `type ∈ {workshop, practice, critique}` 时不得为空
8. **theory_link 引用完整性**：`concept_id` 须存在于 `course.yaml.concept_registry[]`；`course_objective` 须存在于同周 `supported_objectives[]`
9. **upstream_dependencies 一致性**：若 `description/steps` 引用其他周次产出物且 `upstream_dependencies` 为空 → 标记 `[UPSTREAM_IMPLICIT]`

> [!IMPORTANT]
> **终极闭环产出要求**：所有 YAML 修改生效并生成完材料后，**必须强制**使用 Markdown 为该次实践额外补充渲染并生成用于学生阅读操作的手册方案：`weeks/W0X_Name/practice_guide.md` 或 `<课程>/practices/W0X_Practice_Guide.md`，以此实现真正的双轨交付。
