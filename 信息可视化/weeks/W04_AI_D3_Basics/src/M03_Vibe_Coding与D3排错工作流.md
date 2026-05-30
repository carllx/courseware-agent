## 模块 3: Vibe Coding 与 D3 排错工作流 (50 分钟)
<!-- BUDGET: 3600 chars | SLIDES: ≥6 | STATUS: draft -->

### 3.1 数据游侠：在网页端徒手抓取与清洗数据

在正式开始 Vibe Coding 生成 D3 图表前，我们需要优质的燃料——**Tidy Data (整洁数据)**。上一周我们学习了数据清洗的原则，但数据从哪来？

> [LIFE CONNECT] 不写爬虫，也能抓取数据
> 很多同学以为抓取数据需要写复杂的 Python 爬虫。其实，作为前端可视化设计师，浏览器本身就是你最强大的数据抓取工具。

> [VISUAL]
> *   **Slide**: S10_Web_Data_Scraping
> *   **Layout**: `Split`
> *   **RenderMode**: `pedagogical`
> *   **Keywords**: glowing funnel, floating chaotic data blocks, neat CSV grid
> *   **Scene**: 一个散发魔法光芒的漏斗将混沌漂浮的数据块（象征网页杂乱信息）吸入，并在底部输出为排列整齐的纯净网格（象征 CSV 表格）。
> *   **Text**: Vibe 抓取流：所见即所得的数据获取

如果你想获取“豆瓣电影 Top 250”或者“小红书热门笔记”的排名，最简单粗暴且完全合规的方法，就是**“网页直接复制 + 大模型洗数据”**：
1. **直接选中网页文本**：用鼠标在网页上高亮你需要的那一块内容（哪怕里面混杂着图片、广告词和乱码），直接 `Ctrl+C`。
2. **用自然语言驱动清洗**：把复制的一大坨乱码丢给大模型（如 ChatGPT / Claude），附上这条 Prompt：“*请从以下网页复制的混乱文本中，提取出所有的电影名称、评分和年份，并严格按照 Tidy Data 的原则，整理成一份英文表头的 CSV 格式代码，不需要任何其他解释。*”
3. **另存为燃料**：将大模型生成的 CSV 文本直接保存为 `data.csv`，你的可视化燃料就准备完毕了！

在网页端，JS 也有自带的数据清洗指令。比如以后当我们在代码里需要清洗数据时，AI 经常会用到 `.map()`（对每个数据做转换）和 `.filter()`（过滤掉不需要的数据）。看到这两个词，你就知道 AI 在帮你做数据排沙。

### 3.2 认知纠偏：代码白屏不代表推翻重来

有了数据，我们现在让大模型（LLM）写一段 D3 代码。然而，初次渲染往往是一片死寂的白屏。

> [VISUAL]
> *   **Slide**: S11_Debug_Funnel
> *   **Layout**: `Center`
> *   **RenderMode**: `pedagogical`
> *   **Keywords**: high-tech glowing funnel, red warning signs, magnifying glass, glowing orb
> *   **Scene**: 一个充满科技感的光效漏斗。漏斗顶层漂浮着红色的警告标志，中层是悬浮的放大镜在扫描结构，漏斗最底端分离出一个纯净发光的隔离圆球（象征 MRE）。
> *   **Text**: 三层排错漏斗：找回对 AI 的控制权

代码白屏，很多同学的本能反应是恐慌，直接对大模型吼：“又报错了！全部重写！”
这是个 **致命习惯**。重写会让大模型推翻原本只需改一个标点就能跑通的方案，导致**越改越乱**。代码白屏，就像 PS 里建了 500 个图层后画面全黑。你绝不会删掉整个 PSD 重画，而是去检查哪个图层的混合模式出错了。合格的可视化架构师会使用**排错漏斗策略**结合**D3 常识**，对大模型进行精准修正。

### 3.3 第一道防线：原样抄写控制台红字

按 F12 打开浏览器开发者工具，切换到 **Console（控制台）** 面板（网页的“病历本”）。
这里的心法是：**不要自己翻译！** 不要把“找不到元素”这种模糊的主观感受告诉 AI。直接原封不动复制控制台里那刺眼的红色英文报错。当 AI 看到 `"Error: d3.timeParse is not a function at line 42"`，它瞬间就能开出药方。

### 3.4 第二道防线：结构定位与 D3 画布常识

如果控制台静悄悄没有红字，但图表依然白屏或错位，这就说明代码没有语法错误，而是**视觉逻辑**错了。这时我们需要结合 D3 的常识，给 AI 发送 **结构化定位指令**。

#### 避坑常识 1：颠覆常识的倒置画布与裁切

> [VISUAL]
> *   **Slide**: S12_Inverted_World
> *   **Layout**: `Split`
> *   **RenderMode**: `pedagogical`
> *   **Keywords**: glowing pillars growing upwards, glowing stalactites hanging downwards, inverted spaces
> *   **Scene**: 两个对比强烈的空间：左侧的地面上向上生长着发光柱体（代表常规坐标），右侧则是倒置的世界，发光柱体像钟乳石一样从天花板向下倒挂（代表 SVG 倒置坐标系）。
> *   **Text**: 违背直觉的倒置画布

