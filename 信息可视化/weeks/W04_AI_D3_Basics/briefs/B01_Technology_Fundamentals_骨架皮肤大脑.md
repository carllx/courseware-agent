---
week: W04
brief_id: B01
title: "技术基础：骨架、皮肤与大脑 (Web/HTML/DOM/CSS/JS/SVG)"
textbook: "Interactive Data Visualization for the Web, Scott Murray, 2017"
chapters: ["3"]
source_path: "knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017/chapter_03_Technology_Fundamentals.md"
covers_modules: ["M01"]
status: done
---

## 教材位置
- 原著：Scott Murray, *Interactive Data Visualization for the Web*, 2017
- 章节：Chapter 3 — Technology Fundamentals
- 范围：全文 (Lines 1 - 3528)

## 核心知识提取

### 1. Web 基础架构 (The Web)
- **客户端与服务器 (Clients and Servers)**：Web 本质上是 Web 服务器 (Web servers) 与 Web 客户端 (Web clients，即浏览器) 之间的对话。
- **请求与响应 (Requests and Responses)**：客户端发出请求，服务器以数据（HTML/CSS/JS 等文件）作为响应。
- **URL 与 HTTP**：通过统一资源定位符 (URL) 定位资源，依靠超文本传输协议 (HTTP) 传输网页内容。

### 2. HTML：网页的“骨架” (Skeleton)
- **超文本标记语言 (Hypertext Markup Language)**：用于为 Web 浏览器组织内容结构，赋予纯文本语义结构 (Semantic structure)。
- **元素与标签 (Elements and Tags)**：通过标签（如 `<p>`, `<div>`, `<h1>`）对内容进行标记。标签可以嵌套产生层级结构。
- **属性 (Attributes)**：为元素分配属性，其中最通用的是类 (Classes) 和 ID。ID 在页面中必须唯一，类则可以应用于多个元素。这是数据可视化选中元素的重要挂钩。
- **通俗比喻**：HTML 就像是网页的“骨架” (Skeleton)，支撑起页面的基本结构与内容层次。

### 3. DOM：文档对象模型 (Document Object Model)
- **层次结构 (Hierarchical Structure)**：DOM 代表了 HTML 的层级结构。元素之间具有父 (Parent)、子 (Child)、兄弟 (Sibling)、祖先 (Ancestor) 和后代 (Descendant) 的关系。
- **程序操控接口**：浏览器解析 HTML 并生成 DOM 树。在 D3.js 中，编写的代码必须在 DOM 层次结构中导航，才能选中元素并动态改变其样式和行为。

### 4. CSS：网页的“皮肤” (Skin)
- **层叠样式表 (Cascading Style Sheets)**：用于设置 DOM 元素的视觉呈现 (Visual presentation)。
- **选择器与属性 (Selectors and Properties)**：通过类型选择器 (Type selectors)、后代选择器 (Descendant selectors)、类选择器 (Class selectors, `.class`) 以及 ID 选择器 (ID selectors, `#id`) 定位 DOM 元素，并应用对应的样式规则。
- **层叠与继承 (Cascading and Inheritance)**：子元素通常继承父元素的样式，多个规则作用于同一元素时，更具体 (Specific) 的选择器规则会覆盖通用的规则。
- **通俗比喻**：CSS 就像是网页的“皮肤”或“衣服” (Skin/Clothing)，决定了骨架上的内容最终如何排版、着色与展示。

### 5. JavaScript：网页的“大脑” (Brain)
- **动态脚本 (Dynamic Scripting)**：JS 是一门脚本语言，可以在页面加载后动态操作 DOM，使网页产生交互。
- **变量与数据类型 (Variables and Data Types)**：作为数据的容器 (Containers)，保存数值 (Numbers)、字符串 (Strings)、布尔值 (Booleans)、数组 (Arrays) 与对象 (Objects) 等。
- **控制流与函数 (Control Flow and Functions)**：利用 if 语句进行逻辑分支，用 for 循环处理重复任务。函数 (Functions) 则是可复用的代码块。
- **通俗比喻**：JavaScript 就像是网页的“大脑”与“肌肉” (Brain/Muscle)，赋予页面记忆力（数据变量）、思考力（逻辑控制）与行动力（动态修改 DOM）。

