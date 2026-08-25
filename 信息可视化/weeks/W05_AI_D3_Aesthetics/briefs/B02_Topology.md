---
week: W05
brief_id: B02
title: "排列空间数据与网络/树结构"
textbook: "Visualization Analysis & Design, Tamara Munzner, 2014"
chapters: ["8", "9"]
covers_modules: ["M02"]
status: complete
---

## 教材位置
- 原著：Tamara Munzner, *Visualization Analysis & Design*, 2014
- 章节：
  - Chapter 8 — Arrange Spatial Data
  - Chapter 9 — Arrange Networks and Trees

---

## 核心知识提取

### 第8章：排列空间数据 (Arrange Spatial Data)

- **大局观 (The Big Picture)**
  对于具有空间语义的数据，常见的布局选择是直接利用给定的空间信息。此时，空间位置(Spatial Position)不用于编码其他属性，因为它本身就是传达空间关系的最有效通道。主要分为两大类：**几何数据(Geometry)**和**空间场(Spatial Fields)**。
- **几何数据 (Geometry)**
  几何数据直接通过空间位置传达形状信息，最常见的来源是地理信息(Geographic Data)。例如：**等值区域图(Choropleth Maps)**，它利用给定的地理边界作为面积标记(Area Marks)，并用颜色来编码区域的定量属性。
- **标量场 (Scalar Fields: One Value)**
  每个空间单元格关联一个标量值。视觉编码的三大家族为：
  1. **切片(Slicing)**：每次仅展示二维切面图像。
  2. **等值线/面(Isocontours)**：计算出特定标量值的低维表面几何形状。
  3. **直接体绘制(Direct Volume Rendering)**：不生成中间几何结构，直接利用所有3D空间信息生成图像，其核心在于设计多维**传递函数(Transfer Function)**以将数值变化映射为颜色和不透明度。
- **矢量场与张量场 (Vector and Tensor Fields)**
  矢量场含方向和大小，张量场更复杂。它们有四个主要的编码习语家族：**流动图符(Flow Glyphs)**展示局部信息；**几何流(Geometric Flow)**从稀疏种子点追踪得出几何轨迹；**纹理流(Texture Flow)**利用密集的种子点覆盖；**特征流(Feature Flow)**通过全局计算显式检测特定的流体特征。

### 第9章：排列网络与树 (Arrange Networks and Trees)

- **节点链接图与连接标记 (Node-Link Diagrams & Connection Marks)**
  - **核心概念**：这是最普遍的网络与树布局习语。节点使用点标记(Point Marks)绘制，连接它们的链接使用线标记(Line Marks)。连接标记支持离散的路径追踪(Path Tracing)，非常适合理解网络**拓扑结构(Topology)**。
  - **力导向布局 (Force-Directed Placement)**：通过模拟物理力（节点像电荷般相互排斥，链接像弹簧般相互吸引）进行布局。空间位置不直接编码属性，而是算法用于尽量减少节点重叠与边交叉的副产物。
  - **Hairball 问题 (毛线球难题)**：力导向布局在小规模网络（数十节点）表现极佳，但其具有明显的**可扩展性(Scalability)**短板。当节点数量增加至几百个以上，或者链接密度超过节点数的4倍左右时，大量的线条重叠会导致视觉遮挡灾难，网络退化为无法阅读的**毛线球(Hairball)**，使得路径追踪和结构理解几乎不可能。
- **矩阵视图 (Matrix Views)**
  - **核心概念**：网络可以转换为派生的表格数据，并通过**邻接矩阵(Adjacency Matrix)**展示。所有节点沿长宽两轴排列，节点间的链接由单元格中的区域标记(Area Marks)颜色或状态来表示。
  - **利弊权衡 (Costs and Benefits)**：
    - **优势**：矩阵视图具有极高的感知可扩展性，完全消除了节点链接图带来的视觉遮挡(Occlusion)问题，最高可支持展示百万级甚至更密集的关系网络。此外，它布局稳定且支持**重新排序(Reordering)**，利于快速查找指定节点或聚类区块。
    - **劣势**：不符合常规直觉，用户往往需要训练才能辨识诸如"团(Clique)"等图案。更致命的是，它缺乏对拓扑结构（如多跳路径）的直观追踪支持。
