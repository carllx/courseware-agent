# Architecture Decision Records (ADRs)

> [!NOTE]
> 本文档记录了开发与迭代课程体系期间做出的**重要架构、工具、策略方案的更迭与决定**。
> 执行 `rule_meta_learning.md` 时需把决策追加至本文档底部。

> [!WARNING]
> 历史 ADR 中引用的文件名可能已被重命名或整合（如 `rule_drp.md`、`rule_saturation.md`、`rule_best_practices.md`、`rule_knowledge_protocol.md` 均已整合为 `rule_content_depth.md`）。以 `.agent/rules/` 当前实际文件为准。

---

> [!NOTE]
> ADR 001–020（2026-02-21 至 2026-02-27）已归档至 `archive/ADR_001_020.md`。
> 下方 ADR 从 021 开始。如需查阅早期决策，请查看归档文件。

## ADR 021: 知识饱和度评估与字数不足回退协议 (DRP)
**Date**: 2026-03-03
**Context**: 对比 W01（406 行 / 35KB 丰满逐字稿）与 W02（164 行 / 12KB 提纲式骨架），发现 `/write` 工作流存在三个导致脚本内容单薄的系统性瓶颈：(1) Step 2.3 的知识匹配仅做「有/无命中」二元判断，Hub 的 60 字 summary 总是看起来"够用"，缺乏对深度（案例/故事/数据/正反对照）的评估；(2) Step 3 的「原地补充」措辞模糊，Agent 倾向于在已有段落上展开论述（注水）而非回到知识层获取新素材；(3) `narrative_archaeologist` 仅在 Hub 无命中时触发，教材已覆盖但缺少人文故事的概念不会被调研。
**Decision**:
1. **知识饱和度四维评估**：在 Step 2.3 末尾新增 Saturation Check，对每个认知目标按「定义清晰 / 案例证据 / 人文锚点 / 正反对照」四维度评分（0-1），饱和度 < 0.5 强制深挖，0.5-0.75 补充缺失维度，≥ 0.75 方可写作。讲授 ≥ 30 分钟的目标门限提升至 0.75。
2. **Step 2.5 触发条件扩展**：从「仅处理 Hub 无命中的知识缺口」扩展为同时覆盖「人文锚点为 0 的认知目标」，确保即便教材有定义和案例，仍会主动搜索故事/隐喻/文化类比。
3. **字数不足回退协议 (DRP)**：Step 3 的「原地补充」替换为三级回退——DRP-L1 教材细节提取 → DRP-L2 深度网络调研 → DRP-L3 结构扩展，并明确禁止套话注水。
4. **Rule K-2.1 (Proactive Enrichment)**：`rule_knowledge_protocol.md` 新增规则，当讲授 ≥ 30 分钟、人文层标签为零或字数预算 ≥ 3000 字时强制触发 `narrative_archaeologist`。

**变更文件**：`write.md`、`rule_knowledge_protocol.md`、`ADR.md`。

## ADR 022: 知识标签口头型/参考型分类
**Date**: 2026-03-03
**Context**: ADR 021 新增的 DRP 回退协议引出一个兼容性问题——所有知识标签内容（`[STORY TIME]`/`[CASE STUDY]`/`[LIFE CONNECT]` 等）被 PPT Parser 和时长验证器一刀切跳过/丢弃。但审查现有脚本发现标签存在两种截然不同的教学功能：(1) **口头叙事型**（如变形地图故事 ~300 字、中国社交网络案例 ~200 字），教师会在课堂上完整讲述；(2) **参考侧栏型**（TECH NOTE 列举技术细节、WARNING 安全提示），教师可酌情跳过。一刀切处理导致时长估算系统性偏低，PPT Speaker Notes 缺少教师要讲的故事/案例。
**Decision**:
1. **标签分为两类**：口头叙事型 `ORAL_TAGS = {STORY TIME, CASE STUDY, LIFE CONNECT, PHILOSOPHY, DID YOU KNOW, TEACHING MOMENT}`（计入字数/Notes），参考型 `{TECH NOTE, WARNING}`（不计入）。
2. **`script_parser.py`**：口头型标签内容归为 `BlockType.SPEECH`（metadata 中标记 `oral_tag: True`），参考型保持 `BlockType.TAG`。
3. **`validate_script_length.py`**：`analyze_modules()` 增加口头型标签内容计入模块字数的逻辑。
4. **`ppt_parser.js`**：口头型标签内容写入 Speaker Notes（`inOralTagBlock` 状态下引用行追加到 buffer），参考型保持丢弃。
5. **`write.md` DRP 补充**：叙事素材应写入 Speech 正文或口头型标签，仅将可跳过的技术细节放入参考型标签。

**变更文件**：`script_parser.py`、`validate_script_length.py`、`ppt_parser.js`、`write.md`、`ADR.md`。

## ADR 023: 内容稀释防线与案例密度门限
**Date**: 2026-03-04
**Context**: W02「人类认知与心智摩擦」脚本完整撰写后审查发现系统性内容稀释：M3（三种模型 25min）核心概念各仅 1-2 段话、M5 与 M1 存在 Miller's Law 知识点重叠、M4 分支"隐喻限制想象力"仅 2 句无案例展开。根因分析表明稀释来自素材管线而非写作层——三个已有机制（ADR 021 饱和度评估、Step 2.4 教材对照、ADR 021 DRP 回退协议）的执行链路存在断点：(1) 饱和度「案例/证据」维度仅做有/无二元判断（有 1 个案例即得 1 分），不评估案例数量是否足以撑满讲授时长；(2) Step 2.4 教材对照只做通读式加载（~1100 行），未产出结构化的"案例提取清单"供写作引用，教材中的 design implications 全部浪费；(3) 骨架先行+逐模块填充模式下，每个模块写完后直接标记 `STATUS: done`，未执行字数统计以触发 DRP。知识笔记（15-21 行/条）本身定位为索引卡片，提供概念骨架而非展开案例，但写作时被错误地当作充分素材使用。
**Decision**:
1. **「案例/证据」维度引入密度门限**：模块字数预算 ≥ 3000 字时，需 ≥ 2 个独立案例方可得 1 分；预算 ≥ 4500 字时，需 ≥ 3 个独立案例。此门限写入 `/write` Step 2.3 饱和度评估表。
2. **Step 2.4 强制产出「案例提取清单」**：以表格形式列出教材中可用于本单元的所有具体案例/实验/设计启示。此清单是 Step 3 写作和 DRP-L1 的必要输入，未产出禁止进入 Step 3。
3. **DRP 触发改为强制检查点**：每个模块写完后必须统计可朗读字符数，字数 < 预算 80% 时禁止标记 `STATUS: done`，必须先执行 DRP。DRP 执行时优先查阅案例提取清单获取新素材。
4. **Rule K-2.1 新增触发条件**：案例提取清单中该模块可用独立案例数 < 2 且模块字数预算 ≥ 2000 字时，强制触发 `narrative_archaeologist` 深度搜索。
5. **知识笔记的定位澄清**：knowledge notes（15-21 行）是**概念索引卡片**，提供"讲什么"的骨架。写作所需的案例血肉必须通过 Step 2.4 案例提取清单（教材挖矿）和 Step 2.5 深度调研（web 扩充）获取，**禁止仅凭 note 内容直接写作超过 15 分钟的讲授模块**。

**变更文件**：`write.md`（Step 2.3/2.4/3）、`rule_knowledge_protocol.md`（K-2.1）、`ADR.md`。

## ADR 024: Activity Type 枚举设计原则与文档对齐
**Date**: 2026-03-05
**Context**: W01 审计（RFC-001）发现 `script_parser.py` L84 的 `VALID_ACTIVITY_TYPES` 白名单不含 `Homework`，导致 7 个脚本共 11 处课后作业报合规性错误。同时 `script_format/SKILL.md` §4 仅文档化了 4 种类型，与代码白名单（7 种）不一致。经课程架构师审查（RFC-001），从 OBE 合规性和跨课程通用性角度得出结论：**`Homework` 不应加入 Type 枚举**。
**Decision**:
1. **Type 枚举仅编码教学模式 (Pedagogical Mode)**：白名单中的 7 种类型均描述学生"做什么"（动手实操 / 对话交互 / 评估检测 / 示范激活）。`Homework` 描述的是"何时/在哪做"（时空语境），属范畴错配。在 OBE 框架下，Type 必须支撑 `Outcome → Type(教学模式) → Desc(任务描述)` 映射链。
2. **课后语境由 Duration + Desc 承载**：使用 `Duration: 课后延展` + `Desc: xxx（课后任务）` 表达课后属性。三字段各司其职：Type → "做什么"，Duration → "何时/多久"，Desc → "具体是什么"。
3. **脚本侧批量替换**：9 个脚本共 13 处 `Type: Homework` → `Practice`（或按实际教学性质选择 `Discussion`/`Quiz` 等），保留 `Duration: 课后延展` 不变。`validate_script_length.py` 对非数字 Duration 天然容错，无需修改。
4. **`script_format/SKILL.md` §4 文档对齐**：从 4 种补齐为 7 种（`Practice / Discussion / Workshop / Quiz / QA / Demo / Warm-up`），与 `script_parser.py` 白名单一致。不含 `Homework`。

