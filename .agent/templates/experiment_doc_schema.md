# 课程大实验 — 增量文档规范 (Experiment Increment Schema)

> **全量 SSOT (Single Source of Truth)**：
> - `practices/experiments/exp_X.yaml` — 单一实验的**完全事实源**（包含 id, name, type, hours, objectives, equipment 等所有教务元数据，以及 steps, rubric 等执行细节）。
> - `practices/experiment_planning.md` — 实验细则概览（目标/工具/交付物/周次等）
>
> **本文件职责**：
> 定义 `practices/experiments/exp_X.yaml` 的全量配置规范。
> 根据最新架构决策，已废弃“course_experiments.yaml(总表) + exp_X.yaml(增量)”的双轨模式，彻底消除数据同步带来的孤儿数据问题。
>
> **存放路径**：`<课程>/practices/experiments/exp_X.yaml`
> **工具链**：由 `/design_experiment` 工作流及底层解析脚本驱动。
> **生成机制**：引擎遍历读取 `practices/experiments/` 下的独立 YAML，在内存中拼接为完整的课程实验清单，进而生成各级教务与教学文档。
>
> **合规约束**：
> - 必须在 `exp_X.yaml` 中全量填写所有必需字段。
> - 实验类型枚举必须使用含"性"后缀的值：`验证性`/`综合性`/`设计性`/`演示性`（ADR 011）

---

## 一、 全量 YAML 结构

`exp_X.yaml` 需要包含以下教务元数据与教学增量数据：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `exp_id` | int/str | ✅ | 实验编号，引擎据此进行全局排序 |
| `name` | str | ✅ | 实验名称 |
| `type` | str | ✅ | 实验类型（验证性/综合性/设计性/演示性） |
| `hours` | int | ✅ | 实验学时 |
| `group_size` | int | ✅ | 每组人数 |
| `requirement` | str | ✅ | 必做/选做 |
| `summary` | str | ✅ | 实验内容简介 |
| `method_theory` | str | ✅ | 实验方法与原理 |
| `objectives` | str | ✅ | 实验目的 |
| `equipment` | str | ✅ | 实验设备与环境 |
| `requirements` | str | ✅ | 实验要求 |
| `methods` | str | ✅ | 实验整体方法步骤概述 |
| `conclusions` | str | ✅ | 实验结论要求 |
| `steps` | list[Step] | ✅ | 步骤级详细指导与报告占位符 |
| `analysis_prompts` | list[str] | ✅ | 实验报告"五、实验分析"的引导语 |
| `grading_rubric` | list[Criterion] | ✅ | 实验报告"六、成绩评定"的教师打分表 |

### Step 对象

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | str | 步骤编号（如 `S1`），在指导书和报告中共享，实现一一映射 |
| `name` | str | 步骤标题 |
| `guide_text` | list[str] | 仅出现在《实验指导书》中的详细操作要点 |
| `report_prompt` | list[ReportItem] | 仅出现在《实验报告》"四、实验内容"中的图文占位符 |

### ReportItem 对象

为强制"图文穿插"，每条 report_prompt 必须用 `type` 字段标明该占位位置需要学生填写的是文字还是图片：

| 字段 | 类型 | 说明 |
|---|---|---|
| `type` | enum | `text` (文字填写区) 或 `image` (截图粘贴区) |
| `prompt` | str | 引导文字，如 `"请描述你选择该数据集的原因"` |

### Criterion 对象 (评分维度)

| 字段 | 类型 | 说明 |
|---|---|---|
| `dimension` | str | 考核维度名称 |
| `points` | int | 满分 |
| `standard` | str | 评分标准说明 |

---

## 二、 双轨文档章节映射

### 实验指导书（5 个环节）

| 环节 | 数据来源 |
|---|---|
| 一、实验目的 | `exp_X.yaml → objectives` |
| 二、实验设备与环境 | `exp_X.yaml → equipment` |
| 三、实验要求 | `exp_X.yaml → requirements` |
| 四、实验步骤与要点 | `exp_X.yaml → steps[].guide_text` |
| 五、实验结论 | `exp_X.yaml → conclusions` |

### 实验报告（6 个环节）

| 环节 | 数据来源 | 填写者 |
|---|---|---|
| 一、实验目的 | `exp_X.yaml → objectives` | 预填（教师） |
| 二、实验设备与环境 | `exp_X.yaml → equipment` | 预填（教师） |
| 三、实验要求 | `exp_X.yaml → requirements` | 预填（教师） |
| **四、实验内容（步骤）** | `exp_X.yaml → steps[].report_prompt` | **学生填写（图文穿插）** |
| **五、实验分析** | `exp_X.yaml → analysis_prompts` | **学生填写** |
| **六、成绩评定** | `exp_X.yaml → grading_rubric` | **教师填写** |

---

## 三、 禁止行为

- ❌ 在文件之间分散存放同一实验的数据（禁止恢复已被废弃的双轨制）。
- ❌ `report_prompt` 中连续出现多个 `type: image` 而无 `type: text` 间隔（违反图文穿插原则）。

---

## 四、 示例

```yaml
# exp_1.yaml — 全量单一事实源
exp_id: 1
name: "数据源探索与导入"
type: "设计性"
hours: 2
group_size: 1
requirement: "必做"
summary: "本实验指导学生..."
method_theory: "通过 Kaggle..."
objectives: "掌握数据获取..."
equipment: "个人计算机，网络连接..."
requirements: "独立完成，严禁抄袭..."
methods: "1. 注册账号 2. 搜索并下载 3. 读取数据"
conclusions: "反思数据质量对分析的影响。"

steps:
  - id: "S1"
    name: "定位并引入数据源"
    guide_text:
      - "前往 Kaggle (kaggle.com) 搜索相关主题数据集。"
      - "使用 `pandas.read_csv()` 读取数据。"
    report_prompt:
      - type: text
        prompt: "请写明你选择的数据集名称、来源及业务背景"
      - type: image
        prompt: "请粘贴成功读取数据后的 head() 或 info() 运行截图"

analysis_prompts:
  - "[请总结本次实验中你的数据清洗策略及其效果]"

grading_rubric:
  - dimension: "数据源选择与引入"
    points: 20
    standard: "数据集具有业务价值，成功导入并宏观描述了数据结构。"
```
