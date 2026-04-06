---
description: 一键发布：构建 dist + 推送源码到 GitHub + 部署到 Netlify（交互式选择推送目标）
---

# /publish — 一键发布编排工作流

> **定位**：编排 `/build`、`/git_sync`、`/deploy_netlify` 三个子工作流，提供完整的发布体验。
> 如果只需执行其中一步，请直接使用对应的子命令。

## 前置条件

1. Git 远程仓库已配置（`git remote -v`）
2. Netlify Site ID 已绑定（`.netlify/state.json` 存在）
3. 网络代理可用（参见 `/git_sync` §3 中国网络环境配置）

---

## Step 1: 构建 dist/

执行 `/build` 工作流（预检 → SSG 构建 → 产物验证）。

> 如果 `/build` 的 Step 1 预检显示「dist 是最新的」，**询问用户是否跳过构建直接发布**。

---

## Step 2: 选择发布目标

向用户确认发布范围：

```
📦 构建完成。请选择发布目标：
  A) 仅推送源码到 GitHub (/git_sync)
  B) 仅部署 dist/ 到 Netlify (/deploy_netlify)
  C) 两者都执行 (推荐)
```

> 默认推荐 C，但用户可以选择单独执行。

---

## Step 3A: 推送源码到 GitHub

执行 `/git_sync` 工作流（暂存 → 提交 → 推送）。

> [!IMPORTANT]
> 提交信息应基于本次构建涉及的变更自动生成，遵循 conventional commits 格式。

---

## Step 3B: 部署到 Netlify

执行 `/deploy_netlify` 工作流（验证 dist → 推送 CDN → 线上验证）。

---

## Step 4: 收尾

执行 `/_epilogue` 共享收尾协议：
1. 更新 `briefing.md` 当前状态和活动记录
2. 检查是否需要记录 ADR
