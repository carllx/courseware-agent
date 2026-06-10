# Getting Started with D3.js

## What is D3?
D3.js (Data-Driven Documents) is a JavaScript library for manipulating documents based on data. D3 helps you bring data to life using HTML, SVG, and CSS.

<!-- D3.js 是一个基于数据操作文档的 JavaScript 库。它利用 HTML、SVG 和 CSS，帮助你将数据生动地呈现出来。 -->

## SVG Basics for Beginners
Scalable Vector Graphics (SVG) is an XML-based markup language for describing two-dimensional based vector graphics. D3 heavily relies on SVG to draw shapes like rectangles, circles, and lines.

<!-- 可缩放矢量图形 (SVG) 是一种基于 XML 的标记语言，用于描述二维矢量图形。D3 很大程度上依赖 SVG 来绘制形状，例如矩形、圆形和线条。 -->

```html
<!-- SVG 基础示例 (Basic SVG Example) -->
<svg width="200" height="200">
  <!-- 绘制一个矩形 (Draw a rectangle) -->
  <rect x="10" y="10" width="50" height="50" fill="blue"></rect>
  <!-- 绘制一个圆形 (Draw a circle) -->
  <circle cx="100" cy="100" r="25" fill="red"></circle>
</svg>
```

## Basic Data Binding
Data binding is the core concept in D3. It connects data to DOM elements.

<!-- 数据绑定是 D3 的核心概念。它将数据与 DOM 元素连接起来。 -->

### The `join` Pattern (Modern Approach)
The `join` method is the modern way to handle the enter, update, and exit phases of data binding.

<!-- `join` 方法是处理数据绑定中 enter（进入）、update（更新）和 exit（退出）阶段的现代方式。 -->

```javascript
const data = [10, 20, 30, 40];

// 选择所有的 circle 元素，并绑定数据 (Select all circles and bind data)
d3.select("svg")
  .selectAll("circle")
  .data(data)
  .join("circle") // join 处理 enter, update, exit (join handles enter, update, exit)
    .attr("r", d => d) // 这里的 d 就是绑定的数据 (d is the bound data: 10, 20, 30, 40)
    .attr("cx", (d, i) => i * 50 + 25) // i 是索引 (i is the index)
    .attr("cy", 50)
    .style("fill", "steelblue");
```

### Enter, Update, Exit (Traditional Approach)
Before `join`, we explicitly handled the three states:
- **Enter**: Data exists, but no corresponding DOM element. (Create new elements)
- **Update**: Data and DOM element both exist. (Update existing elements)
- **Exit**: DOM element exists, but no data. (Remove elements)

<!-- 
在 `join` 之前，我们显式地处理三种状态：
- Enter (进入): 存在数据，但没有对应的 DOM 元素。（需要创建新元素）
- Update (更新): 数据和 DOM 元素都存在。（更新现有元素）
- Exit (退出): 存在 DOM 元素，但没有数据。（需要删除元素）
-->

```javascript
// 1. Data Binding (数据绑定)
const circles = d3.select("svg").selectAll("circle").data(data);

// 2. Exit (退出：删除多余的元素)
circles.exit().remove();

// 3. Update (更新：更新已有的元素)
circles.attr("fill", "blue");

// 4. Enter (进入：创建缺失的元素并合并)
circles.enter()
  .append("circle")
  .attr("r", d => d)
  .merge(circles) // 合并 enter 和 update 选择集 (Merge enter and update selections)
  .attr("cx", (d, i) => i * 50 + 25)
  .attr("cy", 50);
```
