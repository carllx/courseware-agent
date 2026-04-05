# 视觉系统全量检验沙盒 (Visual System Storybook)

> 本文件是活的视觉组件字典 (Living Documentation)。
> 包含全部 12 种合法**语义宏布局**的极端用例。您可以通过调整本文件的字段，实时验证 H5 引擎渲染的鲁棒性。

## 1. 单焦点与版式声明 (Center 系)

### 1-1 Center 居中骨架

> [VISUAL]
> *   **Slide**: S01_Center_Demo
> *   **Layout**: `Center`
> *   **Scene**: 极简白墙上的哲学陈述
> *   **Text**: 不好的设计如同灾难现场
> *   **Caption**: Alan Cooper《About Face》第4版

对于纯粹的 Center，系统仅仅依靠 Text 的长度自动伸缩字号大小。

### 1-2 CTA 行动号召

> [VISUAL]
> *   **Slide**: S02_CTA_Demo
> *   **Layout**: `CTA`
> *   **Scene**: 深邃黑底，带有红色警示意味的操作终态
> *   **Text**: 课后挑战：寻找身边让人抓狂的三个体验

CTA 必须能触发深颜色底（由 `visual_system.yaml` 决定），打破前序所有视觉连续性。

### 1-3 Agenda 大纲目录

> [VISUAL]
> *   **Slide**: S03_Agenda_Demo
> *   **Layout**: `Agenda`
> *   **Scene**: 结构清晰的三层课程架构
> *   **Text**: 本周要解决的问题：
> *   **List**: 1. 产品之殇 / 2. 用户心理模型 / 3. 破局之道

Agenda 会被引擎推测为带编号序号的目录呈现。

---

## 2. 图文双拼 (Split 系)

### 2-1 Split 基础双栏（文+图）

> [VISUAL]
> *   **Slide**: S04_Split_Demo_Normal
> *   **Layout**: `Split`
> *   **Scene**: 左撇子使用鼠标的荒谬场景图
> *   **List**: 违背直觉的设计 / 强迫用户适应机器 / 缺乏反馈的动作
> *   **Asset**: `dummy_ui_error.png`

系统检测到 List+Asset 会自动将之推入分栏两侧。

### 2-2 Quote 金句引用

> [VISUAL]
> *   **Slide**: S05_Quote_Demo
> *   **Layout**: `Quote`
> *   **Scene**: 乔布斯思考产品设计的肖像特写
> *   **Text**: 设计不在于外观感觉，设计是产品如何运作。
> *   **Asset**: `steve_jobs_portrait.png`
> *   **Caption**: - Steve Jobs, 1997

Quote 应该触发巨型的引号底纹和特殊的衬线字体样式。

### 2-3 Workshop 工坊模式

> [VISUAL]
> *   **Slide**: S06_Workshop_Demo
> *   **Layout**: `Workshop`
> *   **Scene**: Figma 界面原型的实操作图演示
> *   **Text**: 动手时间：建立你的第一个组件
> *   **List**: 建立 Frame (F) / 绘制矩形 (R) / 创建组件 (Option+Cmd+K)
> *   **Asset**: `figma_component_demo.gif`

必须看到明显的“正在操作/指导”状态栏。

---

## 3. 沉浸全屏 (Full 系)

### 3-1 Full 满屏全画幅

> [VISUAL]
> *   **Slide**: S07_Full_Demo
> *   **Layout**: `Full`
> *   **Scene**: 数据中心机房发生爆炸的灾难性大图背景
> *   **Text**: AWS S3 工程师的一个拼写错误
> *   **Asset**: `aws_outage_datacenter.jpg`

图片应以 Cover 模式填充屏幕所有边缘，文字由于背景复杂，需要有一层深色半透明掩罩 (Scrim) 来保证阅读。

### 3-2 Screenshot 带设备壳截图

> [VISUAL]
> *   **Slide**: S08_Screenshot_Demo
> *   **Layout**: `Screenshot`
> *   **Scene**: 极度扭曲混乱的报表工具界面原始切图
> *   **Asset**: `horrible_dashboard_ui.png`

引擎不应该把这当做普通 Full 对待，必须在其外围生成一层 Mac Window 外框或带有投影的包裹层。

### 3-3 Poll 互动轮询

> [VISUAL]
> *   **Slide**: S09_Poll_Demo
> *   **Layout**: `Poll`
> *   **Scene**: 微信扫码答题的互动大屏二维码
> *   **Text**: 扫码进行知识点摸底测试！
> *   **Asset**: `quiz_qrcode.png`

特定交互版面，应能有效诱导学生拿出手机。

---

## 4. 多列网格 (Grid 系)

### 4-1 Grid 并列特征网格

> [VISUAL]
> *   **Slide**: S10_Grid_Demo
> *   **Layout**: `Grid`
> *   **Scene**: 四组图标阵列
> *   **List**: 易用性 / 效率 / 容错 / 满意度

引擎须根据 4 个无序列表项自动推算出 2x2 等比例方块。

### 4-2 Comparison 正反对抗网格

> [VISUAL]
> *   **Slide**: S11_Comparison_Demo
> *   **Layout**: `Comparison`
> *   **Scene**: 原先糟糕的布局跟现在极简的布局的左右对照映射
> *   **List**: ❌ 让用户填50多个抽象参数 / ✅ 提供 12 个贴近常识的常用场景
> *   **Code**: \`\`\`css\n/* 假装这是对比附加代码 */\n.bad { color: red }\n\`\`\`

引擎应触发强烈的左红右绿（或符合 `visual_system` 设定主调）对抗色系。

---

## 5. 线性流向 (Flow 系)

### 5-1 Flow 顺序流线

> [VISUAL]
> *   **Slide**: S12_Flow_Demo
> *   **Layout**: `Flow`
> *   **Scene**: 从小白到专家的用户旅程时间线
> *   **List**: 1. 探索阶段 / 2. 爬坡遇阻 / 3. 习惯养成 / 4. 盲打专家

必须脱离枯燥的垂直 Bullet-list（项目符号），强制转化为附带引线、箭头或者水平排布的时间线 UI 组件。
