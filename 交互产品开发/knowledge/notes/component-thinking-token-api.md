# 组件化思维与 Token 映射

## 核心概念

组件化思维是将界面拆解为可复用、可组合的"零件"的设计方法论。Design Token 则是描述这些零件视觉属性的"参数集"——它是设计师给 AI 编码工具和开发者的"API"。

## 从原子到分子：组件层级

Brad Frost 提出的 Atomic Design 将界面拆解为五层：

1. **Atoms（原子）**: 最小不可拆分的UI元素 — 按钮、输入框、标签、图标
2. **Molecules（分子）**: 原子的组合 — 搜索框 = 输入框 + 按钮；表单字段 = 标签 + 输入框
3. **Organisms（有机体）**: 分子的组合 — 导航栏 = Logo + 搜索框 + 菜单项；产品卡片 = 图片 + 标题 + 价格 + 按钮
4. **Templates（模板）**: 有机体在页面中的布局骨架
5. **Pages（页面）**: 模板填充真实数据后的最终呈现

## Design Token：设计师的 API

Design Token 是将设计决策编码为变量的方式。它不是"颜色值"或"字号"本身，而是这些值被赋予的**语义名称**。

| Token 类别 | 示例命名 | 值 |
|:---|:---|:---|
| **颜色** | `color-primary-500` | `#3B82F6` |
| **字号** | `font-size-lg` | `18px` |
| **间距** | `spacing-md` | `16px` |
| **圆角** | `radius-card` | `12px` |
| **阴影** | `shadow-elevated` | `0 4px 12px rgba(0,0,0,0.1)` |

## 为什么 Token 对 Vibe Coding 至关重要

在本课程的 Exp3 中，学生将使用 AI 代码生成工具（如 v0）将设计稿转化为前端代码。如果设计稿中使用了零散、随意的颜色和尺寸值，AI 生成的代码将充斥硬编码（hard-coded magic numbers），难以维护。

但如果设计稿基于一套 Token 系统构建——

- **颜色不是 `#3B82F6`，而是 `primary-500`**
- **间距不是 `17px`，而是 `spacing-md` (16px)**
- **字号不是 `15px`，而是 `font-size-base` (16px)**

——AI 工具能更准确地将设计意图翻译为结构化代码，生成统一的 CSS 变量或 Tailwind 类名。

## 在 Figma 中的落地

1. **Local Styles / Variables**: Figma 的 Color Styles、Text Styles、Effect Styles 就是 Token 的设计端载体
2. **命名约束**: Token 名称应遵循 `{类别}-{语义}-{梯度}` 模式（如 `color-danger-600`），避免 `red-button-color` 这种非系统化命名
3. **Auto Layout + Token**: 组件的间距使用 Spacing Token，而非任意像素值 → 保证在不同屏幕尺寸下的一致性

## 核心洞察

> "Token 不是给设计师用的装饰，它是给机器看的合同。你在 Figma 里用了哪些 Token，AI 工具就生成怎样的代码。Token 越规范，代码越干净。"

参考来源：Brad Frost — Atomic Design (2016), Nathan Curtis — Design Tokens concepts