浏览器的坐标系是一个**倒置画布 (Inverted Canvas)**：`(0,0)` 坐标在**左上角**，Y 轴是**向下递增**的。如果 AI 忘了反转 Y 轴，你的柱子就会像钟乳石一样向下生长。
此外，SVG 就像没有边框的白纸，如果不预留内边距，坐标轴的文字就会被浏览器边缘切掉（**Margin Convention**）。

💡 **Vibe 排错话术**：“*图表的柱子反向朝下生长了，且左侧 X 轴文字被裁切。请检查 Y 轴的比例尺 Range 映射是否正确反转，并加上标准的 Margin 边距预留。*”

#### 避坑常识 2：贫富差距带来的视觉塌陷 (Scale)

> [VISUAL]
> *   **Slide**: S13_Wealth_Disparity
> *   **Layout**: `Center`
> *   **RenderMode**: `pedagogical`
> *   **Keywords**: colossal pillar of light, microscopic glowing dots densely packed at base
> *   **Scene**: 一根极其巨大的光柱直破天际，而在其底部，密密麻麻地挤着成千上万个如同灰尘般微小、几乎看不见的幽暗光点，形成极端的体积反差。
> *   **Text**: 比例尺：连接海量数据与有限屏幕的桥梁

**比例尺 (Scales)** 是连接数据与像素的汇率转换器。如果你有一组极端数据（如普通人数万存款，与首富数千亿），默认的线性比例尺 (`scaleLinear`) 会导致普通人的数据点被压缩到连 1 像素都不到，图表仿佛空无一物。

💡 **Vibe 排错话术**：“*小数值的数据完全看不见，被大数值压扁了。请不要用线性比例尺，帮我换成对数比例尺 (`scaleLog`) 来解救微小数值，或者如果是时间轴请用 `scaleTime`。*”

#### 避坑常识 3：忒修斯之船与幽灵残留 (Data Join)

> [VISUAL]
> *   **Slide**: S14_Data_Join_Lifecycle
> *   **Layout**: `Split`
> *   **RenderMode**: `pedagogical`
> *   **Keywords**: ancient Greek ship of Theseus, glowing new timber, fading wooden planks turning to dust
> *   **Scene**: 充满史诗感的船坞中停靠着一艘古希腊木船（忒修斯之船）。船身上，一部分是散发新生光芒的崭新木材（Enter），一部分是被魔法光晕笼罩正在变化的木板（Update），还有一部分腐朽的旧木板正在随风化作飞灰消散（Exit）。
> *   **Text**: 忒修斯之船与数据生命周期

当你的图表有交互（比如通过下拉菜单切换数据），AI 经常犯一个低级错误：旧数据没有被销毁，新数据直接盖在上面，导致屏幕上残留着诡异的“幽灵图表”。
这是因为 D3 有三个生命周期状态。AI 往往只写了 `Enter`（新增元素）和 `Update`（更新元素），却忘了写 `Exit`（元素比数据多时，将旧元素销毁）。

💡 **Vibe 排错话术**：“*当我切换数据时，旧的图形没有消失，重叠在了一起。你忘记处理 D3 的 Data Join 生命周期了，请把 `exit().remove()` 的逻辑加上。*”

### 3.5 终极制裁：MRE 最小可复现示例

如果连审查元素都找不到具体的标签，整个文档彻底混乱了怎么办？当红字拦截和结构定位双双失效时，你需要动用**终极拆解策略**。

> [VISUAL]
> *   **Slide**: S15_MRE_Isolation
> *   **Layout**: `Split`
> *   **RenderMode**: `pedagogical`
> *   **Keywords**: tangled glowing wires, chaotic energy, isolated glowing crystal in sterile chamber
> *   **Scene**: 左半边是缠绕成一团的乱麻状发光线缆和失控的混沌能量；右半边则是一个极度纯净、无菌的玻璃隔离舱，里面安静地悬浮着一颗完美的单体发光水晶。
> *   **Text**: 最小可复现示例 (MRE)：代码越少，AI 智商越高

千万不要在几千行报错代码中手工删减，那极易二次崩溃。你需要做的是**开启新对话，命令 AI 降维**：
“*暂时忽略网格、坐标轴和悬浮框，给我一个只有 3 条数据、最基础的 D3 散点图，先让纯粹的圆画在画布上。*”
只有当杂音被剥离到极致——即 **MRE（最小可复现示例）**——AI 的逻辑推导能力才会大幅上升。一旦基础 MRE 跑通，再让 AI 逐步把动效加回去。

> [TEACHING MOMENT] 金句
> **排错的本质不是修补，而是控制变量。能看懂数据骨架、掌控空间分配，并拥有漏斗排错思维的设计师，永远不可替代。我们要成为在机器狂欢中按下制动按钮的人。**

---

## 课后作业与综合演练
<!-- BUDGET: 0 chars | TYPE: activity | STATUS: exempt -->

> [ACTIVITY]
> *   **Type**: `Practice`
> *   **Duration**: `60min`
> *   **Desc**: **大课作业 (Lab Session)：Vibe 排错实录**
>   采用前文所学的“网页复制+大模型清洗”方法，获取一份你感兴趣的真实排名表（如豆瓣/淘宝），整理为 Tidy CSV。
>   使用 D3 创作一个带悬浮交互的多变量图表。**核心要求**：必须在生成过程中运用漏斗排错策略（查红字/提示比例尺/MRE降维），并提交一份包含 3 次关键错误的**排错交锋实录（截图或文字）**，证明你没有被白屏击倒。
