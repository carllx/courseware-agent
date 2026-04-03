---
trigger: model_decision
description: 当修改 course.yaml 的 objectives.mappings 或新增课程时，必须校验观测点命名与人培支撑矩阵的合规性。
---

# 规则：人培合规性约束 (Training Plan Compliance)

**依据**：教务材料项目 `training_plan_2025.yaml` + `graduation_requirements.yaml`

## 1. 观测点命名约束

- `objectives.mappings[].point` 命名**必须**与 [`graduation_requirements.yaml`](file:///Users/yamlam/Downloads/教务材料/00_Data_Context/graduation_requirements.yaml) 中的编号精确一致
- **禁止**自创观测点名称或编号
- 格式示例：`2.2 跨学科知识整合`（编号 + 中文名）

## 2. 支撑矩阵覆盖约束

- 人培 [`training_plan_2025.yaml`](file:///Users/yamlam/Downloads/教务材料/00_Data_Context/training_plan_2025.yaml) 的 `course_matrix.support_map` 中标注的所有观测点，在 `course.yaml` 中**必须**至少有一条 `objectives.mappings` 映射
- 额外扩展的观测点（超出人培矩阵的）允许存在，但应在 `course.yaml` 顶部注释块中说明理由

## 3. 学分/学时差异标注

- 实际开课设置（`course.credits` / `course.hours`）与人培方案不一致时，**必须**在 `course.yaml` 顶部人培参考注释块中注明差异来源
- 格式参考（已在两门课程中实践）：
  ```yaml
  # 人培学分/学时:  3学分 / 60学时 (理20+实40)
  # 实际开课设置:   2学分 / 40学时 (理20+实20), 以实际排课为准
  ```

## 4. OBE 行为动词合规

- `objectives.desc` **禁用动词**：了解 / 熟悉 / 理解 / 掌握
- 推荐替换为 Bloom 分类法可测量动词：列举 / 解释 / 分析 / 应用 / 评价 / 创建 / 描述 / 执行 / 演示
- 此规则**仅限** `objectives.desc` 字段，`teaching_requirements`、`lessons.objectives` 等其他字段不受此限

## 5. 验证方法

```bash
cd /Users/yamlam/Downloads/教务材料
/opt/anaconda3/envs/mybase/bin/python scripts/audit_course_data.py \
  --root "/Users/yamlam/Downloads/2025-2026-2 课程"
```
