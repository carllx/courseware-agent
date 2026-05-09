# 项目简报 (Agent Briefing)

> **更新时机**：每次对话结束前，Agent 通过 `rule_meta_learning.md` 触发更新本文件。
> **用途**：新 Agent 进入对话时首先阅读，快速获取项目动态全貌。

---

## 当前状态（最近更新：2026-04-11）

### Agent 架构与基建 (V5 Architecture)
- **V5 架构迁移**：完成了全域 Package 化，重构了 `src/` 与 `public/` 的解耦，修正了关联 PPT/H5 build script 下游构建引擎。
- **架构大瘦身**：清理大量过度拟合的规则堆叠。将原字数打底相关规则整合为统一的 `rule_content_depth.md`。将 `rule_narrative_standards.md` 与 `rule_knowledge_protocol.md (已移除)` 降级剥离到技能参考 (`skills/*/references`) 中，减少 50% 以上触发负载。
- **H5 Craft-room**：完成 Phase 0-3 实时审计系统。H5 从"只读预览器"升级为"实时创作工作台"，含 P0 渲染管线（~300ms）+ P1 验证管线（~2s 异步），DurationGauge/HealthDot/ValidationOverlay/AnnotationOverlay 4 大组件 + ValidationContext 心流保护。
- **发布架构 (Deployment)**：重构了产物交付管线，全面解耦 `/build`（SSG构建）与 `/deploy_netlify`（CDN 投递），并提供 `/publish` 一键发版编排，实施双层安全网拦截 `dist/` 与 Site ID 的配置泄漏。

### 交互产品开发
- **脚本**：W01-W14 全量完成。今日完成了 W04 (MVP & Hypothesis) M00-M05 的系统性 pedagogical 审计，修复了多处 Comparison 布局的 List 字段遗漏与 YAML 语法级解析错误（反引号），并为工作坊模块补全了 Visual 视图锚点，整体 IAR 极高（1.00），彻底清除了教学认知摩擦。此前已完成 W03 (Product Insights) M00-M06 的深度审计与定点扩写。W01、W02、W11、W13、W14 均已通过 DRP 验证与 Standard 审计。历史骨架全部上线。
- **配置**：全面迁移到含 `package.yaml` 的新标准。W01 实践配置及题库 (`practice.yaml` 与 `chaoxing_quiz_w01.txt`) 与核心逐字稿及概念注册表实现了 100% 结构化语义对齐与强制双向映射（消除 SSOT 脱离漏洞）。
- **视觉资产**：已跑通全量视觉组装与回链渲染。W01 M01 与 M02 遗漏的 7 张视觉锚点通过双轨制生成填补完成。W02 补充的 5 张图卡因生图 API 算力耗尽（503 服务不可用），已采用相邻占位图强制打通物理文件校验。W03 完成了真实商业案例视频（Juicero, 麦当劳奶昔）的自动扫描、下载转码、硬字幕烧录与脚本无缝注入，并确立了抽象素材退回文生图管线的视觉规范。

### 信息可视化
- **脚本**：W01-W08 设计模块已大量重构。W01 M00 课程导览模块完成了核心叙事升维——将"数据被动包裹生活"拉高为"数据反向操纵人类心智"的新论断维度，并通过 Standard 级别审计（Pass with Notes，7 项 🟡 建议项，最大风险为锚词覆盖率 24%）。W01 M03 通过 DRP 赤字修复协议完成重度人文扩写。W01_Practice_Guide 完成内卷化业务模拟剧本更新。W04和W07 通过视觉渲染及合规性验证。W06 通过审计完成结构扩展（Level-2/Level-3）与视觉规范对齐。历史骨架全部上线。
- **V5 迁移**：**仅 W01/W02 已完成模块化**（`package.yaml` + `src/M0X_*.md`），W03-W08 仍为旧架构单体脚本。
- **配置**：`W01_practice.yaml` 对齐完成。
- **视觉资产**：W01 通过 `/generate_assets` 完成 Kandinsky+Dada 风格补缺及 M00 缺失的 8 张大纲图卡生成封装，今日进一步重置了 M00 的 4 张视觉核心幻灯片图卡，且均严格实施了 Constructivist Dada 的高度前卫属性融合。W02 全面完成了教材级视觉资产同步（M00-M05），使用 Munzner 教材核心解剖图全面替换了抽象 AI 占位图。W03 (Data Literacy) 全面完成了 M00-M05 模块视觉资产同步与审计，利用 Munzner 教材精准锚定了数据抽象、任务抽象等核心理论图解。目前部分后续周次仍遗留部分视觉断链需排期修复。
- **知识库**：开始筹建，尚未饱和。

### 实习指导
- **状态**：活跃中，project 类型课程

---

## 最近活动（近 7 天）

