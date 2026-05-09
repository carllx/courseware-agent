---
trigger: model_decision
description: 当 Agent 执行视频/图片下载、ffmpeg 转码、文件移动等操作并将产物写入 public/ 目录时，强制校验目标路径是否在周次级 weeks/W0X_*/public/ 内，禁止写入课程级 <课程>/public/。
---

# 规则：资产落位守卫 (Asset Placement Guard)

> **核心原则**：V5 自洽包架构下，所有媒体资产必须存放在**周次级** `weeks/W0X_*/public/` 内。课程级 `<课程>/public/` 是禁区。

## TL;DR

- ✅ 正确：`信息可视化/weeks/W01_Visual_Perception/public/videos/demo.webm`
- ❌ 错误：`信息可视化/public/videos/demo.webm`
- 写入前必须用绝对路径确认目标包含 `weeks/W0X` 层级

## §1 触发时机

本规则在以下操作**执行前**自动触发：

1. `yt-dlp` 或 `ffmpeg` 的 `-o` / `-y` 输出路径包含 `public/videos/` 或 `public/slides/`
2. `mv` / `cp` / `write_to_file` 的目标路径包含 `public/`
3. Agent 讨论"保存视频到"、"输出到"、"导出到"等落位操作

## §2 校验协议

Agent 必须在写入前完成以下 3 步自检：

### 2.1 路径层级确认

```
目标路径是否匹配: <课程>/weeks/W[0-9]{2}_*/public/{slides,videos,textbook,data,practice}/
  ├── 是 → ✅ 继续执行
  └── 否 → ❌ 阻断，报告违规并修正路径
```

### 2.2 周次归属推导

如果 Agent 无法确定目标周次：

1. 从当前正在编辑的脚本路径中提取（`src/M0X.md` → 上上级 `weeks/W0X_*/`）
2. 从用户指令中的周次关键词推导（"第一周"、"W01"）
3. 无法推导时 → **主动询问用户**，不得猜测默认值

### 2.3 绝对路径输出

所有 `yt-dlp -o`、`ffmpeg -y`、`mv`、`cp` 命令的目标参数**必须使用绝对路径**。
禁止使用 `../` 等相对路径（与 video-downloader §3 路径防漂移红线一致）。

## §3 禁止行为

- ❌ 向 `<课程>/public/videos/` 写入任何视频文件（该目录仅存在于非 V5 课程的历史遗留中）
- ❌ 向 `<课程>/public/slides/` 写入任何图片文件
- ❌ 使用相对路径 `-o "../public/videos/xxx"` 作为下载/转码输出
- ❌ 在无法确定周次归属时"先放到课程根目录再移动"
- ❌ 将中间产物（`.part`、`Video.*`、临时 `.py` 脚本）遗留在任何 `public/` 目录中

## §4 违规补救

如果发现文件已存放在课程级 `public/`：

1. 将文件**移动**到正确的周次级目录
2. 确认脚本中的 `[VISUAL]` Asset 引用路径无需修改（`../public/` 相对路径在周次级是正确的）
3. 运行 `validate_asset_placement.py --course "<课程>"` 确认零违规
4. 清理课程级 `public/` 中不应存在的临时文件

## §5 与现有规则的关系

| 规则 | 关系 |
|:---|:---|
| `rule_asset_management.md` §3.3 | 本规则是其 `[!WARNING]` 的运行时执行层 |
| `rule_visual_video_isolation.md` | 互补：该规则管 VISUAL 块格式，本规则管物理文件位置 |
| `video-downloader` §3 路径防漂移 | 互补：该技能管路径格式（绝对 vs 相对），本规则管路径层级（周次 vs 课程） |
