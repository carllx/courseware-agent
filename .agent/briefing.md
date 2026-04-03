# 项目简报 (Agent Briefing)

> **更新时机**：每次对话结束前，Agent 通过 `rule_meta_learning.md` 触发更新本文件。
> **用途**：新 Agent 进入对话时首先阅读，快速获取项目动态全貌。

---

## 当前状态（最近更新：2026-03-30）

### Agent 架构与基建 (V5 Architecture)
- **V5 架构迁移**：完成了全域 Package 化，重构了 `src/` 与 `public/` 的解耦，修正了关联 PPT/H5 build script 下游构建引擎。
- **架构大瘦身**：清理大量过度拟合的规则堆叠。将原字数打底相关规则整合为统一的 `rule_content_depth.md`。将 `rule_narrative_standards.md` 与 `rule_knowledge_protocol.md (已移除)` 降级剥离到技能参考 (`skills/*/references`) 中，减少 50% 以上触发负载。

### 交互产品开发
- **脚本**：W01-W14 全量完成。近期 W11、W13、W14 均已通过 DRP 扩写验证与 Standard 审计（完全闭环，视觉充填、TTS 脱盲）。历史骨架全部上线。
- **配置**：全面迁移到含 `package.yaml` 的新标准。
- **视觉资产**：已跑通全量视觉组装与回链渲染。

### 信息可视化
- **脚本**：W01-W08 设计模块已大量重构。W01 M03 通过 DRP 赤字修复协议完成重度人文扩写。W01_Practice_Guide 完成内卷化业务模拟剧本更新。W04和W07 通过视觉渲染及合规性验证。W06 通过审计完成结构扩展（Level-2/Level-3）与视觉规范对齐。
- **V5 迁移**：**仅 W01/W02 已完成模块化**（`package.yaml` + `src/M0X_*.md`），W03-W08 仍为旧架构单体脚本。
- **配置**：`W01_practice.yaml` 对齐完成。
- **视觉资产**：W01 通过 `/generate_assets` 完成 Kandinsky+Dada 风格的补缺渲染与替换配置。
- **知识库**：开始筹建，尚未饱和。

### 实习指导
- **状态**：活跃中，project 类型课程

---

## 最近活动（近 7 天）

| 日期 | 事件 |
|:-----|:-----|
| 2026-03-30 | 审计工作流 Token 浪费修复（ADR 035）。为 4 个验证脚本统一注入 `--week N` 过滤、`validate_project.py` 周次模式智能跳过全局验证器、`audit.md` 新增 Step 0 范围解析 + V5 模块级聚焦指令。审计单周节省 ~65% tokens。 |
| 2026-03-30 | 执行 `/generate_assets` 工作流。针对信息可视化 W01 M03 DRP 修复以及历史报告，按 `theme_constructivist_dada` 视觉系统生成了 8 张关键美术资产，并完成了落地测试。 |
| 2026-03-29 | Agent 架构深度瘦身 (Rule Consolidation)。整合冗余规则为 `rule_content_depth.md` 与 `rule_practice_standards.md`；将说明书级的叙事/知识库规则降归 `references/` 防止过度拟合加载。 |
| 2026-03-29 | 完成全量 V5 架构升级 (`package.yaml` + `src/` 解耦与隔离)。重构 delivery 为 engines、解决历史 glob 与相对路径依赖残留；解决长文本生成的 OOM OBA 问题与上下文预警瓶颈。 |
| 2026-03-29 | IDE Markdown 实时渲染与结构验证环境搭建；修复 V5 信息可视化及交互原型架构的断链警告；审查信息可视化历史内容遗留。 |
| 2026-03-28 | 彻底打通信息可视化 W01_Practice_Guide 业务剧本，验证 Anscombe 四家大厂逻辑；重建高保真图形。 |
| 2026-03-22 | 交互开发 W11/W13/W14 Standard 审计批量修复完毕并达成 Phase 3；信息可视化 W06/W04/W07 渲染及审计闭环，大面积生成及修复视觉资产。 |
| 2026-03-21 | 交互开发 W01-08 验证与修缮收尾。Rules Frontmatter 格式合规性深度审计发现并补丁。 |

---

## 关键架构决策（速查）

> 完整版见 `.agent/memory/ADR.md`，摘要见 `.agent/memory/ADR_summary.md`

- **脚本写作**：模块化分段（ADR 020）+ 知识饱和度四维评估（ADR 021）+ 案例密度门限（ADR 023）
- **数据管理**：消费者导向 SSOT（ADR 007）+ 学时必须整数（ADR 016）
- **跨项目**：严禁直接修改教务材料项目文件（ADR 015）
- **邮箱**：统一通用邮箱，身份自由声明
- **H5 课件**：脚本→slides.json→React SPA，Audio-first 联动（ADR 026）
- **Agent 机制**：audit 三层拆分、DRP/饱和度 SSOT 化、K-2 改模块预算（ADR 027）
- **审计过滤**：`/audit --week N` 统一过滤注入，周次/模块级审计节省 65-80% tokens（ADR 035）

---

## 活跃邮箱消息

> 执行 `/mailbox_in` 获取最新待办。当前 `active/` 为空。

---

## 待办事项（未分配）

- [x] W01-14 全量脚本撰写（交互产品开发）
- [ ] 交互产品开放的全面最终交付物出包
- [ ] 信息可视化 剩余 W09-W14 脚本结构构建及审计
- [ ] 知识库持续扩充及 Hub 体积治理
