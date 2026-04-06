---
description: 将项目同步到 GitHub 远程仓库（日常推送 / 初始化 / 大文件处理）
---

# /git_sync — GitHub 同步工作流

// turbo-all

> **互操作**：本工作流仅负责源码推送到 GitHub。
> 如需同时构建 dist/ 并部署到 Netlify，使用 `/publish` 一键编排全流程。

## 0. 前置检查

```bash
# 确认 Git 仓库已初始化
git rev-parse --is-inside-work-tree

# 确认远程仓库已配置
git remote -v
```

如果未初始化，参见 §A 附录「首次初始化」。

---

## 1. 日常推送（最常用）

```bash
# 1.1 查看变更
git status --short

# 1.2 暂存所有变更
git add .

# 1.3 提交（附有意义的信息）
git commit -m "feat/fix/docs: 简要描述变更内容"

# 1.4 推送
git push origin main
```

> **提交信息前缀规范**：
> - `feat:` 新功能/新课程/新脚本
> - `fix:` 修复错误
> - `docs:` 文档更新
> - `assets:` 图片/视觉资产变更
> - `chore:` 配置/工具链维护

---

## 2. 大文件分批推送策略

当变更涉及大量图片（>100MB 总量）时，**必须分批提交和推送**，避免超时：

```bash
# 第一批：仅源码（md, yaml, py, js, docx, pdf 等）
git add . ':!*.png' ':!*.jpg' ':!*.jpeg' ':!*.webp' ':!*.gif'
git commit -m "feat: 源码与配置更新"
git push origin main

# 第二批：图片资产
git add *.png *.jpg *.jpeg *.webp *.gif
git commit -m "assets: 视觉资产更新"
git push origin main
```

> [!IMPORTANT]
> 如果推送过程中遇到 **HTTP 408 超时**，直接重试 `git push origin main`。
> Git 会自动续传已发送的数据，第二次通常秒过。

---

## 3. 中国网络环境配置（已在本仓库生效）

本仓库已配置以下 Git 优化参数，**无需重复设置**：

| 参数 | 值 | 作用 |
|------|-----|------|
| `http.proxy` | `http://127.0.0.1:7890` | 走 Clash 代理 |
| `https.proxy` | `http://127.0.0.1:7890` | 走 Clash 代理 |
| `http.postBuffer` | `524288000` (500MB) | 防止大文件推送被截断 |
| `http.lowSpeedLimit` | `1000` (1KB/s) | 最低限速阈值 |
| `http.lowSpeedTime` | `300` (5min) | 低速容忍时长 |

### 代理故障排查

```bash
# 测试代理是否正常
curl -x http://127.0.0.1:7890 -s -o /dev/null -w "HTTP: %{http_code}, Speed: %{speed_download}" https://github.com

# 如果代理不通，检查 Clash 是否启动，或临时切换：
git config http.proxy http://127.0.0.1:新端口号
git config https.proxy http://127.0.0.1:新端口号

# 如果需要临时关闭代理（比如在国外网络）：
git config --unset http.proxy
git config --unset https.proxy
```

---

## 4. .gitignore 管控清单

以下文件类型**已在 .gitignore 中排除**，不会被推送：

| 类别 | 规则 | 原因 |
|------|------|------|
| 构建产物 | `**/build/`, `**/dist/`, `**/node_modules/` | 可重新生成 |
| Netlify 状态 | `**/.netlify/` | 含 Site ID，不应泄露到公开仓库 |
| 编译脚本 | `*_compiled.md`, `*.oot.txt` | dumptext.py 生成 |
| 演示文稿 | `*.pptx` | 单文件太大(3-10MB)，且可从脚本重新生成 |
| 视频/音频 | `*.mov`, `*.mp4`, `*.wav`, `*.mp3` 等 | 单文件几十~几百 MB |
| 系统文件 | `.DS_Store`, `__pycache__/` | 不相关 |

以下文件类型**保留推送**：

| 类别 | 格式 | 原因 |
|------|------|------|
| 课程脚本 | `.md`, `.yaml` | 核心资产，必须版本控制 |
| 幻灯片图片 | `.png`, `.jpg` | 单张 30-80KB，总量可控 |
| 教务文档 | `.docx`, `.pdf`, `.xlsx` | 重要但单文件不大 |
| Agent 配置 | `.agent/` 全部 | 工作流/技能/规则定义 |
| 引擎代码 | `engines/` (源码) | 通用生成引擎 |
| 锁文件 | `package-lock.json` | 确定性构建保障，必须入库 |

> [!CAUTION]
> **绝对不要** `git add -f engines/h5_template/dist/` 或 `git add -f .netlify/`。
> 这两个目录已在 2026-04-06 安全审查后被永久排除。强制添加会导致 Site ID 泄露和仓库膨胀。

---

## A. 附录：首次初始化新仓库

仅在全新项目中使用一次：

```bash
# A1. 初始化本地仓库
git init && git branch -m main

# A2. 提交 .gitignore 作为首个 commit
git add .gitignore README.md
git commit -m "chore: 初始化项目"

# A3. 关联 GitHub 远程仓库（需先在 github.com/new 创建空仓库）
git remote add origin https://github.com/carllx/仓库名.git

# A4. 配置中国网络代理
git config http.proxy http://127.0.0.1:7890
git config https.proxy http://127.0.0.1:7890
git config http.postBuffer 524288000
git config http.lowSpeedLimit 1000
git config http.lowSpeedTime 300

# A5. 分批推送（参见 §2）
```

## B. 附录：速度参考基线

基于 2026-04-03 首次推送实测数据：

| 方式 | 速度 | 预计推送 200MB 所需时间 |
|------|------|------------------------|
| 直连 GitHub（无代理） | ~17 KB/s | ~3.4 小时 |
| Clash 代理 (7890) | ~120 MB/s（复用连接） | ~2 秒 |
| Clash 代理 (7890) 首次连接 | ~25-130 KB/s | ~26-136 分钟 |

> [!TIP]
> 关键发现：首次推送因为 Git 需要上传所有对象，速度较慢。
> 但如果上次推送因 408 中断后**重试**，Git 会复用已上传数据，秒级完成。
