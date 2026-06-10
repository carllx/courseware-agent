# 工作流：通道有效性评估与 3D/2D 决策 (Channel Effectiveness & 3D Justification)

## 1. Prerequisites & Context (先决条件与上下文)

**WHY (为什么需要评估通道有效性)：**
在信息可视化的空间域中，如何评价某个视觉通道（Visual Channel）比另一个更好？这是构建可视化系统时的核心依据。通道有效性通过五个关键指标来衡量：准确性、可辨识性、可分离性、视觉弹出（Popout）能力以及分组能力。同时，基于 **Weber 定律（韦伯定律）**，人类的感知系统本质上是基于**相对判断（Relative Judgments）**而非绝对判断的，这一前提深刻影响了视觉设计。

**WHEN (何时使用本工作流)：**
- 当你在为不同的数据属性选择视觉编码（Visual Encoding）时。
- 当你需要审查当前使用的视觉通道是否引起了冲突或误解时。
- 当你的团队尝试引入 3D 视图（3D Vis），你需要客观评估其必要性时。

> **Theory Deep Dive:**
> 如需查阅有关韦伯定律或 Bertin/Stevens/Cleveland 视觉通道分级的深度理论基石，请运行：
> ```bash
> bash scripts/query_theory.sh "What are the foundational theories behind visual marks and channel effectiveness by Bertin, Stevens, and Cleveland, and what is Weber's Law?"
> ```

---

## 2. Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 2.1 衡量通道有效性的五大原则
评估视觉编码设计应从以下五个维度综合考量：

1. **准确性 (Accuracy)**：
   - 优先选择沿着共同基准线对齐的位置编码（Aligned Position against a common scale）。
   - 我们对一维平面长度的感知最接近真实数值差异，对面积的感知通常会被**压缩**（低估），对色彩饱和度的感知会被**放大**（高估）。
   > ```bash
   > bash scripts/query_theory.sh "Detail Steven's Psychophysical Power Law and explain why the apparent magnitude exponent for length is 1.0 but area is compressed."
   > ```
   - ![](../../images/b3119f251df7f330a73f93086d2a3b9987404fbb68e789e1999a3d26e4e12e7f.jpg)

2. **可辨识性 (Discriminability)**：
   - 匹配范围：所选通道能提供的“可用辨识等级（Bins）”必须大于或等于需要编码的数据属性种类数。
   - 例如：线宽（Linewidth）通常只能提供 3 到 4 种视觉上清晰可辨的级别，不适用于具有几十种枚举值的数据。

3. **可分离性 (Separability) 与通道干扰**：
   - 视觉通道之间并非独立。需要留意其组合是**完全正交可分离的（Separable）**还是**内在整合的（Integral）**。
   - **推荐（分离）**：位置与色相（Position + Hue），观众可独立分离出两个变量。
   - **警告（整合）**：水平宽度与垂直高度，人类会自动将其融合成一个概念——面积（Area），无法再分离读取。使用 RGB 红绿轴也会融合成混合颜色，难以剥离解析原始值。
   - ![](../../images/9db2d16e02f22a05bd251e27ed5d07637330e0b032c76811a656eee828fbb369.jpg)

4. **视觉弹出 (Popout / Preattentive Processing)**：
   - 如果需要让某个特殊项立刻吸引注意力，且不受周围干扰项数量的影响，必须使用视觉弹出通道。
   - **关键限制**：视觉弹出只能针对**单个通道**生效。尝试组合两个通道（例如：在一堆红方块和蓝圆圈中找“红圆圈”）会导致弹出失效，被迫降级为线性耗时的**序列搜索（Serial Search）**。
   - 支持弹出的通道：颜色、倾斜度、尺寸、形状、阴影方向。
   > ```bash
   > bash scripts/query_theory.sh "Explain the mechanism of preattentive processing, popout speed, and why conjunctive searches fail to pop out."
   > ```
   - ![](../../images/8907137bc803689791357c5f88b7c421f36f65bfb77d81081a8aecd0f0833107.jpg)

5. **分组 (Grouping)**：
   - 为元素建立组别感知的层级（按强度排序）：包含（Containment，最强）> 物理连接（Connection）> 空间接近性（Proximity）> 相似性（Similarity，如同类颜色或运动方向）。
   - 注意使用形状和运动通道来分组时，不要使用容易引起混淆的复杂形状或过多的并发多向运动。