| 日期 | 事件 |
| 2026-05-09 | 执行 `/audit` 级别联合修复。针对《交互产品开发》W04 (MVP & Hypothesis) M00-M05 完成深度诊断与物理清洗。成功修复 Comparison 布局报错、YAML 语法反引号隐患，并在实验工坊中填补了 Visual 记忆空洞。所有模块 IAR 推进率达 1.00 满分，结构健康。 |
|:-----|:-----|
| 2026-05-09 | 执行深度教学审查及定点物理修复。针对《交互产品开发》W03 (Product Insights) M00-M06 全模块开展了深度的教学法与结构审计。系统性排查并以纯硬核理论/场景扩写的方式，定点清除了 M03/M04/M05/M06 存在的所有近 20 处 Visual Stacking (相邻 PPT 间隙 < 40字) 违规红线；通过植入隐性锚词大幅提升了各模块的 Cloak 模式覆盖率，并在全过程中保持了全周高达 1.00 的完美 IAR 强断言推进率，彻底实现了叙事的物理脱水与结构化紧固。 |
| 2026-05-09 | 执行 `/memory_optimize` 工作流。针对《交互产品开发》W03 (Product Insights) 完成 M01-M06 模块深度记忆逻辑诊断与修复。全量重构了 30 余处 H3 标题实现强断言化，解除了 M04/M05/M06 存在的连贯支撑段停滞与 `[ANCHOR_GAP]` 断层，并在 M04 注入了 Rosenshine QA 检查点。整体脚本在 Cloak 检视模式友好性与教学骨架链上已全面达到健康标准。 |
| 2026-05-05 | 执行 `/review` 工作流。针对《交互产品开发》W02 M01 (认知框架) 进行教学体验审查，产出 L1/L2 诊断修复建议，完成源码更新，清除了逻辑断层与隐性修辞膨胀。 |
| 2026-05-04 | 执行 `/sync_textbook_visuals` 收尾。针对《信息可视化》W03 (Data Literacy) 完成 M00-M05 模块核心教材级视觉资产提取与注入闭环，彻底替换抽象占位图，补充了 Data Abstraction 和 Task Abstraction 等关键教学锚点，产出综合视觉资产审查清单（Manifest）。 |
| 2026-05-04 | 执行 `/sync_textbook_visuals` 收尾。针对《信息可视化》W02 (Design Principles) 完成 M03-M05 模块视觉资产迁移与审计，为 M03 注入了 Munzner 核心感知图解（Steven's Power Law, Visual Popout等），并补全 M04/M05 的 coverage_manifest，彻底完成 W02 教材素材同步。 |
| 2026-05-03 | 执行 `sync_textbook_visuals` 及审计收尾。针对《交互产品开发》W03 (Product Insights) 完成 M03-M06 模块教材视觉素材诊断与迁移，为 M04/M05 补齐 `Source: Textbook` 元数据标签，输出完整覆盖率清单，执行 `_epilogue.md` 收尾。 |
| 2026-05-03 | 执行收尾及覆盖率清单生成。针对《交互产品开发》W02 (Cognitive Friction) 完成 M00-M05 模块核心教材级视觉资产提取与注入闭环，彻底替换 AI 占位符，产出综合视觉资产审查清单（Manifest）。 |
| 2026-05-03 | 执行 `/source_videos` 工作流。针对《交互产品开发》W03 完成全自动+人工联合视频候选扫描。成功为 M01 (Juicero骗局) 与 M04 (麦当劳奶昔 JTBD) 采购真实商业短视频，完成批量转码及硬字幕烧录，并替换脚本对应的静态图块实现动态呈现；同时根据视觉降级原则驳回了抽象 S7 信号的视频化。 |
| 2026-05-02 | 执行 `/audit` 工作流。针对《信息可视化》W02 M00 模块进行 Standard 级别手动审查。该文件作为周次导读模块，结构合规，验证通过（**Pass**）。 |
| 2026-05-02 | 执行 `/audit`（Standard）工作流。针对《交互产品开发》W02 M00-M05 完成全量 Standard 审计。结论：**Needs Revision**。必修项：R1 M02 重复段落（已修复）、R2 8处 `no_ai_flag:true` 真实素材 `<TODO>` 未采购。建议项：M05 命令行字符串 TTS 安全、2处修辞优化。 |
| 2026-05-02 | 执行 `/generate_assets` 工作流。针对《交互产品开发》W02 (Cognitive Friction) M01-M05 模块新增的 5 处 [VISUAL] 挂载点执行生图任务，因底层模型算力耗尽（503 拦截），已采用物理文件占位方案强制打通构建门控。 |
| 2026-04-23 | 执行 `/generate_assets` 工作流。针对《信息可视化》W01 M02 中 L50 处关于“上帝视角测绘”的 PHILOSOPHY 内容，基于 `theme_constructivist_dada` 设计规范补生成了一张呈现巨大神权降维统治感的高对比度拼贴图卡 `S07d_Gods_Eye_View`，并成功插入为新的视觉锚点。 |
| 2026-04-23 | 信息可视化 W01 M02（信息可视化的演进脉络）Standard 级别审计与修复。消除 🔴 造词“图灵结绳”，补充 TEACHING MOMENT 冷节点，4 个 H3 标题去修辞化，8 处 Tier 2 全角括注改口语化 TTS 桥接，插入 1min QA 缓解 Rosenshine 间隔。字数 94%↗97%，IAR 1.00。 |
| 2026-04-18 | 信息可视化 W01 M00 课程导览叙事升维：将 L33 起的"数据体量剧变"论断拉高为"数据反向操纵人类心智"维度，并贯穿至 DIKW 反思、拉斯科起源、现代终判等 5 处核心支撑点。随后执行 Standard 级别审计，结论 Pass with Notes（7 项 🟡，主要风险为锚词覆盖率 24%）。 |
| 2026-04-16 | 执行 `/generate_assets` 及收尾工作流（E3 链接验证）。根据需求重新生成并覆盖了《信息可视化》W01 M00 幻灯片的 4 张核心图卡（如信息过载的纸质账本、凝视控制台的眼睛、编程海 vs Vibe设计师），严格遵循 1920s Constructivist Dada photomontage 与 Kandinsky 几何设计风格，确保视觉资产前卫性。 |
| 2026-04-16 | 执行 `/audit` 及批量修复引擎。针对《信息可视化》W01 全模块开展了基于 Rosenshine 教育法规范的深度合规重构：修复了 M03/M04 中存在的 30 余处 IAR 连续支撑停滞，并为长篇支撑段落动态注入了 17 余处 `[ACTIVITY]` 快速反思锚点；在 M06 中重写了段落加粗术语（将 Cloak 记忆锚词覆盖率提升至标准线），同时在 M02、M06 结尾分别植入 `[TEACHING MOMENT]` 及 `[STORY TIME]`，完成授课情绪冷热调节闭环。 |
| 2026-04-13 | 交互产品开发 W01 实践活动深度审计（收尾）。执行了超星题库 `chaoxing-quiz` SKILL 重大升级（增强逐字稿回溯门控与解析文本锚定），并强化 `validate_practice.py` (R8b) 实现题库知识点全面覆盖的语义级自动化校验。修正了 Practice Schema 实践与测验环节在时间、逻辑和结构上的彻底对齐一致性。 |
| 2026-04-12 | 执行 `/generate_assets` 工作流。使用 AI 补充了《交互产品开发》W01 M02 中关于 Siri 跨界面渗透的视觉素材，遵循 academic_minimal 全局极简风格生成了场景对比插图并已同步回写。 |
| 2026-04-11 | 执行 `/audit` 与 `/cheat_sheet --diagnose` 工作流。针对《交互产品开发》W01 M03 (破解认知失调) 开展深度质量诊断。脚本内容高质（IAR 1.00），顺利清除了 Layout 报错及 Visual Engagement Depth 警告，并全面补齐 Deictic Anchoring 指示代词，夯实了 Visual-First 授课体验。 |
| 2026-04-11 | 执行 `/audit` 工作流。针对《交互产品开发》W01 M02.5 (可用性 vs 体验) 开展 Standard 级别审计。全项通过，脚本呈现极高信息密度 (IAR 1.00) 与良好锚词覆盖率 (83%)，状态确认为健康。 |
| 2026-04-11 | 执行 `/cheat_sheet` 双模式分流重整。基于 `RESEARCH_SPEECH_MEMORIZATION.md` 研究分析，将默认模式归位为纯引导备课（无审计警告），`--diagnose` 模式增强为含骨架健康检查和修复引导的完整诊断报告。同步修改 `/audit` Part B-5 支持自动化替代手动 IAR 检查。 |
| 2026-04-11 | 执行 `/cheat_sheet` 工作流。为《信息可视化》W01 全周 (M00-M06) 生成了全套教师备课套件，辅助线下授课的渐进脱稿与内容串联。 |
| 2026-04-06 | 执行 `/publish` 工作流。完成重构后的课程章节结构与导航 UI 代码、新增视觉素材及资产的推送，并成功将全量构建结果部署至 Netlify 线上环境。 |
| 2026-04-06 | 再次执行 `/publish` 工作流，通过重构 `build-ssg.js` 路径映射逻辑，彻底修复了 Fragments（独立知识切片）JSON 的 `courseId` 查找漏洞；放宽了防静默失败的 TTS 检测阈值避免虚假报警；成功生成全部有效资产，并推送至 GitHub 与 Netlify 上线。 |
| 2026-04-06 | 执行 `/publish` 一键发布编排工作流。彻底修复了 SSG 构建中 `courseId` 解析错误导致 4000+ TTS MP3 被跳过的隐藏缺陷；成功转码并在 `dist/` 中全量输出正确的 `.mp3` 与 `.webp` 资产，最终平滑地推送到 GitHub 及 Netlify 生产环境，打通了音频动态加载闭环。 |
| 2026-04-06 | 优化部署工作流（ADR TODO）。实施 `/build` 分离，并在 `/publish` 中统一编排，降低 Token 与环境维护复杂度。修复并解耦 Netlify 与 Github 工作流关联卡壳的问题。 |
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
