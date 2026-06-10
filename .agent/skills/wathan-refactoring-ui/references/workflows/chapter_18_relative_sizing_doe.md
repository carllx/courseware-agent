# 文本与排版设计工作流 (Typography & Layout Design Workflow)

## 前置条件与上下文 (Prerequisites & Context)

在进行界面设计时，文本、间距和相对比例是影响视觉层级和用户体验的核心因素。本工作流涵盖了相对尺寸缩放、消除模糊间距、文本排版、字体选择及对齐方式等核心原则。遵循这些启发式规则，能够确保界面在不同设备上均保持极佳的可读性和设计一致性。

当需要深入理解背后的设计理论时，请运行时 Agent 使用动态拉取脚本获取上下文：
`bash scripts/query_theory.sh "Why is relative sizing ineffective across different screen sizes?"`
`bash scripts/query_theory.sh "What are the psychological impacts of ambiguous spacing in UI?"`
`bash scripts/query_theory.sh "Why is a handcrafted type scale preferred over a modular type scale in UI design?"`

---

## 综合指南与最佳实践 (Comprehensive Guide & Best Practices)

### 1. 放弃绝对的相对尺寸缩放 (Relative Sizing Doesn't Scale)
不要错误地认为界面的所有部分都应按照统一比例进行缩放。
- **断点缩放的不对称性**：在小屏幕上，原本在大屏幕上显示很大的元素需要以**更快的速度缩小**，而较小元素的缩小幅度应相对缓和，缩小元素尺寸差异的极端感。
- **组件内部的非线性比例**：例如调整按钮尺寸时，不应简单地按比例缩放字体和 `padding`。大按钮应当增加相对更宽裕的 `padding`，而小按钮应更加紧凑。
  ![](../../images/index-93_1.png)
  ![](../../images/index-94_1.png)
  ![](../../images/index-96_1.png)

### 2. 消除模糊间距 (Avoid Ambiguous Spacing)
元素分组的逻辑必须通过间距清晰地表达。
- **外部间距 > 内部间距**：确保相关联的元素组（如表单的 `label` 和 `input`、文章标题与正文）的外部间距大于其内部间距，否则用户将难以识别元素的归属关系。
  ![](../../images/index-97_1.png)
  ![](../../images/index-98_1.png)

### 3. 建立并固化排版比例系统 (Establish a Type Scale)
放弃随意指定如 13px、15px 等无规则的字体大小，建立一套约束系统。
- **避免使用 em 单位定义层级**：嵌套元素的 `em` 值会导致计算出的像素偏离你的比例系统。优先使用 `px` 或 `rem`。
- **手动打造 UI 排版比例**：由于数学模块化比例（Modular scales）会导致亚像素渲染问题和字号缺失，推荐手动定义一套约束比例（如：12, 14, 16, 18, 20, 24, 30, 36, 48）。
  ![](../../images/index-106_1.png)
  ![](../../images/index-108_1.png)

### 4. 优化阅读体验的行长与行高 (Line Length & Proportional Line-height)
良好的阅读体验依赖于科学的行长与行高配合。
- **行长控制**：最佳阅读行长为每行 45-75 个字符（在 Web 端通常为 20-35em 宽度）。即便父容器很宽，也应当对段落的宽度做出限制。
- **行高（Line-height）成反比与正比规则**：
  - **行长正比**：长行文本需要更大的行高（如 2.0），短行文本可适当减小行高（如 1.5），以防止视线换行时串行。
  - **字号反比**：小字号文本需要更大的行高增强可读性，而大字号的标题文本需要的额外行间距极小，甚至可以设置为 1。
  ![](../../images/index-115_1.png)
  ![](../../images/index-124_1.png)

### 5. 文本对齐与基线对齐 (Alignment Strategies)
- **同行多字号基线对齐 (Baseline, not center)**：如果同一行混排了不同字号的文本，切忌垂直居中对齐，必须遵循**基线对齐 (Baseline alignment)**。
  ![](../../images/index-119_1.png)
  ![](../../images/index-120_1.png)
- **避免居中长文本**：超过两到三行的文本请始终左对齐。只有短标题或极短文案才适合居中。如果必须居中，考虑重写并精简文案。
- **数字右对齐**：表格中的数字内容应该右对齐，以保证小数点位置一致，便于用户快速比对。
- **两端对齐必须断字 (Hyphenate justified text)**：两端对齐如果不断字（Hyphenation）会产生尴尬的文字缝隙。
  ![](../../images/index-130_1.png)

### 6. 链接与字体的选择策略 (Link and Font Selection)
- **链接低调化**：当界面存在大量交互元素时，不要给每一个链接都加上刺眼的颜色或下划线。使用稍重的字重 (Font weight) 或深色，将下划线仅在 `:hover` 状态显示。
- **好字体的评判标准**：
  - UI 优先选用中性无衬线字体 (如系统自带的 `-apple-system`, `Roboto`, `Segoe UI`)。
  - 过滤掉字重 (Weights) 种类小于 5 种的字体。
  - UI 字体应有较高的 `x-height` 以提升小尺寸下的可读性。
  ![](../../images/index-127_1.png)

---

## 条件故障排除逻辑 (If/Then Troubleshooting Logic)

- **IF** 标题在移动端看起来大得夸张且占据过多空间，**THEN** 检查是否使用了针对桌面端设计的硬编码缩放比例（如 `2.5em`）。改用基于断点手动调整的绝对字号，确保大屏幕大字体缩放的幅度大于小屏幕的缩小幅度。
- **IF** 表单填写时感觉视觉混乱，用户分不清 `label` 属于哪个 `input`，**THEN** 检查并扩大表单组（Form groups）之间的外边距，使分组之间的间隔显著大于 `label` 与 `input` 的内边距。
- **IF** 在一行内容中左侧大标题与右侧的小号操作按钮感觉视觉不平衡，**THEN** 将两者的垂直对齐方式从 `center` 改为 `baseline`。
- **IF** 段落文字阅读吃力，容易读错行，**THEN** 确认：(1) 每行字符数是否超过了 75 个？若是，缩减内容容器最大宽度（如 `max-w-prose`）；(2) 行高是否不够？为该宽度的段落增加行高（如增至 `1.75` 或 `2.0`）。

---

## 验证清单 (Verification Checklists)

- [ ] 响应式尺寸检查：检查在大屏和小屏下，文本和组件比例是否独立微调，而非粗暴的全局等比缩放。
- [ ] 分组间距审查：检查组件外部留白是否显著大于内部元素之间的留白。
- [ ] 字体排版系统一致性：代码库中不存在 `13px`、`17px` 等脱离预设排版系统的非标准字号，且未滥用 `em` 单位导致字号偏移。
- [ ] 行长约束验证：长篇文章或描述段落被约束在每行 45-75 字符（20-35em 宽度）。
- [ ] 文本对齐逻辑：大于三行的文本段落已经改为左对齐；表格中的数字列为右对齐；同一行的多个字号已基于基线（Baseline）对齐。
- [ ] 链接交互噪音最小化：非核心主路径的辅助链接已经弱化视觉处理（如仅通过字重或 `:hover` 状态区分）。
- [ ] 动态上下文预留：文中已将所有深度理论探究交由 `scripts/query_theory.sh` 拉取，保障了本文档作为纯粹的操作工作流的精简与高效。