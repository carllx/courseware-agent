# 📊 图表选择与视觉呈现工作流 (Visual Display & Graph Selection Workflow)

## 前置条件与上下文 (Prerequisites & Context)

**何时使用此工作流：**
- 当需要选择最有效的图表类型以视觉化方式传达数据洞察时。
- 当需要将低效或具有误导性的视觉元素（如饼图、3D 图表或双 y 轴）替换为更清晰的替代方案时。

**为什么这很重要：**
图表主要与我们的视觉系统交互，其处理信息的速度远快于处理表格的语言系统。精心设计的图表能够更快速地传递信息。与其探索新奇的可视化类型，不如熟练掌握一组核心的标准图表（点图、线图、条形图和面积图），这足以满足绝大多数的业务需求，同时将受众的认知负荷降至最低。

> **深度理论查询 (Deep Context Query):**  
> 如果需要了解人类大脑处理视觉与语言信息差异的理论基础，请执行：
> ```bash
> bash scripts/query_theory.sh "How do graphs interact with the visual system compared to tables?"
> ```

---

## 综合指南与最佳实践 (Comprehensive Guide & Best Practices)

### 1. 选择正确的图表类型
评估数据的性质和你的核心信息，然后从四大基本类别中进行选择：

- **点图 (Scatterplots)**
  - *使用场景:* 可视化两个变量之间的关系（例如，成本与行驶里程的关系）。
  - *启发式原则:* 使用散点图来识别聚类、相关性和异常值。应用条件格式将注意力吸引到特定区域（例如，高于平均成本的区域）。

- **线图 (Lines - 连续数据)**
  - *使用场景:* 跟踪随时间变化的连续数据。
  - *启发式原则:* 确保 x 轴使用一致的时间间隔，以防产生误导性的斜率。
  - *变体:* 
    - **标准折线图 (Standard Line Graph):** 比较一个或多个时间序列。
    - **带范围的折线图 (Line Graph with Range):** 显示点估计值（平均值），并以阴影带的形式显示范围（最大/最小值或置信区间）。
    - **斜率图 (Slopegraphs):** 非常适合显示恰好两个时间点之间跨多个类别的相对变化。
      - *注意:* 如果线条严重重叠，请仅强调你最关注的特定数据系列。

- **条形图 (Bars - 分类数据)**
  - *使用场景:* 比较不同的类别或分组。
  - *启发式原则:* 尽量利用条形图，因为受众对它们非常熟悉。较低的学习曲线意味着他们将脑力花在理解*数据*上，而不是*设计*上。
  - *条形图规则:*
    - **零基线 (Zero Baseline):** 条形图**必须**具有零基线。否则，会人为夸大差异。
    - **条形宽度:** 条形的宽度应大于条形之间的空白，但不要太宽以至于看起来像面积块。
    - **水平 vs 垂直:** 默认使用**水平条形图 (Horizontal Bar Charts)**，特别是当类别名称很长时。它们符合自然阅读习惯（从左到右，从上到下），允许受众在接触数据前先阅读类别标签。
    - **逻辑排序:** 对条形进行逻辑排序。如果没有自然顺序（如年龄段），则按值降序或升序排列，使最重要的数据点位于左上方。
    - **堆叠条形图 (Stacked Bars):** 用于显示总数和各个子组件，但要小心视觉过载。对于李克特量表/调查数据，考虑使用 100% 堆叠水平条形图。

- **面积图 (Area Graphs)**
  - *使用场景:* 通常应避免使用，除非在可视化数量级差异极大的数值时，使用二维正方形可以实现更紧凑的显示。

### 2. 精简标签与轴线 (Streamlining Labels & Axes)
- 决定是保留坐标轴还是直接在数据点上标记。
- *启发式原则:* 如果最重要的是宏观趋势，请保留坐标轴但淡化它（例如使用灰色）。如果具体的数值至关重要，请完全省略坐标轴，直接在数据点或条形末端标记，以减少冗余信息。

### 3. 必须严格避免的图表类型
- **饼图与环形图 (Pie Charts & Donut Charts):** 人类极其不擅长对二维空间、角度或弧长赋予准确的定量值。
  - *替代方案:* 使用水平条形图（逻辑排序）或 100% 堆叠条形图。
- **3D 效果:** 绝对不要使用 3D，除非你确实在绘制第三个数据维度。它会扭曲视角，使数据与网格线错位，并损害数据的可信度。
- **双 y 轴 (Secondary y-Axes):** 它们会导致混乱，迫使受众去破译哪条线对应哪个轴。
  - *替代方案 1:* 直接标记次要指标的数据点。
  - *替代方案 2:* 将两个不同的图表垂直堆叠，并共享相同的 x 轴。

