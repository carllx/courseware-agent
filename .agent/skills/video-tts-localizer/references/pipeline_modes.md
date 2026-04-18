# 管线模式详解

> 本文档由 SKILL.md §2 按需加载。详细说明四种管线模式的完整步骤和 ffmpeg 命令模板。

## 目录

1. [M1: 全自动模式](#m1-全自动模式)
2. [M2: 字幕驱动模式](#m2-字幕驱动模式)
3. [M3: 纯对齐模式](#m3-纯对齐模式)
4. [M4: 纯转录模式](#m4-纯转录模式)
5. [时间轴对齐算法说明](#时间轴对齐算法)
6. [ffmpeg 命令模板](#ffmpeg-命令模板)

---

## M1: 全自动模式

**输入**：视频 URL（YouTube / B 站等）
**输出**：中文配音视频（.webm 或 .mp4）

### 完整步骤

```
步骤 1: 获取 (video-downloader)
├── 下载视频（遵循 video-downloader §2 流程）
├── 提取字幕（--write-subs --write-auto-subs）
└── 交付：<video>.mkv + <video>.en.vtt

步骤 2: 转录/提取 (aeneas-ng)
├── 如有字幕：直接使用下载的 .vtt/.srt
├── 如无字幕：调用 transcribe_video.py --audio <video> --lang auto
└── 交付：原始语言 SRT

步骤 3: 翻译 (Agent 精译)
├── 逐条翻译 SRT 为中文
├── 控制每条 ≤ 25 个中文字符
├── 专业术语查 concept_registry.yaml
└── 交付：<video>.zh-Hans.srt

步骤 4: 拆段 (prepare_tts_segments.py)
├── 解析中文 SRT
├── 合并短段 + 拆分长段
├── 生成 DJB2 指纹
└── 交付：tts_manifest.json

步骤 5: 合成 (doubaotts)
├── 按 manifest 逐段提取 TTS
├── 音频文件以指纹命名
└── 交付：{fingerprint}.aac 文件集

步骤 6: 混流 (merge_tts_audio.py)
├── 拼接 TTS 片段（静音填充间隙）
├── 与原始视频混流
└── 交付：最终产物 .webm/.mp4
```

### 时间估算

| 视频时长 | 总处理时间 (M1 Mac) | 瓶颈 |
|:---|:---|:---|
| 1 分钟 | ~5 分钟 | Whisper 转录 |
| 5 分钟 | ~15 分钟 | TTS 提取 |
| 15 分钟 | ~45 分钟 | VP9 编码 |

---

## M2: 字幕驱动模式

**输入**：本地视频 + 已有 SRT 文件
**输出**：中文配音视频

### 与 M1 的区别
- 跳过步骤 1（不需要下载）
- 跳过步骤 2（已有字幕）
- 从步骤 3 开始

### 适用场景
- B 站已有中文字幕的英文视频
- 用户手动精修过的 SRT 文件
- 第三方字幕组提供的翻译字幕

---

## M3: 纯对齐模式

**输入**：音频文件 + 中文逐字稿
**输出**：精确 SRT

### 完整步骤

```
步骤 1: 清洗逐字稿
├── Markdown 标记清除（transcribe_video.py 内置）
├── [VISUAL] / [ACTIVITY] 块过滤
└── 交付：纯文本

步骤 2: Hybrid Match 对齐
├── Whisper 转录获取词级时间戳
├── difflib.SequenceMatcher 字符级匹配
├── 保留原始逐字稿文本 + 使用转录时间戳
└── 交付：精确 SRT

步骤 3: 质量验证
├── 抽检 5 个随机段落的时间戳偏差
├── 偏差应 < 300ms
└── 如偏差过大，检查逐字稿与实际朗读的一致性
```

### 核心命令

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/video-tts-localizer/scripts/transcribe_video.py \
  --audio recording.mp3 \
  --transcript lecture_script.md \
  --lang zh \
  --output aligned.srt
```

### 典型用例
- 教师课堂录音 + 已有课程逐字稿（Markdown）
- TTS 音频 + 逐字稿 → 精确时间戳（用于 H5 课件的段落级高亮）
- 播客/有声书的逐字稿对齐

---

## M4: 纯转录模式

**输入**：音频或视频文件
**输出**：自动生成的 SRT

### 核心命令

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/video-tts-localizer/scripts/transcribe_video.py \
  --audio meeting.mp3 \
  --lang auto \
  --model large-v3-turbo \
  --output transcript.srt
```

### 模型选择

| 模型 | 速度 (M1 Mac) | 精度 | 体积 | 推荐场景 |
|:---|:---|:---|:---|:---|
| `tiny` | 100x 实时 | 低 | 75 MB | 快速预览 |
| `base` | 50x 实时 | 中 | 145 MB | 时间轴骨架 |
| `small` | 20x 实时 | 较高 | 488 MB | 对话密集 |
| `medium` | 5x 实时 | 高 | 1.5 GB | 通用推荐 |
| `large-v3-turbo` | 2x 实时 | 最高 | 3.1 GB | 极致精度 |

---

## 时间轴对齐算法

### Hybrid Match 工作原理

aeneas-ng 的核心对齐策略，解决了 stable-ts 原生 `align()` 在中文长音频上的漂移问题：

```
1. Whisper 转录阶段
   ┌──────────────────────────────────────┐
   │ stable-ts transcribe(word_timestamps=True)  │
   │                                      │
   │ 输出：每个"词"的 {char, start, end}   │
   │ 展平为字符级时间戳序列               │
   └──────────────────────────────────────┘
                    ↓

2. 文本匹配阶段
   ┌──────────────────────────────────────┐
   │ difflib.SequenceMatcher              │
   │                                      │
   │ 转录文本 vs 用户逐字稿               │
   │ → equal: 直接复制时间戳              │
   │ → replace: 线性插值时间戳            │
   │ → insert/delete: 跳过               │
   └──────────────────────────────────────┘
                    ↓

3. 重组阶段
   ┌──────────────────────────────────────┐
   │ 按原始逐字稿的行结构重组              │
   │ 每行收集所有字符的时间戳              │
   │ start = 第一个字符的 start            │
   │ end = 最后一个字符的 end              │
   └──────────────────────────────────────┘
```

### 为什么不用 stable-ts align()

| 问题 | stable-ts align() | Hybrid Match |
|:---|:---|:---|
| 中文长音频漂移 | ❌ ~10s 漂移 | ✅ 零漂移 |
| 静音段处理 | ❌ 跳跃 | ✅ 平滑 |
| 文本不完全匹配 | ❌ 崩溃 | ✅ 模糊匹配 |
| 保留原文 | ✅ | ✅ |

---

## ffmpeg 命令模板

### 音频提取（从视频中提取音轨）

```bash
/opt/homebrew/bin/ffmpeg \
  -i "<视频文件>" \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 \
  -y "<输出>.wav"
```

> Whisper 最佳输入格式：16kHz 单声道 WAV

### 音频拼接（concat 协议）

```bash
/opt/homebrew/bin/ffmpeg \
  -f concat -safe 0 \
  -i concat_list.txt \
  -c:a aac -b:a 128k \
  -y "<输出>.aac"
```

### 视频混流 - WebM (H5 课件)

```bash
/opt/homebrew/bin/ffmpeg \
  -i "<视频>" -i "<音频>" \
  -map 0:v:0 -map 1:a:0 \
  -c:v libvpx-vp9 -crf 35 -b:v 0 -row-mt 1 -cpu-used 4 \
  -c:a libopus -b:a 64k \
  -y "<输出>.webm"
```

### 视频混流 - MP4 (PPT/本地)

```bash
/opt/homebrew/bin/ffmpeg \
  -i "<视频>" -i "<音频>" \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy \
  -c:a aac -b:a 128k \
  -y "<输出>.mp4"
```

### 静音生成

```bash
/opt/homebrew/bin/ffmpeg \
  -f lavfi -i "anullsrc=r=44100:cl=mono" \
  -t <秒数> \
  -c:a aac -b:a 64k \
  -y "<输出>.aac"
```
