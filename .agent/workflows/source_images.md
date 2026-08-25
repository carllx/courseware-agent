---
description: 为指定教学周扫描脚本中的真实图片素材需求、执行网络调研、生成用户审批清单、批量下载拼接并注入 Markdown 脚本
---

# /source_images — 真实图片素材采购管线

从脚本中的 `[VISUAL]` 块自动识别真实图片需求 → 输出带搜索建议的清单 → 用户审批并填写 URL → 批量下载/拼接 → Markdown 双轨注入。

> **镜像关系**: 本工作流是 `/source_videos`（视频采购）的图片对等版本。

## 前置条件

- 目标教学周 `src/` 目录下已有 Markdown 逐字稿
- `real-asset-scanner` 技能已安装

---

## §1 定位目标教学周

1. 从用户指令中提取目标教学周（如 "W02"、"第二周"、"认知摩擦"）
2. 若未指定，从当前打开的脚本文件路径推导：`src/M0X.md` → 上上级 `weeks/WXX_*/`
3. 确认 `src/` 目录下有至少一个 `M*.md` 文件
4. 确认 `public/slides/` 目录存在（不存在则创建）

**输出**：锁定目标路径 `<课程>/weeks/WXX_*/src/`

---

## §2 自动扫描真实图片候选

// turbo
运行 `scan_real_assets.py` 对目标教学周执行全量扫描：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/scan_real_assets.py \
  <课程>/weeks/<周次>/src/
