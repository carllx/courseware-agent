# 课程大实验 — 增量文档规范 (Experiment Increment Schema)

> **上游 SSOT (Single Source of Truth)**：
> - `course.yaml → experiments[]` — 实验元数据的最高权威（id/name/type/hours/objectives/equipment/requirements/methods/conclusions/questions）
> - `practices/experiment_planning.md` — 实验细则（目标/工具/交付物/周次等）
>
> **本文件职责**：
> 定义 `practices/experiments/exp_X.yaml` 的**增量字段**规范。
> 这些字段**仅包含 `course.yaml` 中不存在的**教学细节数据——步骤指导文本、报告占位符、分析引导语和评分表。
>
> **存放路径**：`<课程>/practices/experiments/exp_X.yaml`
> **工具链**：由 `/design_experiment` 工作流及 `.agent/scripts/generate_exp_docs.py` 驱动。
> **生成机制**：脚本运行时**合并读取** `course.yaml` (上游) + `exp_X.yaml` (增量)，输出双轨文档。
>
> **合规约束**：
> - 遵守 `rule_document_boundaries.md` §4（实验外键关联规范）和 §6.5（禁止在 practices/ 重复 course.yaml 已有字段）
> - 实验类型枚举必须使用含"性"后缀的值：`验证性`/`综合性`/`设计性`/`演示性`（ADR 011）

---

## 一、 增量 YAML 结构

`exp_X.yaml` 仅包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `exp_id` | int | ✅ | 实验编号，**必须匹配** `course.yaml.experiments[].id` |
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
| 一、实验目的 | `course.yaml → experiments[id].objectives` |
| 二、实验设备与环境 | `course.yaml → experiments[id].equipment` |
| 三、实验要求 | `course.yaml → experiments[id].requirements` |
| 四、实验步骤与要点 | `exp_X.yaml → steps[].guide_text` |
| 五、实验结论 | `course.yaml → experiments[id].conclusions` |

### 实验报告（6 个环节）

| 环节 | 数据来源 | 填写者 |
|---|---|---|
| 一、实验目的 | `course.yaml → experiments[id].objectives` | 预填（教师） |
| 二、实验设备与环境 | `course.yaml → experiments[id].equipment` | 预填（教师） |
| 三、实验要求 | `course.yaml → experiments[id].requirements` | 预填（教师） |
| **四、实验内容（步骤）** | `exp_X.yaml → steps[].report_prompt` | **学生填写（图文穿插）** |
| **五、实验分析** | `exp_X.yaml → analysis_prompts` | **学生填写** |
| **六、成绩评定** | `exp_X.yaml → grading_rubric` | **教师填写** |

---

## 三、 禁止行为

- ❌ 在 `exp_X.yaml` 中定义 `purpose`/`environment`/`requirements`/`conclusions` 等已在 `course.yaml` 中存在的字段
- ❌ `exp_id` 不匹配 `course.yaml.experiments[].id`
- ❌ `report_prompt` 中连续出现多个 `type: image` 而无 `type: text` 间隔（违反图文穿插原则）

---

## 四、 示例

```yaml
# exp_1.yaml — 仅增量数据，元数据从 course.yaml 读取
exp_id: 1

steps:
  - id: "S1"
    name: "定位并引入数据源"
    guide_text:
      - "前往 Kaggle (kaggle.com) 搜索相关主题数据集。"
      - "使用 `pandas.read_csv()` 或 `read_json()` 读取数据。"
    report_prompt:
      - type: text
        prompt: "请写明你选择的数据集名称、来源及业务背景"
      - type: image
        prompt: "请粘贴成功读取数据后的 head() 或 info() 运行截图"

analysis_prompts:
  - "[请总结本次实验中你的数据清洗策略及其效果]"
  - "[请反思在数据处理过程中遇到的主要困难和解决方案]"

grading_rubric:
  - dimension: "数据源选择与引入"
    points: 20
    standard: "数据集具有业务价值，成功导入并宏观描述了数据结构。"
```
