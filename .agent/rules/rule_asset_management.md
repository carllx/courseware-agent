---
trigger: glob
description: 当编辑 weeks/delivery 目录下的文件时，强制执行资产命名规范与 SSOT 引用规则。
globs:
  - "**/visuals/**"
  - "**/weeks/**"
  - "**/build/**"
---

# 规则：资产管理协议 (Asset Management Protocol)

**生效范围**: 所有课程的 `visuals/`、`scripts/`、`weeks/`、`delivery/` 目录。

## 1. 核心哲学

*   **Spec-First (定义先行)**: 任何物理文件出现前，必须先在数据源中定义。
*   **Decoupled Pipelines**: 内容创作与工程实现解耦，可并行推进。

## 2. 单一事实来源 (SSOT)

每个课程内的 SSOT 对应关系：

| 信息类型 | 存储位置 | 说明 |
|:---|:---|:---|
| **PPT 视觉内容** | `<课程>/weeks/Sxx_*/src/*.md` 中的 `> [VISUAL]` 块 | Slide 定义内联于脚本（`slide_database.md` 已废弃） |
| **视觉生成标准** | `course.yaml` 内 `agent.standards` 指定的共享配置文件指针 | 全局统一的 AI 生图色彩、风格、Prompt 模板 |
| **课程结构** | `<课程>/weeks/_archive/00_structure_map.md` | 教学节奏与时间轴 |
| **教材知识** | `<课程>/knowledge/` | 教材、术语表、教纲 |

## 3. 命名规范

### 3.1 视觉资产前缀系统

| 前缀 | 含义 | 示例 |
| :--- | :--- | :--- |
| `Sxx_` 或 `Wxx_` | **核心素材** — 按章节/周次编号 | `S02_noise_reduction.png` |
| `ref_` | **参考图** — 仅灵感参考 | `ref_color_palette.png` |
| `doc_` | **文档** — 研发笔记 | `doc_design_notes.md` |

### 3.2 来源后缀

| 后缀 | 含义 | 示例 |
| :--- | :--- | :--- |
| `_ai` | AI 生成 | `S06_concept_ai.png` |
| `_web` | 网络搜索 | `S06_diagram_web.jpg` |
| `_cap` | 截图 | `S07_panel_cap.png` |
| `_rec` | 录屏 | `S07_demo_rec.mp4` |
| `_photo` | 实拍 | `S11_setup_photo.jpg` |

### 3.3 目录结构

使用 **"模块卡槽"** 而非状态文件夹：

```text
# 旧架构（交互产品开发、实习指导等）
<课程>/weeks/*/assets/slides/
├── _Global/              (Logo, 水印等)
├── S01_Intro/            (章节 1)
├── S02_Basics/           (章节 2)
└── ...

# V5 Package 新架构（信息可视化等）— 教学周自洽单元包
<课程>/weeks/
├── W01_Visual_Perception/
│   ├── src/              (源切片，如 M01.md)
│   ├── .build/           (引擎生成的 compiled.md)
│   ├── package.yaml      (索引组装器)
│   └── public/           (全部资产存放区)
│       ├── slides/       (理论幻灯片素材 — 仅 .png/.jpg)
│       ├── videos/       (视频素材 — .webm/.mp4 + 衍生字幕 .vtt)
│       ├── textbook/     (教材引用图)
│       ├── practice/     (实践素材)
│       └── data/         (数据文件)
└── W02_Design_Principles/
    └── public/...
```

> [!NOTE]
> **V5 相对路径约束**：在 V5 架构下，所有 `src/*.md` 碎片内部的资产声明必须使用跳出一层的 `../public/` 前缀（如 `![预览](../public/slides/S01.png)`）。这样能兼容 Typora 和 VSCode 的原生渲染器，同时底层的 PPT/H5 Node 解析器也会自动清洗该路径。

> [!WARNING]
> **禁止使用 course 级 `public/`**：视频和图片必须存放在**教学周级** `weeks/W0X/public/` 内（如 `weeks/W01/public/videos/demo.webm`），**禁止**存放在课程根目录的 `<课程>/public/` 中。原因：(1) V5 架构的自洽包原则要求每个教学周可独立分发；(2) `find_image()` 引擎的 `../` 清洗会将 course 级和 week 级路径混淆导致 Symlink 寻址失效；(3) 构建垃圾（如 yt-dlp 的中间 MP4 产物）容易误存到 course 级污染仓库。

> [!NOTE]
> **`--fragment` 模式路径**：H5 引擎的 `--fragment` 模式（ADR 036）直接从 `src/M0X.md` 读取源文件，不经过 `.build/compiled.md`。此模式下 `srcPath` 天然指向源文件精确行号，无需源映射回馈。

> [!NOTE]
> **`--rebuild-week` 热重载路径**（ADR 037）：Vite 插件触发时，Python 引擎重建整个教学周 JSON 并写入 `build/h5_preview/public/courses/<courseId>/<weekName>.json`，同时兼容写入 `build/h5_preview/public/slides.json`。此模式包含完整编译和源映射。

### 3.4 教材资产硬拷贝与跨域隔离原则 (Textbook Asset Isolation)
❌ **禁止事项**：绝对禁止在逐字稿中直接通过深层相对路径（如 `../../knowledge/textbook/...`）调用公用知识库内的大书原图。
✅ **执行标准**：如果原书中有必须引入的高质量视觉素材，必须进行**实名复制/迁移**。将该大书截图拷贝存放至当前周次教学模块自己的内网库 `public/textbook/` 里，然后在 Markdown 脚本内引用 `../public/textbook/目标图.jpg`，确保当前文件夹变成一个不缺胳膊少腿、发给任何人直接能一键渲染的纯净“自洽包”。

### 3.5 多模态媒体支持 (Video & CC Subtitles)
根据 ADR 042，在 `[VISUAL]` 块内现在原生支持视频流挂载，必须遵循**"纯净 Markdown 壳"**协议：
✅ **正确写法**：`> *   **Asset**: ![视频演示](../public/videos/xyz.webm)` (必须使用 `![]` 以通过 AST 解析)
❌ **错误写法**：在 Asset 字段强行写 `<video>` 原始 HTML。
❌ **错误写法**：将视频文件放入 `public/slides/`（该目录仅存放静态图片）。

**Layout 字段约定**：包含视频的 VISUAL 块应将 Layout 设置为 `Video`（映射到 `full` → `Layout_Image`，但语义标记该 Slide 为视频而非静态图，供审计引擎识别）。

**格式优先级**：H5 课件必须使用 `.webm`（VP9 + Opus），PPT 嵌入使用 `.mp4`（H.264）。使用 FFmpeg 转码命令：
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 35 -b:v 0 -row-mt 1 -c:a libopus -b:a 64k output.webm
```

**衍生字幕轨协议**：H5 引擎侦测到 `.mp4/.webm` 扩展名后分发原生播放面板（`AssetPlaceholder.jsx`），并会**自动寻址**源目录同名的 `.zh-Hant.vtt`（默认显示）与 `.en.vtt`（英文字幕），实现无埋点挂载。请确保所有视频放入 `public/videos/` 时连同字幕轨一并命名落位。

**SSG 引擎依赖**：`generate_course_h5.py` 的 `create_symlinks()` 必须为 `public/` 创建符号链接才能使 Vite 开发服务器正确serve视频文件。若 H5 预览中视频无法播放，优先检查 `build/h5_preview/public/courses/<courseId>/` 下是否存在 `weeks` 和 `public` 两个 symlink。

## 4. 质量保证

在课程根目录下运行验证：
```bash
python .agent/skills/validation_suite/scripts/validate_links.py
```