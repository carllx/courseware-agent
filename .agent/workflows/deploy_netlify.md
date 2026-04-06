---
description: 将已构建的 dist/ 目录推送至 Netlify 生产环境（仅投递，不含构建）
---

# /deploy_netlify — Netlify 部署工作流

// turbo-all

> **定位**：纯投递命令——将已就绪的 `dist/` 推送至 Netlify CDN。
> 构建逻辑已分离至 `/build` 工作流。如需一键操作，使用 `/publish`。

## 📝 前置准备

1. **构建产物就绪**：`build/h5_preview/dist/` 目录存在且通过验证（由 `/build` 生成）
2. **Netlify 认证**：本地已安装 `netlify-cli` 并完成 `netlify login`
3. **站点绑定**：`.netlify/state.json` 已绑定至 `endearing-mooncake-60c90e`

> [!WARNING]
> **安全须知**：`.netlify/state.json` 和 `dist/` 目录已从 Git 版本控制中排除（2026-04-06 安全修复）。
> 切勿手动将其加入 Git，否则 Site ID 将泄露到公开 GitHub 仓库。

## 👟 步骤

### 1. 产物完整性验证

```bash
cd "build/h5_preview"
bash scripts/preflight.sh --mode verify
```

> **决策**：
> - 如果验证通过（exit code 0）→ 继续 Step 2
> - 如果验证失败（exit code 1）→ **中止部署，提示用户先执行 `/build`**

### 2. 发布到 Netlify (Production)

```bash
cd "build/h5_preview"
npx netlify deploy --prod --dir=dist
```

> **注**：
> - **如果由 Agent 操作且配置了 Netlify MCP**：优先调用 `mcp_netlify_netlify-deploy-services-updater` 工具，将 `operation` 设为 `deploy-site`，`deployDirectory` 设为 `dist` 的绝对路径。
> - Site ID 已通过 `.netlify/state.json` 自动读取，无需手动指定。

### 3. 发布验证与收尾

- 拿到最终的 **Live URL**（`endearing-mooncake-60c90e.netlify.app`）
- 验证 TTS 音频和 WebP 图片是否可正常加载
- 验证安全头是否生效：`curl -I https://endearing-mooncake-60c90e.netlify.app/ | grep -i "x-frame\|x-content-type\|referrer"`

> [!IMPORTANT]
> **部署后不要执行 `git add .`**。`dist/` 已从 `.gitignore` 排除。
> 正确做法：部署完毕后仅提交源码变更（使用 `/git_sync`）。

- 结束并执行 `/_epilogue` 通知完成。
