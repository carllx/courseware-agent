---
description: 为指定教学周扫描脚本中的视频候选、执行网络调研、生成审批清单并批量下载转码
---

# /source_videos — 教学视频素材采购管线

从脚本中的 `[VISUAL]` 块自动识别视频候选 → 网络调研匹配视频源 → 生成候选审批清单 → 用户审批 → 批量下载/字幕/转码 → 脚本注入。

## 前置条件
- 目标教学周 `src/` 目录下已有 Markdown 逐字稿
- `video-downloader` 技能已安装且 §1 环境检查通过

---

## §1 定位目标教学周

1. 从用户指令中提取目标教学周（如 "W02"、"第二周"、"认知框架"）
2. 若未指定，从当前打开的脚本文件路径推导：`src/M0X.md` → 上上级 `weeks/WXX_*/`
3. 确认 `src/` 目录下有至少一个 `M*.md` 文件
4. 确认 `public/videos/` 目录存在（不存在则创建）

**输出**：锁定目标路径 `<课程>/weeks/WXX_*/src/`

---

## §2 自动扫描视频候选

// turbo
运行增强版 `scan_real_assets.py` 对目标教学周执行全量扫描：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/scan_real_assets.py \
  <课程>/weeks/<周次>/src/
```

从输出的 `sourcing_checklist.yaml` 中筛选 `media_type: video` 的条目，
这些就是自动识别的视频候选。

**同时人工复读**：Agent 应逐文件阅读 `src/M*.md`，补充扫描引擎可能遗漏的视频候选
（重点关注以下标签类型中描述的动态场景、沉浸式体验或交互过程）：

| 重点标签 | 视频信号关键词 |
|:---|:---|
| `[ART/AESTHETICS]` | 装置艺术、沉浸体验、光影互动、投影映射、行为艺术 |
| `[CASE STUDY]` | 实验过程、产品交互、动态演示、用户测试录像 |
| `[STORY TIME]` | 历史纪录片、经典实验影像 |
| `[LIFE CONNECT]` | 日常交互过程、App 操作流程 |

**视频优先判据**：当叙事标签内容满足 ≥3 条视频偏向信号（动态性/沉浸感/时序性/权威性/持续时间）时，
该素材应优先作为视频候选录入，而非图片候选。

**输出**：视频候选实体列表（实体名 + 对应的 VISUAL 块 Slide ID + 建议截取描述）

---

## §3 网络调研

对 §2 产出的每个候选实体，执行精准搜索：

1. **搜索策略**遵循 `video-downloader` §0.1：
   - 搜索查询必须包含具体实体名（禁止泛词）
   - 中国产品/案例 → 优先 B站（`bilibili.com`）
   - 国际案例 → YouTube（`yt-dlp ytsearch`）

2. **并行搜索**：对独立的实体可同时发起多个搜索命令

3. **候选筛选**：至少浏览 3 个结果的标题和时长，选择匹配度最高的

**输出**：每个候选填充 URL、标题、时长、建议截取时段

---

## §4 生成候选确认清单

将所有候选整理为一份 Markdown Artifact（`video_sourcing_candidates.md`），格式遵循 `video-downloader` §0.2：

```markdown
### N. <案例名称> (<模块>)
**📹 候选视频确认**
- **标题**：<视频标题>
- **链接**：<URL>
- **时长**：<总时长>，拟截取 `<起始>–<结束>`
- **匹配度**：<高/中/低> — <一句话理由>
- **与脚本 Scene 的对照**：「<Scene 原文摘要>」
```

> [!IMPORTANT]
> **门禁点**：此步骤完成后，**必须等待用户明确批准**才能继续。
> 用户可以逐条审批、全部批准、或要求替换某个候选。

---

## §5 批量下载与转码

用户批准后，将候选清单转换为 `video_tasks.yaml` 格式：

```yaml
- id: v01
  url: "<URL>"
  start: "<起始>"
  end: "<结束>"
  name: "<模块>_<案例名>"
  subtitle_lang: "zh-Hans"
```

// turbo
然后调用批量处理脚本（后台执行）：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  <video-downloader>/scripts/batch_video_processor.py \
  video_tasks.yaml \
  --output-dir "<weeks/WXX_*/public/videos/>"
```

**交付物**：每支视频的 `.mp4` + `.webm` 双格式文件 + 中文硬字幕

---

## §6 脚本注入

遵循 `video-downloader` §7.4 和 `script-format` §3 视频型 Asset 规范：

1. 定位每支视频对应的 `[VISUAL]` 块
2. 将 `**Asset**` 路径替换为 `![描述](../public/videos/<视频名>.webm)`
3. 设置 `**Layout**` 为 `Full`（或 `Video`）
4. 补充必填字段：
   - `**Source**`: `Video` — <来源说明>
   - `**Duration**`: 通过 ffprobe 自动提取
   - `**TimeCategory**`: `activity`（>30s）或 `lecture`（≤30s）
5. 如果原 VISUAL 块有 `**Asset (AI fallback)**`，删除该行（视频块禁止双轨）
6. 遵循 `script_format/SKILL.md` §3 视频型 Asset 规范：一块一视频原则

---

## §7 卫生检查与交付报告

// turbo
1. 清理 `public/videos/` 中所有 `_temp_*` 中间文件
2. 验证每个产物文件体积 > 100KB（防空壳文件）
3. 输出交付报告 Artifact（`walkthrough.md`），包含：
   - 所有成功落地的视频列表（文件名、格式、大小、时长、字幕状态）
   - 失败项及原因
   - 脚本注入状态

---

## 与其他扩展的关系

| 扩展 | 关系 |
|:---|:---|
| `real-asset-scanner` (S7) | §2 步骤的自动化信号源 |
| `video-downloader` (§7/§8) | §5 步骤的底层执行引擎 |
| `script-format` (§3) | §6 步骤的 VISUAL 块规范 + 一块一视频校验 |
| `rule_asset_placement_guard` | §1/§5 步骤的路径合规校验 |