```

从输出的 `sourcing_checklist.yaml` 中筛选 `media_type: image` 的条目。

**输出**：`sourcing_checklist.yaml` — 包含搜索建议和待填写的用户回填区

**同时人工复读**：Agent 应逐文件阅读 `src/M*.md` 正文及叙事标签
（`[CASE STUDY]`、`[ART/AESTHETICS]`、`[STORY TIME]`、`[LIFE CONNECT]`），
识别扫描引擎因无 `[VISUAL]` 块而遗漏的真实素材需求。

---

### §2.3 视频交叉路由 (Video Cross-Routing)

在图片候选清单完成后，Agent 必须对每个候选执行视频优先评估：

1. **评估五判据**：动态性 / 沉浸感 / 时序性 / 权威性 / 持续时间
2. 若 ≥3 条偏向视频 → 将该候选的 `media_type` 从 `image` 改为 `video`
3. 在审批清单中以 `🎬 建议升级为视频` 标注
4. 用户审批时可决定是否接受升级（接受 → 该候选转入 `/source_videos` §3 流程）

> [!TIP]
> 典型视频升级场景：艺术装置体验（Turrell Skyspaces）、经典实验过程（看不见的大猩猩）、
> 产品交互演示（Apple 解锁动画）、建筑空间漫游（Zaha Hadid 作品）

---

## §2.5 教材库优先匹配 (Textbook-First Check)

> **教材优先原则**：教材原版图的学术权威性高于网络搜索图，且无版权风险。
> **关联规则**: `rule_textbook_sourcing.md`  |  **关联工作流**: `/sync_textbook_visuals`

1. 检查当前课程的 `knowledge/textbook/` 目录。若不存在或为空 → 跳过，直接进入 §3。
2. 对 §2 扫描出的每个候选 VISUAL 块，提取其核心概念关键词。
3. 对照 `knowledge/textbook/` 下各教材的章节标题，定位可能包含相关插图的章节。
4. 对命中章节使用 `grep_search` 检索 `![](images/` 引用，逐图审阅图注（Figure Caption）。
5. 对匹配项：
   - 从 `sourcing_checklist.yaml` 中将该条目的 `disposition` 标记为 `textbook`
   - 执行迁移：复制到 `public/textbook/`，更新脚本 VISUAL 块引用
   - 该条目**不再进入 §3 的网络搜索流程**
6. 在 §3 清单中标注已通过教材匹配解决的条目，便于用户审阅。

---

## §3 清单增强与用户审批

Agent 对清单进行增强处理：

1. **搜索辅助**：对每个 HIGH 优先级条目，使用 `search_web` 工具执行关键词搜索，
   尝试定位可用的图片 URL（优先 Wikimedia Commons、官方 Press Kit、无版权高清图站）
2. **补充建议**：在清单中填入 Agent 建议的 `confirmed_urls` 和 `stitch_mode`
3. **分类路由**：根据素材性质预设 `disposition` 建议值：
   - 具名实体/历史事件/产品实物 → `download`
   - 抽象概念/心理模型/理论图解 → `generate`（交给 `/generate_assets`）
   - 用户指定保留 AI 素材 → `lock`

整理为一份 Markdown Artifact（`image_sourcing_candidates.md`）：

```markdown
### N. <Slide ID> — <描述> (<模块>)
**📷 图片素材确认**
- **优先级**：<HIGH/MEDIUM/LOW>
- **建议 URL**：<URL 列表>
- **拼接模式**：<horizontal / vertical / single>
- **建议处置**：<download / generate / lock>
- **搜索词**：<search_queries>
```

> [!IMPORTANT]
> **门禁点**：此步骤完成后，**必须等待用户明确批准**才能继续。
> 用户可以：
> - 逐条审批或全部批准
> - 替换/追加 URL
> - 调整 stitch_mode 或 disposition
> - 标记特定条目为 `lock` 或 `skip`

---

## §4 回写用户决策到清单

将用户的审批结果回写到 `sourcing_checklist.yaml` 的对应字段：
- `confirmed_urls`: 用户确认的 URL 列表
- `stitch_mode`: 拼接模式
- `disposition`: 处置路由（download / generate / lock / skip）
- `lock_reason`: 锁定理由（如适用）

---

## §5 批量下载与拼接

// turbo
对所有 `disposition: download` 的条目，调用下载引擎：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/download_and_stitch.py \
  <课程>/weeks/<周次>/src/sourcing_checklist.yaml
```

**功能**：
- 按 `confirmed_urls` 逐条下载（含 5 次指数退避重试）
- 根据 `stitch_mode`（或自动从 Layout 推断）执行多图拼接
- 输出到 `target_path` 指定的 `public/slides/<slide_id>_real.<ext>`
- 生成 `download_report.yaml`

**交付物**：`public/slides/` 下的 `_real.jpg` / `_real.png` 文件

---

## §5.5 AI 文生图（可选）

对所有 `disposition: generate` 的条目：

1. 按 `/generate_assets` 工作流的 Step 1-4 生成图片
2. 将产物命名为 `<slide_id>_real.png` 并移入 `public/slides/`
3. 在 `download_report.yaml` 中追加生成记录

> [!TIP]
> 如果 generate 条目较多（≥5），建议拆分为独立的 `/generate_assets` 调用以利用其完整的设计系统对齐流程。

---

## §6 Markdown 脚本注入

// turbo
调用注入引擎，将下载/生成的素材批量写入脚本：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/inject_assets.py \
  <课程>/weeks/<周次>/src/sourcing_checklist.yaml \
  --src-dir <课程>/weeks/<周次>/src/
```

**注入规则**（遵循 `real-asset-scanner` SKILL.md §5）：
- `disposition: download` → 双轨注入（`Asset` + `Asset (AI fallback)` + `Source: Web Source`）
- `disposition: generate` → 双轨注入（`Asset` + `Asset (AI fallback)` + `Source: AI Generated`）
- `disposition: lock` → 仅更新 Source 为 `Locked -- <理由>`
- `disposition: skip` → 不修改

**幂等性**：已有 `_real` 路径的块自动跳过，重复执行不会破坏结构。

---

## §7 验收与交付

// turbo
1. 运行资产验证（如 `validate_real_assets.py` 可用）：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_real_assets.py \
  --course "<课程名>" --week <周次>
```

2. 检查产出统计：
   - ✅ 成功注入的 Slide 列表
   - 🔒 已锁定的 Slide 列表
   - ❌ 失败项（附原因）

3. 输出交付报告 Artifact（`walkthrough.md`），包含：
   - 素材来源明细（URL + 处置决策）
   - 拼接模式与输出尺寸
   - 注入统计

---

## §8 收尾 (Epilogue)

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）+ E3（链接验证）。

---

## 与其他扩展的关系

| 扩展 | 关系 |
|:---|:---|
| `real-asset-scanner` (SKILL) | §2 步骤的扫描引擎 + §5-§6 步骤的下载/注入脚本 |
| `/source_videos` (Workflow) | **镜像关系**：视频版采购管线，共享 §2 扫描步骤 |
| `/generate_assets` (Workflow) | §5.5 步骤的 AI 文生图执行引擎 |
| `rule_asset_placement_guard` (Rule) | §5 步骤的路径合规校验 |
| `rule_visual_generation` (Rule) | §5.5 步骤的生图协议约束 |
| `scripts/validation` (Scripts) | §7 步骤的资产验证 |
