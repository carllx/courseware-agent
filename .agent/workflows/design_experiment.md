---
description: 为课程的大型正式实验自动生成双轨文档（指导书与报告模板）
---

# /design_experiment 工作流

> **输入**: 课程名 + 实验编号 (如 `信息可视化 --exp 1`)
> **输出**: `<课程>/practices/experiments/Output/` 下的实验指导书与实验报告模板。
> **设计原则**: 合并读取 `course.yaml` (上游 SSOT) 与 `exp_X.yaml` (增量数据)，遵守 SSOT 职责边界。

## 前置条件

- `<课程>/course.yaml` 已配置 `experiments[]` 字段（含 objectives/equipment/requirements/methods/conclusions）
- `<课程>/practices/experiments/exp_<编号>.yaml` 已创建（遵循 `.agent/templates/experiment_doc_schema.md` 增量规范）
- `practices/experiment_planning.md` 已存在（作为实验细则参考）

## 步骤

### Step 0: 读取 course.yaml 实验元数据

从 `course.yaml → experiments[]` 提取目标实验的 SSOT 字段：
- `id`, `name`, `type`, `hours`, `group_size`, `requirement`
- `objectives`, `equipment`, `requirements`, `methods`, `conclusions`, `questions`

> 本工作流属于"教务生成器"类别（参见 `rule_document_boundaries.md` §4），允许读取 `course.yaml` 全量。

### Step 1: 校验增量 YAML

验证 `exp_X.yaml` 的合规性：
1. `exp_id` 必须存在于 `course.yaml.experiments[].id`
2. 不得包含 `purpose`/`environment`/`requirements`/`conclusions` 等已在 `course.yaml` 中定义的字段（`rule_document_boundaries.md` §6.5）
3. 每个 step 的 `report_prompt` 不得连续出现多个 `type: image` 而无 `type: text` 间隔

### Step 2: 生成双轨文档

调用 Python 引擎合并两个数据源并输出文档：

```bash
/opt/anaconda3/envs/mybase/bin/python .agent/scripts/generate_exp_docs.py \
  --course_dir "<课程>" --exp <实验编号>
```

### Step 3: 验证输出

验证 `practices/experiments/Output/` 下是否成功生成：
1. `Exp_<编号>_<名称>_实验指导书.md` — 含 5 个环节（目的→设备→要求→步骤与要点→结论）
2. `Exp_<编号>_<名称>_实验报告_学生模板.md` — 含 6 个环节（目的→设备→要求→**实验内容**→**实验分析**→**成绩评定**）

交叉校验：
- 指导书"四、步骤与要点"的步骤 ID 与报告"四、实验内容"的步骤 ID 一一对应
- 报告前三节（目的/设备/要求）的内容与 `course.yaml` 完全一致

### Step 4: 通知用户

```
✅ 实验 <编号> 文档生成完毕（合并 course.yaml + exp_X.yaml）！
指导书与报告模板已保存至 practices/experiments/Output/ 目录。
后续可将这两个 Markdown 文档传递至教务材料项目，通过 Pandoc 或 04_Experiment_Generator 转换为正式 Docx。
```

## 加载规则

| 步骤 | 加载的规则 |
|:---|:---|
| Step 0-1 | `rule_document_boundaries.md` §4 (实验外键关联) + §6.5 (禁止重复定义) |

## 与现有工作流集成

> [!IMPORTANT]
> `/design_experiment` 是实验教务文档生成的**独立链路**，与平时周次练习的 `/design_practice` **互不干涉**。
> - `/design_practice` → 生成每周的 `practice.yaml` + `practice_guide.md`（平时练习）
> - `/design_experiment` → 生成正式实验的 `指导书.md` + `报告模板.md`（教务归档）

- `/audit_deep` Part H 可增加对 `exp_X.yaml` 与 `course.yaml` 一致性的校验
- 最终的教务 Docx 生成由 `教务材料/04_Experiment_Generator` 负责，本工作流仅输出 Markdown 骨架
