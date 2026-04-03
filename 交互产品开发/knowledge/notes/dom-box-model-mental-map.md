# DOM 盒模型心智地图

## 核心概念

DOM（文档对象模型）中的每一个 HTML 元素，在浏览器渲染时都被当作一个**矩形盒子**处理。这个"盒子套盒子"的结构，就是设计稿与代码之间最底层的翻译协议。

## 盒模型四层结构（由内到外）

1. **Content（内容区）**: 文字、图片等实际内容所占区域。CSS 中 `width` / `height` 默认定义的就是这一层的尺寸。
2. **Padding（内边距）**: 内容与边框之间的透明空间。增加 padding 会扩大元素的可触控/点击面积，但不影响外边距。对应 Figma 中 Auto Layout 的 **Padding** 设置。
3. **Border（边框）**: 包裹内容和 padding 的可视线条。可设置粗细、样式（实线/虚线）和颜色。
4. **Margin（外边距）**: 边框之外的透明空间，用于分隔相邻元素。对应设计中"元素间的间隔"。

## box-sizing 的关键区别

- **content-box（默认）**: `width` 只计算内容区，padding 和 border 额外叠加 → 导致"设计稿标注 300px 宽，代码写出来 340px"的经典翻车。
- **border-box（推荐）**: `width` 包含 content + padding + border → 尺寸所见即所得，与设计工具中的行为一致。

## 设计师的心智映射

| 设计师在 Figma 中看到的 | 对应 DOM 盒模型层 |
|:---|:---|
| Frame / 容器的宽高 | `width` / `height`（border-box 下含 padding） |
| Auto Layout 的 Padding 设置 | CSS `padding` |
| Auto Layout 的 Item Spacing | CSS `gap`（Flex 容器内） |
| 元素之间的留白 | CSS `margin` 或 Flex `gap` |
| 描边 / Stroke | CSS `border` |

## 核心洞察

> "在浏览器的世界里，**万物皆盒子**。你的设计稿上每一个图层——文字、图片、按钮、卡片——到了代码里都是一个矩形容器。理解这个盒子的四层结构（内容→内边距→边框→外边距），就是理解'设计如何变成代码'的第一步。"

参考来源：MDN Web Docs — CSS Box Model, W3Schools CSS Box Model
