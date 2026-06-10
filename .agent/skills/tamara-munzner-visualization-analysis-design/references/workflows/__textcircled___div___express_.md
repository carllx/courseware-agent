# 工作流：空间排布与视觉编码设计 (Arrange Tabular Data)

## 1. 前置准备与上下文 (Prerequisites & Context)

**为什么需要这个工作流 (WHY & WHEN)**：
在处理表格数据（Tabular Data）时，空间排布是最核心的视觉编码通道。通过正确的空间排布，数据中的属性及其内在关联才能被人类视觉系统有效解析。本工作流指导如何在图表设计时，从“表达值（Express Values）”、“区域的分离/排序/对齐（Separate, Order, Align Regions）”、“坐标轴朝向（Axis Orientation）”以及“布局密度（Layout Density）”四个维度进行决策。

> **深度理论检索 (Progressive Disclosure)**
> 如果你想深入了解为什么空间排布（Spatial Arrangement）在所有视觉编码通道中优先级最高，请让 Agent 运行以下命令：
> ```bash
> bash scripts/query_theory.sh "Why is spatial arrangement the most effective visual encoding channel?"
> ```
> ```bash
> bash scripts/query_theory.sh "Explain Figure 7.1: Design choices for arranging tables in detail."
> ```

## 2. 综合指南与最佳实践 (Comprehensive Guide & Best Practices)

在处理表格数据排布时，主要需经历四大设计决策：

### 2.1 表达数值 (Express Values)
用于呈现连续变量或定量数据（Quantitative Data）的大小和分布。
- **行动指南**：为属性分配相应的长度或位置进行空间映射。确保表达方式与数据连续性或离散特性相符。
- **示例图解**：
  ![](../../images/fd2f01085622b0f8b3d2aa2d1e6dfe84cd4bd8e08e85017d477f16c83141c82a.jpg)

### 2.2 分离、排序与对齐区域 (Separate, Order, Align Regions)
用于对分类数据（Categorical Data）或多维度数据进行切分与结构化，使其能够在空间中可控地延展。
- **单键列表 (1 Key List)**：依据一个键值（Key）将数据分离为线性的列表。
  ![](../../images/649d39b7436c1565ac8e5c45e04e168d5534c776774fb6fba5248c4c1864c64e.jpg)
  ![](../../images/28bf486c82c25f1b24da66dbd727e0305cbca1366f7f3b62d3e46f9e5a9efbeb.jpg)
- **双键矩阵 (2 Keys Matrix)**：依据两个键值分离数据，形成二维矩阵，分别映射至水平与垂直方向。
- **三键体积 (3 Keys Volume)**：扩展到三个键值，利用三维空间分离数据（请谨慎使用三维图表，避免视觉遮挡）。
- **多键递归细分 (Many Keys Recursive Subdivision)**：面对超过三个键值的多维数据，可采用嵌套和递归的方法划分空间，如 Treemap 或马赛克图（Mosaic Plot）。
  - **其他图解参考**：
    ![](../../images/8dc432da71e506dbadbeed8476d5f2772f5e81bb409ae8b40eaf3ba80ff65314.jpg)
    ![](../../images/5f64d2c244a0a6844b455187eb09e2341639565abd17670bb6abb1eb373bcabe.jpg)
    ![](../../images/915f70d1a27fdcf3fcf38c29a9e9ab94ec1178746419c8b71693b086ef0c5007.jpg)
    ![](../../images/3f8a7ff251b16a157ebf2f83aad080a3846c21657d275c1e304043eae78f180c.jpg)
    ![](../../images/42041f057efcefea783790cbed70cdab1717d2f433d6284276145022f5606cdf.jpg)

> **深度理论检索**
> 什么是 Keys？在可视化设计中它们与 Attributes 有何不同？
> ```bash
> bash scripts/query_theory.sh "Difference between keys and values/attributes in dataset structures."
> ```

