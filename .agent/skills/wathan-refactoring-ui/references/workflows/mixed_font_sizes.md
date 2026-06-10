# 启发式工作流：混合字体大小与基线对齐 (Mixed Font Sizes & Baseline Alignment)

## 1. 前置条件与上下文 (Prerequisites & Context)
- **应用场景 (WHEN)**: 当同一行内出现不同字号的文本时（例如：大号的商品价格与小号的货币符号、标题后紧跟小号的“标签/日期”、大号数字指标旁边的百分比变化）。
- **理论依据 (WHY)**: 文本有其自身的解剖学结构。所有字母都“坐”在一条看不见的线上，这条线称为基线（Baseline）。如果仅仅使用标准的垂直居中对齐（Center Alignment），由于大字号和小字号文本的几何中心不同，视觉上小字会显得悬浮在半空中或者下沉，导致界面显得杂乱和不专业。对齐基线能保持文本排版的重心稳定。

## 2. 综合指南与最佳实践 (Comprehensive Guide & Best Practices)
- **坚守基线对齐（Baseline Alignment）**
  - 在混排多字号文本时，绝对不要使用 `align-items: center`，必须替换为 `align-items: baseline`。
  - 这种做法确保所有文字的底部边缘（忽略下降部如 g, y）都在同一条水平线上，模拟传统印刷品中的排字效果。
- **CSS Flexbox 实现细节**
  - 构建一个 Flex 容器：`display: flex; align-items: baseline;`。
  - 这种布局不仅适用于文字，也适用于内联元素（Inline elements），它能自然地让不同尺寸的文本显得是一个整体。
- **视觉平衡感**
  - 当小字号跟在大字号后面（例如 "$19.99 /month"），基线对齐能让用户的视线平稳过渡，避免视线跳跃引起的疲劳。
  - 注意字重（Font Weight）的配合：小字号往往需要稍微加粗（如增加到 Medium 或 Semibold），以平衡它与大字号之间的视觉重量（Visual Weight）。

## 3. 如果/那么 故障排除逻辑 (If/Then Troubleshooting Logic)
- **IF** 你应用了 `align-items: baseline` 但发现图标（Icon）的对齐完全崩溃了，**THEN** 这是因为 SVG 图标通常没有字体基线数据。解决方法是将图标与文本分别包装，对纯文本组使用基线对齐，再将图标与文本组整体进行 `align-items: center` 对齐；或者通过相对定位（`top: Xpx` / `transform: translateY()`）手动进行光学补偿微调。
- **IF** 使用基线对齐后，行高（Line Height）导致父容器异常撑开，**THEN** 检查并统一大字和小字的行高策略。有时候需要将内部包裹元素设置为 `line-height: 1` 消除多余的行距干扰。
- **IF** 设计工具（如 Figma）中对齐良好，但在前端实现时偏移，**THEN** 检查是否前端代码中误用了内边距（Padding）或边距（Margin）破坏了默认的基线环境。

## 4. 验证检查单 (Verification Checklists)
- [ ] 检查界面中所有的价格、指标、带副标题的卡片，确认大小字体是否贴合在同一水平底部。
- [ ] 代码层面，混合文本的父容器是否正确配置了 `align-items: baseline`？
- [ ] 缩小字体的同时，是否适当提高了其字重或颜色对比度，以保证其视觉声量不至于完全被大字号淹没？
- [ ] 包含非文本元素（如徽章、SVG）的行内布局是否仍然保持了光学意义上的居中或对齐？