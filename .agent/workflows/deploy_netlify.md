---
description: 编译 H5 前端项目并包含最近的 SSG 管线将资产优化打包，最后将其部署到 Netlify 生产环境
---

## 🎯 目标

将 H5 预览引擎以及引用的课程资产（课件、图片、录音）整合打包，通过 SSG 管道（图片格式转换、音频转码为单声道）后，将静态 `dist` 目录推送至 Netlify 进行正式线上托管。

## 📝 前置准备

1. 确保在 `engines/h5_template` 目录下进行操作。
2. （如果是首次手动执行）确认本地已安装 `netlify-cli` 并且已经完成登录 `netlify login`。
3. **站点绑定声明**：本项目已通过 `.netlify/state.json` 永久绑定至 `endearing-mooncake-60c90e`，不论通过 Agent 发布或是人工发布，都会自动覆盖更新线上版本。

> [!WARNING]
> **安全须知**：`.netlify/state.json` 和 `dist/` 目录已从 Git 版本控制中排除（2026-04-06 安全修复）。
> 切勿手动将其加入 Git，否则 Site ID 将泄露到公开 GitHub 仓库。

## 👟 步骤

### 0. 🛡️ 构建新鲜度预检 (Freshness Gate)

> 此步骤由 `rule_deploy_freshness.md` 强制要求。**禁止跳过。**

在构建之前，先检测源文件是否有比上次构建更新的变更，以便向用户报告即将同步的内容：

```bash
cd "engines/h5_template"

echo "=== 🔍 构建新鲜度预检 ==="

# 检查 dist 是否存在
if [ ! -f dist/index.html ]; then
  echo "⚠️  dist/ 不存在或不完整 — 需要全量构建"
else
  echo "📅 上次构建: $(stat -f '%Sm' dist/index.html)"

  # 检查新 TTS 音频
  TTS_NEW=$(find ../../*/weeks/*/tts/ -name "*.aac" -newer dist/index.html 2>/dev/null | wc -l | tr -d ' ')
  echo "🔊 新 TTS 音频: ${TTS_NEW} 个文件待转码"

  # 检查新图片
  IMG_NEW=$(find ../../*/weeks/*/public/slides/ -name "*.png" -newer dist/index.html 2>/dev/null | wc -l | tr -d ' ')
  echo "📸 新图片资产: ${IMG_NEW} 个文件待转码"

  # 检查 dist/assets/tts 完整性
  TTS_DIST=$(find dist/assets/tts/ -name "*.mp3" 2>/dev/null | wc -l | tr -d ' ')
  echo "📦 dist 中已有 TTS: ${TTS_DIST} 个 MP3"
fi

echo "=== 预检完成 ==="
```
// turbo

> **决策**：根据输出判断是否需要构建。如果全部为 0 且 dist 完整，可跳到 Step 3 直接部署。
> 否则必须执行 Step 1 构建。通常建议**总是执行构建**以确保一致性。

### 1. 触发构建管线 (SSG Pipeline)

跳转到 H5 引擎目录，并执行生产环境完全构建：

```bash
cd "engines/h5_template"
npm run build
```
// turbo

> **预期结果**：Vite Build 成功后，`build-ssg.js` 脚本将自动接管，扫描引用资产、通过 sharp 压缩输出 WebP，通过 FFmpeg 转码输出 MP3，并将静态文件产物存放于 `dist/` 目录中。

### 2. 构建产物验证 (Post-Build Gate)

构建完成后，验证关键资产是否已就位：

```bash
cd "engines/h5_template"

echo "=== 📋 构建产物验证 ==="

# 核心目录存在性
[ -d dist/assets/media ] && echo "✅ assets/media" || echo "❌ assets/media 缺失"
[ -d dist/assets/tts ]   && echo "✅ assets/tts"   || echo "❌ assets/tts 缺失"

# 统计量
echo "📸 WebP 图片: $(find dist/assets/media/ -name '*.webp' 2>/dev/null | wc -l | tr -d ' ') 张"
echo "🔊 MP3 音频: $(find dist/assets/tts/ -name '*.mp3' 2>/dev/null | wc -l | tr -d ' ') 段"
echo "📄 课程 JSON: $(find dist/courses/ -name '*.json' 2>/dev/null | wc -l | tr -d ' ') 个"
echo "📦 dist 总大小: $(du -sh dist/ | cut -f1)"

echo "=== 验证完成 ==="
```
// turbo

> 如果出现 `❌` 或关键统计为 0，**中止部署并排查**。

### 3. 发布到 Netlify (Production)

执行静态部署命令，将 `dist` 推送上线：

```bash
cd "engines/h5_template"
npx netlify deploy --prod --dir=dist
```
// turbo

> **注**：
> - 如果此项目没有关联 Netlify Site ID (`.netlify/state.json`)，CLI 命令可能会进入交互式界面让用户选择。
> - **如果由 Agent 操作且配置了 Netlify MCP**：不要执行上面的 CLI 命令，请直接调用 `mcp_netlify_netlify-deploy-services-updater` 工具，将 `operation` 设为 `deploy-site`，并将 `deployDirectory` 设为 `dist` 的绝对地址（可能需向用户索要 siteId）。

### 4. 发布验证与收尾

- 拿到最终的 **Live URL**（通常结尾形式为 `{site_name}.netlify.app`）。
- 使用内部模块测试验证：加载首个课件界面，检查右侧讲稿区是否亮起 TTS-ready 图标并能正确进行语音播放（需测试 `.mp3` 走子链接网络请求是否触发正常）。
- 验证安全头是否生效：`curl -I https://endearing-mooncake-60c90e.netlify.app/ | grep -i "x-frame\|x-content-type\|referrer"`

> [!IMPORTANT]
> **部署后不要执行 `git add .`**。`dist/` 已从 `.gitignore` 排除，
> 但如果误用 `git add -f` 强制添加，会重新引入构建产物污染。
> 正确做法：部署完毕后仅提交源码变更。

- 结束并执行 `/epilogue` 通知完成。
