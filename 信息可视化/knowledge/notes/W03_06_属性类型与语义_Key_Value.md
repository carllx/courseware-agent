# W03_06_属性类型与语义_Key_Value

## 教材位置
- 原著：Tamara Munzner, Visualization Analysis & Design, 2014
- 章节：Chapter 2 — What: Data Abstraction
- 范围：2.5 - 2.7 (Lines 226 - 400)

## 核心知识提取

### 2.5 属性类型 (Attribute Types)
属性是可视化编码的核心。主要分为两类：分类（Categorical）和有序（Ordered）。有序数据进一步细分为序数（Ordinal）和定量（Quantitative）。

![Figure 2.7 — 属性类型分类树及排序方向](../textbook/Visualization%20Analysis%20%26%20Design%20--%20Tamara%20Munzner%20--%202014/images/d3d577a260cbf2d2a221d09bea8dc9cca114454d264c1484fe3f9b88c2d5f64c.jpg)

#### 2.5.1 分类数据 (Categorical / Nominal)
- **定义**：不具备隐式排序（Implicit ordering）的数据。
- **作用**：只能区分两个事物是相同（如都是苹果）还是不同（苹果 vs 橘子）。
- **示例**：最喜欢的水果、人名、电影类型、文件类型、城市名。
- **注意**：分类数据可以有层次结构（Hierarchical structure）；可以施加任意的外部排序（如按字母表或价格排序），但这不属于属性本身的隐式特性。

#### 2.5.2 有序数据：序数与定量 (Ordered: Ordinal and Quantitative)
- **序数数据 (Ordinal)**：具有明确定义的顺序，但不能进行全面的算术运算。例如，衣服尺寸（大减去中没有意义，但中介于小和大之间）、电影排行榜排名。
- **定量数据 (Quantitative)**：测量可以支持算术比较的量级（Magnitude）。例如，68英寸减去42英寸等于26英寸。示例包括身高、体重、温度、股票价格。整数和实数都属于定量数据。

#### 2.5.3 排序方向 (Ordering Direction)
有序数据可以具有以下三种方向之一：
1. **顺序 (Sequential)**：从最小值到最大值的同构范围（Homogeneous range）。例如从海平面到珠穆朗玛峰的高度，或者从海平面到海底最深处的深度。
2. **发散 (Diverging)**：可以解构为指向相反方向、在中间的零点相遇的两个序列。例如，以海平面为共同零点，向上的山峰高度和向下的海底深度的完整海拔数据集。
3. **循环 (Cyclic)**：值会绕回到起点，而不是无限增加。通常与时间测量有关，如一天中的小时、一周中的天、一年中的月。

#### 2.5.4 分层属性 (Hierarchical Attributes)
属性内部或多个属性之间可能存在层次结构。
- **示例**：十年来收集的公司每日股票价格（时间序列数据）。时间可以按层级聚合（Aggregated hierarchically）：天 -> 周 -> 月 -> 年。
- **应用**：可以在多个尺度上寻找模式，如平装与周末的周度模式，或冬夏的季节性模式。空间数据同样有层次（邮编 -> 城市 -> 州/省 -> 国家）。

### 2.6 语义 (Semantics)
知道属性的**类型**并不能告诉我们它的**语义**（它们是正交交叉的）。本书重点关注键（Keys）与值（Values）的语义，以及空间/连续数据与非空间/离散数据的区别。还有一个额外考量是时间语义。

#### 2.6.1 键与值语义 (Key versus Value Semantics)
- **键 (Key / Independent attribute / Dimension)**：作为查找值属性的索引。
- **值 (Value / Dependent attribute / Measure)**：被查找的属性。
区分键和值对于表格和场非常重要。

![Figure 2.8 — Tables 与 Fields 的 Key/Value 语义对比](../textbook/Visualization%20Analysis%20%26%20Design%20--%20Tamara%20Munzner%20--%202014/images/b323d1c56de0f5380cbe657be68d1fd79ace875be397a4dc68a6be03918c879b.jpg)

##### 扁平表 (Flat Tables)
- 只有一个键，每条目对应表中的一行。
- 键可以隐式存在（行号索引），也可以显式包含为属性。作为显式键的属性必须具有唯一值（不能有重复项）。
- 键通常是分类或序数属性。定量属性通常不适合做键，因为无法阻止多个条目拥有相同的定量值。

![Figure 2.9 — 扁平表属性列按类型着色示例](../textbook/Visualization%20Analysis%20%26%20Design%20--%20Tamara%20Munzner%20--%202014/images/87ab3d9f47413a2fdcab036e97a8904ec2165dd6fab519c3069c74e7c2e74838.jpg)

