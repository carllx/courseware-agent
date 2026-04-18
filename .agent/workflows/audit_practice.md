---
description: Standard 级别检查 — Part P (Practice 冒烟检查)。仅在目标周次存在 practice.yaml 时加载。
---

# Part P: Practice 冒烟检查 (Practice Smoke Test)

> **目的**：在日常 Standard 审计中捕获 practice.yaml 的 SSOT 违规回归，无需加载 `/audit_deep` Part H 全量。
> **加载条件**：当目标周次存在 `practice.yaml`（`weeks/W0X_.../practice.yaml`）时执行。
> **ADR 参考**：ADR 043 R-10

## 自动化校验（推荐）

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_practice.py \
  --course "<课程>" --week <周次数字>
```

> [!TIP]
> `validate_practice.py` 已覆盖以下全部检查项，输出结构化报告。仅当脚本不可用时才回退到手动 grep。

## 手动检查（回退方案）

```bash
PRACTICE_FILE="<课程>/weeks/<周次>/practice.yaml"
if [ -f "$PRACTICE_FILE" ]; then
  echo "=== P1: SSOT 越界检查 (H9) ==="
  grep -n "weight:\|scoring_rubric" "$PRACTICE_FILE" && echo "❌ [SSOT_VIOLATION]" || echo "✅ 无违规字段"

  echo "=== P2: experiment_link 类型检查 (H10) ==="
  grep -n "experiment_link:" "$PRACTICE_FILE"
  # 期望：list 格式 [N] 或 [N, M]，非字符串

  echo "=== P3: theory_link 格式检查 ==="
  grep -n "theory_link:" "$PRACTICE_FILE"
  # 期望：结构化对象格式（下一行为 concept_id），非纯字符串
fi
```

## 检查项与严重度

| # | 检查项 | 标准 | 不合格标记 |
|---|---|---|---|
| P1 | `weight` / `scoring_rubric` 不存在 | Phase/Homework 中无此字段 | `[SSOT_VIOLATION]` 🔴 |
| P2 | `experiment_link` 为 `list[int]` | 非字符串格式 | `[EXP_LINK_LEGACY]` 🔴 |
| P3 | `theory_link` 为结构化对象 | 含 `concept_id` 子字段 | `[CA_LEGACY_FORMAT]` 🟡 |

> 任何 P1/P2 🔴 项 → **Needs Revision**，建议重新执行 `/design_practice` 修复。