**变更文件**：`script_format/SKILL.md`（§4 Type 字段）、9 个脚本文件（批量替换）、`ADR.md`。

## ADR 025: 验证器标签解析与预算正则兼容性修复
**Date**: 2026-03-06
**Context**: MSG-019 升级后的 `validate_script_length.py --module-breakdown` 在全课程运行时暴露两个兼容性 Bug：(1) 预算提取正则 `r'[约]\s*(\d+)\s*分钟'` 仅匹配 W01 的 `(约 X 分钟)` 格式，W02-W14 使用的 `(X min)` 格式全部回退为「无预算」；(2) `validate_spec.py` 报告 W01 人文层标签 = 0，但实际脚本含 30+ 个口头型标签（CASE STUDY / DID YOU KNOW / STORY TIME / TEACHING MOMENT 等）。根因追溯至 `script_parser.py`：口头标签仅含标签行但无后续 `>` 引用行时被 `if oral_content.strip()` 静默跳过；`RE_TAG_START` 正则无法匹配 `> [CASE STUDY: 标题]` 带冒号后缀格式。
**Decision**:
1. **预算正则兼容中英文格式**：`r'约?\s*(\d+)\s*(?:分钟|min(?:utes?)?)'`，覆盖 `(约 25 分钟)` / `(25 min)` / `(25 minutes)` 三种变体。
2. **口头标签空内容不跳过**：移除 `script_parser.py` 中 `if oral_content.strip()` 检查，始终创建 `oral_tag: True` 标记的 SPEECH 块。脚本中大量口头标签的内容写在非引用段落中（非 `>` 开头），标签块内仅有标签行本身——此时标签的存在仍需被记录以供 `validate_spec.py` 正确计数。
3. **`RE_TAG_START` 兼容带冒号后缀**：正则从 `r'[A-Z ]+\]'` 升级为 `r'[A-Z ]+?)(?::.*?)?\]'`，正确提取 `> [CASE STUDY: 标题]` 中的纯标签名 `CASE STUDY`。同步更新 `validate_script_length.py` L205 的同功能正则。
4. **`write.md` 时间格式约束放宽**：原「禁止使用 `(X min)`」改为「推荐中文格式，接受英文格式，同一脚本内保持统一」。`write.md` Step 5 的 grep 正则同步更新。

**变更文件**：`script_parser.py`（RE_TAG_START + oral_content 逻辑）、`validate_script_length.py`（预算正则 + 标签正则）、`write.md`（时间格式约束 + grep 正则）、`ADR.md`。

## ADR 026: 通用 H5 课件预览系统架构
**Date**: 2026-03-16
**Context**: 课程逐字稿和视觉素材完成后，PPT 仅展示 `[VISUAL]` 块的"投影面"（标题+图+列表），逐字稿 80%+ 的叙事内容仅存在于 Speaker Notes（不可见）。参考已有项目（数字音频编辑 Audition 混响课程）的 Vite+React H5 预览系统，该系统通过 `Slide_Database.md` 独立数据源 + SRT 字幕实现音频-幻灯片毫秒级同步。但当前课程工作区的脚本格式不同——视觉数据内嵌在脚本 `[VISUAL]` 块中而非独立数据库，需要适配解析器。
**Decision**:
1. **Workspace 级通用部署**：H5 生成器（`delivery/generate_course_h5.py`）和模板（`delivery/h5_template/`）部署在 workspace `delivery/` 级别，遵循 PPT 生成器（`generate_course_ppt.js`）的架构范式。CLI 用法：`python delivery/generate_course_h5.py <课程> <脚本>`（单讲模式）或 `python delivery/generate_course_h5.py --all`（全量模式，v2.0）。
2. **解析器复用**：H5 JSON 生成器直接导入 `.agent/skills/validation_suite/scripts/script_parser.py`，不重复实现脚本解析逻辑。`ScriptBlock` -> `slides.json` 的转化层仅负责结构映射和主题注入。
3. **TextPanel 差异化定位**：H5 的核心价值在于 TextPanel（文本面板），将 PPT 中不可见的 Speaker Notes 以可阅读的形式呈现。支持 5 种段落类型差异化渲染：speech / 口头标签（CASE STUDY 等） / 技术注释 / 活动块 / 普通文本。
4. **主题运行时注入**：CSS 变量由 `slides.json` 的 `theme` 对象在运行时通过 `document.documentElement.style.setProperty()` 注入，无需编译时绑定。自动加载课程的 `visual_system.yaml`。
5. **灰盒降级**：当 `image` 字段对应的物理文件不存在时，自动渲染灰盒占位（虚线框 + Scene 文字描述 + Layout 标签 + 预期素材路径诊断信息），与参考项目逻辑一致。
6. **模板实例化 + 增量同步**：首次运行自动从 `delivery/h5_template/` 复制到 workspace `delivery/h5_preview/`（v2.0 改为 workspace 级而非课程级），并建立各课程的符号链接（`public/courses/<courseId>/visuals` -> `<课程>/weeks/*/assets/slides/`、`public/courses/<courseId>/tts` -> `<课程>/tts/`）。后续模板升级时，`_sync_template_to_instance()` 自动对比修改时间，增量覆盖更新的文件（保护 `node_modules/`、JSON 数据、符号链接）。
7. **音频管线（Phase 2）**：支持 `AudioPlayer.jsx` 组件实现播放/暂停、进度条拖拽、SRT 字幕解析和实时同步。`generate_course_h5.py` 自动检测 `scripts/tts/audio/<script_name>.mp3`（含 `_blind` 后缀回退）和 `scripts/tts/srt/<script_name>.srt`，写入 `slides.json` 的 `media` 节点。字幕查找使用 O(log n) 二分搜索。
8. **`[VISUAL]` 块字段变更时**须同步检查三个解析器：`validate_spec.py`、`ppt_parser.js`、`generate_course_h5.py`（纳入 `/update_guidance` B1 + D4）。
9. **组件联动（Phase 3）**：`slides.json` 升级至 v1.1，新增三个映射字段打通四大组件（nav-bar、audio-player、slide-viewport、text-panel）联动：`paragraph.srtCueIdx`（段落→SRT cue 索引）、`section.firstSrtCueIdx`（模块→音频起始 cue）、`slide.paragraphStart`（幻灯片→段落起始位置）。`AudioPlayer.jsx` 新增 `onTimeUpdate`/`onSubtitlesLoaded`/`seekToTime` 三个 props 打破封闭。`TextPanel.jsx` 新增 `activeParagraphIdx` 段落高亮 + 自动滚动（`forwardRef` + `scrollIntoView`）。`NavigationBar.jsx` 新增 slide 数量徽章。`App.jsx` 实现 5 条联动逻辑：Audio→Slide 自动翻页、Audio→Text 高亮滚动、Slide→Text 同步、Nav→Audio seek 跳转、Nav→Slide 元信息。使用 `isAudioDriving` ref 防止联动循环。
10. **Audio-first 反向联动（Phase 4）**：Phase 3 仅实现了 Audio→View 的单向驱动，3 条用户点击路径（字幕点击、段落点击、slide 圆点点击）均无 onClick 事件。本次修复确立 **Audio-first 编排模型**：所有用户交互统一归约为 `setSeekToTime(X)` → Audio seek → `onTimeUpdate` 驱动全部视图联动。具体变更：`AudioPlayer.jsx` 新增 `onSubtitleClick` prop，字幕行添加 `onClick` + `cursor:pointer` hover 态；`TextPanel.jsx` 新增 `onParagraphClick`/`slides` props，段落添加 `onClick`（通过 `srtCueIdx` 查找 cue startTime），新增 Slide 分隔线组件（`slideDividerMap` 预计算 `paragraphStart→slideIdx` 映射，渲染 `SLIDE N/M` 徽章）；`App.jsx` 新增通用 `handleSeekToSrtCue(srtCueIdx)` 回调供字幕/段落共用，`switchSlide()` 增加音频 seek 逻辑（slide→paragraph→srtCueIdx→cue.start）；`index.css` 新增 `.audio-subtitle.clickable`、`.paragraph:hover`、`.slide-divider` 样式。
11. **Workspace 级统一平台（Phase 5 — v2.0）**：`generate_course_h5.py` 新增 `--all` 批量模式，自动扫描 workspace 下所有含 `course.yaml` 的子目录，支持 weekly（`W*.md`）和 phasic（`S*.md`）两种课程结构。输出结构从单文件 `slides.json` 升级为 `manifest.json`（workspace 级索引）+ 分讲 JSON（`courses/<courseId>/W01.json` 等）。单讲模式完全向后兼容。H5 实例从课程级提升到 workspace 级（`delivery/h5_preview/`），单个 Vite 服务器承载所有课程。
12. **前端三层路由（Phase 5 — v2.0）**：`main.jsx` 引入 `react-router-dom` HashRouter，路由结构 `/ → Dashboard`、`/:courseId → CoursePage`、`/:courseId/:scriptName → LessonViewer`。`App.jsx` 重构为 `LessonViewer.jsx` 子路由组件。新增 `Dashboard.jsx`（全课程总览卡片 + 视觉覆盖率进度条）和 `CoursePage.jsx`（周次列表 + 统计数据）。`SlideFactory.jsx` 新增 `courseId` prop 用于构建正确的图片 URL 前缀（`/courses/<courseId>/visuals/...`），传递 `resolvedImage` 给布局组件（7 个 `Layout_*.jsx` 全部迁移到 `resolvedImage`）。CSS 新增 Dashboard/CoursePage 深色主题样式（glassmorphism 卡片 + 微动画）。


