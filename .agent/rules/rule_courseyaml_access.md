---
trigger: glob
description: 当 Agent 试图直接打开 course.yaml 时，提醒使用 extract_week.py 提取局部数据以节省 Token。
globs:
  - "**/course.yaml"
---

# 规则：course.yaml 访问约束 (Course YAML Access Guard)

> **核心原则 (ADR 043 R-6)**：course.yaml 体积 ~51KB / ~19.6K tokens。日常工作流**禁止**直接加载全文。

## §1 禁止直接读取的工作流

以下工作流在执行过程中**必须**通过 `<课程>/extract_week.py --week N` 提取局部数据（~2-5KB），**不得**直接 `view_file` course.yaml 全文：

- `/write`（Phase 1/2/3 全部阶段）
- `/audit`（Quick / Standard 级别）
- `/design_practice`
- `/generate_assets`
- `/ppt`

## §2 允许全量读取的场景

仅以下低频场景允许加载 course.yaml 全文：

- `/audit --deep` Part F（`audit_courseyaml.md` 跨周引用校验）
- 教务生成器（`gen_*.py`、`audit_course_data.py`）
- `/new_course`（初始化阶段需读取模板）
- 用户明确要求全量查阅

## §3 提取器可用模式

```bash
# 基础模式：提取单周 calendar + objectives + meta
python <课程>/extract_week.py --week N

# 扩展模式（ADR 043）
python <课程>/extract_week.py --week N --include-concepts
python <课程>/extract_week.py --week N --section experiments
python <课程>/extract_week.py --week N --section practice-context
```

## ❌ 禁止行为

- ❌ 日常工作流中直接 `view_file <课程>/course.yaml`（~19.6K tokens 浪费）
- ❌ 在不确定是否需要全量时默认加载全文（应先尝试提取器）
