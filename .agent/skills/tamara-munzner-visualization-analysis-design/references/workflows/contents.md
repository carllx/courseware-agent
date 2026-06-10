# 可视化分析与设计：核心框架与工作流 (Visualization Analysis & Design: Core Framework & Workflow)

## Prerequisites & Context (前提条件与上下文)

**应用场景 (WHEN)**：
当需要设计可视化系统以增强人类的认知能力（Augment human capabilities），而不是用全自动计算模型完全替代人类决策时。特别适用于探索性分析、需求尚未完全明确、或需要人为判断（Human-in-the-loop）的复杂数据场景。

**核心理念 (WHY)**：
- **避免盲目设计**：可视化设计空间极其庞大，大多数可能的组合对于特定任务往往是无效的。必须基于清晰的原则进行过滤。
- **转移认知负担**：利用精确设计的图像作为外部记忆（External representations），将人类内部认知和工作记忆的负荷转移到高带宽的视觉感知系统上。
- **任务与数据驱动**：以“What-Why-How”为核心分析脉络，确保视觉呈现不仅好看，更能切实支持目标任务。

> **理论深潜**：
> ```bash
> bash scripts/query_theory.sh "Why have a human in the loop vs purely computational approaches?"
> bash scripts/query_theory.sh "Why use an external representation and depend on vision?"
> ```

---

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

设计任何可视化系统前，请严格按照以下层级展开分析与定义。

### 阶段 1：确定人工干预的必要性 (Human-in-the-Loop Validation)
1. **评估决策自动化程度**：如果分析问题边界明确且可由机器学习或统计算法全自动解决，则**不需要**复杂的可视化设计。
2. **界定使用类型**：
   - **过渡性使用 (Transitional Use)**：在设计纯计算黑盒算法前，用可视化工具帮助研究人员探索数据特征、明确需求或调试算法参数。
   - **长期使用 (Long-term Use)**：旨在长期支持终端用户的科学探索、异常排查与模式发现。
   - **展示说明 (Presentation)**：向非专业观众展示、解释已有结论的数据事实。

### 阶段 2：执行 What-Why-How 分析框架 (The What-Why-How Framework)
所有复杂的可视化系统都应被拆解为该三元组及其链式序列 (Chained sequences of instances)。

![What-Why-How Analysis Framework](../../images/b45917b9fd715e686911222aeb90114d69b3fe3ece037df4336d2b70718e87fe.jpg)
*(图：可视化使用实例的三段式分析框架：用户看到什么数据、为什么使用该工具、以及如何通过设计选择构建视图)*

#### 2.1 "What"：数据抽象 (Data Abstraction)
必须剥离业务词汇，将其映射为底层数据抽象。
- **数据集类型 (Dataset Types)**：表格 (Tables)、网络/树 (Networks and Trees)、场 (Fields - Spatial/Grid)、几何体 (Geometry)。
- **属性类型 (Attribute Types)**：
  - **分类 (Categorical)**：用于区分身份（如地区、品种）。
  - **有序 (Ordered)**：进一步分为真实的**定量属性 (Quantitative)**（数值大小）和**定序属性 (Ordinal)**（小中大排位）。评估其是否有发散 (Diverging) 或循环 (Cyclic) 结构。
- **语义 (Semantics)**：区分**键 (Key, 自变量)**与**值 (Value, 因变量)**。

> **理论深潜**：
> ```bash
> bash scripts/query_theory.sh "Explain the difference between Key and Value semantics in multidimensional tables vs fields."
> ```

#### 2.2 "Why"：任务抽象 (Task Abstraction)
将用户的动作意图（Actions）和关心的目标（Targets）解耦。
- **动作 (Actions)**：
  - **高级 - 分析 (Analyze)**：消耗数据 (发现 Discover、展示 Present、享受 Enjoy) 或 产生数据 (注释 Annotate、记录 Record、派生 Derive)。
  - **中级 - 搜索 (Search)**：
    - 查找 (Lookup)：已知目标特征，已知位置。
    - 定位 (Locate)：已知目标特征，未知位置。
    - 浏览 (Browse)：未知具体目标，已知位置（在特定区域找满足特征的项）。
    - 探索 (Explore)：未知具体目标，未知位置（寻找全局未知模式）。
  - **低级 - 查询 (Query)**：识别单一目标 (Identify)，比较部分目标 (Compare)，或总结全部目标 (Summarize)。
- **目标 (Targets)**：
  - **所有数据**：趋势 (Trends)、异常值 (Outliers)、结构特征 (Features)。
  - **单个属性**：极值 (Extremes)、分布 (Distribution)。
  - **多个属性**：相关性 (Correlations)、依赖性 (Dependencies)。

