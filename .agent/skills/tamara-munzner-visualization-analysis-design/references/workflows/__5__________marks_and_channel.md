# Workflow: 视觉编码核心 - 标记与通道 (Marks and Channels)

## Prerequisites & Context (先决条件与背景)
在开始视觉编码设计之前，明确数据属性的类型（有序数据 vs. 分类数据）。标记 (Marks) 构成了图形的骨架，而通道 (Channels) 控制了这些骨架的视觉属性。正确选择标记与通道是图表表达性 (Expressiveness) 和有效性 (Effectiveness) 的基础。

> [!NOTE]
> 深入探索：如果需要了解本理论体系在人类视觉感知上的底层认知科学实证基础，请执行以下命令获取补充理论：
> ```bash
> bash scripts/query_theory.sh "What are the cognitive science foundations for the separation of Identity and Magnitude channels?"
> ```

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 1. 明确数据的核心维度
在设计前，必须将待编码的数据集拆解为“节点/个体 (Items/Nodes)”和“关系/链接 (Links)”。
- 如果展示**个体**：选择几何图元作为标记。
- 如果展示**关系**：使用连接 (Connection)（如线段） 或者是包含 (Containment)（如面嵌套）标记。绝对不要使用点来表示链接。

### 2. 选择合适的标记 (Marks)
根据你想赋予通道的数量和自由度，考虑几何维度约束来选择标记：
- **点 (Point) - 0D**：最自由，无任何物理维度约束，可挂载所有通道属性（空间位置、颜色、尺寸、形状）。
- **线 (Line) - 1D**：已经被长度约束，只能利用宽度、颜色或者空间位置来挂载新数据。
- **面 (Area) - 2D**：被形状和面积完全约束（如地图的省份轮廓），只能通过颜色或空间位置附加维度。严禁在面上叠加尺寸通道。

![](../../images/2c40271ff1f1c92ebd6568da369fbcbd922bbb30ada3054703006029a94217a9.jpg)

> [!TIP]
> 深入探索几何图元的原子组合约束机制：
> ```bash
> bash scripts/query_theory.sh "How do geometric constraints limit the atomic combination of Marks and Channels?"
> ```

### 3. 选择正确的通道 (Channels)
通道两大认知阵营的分类直接决定了你能多大程度上传达数据的本质特征：
- **有序数据 (Ordered data)** 必须使用 **量化通道 (Magnitude Channels)**：
  - 首选：**对齐的空间位置 (Position on common scale)** - 绝对王者。
  - 备选：未对齐空间位置、长度 (1D)、角度、面积 (2D)、深度、颜色明度/饱和度等。
- **分类数据 (Categorical data)** 必须使用 **身份通道 (Identity Channels)**：
  - 首选：**空间区域划分 (Spatial region)** - 最有效的分类法。
  - 备选：颜色色相 (Color hue)、运动模式、形状等。

*(注：空间位置通道 (Spatial position) 是唯一对两类数据都最有效的通道，将绝对主导观众对数据的心理模型。)*

![](../../images/ba68902f44c8e7e18ddcbe9a8ef1cc59c2e5f0989cc8a207876eb87e3da630da.jpg)

### 4. 遵循设计的两条铁律 (Rules of Marks and Channels)
- **表达性原则 (Expressiveness)**：视觉编码必须且仅能表达数据集中的底层信息属性。切勿使用带有顺序暗示的通道（如大小、长度）来呈现分类数据，反之亦然。
- **有效性原则 (Effectiveness)**：数据属性的重要性应与视觉通道的显著性排名相匹配。最重要的属性分配给排名最高的通道。

### 5. 考虑视觉感知的物理与心理边界
在组合多个通道时，注意以下科学实证规律：
- **相对判断与绝对判断**：人类倾向于进行相对比较（韦伯定律）。提供对齐基准或边框能指数级提升判断精度，因此柱状图永远是量化比较之王。
- **可分离性 (Separability)**：避免使用不可分离的通道组合（例如红绿光效组合会融合成黄色、水平宽度加垂直高度会融合成面积错觉）。
- **视觉弹出 (Popout)**：要在密集数据中凸显目标，务必只在**单一通道**上制造差异。同时组合两个通道（如又改形状又改颜色）将破坏预先注意处理，导致变为逐个扫描。
- **准确性 (Accuracy)**：依据 Stevens 幂定律，人类对长度感知是完美的线性 ($n=1.0$)，对面积感知有心理压缩 ($n=0.7$)，对色彩饱和度感知有放大 ($n=1.7$)。

