# Practice YAML 规范说明（通用）

> 适用于所有课程的每周实践步骤设计文档模板。每个 `W0X_practice.yaml` 遵循此结构。
> 路径：`<课程>/practices/W0X_practice.yaml`

## 必填字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `week` | int | 周次编号 (1-8) |
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
| `theory_link` | str | ❌ | 回链的理论知识点 |
| `upstream_dependencies`| list[str]| ❌ | 跨阶段/跨周依赖（如需 W03 清洗的 CSV 数据） |
| `materials` | list[Material] | ❌ | **素材定义列表**（详见下方 Material 对象） |

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

### poll — 投票活动

```yaml
materials:
  - type: poll
    title: "安斯库姆四重奏趋势预测"
    rounds:
      - round: 1
        stimulus:
          image: "practices/materials/W01/anscombe_group1_numbers.png"
          caption: "数据组 I：X/Y 数值表"
        options: ["线性上升", "曲线", "离散分布", "无明显趋势"]
        answer: "线性上升"
        reveal:
          image: "practices/materials/W01/anscombe_group1_scatter.png"
          explanation: "组 I 呈现经典线性关系"
```

### quiz — 限时测试题

```yaml
materials:
  - type: quiz
    title: "前注意弹出限时挑战"
    time_limit_sec: 8
    questions:
      - id: Q1
        image: "practices/materials/W01/preattentive_color_pop.png"
        prompt: "图中红色圆点共有几个？"
        question_type: judgment   # judgment | choice | short_answer
        answer: true
        explanation: "颜色属于前注意属性，可在 200ms 内弹出"
```

### critique_card — 找茬评审卡

```yaml
materials:
  - type: critique_card
    title: "找茬第 1 题"
    image: "practices/materials/W01/bad_3d_pie_chart.png"
    context: "某公司年度财报中的市场份额图表"
    known_issues:
      - category: "前注意属性误用"
        description: "3D 透视导致面积感知偏差"
        severity: critical    # critical | major | minor
      - category: "格式塔原则违反"
        description: "相似色相导致相邻切片无法区分"
        severity: major
    rubric:
      full_marks: 5
      criteria: "至少识别 2 个问题并引用正确的感知原则"
```

### tutorial_steps — 工具操作指南

```yaml
materials:
  - type: tutorial_steps
    title: "RAWGraphs 数据映射探索"
    steps:
      - step: 1
        instruction: "打开 RAWGraphs，点击 'Paste your data'"
        screenshot: "practices/materials/W01/rawgraphs_step1.png"
      - step: 2
        instruction: "粘贴示范 CSV 数据"
        screenshot: "practices/materials/W01/rawgraphs_step2.png"
        data_file: "practices/materials/shared/sample_data.csv"
```

### dataset — 数据集

```yaml
materials:
  - type: dataset
    title: "示范数据集"
    file: "practices/materials/shared/sample_data.csv"
    format: csv
    source_url: "https://www.gapminder.org/data/"
    license: "CC-BY 4.0 / 公共领域"
    rows: 195
    columns: ["country", "year", "gdp"]
    schema:
      keys: ["country", "year"]
      values: ["gdp"]
      types:
        country: categorical
        year: ordinal
        gdp: quantitative
```

### code_template — 代码模板

```yaml
materials:
  - type: code_template
    title: "D3 力导向残缺代码"
    file: "practices/materials/W04/d3_force_buggy.html"
    language: html
    scaffold_zones:
      - zone: "比例尺定义"
        hint: "此处 scaleLinear 的 domain 与 range 参数被交换"
      - zone: "数据绑定"
        hint: "selectAll 选择器与 append 元素不匹配"
```

### case_study — 案例展示

```yaml
materials:
  - type: case_study
    title: "防疫追踪 vs 监控网络"
    images:
      - "practices/materials/W05/contact_tracing_network.png"
      - "practices/materials/W05/surveillance_network.png"
    context: "同种力导向图因社会语境产生对立隐喻"
    discussion_prompts:
      - "技术中立是否是一种伪命题？"
      - "可视化设计师的伦理边界在哪里？"
```

### comparison — 对比材料

```yaml
materials:
  - type: comparison
    title: "前注意 vs 非前注意视觉搜索"
    items:
      - label: "有前注意属性（颜色弹出）"
        image: "practices/materials/W01/preattentive_with.png"
        description: "红色目标立即弹出，搜索时间 < 200ms"
      - label: "无前注意属性（需逐一扫描）"
        image: "practices/materials/W01/preattentive_without.png"
        description: "需顺序扫描每个元素，搜索时间随数量线性增长"
```

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

> [!NOTE]
> **架构变更 (2026-03-28)**：目录模型已从"按类型分目录"迁移至"按教学周分目录"。
> 所有教学内容统一存放在 `weeks/W0X_Name/` 教学单元包中。

```
<课程>/
├── weeks/                               ← 统一教学周目录
│   └── W0X_Name/                        ← 自洽的教学单元包
│       ├── script.md                    ← 逐字稿
│       ├── practice.yaml                ← 实践规格 (本文档定义的结构)
│       ├── practice_guide.md            ← 面向学生的操作手册
│       └── assets/                      ← 统一素材目录
│           ├── slides/                  ← 理论幻灯片素材 (S*.png)
│           ├── textbook/                ← 教材引用图
│           ├── practice/                ← 实践用图/截图
│           └── data/                    ← 数据文件 (csv/xlsx)
├── shared_assets/                       ← 跨周共享资源
└── practices/                           ← 全局性文件（非周次文件）
    ├── _schema.md                       ← 本文档
    ├── experiment_planning.md
    └── project_brief.md
```

- 素材路径在 YAML 和 Markdown 中使用 **相对于教学周目录** 的路径（如 `assets/practice/xxx.png`）
- `script.md` 和 `practice_guide.md` 共享同一 `assets/` 前缀，零路径翻译
- 命名使用小写英文 + 下划线，如 `anscombe_group1_scatter.png`
- 旧的 `scripts/W0X_Name.md` 符号链接仍可用（指向 `weeks/*/script.md`）

## 校验规则

1. `sum(phases[].minutes)` = `total_minutes`
2. `total_minutes` = `course.yaml` 对应周的 `hours_practice × 45`
3. `tools[]` ⊂ `course.yaml.resources_url` 声明的工具集
4. `experiment_link` 须准确映射由 `experiment_planning.md` 划定的周次/阶段，跨周实验须在对应周次声明。
5. `materials[].type` 须属于本文档定义的枚举集（含自定义扩展）
6. `materials` 中引用的文件路径须存在于对应 `weeks/W0X_Name/assets/` 目录中

> [!IMPORTANT]
> **终极闭环产出要求**：所有 YAML 修改生效并生成完材料后，**必须强制**使用 Markdown 为该次实践额外补充渲染并生成用于学生阅读操作的手册方案：`weeks/W0X_Name/practice_guide.md`，以此实现真正的双轨交付。
