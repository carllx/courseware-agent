# 视觉编码通道：色盲友好与替代通道设计 (Visual Encoding Channels: Colorblind Safety and Alternative Channels)

## 前置条件与上下文 (Prerequisites & Context)

在进行可视化设计时，必须考虑到红绿色盲（影响约8%的男性和0.5%的女性）等常见的视觉缺陷。当基本的位置和颜色通道不足以表达多维数据，或者需要确保所有人都能准确读取信息时，设计者需要引入其他的视觉通道（如大小、角度、形状、纹理和运动）。

**深入探索指令 (Progressive Disclosure)**:
如果需要深入了解特定通道的理论基础，请通过运行时代理 (Runtime Agent) 动态获取：
- `bash scripts/query_theory.sh "What is the physiological basis of red-green color blindness and opponent color theory?"`
- `bash scripts/query_theory.sh "How do Stevens' power law exponents apply to area and volume perception in visual encoding?"`
- `bash scripts/query_theory.sh "What are the historical and technical reasons behind red-green usage in the bioinformatics domain?"`

## 综合指南与最佳实践 (Comprehensive Guide & Best Practices)

### 1. 色盲友好的色表设计 (Colorblind-Safe Colormap Design)
- **视觉混淆的范围**：红绿色盲患者不仅难以区分红与绿，还常常混淆红与黑、蓝与紫、浅绿与白、以及棕与绿。
- **核心启发式规则**：**永远不要仅仅依赖色相 (Hue) 来编码信息**。在设计分类色表时，必须结合亮度 (Luminance) 或饱和度 (Saturation) 的变化。
- **避免高风险组合**：极力避免强调红绿的色表，尤其是发散型红绿渐变色 (divergent red-green ramps)。
- **兼容领域惯例**：如果某些领域强行要求使用红绿配色，必须通过确保红色和绿色之间有明显的**亮度差异**来适应用户的预期。
- **实操测试**：将设计导入 Adobe Illustrator/Photoshop 或使用在线模拟器（如 rehue.net, color-blindness.com, etre.com/tools/colourblindsimulator）进行色盲模拟验证。

### 2. 大小通道：长度、面积与体积 (Size Channels)
- **精准度层级**：长度（1D）感知极度准确 > 面积（2D，指数约为 0.7）感知精度中等 > 体积（3D）感知极不准确。
- **通道组合限制**：严禁同时使用高维大小（如面积）和低维大小（如长度）来分别编码不同的数据维度。这会导致感知上的“整体性 (integral)”混淆，用户可能会走捷径仅评估长度。
- **相互作用**：标记的大小会严重影响其他通道。如果区域过小，形状或颜色饱和度的编码将无法被识别。

### 3. 角度与倾斜通道 (Angle and Tilt Channels)
- **非均匀的感知精度**：人类对接近水平（0°）、垂直（90°）和对角线（45°）的角度判断极其精确，但在中间角度（如37°与38°之间）精度急剧下降。
- **数据类型适配**：
  - **顺序型 (Sequential)**：在90°单象限内使用线段或箭头。
  - **发散型 (Diverging)**：在180°双象限内使用箭头，中心垂直位置代表中性零点。
  - **循环型 (Cyclic)**：使用不对称标记（如箭头）在360°全圆内循环。
- **参考图例**：
  - 顺序型属性：
    ![Sequential ordered line mark](../../images/8eb2f4c74f5e8ca142b108052b705794243c5cb935fe9dda7008450b6f6212e8.jpg)
  - 发散型属性：
    ![Diverging ordered arrow glyph](../../images/cd235b06acf699424c0c69619b3e6fa7b20138c72913e3698f3f071b5ec19a52.jpg)
  - 循环型属性：
    ![Cyclic ordered arrow glyph](../../images/ae1b964ce4a97af05cf86415fd49c3255dfbeed87b36325ad8e80d20d64e3aaf.jpg)

### 4. 形状与曲率通道 (Shape and Curvature Channels)
- **形状 (Identity Channel)**：最适合点标记 (Point marks)；用于线标记时呈现为点画线 (Stippling)。**严禁**应用于面标记。
  - *容量限制*：大尺寸下可分辨数十种形状；若限制在极小区域（如10x10像素），仅能分辨约12种。
  - *基底选择*：复杂的形状（如十字形）可用像素少，会严重削弱颜色的表达。推荐使用实心形状（如圆盘）来承载颜色编码。
- **曲率 (Magnitude Channel)**：精度极低，仅能提供 2-3 个可辨识的档位，且只能用于线标记。

### 5. 运动通道 (Motion Channels)
- **高显著性与可分离性**：运动（方向、速度、闪烁）极度吸引注意力，与其他静态通道高度分离。
- **使用节制**：由于它几乎无法被忽略，**应仅用于二元分类**（如：移动 vs 静止）或短暂的高亮状态（如鼠标悬停、点击）。
- **慎用闪烁**：闪烁 (Flicker) 非常容易引起反感，仅限用于动态布局中极其强烈的短暂强调（如大量新元素刚加入视图的瞬间）。

### 6. 纹理与点画 (Texture and Stippling)
- **视觉维度**：由方向、缩放比例和对比度（亮度）组合而成。
- **容量评估**：在精心设计下，纹理可支持数十种分类数据的辨别；对于有序数据，每个维度的分辨能力建议不超过 3-4 个档位。

## 条件排障逻辑 (If/Then Troubleshooting Logic)

- **如果 (If)** 用户在识别分类色表时频繁发生混淆（尤其是红/绿、蓝/紫等组合），**那么 (Then)** 立即通过色盲模拟器检查色表，并引入基于亮度 (Luminance) 和饱和度 (Saturation) 的辅助阶梯差异，而不再单独依赖色相。
- **如果 (If)** 你的数据模型需要表达高精度的数值对比，**那么 (Then)** 必须优先使用长度 (Length) 通道，果断放弃使用精度较弱的面积 (Area) 或体积 (Volume) 编码。
- **如果 (If)** 角度编码的微小数值差异在某些区域难以被用户察觉，**那么 (Then)** 检查这些角度是否落在了 0°、45° 或 90° 以外的“感知盲区”（如 37°），考虑重新映射以对齐高精度感知基准线。
- **如果 (If)** 必须使用形状通道来表达大量（十几种以上）的分类，**那么 (Then)** 确保该图元标记的基础尺寸足够大，否则视觉上将无法有效区分局部特征。
- **如果 (If)** 图表界面中存在闪烁或持续运动的元素导致用户分心，**那么 (Then)** 立即更改为由轻量级交互（如 Hover）触发的瞬时高亮，或只保留简单的二元运动状态。

## 验证检查表 (Verification Checklists)

- [ ] 所有色彩方案均已通过色盲模拟器 (Color blindness simulator) 的有效性测试。
- [ ] 色表中没有单纯依靠色相 (Hue) 差异来进行编码的情况，已添加了亮度和饱和度变化。
- [ ] 确保多维大小编码（如混合使用长度和面积）未被错误地用于表示不相关的数据维度。
- [ ] 关键的角度感知阈值已对齐到 0°、45° 或 90° 这三个高精度感知锚点。
- [ ] 形状通道仅被应用于点标记或线标记，绝对未被应用于面标记 (Area marks)。
- [ ] 动态与运动效果仅限用于临时的高亮提醒，且去除了任何非必要的干扰性闪烁。
- [ ] 引用的所有图片路径均已重写为相对 `workflows` 目录的正确相对路径。