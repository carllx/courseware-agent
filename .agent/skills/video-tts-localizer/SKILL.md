---
name: video-tts-localizer
description: >
  视频字幕中文 TTS 本地化引擎。将外语视频+字幕处理成中文 TTS 音频，
  桥接 aeneas-ng（语音对齐）+ doubaotts（中文语音合成）+ video-downloader（视频获取）。
  当用户提到"视频配音"、"中文 TTS"、"字幕转语音"、"视频本地化"、"aeneas"、
  "音频对齐"、"逐字稿对齐"、"tts 对齐"时触发。
---

# 视频字幕中文 TTS 本地化引擎

将外语视频（含字幕）处理成中文 TTS 音频的端到端管线编排器。

## 架构概述

```
video-downloader        aeneas-ng              doubaotts / ffmpeg
(获取视频+字幕)    →    (转录/对齐)       →    (中文语音合成)
    ↓                      ↓                       ↓
 .mkv + .srt          词级时间戳            中文 TTS 音频片段
                           ↓                       ↓
                    Agent 精译 EN→ZH         aeneas-ng align()
                           ↓                       ↓
                      .zh-Hans.srt            对齐后音轨
                                                   ↓
                                            ffmpeg 混流 → 最终产物
```

**核心依赖路径**：`/Users/yamlam/Downloads/aeneas-ng-api`（通过 `sys.path` 动态加载）

---

## §1 环境前置检查

在执行任何操作前，**必须**验证以下 4 项：

### 1.1 aeneas-ng 可达性

```bash
/opt/anaconda3/envs/mybase/bin/python -c "
import sys; sys.path.insert(0, '/Users/yamlam/Downloads/aeneas-ng-api')
from aligner import Aligner
print('aeneas-ng OK')
"
```

### 1.2 Whisper 模型路径

```bash
ls /Volumes/T7-carllx2T/pyvideotrans-models/ 2>/dev/null && echo "外置模型 OK" || echo "WARN: 外置硬盘未挂载，将回退到 ~/.cache"
```

### 1.3 ffmpeg 可用性

```bash
/opt/homebrew/bin/ffmpeg -version 2>&1 | head -1
```

### 1.4 Python 环境

```bash
/opt/anaconda3/envs/mybase/bin/python -c "import stable_whisper, jieba; print('依赖 OK')"
```

> [!WARNING]
> 如果 §1.1 失败，需要先安装 aeneas-ng 依赖：
> ```bash
> cd /Users/yamlam/Downloads/aeneas-ng-api && /opt/anaconda3/envs/mybase/bin/pip install -e .
> ```

---

## §2 管线模式路由

收到请求后，按以下决策树选择模式：

```
有视频 URL 或文件？
  ├─ 有 → 有现成字幕 (SRT/VTT)？
  │        ├─ 有 → M2: 字幕驱动模式
  │        └─ 无 → M1: 全自动模式
  └─ 无 → 有音频文件？
           ├─ 有 → 有中文逐字稿？
           │        ├─ 有 → M3: 纯对齐模式
           │        └─ 无 → M4: 纯转录模式
           └─ 无 → 输入不足，请求补充
```

> 各模式的详细步骤：见 [pipeline_modes.md](references/pipeline_modes.md)

---

## §3 模式执行概要

### M1: 全自动模式（视频 URL → 中文配音）

1. **获取**：调用 `video-downloader` 技能下载视频 + 提取字幕
2. **转录**（如无字幕）：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  /Users/yamlam/Downloads/2025-2026-2\ 课程/.agent/skills/video-tts-localizer/scripts/transcribe_video.py \
  --audio "<视频文件>" \
  --lang auto \
  --output "<输出目录>/subtitles.srt"
```

3. **翻译**：Agent 逐条精译 SRT（遵循 video-downloader §4.6 翻译质量要求）
4. **拆段**：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  /Users/yamlam/Downloads/2025-2026-2\ 课程/.agent/skills/video-tts-localizer/scripts/prepare_tts_segments.py \
  --srt "<中文字幕>.zh-Hans.srt" \
  --output "<输出目录>/tts_manifest.json"
```

5. **合成**：将 manifest 中的每段文本通过 `doubaotts` 提取 TTS 音频
6. **混流**：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  /Users/yamlam/Downloads/2025-2026-2\ 课程/.agent/skills/video-tts-localizer/scripts/merge_tts_audio.py \
  --manifest "<输出目录>/tts_manifest.json" \
  --tts-dir "<TTS音频目录>" \
  --video "<原始视频>" \
  --output "<最终输出>.webm"
```

### M3: 纯对齐模式（教师录音 + 课程脚本 → SRT）

最常用的单步模式，直接调用 aeneas-ng 的 Hybrid Match：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  /Users/yamlam/Downloads/2025-2026-2\ 课程/.agent/skills/video-tts-localizer/scripts/transcribe_video.py \
  --audio "<录音文件>.mp3" \
  --transcript "<逐字稿>.md" \
  --lang zh \
  --output "<输出>.srt"
```

---

## §4 跨技能协作协议

### 4.1 与 video-downloader 的交接

- **输入契约**：video-downloader 完成 §2-§4 后，交付的文件应位于 `public/videos/`
- **文件命名**：遵循 video-downloader §5.2 的命名规范
- **字幕格式**：优先 SRT（aeneas-ng `parse_srt()` 原生支持），VTT 亦可

### 4.2 与 doubaotts 的交接

- **段落指纹**：`prepare_tts_segments.py` 使用与 doubaotts 相同的 DJB2 哈希算法
- **音频格式**：doubaotts 输出 AAC，本技能接受 AAC/MP3/WAV
- **存储路径**：TTS 音频临时存放于 `<周次>/tts/` 目录

### 4.3 与 aeneas-ng 的交接

- **加载方式**：`sys.path.insert(0, '/Users/yamlam/Downloads/aeneas-ng-api')`
- **模型路径**：自动检测外置硬盘 `/Volumes/T7-carllx2T/pyvideotrans-models/`
- **设备选择**：Apple Silicon 默认 `cpu` + `int8` 量化

---

## §5 故障排除

| 错误签名 | 根因 | 解决方案 |
|:---|:---|:---|
| `ModuleNotFoundError: stable_whisper` | mybase 环境缺少依赖 | `pip install stable-ts faster-whisper jieba` |
| 中文对齐漂移 > 1s | 逐字稿与音频不匹配 | 检查逐字稿是否为实际朗读内容 |
| `FileNotFoundError: ffmpeg` | ffmpeg 不在 PATH | 脚本内硬编码 `/opt/homebrew/bin/ffmpeg` |
| TTS 段落过长 (> 200 字) | SRT 分段粒度太粗 | `prepare_tts_segments.py --max-chars 100` |
| 外置硬盘未挂载 | 模型不可达 | 回退到 `~/.cache/aeneas-ng`，首次需下载 |
