# 字体排印与现代色彩体系构建 (Typography & Color System Workflow)

## Prerequisites & Context (前提条件与上下文)

在用户界面设计中，字体的微调（特别是字距）与色彩系统的科学构建直接决定了界面的专业度与一致性。使用纯感觉进行设计往往会导致决策疲劳并产生几十种相似但混乱的色值。本工作流旨在将字体排印微调以及系统化的色彩搭建转化为可操作的步骤。

> **Progressive Disclosure (渐进式披露)**：
> 若需要深入了解关于字体设计的核心原则或色彩空间计算原理，请执行以下命令获取更多理论依据：
> ```bash
> bash scripts/query_theory.sh "What are the structural differences between sentence-case and all-caps text readability?"
> bash scripts/query_theory.sh "How does perceived brightness work in human visual perception and the HSL color space?"
> ```

## Comprehensive Guide & Best Practices (全面指南与最佳实践)

### 1. 巧妙使用字距 (Use Letter-Spacing Effectively)
一般情况下，应当信任字体设计师的默认设定。但在以下特定场景中，主动调整字距将极大改善设计质感：

*   **收紧标题字距 (Tightening Headlines)**：
    像 Open Sans 这样为正文小字优化的字体通常默认字距较大。当将其用于大号标题时，**应适当减小字距 (Decrease letter-spacing)**，以模拟专为标题设计的压缩感（如 Oswald 字体）。
    *不要反向操作：专用的标题字体即使加大字距，也极难在小尺寸下保持高可读性。*
    ![](../../images/index-134_1.png)
    ![](../../images/index-134_2.png)

*   **提升全大写字母的可读性 (Improving All-Caps Legibility)**：
    默认字距针对的是首字母大写、其余小写的“句子拼写”模式。小写字母拥有丰富的视觉变化（x-height, ascenders, descenders），而全大写字母高度一致，极易糊在一起。因此，对于全大写文本，**必须增加字距 (Increase letter-spacing)** 以提升辨识度。
    ![](../../images/index-133_1.png)
    ![](../../images/index-133_2.png)

### 2. 构建系统化的 HSL 色彩体系 (Working with Color)

#### 摒弃 Hex，拥抱 HSL
Hex 和 RGB 无法直观反映颜色间的视觉关系。在前端开发和设计中应切换到 **HSL（色相、饱和度、亮度）** 模型：
*   **Hue (色相)**: 在色环上的位置（0° 红, 120° 绿, 240° 蓝）。
*   **Saturation (饱和度)**: 颜色的鲜艳程度（0% 为灰，100% 为极其鲜艳）。
*   **Lightness (亮度)**: 0% 是黑，100% 是白，50% 是纯正的色相本色。
*(注意：请区分 HSL 与 HSB/HSV，Web 标准仅支持 HSL)*

#### 你需要的颜色远比想象中多
不要依赖只能生成 5 个颜色的配色生成器。构建真实应用需要：
1.  **灰阶 (Greys)**: 文字、背景、边框通常都使用灰色。**准备 8-10 个不同层级的灰度**，避免在纯黑与白之间找不到合适的过渡。
2.  **主色 (Primary Colors)**: 1-2 种用于主要操作和品牌基调，配备 5-10 个明暗色阶。
3.  **辅助色/状态色 (Accent Colors)**: 用于强调（如黄色/粉色/青色）、破坏性操作（红色）、警告（黄色）、成功（绿色）。同样需要各自的色阶系统。

#### 提前定义色板层级 (Define your shades up front)
严禁使用 CSS 的 `lighten()` 或 `darken()` 动态生成色阶，这会导致颜色数量失控。应在设计初期手动定义色带（如 100 到 900）：
*   **第一步**：选择**基础色 (Base Color, 500层级)**。通常寻找能够完美作为按钮背景色的色度。
*   **第二步**：寻找**边界 (The Edges, 100 和 900)**。最暗的 900 往往用于文本，最亮的 100 用于背景微光填充（如 Alert 框的背景）。
*   **第三步**：**填补空白 (Filling the gaps)**。从 500 到 900 之间取中间值（700），以此类推，逐步填满 100, 200, 300... 900 共 9 个色阶。
![](../../images/index-151_1.png)

