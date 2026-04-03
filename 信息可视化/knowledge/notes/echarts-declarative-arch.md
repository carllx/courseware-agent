# ECharts 声明式架构

**知识节点**: `echarts-declarative-arch`
**认知目标**: 理解 ECharts 的声明式编程范式，掌握 Option 对象分层结构，能够用自然语言精准下达 AI 图表生成指令

---

## 1. 声明式 vs 指令式：两种编程哲学

可视化领域的开发工具栈，天然分化为两大阵营：

- **声明式 (Declarative)**：你只需告诉机器 **"我要什么"**，而不需要写出每一步的执行路径。ECharts、Vega-Lite、ggplot2 都属此类。
- **指令式 (Imperative)**：你必须精确指定 **"怎么做"**——画布建多大、点从哪来到哪、每根线的路径算法。D3.js 是典型。

类比思考：声明式像是在餐馆点菜（"我要一份红烧牛肉面，微辣"），指令式像是在自家厨房手搓面条（"先和面，加 300ml 水，揉 15 分钟……"）。

ECharts 的声明式本质使它成为大语言模型 Vibe Coding 的**天然盟友**——因为 JSON 配置与自然语言的语义结构高度同构。

## 2. Option 对象：ECharts 的宇宙总线

ECharts 的所有图表都由一个单一的 `option` 对象驱动。它是一棵配置树，通常包含以下核心层：

```
option = {
  title:     { ... },    // 标题组件
  legend:    { ... },    // 图例
  tooltip:   { ... },    // 悬浮提示
  xAxis:     { ... },    // 横轴定义（类别/时间/数值）
  yAxis:     { ... },    // 纵轴定义
  series:    [ ... ],    // 🔴 核心：数据系列（图表类型在这里决定）
  dataZoom:  [ ... ],    // 缩放滑块
  visualMap: { ... },    // 视觉映射（颜色/大小与数据的绑定）
  toolbox:   { ... },    // 右上角工具栏
}
```

### 关键认知：Series 决定图表形态

在 ECharts 中，根**不存在**"柱状图组件"或"散点图组件"。所有图表形态的差异，仅仅取决于 `series[i].type` 的字符串值：

| `type` 值 | 图表形态 | Munzner 对标 |
|:---|:---|:---|
| `'bar'` | 柱状图 | 1 Key + 1 Value, Line marks |
| `'line'` | 折线图 | 1 Key + 1 Value, Connection marks |
| `'scatter'` | 散点图 | 2 Values, Point marks |
| `'pie'` | 饼图 | 1 Key + 1 Value, Area marks + Angle |
| `'heatmap'` | 热力图 | 2 Keys + 1 Value, Area marks + Color |
| `'parallel'` | 平行坐标 | N Values, Parallel axes |

这意味着：当你与 AI 对话时，只需明确"series type"，模型即可精准定位图表基因。

## 3. 交互组件：无需编码的响应式增强

ECharts 的巨大优势在于，复杂交互不需要自己写事件监听器。只需在 `option` 中声明组件即可：

- **dataZoom**: 底部滑块（slider）或框选缩放（inside），让用户自主聚焦局部时间窗口
- **tooltip**: 悬停即显示精确数值 + 自定义 HTML 格式器
- **brush**: 框选刷取一组数据点并联动其他图表

这对应了 Munzner Ch11 中 **Overview + Detail** 及 **Brush & Link** 的交互操控模式。

## 4. 反面：ECharts 的天花板

- **像素级控制不可能**：你无法让某个特定数据点按贝塞尔曲线运动
- **自定义标记受限**：series type 之外的异形标记（水滴、不规则多边形）极难实现
- **封装即黑箱**：渲染流程不透明，出现排版异常时，调试无从下手

当教学需求超越了标准图表范畴（如数据艺术、生成式可视化），就必须退回到 D3 的底层控制权。

## 5. AI Vibe Prompt 模板

向 LLM 下达 ECharts 图表生成指令时，高成功率的 Prompt 应包含：

```
1. 数据描述 — "附带了一份 CSV，X 列是年份 (Ordinal), Y 列是 GDP 值 (Quantitative)"
2. Series 类型 — "请使用 type: 'bar' 柱状图"
3. 交互组件 — "添加 dataZoom 组件，tooltip 悬停显示原始数值"
4. 风格指令 — "使用深色背景 + 霞光渐变配色"
5. 输出格式 — "输出为单一 HTML 文件，内联 ECharts CDN"
```

---

**参考来源**: ECharts 官方文档 (https://echarts.apache.org), Munzner Ch7 (Arrange Tables)
