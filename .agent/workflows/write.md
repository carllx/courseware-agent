---
description: 为指定课程的教学单元撰写逐字稿
---

# /write 工作流 (通用版)

> **输入**: 课程名 + 教学单元 ID（如 `交互产品开发 W01`）
> **输出**: `<课程>/weeks/<单元ID>_<名称>/package.yaml` 及源文件

## 三阶段架构

`/write` 工作流分为三个阶段文件，**依次加载执行**：

| 阶段 | 文件 | 内容 | 门控 |
|:---|:---|:---|:---|
| **Phase 1: 备料** | [`write_phase1_prep.md`](write_phase1_prep.md) | Step 0-2.8：环境预检 → 预算声明 → 课程定位 → 上下文加载 → 知识扫描 → 教材审查 → 深度调研 → 素材预算表 | 素材覆盖率 ≥ 70% 方可进入 Phase 2（参见 `rule_content_depth.md` §1.2） |
| **Phase 2: 写作** | [`write_phase2_compose.md`](write_phase2_compose.md) | Step 3：Phase A/B/C 分段写作闭环 + 素材补充 + 上下文管理 | 逻辑自检通过方可标记 done（参见 `rule_content_depth.md` §2-3） |
| **Phase 3: 校验** | [`write_phase3_verify.md`](write_phase3_verify.md) | Step 3.5-6：大纲对齐 → 时长自检 → 知识面覆盖 → 收尾 | 全部通过方可进入 `/audit` |

## 全局约束

> [!CAUTION]
> **Frontmatter 边界 (ADR 007)**：写作过程中严禁在 frontmatter 中添加教案索引字段（`supported_objectives`/`task`/`steps`）。这些字段的 SSOT 在 `course.yaml`，非脚本的职责范围。Frontmatter 仅含：`week`/`topic`/`title`/`hours`/`objectives`/`created`/`status`。

## 加载规则

Agent 按需加载规则，**不得**在任务开始时一次性加载全部：

| 阶段 | 加载的规则和技能 |
|:---|:---|
| Phase 1（知识检索） | `rule_content_depth.md`、`librarian`、`narrative_archaeologist` |
| Phase 2（写作） | `script_format`、`rule_narrative_standards.md`、`rule_localization.md`、`rule_content_depth.md` |
| Phase 3（校验） | `rule_outline_alignment.md`、`real_asset_scanner` |

> [!IMPORTANT]
> **字数达标最佳实践**：参见 `rule_content_depth.md` §2 —— Phase A→中间检查点→Phase B 是字数达标的核心机制。
