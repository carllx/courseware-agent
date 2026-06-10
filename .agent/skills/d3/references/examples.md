# D3.js (v7) 常用图表代码模板

本文档提供了三个完整、可运行的 D3.js (v7) 常见图表模板：柱状图（Bar Chart）、折线图（Line Chart）和力导向图（Force-Directed Graph）。这些代码使用了 D3 的标准约定（如 margin 模式、数据绑定等）。

## 1. 柱状图 (Bar Chart)

带有坐标轴、比例尺、基本交互和提示框（Tooltip）的柱状图模板。

```javascript
// 假设 HTML 中有一个 <div id="chart"></div> 和 <div id="tooltip"></div>
const data = [
  { name: 'A', value: 30 },
  { name: 'B', value: 80 },
  { name: 'C', value: 45 },
  { name: 'D', value: 60 },
  { name: 'E', value: 20 },
  { name: 'F', value: 90 },
  { name: 'G', value: 55 }
];

// 定义图表的边距和尺寸
const margin = { top: 20, right: 30, bottom: 40, left: 40 };
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// 创建 SVG 容器
const svg = d3.select("#chart")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

// X 轴比例尺 (Band Scale 用于离散数据)
const x = d3.scaleBand()
  .domain(data.map(d => d.name))
  .range([0, width])
  .padding(0.1); // 柱子之间的间距

// Y 轴比例尺 (Linear Scale 用于连续数据)
const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)]).nice() // .nice() 使轴刻度更整齐
  .range([height, 0]);

// 添加 X 轴
svg.append("g")
  .attr("transform", `translate(0,${height})`)
  .call(d3.axisBottom(x));

// 添加 Y 轴
svg.append("g")
  .call(d3.axisLeft(y));

// 获取提示框元素
const tooltip = d3.select("#tooltip")
  .style("opacity", 0)
  .style("position", "absolute")
  .style("background-color", "white")
  .style("border", "solid")
  .style("border-width", "1px")
  .style("border-radius", "5px")
  .style("padding", "10px");

// 绘制柱子 (Rect)
svg.selectAll(".bar")
  .data(data)
  .enter()
  .append("rect")
  .attr("class", "bar")
  .attr("x", d => x(d.name))
  .attr("y", d => y(d.value))
  .attr("width", x.bandwidth())
  .attr("height", d => height - y(d.value))
  .attr("fill", "steelblue")
  // 添加鼠标交互
  .on("mouseover", function(event, d) {
    d3.select(this).attr("fill", "orange"); // 鼠标悬停改变颜色
    tooltip.transition().duration(200).style("opacity", .9);
    tooltip.html(`类别: ${d.name}<br/>值: ${d.value}`)
      .style("left", (event.pageX + 10) + "px")
      .style("top", (event.pageY - 28) + "px");
  })
  .on("mouseout", function(event, d) {
    d3.select(this).attr("fill", "steelblue"); // 恢复原来的颜色
    tooltip.transition().duration(500).style("opacity", 0);
  });
```

## 2. 折线图 (Line Chart)

标准的折线图模板，使用 `d3.line` 生成路径，并配置了曲线平滑效果。

```javascript
// 假设 HTML 中有一个 <div id="chart"></div>
const data = [
  { date: new Date(2023, 0, 1), value: 10 },
  { date: new Date(2023, 1, 1), value: 50 },
  { date: new Date(2023, 2, 1), value: 30 },
  { date: new Date(2023, 3, 1), value: 90 },
  { date: new Date(2023, 4, 1), value: 40 },
  { date: new Date(2023, 5, 1), value: 120 }
];

// 定义图表的边距和尺寸
const margin = { top: 20, right: 30, bottom: 30, left: 40 };
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// 创建 SVG 容器
const svg = d3.select("#chart")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

// X 轴比例尺 (Time Scale 用于日期时间)
const x = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);

// Y 轴比例尺 (Linear Scale)
const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)]).nice()
  .range([height, 0]);

// 添加 X 轴
svg.append("g")
  .attr("transform", `translate(0,${height})`)
  .call(d3.axisBottom(x));

// 添加 Y 轴
svg.append("g")
  .call(d3.axisLeft(y));

// 定义折线生成器
const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.value))
  .curve(d3.curveMonotoneX); // 使用曲线平滑过渡

// 绘制折线路径
svg.append("path")
  .datum(data) // 使用 datum 绑定单个数组元素给一个 DOM 元素
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 2)
  .attr("d", line);

// (可选) 绘制数据点
svg.selectAll(".dot")
  .data(data)
  .enter()
  .append("circle")
  .attr("class", "dot")
  .attr("cx", d => x(d.date))
  .attr("cy", d => y(d.value))
  .attr("r", 4)
  .attr("fill", "red");
```

## 3. 力导向图 (Force-Directed Graph)

展示节点与连线的网络图模板，使用 D3 内置的力模拟（Force Simulation），支持节点的拖拽。

```javascript
// 假设 HTML 中有一个 <div id="chart"></div>
// 节点与连线数据
const data = {
  nodes: [
    { id: "A", group: 1 },
    { id: "B", group: 2 },
    { id: "C", group: 2 },
    { id: "D", group: 3 },
    { id: "E", group: 3 }
  ],
  links: [
    { source: "A", target: "B" },
    { source: "A", target: "C" },
    { source: "B", target: "D" },
    { source: "C", target: "E" },
    { source: "D", target: "E" }
  ]
};

const width = 600;
const height = 400;

// 颜色比例尺用于不同组别
const color = d3.scaleOrdinal(d3.schemeCategory10);

// 创建 SVG 容器
const svg = d3.select("#chart")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

// 定义力模拟器 (Force Simulation)
const simulation = d3.forceSimulation(data.nodes)
  // link: 设定连线力，使用 id 作为标识
  .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
  // charge: 设定节点排斥力/吸引力 (负值表示互相排斥)
  .force("charge", d3.forceManyBody().strength(-200))
  // center: 设定图的中心点
  .force("center", d3.forceCenter(width / 2, height / 2));

// 绘制连线 (Links)
const link = svg.append("g")
  .attr("stroke", "#999")
  .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(data.links)
  .enter()
  .append("line")
  .attr("stroke-width", 2);

// 绘制节点 (Nodes)
const node = svg.append("g")
  .attr("stroke", "#fff")
  .attr("stroke-width", 1.5)
  .selectAll("circle")
  .data(data.nodes)
  .enter()
  .append("circle")
  .attr("r", 15)
  .attr("fill", d => color(d.group))
  // 绑定拖拽事件
  .call(drag(simulation));

// 添加节点标签
const label = svg.append("g")
  .selectAll("text")
  .data(data.nodes)
  .enter()
  .append("text")
  .attr("dy", 4)
  .attr("dx", -5)
  .attr("fill", "black")
  .attr("font-size", "12px")
  .text(d => d.id);

// 监听 tick 事件以更新坐标
simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);

  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);

  label
    .attr("x", d => d.x)
    .attr("y", d => d.y);
});

// 拖拽事件处理函数
function drag(simulation) {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  return d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
}
```
