# 项目简报 (Agent Briefing)

> **更新时机**：每次对话结束前，Agent 通过 `rule_meta_learning.md` 触发更新本文件。
> **用途**：新 Agent 进入对话时首先阅读，快速获取项目动态全貌。

---

## 当前状态（最近更新：2026-04-06）

### Agent 架构与基建 (V5 Architecture)
- **V5 架构迁移**：完成了全域 Package 化，重构了 `src/` 与 `public/` 的解耦，修正了关联 PPT/H5 build script 下游构建引擎。
- **架构大瘦身**：清理大量过度拟合的规则堆叠。将原字数打底相关规则整合为统一的 `rule_content_depth.md`。将 `rule_narrative_standards.md` 与 `rule_knowledge_protocol.md (已移除)` 降级剥离到技能参考 (`skills/*/references`) 中，减少 50% 以上触发负载。
- **H5 Craft-room**：完成 Phase 0-3 实时审计系统。H5 从"只读预览器"升级为"实时创作工作台"，含 P0 渲染管线（~300ms）+ P1 验证管线（~2s 异步），DurationGauge/HealthDot/ValidationOverlay/AnnotationOverlay 4 大组件 + ValidationContext 心流保护。
- **发布架构 (Deployment)**：重构了产物交付管线，全面解耦 `/build`（SSG构建）与 `/deploy_netlify`（CDN 投递），并提供 `/publish` 一键发版编排，实施双层安全网拦截 `dist/` 与 Site ID 的配置泄漏。

### 交互产品开发
- **脚本**：W01-W14 全量完成。近期 W01 M03、M04 等通过 DRP 扩写与去 AI 语感（反退化 4-gram 循环）深度重写，达到 95% 充实率的优异预算对标，整体打通 Phase 3；W11、W13、W14 均已通过 DRP 扩写验证与 Standard 审计。历史骨架全部上线。
- **配置**：全面迁移到含 `package.yaml` 的新标准。
- **视觉资产**：已跑通全量视觉组装与回链渲染。W01 M01 与 M02 遗漏的 7 张视觉锚点通过双轨制生成（4张从基站获取历史原片，3张严格依托 `theme_academic_minimal` 的 AI 概念资产重建）填补完成，且已通过底层链路完整性验证。

### 信息可视化
- **脚本**：W01-W08 设计模块已大量重构。W01 M03 通过 DRP 赤字修复协议完成重度人文扩写。W01 M00 课程导览模块执行了 Standard 等级审计，并于本周完成了全量 Repair 修复（包括声画对齐、TTS 吞音根除及 8 张大纲图卡的 AI 视觉补充）。W01_Practice_Guide 完成内卷化业务模拟剧本更新。W04和W07 通过视觉渲染及合规性验证。W06 通过审计完成结构扩展（Level-2/Level-3）与视觉规范对齐。
- **V5 迁移**：**仅 W01/W02 已完成模块化**（`package.yaml` + `src/M0X_*.md`），W03-W08 仍为旧架构单体脚本。
- **配置**：`W01_practice.yaml` 对齐完成。
- **视觉资产**：W01 通过 `/generate_assets` 完成 Kandinsky+Dada 风格补缺及 M00 缺失的 8 张大纲图卡生成封装，视觉断链全部修复闭环。
- **知识库**：开始筹建，尚未饱和。

### 实习指导
- **状态**：活跃中，project 类型课程

---

## 最近活动（近 7 天）

| 日期 | 事件 |
|:-----|:-----|
| 2026-04-06 | 执行 `/publish` 一键发布编排工作流。完成 H5 引擎构建、新增图文产物转换，同时将本地代码同步至 GitHub 并成功部署 `dist/` 产物至 Netlify 生产环境。 |
| 2026-04-06 | 执行 `/generate_assets` 扫尾。完成信息可视化 W01 M00 模块的 `Repair Plan`，彻底解决图文隐喻错位与 TTS 双语词吞音漏洞，并依据 `theme_constructivist_dada` 约束规则针对 8 张空置的大纲幻灯片进行几何矢量生成补全，验证落地闭环。 |
| 2026-04-06 | 针对信息可视化课程 W01 `M00_课程导览.md` 开展了 Standard 级别审计；提交了全模块审查缺陷报告，成功拦截了开头 3 处可能导致课堂翻车体验的“声画严重错位”，并标记出 TTS 把“Vibe Coding（直觉编程）”的核心中文吞噬的事故倾向。 |
| 2026-04-04 | 执行 `/generate_assets` 扫尾。针对交互产品开发 W01 空白视觉链开展抓补——双轨制填入了 4 张考证严谨的交互历史底图（Engelbart/Compass）和 3 张严格遵循学术极简系统的 AI 概念图。消除 W01 全周断链盲区。 |
| 2026-04-04 | 完成交互产品开发 W01 连杀：深度扩写 M02~04 并成功执行反退化 (Anti-Degeneration) 清洗，消除 4-gram 循环及极端修饰语词汇，以 95% 的预算填充率通过了最严厉的 Phase 3 字数与结构联合审查。 |
| 2026-04-03 | H5 Craft-room Phase 0-3 全量落地。后端注入精确字数（V1）、ValidationContext 心流保护（V2）、VSCode 直跳（V3）、段落指纹批注层（V4）。新增 validate_runner.py 统一验证管线 + Vite P1 异步推送。 |
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
- **H5 实时审计**：双管线架构（P0 渲染 + P1 异步验证），validate_runner.py 统一入口 + Q3 门控 + 心流保护期（ADR 036）

---

## 活跃邮箱消息

> 执行 `/mailbox_in` 获取最新待办。当前 `active/` 为空。

---

## 待办事项（未分配）

- [x] W01-14 全量脚本撰写（交互产品开发）
- [ ] 交互产品开放的全面最终交付物出包
- [ ] 信息可视化 剩余 W09-W14 脚本结构构建及审计
- [ ] 知识库持续扩充及 Hub 体积治理