### 2.3 坐标轴朝向设计 (Axis Orientation)
控制数据如何在物理或屏幕像素空间上延伸。
- **正交/直线朝向 (Rectilinear)**：最常见的笛卡尔坐标系，适用于大部分散点图、柱状图。
  ![](../../images/e8ea9972596f36d0a7408710c7a403521914ca7a4b8a1bf9b84288f663b870dc.jpg)
- **平行朝向 (Parallel)**：常用于平行坐标图（Parallel Coordinates），适合展现高维多属性数据，以纵轴并排表示各个维度。
  ![](../../images/acdf74b911fb0a070d6df70539835c5f08209dcdfc06cd8dc2987d3037139618.jpg)
- **径向/极坐标朝向 (Radial)**：用于体现周期性、部分与整体关系或强调放射状流动的场景，如雷达图、极坐标柱状图。
  ![](../../images/32841050868494441a115ee6ce639bea8d6794a6c7e78965fefff450f64df978.jpg)

### 2.4 布局密度 (Layout Density)
决定了画布空间的利用率和数据节点的紧凑程度。
- **密集布局 (Dense)**：适合大规模数据集，通过紧密相连的像素或极小标记（如密集热力图）揭示整体趋势和模式。
  ![](../../images/7798002cc6772722d0b85664b390b44139fce101d5bb80edd7f445ca95bb5031.jpg)
- **空间填充 (Space-Filling)**：最大化利用屏幕可用空间，通常配合面积与区域划分共同表达分类数据的嵌套关系及权重（如树状图）。
  ![](../../images/0813c204b9f218b903cfcc91b0075a591f6e1f75753b6b5f0a4deb63c8bf05d9.jpg)

> **深度理论检索**
> 想要了解密集布局的局限性和过绘（Overplotting）问题如何应对？
> ```bash
> bash scripts/query_theory.sh "How to handle overplotting and when to use space-filling layout density?"
> ```

## 3. 故障排除逻辑 (If/Then Troubleshooting Logic)

在执行空间排布设计时，可能会遇到以下边缘情况或理论冲突，请参考如下逻辑进行调整：

- **IF** 发现图表中重叠过多导致“表达数值”无法清晰辨识（产生 Overplotting）：
  - **THEN** 尝试更换坐标轴的 **布局密度** 到更易于观察分布的类型，或者将过度集中的数据点聚合（Aggregate）后再进行区域的分离和排序。
- **IF** 数据存在极多属性（维度远高于二维），而传统的直线坐标系无法有效承载：
  - **THEN** 考虑切换 **坐标轴朝向** 为“平行（Parallel）”，或应用“多键递归细分（Many Keys Recursive Subdivision）”策略对视图进行分面布局（Faceting）。
- **IF** 分类键值过多，导致使用“单键列表”排布时屏幕需要进行无止境的滚动：
  - **THEN** 降维或引入“双键矩阵（2 Keys Matrix）”进行平面分割，利用二维方向展示；或者利用高层级属性对其进行分组嵌套。
- **IF** 使用了径向（Radial）坐标系但发现角度和面积容易产生视觉误导：
  - **THEN** 判断是否绝对必须展示周期性特征。如果是典型的非周期性数据或需要精确比对数值的场景，请坚决退回到正交/直线（Rectilinear）坐标系。

## 4. 验证清单 (Verification Checklists)

- [ ] **视觉通道映射一致性**：确认是否正确且直观地使用了位置或长度在空间中“表达值（Express Values）”。
- [ ] **区域划分逻辑清晰度**：针对数据中的分类属性，检查是否采用了合理的键数量（单键、双键或多键递归细分）将数据正确切分为了无重叠或易理解的区域。
- [ ] **坐标系适配度验证**：坐标轴的朝向（正交、平行、径向）是否完美契合数据的业务分析意图（如强调周期性、对比多维度属性）。
- [ ] **密度控制与屏幕利用**：视图是采用密集式布局（Dense）还是空间填充（Space-Filling），是否最大化利用了像素空间且不存在由于过于拥挤造成的视觉混淆。
- [ ] **图片引用路径确认**：所有的说明配图均使用相对于当前文件的工作流图片路径（即 `../../images/` 前缀），保证文件独立查看时图片不丢失。