# 可视化动作与四层验证工作流 (Query & Four Levels of Validation)

## Prerequisites & Context (前提条件与上下文)

在构建任何可视化 (Vis) 系统时，必须明确用户的查询目标 (Why) 以及可视化意图 (What)。为了确保可视化设计的科学性与有效性，必须通过**四层嵌套模型 (Four Nested Levels of Vis Design)** 自上而下进行分解与验证。上层设计错误将不可避免地级联导致下游方案失效，因此理解用户的高阶使用意图（如探索、展示或享受）是后续交互方式与算法选择的基石。

> **动态理论查询 (Progressive Disclosure):**
> 深入了解目标与模型的理论背景，请通过运行以下命令获取：
> - `bash scripts/query_theory.sh "可视化目标中 Discover、Present、Enjoy 分别有哪些经典用例？"`
> - `bash scripts/query_theory.sh "什么是可视化设计的四层嵌套模型（Four Nested Levels of Vis Design）？"`
> - `bash scripts/query_theory.sh "不同层级的验证方式（Validation Approaches）有何区别？"`

---

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### Step 1: 解构查询动作 (Deconstruct Query Actions)
在制定任何高级交互前，明确可视化任务中的三种核心基础查询动作：
- **Identify (识别)**: 识别单个目标的特征。
  ![](../../images/3f61e6ff15436f33f73faf5d1131e1208ece69aa9b03d8ccd26cf6e18871a261.jpg)
- **Compare (比较)**: 对比多个数据点或结构的异同。
  ![](../../images/f918b8641bbcdcd2b86e2e45fbc81e14103acbc6b30974bf2985a297bf569ac4.jpg)
- **Summarize (总结)**: 对整体数据集合进行概括。
  ![](../../images/2df91f7765755916794ea6bae0bf3e78a175b867adf61816dd785d6d326afe7b.jpg)

### Step 2: 明确用户的高级意图 (Identify User Intent)
可视化为何被使用？（Why does not dictate How）
- **Discover (发现)**: 用于产生新假设或验证现有猜想（经典科学探索）。该模式下，设计者无法提前预知用户需要查看什么。
- **Present (展示)**: 基于**已知的结论**进行简洁有效的数据叙事。输出内容通常是 Discover 环节的结果延伸。可用于决策制定、规划或教学。
- **Enjoy (享受)**: 满足好奇心和非强制性的探索体验。即使设计初衷并非为了“享受”，部分用户也可能以此目的使用。
  - *案例：Name Voyager（供探索趋势的享受型设计）*
    ![](../../images/089a76ca416e55d45cad1ce152888bdf1760eed76c3aae4f6baeb8cd25c7e7a2.jpg)
    ![](../../images/7d18d1b3301d6d548f9aeac0f16dc7303b2592c8bd38d2a8eca0e043b5f3e688.jpg)
- **Produce (生产)**: 基于现有信息生成新素材。包含 **Annotate (注释)**（给已有元素增加数据文本或图形）等操作。

### Step 3: 四层嵌套设计方法论 (The Four Nested Levels of Design)
为了规避庞大设计空间的无效探索，必须将设计划分为四层进行严格论证。
![](../../images/0fc39424f1826862f476b57448f53c5157b1cd058dcee887a6792a26cc7f4995.jpg)

1. **Domain Situation (领域情境)** 
   - 目标：分析目标用户的特定词汇、数据与工作流。
   - **启发式法则**: 绝不能主观臆测用户需求！应采用实地观察和上下文访谈 (Contextual inquiry) 定位问题。
   - ![](../../images/3e61542445b078a6687e5c2457d01c13a231d8d1cff932d589bb30219eab2909.jpg)

2. **Data / Task Abstraction (数据/任务抽象)** 
   - 目标：将特定的领域术语映射为抽象的数据结构与任务形态。
   - **启发式法则**: 问题需极其具体（如“相邻节点的差异是什么”），切忌假大空。
   - ![](../../images/3eada9a9635254c7ba3bbdb4bbf614be74273143d5a8924f07325b7ce7faee84.jpg)

3. **Visual Encoding / Interaction Idiom (视觉编码与交互习惯)** 
   - 目标：选择展示数据和控制交互的正确形态。
   - **启发式法则**: 评估多种候选编码形式，并以已知的视觉认知原则（Perceptual principles）证明该选择的合理性。
   - ![](../../images/484f5f53a626b1a4d5950c39ff453d622408ebd56e16a8c074ff9fecf4284878.jpg)

