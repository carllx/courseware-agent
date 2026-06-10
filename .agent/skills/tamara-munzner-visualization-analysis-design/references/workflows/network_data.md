# Workflow: 网络与树状数据结构可视化 (Network & Tree Data)

> **[Agent Action Required]** 根据目标规模、密度与交互任务，执行网络数据可视化策略与视觉编码推导。

## 1. Prerequisites & Context (前置准备与背景)

在处理网络（Network）与树（Tree）数据时，数据结构的复杂性往往伴随着高昂的可视化成本。本工作流旨在指导你如何根据**网络规模（Scale）**、**链路密度（Link Density）**以及**用户意图（Why: Tasks）**，选择或推导出最有效的视觉编码（Visual Encoding）策略。

**核心设计理念**：
- **连接（Connection）**：使用节点-链接（Node-Link）范式呈现直接的拓扑结构。
- **包含（Containment）**：使用空间嵌套（如 Treemaps）呈现多层级的属性与树状聚合。
- **矩阵（Matrix）**：使用邻接矩阵（Adjacency Matrix）在极高密度下完全消除线条交叉遮挡（Occlusion）。

> 💡 **深层理论查询**
> 当你需要理解节点-链接与矩阵视图在不同底层任务中的认知效率时，请执行：
> `bash scripts/query_theory.sh "What are the cognitive trade-offs and limits of node-link diagrams vs matrix views for network data?"`

---

## 2. Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 步骤 1：度量网络规模与密度 (Scale & Density Profiling)

在着手设计任何图表前，必须先量化数据集的规模与密度界限。
- **计算公式**：链路密度（Link Density） = 总链接数（Links）/ 总节点数（Nodes）。
- **分析依据**：
  - 如果是一棵标准树，其链路密度为 1。
  - 对于**节点-链接图**，其实用上限是链路密度小于 $4$（$L < 4N$）。
  - 若数据量为千级或万级节点，传统的力导向图（Force-Directed Placement）将不可避免地退化为视觉上的“毛线球（Hairball）”。

### 步骤 2：基于任务目标的编码策略选择 (Idiom Selection via Task Matching)

#### 模式 A：专注拓扑结构与路径追踪 (Topology & Path Tracing)
- **适用场景**：用户需要寻找最短路径、评估节点间的“跳数（Hops）”，或是探索局部邻域结构。
- **最佳实践**：采用**节点-链接布局（Node-Link Layouts）**。
- **警惕效应**：力导向布局是启发式算法，其节点间的物理临近性（Spatial Proximity）有时是由排斥力导致的“伪聚类（Artifactual visual clumps）”，而非强连接性。
  - 示例参考：
  ![](../../images/67b56107f23eb11c54a6eb1496732d43c77fa7ed063a93b396039ab8173dd33e.jpg)

#### 模式 B：稠密网络与聚类检测 (Dense Networks & Clique Detection)
- **适用场景**：图密度极高（达到数学极限 $N^2$），用户需要快速寻找派系（Cliques）、估算节点总数或进行节点属性的快速对齐。
- **最佳实践**：采用**邻接矩阵视图（Adjacency Matrix Views）**。
- **优势**：绝对的空间可预测性与稳定性。添加新节点不会导致整个布局的剧变，完全消除了线条交错带来的视觉混乱。
  - 矩阵与节点-链接对比示例：
  ![](../../images/cd08fc961b72b5c4be222b94b0f33261fcfc066a85fd325db63a6826b017ed00.jpg)

#### 模式 C：树状数据的叶子属性查询 (Querying Attributes at Leaf Nodes)
- **适用场景**：任务不侧重于拓扑路径，而是关注“分布”与“规模”（例如发现异常的巨大文件）。
- **最佳实践**：采用**基于包含关系的标记（Containment Marks / Treemaps）**。
- **实现细节**：将子节点完全包含在父节点的面积内，将定量属性映射到矩形的面积（Size / Area）上。
  - Treemap 示例：
  ![](../../images/276175e811b4fba43da756768954eb6a289ce2fb23498ed806e4eeaefcd3a91b.jpg)

### 步骤 3：运用高阶降维与层级衍生 (Advanced Reduction & Derivation)

当网络规模超出视觉承载极限时，必须进行数据抽象：
- **衍生定量属性过滤**：例如计算图的 Strahler number 中心性指标。过滤掉低权重的边缘节点，仅展示由高排位节点构成的核心“骨架（Skeleton）”。
  > `bash scripts/query_theory.sh "How does Strahler number summarization efficiently filter large network graphs?"`
- **构建复合网络（Compound Networks）**：提取网络中的聚类层次（Cluster Hierarchy）。在展示图布局时，组合使用“原始连接线”与“层级包含关系”来呈现多层次网络结构（如 GrouseFlocks 系统）。
  ![](../../images/f0f2f1ab1ee372914f59b58136b7f27939828dc8cffbd7902768cf9eb2cdf975.jpg)

---

## 3. If/Then Troubleshooting Logic (故障排除与逻辑分支)

- **[IF]** 节点-链接图变成了无法分辨的“毛线球（Hairball）”，出现大面积的遮挡（Occlusion）：
  - **[THEN]** 检查链路密度是否 $>4$。若是，强制切换至**邻接矩阵视图（Matrix View）**。若需保留连接属性，应引入多级缩放机制（如 multilevel sfdp 算法）或过滤不必要的边。
- **[IF]** 用户在矩阵视图中难以追踪两个节点之间的多跳路径（Multiple-link paths）：
  - **[THEN]** 承认这是矩阵视图的内生缺陷。提供混合协调视图（Hybrid Multiple-view），在主屏使用矩阵降噪，选中节点时在侧边栏渲染其局部节点-链接子图。
- **[IF]** 力导向图每次运行的结果都不一样（Nondeterministic layout），导致用户的空间记忆无法建立：
  - **[THEN]** 提供持久化或固定随机种子的机制；或者改用确定性的树形布局（如果数据可近似为树）及带有固定排序的矩阵视图。
- **[IF]** Treemap 难以展现深层的树层级关系，父节点界限模糊：
  - **[THEN]** 增加边缘的内边距（Padding）或使用颜色明暗渐变（Icicle/Sunburst布局）来强化包含层级。

---

## 4. Verification Checklists (验证清单)

在将方案交付给用户或投入生产环境前，请执行以下检查：

- [ ] **规模审查**：是否已经提取了数据的 Nodes 与 Links 数量，并显式判断了其是否在目标视觉范式（Idiom）的承载范围内？
- [ ] **任务契合度审查**：当前的编码选择是否符合核心业务痛点？
  - *寻找短路径 -> Node-Link*
  - *分析连通派系 -> Matrix*
  - *查找占用空间最大的子元素 -> Treemap*
- [ ] **视觉稳定性审查**：布局过程中的微小数据变动是否会引起全局结构的剧烈变动？（尤指不稳定的力导向图）。
- [ ] **衍生抽象审查**：对于超大规模节点集，是否自动提供了降维（如计算中心度）或聚合方案？

