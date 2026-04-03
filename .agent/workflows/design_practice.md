---
description: 为指定课程的教学单元设计/编辑实践步骤规格
---

# /design_practice 工作流

> **输入**: 课程名 + 周次（如 `信息可视化 W02`）
> **输出**: `<课程>/practices/W0X_practice.yaml`

## 前置条件

- `course.yaml` 已配置完毕
- `practices/experiment_planning.md` 已存在（如含实验关联）

## 步骤

### Step 1: 读取 course.yaml 上下文

从 `course.yaml → calendar[week]` 提取：
- `hours_practice` → 计算 `total_minutes = hours_practice × 45`
- `exp_id` → 定位关联实验
- `lessons[].steps` → 获取教案步骤概览
- `task` → 获取课后作业描述
- `teaching_requirements` → 理论知识前置要求

### Step 2: 读取实验规划

从 `practices/experiment_planning.md` 定位对应实验的内容与工具链约束。

### Step 2.5: UbD 逆向设计（先交付物后活动）

> 借鉴 Wiggins/McTighe Understanding by Design 三阶段倒推法：
> ① 确定期望结果 → ② 确定可接受证据 → ③ 规划学习体验

1. **锁定交付物**：从 `course.yaml → calendar[week].task` 和 `experiment_planning.md`
   提取本周学生最终需要提交的交付物清单
2. **逆推活动**：为每个交付物标注"学生需要经历什么步骤才能产出此交付物"，
   据此设计 `phases[]` 的顺序和内容
3. **绑定理论**：为每个 phase 填写 `theory_link`，确保每个活动都有理论支撑
   - 使用 `course.yaml.concept_registry[].id` 作为 `theory_link.concept_id`
   - 使用 `course.yaml.supported_objectives[]` 作为 `theory_link.course_objective`
   - `type ∈ {workshop, practice, critique}` 的 phase **必须** 填写 `theory_link`

### Step 3: 读取已有脚本（如存在）

如该周脚本已完成（`scripts/W0X_*.md`），提取其中 `[ACTIVITY]` 块：
- 活动类型、时长、描述、工具
- 作为 practice YAML 的参考依据

### Step 4: 生成/编辑 practice YAML

创建或编辑 `practices/W0X_practice.yaml`：
- 遵循 `_schema.md` 定义的结构规范
- **人工审阅**：具体步骤分解需用户确认
- **自动校验**：时间合计、工具链、AI 边界

### Step 4.5: 素材清单生成

根据每个 phase 的 `type` 推断所需素材类型，生成 `materials` 块：
- `warmup` → 检查是否需要 `poll` 或 `comparison` 素材
- `practice` → 检查是否需要 `quiz` 或 `tutorial_steps` 素材
- `critique` → 检查是否需要 `critique_card` 素材
- `workshop` → 检查是否需要 `tutorial_steps`、`dataset` 或 `code_template` 素材
- `discussion` / `demo` → 检查是否需要 `case_study` 或 `comparison` 素材

创建对应的 `<课程>/practices/materials/W0X/` 目录脚手架。
素材文件本身（图片/数据）的实际生成需通过 `generate_image` 或手动放置完成。

### Step 5: 运行 rule_practice_design 校验

- `sum(phases[].minutes)` = `total_minutes`
- `total_minutes` = `course.yaml.hours_practice × 45`
- `experiment_link` 与 `exp_id` 正确映射
- `ai_allowed` 与 AI 递进曲线一致
- 所有必填字段存在
- `homework.weight` 必填，`homework.deliverables` 非空
- **theory_link 条件必填**（规则 11）
- **theory_link 引用完整性**（规则 12）
- **upstream_dependencies 一致性**（规则 13）

### Step 5.5: 强制生成 Practice Guide

根据 `_schema.md` 的终极闭环产出要求，生成或更新 `practices/W0X_Practice_Guide.md`：
- 从 YAML 中提取 phases/materials/homework 结构
- 渲染为面向学生的图文并茂的 Markdown 操作手册
- 素材图片使用相对路径引用 `materials/W0X/`

### Step 6: 通知用户

```
✅ W0X 实践步骤设计已完成。
请检查 practices/W0X_practice.yaml 的步骤分解和时间分配。
```

## 加载规则

| 步骤 | 加载的规则 |
|:---|:---|
| Step 4-5 | `rule_practice_standards.md` |

## 与现有工作流集成

> [!IMPORTANT]
> `/design_practice` 是脚本生命周期管道的**条件必经节点**（当该周 `hours_practice > 0` 时）。
> 在 `/write` 之前执行，确保理论-实践的 CA 三角完整性。

- `/write` Phase 1 Step 2.1c 加载 `practices/W0X_practice.yaml` 作为实践模块写作输入
- `/audit_deep` Part H 检查 practice YAML 与 script `[ACTIVITY]` 块的一致性
- `/audit_deep` Part H6-H8 检查 theory_link 覆盖率、upstream DAG、Guide 生成状态
