---
description: 执行 H5 课件 SSG 构建管线（资产转码 + 产物验证），生成可部署的 dist/ 目录
---

# /build — H5 课件构建工作流

// turbo-all

> **定位**：独立的构建命令，与投递（`/deploy_netlify`）和版本控制（`/git_sync`）解耦。
> 构建完成后可单独部署 `dist/` 或提交源码，也可通过 `/publish` 一键编排全流程。

## 前置条件

1. 确保已运行 `python engines/generate_course_h5.py --all` 初始化 `build/h5_preview` 实例
2. 已执行 `npm install`（首次运行时）
3. 已运行 `python engines/generate_course_h5.py --all` 生成课程 JSON（或由 `/h5` 工作流处理）

---

## Step 1: 构建前预检 (Freshness Gate)

```bash
cd "build/h5_preview"
bash scripts/preflight.sh --mode check
```

> **决策**：
> - 如果输出「✅ dist 是最新的」且用户只想部署 → 可直接跳到 `/deploy_netlify`
> - 否则继续 Step 2 执行构建
> - 用户可通过 `--force` 意图强制重建

---

## Step 2: 执行 SSG 构建管线

```bash
cd "build/h5_preview"
npm run build
```

> **构建包含**：
> 1. `vite build` — 前端打包
> 2. `build-ssg.js` — 资产转码管线：
>    - PNG/JPG → WebP (via sharp)
>    - AAC → MP3 单声道 24kHz (via FFmpeg)
>    - 重写课程 JSON 中的路径引用
>    - 生成 TTS manifest

---

## Step 3: 构建后验证 (Artifact Gate)

```bash
cd "build/h5_preview"
bash scripts/preflight.sh --mode verify
```

> **验证项**：
> - `dist/assets/media/` 存在且含 WebP 图片
> - `dist/assets/tts/` 存在且含 MP3 音频
> - `dist/courses/` 存在且含课程 JSON
>
> 如果验证失败（exit code 1），**中止后续流程并排查**。

---

## 完成

构建产物位于 `build/h5_preview/dist/`。后续操作：

- **部署到 Netlify** → 执行 `/deploy_netlify`
- **提交源码到 GitHub** → 执行 `/git_sync`
- **一键全流程** → 执行 `/publish`

> [!WARNING]
> `dist/` 是临时构建产物，已从 `.gitignore` 排除。切勿使用 `git add -f dist/`。
