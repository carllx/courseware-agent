# Prompt Engineering for UI 生成

> **来源**: 综合调研 — UXPin, Miro, Medium, thedesignsystem.guide 等 (2024-2025)
> **关联**: W09 Module 2-3

## 核心概念

UI 生成的 Prompt Engineering 是**将设计意图转化为 AI 可执行指令**的结构化方法。不同于通用 Prompt Engineering，UI Prompt 必须同时承载**视觉信息、交互逻辑和品牌约束**三层语义。

## 结构化 Prompt 框架

### 五层 Prompt 架构 (RCPVU)

| 层 | 全称 | 说明 | 示例 |
|:--|:---|:---|:---|
| R | Role (角色) | AI 扮演的角色 | "你是一个前端 UI 工程师" |
| C | Context (上下文) | 项目背景与约束 | "这是一个外卖点餐单页应用" |
| P | Platform (平台) | 目标平台与技术栈 | "React + Tailwind，移动端优先" |
| V | Visual Style (视觉风格) | 设计语言与品牌调性 | "现代极简、圆角、柔和阴影" |
| U | UI Components (组件清单) | 需要包含的具体组件 | "底部导航栏、菜品卡片、购物车浮层" |

### 从 Design Tokens 到 Prompt

Design Tokens（设计标记）是设计系统的原子级变量。Prompt Engineering 的核心技术之一是**将 Token 集翻译为 AI 可读的结构化约束**：

```
❌ 模糊描述：
"做一个好看的按钮"

✅ Token 驱动的结构化 Prompt：
"主按钮：
- 背景色 = Primary-600 (#2563EB)
- 文字色 = White
- 圆角 = 8px
- 内边距 = 12px 24px
- 悬停态：背景色加深至 Primary-700
- 禁用态：透明度 50%"
```

### AI 可读的 Token 格式

Design Tokens 需要从"设计稿标注"升级为"AI 可读格式"：

| 维度 | 设计稿标注 | AI 可读 Token |
|:---|:---|:---|
| 颜色 | #2563EB | `primary-600: { value: "#2563EB", description: "主操作按钮和关键链接" }` |
| 间距 | 16px | `space-4: { value: "16px", description: "卡片内部填充和组件间距" }` |
| 字体 | Inter 14px | `text-sm: { value: "14px/1.5", font: "Inter", description: "正文和表格内容" }` |

关键区别在于 `description` 字段——它告诉 AI **何时用、为什么用**这个 Token，防止语义错配（如用通用灰色替代了特定语义色）。

## Prompt 迭代策略

### 三阶段迭代法

1. **骨架阶段 (Scaffold)** — 先生成页面结构和布局，不指定细节样式
   - Prompt 焦点：组件列表、布局方式、数据结构
2. **皮肤阶段 (Skin)** — 在骨架基础上注入视觉 Token
   - Prompt 焦点：颜色、字体、间距、阴影
3. **交互阶段 (Interaction)** — 添加状态变化和微交互
   - Prompt 焦点：hover/active/disabled 状态、过渡动画、反馈

### 避坑指南

| 常见错误 | 后果 | 正确姿势 |
|:---|:---|:---|
| 一次性描述全部需求 | AI 丢失细节，输出混乱 | 分层迭代：骨架→皮肤→交互 |
| 只用形容词（"好看"/"现代"） | AI 主观发挥，结果不可控 | 用具体 Token 值替代形容词 |
| 不给示例和参考 | AI 缺乏方向感 | 提供视觉参考图或已有组件代码 |
| 忽略边界状态 | 空态/错误态缺失 | 在 Prompt 中明确列出所有状态变体 |

## 与课程 Exp3 的对接

学生在 Exp2 积累的三个关键资产直接转化为 W09 的 Prompt 输入：

1. **状态流转图 → Context 层** — 告诉 AI 页面之间的跳转关系
2. **Visual Token 集 → Visual Style + Platform 层** — 提供颜色、字体、间距的精确值
3. **组件清单 → UI Components 层** — 列出每个页面需要的具体组件