> **深度理论查询 (Deep Context Query):**  
> 要查阅饼图为何失败的详细案例研究和视觉心理学原理，请执行：
> ```bash
> bash scripts/query_theory.sh "Why are pie charts considered evil and how do they distort perception?"
> ```

---

## If/Then 故障排除逻辑 (If/Then Troubleshooting Logic)

| 条件 / 观察现象 (Condition / Observation) | 行动 / 解决方案 (Action / Resolution) |
| :--- | :--- |
| **If** 你正在折线图上绘制时间，但测量间隔不一致（例如，十年与单一年份混合）... | **Then** 严格格式化 x 轴，保持与经过时间成比例的一致空间距离，以避免产生误导性的视觉叙事。 |
| **If** 你的斜率图看起来像“意大利面条图”，有太多交叉的线条... | **Then** 用浅灰色弱化背景数据系列，只突出显示推动核心叙事的 1 到 2 条线。 |
| **If** 你的条形图显示了巨大的百分比差异，但 x 轴并非从零开始... | **Then** 立即将基线重置为零。具有误导性的数据可视化会破坏信任。 |
| **If** 你需要显示两个比例截然不同的指标（例如，数百万的收入 vs 员工人数）... | **Then** 将它们拆分为两个垂直堆叠的图表并共享 x 轴，而不是使用令人困惑的右侧次要 y 轴。 |
| **If** 你的类别名称太长，导致 x 轴上出现尴尬的对角线倾斜文本... | **Then** 将视觉效果翻转为水平条形图，以便标签可以从左到右自然阅读。 |

---

## 验证检查清单 (Verification Checklists)

### 1. 图表选择与结构
- [ ] 选择的视觉形式是否是受众处理信息的最快、最直观的方式？
- [ ] 对于连续数据：x 轴上的时间间隔是否一致？
- [ ] 对于分类数据：是否设置了零基线 (Zero Baseline)？条形宽度是否合适？
- [ ] 对于分类数据：类别是否按逻辑进行了排序（自然顺序，或按数值升序/降序）？

### 2. 清晰度与完整性
- [ ] 是否已消除所有 3D 效果？
- [ ] 是否已将饼图和环形图替换为水平或堆叠条形图？
- [ ] 是否已移除任何次要 y 轴并替换为更好的替代方案（直接标记或垂直堆叠图表）？
- [ ] 你是否将图表展示给第三方（同事）以获取新鲜视角的反馈，确认他们无需解释就能理解你想要传达的意图？

### 3. 美学与引用
- [ ] 所有嵌入的图像是否都使用了相对路径正确链接？（例如，`../../images/Image00018.jpg`）

> **深度理论查询 (Deep Context Query):**  
> 要获取在标准工具中创建斜率图或瀑布图的高级格式化指南，请执行：
> ```bash
> bash scripts/query_theory.sh "Provide instructions for creating slopegraphs and waterfall charts"
> ```

## 图像参考 (Image References)
*在引用教科书中的特定图表示例时，请使用以下调整后的路径：*
- 散点图 (Scatterplot): `../../images/Image00018.jpg`
- 修改后的散点图 (Modified scatterplot): `../../images/Image00019.jpg`
- 折线图 (Line graphs): `../../images/Image00020.jpg`
- 显示平均值和范围 (Showing average within range): `../../images/Image00021.jpg`
- 斜率图 (Slopegraph): `../../images/Image00022.jpg`
- 修改后的斜率图 (Modified slopegraph): `../../images/Image00023.jpg`
- 福克斯新闻条形图 (Fox News bar chart): `../../images/Image00024.jpg`
- 零基线修正 (Zero baseline correction): `../../images/Image00025.jpg`
- 比较数据系列 (Comparing series): `../../images/Image00028.jpg`
- 瀑布图 (Waterfall chart): `../../images/Image00029.jpg`
- 水平条形图 (Horizontal bar charts): `../../images/Image00030.jpg`
- 100% 堆叠水平条形图 (100% stacked horizontal): `../../images/Image00031.jpg`
- 方形面积图 (Square area graph): `../../images/Image00032.jpg`
- 饼图 (Pie chart): `../../images/Image00033.jpg`
- 标记的饼图 (Pie chart labeled): `../../images/Image00034.jpg`
- 饼图替代方案 (Pie alternative): `../../images/Image00035.jpg`
- 环形图 (Donut chart): `../../images/Image00036.jpg`
- 3D 柱状图 (3D column chart): `../../images/Image00037.jpg`
- 双 y 轴 (Secondary y-axis): `../../images/Image00038.jpg`
- 双 y 轴替代方案 (Secondary y-axis alternatives): `../../images/Image00039.jpg`