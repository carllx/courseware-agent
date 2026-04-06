---
trigger: model_decision
description: 当执行 Netlify 部署（/deploy_netlify）或讨论"发布"、"上线"、"deploy"时，必须先执行 dist 新鲜度验证，防止 TTS 音频或图片资产断链。
---

# 规则：部署前构建新鲜度验证 (Pre-Deploy Build Freshness Gate)

> **核心原则**：`dist/` 是临时构建产物，其内容必须与源文件保持同步。部署前必须验证，绝不盲推。

## §1 强制预检清单

在执行 `npx netlify deploy` 或调用 Netlify MCP 部署工具**之前**，Agent 必须完成以下检查：

### 1.1 TTS 音频新鲜度

对每个已启用 TTS 的课程，比对**源 TTS 目录**和 **dist TTS 目录**的时间戳与文件数量：

```bash
# 源文件：最新 TTS 提取时间
find {workspace}/{courseId}/weeks/*/tts/ -name "*.aac" -newer engines/h5_template/dist/index.html 2>/dev/null | head -5
```

- 如果存在比 `dist/index.html`（上次构建产物）更新的 `.aac` 文件 → **构建已过期，必须重新执行 `npm run build`**
- 如果 `dist/assets/tts/` 不存在或为空 → **构建缺失 TTS 管线产物，必须重建**

### 1.2 图片资产新鲜度

```bash
# 检查是否有更新的源图片
find {workspace}/*/weeks/*/public/slides/ -name "*.png" -newer engines/h5_template/dist/index.html 2>/dev/null | wc -l
```

- 如果计数 > 0 → 有新图片未被 SSG 管线转码，必须重建

### 1.3 dist 完整性

```bash
# dist 必须包含以下目录
ls engines/h5_template/dist/assets/media/ 2>/dev/null && echo "✅ media" || echo "❌ media 缺失"
ls engines/h5_template/dist/assets/tts/   2>/dev/null && echo "✅ tts"   || echo "❌ tts 缺失"
```

## §2 决策逻辑

```
预检结果全部通过？
  ├─ 是 → 继续部署
  └─ 否 → 向用户报告具体断裂点，建议执行 npm run build
           用户确认后执行构建，构建成功后重新预检，通过后部署
```

## §3 禁止行为

- ❌ 跳过预检直接执行 `netlify deploy`
- ❌ 仅因为上次部署成功就假设当前 dist 仍有效
- ❌ 在 dist 不存在或结构不完整时执行部署
- ❌ 使用 `git add -f` 将 dist 重新加入版本控制（参见 2026-04-06 安全审查）
