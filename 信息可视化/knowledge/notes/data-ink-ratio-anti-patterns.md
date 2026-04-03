# 数据墨水比与可视化反面设计

> 来源：Munzner Ch6 §6.1-6.9 (Rules of Thumb); Tufte 1983 "The Visual Display of Quantitative Information"

## 核心论点

好的可视化设计是减法艺术。**每一滴墨水都必须为数据服务**，否则就是噪声。

### Tufte 的数据墨水比 (Data-Ink Ratio)
- 定义：数据墨水 / 总墨水 = 越接近 1 越好
- 规则：如果删掉某个图形元素（网格线、边框、装饰）后信息不减少 → 果断删掉
- 经典反面案例：3D 柱形图（深度通道浪费在装饰而非数据上）

### Munzner 八大经验法则 (Ch6)
1. **No Unjustified 3D**：3D 必须有正当理由（如形状理解任务），否则引入遮挡、透视失真、倾斜文字不可读三大灾难
2. **No Unjustified 2D**：使用二维布局也需证明比一维列表更有效
3. **Eyes Beat Memory**：让眼睛做比较，别让大脑记忆——并置 > 叠加 > 动画
4. **Resolution over Immersion**：分辨率比沉浸感更重要——大桌面屏幕通常优于 VR 头盔
5. **Overview First, Zoom and Filter, Details on Demand**：Shneiderman 的信息搜索箴言
6. **Responsiveness Is Required**：交互延迟 > 100ms 用户就感到迟钝
7. **Get It Right in Black and White**：先用灰阶验证信息是否清晰，颜色只是额外维度
8. **Function First, Form Next**：功能优先、形式随后——但两者缺一不可

### 3D 的五宗罪 (§6.3)
- **遮挡 (Occlusion)**：前方物体挡住后方，丢失信息
- **透视失真 (Perspective Distortion)**：远处的物体看起来更小，长度/面积通道失效
- **深度感知差异 (Depth Disparity)**：我们对深度的感知精度远低于平面位置
- **倾斜文字不可读 (Tilted Text)**：文字必须正面朝向观察者
- **唯一合理场景**：任务本质就是"理解 3D 形状"（如流体力学流线可视化）

### DMA 艺术生的设计陷阱
- 倾向追求"炫酷"的 3D 旋转效果 → 实际上牺牲了数据可读性
- 过度装饰（渐变阴影、纹理填充）→ 增加认知负荷而非信息密度
- AI 生成的默认图表带有冗余网格线、丑陋的默认边框 → 需要人工精修减法

## 反面论据（双覆盖）

- 极端极简可能导致"过度删减"：去掉所有参考线后，读者失去定位锚点
- Function First ≠ 丑陋的工程图表。DMA 专业需在极简与审美之间找到平衡
- Tufte 的观点在信息仪表盘场景下是黄金法则，但在数据艺术/生成艺术语境中可以有节制地打破

## 教学关键词
`data-ink-ratio`, `no-unjustified-3D`, `occlusion`, `perspective-distortion`, `eyes-beat-memory`, `function-first`, `Tufte`
