---
trigger: model_decision
description: 当编写或审计 [VISUAL] 块中包含视频 Asset（.mp4/.webm）时，强制执行"一块一视频"隔离规范，禁止在单个 VISUAL 块中堆叠多个视频 Asset。
---

# 规则：视频 Asset 单块隔离 (Video Asset Isolation per VISUAL Block)

> **核心原则**：H5 课件引擎每个 `[VISUAL]` 块只能渲染**一个主 Asset**。多视频堆叠在同一块中会导致渲染失败（仅显示断链占位符和原始 Markdown 文本）。

## TL;DR

- 每个 `> [VISUAL]` 块**最多一个视频 Asset**
- 多个视频必须拆分为独立 VISUAL 块，间夹叙事段落
- 视频 Asset 禁止使用 `▶️` emoji 前缀链接写法
- 视频 Asset 的 Layout 应为 `Full`（非 `Center`）

---

## §1 一块一视频原则

当教学场景需要展示多个视频片段时（如同一项目的多个功能演示），**必须**将每个视频拆分为独立的 `> [VISUAL]` 块：

### ❌ 错误写法（多视频堆叠）

```markdown
> [VISUAL]
> *   **Slide**: `S10_Demo`
> *   **Layout**: `Full`
> *   **Asset**: ▶️ [Video A](../public/videos/A.webm)
> *   **Asset 1**: ▶️ [Video B](../public/videos/B.webm)
> *   **Asset 2**: ▶️ [Video C](../public/videos/C.webm)
```

### ✅ 正确写法（一块一视频 + 叙事穿插）

```markdown
> [VISUAL]
> *   **Slide**: `S10a_Video_A`
> *   **Layout**: `Full`
> *   **Asset**: ![Video A](../public/videos/A.webm)
> *   **Source**: `Video` — 来源说明
> *   **Duration**: `1m30s`
> *   **TimeCategory**: `activity`

这是关于 Video A 的叙事段落……

> [VISUAL]
> *   **Slide**: `S10b_Video_B`
> *   **Layout**: `Full`
> *   **Asset**: ![Video B](../public/videos/B.webm)
> *   **Source**: `Video` — 来源说明
> *   **Duration**: `0m45s`
> *   **TimeCategory**: `activity`

这是关于 Video B 的叙事段落……
```

## §2 视频 Asset 语法规范

| 规则 | 说明 |
|:---|:---|
| 必须用 MD 图片语法 | `![描述](路径.webm)` — H5 引擎通过扩展名判断 Asset 类型 |
| 禁止 emoji 链接写法 | `▶️ [名称](路径)` 不会被引擎识别为视频，会被渲染为原始文本 |
| Layout 禁用 `Center` | `Center` 映射到 `Layout_Title`（纯文字标题布局），不支持视频播放器渲染。视频应使用 `Full` |
| 禁止 AI fallback 共存 | 视频 VISUAL 块中不得追加 `Asset (AI fallback)` 静态图片行（script-format §3 已有此禁令） |

## §3 审计检查点

`/audit` 执行时，对每个 `> [VISUAL]` 块检查：

1. 是否存在多个 `Asset` / `Asset N` 行同时指向 `.mp4` / `.webm` 文件 → 🔴 强制拆分
2. 视频 Asset 是否使用 `▶️ [链接文本](路径)` 而非 `![描述](路径)` → 🔴 修正语法
3. 视频 VISUAL 块的 Layout 是否为 `Center` → 🟡 建议改为 `Full`
4. 视频 VISUAL 块是否缺少 `Duration` / `TimeCategory` / `Source` 必填字段 → 🔴 补全

---

## 问题溯源记录

**发现于**：2026-04-17，信息可视化 W01 M02 脚本 `S10_Big_Data_Interaction` 块。
**现象**：三个 MIT Senseable City Lab 视频（LIVE_Singapore / Data_Lenses / Traffic_Origins）堆叠在同一 VISUAL 块中，H5 预览界面显示"图片缺失"叠加层 + 原始 Markdown 链接文本。
**根因**：
1. H5 `SlideFactory.jsx` 每块只解析一个主 `image` 字段，多 Asset 的后续视频被忽略
2. `▶️ [链接文本](路径)` 语法不被 Asset 解析器识别（需 `![描述](路径)` MD 图片语法）
3. `Layout: Center` 映射到 `Layout_Title`，该组件无视频播放器渲染能力
