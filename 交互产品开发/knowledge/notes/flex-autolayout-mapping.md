# CSS Flex 与 Figma AutoLayout 映射

## 核心概念

CSS Flexbox 是前端布局的核心技术之一，而 Figma 的 Auto Layout 本质上就是 Flexbox 的设计工具翻版。掌握两者的映射关系，是设计师与开发者"说同一种语言"的关键。

## Flex 容器与子元素

- **Flex Container（容器）**: 在 CSS 中通过 `display: flex` 声明。在 Figma 中 = 添加了 Auto Layout 的 Frame。
- **Flex Items（子元素）**: 容器的直接子元素自动成为弹性子项，受容器规则约束。在 Figma 中 = Auto Layout Frame 内的所有直接子图层。

## 属性对照表

| Figma Auto Layout 设置 | CSS Flexbox 属性 | 说明 |
|:---|:---|:---|
| **Direction**: Horizontal/Vertical | `flex-direction`: row/column | 主轴方向：水平排列或垂直堆叠 |
| **Padding** (上右下左) | `padding`: top right bottom left | 容器内部留白 |
| **Spacing between items** | `gap` | 子元素之间的间距 |
| **Primary axis alignment** | `justify-content` | 沿主轴对齐方式（start/center/end/space-between） |
| **Counter axis alignment** | `align-items` | 沿交叉轴对齐方式（start/center/end/stretch） |
| **Resizing → Hug contents** | 不设固定 width/height（内容撑开） | 容器尺寸由内容决定 |
| **Resizing → Fill container** | `flex-grow: 1` / `width: 100%` | 子元素扩展填满父容器可用空间 |
| **Resizing → Fixed** | `width: Npx` / `height: Npx` | 固定尺寸，不随容器变化 |
| **Wrap** | `flex-wrap: wrap` | 子元素超出时换行 |

## 嵌套逻辑

Auto Layout 的强大之处在于**嵌套**：一个垂直方向的 Auto Layout 内部可以嵌套水平方向的 Auto Layout，反之亦然。这与 CSS 中嵌套 Flex 容器完全一致。

```
Container (flex-direction: column)
  ├── Header Row (flex-direction: row)
  │     ├── Logo
  │     └── Nav Links
  ├── Content Area (flex-direction: row)
  │     ├── Sidebar (fixed width)
  │     └── Main Content (flex-grow: 1)
  └── Footer Row (flex-direction: row)
```

## 关键心智模型

1. **父控制子**: Auto Layout 中，父容器决定子元素的排列规则（方向、间距、对齐）。如果布局看着不对，先检查父容器的 Auto Layout 设置。
2. **Hug vs Fill 的博弈**: 这是设计师最常纠结的地方 — 容器到底该"收缩包裹内容"还是"膨胀填满空间"？答案取决于上下文：标签/按钮通常 Hug，主内容区通常 Fill。
3. **间距 ≠ 边距**: Auto Layout 的 Item Spacing 对应 Flex 的 `gap`，这是子元素**之间**的距离；Padding 是容器**内壁到子元素**的距离。二者不可混淆。

## 设计师的实操口诀

> "方向定好，间距拉开，对齐选准——Auto Layout 和 Flex 的核心参数就这三板斧。剩下的，靠嵌套解决。"

参考来源：Figma Help Center — Auto Layout, CSS-Tricks — A Complete Guide to Flexbox, MDN Web Docs — CSS Flexible Box Layout