#### 亮度与饱和度的平衡艺术 (Don't let lightness kill your saturation)
当颜色的 Lightness 接近 0% 或 100% 时，它会显得苍白（Washed out）。
*   **增加两端饱和度**：当你向暗或向亮移动色阶时，**务必增加饱和度 (Saturation)**，以保持色彩的活力。
*   **利用“感官亮度”旋转色相 (Rotating Hue for Brightness)**：
    不同色相天生具有不同的亮度（如黄色看起来永远比蓝色亮）。为了使颜色变亮但不失真，可以**将色相 (Hue) 向最近的明亮色调（60°黄, 180°青, 300°洋红）旋转**。
    为了使颜色变暗且深邃，**将色相向最近的暗色调（0°红, 120°绿, 240°蓝）旋转**。*(旋转幅度保持在 20-30° 以内避免色变)*。
    ![](../../images/index-155_1.png)
    ![](../../images/index-156_2.png)

#### 灰色的情感温度 (Greys don't have to be grey)
正宗的 0% 饱和度灰色在界面中通常显得冰冷死板。
*   **冷灰 (Cool Greys)**：为灰色注入少许蓝色饱和度。
*   **暖灰 (Warm Greys)**：为灰色注入少许黄色或橙色饱和度。
*(注意：最亮和最暗的灰色层级需要更高的饱和度来维持一致的温度感)*
![](../../images/index-159_1.png)
![](../../images/index-162_1.png)

#### 无障碍设计与视觉美感并存 (Accessible doesn't have to mean ugly)
WCAG 规范要求常规文本具有 **4.5:1** 的对比度。但在彩色背景上应用彩色文本时极难达到合规。
*   **翻转对比度 (Flipping the contrast)**：不要在暗彩色背景上用白色文本，这太抢眼了。改为**在极浅的彩色背景上使用深色的彩色文本**，以达成柔和的无障碍对比度。
*   **色相旋转突破亮度瓶颈**：如果必须在彩色背景上显示彩色次要文本，为了达到对比度同时避免发白，**旋转文本的色相**向邻近的亮色（Cyan, Magenta, Yellow）偏移，从而在不提高 Lightness 参数的前提下获得充足的可视度。
    ![](../../images/index-165_2.png)
    ![](../../images/index-166_1.png)

> **Deep Dive**:
> `bash scripts/query_theory.sh "What are the WCAG 4.5:1 formulas and how do color palettes effectively clear these checks dynamically?"`

## If/Then Troubleshooting Logic (条件排障逻辑)

*   **IF** 一段较小尺寸的字体感觉过于松散，
    **THEN** 检查它是否使用了默认字距极大的正文字体。考虑维持原状（正文确实需要较大字距），如果是作为标签，可小幅缩小字距并调高字重。
*   **IF** 全大写按钮或标签阅读困难、黏连在一起，
    **THEN** 立即增加字母间距（Letter-spacing），直到每个字符清晰独立。
*   **IF** 你的界面显得阴暗死板，颜色偏脏偏褐，
    **THEN** 检查你的暗色阶是否只调低了 Lightness。尝试提高暗色阶的 Saturation，并将 Hue 微微向蓝色、紫色或红色偏移。
*   **IF** 无障碍对比度测试失败，且调低 Lightness 会让颜色变成沉闷的灰色，
    **THEN** 翻转你的 UI 层级：用 100/200 极浅色作为背景，用 800/900 深色作为文本色调。
*   **IF** 你的色板中灰色与你的主色(Primary Color)风格冲突，
    **THEN** 将你的灰色色温（通过添加色相和饱和度）向你的主色微微偏移，使其呈现统一的色调。

## Verification Checklists (验证清单)

- [ ] 大号标题（尤其是使用专为正文设计的字体时）已适当收紧了字距。
- [ ] 所有使用全大写字母的 UI 元素（如小标签、按钮）都应用了宽字距。
- [ ] 代码库与设计令牌中完全淘汰 Hex/RGB，统一使用 HSL 色值声明。
- [ ] 色彩系统具备 8-10 个连续且合理的灰阶调色板，并注入了一致的色温（冷或暖）。
- [ ] 主色、状态色均拥有一套从 100 到 900、通过亮度/饱和度/色相联调得出的色阶系统。
- [ ] 颜色的明暗色阶变化使用了“色相旋转”技巧，颜色依然保持浓郁不发灰。
- [ ] UI 层面的主要文本色彩符合 WCAG 4.5:1 对比度要求，且非重点背景色没有过度抢占注意力（采用了浅色底深色字策略）。
- [ ] 所有文档引用的原图路径均正确重写为 `../../images/` 相对路径。