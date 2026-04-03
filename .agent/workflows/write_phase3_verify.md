---
description: "/write Phase 3 — 校验（Alignment + Length + Coverage）"
---

# Phase 3: 校验 (Verification)

> **前置**：Phase 2 写作已完成（所有模块 Phase A/B/C 闭环通过）。

### Step 3.5: 大纲对齐检查表 (Outline Alignment Checklist)

> **强制执行**：所有模块写完后、时长自检前，必须逐项核对以下清单。任何一项未通过则**禁止进入 Step 4**。
> **引用检查表**: `.agent/rules/rule_outline_alignment.md`（O1-O10）

逐项执行 `rule_outline_alignment.md` 中定义的 **O1-O10** 检查（O8 为 `/write` 专用的 `teaching_requirements` 覆盖检查，O9 为模块字数预算达标检查，O10 为人文标签密度检查）。

### Step 4: 时长自检（必须执行，不得跳过）

从**课程目录**下运行时长验证器（注意路径为相对课程目录的上级 `.agent`）：

```bash
# 从 Workspace 根目录运行：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程名>"
```

**时长门限（硬性约束）**：

| 检查项 | 标准 | 不合格处理 |
|:---|:---|:---|
| 预估总时长 ≥ 课程计划时长 x 80% | 如 5 小时课 → 预估需 ≥ 240 分钟 | **禁止提交，必须回到 Step 3 补充** |
| ACTIVITY 总时长 > 0 | `lecture`/`workshop` 模式强制要求 | 补充 `[ACTIVITY]` 块后重新验证 |
| **模块字数 ≥ 预算的 100%** | 逐字稿宁多勿缺，任何模块不得低于自声明预算 | **禁止提交，回到 Step 3 执行 DRP** |
| 模块字数 < 预算的 80% | 严重不足红线 | **禁止提交，强制 DRP-L1→L2→L3** |

> **ℹ️ 分片架构提示**：验证器现在支持 `--file` 参数直传文件路径。对 `weeks/` 架构，`--course` 模式会自动编译分片脚本并使用 `_compiled.md`。

> **⚠️ 理论+实践混合模式**：当 `course.yaml` 中同时定义了 `hours_theory` 和 `hours_practice` 时，验证逻辑应为“讲授时长 + 活动时长 ≈ 计划总课时”，而非纯用 80% 塞进公式。典型的 4 课时“理论 2h + 实践 2h”单元，预估总时长在 150-200 分钟即合格。

**模块级预算对标**（**强制执行**，不可跳过）：

```bash
# 从 Workspace 根目录运行：
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程名>" --module-breakdown
```

### Step 5: 知识面覆盖率检查

```bash
# 检查标签分布（兼容分片架构：搜索 src/ 和 _compiled.md）
echo "=== 知识标签分布 ==="
# 分片架构
grep -roP '> \[([A-Z ]+?)(?::.*?)?\]' "<课程>/weeks/"*"/src/" 2>/dev/null | sort | uniq -c | sort -rn
# 或使用编译产物
grep -oP '> \[([A-Z ]+?)(?::.*?)?\]' "<课程>/weeks/"*/".build/compiled.md" 2>/dev/null | sort | uniq -c | sort -rn

echo "=== VISUAL 块完整性 ==="
grep -rc '> \[VISUAL\]' "<课程>/weeks/"*"/src/" 2>/dev/null || \
grep -c '> \[VISUAL\]' "<课程>/weeks/"*/".build/compiled.md" 2>/dev/null

echo "=== 知识节点标签一致性 ==="
# 提取脚本中的知识节点标签，检查是否在 Hub 中存在
grep -roP '\*\*知识节点\*\*: `([^`]+)`' "<课程>/weeks/" 2>/dev/null | \
  sed 's/.*`\(.*\)`.*/\1/' | while read tag; do
    if grep -q "$tag" "<课程>/knowledge/knowledge_hub.yaml"; then
      echo "✅ $tag"
    else
      echo "❌ $tag — 未在 Hub 中找到，请检查或新建条目"
    fi
  done
```

### Step 6: 收尾 (Epilogue)

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）+ E2（ADR 检查）+ E3（链接验证）。
