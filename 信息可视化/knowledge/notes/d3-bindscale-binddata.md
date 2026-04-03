# D3.js SVG 坐标系与比例尺机制

**知识节点**: `d3-bindscale-binddata`
**认知目标**: 理解 SVG 画布坐标系的倒置逻辑，掌握 D3 比例尺 (Scale) 的 domain→range 映射原理，以及 Enter-Update-Exit 数据绑定模式

---

## 1. SVG 坐标系：那个违反直觉的 (0,0)

在传统数学课本里，坐标原点 (0,0) 在**左下角**，Y 轴向上增长。但浏览器的 SVG 画布是从**左上角**开始的：

```
(0,0) ——————→ X 轴 (width)
  |
  |
  ↓
  Y 轴 (height)
```

这意味着：Y 值越大，元素反而画得越靠**下**。如果你不主动翻转坐标，一根 GDP 数据为 10000 的柱状图会直插屏幕最底部，而不是"向上生长"。

**AI 生成代码的第一号陷阱**：当 LLM 为你生成 D3 柱状图时，如果没有用 `height - scale(d.value)` 做 Y 轴反转，所有柱子都是"倒着长"的。

## 2. 比例尺 (Scale)：真实世界到屏幕的翻译官

比例尺是 D3 最核心的数学机制。它解决一个根本问题：**如何把人间万象（如 10,000 公里的距离）映射到区区 800 像素的屏幕空间？**

### 2.1 三步骤：Domain → Scale Function → Range

```
d3.scaleLinear()
  .domain([0, 10000])    // 输入域：数据的最小值到最大值
  .range([0, 800])       // 输出域：屏幕的起始像素到终止像素
```

调用 `scale(5000)` 会返回 `400`——数据空间的正中间被映射到了屏幕的正中间。

### 2.2 常用比例尺类型

| 比例尺 | 适用属性类型 | 映射逻辑 |
|:---|:---|:---|
| `scaleLinear` | 量化型 (Quantitative) | 线性等比映射 |
| `scaleLog` | 量化型（跨数量级） | 对数压缩极端值 |
| `scaleBand` | 分类型 (Categorical) | 等宽带状分段 |
| `scaleOrdinal` | 分类型 → 颜色 | 离散到离散的查表映射 |
| `scaleTime` | 时间序数型 | 日期到像素的线性映射 |

### 2.3 Margin Convention（边距惯例）

D3 社区有一项"不成文宪法"：必须在 SVG 画布四周预留 margin 空间给坐标轴标签。

```
const margin = {top: 20, right: 30, bottom: 40, left: 50};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;
```

**AI 生成代码的第二号陷阱**：如果你不在 Prompt 中提及 margin，LLM 经常在 SVG 的 (0,0) 处直接画内容，导致坐标轴标签被屏幕边缘截断，或者图形被挤压到角落。

## 3. 数据绑定：Enter-Update-Exit 三态机

D3 的灵魂在于 **数据驱动的 DOM 操作**。当你把一个数组绑定到一组 SVG 元素时，D3 会自动计算三种状态：

- **Enter**: 数据有了，但 DOM 节点还没有 → 需要**新增**节点
- **Update**: 数据和 DOM 节点都有 → 需要**更新**属性
- **Exit**: DOM 节点有了，但数据没了 → 需要**删除**节点

```javascript
const bars = svg.selectAll("rect")
   .data(dataset);

bars.enter()         // 新数据 → 创建新矩形
   .append("rect")
   .attr("x", d => xScale(d.category))
   .attr("y", d => yScale(d.value))
   .attr("height", d => height - yScale(d.value));

bars.exit().remove(); // 多余矩形 → 移除
```

D3 v7 中推荐使用 `.join()` 简写，但理解底层三态对排错至关重要。

## 4. 反面：D3 代码的常见崩溃模式

| 崩溃场景 | 根因 | 表现 |
|:---|:---|:---|
| 画布全白 | SVG 的 width/height 未设置或为 0 | 浏览器无可见区域 |
| 图形在画布最下方挤成一条线 | Y 轴比例尺 domain 远超 range，或未翻转 | 所有元素 y 坐标趋近 0 |
| 只画出第一个数据点 | data bind 读取了嵌套对象而非扁平数组 | enter() 只触发一次 |
| 坐标轴标签消失 | 未设置 margin 或 g 的 translate | 标签渲染在画布外 |

## 5. D3 与 ECharts 的本质区别

| 维度 | ECharts | D3.js |
|:---|:---|:---|
| 编程范式 | 声明式（配 JSON） | 指令式（写函数） |
| 学习曲线 | 低（直接上手图表） | 高（需懂 SVG + 数学 + DOM） |
| 自由度 | 标准图表内极高 | 无限制，像素级控制 |
| AI 生成成功率 | 极高（JSON 结构清晰） | 中等（易出坐标/绑定错误） |
| 适用场景 | 商业仪表盘、数据分析原型 | 数据艺术、非标准可视化 |

---

**参考来源**: D3.js 官方文档 (https://d3js.org), Munzner Ch7 §7.2-7.4, Mike Bostock's Observable 教程