### 2.2 绝对判断陷阱与“无正当理由不用 3D”原则
人类感知是基于相对比较的，这不仅适用于大小长度，也适用于颜色（受周围环境光/色块影响）。
同时，3D 视图违背了多个二维平面赋予的准确性优势：

- **平面的力量 (The Power of the Plane)**：位置和长度编码的极高准确度仅适用于二维图像平面。
- **深度的视差 (The Disparity of Depth)**：对深度轴（Z轴）的长度估计是不准确的，其心理物理学幂指数极低（~0.67）。
- **遮挡的危害 (Occlusion)**：3D 布局会直接隐藏重要数据。强迫用户在 3D 中游历来合成认知，会极大增加记忆负荷和时间成本。
- **透视畸变 (Perspective Distortion)**：透视效果（近大远小）完全摧毁了“平面位置”和“尺寸”这两个最重要的视觉编码通道。用户将无法直接比较柱状图的高度。
  - ![](../../images/c412c50c7eae8695963e382eec60c66ab9f00069586803fe99a7a443c0779c88.jpg)
- **文字可读性破坏 (Tilted Text)**：只要文本不在图像平面上（发生倾斜），通常会遭遇严重的锯齿和渲染模糊问题。

**3D 唯一适用的合理场景：内在几何形状理解 (Shape Perception)**
当用户的任务核心是理解本就是三维结构的几何形态时（例如：流体力学流线、核磁共振医学影像、航空发动机模型），3D 及其带来的交互式空间漫游才利大于弊。

---

## 3. If/Then Troubleshooting Logic (故障排查与应对逻辑)

- **IF (如果)** 你需要在一个图表中展示 5 个以上的不同数据层级：
  - **THEN (那么)** 绝不能使用线宽（Linewidth）或简单形状。考虑转换为多个并排视窗（Small Multiples），或切换为空间位置、色相等具有更多辨识 Bin 的通道。

- **IF (如果)** 你在尝试同时使用水平宽度映射变量 A，垂直高度映射变量 B：
  - **THEN (那么)** 停止该方案。这会触发通道的内在整合性（Integrality），用户只会将其理解为“三类不同的面积（小、大、扁平）”，无法分离解读 A 和 B。应改为使用“位置 + 颜色”等完全可分离（Separable）的组合。

- **IF (如果)** 目标项在设计中未能实现预期的“立刻抓人眼球”的效果：
  - **THEN (那么)** 检查你是否同时叠加了多个维度进行区分（如寻找特定的形状加特定的颜色）。简化设计，确保目标项在至少**一个**独立通道上具有排他性的差异以触发视觉弹出（Popout）。

- **IF (如果)** 业务方要求制作“酷炫的 3D 柱状图 / 3D 散点图”：
  - **THEN (那么)** 坚决拒绝。指出这属于“非正当 3D”，透视畸变会破坏高度对比，互相遮挡会隐藏数据点。将 3D 图表展开重构为 2D 对齐图表或并排分面图。

- **IF (如果)** 颜色在不同区域看起来有严重偏差：
  - **THEN (那么)** 回顾韦伯定律的相对判断原理。排查是否是由于对比色的差异或背景渐变引发的“色彩/亮度恒常性”错觉（Color Constancy錯觉）。对所有带颜色编码的数据标记使用统一的灰色/中性色背景。

---

## 4. Verification Checklists (验证检查清单)

- [ ] **辨识度检查**：所有视觉通道所需的等级数量（Bins），是否全部落在了该通道的人类分辨极限内？
- [ ] **分离度检查**：图表中用于展示两个独立变量的视觉通道组合，是否属于正交且可分离（Separable）的类别？
- [ ] **视觉弹出检查**：如果依赖预注意（Preattentive）提示，是否确保了只依赖单一通道特征即可区分？
- [ ] **相对基准线检查**：是否为需要精确数值对比的图形元素（如条形图）提供了公共参考基准线或边框框架？
- [ ] **分组层次检查**：同组元素是否优先使用了最强感知暗示（包含或连接）或至少空间接近暗示？
- [ ] **3D 免疫检查**：如果使用了 3D 视图，该数据集是否具有先天的三维物理结构（如医疗成像）且任务需理解该形状？如不是，立刻降级为 2D。
- [ ] **抗遮挡与透视检查**：重要的数据标点和文字标签，是否避免了被空间透视所扭曲，并且完全不受遮挡影响？