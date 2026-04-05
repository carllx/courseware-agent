# 依赖关系图 (Dependency Map)

> 修改任何规则或工作流前，先查阅此图确认下游影响。
> 此文件由 `/update_guidance` 工作流自动引用。

---

## 规则 → 工作流/技能引用矩阵

| 规则文件 | 被引用方 | 影响范围 |
|:---|:---|:---|
| `rule_localization.md` | write (Phase 2), audit, script_format | 语言规范 |
| `rule_asset_management.md` | generate_assets, ppt, h5 | 资产路径 |
| `rule_content_depth.md` | write (Phase 1/2), audit Q3, narrative_archaeologist | 知识饱和度 + 素材预算 + DRP 字数修复（整合原 `rule_saturation`/`rule_drp`/`rule_best_practices`） |
| `rule_narrative_standards.md` | write (Phase 2), audit Q4, script_format, update_guidance | 叙事质量 |
| `rule_outline_alignment.md` | write (Phase 3), audit Q5, audit_deep G4 | 大纲一致性 O1-O10 |
| `rule_dma_course_design.md` | new_course, write (DMA 课) | DMA 设计范式 |
| `rule_visual_generation.md` | generate_assets | 视觉生成约束 |
| `rule_training_plan_compliance.md` | audit_deep G1-G6, audit_courseyaml | 人培/OBE 合规 |
| `rule_document_boundaries.md` | write, audit, new_course, update_guidance | 文档职责边界 |
| `rule_security_governance.md` | 全局 | 安全治理 |
| `rule_meta_learning.md` | 全局 | 自演化协议 |
| `rule_cross_agent_protocol.md` | mailbox_in, mailbox_out | Agent 通信 |
| `rule_assessment_constraints.md` | audit_courseyaml | 成绩分值映射 |
| `rule_practice_standards.md` | design_practice, write (Phase 1), audit_deep (Part H) | 实践步骤合规 |

---

## 工作流 → 工作流依赖矩阵

| 工作流 | 前置条件 | 后续工作流 |
|:---|:---|:---|
| `/new_course` | — | `/design_practice`, `/write` |
| `/design_practice` | `/new_course`（首次） | `/write` |
| `/write` | `/design_practice`（条件必选：当该周 `hours_practice > 0` 时） | `/audit` |
| `/audit` (Quick+Standard) | `/write` (fill_ratio ≥ 0.8) | `/generate_assets`, `/audit_deep` |
| `/audit_deep` (Part D+G+H) | `/audit` Q1-Q7 通过 | `/generate_assets` |
| `/audit_courseyaml` (Part F) | `/audit` Q1-Q7 通过 + course.yaml 在审计范围 | — |
| `/generate_assets` | `/audit` Q3 通过（字数门控） | `/ppt` |
| `/ppt` | `/generate_assets` | `/h5` |
| `/h5` | `/ppt`（可选）；热重载模式仅需 `npm run dev` | `/export` |
| `/export` | `/write` | — |
| `/update_guidance` | 规则/技能变更 | 受影响的工作流（参上表） |

---

## 技能 → 工作流绑定

| 技能 | 绑定工作流 | 触发条件 |
|:---|:---|:---|
| `librarian` | `/write` Phase 1 Step 2.3 | 知识扫描 |
| `narrative_archaeologist` | `/write` Phase 1 Step 2.5 | 深度调研 |
| `script_format` | `/write` Phase 2 Step 3 | 写作规范 |
| `validation_suite` | `/write`, `/audit`, `/generate_assets` | 验证器调用 |
| `validation_suite` (rules) | `/update_guidance` §C | `validate_rules.py` — 规则 frontmatter 合规性 |
| `validation_suite` (V5) | `/audit`, `/new_course` | `validate_package.py` — V5 package.yaml 校验 |
| `docx` | `/export` | Word 导出 |
| `pptx` | `/ppt` | PPT 生成 |
| `pdf` | 按需 | PDF 处理 |
| `agent-architect` | 按需 | Rule/Workflow/Skill 创建与管理 |

---

## 变更影响速查

修改一个文件时，通过上表查找「被引用方」列，即为需要检查的下游文件。
例如修改 `rule_content_depth.md` → 需检查 `write_phase2_compose.md`、`write_phase1_prep.md`、`audit.md`。

### 隐式依赖（不在上表中但需注意）

| 上游文件 | 下游依赖 | 影响说明 |
|:---|:---|:---|
| `dumptext.py` 的 `BEGIN/END` 标记格式 | `generate_course_h5.py` 的 `_build_source_map()` 正则 | 标记格式变更须同步更新源映射正则，否则 copy-locator 精度静默退化（ADR 036） |
| 课程目录结构 `<course>/weeks/<week>/src/*.md` | `vite-plugin-h5-hot-reload.js` 的 `shouldHandle()` 正则 | 目录层级变更（如 V5→V6 重构）会静默使热重载监听失效（ADR 037） |
| `generate_course_h5.py` 的 `--rebuild-week` CLI 参数 | `vite-plugin-h5-hot-reload.js` 的 `handleFileChange()` spawn 调用 | Python CLI 参数名变更须同步更新插件中的 args 数组（ADR 037） |
| `validate_runner.py` 的 JSON 返回结构 | `ValidationContext.jsx` 及相关可视化组件 | 前端 Craft-room 的可视化强依赖由 `--h5-ws` 通道传来的字数、断链等数据结构（ADR 038） |
| `tts_bridge.user.js` 的 postMessage 协议 | `doubao-tts.js` 消息路由 + `TtsSegmentContext.jsx` 状态引擎 | 桥接协议变更须三文件同步（ADR 039） |
| `generate_course_h5.py` 的 `_compute_tts_fingerprint()` 格式 | `fingerprint.js` 的 `computeTtsFingerprint()` + IndexedDB 缓存键 | 指纹格式不一致将导致前后端缓存键永久失配（ADR 039 V-04） |
| `engines/h5_template/vite-plugin-h5-hot-reload.js` 的 TTS 中间件 | `build/h5_preview/vite-plugin-h5-hot-reload.js`（部署快照） | **SSOT 在 engines/**，修改后须 `cp` 同步到 build/（ADR 040） |
| `TtsSegmentContext.jsx` 的 `getTtsAudioUrl()` URL 格式 | `vite-plugin-h5-hot-reload.js` 的 TTS 音频代理正则 | URL 路径格式变更须同步代理中间件（ADR 040） |

---

## 实验规划 → 工作流引用

| 文件 | 被引用方 | 影响范围 |
|:---|:---|:---|
| `<课程>/practices/experiment_planning.md` | `/write` Phase 1 Step 2.1b, `/audit_deep` Part H, `/design_practice` Step 2 | 实验进度、数据流、AI 边界、工具链约束 |
| `<课程>/practices/project_brief.md` | `/write` Phase 1 Step 2.1b, `/audit_deep` Part H | 综合项目节点、交付物清单 |
| `<课程>/practices/W0X_practice.yaml` | `/write` Phase 1 Step 2.1b, `/audit_deep` Part H | 每周实践步骤规格、时间分配、AI 边界 |
