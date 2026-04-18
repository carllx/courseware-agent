---
description: 编辑 practices 或相关教程文档时自动激活，确保实践活动的规范对齐、数据闭环及 AI 教学法最佳实践落地。本规则整合了结构校验与设计心法。
trigger: glob
globs:
  - "**/practices/*.yaml"
  - "**/practices/*.md"
  - "**/weeks/*/practice.yaml"
  - "**/weeks/*/practice_guide.md"
---

# 实践教学规范与设计指南 (Practice Standards & Best Practices)

> 适用场景：编写实践手册、实验大纲、`/design_practice` 或 `/audit_deep` 时自动生效。本指南融合了 UbD（逆向设计）、CA（构建性对齐）与前沿 AI 教学法。

## 一、 结构与合规校验基准 (Structural Compliance)

### 1.1 `practice.yaml` 强制要素
1. **必须字段**：`week`, `title`, `total_minutes`, `theory_prerequisites`, `phases`, `homework`
2. **Phase 的基本素养**：每个阶段必须含 `id`, `name`, `minutes`, `type`（合法枚举参见 Schema）, `description`, `tools`, `deliverables`
3. **课时硬门槛**：`sum(phases[].minutes)` 必须精确等于 `total_minutes`，且对齐于 `course.yaml` 规定的实验课时上限（例如 `hours_practice × 45`）。

### 1.2 构建性对齐 (Constructive Alignment)
- **拒绝无效动作**：任何 "点鼠标照做" 的纯流水线缺乏价值。当 phase 类型为 `workshop`/`practice`/`critique` 时，**必须显式提供 `theory_link`**（结构化对象格式），且该 `concept_id` 必须命中 `<课程>/concept_registry.yaml`。
- **目标必须可见**：若教学目标是 "分析 (Analyze)"，设计中必须有拆解、对比环节（如 `critique`）；若目标是 "创造"，必须是半开放式的 `workshop`。

### 1.3 跨周数据生命追踪 (Upstream Dependencies)
当实践涉及连续数据流（例如 W01 做清洗，W02 做分析，W03 做可视化）时：
- 消费端（如 W02）必须在 `phases[].upstream_dependencies` 显式写入其数据源（如 `source: W01.P3`，`artifact: tidy_dataset.csv`），严禁仅在纯文本中描述。

### 1.4 素材存管合规与隔离墙原则 (Material Sandboxing)
- **物理隔离**：实践手册专用素材（数据集/填字图/测验卡等）**必须**存放在 `<课程>/practices/materials/W0X/`。
- **防止资产污染**：**严禁**把实践辅助图片塞入 `weeks/W0X/public/practice/`。`public` 目录属于 H5 前端引擎专用，不负责存储教学考评类沙盒文件。
- **引用范式**：在 `practice_guide.md` 中插入图片时，**必须**使用回溯路径引用沙盒文件：`![...](../../practices/materials/W0X/xxx.png)`。

---

## 二、 实践环节逆向设计三步法 (UbD Blueprint)

永远不要按照 "今天学什么工具" 顺向设计。
1. **锁定交付物**：学生这周最后到底交什么？（填死 `homework.deliverables`，比如 "带完整可解释性的交互图 H5 链接"）
2. **逆推活动流**：怎么做才能交差？从后往前推算每个 Phase（例如 P3 是部署、P2 是作图、P1 是找数据）。
3. **绑定理论锚**：这套动作背后证明了什么核心素养？填入精确的 `theory_link`。

---

## 三、 Vibe Coding 教学法参考基线与分层隔离带

编写涉及 "Vibe Coding" 或 AI 生成能力的模块时，**必须严格遵守教学阶段的能力隔离**，绝不允许将晚期工程概念（如 Cursor、代码审查）强植入早期认知课件中，避免引发学员认知崩溃。

### 3.1 分级实施原则 (Tiered Vibe Coding Adoption)

**【Tier 1: 概念启发与无代码期（适用 W01-W02 等初期教学）】**
*   **核心界限**：严禁在此阶段引入任何关于 `Cursor`、`IDE编辑器`、`代码Debug`、`底层代码参数审查` 的操作与强工程术语！
*   **教学形式**：仅限使用带有内置可视化渲染沙箱的对话式 AI 网页端（如 Claude Artifacts、ChatGPT Advanced Data Analysis ），或类似 RAWGraphs 等纯 GUI 无代码工具。
*   **训练目标**：体验“自然语言直出视觉结果”的魔法，建立批判性审查意识（如：通过肉眼对抗图表欺诈或截断零点），彻底屏蔽代码门槛。

**【Tier 2: 架构微操与极客沙盒期（适用 W03/W04 及之后涉及真实框架如 ECharts/D3 阶段）】**
*   **核心界限**：正式引入 `Cursor` / `Copilot` 等真实工程辅助代码流，允许开启底层白盒探索。
*   **训练目标**：培养“系统工程外包”视角。不再需死记语法，但学生在向 AI 下指令前，必须写出一份结构严密的 markdown 草图（包含业务逻辑、设计映射、防错兜底）。不培养"无情的 Prompt 复制机"。

### 3.2 体验痛点先行 (Let them feel the pain first)
**黄金法则**：AI 是为了解决具体瓶颈的救兵，不是直接取代学习的黑盒。
*   _实践设计_：先让他们用低效的工具阵列体验极大的修改成本（如纯手绘草图、Excel手工拉线），或面临深不可测的 Munzner 设计空间引发选择瘫痪；然后再引入 AI 编排工具进行降维打击，以此建立心智痛点锚点。

### 3.3 读大于写，修剪大于生成 (Reading & Pruning > Writing) *(仅限 Tier 2 阶段)*
*   **Debug 是第一生产力**。当进入代码生成沙盒期，所有的报错测试环节不是为了证明 "跑通了"，而是教学生如何识别 AI 的幻觉错误、精准缩小出错代码的边界定位，以及如老猎手一般教导引导 AI 自我纠错，而非全盘重写瞎跑。

---

## 变更检查单

- 修改 `.yaml` 后，检查原 `src/` Markdown 课件里的 `[ACTIVITY]` 引用块是否已同步。
- 确认 `experiment_link` 为 `list[int]` 格式（绑定 `course.yaml.experiments[].id`）。
- 确认无 `weight` 或 `scoring_rubric` 字段出现在 Phase 或 Homework 对象中（SSOT 在 course.yaml，ADR 043）。
- **强制闭环**：课表设计完成后，必须生成/更新出供学生直接调用的 `_Practice_Guide.md` 操作指南手册，严禁让学生直接对着 `yaml` 施工。