![Chained Sequences](../../images/423079adb81cdf33eefe4a73cf5223433e9cfde34bec97a3a1e38a8d14f8095b.jpg)
*(图：可视化使用场景往往是由多个抽象任务实例级联而成的)*

> **最佳实践**：不要局限于原始数据。如果原始数据无法高效回答 Why，优先使用**派生动作 (Derive)**生成新属性再进行可视化展现。
> ```bash
> bash scripts/query_theory.sh "Provide examples of transforming domain-specific task descriptions into abstract action-target pairs."
> ```

#### 2.3 "How"：视觉编码与交互习惯 (Visual Encoding & Interaction Idioms)
进入具体的可视化图表与交互设计映射阶段。
- **核心法则**：定量数据必须映射到**量化通道 (Magnitude Channels)**（如对齐位置、长度）；分类数据必须映射到**身份通道 (Identity Channels)**（如空间区域划分、颜色色相）。
- **设计范式空间 (Design Space)**：
  - **空间排布 (Arrange)**：针对表格的排布、空间数据的映射、节点链接/矩阵的排布。
  - **映射通道 (Map)**：颜色通道与其他通道。
  - **视图操作 (Manipulate)**：导航、选择、随时间切换。
  - **多视图 (Facet)**：并列多视图 (Juxtapose)、分割数据到多视图 (Partition)、在同一空间叠加图层 (Superimpose)。
  - **数据缩减 (Reduce)**：通过过滤 (Filter) 与聚合 (Aggregate) 对抗信息过载。

### 阶段 3：嵌套验证模型 (Four Levels for Validation)
设计必须在对应的层级上进行防御性评估。
1. **领域情境层 (Domain Situation)**：验证是否误解了用户的真正需求。
2. **抽象层 (Task & Data Abstraction)**：验证抽象出的数据形态和操作是否能完美解答该领域的问题。
3. **视觉习惯层 (Visual Encoding & Interaction Idiom)**：验证当前的视觉表达法则（如散点图+刷选交互）是否真的比其他方法（如柱状图+下拉框）能更有效地传达目标信息。
4. **算法层 (Algorithm)**：验证渲染或数据转换算法是否满足实时性与资源约束。

> **理论深潜**：
> ```bash
> bash scripts/query_theory.sh "What are the common mismatches between the validation methodologies and the level of design claims in the nested model?"
> ```

---

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 用户抱怨屏幕太乱、遭遇严重的遮挡 (Occlusion) 或信息过载， 
  **THEN** 重新审视你的 How 设计。执行数据缩减 (Reduce items and attributes)，考虑使用过滤 (Filter) 或聚合 (Aggregate)，或者引入带交互的多视图系统 (Facet)。不要指望在一个视图内解决所有问题。
- **IF** 发现用户无法精准比较两个条目的数值差距， 
  **THEN** 检查是否错误使用了效能较低的通道（如颜色饱和度、面积）。改为将目标对比数据映射到**对齐的空间位置 (Position on common scale)**，并提供基准辅助线。
- **IF** 研究测试表明可视化系统的算法跑得极快，但用户在实际业务中依然不愿使用它， 
  **THEN** 说明在嵌套模型的高层（领域情境 Domain Situation 或 抽象层 Abstraction）出现了错位。必须后退到 阶段 1 和阶段 2，重新进行业务共情与需求抽象。
- **IF** 用户想寻找未知模式，但当前系统强迫他们一次只能看清几个节点， 
  **THEN** 这是缺乏 Explore 任务支持的表现。需要引入“Overview First, Zoom and Filter, Details on Demand”机制，或者设计专门聚合的视图。

---

## Verification Checklists (验证清单)

- [ ] **人工干预校验**：当前任务确实需要人类的模式识别或判断参与？不是一个全自动算法就能抛出结果的问题？
- [ ] **属性类型剥离**：是否已经将所有列的数据严格分类为 Categorical, Ordinal, 或 Quantitative，并搞清了 Key/Value 关系？
- [ ] **目标抽象匹配**：当前每个视图界面的功能，是否都能用规范的（Actions x Targets）动作目标对来进行描述（如 Explore + Outliers）？
- [ ] **数据派生考量**：在做复杂的视觉设计映射之前，是否评估过：直接根据原始数据派生 (Derive) 出一个新的关键属性列会更省事？
- [ ] **通道效能法则检验**：分类数据是否严格绑定在身份通道（色相、空间分区）上？连续定量数据是否使用了高排名的量化通道（位置对齐优先）？
- [ ] **嵌套验证对齐**：当你宣称设计的优点是“更符合直觉”时，是否安排了人为因素测试 (User Study) 而不是仅仅去测算法的帧率 (FPS)？