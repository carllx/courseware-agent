# 视觉系统架构规范 (Visual Layout Architecture v2.1)

> 本文档基于对现代幻灯片生成框架（Slidev, Marp, Reveal.js）的深度对标，并结合 **UX 前轴设计理论**重构制定。
> 核心目标：既解决历史遗留的解析器碎片化混乱，又绝不增加讲师/作者的心智执行负担。

## 1. 设计哲学：“内紧外松”的前后端分离模型

在视觉排版中，存在两种截然不同的心智模型：
*   **作者的心智 (UX)**：教学目标导向（如“我要做一页对比图” $\to$ `Comparison`）
*   **引擎的心智 (工程)**：参数属性导向（如“这是一个两列网格布局，外加一个红绿对比的 CSS 样式类” $\to$ `Grid` + `compare`）

如果强迫作者在一线写作时拆解底层参数（设定 `Layout` = `Grid` 然后附加 `Intent` = `compare`），这破坏了流畅的所写即所思体验。

为此，我们将视觉体系划分为完全隔离的**前端作者交互层**与**后端渲染引擎层**。

---

## 2. 前端交互层：语义预设 (The Semantic UI)

> 面向：讲师、Agent (`/write` 工作流)
>
> 📘 **详见对照手册：[VISUAL_LAYOUT_CATALOG.md](./VISUAL_LAYOUT_CATALOG.md)** 对每种语义宏的语法范例及 H5 呈现结果进行了完整录入。

作者写入脚本的 `[VISUAL]` 块时，只需在 `Layout` 字段填写符合人脑直觉的**场景定义名**，无需关心空间网格如何计算。在规范 v2.1 下，我们收敛出了 **12 个核心预设 (Semantic Aliases)**：

### 2.1 空间导向预设 (基础模型)
表达纯粹的空间排布，无特殊的业务样式修饰：
*   **`Center`**：单焦点视觉居中（主要用于大组文字、引言）。
*   **`Split`**：双侧对峙的图文、文图等分割结构。
*   **`Full`**：打破安全边距的满屏视觉（多用于沉浸图片）。
*   **`Grid`**：二维网格矩阵（用来装载卡片组）。
*   **`Flow`**：节点与连线的线性逻辑（基于底层 Mermaid 的图表、时间线）。

### 2.2 教学场景导向预设 (复合模板 Macros)
讲师脑海中非常具体、特定的教学版式，由底层自动转化为（基础模型+特定 CSS 样式）：
*   **`Comparison`**：方案/红绿好坏的直接对比预设。
*   **`Quote`**：名人金句居中展示。
*   **`Screenshot`**：包含浏览器外壳/设备外框的截图展示。
*   **`Workshop`**：带独立步骤序号与计时器的高亮实操预设。
*   **`Agenda`**：章节导航目录。
*   **`Poll`**：带二维码/互动的轮询预设。
*   **`CTA`**：黑底反色的“行动号召”行动终页。

**如何标注内容？** 作者无需声明内容类型，只需正常填充 `Text`, `List`, `Asset`, `Code` 字段，系统将执行**自动推断**。

---

## 3. 后端渲染引擎层：三层正交解耦 (The Engine Architecture)

> 面向：H5 预览引擎、`pptxgenjs` 组装器

当引擎读取到上述简单的宏（Macro）时，系统底层**坚决不可以**创建冗杂平行的 `renderComparison`、`renderQuote` 函数，引擎内部必须采用**三层正交解析器**进行强制降维。

### Layer 1: 绝对空间系 (Layout Grid - 仅限5种)
解析器首先建立底层的安全边距网格计算，所有宏都将被路由至这五个核心渲染器：
1. `renderTitle()` $\leftarrow$ 映射自 `Center`, `CTA`, `Agenda`
2. `renderSplit()` $\leftarrow$ 映射自 `Split`, `Quote`
3. `renderGrid()`  $\leftarrow$ 映射自 `Grid`, `Comparison`
4. `renderImage()` $\leftarrow$ 映射自 `Full`, `Screenshot`, `Poll`
5. `renderDiagram()` $\leftarrow$ 映射自 `Flow`

### Layer 2: 内容渲染器 (Content Types)
检测到哪些字段有效，就启动哪个子渲染器注入槽位（Slot）：
具有 `Code` 激活高亮组件；具有 `List` 激活列表循环组件。同一份空间逻辑承载任意合法内容模型。

### Layer 3: 样式修饰器 (Style Modifiers / Intent)
这是引擎拦截特定「语义预设」的重要环节，注入专属 CSS 类名或预配项。
*   若读取到原始 Layout 为 `Comparison`：引擎会给 `renderGrid()` 上抛一个上下文令牌 `modifiers: ['compare-theme']`，让前端挂载特定的差异高亮。
*   若读取到原始 Layout 为 `Workshop`：引擎在主干流线外渲染出一个悬浮的倒计时器组件。

### 引擎伪码演示
```javascript
// H5 预览引擎底层路由逻辑示例
function renderVisualBlock(block) {
  // 1. 拆解 Macro 得到三层元数据
  const { spatialGrid, isDarkMode, specificVueComponent } = engine.resolveMacro(block.Layout);
  
  // 2. 根据存在的字段挂载 Content Typ
  const content = deduceComponentByProps(block);
  
  // 3. 执行唯一的空间函数
  switch(spatialGrid) {
      case 'Center': return renderTitle(content, specificVueComponent);
      case 'Grid':   return renderGrid(content, specificVueComponent);
      // ...只保留 5 条基础 case，维护成本大幅下降
  }
}
```

---

## 4. 废弃清单 (Deprecations)
为保持心智极简，以下旧称已彻底弃用（Validation Suite 会拦截并强制要求更改）：
`Title`, `Section`, `Statement`, `Stat`, `Cards`, `Card`, `Dashboard`, `Timeline`, `Chart`, `List`, `Table`, `Image`, `CodeBlock`。

**(举例说明：为什么废弃 `List` ? 由于列表可以随意被放入 Center、Split 或者 Grid 矩阵空间中，它应当被降级为一个字段触发器，而非版式类型)。**
