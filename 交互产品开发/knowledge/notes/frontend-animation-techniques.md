# 前端动效技术原理（CSS Animations & Performance）

> **来源**: Web 调研综合（MDN / web.dev / 掘金等）
> **适用周次**: W10

## 1. CSS 过渡 vs CSS 动画

| 特性 | `transition` | `animation` + `@keyframes` |
|:--|:--|:--|
| **触发方式** | 属性值变化时自动触发（hover/class 切换） | 可自动播放、循环、延迟 |
| **复杂度** | 简单 A→B 过渡 | 多阶段关键帧序列 |
| **适用场景** | 按钮悬停、面板展开、颜色渐变 | 加载动画、粒子效果、循环反馈 |

## 2. 高性能动画黄金法则

浏览器渲染流水线：**Layout → Paint → Composite**

| 阶段 | 触发属性 | 性能代价 |
|:--|:--|:--|
| Layout（回流） | `width`, `height`, `margin`, `padding`, `top`, `left` | 🔴 最昂贵：重新计算整棵 DOM 树 |
| Paint（重绘） | `background-color`, `box-shadow`, `border-radius` | 🟡 中等：重新绘制像素 |
| **Composite（合成）** | **`transform`, `opacity`** | 🟢 最廉价：GPU 直出 |

> **规则**: 动画**只用** `transform`（移动/旋转/缩放）和 `opacity`（透明度渐变）——这两个属性由 GPU 硬件加速，跳过 Layout 和 Paint。

## 3. 缓动函数（Easing）

缓动函数决定动画的"节奏感"——速度如何随时间变化。

| 函数 | 特征 | 适用场景 |
|:--|:--|:--|
| `ease-out` | 快启动→慢收尾 | **最推荐用于交互反馈** — 瞬间响应，优雅着陆 |
| `ease-in` | 慢启动→快结尾 | 元素退出/消失 |
| `ease-in-out` | 慢→快→慢 | 循环动画、转场 |
| `linear` | 匀速 | 进度条、持续旋转 |
| `cubic-bezier()` | 自定义 | 弹簧效果、超调（overshoot） |

> **心智桥接**: 缓动函数 = 动效的"演技"。`linear` 像机器人，`ease-out` 像人——快速反应但从容收住。

## 4. `will-change` 与性能提示

```css
.animated-card {
  will-change: transform, opacity; /* 提前告诉浏览器"我要动了" */
  transition: transform 0.3s ease-out;
}
```

- **作用**: 让浏览器预分配 GPU 图层，避免动画启动时的"卡顿一帧"
- **禁忌**: 不要对所有元素都加 `will-change`——每个图层消耗显存，滥用适得其反
- **降级方案**: `transform: translateZ(0)` 或 `translate3d(0,0,0)` 强制创建合成层

## 5. 60fps 目标

- 屏幕刷新率 60Hz → **每帧 16.67ms**
- 每帧内浏览器要完成：JavaScript → Style → Layout → Paint → Composite
- 如果一帧超过 16.67ms → **掉帧 (jank)**，用户感知为卡顿
- **减法思维**: 同时动画的元素越少、触发的渲染阶段越轻，帧率越稳

## 6. `prefers-reduced-motion` 无障碍

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- iOS 7 动效引发前庭敏感用户眩晕的教训
- **设计约束**: 任何动效方案必须同时提供"减少动态效果"的降级版本
