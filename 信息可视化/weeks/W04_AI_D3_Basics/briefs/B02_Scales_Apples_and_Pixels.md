---
week: W04
brief_id: B02
title: "比例尺：苹果与像素 (Scales: Apples and Pixels)"
textbook: "Interactive Data Visualization for the Web, Scott Murray, 2017"
chapters: ["7"]
line_range: [1, 1307]
source_path: "knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017/chapter_07_Scales.md"
covers_modules: ["M04"]
status: draft
---

## 教材位置
- 原著：Scott Murray, *Interactive Data Visualization for the Web*, 2017
- 章节：Chapter 7 — Scales
- 范围：7 (Lines 1 - 1307)

## 核心知识提取

### 比例尺 (Scales) 简介
- 比例尺是将**输入域 (input domain)**映射到**输出范围 (output range)**的函数（Mike Bostock 的定义）。
- 数据集中的值通常不直接对应可视化中的像素尺寸，比例尺提供了一种将数据值映射到对可视化有用的新值的方法。
- D3 的比例尺是你自定义参数的**函数 (functions)**。调用比例尺函数并传入数据值，它会返回一个缩放后的输出值。

### 苹果与像素 (Apples and Pixels)
- **教材经典锚点**：路边水果摊卖苹果。假设苹果销量数据是 `[100, 200, 300, 400, 500]`。若直接用数据作为条形图的像素高度，500 个苹果对应 500 像素高。但如果下个月卖了 1800 个苹果，屏幕就装不下了。
- 因为“苹果不是像素 (apples are not pixels)”，我们需要比例尺在它们之间进行转换。

### 定义域和值域 (Domains and Ranges)
- **输入域 (input domain)**：可能的输入数据值的范围。比如基于苹果数据，输入域可以是 `100` 到 `500`（数据的最小和最大值），或者是 `0` 到 `500`。
- **输出范围 (output range)**：可能的输出值的范围，通常用作像素单位的显示值。
- **教材经典互动**：“当我喊‘输入 (Input)’，你喊‘定义域 (Domain)’！当我喊‘输出 (Output)’，你喊‘值域 (Range)’！” 这有助于强化记忆。

### 归一化 (Normalization)
- 线性比例尺的本质就是归一化。这是一种将数值基于可能的最小值和最大值映射到 `0` 和 `1` 之间的新值的过程。
- D3 会处理归一化的数学运算：输入值根据输入域 (domain) 归一化，然后归一化的值再按比例扩展到输出范围 (range)。

### 创建比例尺 (Creating a Scale)
- D3 的线性比例尺生成器通过 `d3.scaleLinear()` 访问。
- 使用 `.domain([min, max])` 设置输入域，使用 `.range([min, max])` 设置输出范围。
- 它们通常通过链式调用写在一起。
- 比例尺函数通常在 `attr()` 等方法中调用，而不是单独调用。

### 缩放散点图 (Scaling the Scatterplot)
- **动态计算极值**：使用 `d3.min()` 和 `d3.max()` 在运行时分析数据集，而不是硬编码域的边界值。
- 对于嵌套数组，需要传入**访问器函数 (accessor function)**作为第二个参数给 `min/max`，以指定要比较的具体值（例如 `function(d) { return d[0]; }`）。
- **设置动态比例尺**：例如 `xScale` 的定义域是 `[0, d3.max(...)]`，值域是 `[0, w]`（SVG 宽度）。
- **整合缩放后的值**：在绘图属性（如 `cx`, `cy`）中传入 `xScale(d[0])` 和 `yScale(d[1])`。

### 完善图表 (Refining the Plot)
- **反转 Y 轴**：因为 SVG 的 Y 坐标向下递增，可以通过翻转输出范围来反转 Y 轴，即将 `.range([0, h])` 改为 `.range([h, 0])`，使得较大的值在图表上位居高处。
- **添加内边距 (Padding)**：在 `range()` 中引入 `padding` 变量（例如 `[padding, w - padding]`），以防止图表边缘的元素（如圆圈或文本）被切断。
- **缩放半径 (Scaled Radii)**：创建专门用于缩放视觉属性的比例尺。例如创建一个 `rScale` 将 Y 值域映射为 `[2, 5]`，用于控制圆圈的相对大小。
- 比例尺使得当数据范围极剧扩大（如加入巨大离群值），或更改画布大小 (SVG 尺寸 `h`, `w`) 时，所有元素都会自动按比例进行重新排列，无需修改绘制逻辑代码。

### 比例尺的其他方法 (Other Methods)
- `nice()`：将域的两端扩展到最近的规整整数（如将 `[0.201..., 0.996...]` 扩展为 `[0.2, 1.0]`）。
- `rangeRound()`：输出的所有值四舍五入为最接近的整数，避免子像素抗锯齿导致的模糊边缘。
- `clamp(true)`：默认比例尺在接收到超出输入域的值时会返回超出输出范围的值，使用 `clamp` 强制将过大/过小的值限制在指定的输出范围两端。

### 其他类型的比例尺 (Other Scales)
- `scaleSqrt`：平方根比例尺。绘制圆圈时，应根据**面积 (area)**而非**半径 (radius)**进行缩放。可以通过传入 `scaleSqrt` 替代 `Math.sqrt()` 来处理面积缩放 (`aScale`)。
- `scalePow`：幂比例尺。
- `scaleLog`：对数比例尺。
- `scaleQuantize`：带有离散输出范围的线性比例尺（用于“分桶”）。
- `scaleQuantile`：类似 `scaleQuantize`，但输入域也是离散的。
- `scaleOrdinal`：序数比例尺，使用非定量值（如分类名称）作为输出。
- `schemeCategory10`, `schemeCategory20` 等：预设的分类颜色方案。
- `scaleTime`：时间比例尺，用于处理日期和时间值。