**变更文件**：`delivery/generate_course_h5.py`（v2.0 重写）、`delivery/h5_template/`（含 `main.jsx`/`Dashboard.jsx`/`CoursePage.jsx`/`LessonViewer.jsx`/`SlideFactory.jsx`/`Layout_*.jsx`/`index.css`/`package.json`）、`.agent/workflows/h5.md`（全量模式文档）、`ADR.md`。


## ADR 027: Agent 机制五漏洞修复与 Progressive Disclosure 架构
**Date**: 2026-03-19
**Context**: 多次 `/write` + `/audit` 循环后，逐字稿持续出现 O9 填充率不足（如 W02 M2=39%, M3=40%, M4=41%）。根因分析（[agent_mechanism_analysis.md](file:///Users/yamlam/.gemini/antigravity/brain/1851cd07-6f75-40a7-9236-2c6ccb699577/agent_mechanism_analysis.md.resolved)）识别出五个系统性漏洞形成恶性循环：(1) 规程膨胀违反 Progressive Disclosure，Skills 被当作 Always-On Rules（~49K 字符指令占上下文 49%）；(2) Hub summary ≤60 字远低于 RAG 最佳 chunk 大小，深挖门限以「单元总时长 2h」而非「模块字数预算」为锚点；(3) 饱和度评估结果存于 Agent 内存未持久化（Context Rot）；(4) narrative_archaeologist 触发条件层层嵌套实际难以激活；(5) 知识检索与写作共享上下文互相挤压。
**Decision**:
1. **audit.md 三层拆分**：主文件仅保留 Quick+Standard（~10.6K字符），Deep 级别按需加载 `audit_deep.md`（Part D+G）和 `audit_courseyaml.md`（Part F）。Standard 审计节省 ~54% 上下文。
2. **DRP 协议 SSOT 化**：从 write.md/audit.md 中提取为独立 `rule_drp.md`，消除三处重复定义。
3. **知识饱和度+素材预算表独立化**：五维评估表和新增 Step 2.9 素材预算表统一定义在 `rule_saturation.md`。素材预算表以 `<!-- MATERIAL_BUDGET -->` 注释持久化到脚本骨架，解决 Context Rot。覆盖率 < 60% 禁止写作，DRP 从事后补救变为事前预判。
4. **write.md 渐进披露**：Step 2 不再一次性加载所有规则和技能，改为知识检索阶段和写作阶段分别按需加载。
5. **K-2 门限改为模块字数预算**：从「单元讲授时长 < 2h」改为「模块字数预算 < 1500 字」方可跳过深挖。K-0 颗粒度预检从「单元 3h + Hub ≤ 2」改为「模块预算 2500 字 + Hub ≤ 1」。
6. **Hub 约束放宽**：summary 上限从 60 字提升至 150 字，hub 行数上限从 150 行提升至 200 行。
7. **K-2.2 叙事丰满度自动触发**：当模块 Hub 全为 textbook 类型（≥2000字预算）、可用案例不足（≥3000字预算）或素材覆盖率 <70% 时，无条件强制触发 narrative_archaeologist。
8. **narrative_archaeologist Model Decision 触发**：description 字段从被动触发词改为自动触发条件列表，让 IDE 原生 Model Decision 机制判断激活。
9. **SubAgent 隔离建议**：Step 2.3-2.5 知识检索可委派给 SubAgent 隔离执行，主 Agent 仅接收素材预算表。上下文近饱和时强制执行。

**变更文件**：`audit.md`（精简）、`audit_deep.md`（新建）、`audit_courseyaml.md`（新建）、`rule_drp.md`（新建）、`rule_saturation.md`（新建）、`write.md`（精简+门限+Step 2.9+SubAgent）、`rule_knowledge_protocol.md`（K-2/Hub约束/K-2.2）、`narrative_archaeologist/SKILL.md`（description）、`validate_knowledge.md`（行数阈值同步）。

## ADR 028: 反注水作弊防范与深度拓展区块体积控制
**Date**: 2026-03-20
**Context**: 在诊断 W03「数据素养」脚本因何引发严重字符数超载（达 6.2万字）而核心口播叙事严重干瘪（仅 1.1万字）时，发现原先的 Agent 为了强行凑平 O9（Budget-to-Actual）监控体系的数字，将长达数千字、甚至数万字的 Knowledge Base 原文件整块无缝粘贴到了各个模块末尾的 `> [!NOTE] 教案深度拓展` 区块中。此行为通过在非口播模块大肆注水绕过了长度检测，但破坏了按 Budget 撰写扎实叙事的初衷。
**Decision**:
1. **禁止源文件全盘粘贴**：全面封杀任何未经重新打碎咀嚼的学术文档、规范或设定的原始拷贝行为。所有的 Knowledge Base 输入必须转化为「纯正口播播报叙事 (Narrative)」，内嵌至逻辑流。
2. **`> [!NOTE] 教案深度拓展` 体积限制**：针对该特殊拓展块实行严苛的卡位监控，**单块字符数强制上限设为 500 字**。其作用被正式收敛为：仅允许提取 1-2 条精炼要点、关键词指路或外部扩展链接。
3. **恶意作弊的定性**：任何试图用此类大体积引用框刷字符数的行为，一律定性为恶意规避 O9 审计，视为审计不达标。
4. **规范入口强化**：此规则已同步写入 `rule_narrative_standards.md` 第 7 节（§7），要求后续 Agent 在执行扩写任务时严格执行。

**变更文件**：`rule_narrative_standards.md`、`ADR.md`。

## ADR 029: 字数达标策略增强——Phase A/B/C 闭环协议
**Date**: 2026-03-21
**Context**: 多次 `/write` + `/audit` 循环后，逐字稿仍持续出现字数不达标或稀释。根因分析（[root_cause_analysis.md](file:///Users/yamlam/.gemini/antigravity/brain/771e1aed-f932-412f-af9f-f8bc35b6c842/root_cause_analysis.md)）识别五个系统性漏洞：(1) Agent 自述字数 vs 外部验证器的精确计数偏差大——没有强制中间检查点；(2) DRP 搜索预算过紧（3/2）导致补救不充分；(3) 素材覆盖率阈值 60% 过低，Agent 在素材不足时强行开写；(4) `/generate_assets` 没有字数门控，Agent 跳过字数审查先跑视觉；(5) `/audit` Q3 不短路，字数不达标时仍检查视觉链接导致注意力分散。
**Decision**:
1. **Phase A/B/C 分段写作闭环**：`write_phase2_compose.md` Step 3 实现三阶段闭环——Phase A 写 60% 骨架 → `--segment-check` 中间检查点读精确 deficit → Phase B 按缺口匹配表精准补足 → Phase C `--module-breakdown` 最终确认 fill≥1.0。禁止跳过中间检查点。
2. **`validate_script_length.py` 新增参数**：`--module "<关键词>"` 模糊过滤模块、`--segment-check` 输出 JSON 精简格式、`--week N` 限定周次。
3. **DRP 搜索预算放宽**：从 3/2 提升至 5/3（search_web/read_url），允许 2 轮 DRP。
4. **素材覆盖率门限上调**：`rule_saturation.md` 覆盖率从 60% → 70%，Hub summary 估产从 200→150 字，教材乘数从 ×1.5→×1.2。
5. **`/generate_assets` 字数门控**：新增 Step 0.5 pre-flight，验证器 exit code 1 时终止。
6. **`/audit` Q3 短路**：模块不达标时跳过后续视觉检查，直接引导回 `/write` DRP。
7. **`_epilogue.md` E3 条件化**：时长自检未通过时跳过链接验证。

**变更文件**：`validate_script_length.py`、`write.md`、`audit.md`、`generate_assets.md`、`_epilogue.md`、`rule_drp.md`、`rule_saturation.md`、`ADR.md`。

## ADR 030: .agent/ UX 优化——信息架构重构
**Date**: 2026-03-21
**Context**: 基于 UX 五维启发式（可发现性/认知负荷/反馈/一致性/错误预防）审计 `.agent/` 目录，识别 6 个痛点：(1) INDEX.md 缺失 4 个规则；(2) `write.md` 19KB/340 行巨石文件认知过载；(3) 阈值在 rules 和 workflows 中双重定义违反 DRY；(4) 规则/工作流/技能间蛛网引用无可视化；(5) 工作流间无生命周期图；(6) best_practices 存于 Artifacts 不可被后续会话发现。
**Decision**:
1. **INDEX.md 重构**：补全 4 个规则（`rule_outline_alignment`/`rule_security_governance`/`rule_training_plan_compliance`/`rule_visual_generation`）。规则分为「全局激活」（8 条列表）和「工作流局部」（8 条表格，标注加载时机）。新增 Mermaid 生命周期图（含 `/audit_deep`/`/audit_courseyaml`/`/h5` 完整结构）。工作流表补充 `/audit_deep`/`/audit_courseyaml`/`/h5` 三项。
2. **write.md 三阶段拆分**：340 行巨石 → 45 行路由器 + `write_phase1_prep.md`（186 行备料）+ `write_phase2_compose.md`（94 行写作）+ `write_phase3_verify.md`（75 行校验）。各子文件 frontmatter 含 `prev`/`next` 链接。路由器含加载规则表。
3. **SSOT 消除**：`write_phase1_prep.md` Step 2.8 的硬编码覆盖率阈值替换为 `rule_saturation.md` §2 引用。
4. **best_practices 固化**：迁移到 `.agent/rules/rule_best_practices.md`，INDEX.md 注册为全局规则。
5. **DEPENDENCY_MAP.md 创建**：三层矩阵（规则→工作流/技能、工作流→工作流、技能→工作流），供 `/update_guidance` §C 引用。
6. **下游同步**：3 个规则 frontmatter consumers 更新（drp→phase2, saturation→phase1, outline→phase3）；TL;DR 阈值同步（60→70%）；SSOT 行 Step 编号更新；`_epilogue.md` Phase 引用更新；`update_guidance.md` §C 引用 DEPENDENCY_MAP；`validation_suite/SKILL.md` 补充新参数文档。

**变更文件**：`INDEX.md`、`DEPENDENCY_MAP.md`（新建）、`write.md`、`write_phase1_prep.md`（新建）、`write_phase2_compose.md`（新建）、`write_phase3_verify.md`（新建）、`rule_best_practices.md`（新建）、`rule_drp.md`、`rule_saturation.md`、`rule_outline_alignment.md`、`_epilogue.md`、`update_guidance.md`、`validation_suite/SKILL.md`、`ADR.md`。

## ADR 031: 目录重构 `planning/` → `practices/` 与结构化素材层
**Date**: 2026-03-26  
**Context**: `planning/` 作为中间目录层实质价值低——仅包含 `experiment_planning.md`、`project_brief.md` 和 `practices/` 子目录。`practices/` 才是核心内容载体，`planning/` 仅增加路径深度。同时，`materials/` 放在课程根目录而非 `practices/` 下，与实践活动的逻辑内聚性矛盾。此外，新引入的 Material 对象体系（8 种 type）需要 `_schema.md` 和素材目录有清晰的归属关系。  
**Decision**:
1. **`planning/` 消除**：`practices/` 直接提升为课程顶级目录。`experiment_planning.md` 和 `project_brief.md` 与 practice YAML 同级存放。
2. **`materials/` 归属**：从课程根目录移入 `practices/materials/`，与 YAML 定义逻辑内聚。素材路径使用 `practices/materials/W0X/...` 格式（相对于课程根目录）。
3. **Material 对象体系**：`_schema.md` 新增 8 种 Material Type 枚举（`poll`/`quiz`/`critique_card`/`tutorial_steps`/`dataset`/`code_template`/`case_study`/`comparison`），支持开放扩展。
4. **跨课程一致性**：两门课程（信息可视化、交互产品开发）同步执行重构。`/new_course` 模板中 `mkdir planning` 已更新为 `mkdir practices`。
5. **ADR 001 更新**：原"拆解计划层 `planning/`"重命名为"实践资源层 `practices/`"，语义不变。
6. **影响范围**：19 个文件、34 处引用完成同步更新（含 `.agent/` 规则/工作流/索引/ADR/依赖图 + 课程 `course.yaml` + 项目文档）。`/update_guidance` §C 审计发现并修复 1 处遗漏（`design_practice.md` L52）。

**变更文件**：两门课程的 `course.yaml`、`practices/` 目录（物理迁移）、`_schema.md`、`W01_practice.yaml`、`rule_practice_design.md`、`rule_document_boundaries.md`、`design_practice.md`、`write_phase1_prep.md`、`audit_deep.md`、`new_course.md`、`INDEX.md`、`DEPENDENCY_MAP.md`、`ADR.md`、`README.md`、`ARCHITECTURE.md`、`CONTRIBUTING.md`。

## ADR 032: 视觉资产零冗余渲染合并范式 (V3)
**Date**: 2026-03-28
**Context**: 历史遗留的 `[VISUAL]` 块中，图片的配置被割裂为两行：`> **Asset**: path` 用于数据定义，`> **Preview**: ![预览](path)` 用于在 IDE 内触发原生渲染。这种模式不仅产生严重的视觉信息冗余，而且在旧版生成脚本追加 `Preview` 行时，容易因为散乱的注释而打乱 Markdown 无序列表的缩进排版结构，甚至剥落了 `*` 号，引发游标崩溃。随着 Python (`script_parser.py`) 与 JS (`ppt_parser.js`) 两套核心解析引擎此前均已升级并接装了自动剥除了 Markdown 图片语法的清洗滤镜引擎，独立 `Preview` 字段的存续已无必要。
**Decision**:
1. **废绝 Preview 字段**：彻底从体系中剔除原先用于补丁显示的 `Preview` 专用配置行，清扫历史残存量。
2. **Asset 升级为单行渲染体 (Zero Redundancy)**：物理存在的配图，直接将原本只有文字路径的 `Asset` 字段通过就地合并替换升级为 Markdown 图片语法格式：`> *   **Asset**: ![预览](../visuals/assets/<path>)`。
3. **解析器无缝解耦**：底层解析器在读取到这串看似复杂的符号时，将自动利用正则滤去头尾壳，抽取中间极其干净的业务逻辑路径，供应给 H5 平台及 PPTX 装配器使用——达成“人类面前所见即所得图鉴展现”与“底层管道干净传输路径”的极限融合。
4. **强行对其排版**：对原先诸如无端缩减为 `> **Asset**:` 或等排版丢失病灶进行强制格式对其，重塑回标准游格式 `> *   **Asset**:`。
5. **指导手册级联刷新**：同步删除 `SKILL.md` 中有关预览辅助字段的定义，修改 `/generate_assets.md` 标准回写执行规章。

**变更文件**：`script_format/SKILL.md`、`workflows/generate_assets.md`、22 篇现有讲义、`ADR.md`。

## ADR 022 V3 源码与构件隔离架构 (Build & Engines Separation)

**状态**: 已接受
**时间**: 2026-03-28
**上下文**: 
旧有架构中，工作区根目录的生成脚本存放区被命名为 `delivery/`，而在各门课程的目录下，由于历史原因同样生成名为 `delivery/` 的产物汇总文件夹（存放被编译打包成形的幻灯片和网页应用）。这导致典型的“语义/命名污染”，并在后续迭代中致使代码混杂。另外，存放语音的 `tts/` 与教务材料 `Output/` 同属冗余命名。
需要彻底切分“源码引擎”和“分发构件”，防止工作空间内的历史债务累积。

**决策**: 
实施 V3 工程级隔离策略：
1. **工作区中央统筹层**：原用于存放系统级工作流核心处理脚本（PPT 和 H5 生成代码）的 `delivery/` 固定重命名为 `engines/`，强调其构建引擎本质。
2. **项目局部数据层**：
   - 全面抛弃课程级内部的 `delivery/` 与 `tts/`。引入标准的 `build/` 隔离环境。所有幻灯片与页面编译输出放入 `build/presentations/` 与 `build/h5_preview/`。纯粹由机器可一键再生的资料统统归入 `build/` 环境。
   - 大写的传统教务材料目录 `Output/`（用于上级检查、归档的稳定材料，非程序输出物）被统一改名为 `admin/`，与源文件 `weeks/` 及构件文件 `build/` 保持同级与平行的全小写美学。

**影响**: 
- 项目具有严格的四层生命周期分离机制：`weeks/` 源码数据资产、`admin/` 外部教务规约、`engines/` 中央处理器、`build/` 输出结果展示。
- 各系统生成脚本及 Agent `[@/update_guidance]`, `[@/new_course]` 已全面剥离对 `delivery` 关键词的寻址能力，形成完整的认知闭环。

## ADR 033: V5 Package 架构演进与相对路径同步机制

**状态**: 已接受
**时间**: 2026-03-29
**上下文**: 
随着单体逐字稿字数超越万字界限，IDE Agent 经常遇到严重的 token overflow 和上下文丢失，严重拖累 H5/PPT 自动化链路的稳定性。此外，为了维持原生 Markdown 渲染器的图片显示效果，V4 架构中 `script_compiled.md` 的摊平策略导致深层引用（如 `_segments/M05.md` 内的图片路径）集体断链，且在根目录下散落杂乱的中间文件。

**决策**: 
实施 V5 Package 架构化升级：
1. **彻底摒弃单体入口**：废除原有的 `script.md` 单体文档记录法，全面使用 `package.yaml` 作为周课时（`W0X`）的专属模块装配器（索引中心）。
2. **源码收敛区 (`src/`)**：所有切片化的子核心语料如 `M01.md`, `M02.md` 被强制隔离并存放至新设立的 `src/` 深层池。
3. **隔离编译区 (`.build/`)**：引擎（`dumptext.py`）跑出来的中间组装物如 `compiled.md` 强制降落至专用的隐藏隔离舱 `.build/` 下。并且将该目录加入工作空间的 `.gitignore` 黑名单中。
4. **统一物质资源仓库 (`public/`)**：前端规范入骨！一刀切重命名原有松散的 `assets/` 给定名称为更符合 Web 标准的综合库 `public/`（涵括图像/视频/读本/源码实验物）。
5. **结构学寻址魔法（相对路径同步）**：极度精妙的建筑学解法！不再依赖不可靠的 AST 插件对内部图链进行编译改写，而是规定由于 `src/*.md` 的同级兄弟正好是 `.build/compiled.md`，从这两处读取图片的语法永远都是绝对一致的 `../public/...`。并且后端引擎会自动剥离 `../` 逃逸前缀，达成完美的前后端兼融。

**影响**: 
- `write.md` / `audit.md` / `routing_rules.md` / `/new_course` 及相关验证/组装 Python 及 JS 引擎链路全面向新架构对接。
- 极大避免了核心源文件提交时被非原生代码渣滓污染的问题。

## ADR 034: 字数预算校验机制优先级反转与显式契约 (Budget Priority Inversion)

**状态**: 已接受
**时间**: 2026-03-29
**上下文**: 
原有的 `validate_script_length.py` 在计算模块预算（Budget）时，依赖于从 Markdown 标题（如 `## Module 4 (80 分钟)`）通过正则提取时间并自动减去探测到的 `[ACTIVITY]` 内部时间。这种“隐式提取”导致了致命的系统性漏洞：遇到实践活动并不包裹在专门的块结构中、甚至整整一个模块就是大工坊的情况下，脚本会因为无法剔除活动时长，错误地将 60~80 分钟全数计算为高密度口语讲授要求，导致模块预期字数狂飙至一万字以上（全线报错）。同时，早就在写作期由 `inject_budget.py` 或者人类指定并声明在模块开头的准确标量 `<!-- BUDGET: 3600 chars -->`，反倒被降级为标题解析失败时的备胎，导致真实业务设计的约束力失效。

**决策**: 
实施验证器底层计算优先级翻转（Priority Inversion）：
1. **显式契约绝对优先**：将读取 `<!-- BUDGET: X chars -->` 的匹配行为设定为 P0 级最高权重。只要该语句存在，验证器将无条件采纳该标量作为当前模块考核的最终字符基线要求。
2. **被动回退（Fallback）**：仅在文件缺失显式注释标签的情况下，才被动降级去解析标题的括号分钟数并扣减活动时长。
3. **彻底活动豁免逻辑修正**：明确 `BUDGET: 0 chars` 代表该区域属于纯粹的实操实践免检时段（Exempt），防止该模块被错误地标记为验证失败（❌）。

**影响**: 
- `validate_script_length.py` 内部核心权重已强行翻转重连。
- M05、M06 等包含大规模工坊演练环境的宏观模块，将不再承受极其荒谬的时长字数通胀红线。

## ADR 035: 审计工作流 Token 浪费修复——统一 `--week` 过滤注入

**状态**: 已接受
**时间**: 2026-03-30
**上下文**:
当用户审查特定周次（如 W01）或特定模块（如 M03）时，审计流程仍全课程全量扫描，产生约 20,000-35,000 tokens 的无关输出（目标内容的 2-3 倍）。根因分析识别四个系统性缺口：(1) 6 个验证脚本中仅 `validate_script_length.py` 支持 `--week` + `--module` 双重过滤；(2) `validate_project.py` 在周次级审计中仍运行所有 7 个子验证器（含全局性的 sync_syllabus 和 validate_knowledge）；(3) `audit.md` 工作流模板未参数化过滤变量，Agent 无法确定性地在命令中追加 `--week N`；(4) V5 架构下 Agent 手动检查被迫读取整周 compiled.md（~150KB），约 85% 与目标模块无关。

**决策**:
1. **`script_parser.py` 基础层扩展**：新增 `list_script_files_for_week(scripts_dir, week_num)` 函数，V5 架构下仅编译指定 `W0N_*` 单个子目录，避免触发全部周次的 `_auto_compile_week`；新增 `filter_files_by_week(files, week_num)` 通用过滤器。
2. **4 个验证脚本统一添加 `--week N`**：`validate_spec.py`、`validate_visuals.py`、`check_draft_status.py`、`validate_project.py` 均新增 `--week` 参数，调用基础层函数实现过滤。
3. **`validate_project.py` 智能跳过**：`--week` 模式下自动跳过全局验证器（`validate_steps`、`sync_syllabus`、`validate_knowledge`），仅运行与特定周相关的验证器（spec、visuals、script_length、package），并将 `--week` 传递给子验证器。
4. **`audit.md` 工作流参数化**：新增 Step 0 范围解析，定义 `{SCOPE}`/`{WEEK_FILTER}`/`{MODULE_FILTER}` 三个模板变量。后续所有脚本命令统一携带 `{WEEK_FILTER}` 占位符。
5. **V5 模块级聚焦指令**：audit.md Standard 级别新增聚焦规则——Agent 手动检查（Part A-E）在模块级审计时直接 `view_file` 读取 `weeks/W0N_xxx/src/M0X_xxx.md` 源文件，禁止读取整周 compiled.md。

**影响**:
- 审计单周预计节省 ~65% tokens，审计单模块预计节省 ~80% tokens。
- 全课程审计行为完全向后兼容（不加 `--week` 时行为不变）。
- `INDEX.md`、`validation_suite/SKILL.md` 已同步更新。

**变更文件**：`script_parser.py`、`validate_spec.py`、`validate_visuals.py`、`check_draft_status.py`、`validate_project.py`、`audit.md`、`validation_suite/SKILL.md`、`INDEX.md`、`ADR.md`。

## ADR 036: H5 引擎片段渲染与源映射回馈 (Phase 6)

**状态**: 已接受
**时间**: 2026-04-01
**上下文**:
H5 预览系统的 `copy-locator-btn`（Phase 5 引入）的 `srcPath` 指向 compiled.md 而非源文件，Agent 需经过「compiled.md 行号 → BEGIN/END 标记定位 → 源文件名 → 源文件行号换算」四步间接跳转才能定位源码进行修改。此外，开发迭代单个 `M0X.md` 片段时仍需全局编译（`dumptext.py` 拼合所有模块生成 compiled.md），即使只改了一个段落也要重走完整管线，分钟级的反馈延迟严重拖慢写作→预览→修正闭环。

**决策**:
1. **新增 `--fragment` 模式**：CLI 新增 `--fragment` 参数，直接解析单个 `M0X.md` 源文件（`skip_compile=True`），跳过 `dumptext.py` 编译。所有生成的 `srcPath` 天然指向源文件精确行号，Agent 可一步定位。
2. **源映射后处理 pass**：新增 `_build_source_map()` + `_apply_source_map()` 两个解耦函数——前者解析 compiled.md 的 `<!-- ### BEGIN src/M0X.md ### -->` 标记构建行号映射表，后者将 manifest 中所有段落的 `srcPath/srcLStart/srcLEnd` 从 compiled.md 行号回馈为源文件行号。正式模式（`--all` 和单讲模式）同样自动受益。
3. **零破坏向后兼容**：`blocks_to_h5_json()` 签名和逻辑完全不变。`--all` 和单讲模式行为 100% 兼容。`dumptext.py`、`script_parser.py`、前端组件均未修改。
4. **隐式依赖链**：源映射正则 `r'^<!-- ### BEGIN (.+?) ### -->$'` 依赖 `dumptext.py` 的标记格式。标记格式变更时 `_build_source_map()` 会 graceful degradation（映射回退为空列表，`srcPath` 降级回指向 compiled.md），不会崩溃但 copy-locator 精度悄然退化。

**影响**:
- Agent 的 `/h5` 工作流新增模式 C（片段模式），修改→渲染→验证闭环从分钟级缩短到秒级。
- `DEPENDENCY_MAP.md` 需新增 `dumptext.py` BEGIN/END 标记 → `generate_course_h5.py` 源映射的隐式依赖。

**变更文件**：`engines/generate_course_h5.py`、`.agent/workflows/h5.md`、`.agent/memory/ADR.md`、`.agent/DEPENDENCY_MAP.md`、`.agent/workflows/update_guidance.md`、`.agent/rules/rule_asset_management.md`。

## ADR 037: H5 热重载系统 — Vite Plugin + WebSocket 闭环 (Phase 7)

**状态**: 已接受
**时间**: 2026-04-02
**上下文**:
ADR 036 引入的 `--fragment` 模式将修改→渲染闭环缩短到秒级，但仍需手动运行 Python 命令和手动刷新浏览器。第一性原理分析识别三个断裂点：(1) 文件保存事件无法自动传递到 Python 引擎；(2) Vite 的 HMR 机制**不适用于 `public/` 目录的静态 JSON 文件**（仅作用于 `src/` 下的模块代码），即使 JSON 已更新浏览器也不会收到通知；(3) `--fragment` 模式仅渲染单模块，与 LessonViewer 读取的完整教学周 JSON 路径不匹配——LessonViewer 从 `/courses/<courseId>/<weekName>.json` 加载，而 fragment 输出到 `/courses/<courseId>/fragments/<moduleName>.json`。

**决策**:
1. **新增 `--rebuild-week` CLI 模式**：从变更的 `.md` 文件路径反推所属教学周目录（`src/M0X.md` → `weeks/W0X/`），调用已有的 `generate_single_script()` 重建完整教学周 JSON（含编译 + 源映射），写入 LessonViewer 兼容的 `/courses/<courseId>/<weekName>.json` 路径。同时向后兼容写入 `slides.json`。实测重建耗时 ~300ms。
2. **Vite 自定义插件 `h5HotReload()`**：在 `configureServer` 钩子中将所有课程的 `weeks/` 目录加入 Vite 的 chokidar watcher。仅拦截 `<course>/weeks/<week>/src/*.md` 模式的文件变更（正则过滤），经 500ms 防抖后 spawn Python 子进程执行 `--rebuild-week`。包含并发锁防止同时重建、进程错误捕获。
3. **WebSocket 自定义事件通知**：Python 进程成功后通过 `server.ws.send({ type: 'custom', event: 'h5:reload', data })` 推送通知（不依赖 Vite 原生 HMR——它对 `public/` 静态文件无效）。失败时推送 `h5:error` 事件。React 端通过 `import.meta.hot.on('h5:reload', handler)` 接收并自动 re-fetch JSON。
4. **浏览位置保持**：热重载后通过 `useEffect` 钳位机制将 `currentSectionIdx` 和 `currentSlideIdx` 限制在新数据的有效范围内，避免因 section/slide 数量变化导致越界白屏。
5. **错误容错**：Python 解析失败时浏览器显示错误 toast（红色背景，5 秒消失），保留最后一次有效状态的 UI 内容不被覆盖。
6. **H5 模板与实例双写**：变更同时应用于 `engines/h5_template/`（模板目录）和 `build/h5_preview/`（运行实例），模板通过 `_sync_template_to_instance()` 确保未来新实例继承热重载能力。
7. **环境变量可配**：`H5_WATCH_MODE=fragment` 可降级为片段模式（更快但丢失整周上下文）、`H5_PYTHON` 指定解释器、`H5_DEBOUNCE` 自定义防抖。

**影响**:
- `npm run dev` 一次启动即同时激活前端 HMR 和 Markdown 热重载，开发者无需管理额外进程。
- 编辑→预览闭环从"手动三步"（运行 Python → 等待 → 刷新浏览器）缩短到"保存即看到"（Ctrl+S → ~1s 自动刷新）。

**变更文件**：`engines/generate_course_h5.py`（`run_rebuild_week()` + CLI 路由）、`engines/h5_template/vite-plugin-h5-hot-reload.js`（新建）、`engines/h5_template/vite.config.js`、`engines/h5_template/src/pages/LessonViewer.jsx`、`engines/h5_template/src/App.jsx`、`.agent/workflows/h5.md`、`.agent/memory/ADR.md`。

## ADR 038: H5 Craft-room 实时审计系统与双管线验证架构

**状态**: 已接受
**时间**: 2026-04-03
**上下文**:
随着 H5 热重载能力（ADR 037）的完善，我们希望在创作过程中实现“边写边审”（Craft-room 工作台模式）。以前的审计报告依赖命令行静态输出，割裂了心流状态。为了提供直接的交互式反馈，前端需要实时看到断链警告、字数预算预警、填充热力图，甚至是 Agent 的语义批注。
但这面临三个核心挑战：
1. **性能冲突**：现有的 Python 验证端包含极其复杂的解析逻辑提取，每次调用需数秒，不能直接混入 HMR 热重载进程（其耗时须在 ~300ms）。
2. **状态闪烁**：持续保存时频繁重刷验证界面会导致组件在红（Error）、黄、绿间闪烁、抽搐。
3. **批注漂移**：传统的行号锚点在文段持续增删和拆分合并的热加载阶段极其脆弱。

**决策**:
1. **P0 / P1 双管线异步引擎**：将热重载 H5 构建一分为二——`P0 渲染管线`（~300ms）通过 `generate_course_h5.py` 只负责内容生成和 DOM 变动推送，让内容优先上屏；随后触发在 Node 侧起异步子进程进行的 `P1 验证管线`（~2000ms），调用新建的综合入口 `validate_runner.py`。
2. **WebSocket 状态推送与门控分发**：P1 验证产物（JSON）通过新 WebSocket 事件 `h5:validation` 下发；在 Python 端引入了 `Q3 严重门控` 功能，例如字数太少时折叠后传的图片审计环节。
3. **ValidationContext 心流保护机制**：React 前端新增 ValidationProvider 接管验证数据。如果前端接收到频繁的 `h5:reload`，会抛出 `isInFlow=true`，进入心流冻结保护期（延时 2 秒），防止警告层频繁弹脸；在这期后淡入最新的数据。
4. **组件可视化大升级**：将原组件升级为四大核心交互层：HealthDot (全局脉搏)、DurationGauge (实虚时间差指示器)、ValidationOverlay (侧边抽屉热力详情) 以及直接使用 `vscode://file` 协议打通 H5 和 IDE 视角的定位直跳锚点。
5. **指纹引擎替代行号绑定**：引入无依赖的 DJB2 哈希引擎，对段落全文计算哈希并附加文本长度后缀（格式 `hash_len`，如 `d075f24e_24`），放弃行号，确保 Agent 批注如魔术贴般稳固吸附在动态编辑的文本上，并新增 Annotation 孤立区接收因大改而无家可归的批注。TTS 段落指纹采用相同算法，Python（`generate_course_h5.py`）和 JS（`fingerprint.js`）双端一致。

**影响**:
- 极大地丰富了开发者和审核者的在场体验感。
- React 前端成为 Python 原生验证报告的直观承载容器；该管线拓宽了向外集成任何后续 Validator 的能力。

**变更文件**：`engines/generate_course_h5.py`、`engines/h5_template/vite-plugin-h5-hot-reload.js`、`validate_runner.py`、`engines/h5_template/src/contexts/ValidationContext.jsx`、`engines/h5_template/src/utils/fingerprint.js` + 此相关衍生组件（`ValidationOverlay.jsx`, `AnnotationOverlay.jsx`, `HealthDot.jsx`, `DurationGauge.js`, `LessonViewer.jsx`）。

## ADR 039: H5 段落级动态 TTS 引擎与桥接安全加固 (Phase 8)

**状态**: 已接受
**时间**: 2026-04-05
**上下文**:
ADR 026.7 的音频管线依赖离线批量 TTS（外部工具合成 MP3 → aeneas 对齐生成 SRT → generate_course_h5.py 检测并写入 slides.json media 节点）。该流程存在三个系统性缺陷：(1) 需手动维护 MP3/SRT 文件，脚本每次修改都要重跑离线管线；(2) 音频粒度为整篇脚本而非段落，无法支持段落级按需播放/重录；(3) TTS 凭证需要人工从 doubao.com 提取并配置到 H5 中。在交接审计（cdb9996b 会话）中还识别出 11 项安全和架构漏洞，其中 `postMessage('*')` 通配符凭证泄漏为最高危。

**决策**:
1. **弹窗桥接架构**：H5 不直连豆包 WebSocket（被 Origin 拒绝），而是通过 `doubao.com` 弹窗中的 `tts_bridge.user.js` 油猴脚本中继。桥接脚本调用原版 userscript 暴露的 `window.tts()` API（回退路径：`window.ttsSingleChunk()`），音频以 `Transferable ArrayBuffer` 零拷贝传输回 H5。
2. **凭证安全交换（V-01 修复）**：弹窗端不再使用 `postMessage('*')` 通配符推送凭证，改为白名单候选 origin 逐一尝试（`localhost:5173/5174/3000`）。H5 端同时以 2 秒间隔主动轮询 `h5_tts_request_credentials`，双保险确保跨域场景下凭证交换。
3. **段落索引为 UI 主键（V-06 重构）**：`segmentMap` 从以 `ttsFp` 为键改为以段落索引为键。相同文本的段落拥有独立 UI 状态（播放/提取中/错误），但共享 IndexedDB 缓存（以 `ttsFp` 为键）。解决了重复文本段落的状态污染问题。
4. **增量 diff 防重灾（V2 抗偏移）**：`computeStatus()` 采用三层查找策略——(1) 索引+指纹精确匹配（零偏移场景）→ (2) 按指纹全局查找（处理插入/删除导致的索引偏移）→ (3) IndexedDB 缓存查找（含 V-04 新旧格式兼容回退和自动迁移）。编辑脚本后仅实际变更的段落需重新提取。
5. **指纹抗碰撞增强（V-04）**：DJB2 指纹格式从 `8位hex`（如 `e3b0c442`）升级为 `hash_len`（如 `e3b0c442_1280`），附加文本长度降低碰撞概率。Python（`_compute_tts_fingerprint()`）和 JS（`computeTtsFingerprint()`）双端一致。
6. **异常防阻塞（V-07）**：`extractAll()` 内每个 `extractSingle` 调用包裹 try/catch，外层 finally 确保 `isExtracting` 和 `extractProgress` 始终重置。单段失败不阻塞队列。
7. **Stale Closure 消除（V-08）**：引入 `segmentMapRef` 持有最新状态。`playSegment`/`stopPlayback`/`playAll`/`getStats` 改用 ref 访问，依赖数组清空，消除频繁重建。
8. **IndexedDB 缓存自清洁（V-05）**：`computeStatus()` 末尾异步执行 `cacheCleanup()`，清理超过 30 天且不在当前活跃指纹集中的孤儿缓存。
9. **BlobURL 内存管理**：旧 `segmentMap` 中不再被引用的 `blobUrl` 在 `computeStatus()` 中主动 revoke，防止内存泄漏。

**遗留项（BFF 重构方向）**：
- V-09/10/11（Cookie 泄漏、WebSocket 协议实现、HMR 递归冲突）属于 Backend-For-Frontend 本地代理架构范畴，待 doubao.com 弹窗方案稳定运行后启动。

**变更文件**：`.agent/skills/doubaotts/scripts/tts_bridge.user.js`、`engines/h5_template/src/contexts/TtsSegmentContext.jsx`、`engines/h5_template/src/components/TtsParaButton.jsx`、`engines/h5_template/src/components/TextPanel.jsx`、`engines/h5_template/src/utils/fingerprint.js`、`engines/generate_course_h5.py`、`build/h5_preview/src/utils/doubao-tts.js`、`.agent/workflows/h5.md`、`.agent/memory/ADR.md`、`.agent/DEPENDENCY_MAP.md`、`.agent/INDEX.md`。

## ADR 040: TTS 中间件 SSOT 统一与音频静态代理 (Phase 9)

**状态**: 已接受
**时间**: 2026-04-05
**上下文**:
ADR 037 Phase 7 创建 `vite-plugin-h5-hot-reload.js` 时，针对 `engines/h5_template/`（模板目录）和 `build/h5_preview/`（运行实例）采用双写策略。但 ADR 039 Phase 8 的 TTS 中间件仅被写入了 `build/h5_preview/` 版本，**引擎源码从未同步**。这导致任何从模板新部署的 H5 实例以及直接在 `engines/h5_template/` 下运行 dev server 的场景中，三条 TTS 关键 API 全部缺失：
1. `POST /api/tts/save` — 接收音频、写入本地文件系统
2. `GET /api/tts/manifest` — 返回指定周的 TTS manifest
3. `GET /courses/{id}/weeks/{week}/tts/*.aac` — 音频文件服务

前端的 `TtsSegmentContext.computeStatus()` 从 manifest API 获取段落状态时收到 404 HTML → JSON 解析失败 → **所有 178 个段落全部被标记为 `missing`**，且播放 URL 404 导致已提取的音频无法回放。

**决策**:
1. **SSOT 统一为 engines/**：`engines/h5_template/vite-plugin-h5-hot-reload.js` 确立为 TTS 中间件的唯一真相来源(SSOT)。`build/h5_preview/` 版本通过 `cp` 命令从前者同步。
2. **新增 TTS 音频静态代理中间件**：Dev 模式下 Vite 中间件拦截 `/courses/{courseId}/weeks/{weekName}/tts/{fp}.aac`，从 workspace 源目录（`{workspaceRoot}/{courseId}/weeks/{weekName}/tts/`）读取物理文件并流式返回。这消除了对 `publicDir` symlink 的依赖——build 版依赖物理文件+Vite publicDir 自动服务，引擎版走中间件代理，两者行为等价。
3. **DEPENDENCY_MAP 新增两条隐式依赖**：(a) 引擎版插件 → 部署版插件的同步约束；(b) `getTtsAudioUrl()` URL 格式 → 代理正则的匹配约束。

**影响**:
- 修复 TTS manifest/save/audio 三条 API 在引擎源码开发模式下的完全缺失。
- 后续新建 H5 实例（`_sync_template_to_instance()`）将自动继承完整 TTS 能力。
- `doubaotts/SKILL.md` 核心文件表路径已从 `build/` 修正为 `engines/`。

**变更文件**：`engines/h5_template/vite-plugin-h5-hot-reload.js`、`build/h5_preview/vite-plugin-h5-hot-reload.js`（同步）、`.agent/skills/doubaotts/SKILL.md`、`.agent/DEPENDENCY_MAP.md`、`.agent/memory/ADR.md`。

---

## ADR 041: 部署体系第一性原理与双门闸安全预检 (Phase 10)

**状态**: 已接受
**时间**: 2026-04-06
**上下文**:
在将 H5 引擎进行线上发布(Netlify)时，爆发了一连串的灾难级漏洞：
1. **源码暴露与历史污染**：`dist/` 1221 个生成的静态文件和 `.netlify/` (带 Netlify Site ID) 未被 `gitignore` 管控，直接被暴露在 public GitHub 仓库中，且单次 commit 新建 ~50MB 污染 Git Object Store。
2. **SSG 数据流断裂**：用户通过油猴桥接完成了数百段落的 TTS 获取（更新在 `tts/` 中），但没有重新执行完整的 `npm run build` 即进行了 `netlify deploy`。因缺失预检，结果造成数百音频文件和图片未能更新至线上。

**决策**:
1. **第一性原理重申 — 隔离性保护**：严格限制 `dist/` 与 `.netlify/` 等非原生环境临时态或涉密资产进入 Git 进行追踪。所有非本机的锁和产物都严禁共享，撤销 Git Index 的错误同步。
2. **第一性恢复 — lockfile 同步**：针对先前的反模式——将 `package-lock.json` 也直接 `gitignore` 化，要求立刻恢复并加入全局版本控制，以保障线上线下构建的严格等价和确定性 (Deterministic Builds)。
3. **双门闸防御架构 (Dual-Gate Deploy mechanism)**：为 `deploy_netlify.md` 注入强制的双层校验屏障：
   - **Step 0 门闸 (构建新鲜度预检)**：提取构建动作之前，遍历整个 Workspace 所有启用了生成的关联模块，核对音频 `*.aac` 与幻灯图 `*.png` 的物理修改时间戳是否在 `dist/index.html` 之前以杜绝遗漏重构。
   - **Step 2 门闸 (产物完整性验证)**：强断言 `dist/assets/media` 和 `dist/assets/tts` 中的子目录存在，并盘点 Webp/MP3 编译结果。
4. **Agent-Aware 防护墙**：定义 `rule_deploy_freshness.md` 被动探测部署心智。当触发 "deploy", "上线" 等意图时，智能调用双门闸检测而不是直接推向线上。

**影响**:
- 大幅收窄了构建层及仓库层的危险敞口，封锁了 `git_sync` 可能引起的 500MB+ 重灾区，重塑原子化 CI/CD 构建基础（为后续对接自动触发 Runners 铺平道路）。
- H5 线上预览与开发体验的等价性得到 100% 同构确保。不再发生"获取了但没播"的诡异问题。

**变更文件**：`.agent/workflows/deploy_netlify.md`、`.agent/workflows/git_sync.md`、`.agent/rules/rule_deploy_freshness.md`、`.gitignore`、`engines/h5_template/netlify.toml`、`engines/h5_template/src/components/SlideFactory.jsx`、`.agent/DEPENDENCY_MAP.md`、`.agent/INDEX.md`、`.agent/memory/ADR.md`。

---

## ADR 042: H5 前端原生多模态视频支持与字幕挂载 (Phase 11)

**状态**: 已接受
**时间**: 2026-04-11
**上下文**:
在 W01 添加 Dropbox MVP 实录视频时，原本试图直接在 Markdown `[VISUAL]` 的 `Asset` 字段内硬塞合法的 `<video controls...>` HTML 代码来驱动视频播放及字幕展示。但这直接导致底层正则/AST 解析器将其认定为异常路径并渲染毁损（抛出 404 及 `<a>` 未闭合导致的 key collision `Encountered two children with the same key`）。同时，原先引擎在遇到纯 `.mp4` 资源时，均采用一刀切的 `<img>` 分发，完全剥夺了用户的控制栏、播放体验与多模态特性。

**决策**:
1. **纯净 Markdown 壳回退 (Pure Frontend Decoding)**: Markdown 层不再允许复杂的 HTML5 代码插入，必须继续忠实遵守 `![描述](../public/videos/xyz.mp4)` 的干净图片壳协议语法。
2. **底层组件嗅探升级 (`AssetPlaceholder.jsx`)**: 在 H5 播放核心组件中增加对于 `slide.resolvedImage` 的拦截。若命中正则 `/\.(mp4|webm|ogg)$/i` 即可阻断原有图片渲染路线，主动装配标准的 `<video controls>` 原生播放器。
3. **衍生同源映射字幕轨 (Auto Subtitle Derivation)**: 根据 `.mp4` 源路径，自动猜测同名的 `.zh-Hant.vtt` 与 `.en.vtt`，将其组装到 `<track>` 中，以此避免对已有的后部 Node / Python 处理管线开刀也能达成精确的 CC (Captions) 功能渲染。
4. **模板级 SSOT 返现**：在确认修复 `build/` 环境下实时引擎的可行性后，将修复立即硬复制回退到唯一的真相源即 `engines/h5_template/src/components/primitives/AssetPlaceholder.jsx`，以造福今后所有的全局生成。

**影响**:
- H5 Preview 终于获得了强原生的多模态解析能力，完全避免后端 JSON Node 污染也能跑全功能视频实录。无缝解除了 HTML 污染 Markdown 的架构技术债。

**变更文件**：`engines/h5_template/src/components/primitives/AssetPlaceholder.jsx`、`.agent/memory/ADR.md`、`.agent/rules/rule_asset_management.md`。

## ADR 043: 实践规范 SSOT 重构与 concept_registry 独立化
**Date**: 2026-04-13
**Context**: 审计发现 `practice_schema.md` 要求 `weight`/`scoring_rubric` 必填，但 `rule_document_boundaries.md` 禁止在 practices 层定义计分参数（SSOT 在 course.yaml）。这导致存量 InfoViz practice.yaml 大量违规。同时 `theory_link.concept_id` 引用的 `concept_registry` 在 course.yaml 中不存在，`experiment_link` 为纯字符串无法机器验证。course.yaml 篇幅 51KB/~19.6K tokens，日常全量加载有 Token 溢出风险。

**决策** (R-1 至 R-6):
1. **R-1 计分归属**: 从 Schema 中废弃 `weight`/`scoring_rubric`（SSOT 严格在 course.yaml.assessment_methods），practice.yaml Phase/Homework 禁止出现这两个字段。
2. **R-2 概念注册**: 建立独立文件 `<课程>/concept_registry.yaml`（非 course.yaml 内嵌），作为 `theory_link.concept_id` 的唯一定义点，避免加重 course.yaml 的 Token 负担。
3. **R-3 Schema 版本**: 全局 `practice_schema.md` 升级为 v3.0 (SSOT)，本地 `_schema.md` 缩减为精简引用文件（~20 行），消除规范分叉。
4. **R-4 实验外键**: `experiment_link` 从 `str` 升级为 `list[int]`，直接绑定 `course.yaml.experiments[].id`，实现机器可验证的实践溯源。
5. **R-5 不拆分 course.yaml**: 日常工作流已通过 `extract_week.py` (ADR 021) 有效缓解 Token 溢出，拆分的迁移代价远大于收益。
6. **R-6 访问约束**: 日常高频工作流（/write, /audit Quick/Standard, /design_practice）禁止直接 `view_file` course.yaml 全文，必须通过 `extract_week.py` 提取局部。
7. **extract_week.py 扩展**: 新增 `--section experiments`、`--section practice-context`、`--include-concepts` 三种提取模式。
8. **theory_link 纯字符串格式废弃**: v3.0 起 `/audit_deep` 将纯字符串标记为 `[CA_LEGACY_FORMAT]` 错误。

**影响**:
- 彻底解决 `practice_schema.md` ↔ `rule_document_boundaries.md` 的 SSOT 内战。
- InfoViz 7 个 practice.yaml 需批量清理违规字段。
- IPD 实践层可在新 Schema v3.0 下从零规范化建设。
- concept_registry.yaml 可在 `/write` 工作流中增量维护。

**变更文件**：`.agent/templates/practice_schema.md`、`.agent/rules/rule_document_boundaries.md`、`.agent/rules/rule_practice_standards.md`、`.agent/workflows/design_practice.md`、`信息可视化/practices/_schema.md`、`交互产品开发/practices/_schema.md`(NEW)、`交互产品开发/concept_registry.yaml`(NEW)、`信息可视化/concept_registry.yaml`(NEW)、`*/extract_week.py`。

**修订 (2026-04-13 加固审计)**:
9. **R-7 Glob 覆盖加固**: `rule_document_boundaries.md` 和 `rule_practice_standards.md` 的 globs 扩展覆盖 `**/weeks/*/practice.yaml`、`**/concept_registry.yaml` 等周级路径，确保编辑时自动加载边界约束。
10. **R-8 course.yaml 门禁规则**: 新建 `rule_courseyaml_access.md`（`trigger: glob`, `**/course.yaml`），Agent 打开 course.yaml 时自动注入 R-6 访问约束提醒。
11. **R-9 concept_registry 写回协议**: `/write` Phase 3 新增 Step 3.95，校验阶段自动扫描新写模块中的概念并回写到 registry。
12. **R-10 Practice 冒烟检查**: `/audit` Standard 级别新增 Part P，在日常审计中执行 SSOT 越界 + experiment_link 类型 + theory_link 格式的轻量检查。
13. **R-11 validate_practice.py**: 新建自动化验证脚本，覆盖 Schema v3.0 的 10 条校验规则，集成到 `validate_project.py` 统一入口。
14. **R-12 extract_week.py SSOT 模板**: 从课程副本提升到 `.agent/templates/` 作为 SSOT，`/update_guidance` §G6 定义跨课程同步协议。

**追加变更文件**：`rule_courseyaml_access.md`(NEW)、`write_phase3_verify.md`、`audit.md`、`validate_practice.py`(NEW)、`validate_project.py`、`update_guidance.md`、`DEPENDENCY_MAP.md`、`INDEX.md`、`templates/extract_week.py`(NEW)、`templates/course.yaml.template`。

## ADR 044: `[VISUAL]` 纯文本资产伪字段防范与提取逻辑刚性化
**Date**: 2026-05-28
**Context**: 在修改 M02 脚本新增实验环节（代码块）时，Agent 错误地创造了不存在的 `> *   **Code**:` 伪字段，并将原生 Markdown 代码块裹挟在引用块内部（即 `> ```javascript`）。其根因在于 `script_format/SKILL.md` 第 134 行存在自相矛盾的表述（错误地暗示了存在 `Code` 字段）。这一系统性幻觉导致解析器无法读取视觉素材，破坏了“纯正 Markdown 文本与引擎剥离式处理”架构理念。
**Decision**:
1. **彻底封杀伪属性创造**：严禁在 `[VISUAL]` 块中创造类似 `Code`、`Diagram` 的自定义字段去包裹内容。
2. **文本资产必须脱离引用块 (De-Quote Protocol)**：任何意图作为 `[VISUAL]` 素材在 PPT/H5 上展示的结构化文本（如 Markdown 代码块、Mermaid、表格），**必须**脱离 `>` 引用符，平铺并紧接在 `[VISUAL]` 块结束后。
3. **修复 SKILL 矛盾点**：移除 `script_format/SKILL.md` 中关于“使用 Code 字段”的错误陈述，统一切换为“下方关联原生代码块”。
**影响**:
- 强化了 H5 解析端获取 `assetType` 与 `assetContent` 的底层鲁棒性。
- 防止未来 Agent 再次因规范文件的自相矛盾而脑补出不合法的配置项。

**变更文件**：`.agent/memory/ADR.md`、`.agent/skills/script_format/SKILL.md`。

## ADR 045: 课程加载器 Fail-Fast 与实验学时独立对账 (SSOT Phase 2)
**Date**: 2026-06-10
**Context**: 在“实验文档 SSOT 架构重构”的四方博弈审计中，发现 `course_loader.py` 在排序遇到非数字 ID 时存在静默失败（try-except pass），导致输出乱序。此外，为保障单源数据向下兼容，`load_course_section` 内部混合了旧版读取和动态实验兜底逻辑，增加了架构不确定性。教务端接收到未阻断的残缺/乱序数据后往往直接崩溃。
**Decision**:
1. **统一兼容边界**: 清理 `course_loader.py`，移除 `load_course_section` 中的旧版动态读取兜底逻辑，保证全量加载和局部加载行为严格一致。
2. **底层加载 Fail-Fast**: 使用正则表达式严格提取 `exp_id`。如果提取失败或完全缺失，强制抛出带有文件名的 `ValueError`，在数据管道最初端立即阻断构建进程，绝不隐式放行。
3. **独立学时验证**: 将全局学时对账业务剥离出通用 Loader。在根目录新建 `validation-suite/check_experiment_hours.py`，负责累加所有 `exp_*.yaml` 中的 `hours`，与 `course_meta.yaml` 进行严格对账。同时将其挂载到统一检查入口 `validate_project.py`。
**影响**:
- 数据不合规的课程在编译起点就会立即抛错并挂起，防止烂数据流向渲染层。
- Loader 职责回归纯粹读取（不再越权清洗或计算学时），学时对账业务转移至外部专业检查链。

**变更文件**：`course_loader.py`、`validation-suite/check_experiment_hours.py`、`.agent/skills/validation_suite/scripts/validate_project.py`、`.agent/skills/validation_suite/SKILL.md`、`.agent/memory/ADR.md`。
