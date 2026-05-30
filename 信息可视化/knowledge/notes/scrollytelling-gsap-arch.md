# Scrollytelling 架构与 GSAP ScrollTrigger

> 来源：Web 调研 (2024-2025) + 课程教学目标
> 认知目标：掌握 Scrollytelling 三层架构模式及 GSAP ScrollTrigger 核心 API

## Scrollytelling 定义

Scrollytelling（滚动叙事）= Scroll + Storytelling。用户的滚动行为驱动数据图景的渐进揭示。它不是仪表盘式的"自助探索"，而是编导式的"牵手叙事"。

## 三层架构模型

```
┌─────────────────────────────────────────┐
│  叙事层 (Narrative Layer)               │
│  HTML 文本块 = 演员走位                  │
│  每个 `.step` div = 一幕场景             │
├─────────────────────────────────────────┤
│  触发层 (Trigger Layer)                  │
│  GSAP ScrollTrigger = 摄影机轨迹        │
│  监听滚动位置 → 触发动画/数据切换        │
├─────────────────────────────────────────┤
│  渲染层 (Render Layer)                   │
│  D3 = 特效组                              │
│  执行 bindData / transition / 力重组     │
└─────────────────────────────────────────┘
```

## 四大设计模式

| 模式 | 描述 | 适用场景 |
|:---|:---|:---|
| Pinned (固定元素) | 图表 sticky 固定，文本滚过 | 长篇数据新闻（NYT 风格） |
| Scroll as Trigger | 滚至特定点触发动画 | 关键转折点的戏剧性揭示 |
| Scroll as Steps | 离散步骤逐段推进 | 教学演示、分步拆解 |
| Continuous | 滚动位置连续映射动画进度 | 时间线、进度型叙事 |

## GSAP ScrollTrigger 核心 API

### 关键属性
- **`trigger`**：触发元素（CSS 选择器或 DOM 节点）
- **`start` / `end`**：动画起止点，如 `"top center"` 表示触发元素顶部到达视口中心
- **`scrub`**：`true` = 动画进度与滚动条完全同步；数值 = 添加平滑延迟
- **`pin`**：将元素固定在视口中，直到滚动区间结束

### 调试与性能
- `markers: true`：可视化起止标记线（仅开发环境）
- `ScrollTrigger.refresh()`：动态内容变化后重新计算触发点
- 独立 ScrollTrigger 实例无性能问题，避免嵌套在同一 timeline 内

### 回调生命周期
```
onEnter → 进入触发区
onLeave → 离开触发区（向下）
onEnterBack → 从下方重新进入
onLeaveBack → 从上方离开
```

## 替代方案：IntersectionObserver API
- 浏览器原生 API，零依赖
- 适合轻量级"出现即触发"场景
- 不提供 scrub 同步能力，适合离散步骤模式

## 反面警告

- ❌ **ScrollMagic**：已被社区弃用（臃肿、性能差、维护停滞）
- ❌ **嵌套 ScrollTrigger**：在同一 GSAP timeline 内嵌套多个 ScrollTrigger 会产生逻辑冲突
- ❌ **移动端忽视**：触屏设备的滚动惯性行为与桌面端不同，必须测试 `touch-action` 和惯性锁定