##### 多维表 (Multidimensional Tables)
- 需要多个键（Multiple keys）来查找一个条目。所有键的组合对于每个条目必须是唯一的，即使单个键属性中包含重复项。
- **示例**：生物学基因活动表，"基因"是一个键，"时间"是另一个键，单元格中的值是在特定时间的基因活动水平。
- 很多时候，确定哪些是独立键、哪些是依赖值，恰恰是可视化分析的目标，而不是起点。

##### 场中的键与值 (Fields)
- 场代表连续数据，但在场中键和值同样是核心概念（空间场中常被称为自变量 Independent variable 和因变量 Dependent variable）。
- 空间位置（Spatial position）作为定量键起作用。在采样范围内的任何位置都可以返回有用的属性值，而不仅仅是在记录数据的确切点上。
- **标量场 (Scalar Fields)**：单变量（Univariate），空间中每个点有单个值属性（如房间内每点的温度）。
- **向量场 (Vector Fields)**：多变量（Multivariate），每个点有多个属性值列表（如具有方向和幅度的风速箭头）。
- **张量场 (Tensor Fields)**：每个点有一个属性数组，代表更复杂的多元数学结构（如 3D 应力，无法用单一箭头表示，需要椭球体等复杂形状）。
- 判断场的语义必须依赖外部领域知识，单凭类型信息无法判断（比如给定 9 个数字，无法判断它是 9 个独立的标量场，还是标量+向量的混合，还是一个张量场）。

#### 2.6.2 时间语义 (Temporal Semantics)
与时间相关的任何信息。由于时间的层次结构和潜在的周期性结构，时间数据处理起来很复杂。时间属性可以是值语义，也可以是键语义。

- **时间作为值 (Time as Value)**：例如，已耗费的持续时间（Duration），或交易发生的具体日期。此时数据集并非"时变"的。
- **时变数据 (Time-Varying Data / Time as Key)**：当时间是键属性之一时。例如动物群体传感器，每一秒都会有每个动物的新位置数据。
  - **时间序列 (Time-series)**：有序的时间-值对序列（通常时间间隔均匀），是时间作为键的表格特例。分析任务通常涉及在多个时间尺度（小时、日、周、季节）上寻找趋势和相关性。

- **动态 (Dynamic) 词汇的歧义辨析**：
  1. 某些语境下，Dynamic 意味着数据集具有时变语义（Time-varying semantics，时间作为 Key）。
  2. 另一些语境下（参见 2.4.6），Dynamic 指数据集类型为**流 (Stream)**，即数据条目在可视化系统运行期间动态增加/删除/改变。本书对这两者严格区分。

## 关键图表索引
- **Figure 2.7**: 属性分类树（Attributes -> Categorical / Ordered -> Ordinal / Quantitative）以及排序方向（Sequential / Diverging / Cyclic）。
- **Figure 2.8**: 表格（Tables）与连续场（Fields）的键（Key）和值（Value）语义对比图。扁平表使用分类键，场使用空间位置作为定量键。
- **Figure 2.9**: 扁平表中如果没有显式唯一标识符，行号（隐式键）将作为键存在。

## 易混淆概念辨析
- **Type (类型) vs Semantics (语义)**：类型决定了数据能做何种数学运算（分类/有序/量化）；语义决定了在业务逻辑中它扮演什么角色（Key 还是 Value）。
- **Key (键) vs Value (值)**：数据库语言中称为主键和值；统计学语言中称为自变量 (Independent) 和因变量 (Dependent)；数据仓库术语中称为维度 (Dimension) 和度量 (Measure)。
- **Sequential (顺序) vs Diverging (发散)**：从 0 到 100 的高度是顺序；包含负海拔的山脉-海洋图，0 为中间基准，属于发散。这对选择颜色映射（Colormap）至关重要。

## 与逐字稿的对照检查表
- [ ] 是否向学生强调了 "Categorical" (分类) 与 "Quantitative" (定量) 数据的核心区别（决定了图形通道能否使用大小/长度）？
- [ ] 是否清晰解释了 "Key" 和 "Value" 的概念？（用学生熟悉的 Excel 列、或者数据库概念、或者自变量/因变量隐喻）
- [ ] 是否说明了把连续定量数据聚合（Aggregate）为低精度分类数据（如温度数字 -> 冷/暖/热）是可视化设计的常见策略？
- [ ] 是否梳理了时间的特殊性（既可以是循环的 Cyclic、也可以是顺序的 Sequential；既可以是 Key，也可以是 Value）？
