---
description: 使用通用生成器从 Markdown 脚本自动生成课程 PPT
---

# /ppt 工作流 (统一管线版 v2)

本工作流使用 workspace 级 `engines/generate_course_ppt.js` 通用生成器，**一条命令**即可完成从 Markdown 脚本到 NFU 品牌成品 PPTX 的全链路输出。

## 输出规范

### 统一命名

所有产物遵循 **`<课程ID>_<周次ID>_<产物类型>.pptx`** 格式：

| 产物 | 命名示例 | 位置 |
|------|---------|------|
| **品牌成品** ★ | `信息可视化_W01_Visual_Perception_Branded.pptx` | `build/artifacts/W01_Visual_Perception/` |
| 裸 PPT（中间产物） | `信息可视化_W01_Visual_Perception_Presentation.pptx` | `build/artifacts/_intermediate/` |

### 目录结构

```
<课程>/build/
├── artifacts/                         ← 所有课件交付物
│   ├── W01_Visual_Perception/
│   │   └── 信息可视化_W01_..._Branded.pptx   ← ★ 最终交付物
│   ├── W02_Design_Principles/
│   │   └── ...
│   └── _intermediate/                 ← 中间产物（裸 PPT）
│       └── 信息可视化_W01_..._Presentation.pptx
├── h5_preview/                        ← H5 Vite 项目
├── presentations/                     ← 旧版兼容（自动镜像）
└── tts/                               ← TTS 纯文本
```

## 前置条件

1. **环境**: Node.js 环境已就绪
2. **依赖**: workspace 根目录下已运行 `npm install`（`pptxgenjs`, `js-yaml`, `image-size`）
3. **品牌**: `.agent/skills/pptx-nfu-branded/` 目录存在（自动检测，缺失则降级为裸 PPT）
4. **主题**: 课程 `course.yaml` 中配置了 `visual_system: "@theme:xxx"`（可选）

## 执行步骤

### Step 1: 准备资源

确保脚本中的 Visual Asset 路径正确（V5 架构：`weeks/W0X/public/slides/`）。

### Step 1.5: 视频资产预检（含视频时自动执行）

若脚本中包含视频 Asset（`.webm`/`.mp4`），引擎会自动执行以下预处理：

1. **格式转码**：`.webm` → `.mp4`（H.264 + AAC），缓存于 `.build/_video_pptx/`
2. **硬字幕烧录**：自动检测同名 `.zh-Hant.vtt` / `.en.vtt`，烧录至 MP4 画面
3. **Poster 提取**：从视频 3 秒处提取封面图，作为 PPT 中视频未播放时的占位
4. **嵌入方式**：使用 PptxGenJS `addMedia()` 原生嵌入，教师可直接在 PPT 中点击播放

> **缓存策略**：仅在源视频或字幕文件更新时重新转码（比较 mtime），首次转码每个视频约需 10-30 秒。

> **降级保护**：若 ffmpeg 转码失败，自动回退到 poster 静态截图模式（旧行为）。

### Step 2: 运行生成器（一键全链路）

在 **workspace 根目录** 下运行：

```bash
node engines/generate_course_ppt.js <课程目录> <脚本相对路径>
```

**示例**:
```bash
# 信息可视化 W01
node engines/generate_course_ppt.js 信息可视化 weeks/W01_Visual_Perception/package.yaml

# 交互产品开发 W01
node engines/generate_course_ppt.js 交互产品开发 weeks/W01_Interaction_Basics/package.yaml
```

> **自动化流程**:
> 1. 加载课程主题 (visual_system.yaml)
> 2. 编译 package.yaml → compiled.md
> 3. 解析 [VISUAL]/[SPEECH] 标签
> 4. 生成裸 PPT → `_intermediate/`
> 5. **自动调用 NFU 品牌注入** → `artifacts/<周次>/` ★
> 6. 向后兼容复制到 `presentations/`

### Step 3: 验证

品牌成品位于 `<课程>/build/artifacts/<周次>/`。

确认：
1. **封面页**: NFU 深灰品牌封面存在，课程名/教师/学期信息正确
2. **配色**: 符合课程 `visual_system.yaml` 主题
3. **目录/引用/作业/封底**: 品牌固定环节完整
4. **备注**: Speaker Notes 清晰易读

### Step 4 (可选): 逆向同步 Notes

如果在 PowerPoint 中直接编辑了 Presentation Notes，可逆向同步回 Markdown 脚本：

```bash
# 先 dry-run 查看差异
/opt/anaconda3/envs/mybase/bin/python engines/sync_notes_back.py \
  --pptx "<课程>/build/artifacts/<周次>/<课程>_<周次>_Branded.pptx" \
  --script "<课程>/weeks/W0X_Name/package.yaml" \
  --dry-run

# 确认无误后实际同步
/opt/anaconda3/envs/mybase/bin/python engines/sync_notes_back.py \
  --pptx "<课程>/build/artifacts/<周次>/<课程>_<周次>_Branded.pptx" \
  --script "<课程>/weeks/W0X_Name/package.yaml"
```

## 故障排除

- **Warning: Asset not found**: 检查 `weeks/W0X/public/slides/` 下是否有对应图片
- **⚠️ 品牌注入失败**: 检查 `course.yaml` 是否存在且格式正确。裸 PPT 仍可使用
- **Warning: color not valid**: 检查 `visual_system.yaml` 格式（应包含 top-level `palette`）
- **Error: Cannot find module**: 在 workspace 根目录运行 `npm install`
- **⚠️ [Video→PPTX] 转码失败**: 检查 ffmpeg 是否在 `/opt/homebrew/bin/ffmpeg`，以及视频文件是否损坏。转码失败时会自动降级为 poster 模式
- **⚠️ [Video→PPTX] 转码产物未生成**: 磁盘空间可能不足，或 ffmpeg 因超时（120s）被终止。对于超长视频建议手动预转码
- **视频在 PPT 中无法播放**: 确认使用 Microsoft PowerPoint（LibreOffice 对嵌入视频支持有限）。也可检查 `.build/_video_pptx/` 下的 MP4 文件是否完整
