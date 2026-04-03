---
trigger: glob
description: 大纲一致性检查表（共享规范，供 /write 和 /audit 引用）
globs:
  - "**/weeks/*/src/*.md"
---

# 大纲一致性检查表 (Outline Alignment Checklist)

> **引用方**：`/write` Phase 3 Step 3.5 · `/audit` Quick Q5 / Deep G4
> **SSOT**：本文件为唯一维护点，禁止在工作流中重复定义检查项。
> **数据获取**（ADR-021）：O1-O4/O8/O9 中引用的 `course.yaml` 数据，Quick/Standard 级别通过 `extract_week.py --week N` 按需提取；Deep 级别可加载全量。

## 检查项

| # | 检查项 | 说明 | 来源 | 严重度 |
|---|-------|------|------|:------:|
| O1 | **steps 结构覆盖** | 脚本 Module 结构必须与 `calendar[].lessons[].steps` 的每个 stage 一一对应。首周若含"复习" stage，需有课程导览模块 | `course.yaml` | 🔴 高 |
| O2 | **ideology 思政融入** | 脚本正文中必须包含至少一处与 `calendar[].ideology` 内容呼应的案例或注解（使用 `[CASE STUDY]` 或正文嵌入均可） | `course.yaml` | 🔴 高 |
| O3 | **task 课后任务布置** | 脚本小结或末尾段落中必须明确布置与 `calendar[].task` 一致的课后作业，包含交付物格式与提交要求 | `course.yaml` | 🟡 中 |
| O4 | **frontmatter ↔ lessons.objectives 同步** | 脚本 frontmatter `objectives` 必须与 `calendar[].lessons[].objectives` 逐条一致。若写作中优化了动词表述，必须同步更新 `course.yaml` | 双端 SSOT | 🟡 中 |
| O5 | **OBE 构建性对齐** | 验证 `supported_objectives` 中每个目标在脚本中有 目标→活动→评价 闭环 | OBE 框架 | 🟡 中 |
| O6 | **Bloom 动词** | 检查 frontmatter objectives 是否使用合理的 Bloom 可测量动词（豁免范围内为建议级） | OBE 框架 | 🟢 低 |
| O7 | **Bullet Sync 要点同步** | Speech 中每处结构化要点（≥3 并列项、阶段划分、考核规则、任务要求）必须在紧邻的 `[VISUAL]` 块中有 `**List**` 字段同步展示 | `script_format` §1.3 | 🟡 中 |
| O9 | **模块字数预算达标** | 每个 `##` 模块的讲授字数 ≥ **预算的 100%**（预算 = 模块自声明分钟 × 语速常量 180 字/分，扣除 ACTIVITY 占用）。80%-100% 为 ⚠️ 偏薄；<80% 为 ❌ 严重不足。验证：`validate_script_length.py --module-breakdown`。**兜底规则**：即使验证器全部 ✅，Agent 仍需手动抽检 ≥1 个模块的字数/预算比值；若全脚本预估时长 ÷ 课时预算 < 60%，强制触发手动全量复核 | `course.yaml` + ADR 020 | 🔴 高 |
| O10 | **人文标签密度** | 每个 `##` 讲授模块的口头型人文标签数 ≥ `⌈模块讲授字数预算 ÷ 2000⌉`（最低 1 个/模块）。口头型标签包括：`STORY TIME`/`CASE STUDY`/`LIFE CONNECT`/`PHILOSOPHY`/`DID YOU KNOW`/`TEACHING MOMENT`。验证：`validate_script_length.py --module-breakdown` 的「标签」列 | `script_format` §7 | 🔴 高 |

## 额外项（仅 /write 使用）

| # | 检查项 | 说明 | 来源 |
|---|-------|------|------|
| O8 | **teaching_requirements 覆盖** | 脚本教学活动必须覆盖 `calendar[].teaching_requirements` 中声明的 knowledge / ability / quality 全部维度 | `course.yaml` |

## 判定规则

- 任何 🔴 高严重度项未通过 → 报告结论为 **Needs Revision**
- 🟡 中严重度项累计 ≥ 3 项未通过 → 建议 **Needs Revision**
- 仅 🟢 低严重度项未通过 → **Pass with Notes**
