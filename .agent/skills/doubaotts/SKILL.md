---
name: doubaotts
description: 豆包 TTS 桥接引擎（段落级动态合成 + 本地文件系统持久化）。当 H5 预览需要音频提取、TTS 连接调试、或用户提及"提取语音"、"TTS"、"豆包"时触发。
---

# 技能：豆包 TTS 桥接引擎 (Doubao TTS Bridge)

## 架构概述

H5 预览引擎 **不直连** 豆包 WebSocket（会被 Origin 拒绝）。采用弹窗桥接架构：

```
H5 (localhost:5173)                    doubao.com 弹窗
   │                                       │
   │── postMessage(h5_tts_extract) ──────→ │
   │                                       │→ tts_bridge.user.js
   │                                       │   调用 window.tts(text)
   │                                       │   ← 原版 userscript
   │←── postMessage(ArrayBuffer) ──────── │
   │    (Transferable, 零拷贝)             │
   │                                       │
   └→ Vite POST /api/tts/save → 本地项目文件系统
```

## 前置条件

1. **Chrome 浏览器** + [Tampermonkey](https://www.tampermonkey.net/)
2. **安装两个油猴脚本**（位于本目录 `scripts/`）：
   - `userscript.js` — 原版豆包 TTS 引擎，暴露 `window.tts()` API
   - `tts_bridge.user.js` — H5 凭证桥接器，处理 postMessage 中继
3. **登录 `doubao.com`** — 确保有有效会话（bridge 需要从 cookie 提取 `device_id`）

## 核心文件

| 文件 | 职责 |
|:---|:---|
| `scripts/userscript.js` | 原版豆包 TTS 引擎（第三方，勿修改） |
| `scripts/tts_bridge.user.js` | H5 凭证桥接器（可修改） |
| `engines/h5_template/src/utils/doubao-tts.js` | H5 端 TTS 工具库 |
| `engines/h5_template/vite-plugin-h5-hot-reload.js` | Vite 中间件（`/api/tts/save`, `/api/tts/manifest`, TTS 音频静态代理）|
| `engines/h5_template/src/contexts/TtsSegmentContext.jsx` | 段落状态引擎（基于 manifest 批量校验） |
| `engines/h5_template/src/components/TtsParaButton.jsx` | 段落播放/提取按钮 |
| `engines/generate_course_h5.py` → `_compute_tts_fingerprint()` | Python 端指纹生成 |
| `engines/h5_template/src/utils/fingerprint.js` → `computeTtsFingerprint()` | JS 端指纹生成 |

## 凭证交换流程

1. H5 打开 `doubao.com/chat/` 弹窗（`window.open`）
2. **双向握手**：
   - 桥接端：向白名单候选 origin（`localhost:5173/5174/3000`）逐一推送凭证
   - H5 端：每 2 秒主动轮询 `h5_tts_request_credentials`
3. 凭证包含：`device_id`、`web_id`、`hasUserscript` 标志

> [!IMPORTANT]
> V-01 安全修复：不使用 `postMessage('*')` 通配符。凭证仅发送到白名单 origin。

## 本地持久化储存策略 (V3 架构)

- **存储路径**：`{课程}/weeks/{周次}/tts/{fp}.aac`
- **指纹策略 `fp`**：DJB2 全文哈希 + 文本长度（如 `d075f24e_1280`）
- **状态维护**：以周为单位的 `manifest.json`，存储段落指纹与时长元数据，供前端 `computeStatus` 高效批量判断 (O(1))。
- **Dev 模式音频代理**：Vite 中间件拦截 `/courses/{id}/weeks/{week}/tts/*.aac` 请求，从 workspace 源目录读取物理文件并流式返回（无需 symlink）。
- **静态部署兼容**：写入本地后自动随 `npm run build` 产出加入生成环境，Netlify/Git 同步有效。

## 增量 diff 机制

`computeStatus()` 查找策略：

1. **HTTP/Manifest 快速探测**（通过 Vite `GET /api/tts/manifest` 一次性获取状态）
2. **零开销复用**：提取完毕后，当前会话在内存中保留 BlobURL 提供极速回放；重载后从文件系统提供 HTTP URL 返回。

编辑逐字稿后仅实际文本变更的段落需重新提取。

## 修改须知

修改桥接协议时须**三文件同步**：
- `tts_bridge.user.js`（发送端消息格式）
- `doubao-tts.js`（接收端消息路由）
- `TtsSegmentContext.jsx`（状态引擎）

修改指纹算法时须**双端同步**：
- `generate_course_h5.py` → `_compute_tts_fingerprint()`
- `fingerprint.js` → `computeTtsFingerprint()`

> [!WARNING]
> 指纹格式变更会导致原有 TTS 文件失效（虽可共存，但原缓存视为未获取，需重新提取占用新空间）。
