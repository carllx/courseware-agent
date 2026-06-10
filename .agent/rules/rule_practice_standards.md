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

## 三、 Merrill 首要原则校验 (First Principles of Instruction, Merrill 2002)

> **理论来源**：Merrill, M. D. (2002). *First principles of instruction*. Educational Technology Research and Development, 50(3), 43-59.
>
> **与 UbD 的关系**：UbD 解决"设计什么"（逆向推导交付物），Merrill 解决"设计得对不对"（正向校验教学完整性）。两者互补，不冲突。

在实践环节设计完成后，用以下五条首要原则进行交叉校验：

| # | 原则 | 校验问题 | 不合格信号 |
|:---:|:---|:---|:---|
| M1 | **问题中心** (Problem-centered) | 实践活动是否围绕一个真实的、完整的问题展开（而非围绕一个工具或知识点）？ | Phase 的 `description` 中只有工具名而无业务问题 |
| M2 | **激活旧知** (Activation) | 是否有环节让学生先调用已有经验/知识？ | Phase 列表中无任何 `warm-up` 或 `discussion` 类型 |
| M3 | **示范新知** (Demonstration) | 是否有环节展示"做对了是什么样"（而非只告诉规则）？ | 缺少 `demo` 类型的 Phase 或缺少教师示范步骤 |
| M4 | **应用练习** (Application) | 学生是否亲手操作（而非仅观看/填空）？ | `workshop`/`practice` 类型的 Phase 总时长 < 总时长的 40% |
| M5 | **整合迁移** (Integration) | 是否有环节让学生将新技能与旧知识/真实场景连接？ | `homework` 仅要求提交操作产物，无反思或迁移任务 |

---

## 二、 实践环节逆向设计三步法 (UbD Blueprint)

永远不要按照 "今天学什么工具" 顺向设计。
1. **锁定交付物**：学生这周最后到底交什么？（填死 `homework.deliverables`，比如 "带完整可解释性的交互图 H5 链接"）
2. **逆推活动流**：怎么做才能交差？从后往前推算每个 Phase（例如 P3 是部署、P2 是作图、P1 是找数据）。
3. **绑定理论锚**：这套动作背后证明了什么核心素养？填入精确的 `theory_link`。

---

## 三、 AI 时代后编程教学法：四大核心设计法则

编写实践活动时，必须严格遵守以下四条底层规律，确保实践课不仅是“工具操作”，而是实现专业认知的跃升：

### 3.1 人机接口定律：理论是控制机器的最高级语法 (Theory as Syntax)
*   **核心界限**：实践活动的意义在于**验证理论**。严禁设计脱离专业知识的“纯软件操作”或“口语化抽卡”环节。
*   **落实机制**：在 `practice.yaml` 中，`theory_link` 是强约束字段。实践活动的设计与 Prompt 编写，必须使用由 `librarian` 提取的真实教材/知识库理论词汇作为控制约束条件。如果不把专业理论当作最高级语法，学生就只是在“抽卡”而非“设计”。

### 3.2 技术的本质定律：控制权优先于自动化 (Control over Magic)
*   **核心界限**：教育的目的不是培养 AI 的旁观者，而是培养能对机器进行“精准微创手术”的驾驶员。
*   **落实机制**：在涉及 AI 自动生成（如自动出图、出代码）的实践环节后，**必须强制配套一个“降级干预 / 白盒排障”步骤**。例如，要求学生打开底层代码（如 JSON 结构、SVG 嵌套）去定点修改某个参数，以保证在 AI 失效时，学生仍具备最高控制权。

### 3.3 价值转移定律：从“工程实现”向“认知跃升”转移 (Insight over Spectacle)
*   **核心界限**：AI 抹平了环境配置和查错的时间，这些省下来的时间必须转化为认知价值。实践课的最高检验标准不再是“图表跑没跑通”。
*   **落实机制**：在实践作业或高阶实验的交付物（`deliverables`）中，不仅要求提交工程产物，还**必须要求提交一份“洞见陈述（Insight Statement）”**。例如：“通过这张图表，你看到了别人没看到的数据真相吗？”。可视化的本质是寻找意义，而非视觉堆砌。

### 3.4 认知阶梯定律：效率膨胀下的刻意降速 (Cognitive Scaffolding)
*   **核心界限**：AI 生产结果的速度远超人类消化速度，必须通过刻意降速防止学生认知超载。
*   **落实机制**：严禁设计“一键端到端生成”的黑盒流程。必须遵循教育心理学规律，将复杂的 AI 生成任务拆解成多个小步骤（Phase），并在每步设置中间校验态，控制变量。让学生在每一步都能看清“我改变了什么输入，引发了什么输出”。

---

## 变更检查单

- 修改 `.yaml` 后，检查原 `src/` Markdown 课件里的 `[ACTIVITY]` 引用块是否已同步。
- 确认 `experiment_link` 为 `list[int]` 格式（绑定 `course.yaml.experiments[].id`）。
- 确认无 `weight` 或 `scoring_rubric` 字段出现在 Phase 或 Homework 对象中（SSOT 在 course.yaml，ADR 043）。
- **强制闭环**：课表设计完成后，必须生成/更新出供学生直接调用的 `_Practice_Guide.md` 操作指南手册，严禁让学生直接对着 `yaml` 施工。