### 6. SVG：可缩放矢量图形 (Scalable Vector Graphics)
- **矢量表示 (Vector Representation)**：不同于基于像素的位图 (Raster graphics)，SVG 依赖数学指令进行绘制，在任何缩放比例下都保持清晰。
- **基于 DOM (DOM-based)**：SVG 元素 (如 `<rect>`, `<circle>`, `<text>`) 和普通的 HTML 元素一样存在于 DOM 树中，可以被 CSS 赋予样式，并且被 JavaScript 自由操纵。这使得它成为 D3 数据可视化中最核心的绘图画布。

## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig3.1 | Typical default rendering of simple HTML | `images/ff2a5a09...webp` (L498) | ✅ `public/textbook/Fig3.1_.webp` |
| Fig3.2 | Looking at the source code in a new window in Chrome | `images/61f5d7dc...webp` (L791) | ✅ `public/textbook/Fig3.2_.webp` |
| Fig3.3 | Chrome’s web inspector | `images/ab2978a0...webp` (L829) | ✅ `public/textbook/Fig3.3_.webp` |
| Fig3.4 | Inspector with element box highlighted | `images/0912b2c6...webp` (L899) | ✅ `public/textbook/Fig3.4_.webp` |
| Fig3.8 | CSS cascading and inheritance at work | `images/0ff69d13...webp` (L1444) | ✅ `public/textbook/Fig3.8_CSS.webp` |
| Fig3.9 | A fresh JavaScript console | `images/df6c4edf...webp` (L1516) | ✅ `public/textbook/Fig3.9_A.webp` |

*(注：原书 Chapter 3 共有 27 张配图，以上提取了在解释基础概念与开发者工具时最具教学辅助价值的关键图表)*

## 易混淆概念辨析

- **HTML vs DOM**：HTML 是写在文件中的静态纯文本标签；DOM 则是浏览器解析 HTML 后在内存中建立的“动态树结构”。D3.js 修改的是 DOM，而不是源 HTML 文件。
- **Class vs ID**：ID 在整个页面中必须是独一无二的（用于唯一元素如画板容器）；Class 则可以同时赋给无限多个元素（如同一类数据点 `class="bar"`）。
- **SVG vs Canvas (位图)**：SVG 是基于 DOM 标签的矢量图形，可以为每个图形元素绑定事件和数据；而位图（Canvas/PNG）只是死像素，一旦画上便无法单独操控特定图形（如某个条形）。

## 对照检查表

- [ ] `CHK-B01-01`: 是否通过“骨架、皮肤、大脑”的比喻，向非编程背景学生直观解释了 HTML、CSS 和 JavaScript 各自的职责？
  - 关键词: `骨架`, `皮肤`, `大脑`
  - 预期出现模块: M01
- [ ] `CHK-B01-02`: 在介绍 D3 数据绑定之前，是否明确交代了 DOM 的层级关系概念，并说明 D3 改变的是 DOM 而不是 HTML 文件？
  - 关键词: `DOM`, `文档对象模型`, `树形结构`
  - 预期出现模块: M01
- [ ] `CHK-B01-03`: 在讲解选择器时，是否明确区分了 Class (`.`) 和 ID (`#`) 在 D3 选择元素时的差异及应用场景？
  - 关键词: `Class`, `ID`, `唯一`
  - 预期出现模块: M01
- [ ] `CHK-B01-04`: 是否解释了 SVG 作为矢量图形系统的特性，以及它为什么是 D3 最完美的绘图画布（即 SVG 也是 DOM 的一部分）？
  - 关键词: `SVG`, `矢量`, `无限缩放`
  - 预期出现模块: M01
