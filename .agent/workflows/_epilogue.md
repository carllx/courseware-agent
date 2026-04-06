---
description: 工作流共享收尾协议（Post-Hook）。任何主要工作流完成后引用此文件执行收尾。
---

# Epilogue（共享收尾协议）

> **引用方**：`/write`、`/audit`、`/generate_assets`、`/ppt`、`/export`、`/publish`、`/build`、`/deploy_netlify`
> **定位**：放置在工作流最后一个 Step 之后。

## E1: 更新 briefing.md

读取 `.agent/briefing.md`，更新以下两个区块：

1. **当前状态**：更新涉及课程的进度信息（脚本状态、知识库、视觉资产等）
2. **最近活动**：在活动表格顶部追加一行，记录今日执行的工作流及成果

> [!IMPORTANT]
> 仅更新与本次执行**直接相关**的课程行。不修改其他课程的状态。

## E2: ADR 检查（可选）

如果本次执行过程中产生了新的架构决策（符合 `rule_meta_learning.md` 触发条件），则：
1. 追加 `ADR.md` 完整记录
2. 追加 `ADR_summary.md` 一行摘要

## E3: 链接验证（仅 /write 和 /generate_assets）

> **条件**：当本次工作流为 `/write` 时，仅当 Phase 3 Step 4 时长自检全部通过（exit code 0）后才执行 E3。
> 若 Step 4 未通过，跳过 E3，避免 Agent 被视觉断链分散注意力。

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_visuals.py \
  --course "<课程名>"
```

若存在断链，在报告中附注。