- **包含：层次标记 (Containment: Hierarchy Marks)**
  - 对于树(Trees)和复合网络(Compound Networks)，可使用包含(Containment)或嵌套标记来表现层级结构。典型如**矩形树图(Treemaps)**，利用嵌套矩形面积展示属性，极其适合查找叶子节点的数据分布，但在展现拓扑路径上不如节点链接图。

---

## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig 8.2 | 等值区域图 (Choropleth Maps) | ![](images/4ac5f11c3fe0ac72695d21a390df6093e1611f592406d7f4f9d1aa52ec589b72.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_8_2.webp` |
| Fig 9.4 | 力导向布局 (Force-Directed Layouts)(a) | ![](images/67b56107f23eb11c54a6eb1496732d43c77fa7ed063a93b396039ab8173dd33e.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_4.webp` |
| Fig 9.4 | 力导向布局 (Force-Directed Layouts)(b) | ![](images/7c8d9dd4e1f993e65f6bb779565ebc9b565c14da1f20844a97cbe258d885a8e6.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_4.webp` |
| Fig 9.5 | sfdp算法结构可见 (a) | ![](images/201f411f5ad8f4f07c20fede300241e0257e49f1079fb49da7aa1c298e4f6c8c.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_5.webp` |
| Fig 9.5 | 毛线球问题 (Hairball) (b) | ![](images/62e78393203182b4d2369bd894da2b1e115d0c1fe09ec04e4ba9a037a7f60ca6.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_5.webp` |
| Fig 9.6 | 节点链接图与邻接矩阵视图对比 (a) | ![](images/ab918f43b2a8a3a98c995f65ac269275fa11aefc79de9683e51e99012a43c72e.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_6.webp` |
| Fig 9.6 | 节点链接图与邻接矩阵视图对比 (b) | ![](images/ec80f2e2bcf3b1fd4209df928c8d74b2172544f4bb1e6dab047425fa3ca45571.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_6.webp` |
| Fig 9.6 | 节点链接图与邻接矩阵视图对比 (c) | ![](images/f9959abcfd4b3f9375e04b099ce2df1ccff25e74d65a97ffef0310ce45899be7.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_6.webp` |
| Fig 9.8 | 树图 (Treemaps) | ![](images/276175e811b4fba43da756768954eb6a289ce2fb23498ed806e4eeaefcd3a91b.webp) | ✅ 已迁移 <br> `../public/textbook/Fig_9_8.webp` |

---

## 易混淆概念辨析

- **节点链接图 (Node-Link Diagram) vs 邻接矩阵 (Adjacency Matrix)**：
  - **核心区别**：节点链接图使用线段连接节点，直观展现网络拓扑结构（如连通性、找最短路径），但在网络稠密时极易产生遮挡死角。邻接矩阵则用网格像素色块标定关系，完全没有物理线段的遮挡，能在极高密度下维持清晰呈现，但几乎丧失了"追踪多级关联跳数"的直觉体验。
  - **教学风险**：在教学中，容易误导学生任何网络都可以无脑使用节点链接图，需强化"链路密度突破阈值时必须妥协转用矩阵"的工程意识。

- **标量场等值面 (Isocontours) vs 直接体绘制 (Direct Volume Rendering)**：
  - **核心区别**：等值面是做减法，抽取出特定的二维切片或表面几何图形抛弃其余部分；直接体绘制是全盘保留，不推导中间几何形态，而是用类似 X光穿透的方法通过函数直接投射完整的三维信息。

---

## 与逐字稿的对照检查表

- [ ] `CHK-B02-01`: 阐明在空间数据中为何优先使用基于物理实在的"空间位置"作布局，而不是随意用于映射其它维度。
- [ ] `CHK-B02-02`: 确保强调 Node-Link Diagram 对于寻找多跳网络连接的直觉优势。
- [ ] `CHK-B02-03`: 必须引入力导向布局的扩展极限，提及 "Hairball" 现象及 L > 4N 的坍塌临界点。
- [ ] `CHK-B02-04`: 在讲解大规模网络时，必须对比引入"邻接矩阵(Adjacency Matrix)"，强调其消除视觉遮挡的战略价值。