![](../../images/b3119f251df7f330a73f93086d2a3b9987404fbb68e789e1999a3d26e4e12e7f.jpg)

> [!WARNING]
> 对视觉感知谬误和 Stevens 心理物理学定律的深入探讨：
> ```bash
> bash scripts/query_theory.sh "Explain Stevens' Psychophysical Power Law and its exact application on area vs length perception in charts."
> ```

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 分类数据的类目种类过多（例如 >10 种），且主要依赖颜色色相（Hue）来区分，
  - **THEN** 颜色通道会因“可辨识性 (Discriminability)”超出阈值而失效。应切换到**空间区域 (Spatial region)** 或进行数据分层/聚类以减少同级类别数。
- **IF** 你使用圆的面积或球体体积表示核心定序指标，且发现用户在解读时估算出的数值差异总是偏小，
  - **THEN** 这是由于大脑对 2D/3D 尺寸的感知压缩 ($n=0.7$) 导致的。应当将其降级为 1D 长度（线段），或重新映射到对齐的空间位置上。
- **IF** 你的图形试图用红色和绿色在同一个图元上分别强调两个独立的定量信息，但用户反映难以解读，
  - **THEN** 这引发了“极端不可分离 (Integral Channels)”现象。应将其中一个定量指标改为长度、大小或空间位置。
- **IF** 在高密度散点图中，重点的“异类”数据没有跳脱出来被立刻注意到，
  - **THEN** 你很可能对异类点使用了组合通道策略（例如寻找红色的圆形）。想要触发完美的“视觉弹出 (Popout)”，请撤销多余通道，保证异类点和干扰背景只有单一维度的高对比差异。
- **IF** 你发现原本有连续顺序的变量被随意赋予了分类色板（例如红色、黄色、蓝色相配），
  - **THEN** 违反了表达性原则，暗示了无序性且打断了原有顺序。必须将颜色通道变更为**明度 (Luminance)** 或**饱和度 (Saturation)**。

## Verification Checklists (验证清单)

### 1. 通道匹配与表达性检查
- [ ] 数据集是否已清晰划分为节点（Items）和关系（Links）？链接是否采用了线段连接或包含（面嵌套）？
- [ ] 所有的**定序数据**是否完全映射在**量化通道**（位置、长度、角度、明度等）？
- [ ] 所有的**分类数据**是否完全映射在**身份通道**（区域、色相、形状等）？
- [ ] 最关键、优先度最高的业务指标，是否占据了量化通道榜单之首的**对齐空间位置**？

### 2. 视觉组合与干扰检查
- [ ] 挂载的多重通道是否都在“可分离性连续体”的安全区间内？
- [ ] 是否检查并避免了因为标记本身的几何维数（例如在 2D 面积上继续添加尺寸通道）导致规则冲突？
- [ ] 若存在颜色编码，是否充分考虑了颜色感知的上下文依赖（色彩恒常性错觉），确保底色与图表对比的一致性？

### 3. 可读性与边界检查
- [ ] 所选通道包含的可辨认阶梯（Bins）数是否足以承载数据基数？（例如：线宽最多区分 3-4 种，不可强行映射广泛数值范围）。
- [ ] 需要视觉弹出效应的目标，是否遵循了单一维度特征的原则？
- [ ] 进行比较设计时，是否提供了足够的**相对判断辅助**（如对齐基线、等长刻度边框）？

> [!IMPORTANT]
> 执行前终极检验：
> 如果对当前设计中通道“有效性排名”及应用仍存疑虑，请最后查阅效能排行榜单：
> ```bash
> bash scripts/query_theory.sh "List the exact channel rankings and hierarchy for both Magnitude and Identity channels."
> ```