### 时间比例尺 (Time Scales)
- JavaScript 通过 `Date` 对象理解时间，无法对纯字符串（即使看起来像日期）进行计算。
- **解析时间字符串**：使用 `d3.timeParse("%m/%d/%y")` 将字符串转为 `Date` 对象。格式符如 `%m`（两位月）、`%d`（两日天）、`%y`（两位年）需要查阅 API 文档。
- **时间范围缩放**：`d3.scaleTime()` 支持 `d3.min()` 和 `d3.max()` 对 `Date` 对象直接取极值，设置与线性比例尺相同的范围并返回坐标值。
- **格式化日期用于显示**：使用 `d3.timeFormat("%b %e")` 将 `Date` 对象转回人类可读字符串（如 "Jan 1"），用于在图表轴上显示标签。

## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig 7.1 | An input domain and an output range, visualized as parallel axes | `images/9269569...` (L132) | ✅ 已迁移至 `public/textbook/Fig7.1_Scales.webp` |
| Fig 7.2 | Scatterplot using x and y scales | `images/4b0c59b...` (L536) | ✅ 已迁移至 `public/textbook/Fig7.2_Scales.webp` |
| Fig 7.3 | Scatterplot with y scale inverted | `images/d9a6d2f...` (L585) | ✅ 已迁移至 `public/textbook/Fig7.3_Scales.webp` |
| Fig 7.4 | Scatterplot with padding | `images/bd54808...` (L630) | ✅ 已迁移至 `public/textbook/Fig7.4_Scales.webp` |
| Fig 7.5 | Scatterplot with more padding | `images/7ad430c...` (L651) | ✅ 已迁移至 `public/textbook/Fig7.5_Scales.webp` |
| Fig 7.6 | Scatterplot with scaled radii | `images/b4d5c19...` (L709) | ✅ 已迁移至 `public/textbook/Fig7.6_Scales.webp` |
| Fig 7.7 | Scatterplot with big numbers added | `images/fadac06...` (L729) | ✅ 已迁移至 `public/textbook/Fig7.7_Scales.webp` |
| Fig 7.8 | Large, scaled scatterplot | `images/3a5fb0c...` (L746) | ✅ 已迁移至 `public/textbook/Fig7.8_Scales.webp` |
| Fig 7.9 | Using a square root scale for circle areas | `images/40702f1...` (L977) | ✅ 已迁移至 `public/textbook/Fig7.9_Scales.webp` |
| Fig 7.10 | Look mom, no strings! | `images/d157d91...` (L1153) | ✅ 已迁移至 `public/textbook/Fig7.10_Scales.webp` |
| Fig 7.11 | Verifying the xScale domain runs from January 1 through January 31, 2017 | `images/61e22e9...` (L1193) | ✅ 已迁移至 `public/textbook/Fig7.11_Scales.webp` |
| Fig 7.12 | Time-scaled circles | `images/ece70de...` (L1219) | ✅ 已迁移至 `public/textbook/Fig7.12_Scales.webp` |

## 易混淆概念辨析

- **比例尺 (Scale) vs. 坐标轴 (Axis)**：比例尺是一个在幕后运行的**数学映射关系**（没有任何视觉输出），而坐标轴是比例尺在屏幕上的**视觉表达**（刻度线、标签等）。
- **输入域 (Domain) vs. 输出范围 (Range)**：Domain 代表输入数据的极限值（如 `0` 到 `500` 个苹果），而 Range 映射到物理输出极限值（如屏幕上的 `0` 到 `800` 像素）。
- **半径缩放 vs. 面积缩放 (Radius vs. Area Scaling)**：使用线性比例尺 (`scaleLinear`) 映射圆的半径（`r` 属性）会导致其在视觉上的面积呈平方级爆炸放大，这是一种误导；应该使用平方根比例尺 (`scaleSqrt`) 进行**面积缩放 (Area Scaling)**。
- **时间解析 (timeParse) vs. 时间格式化 (timeFormat)**：`timeParse` 的方向是 `String -> Date 对象`（读取数据时使用）；`timeFormat` 的方向是 `Date 对象 -> String`（生成图表标签输出时使用）。

## 与逐字稿的对照检查表

- [ ] `CHK-B02-01`: 是否通过“苹果与像素”类比清晰解释了比例尺为什么存在（映射数据与物理显示）。
  - 关键词: `苹果`, `像素`, `映射`
  - 预期出现模块: M04
- [ ] `CHK-B02-02`: 是否强调了“输入(Input)即定义域(Domain)”、“输出(Output)即值域(Range)”的对应法则，确保学生分清这两个核心概念。
  - 关键词: `定义域`, `Domain`, `值域`, `Range`
  - 预期出现模块: M04
- [ ] `CHK-B02-03`: 是否清楚区分了“比例尺(Scale)”和“坐标轴(Axis)”是数学函数与视觉呈现的区别。
  - 关键词: `数学关系`, `视觉表达`, `坐标轴`
  - 预期出现模块: M04
- [ ] `CHK-B02-04`: 是否讲解了如何通过反转 Range（`[h, 0]`）来修复散点图中 Y 轴坐标系自上而下的问题。
  - 关键词: `反转`, `倒置`, `Y轴`
  - 预期出现模块: M04