4. **Algorithm (算法)** 
   - 目标：以最高效的方式实例化上述的交互和视觉形态。
   - **启发式法则**: 不要仅关注数据规模（Data items），有些情况下也需要考虑屏幕上的像素规模。

### Step 4: 执行适时的验证方案 (Execute Validation Strategies)
每一层都面临不同的有效性威胁，验证手段分为即时验证 (Immediate) 和下游验证 (Downstream)：
![](../../images/bc7f32c9d1d45c184d66563f47a9fcb82a8b5d6c559de2992f25f90a1098f730.jpg)

- **Domain 层**: 实地考察 (Field study)、半结构化访谈 vs 下游验证工具的采纳率 (Adoption rates)。
- **Abstraction 层**: 在真实工作流中收集由目标用户尝试工具后反馈的轶事证据 (Anecdotal evidence)，或者部署工具后进行观测研究。
- **Idiom 层**: 认知启发式评估 (Heuristic evaluation) / 专家审查 vs 对照实验室研究 (Lab study, time/error metrics)、结果图像定性/定量分析。
- **Algorithm 层**: 计算复杂度分析 vs 下游对系统运行时间 (Wall-clock time)、内存占用的测量。

> **深潜提示**: 如果不熟悉特定案例如何运用这些验证方法，运行：
> `bash scripts/query_theory.sh "请解释 Genealogical Graphs 或 MatrixExplorer 的实际验证案例"`

---

## If/Then Troubleshooting Logic (故障排查与逻辑推演)

当可视化应用部署后遇到反馈不佳或结果谬误时，严格依据四层嵌套模型的**四大威胁 (Threats to Validity)** 向上溯源：
![](../../images/012079474f18ae9f0a3cbf9e4dc7b536558fbe8125104dd98d247c3b180dfef9.jpg)

- **IF 算法响应极快但用户却无法理解图表**：
  - **THEN** 问题大概率出在**编码层 (Wrong Idiom: 展示方式不起作用)** 或更上层的**抽象层 (Wrong Abstraction: 展示了错误的东西)**。首先进行启发式评估，检查是否有违反认知规则的设计，然后考虑开展 Wizard of Oz 原型测试。
- **IF 测试时一切完美，但部署后用户留存率（Adoption rate）极低**：
  - **THEN** 问题极大可能出在**领域层 (Wrong Problem)**。你可能误解了他们真正的需求，或该问题在其真实工作流中无足轻重。必须回退到实地访谈阶段 (Contextual inquiry)。
- **IF 在处理大规模节点-链接图时，图形变成了一团难以区分的“毛线团”**：
  - **THEN** 这属于编码层威胁，可参考 LinLog 案例：必须在算法要求中调整视觉编码，如强制使簇间边距大于簇内边距，并引入更好的拓扑评价指标。或者参考 MatrixExplorer 的案例，当图表变大变密时转为矩阵视图 (Matrix representations) 来消除视觉杂乱。
- **IF 发现系统响应经常呈现不可预测的滞后（超过毫秒级）**：
  - **THEN** 问题归属于**算法层 (Wrong Algorithm: 性能太慢)**。你需要分析计算复杂度，用基准测试集 (Benchmarks) 验证，并重构核心布局代码。

---

## Verification Checklists (验证检查清单)

执行任何可视化方案之前，请校验以下关键节点：

- [ ] **领域评估**: 是否与真实用户在真实工作环境中进行过实地观察与访谈（而非仅靠设计师单方面假设需求）？
- [ ] **意图归类**: 当前可视化界面的首要意图是 Discover (发现未知的假设)、Present (展示已知的故事) 还是 Enjoy (满足随便看看的好奇心)？
- [ ] **链式任务校验**: 若意图是 Present，是否确认用户已理解数据结论，或明确该数据是否是由上一次 Discover 操作的输出流转而来？
- [ ] **抽象转化**: 是否将模糊的领域问题准确转换成了结构化数据抽象，并定义了特定查询（Identify, Compare, Summarize）？
- [ ] **即时与下游验证闭环**: 针对四层嵌套设计模型的每一个层级，是否都明确并执行了相应的有效性防范（如针对编码层的实验室对照测试，针对算法层的时间基准测量）？
- [ ] **图像路径重写**: 所有展示的参考图片是否均已修改为基于 `workflows` 相对路径引用的格式（`../../images/`）？
- [ ] **渐进披露检查**: 文件中是否已将大量的课本枯燥理论替换为按需触发的动态执行脚本 (`bash scripts/query_theory.sh`)？