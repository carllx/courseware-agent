---
name: real-asset-scanner
description: 逐字稿真实素材需求扫描引擎。扫描 Markdown 脚本中的 [VISUAL] 块，识别适合从网络搜索/下载真实素材（而非 AI 文生图）的位置，输出按优先级排序的采购清单。当 /write Phase 3 校验或 /audit 执行视觉素材审计时自动触发。也适用于手动执行 /scan_assets 或用户提到"真实素材"、"网络图片"、"替换 AI 生图"时触发。
---

# 技能：真实素材需求扫描引擎 (Real-Asset Scanner)

## TL;DR (≤ 100 字)

**Phase 1**: 扫描脚本 `[VISUAL]` 块 → 八类信号检测（S1-S8）→ 自动跳过已有真实素材。**Phase 2**: 扫描叙事标签（`[CASE STUDY]`/`[ART/AESTHETICS]`/`[STORY TIME]` 等）→ S9 视频优先路由（5 判据：动态性/沉浸感/时序性/权威性/持续时间，≥3 偏向视频）→ 输出 `sourcing_checklist.yaml`。集成于 `/write` Phase 3 和 `/audit` Q2。

## 描述

本技能提供一套自动化扫描规则和 Python 引擎，用于在课程逐字稿中**快速识别需要真实网络素材替代 AI 文生图的视觉位置**。

> [!IMPORTANT]
> **核心原则**：涉及真实历史事件（含伤亡）、具名实体产品、学科人物肖像的 VISUAL 块，**严禁**使用 AI 生成图像。必须引用真实档案、产品照片或公共领域影像。

---

## 1. 三层实体识别架构

扫描引擎采用行业标准的 **Gazetteer → 结构模式 → 上下文信号** 三层优先级架构，实现跨课程通用性：

| 层级 | 名称 | 来源 | 独立触发? | 最高级别 |
|:---|:---|:---|:---|:---|
| 层1 | **Gazetteer 精确匹配** | 课程级 `scanner_entities.yaml` | ✅ 是 | HIGH |
| 层2 | **通用结构模式** | 大写多词组 / 连字符型号 / CamelCase / 缩写+标识 / 书名号 | ⚠️ 需与层3共振 | HIGH（共振时） |
| 层3 | **上下文信号 (S1-S6)** | Scene / Text 字段关键词 | ✅ 是 | MEDIUM |

### 1.1 层3: 九类上下文信号 (S1-S9)

| 编号 | 信号 | 触发模式 | 权重 |
|:---|:---|:---|:---|
| S1 | 真实历史事件 / 新闻档案 | Scene 含 `真实/实录/纪实/档案/历史/archival` | 高 |
| S2 | 产品实物 / 设备 | Scene 含 `实物/设备/prototype/hardware` | 高 |
| S3 | 真实人物肖像 | Scene 含 `肖像/portrait/档案照` | 中 |
| S4 | 真实界面 / UI 截图 | Scene 含 `界面截图/screenshot/real UI` | 中 |
| S5 | 脚本显式标注禁止 AI | Scene 含 `严禁 AI`/`避免 AI 生成` | 最高 |
| S6 | 著作 / 书籍封面 | Scene 或 Text 含 `封面/书籍/著作/教材/book cover` | 中 |
| **S7** | **动态演示 / 交互录屏** | Scene 含 `演示/动态/手势操作/闪烁/滚动/光影互动/demo/gesture/immersive` | **中** |
| **S8** | **教材已有原图** | Scene/Text 中的理论概念关键词命中 `knowledge/textbook/` 章节标题，且该章节含 `![](images/` 引用 | **高** |
| **S9** | **叙事标签视频优先路由** | 叙事标签（`[ART/AESTHETICS]`/`[CASE STUDY]` 等）内容满足 ≥3/5 条视频偏向判据（动态性/沉浸感/时序性/权威性/持续时间） | **中** |

### 1.2 课程级 Gazetteer 配置 (`scanner_entities.yaml`)

在课程根目录放置可选的 `scanner_entities.yaml`，引擎从 `src/` 向上最多遍历 3 层自动查找：

```yaml
# 示例：信息可视化/scanner_entities.yaml
brands:
  - Tableau
  - D3.js
  - Observable
persons:
  - Florence Nightingale
  - Charles Minard
  - Edward Tufte
products:
  - Therac-25
```

**零配置工作**：未找到词典时，引擎退化到纯结构模式（层2 + 层3），仍能自动发现大写多词组、连字符型号等通用具名实体。

---

## 2. 真实素材自动识别 (防重复四层检测)

已有素材满足以下**任一层级**时，自动跳过，不再产出搜索建议：

| 层级 | 检测对象 | 条件 | 理由 |
|:---|:---|:---|:---|
| **层0: 人工决策锁定** | `[VISUAL].**Source**` | 含 `Locked` 关键词 | 用户已审慎决定当前素材足以满足教学需求，禁止再搜索替代 |
| **层1: Asset 文件特征** | `[VISUAL].Asset` 指向的物理文件 | 格式为 `.gif`/`.mp4`/`.webm`/`.jpg`/`.webp`；或文件名含 `_real`；或 PNG 但大小不在 AI 典型 350-950KB 区间 | 非 AI 生成格式/尺寸 |
| **层2: Source 字段** | `[VISUAL].**Source**` | 含 `External`/`Wikimedia`/`CC-BY`/`Fair Use`/`新华社` 等关键词 | 已人工确认来源 |
| **层3: 上下文多媒体** | VISUAL 块前后 5 行正文 | 包含 `.mp4`/`.webm`/`.gif`/`.mp3` 等多媒体链接 | 该位置已有视频/音频素材 |

> [!IMPORTANT]
> **层0 Locked 标记是最高优先级的跳过信号**，优先于所有启发式检测。一旦标记，无论该位置触发了多少信号（包括 no_ai_flag），扫描引擎和 video-downloader 均静默跳过。

> [!TIP]
> AI 生成的 PNG 通常在 350KB-950KB 范围内（1024×1024 标准尺寸）。真实照片/截图通常显著偏小（<200KB，网络截图）或偏大（>1MB，高分辨率相机照片）。此启发式并非完美，但误判率 <5%。

---

## 3. 使用方法

### 3.1 命令行运行

```bash
# 扫描单个教学周（零配置即可工作，自动查找课程词典）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/scan_real_assets.py \
  <课程>/weeks/<周次>/src/

# 扫描单个文件
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/scan_real_assets.py \
  <课程>/weeks/<周次>/src/M01_xxx.md
```

> [!TIP]
> 扫描引擎会从目标目录向上自动搜索 `scanner_entities.yaml`。若存在，Gazetteer 层激活（控制台显示 `📚 加载课程词典`）；若不存在，退化到通用结构模式，仍可正常工作。

### 3.2 输出

- 控制台：按优先级分组的摘要（CRITICAL / ENHANCE / OPTIONAL）
- 文件：`<扫描目录>/sourcing_checklist.yaml`

### 3.3 输出格式

```yaml
- slide: W01_S01g
  module: M01_数字产品之殡_我们为什么会抓狂
  layout: Full
  priority: high
  media_type: image
  signals: [explicit_no_ai, historical_archive, physical_product]
  entities: [Therac-25, DEC VT100]
  description: "认知摩擦害死人：Therac-25 放射治疗仪事故"
  search_queries:
    - "Therac-25 photo"
    - "DEC VT100 real image"
  target_path: ../public/slides/W01_S01g_real.png
  current_asset: ../public/slides/W01_S01g.png
  no_ai_flag: true
  # ─── 用户回填区（扫描后由用户或 Agent 填写）───
  confirmed_urls: []         # 用户确认的下载 URL 列表
  stitch_mode: auto          # auto / single / horizontal / vertical / grid
  disposition: ""            # download / generate / lock / skip（空=待决）
  lock_reason: ""            # disposition=lock 时的锁定理由
```

**`disposition` 四值路由**：
- `download` → 走 `download_and_stitch.py` 下载管线
- `generate` → 走 `/generate_assets` AI 文生图管线
- `lock` → 标记 Source 为 Locked，写入 `lock_reason`
- `skip` → 不处理

### 3.4 下游执行脚本

扫描产出清单后，可调用以下脚本完成下载与注入：

```bash
# 批量下载 + 多图拼接（消费 confirmed_urls 字段）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/download_and_stitch.py \
  <课程>/weeks/<周次>/src/sourcing_checklist.yaml

# Markdown 双轨注入（消费 disposition 字段）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/inject_assets.py \
  <课程>/weeks/<周次>/src/sourcing_checklist.yaml \
  --src-dir <课程>/weeks/<周次>/src/

# 预览模式（不实际修改文件）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/real_asset_scanner/scripts/inject_assets.py \
  <课程>/weeks/<周次>/src/sourcing_checklist.yaml \
  --src-dir <课程>/weeks/<周次>/src/ --dry-run
```

完整的端到端流程请参见 `/source_images` 工作流。

---

## 4. 工作流集成

### 4.1 `/write` Phase 3 集成

在 `write_phase3_verify.md` 的 **Step 3.8 之后**，执行真实素材扫描：

> 运行 `scan_real_assets.py` 对新写模块进行真实素材需求检查。
> 若发现 CRITICAL 级需求（特别是 `no_ai_flag = true`），**必须**在提交前标注或替换。

### 4.2 `/audit` Q2 集成

在 `audit.md` 的 **Q2: 视觉素材完整性** 之后，追加真实素材真实性检查：

> 运行 `scan_real_assets.py` 检查已有 VISUAL 块中是否存在"使用 AI 生图替代真实素材"的违规情况。
> `no_ai_flag = true` 且 `current_asset` 仍为 AI 生成图 → **Needs Revision**。

---

## 5. 素材注入约定

### 5.0 视觉系统遵循约束 (强制)

> [!CAUTION]
> **插入任何视觉素材前，必须遵守以下规则，否则属于违规操作。**

#### R1: 不得覆盖已有多媒体引用

若 `[VISUAL]` 块前后正文中已存在视频/音频链接（如 `▶️ [..](..mp4)`），禁止向该块插入新的图片素材。该位置的视觉体验已经由视频承载。

#### R2: 遮守视觉系统配置

当需要为没有真实素材的位置 **生成 AI 图像** 时（例如用 `generate_image` 工具），必须先读取课程的 `visual_system.yaml` 并按 `rule_visual_generation.md` 的 Prompt 组装协议构建指令。禁止未经检查直接调用生图工具。

#### R3: 不得改变已有块结构

插入素材时，仅允许修改 `**Asset**` 行和添加 `**Source**` 行。禁止删除、重排或替换其他字段（Slide/Layout/Scene/Text/List）。禁止破坏 `▶️` 视频播放行等块外结构。

#### R4: 双轨保留仅限无视频的位置

“`Asset` + `Asset (AI fallback)`”双轨结构仅在没有视频多媒体的位置使用。已有视频的位置保持原始结构不变。

### 5.1 文件命名

```
<原始Slide_ID>_real.<ext>
```

示例：`W01_S01g_real.jpg`

### 5.2 双轨保留

在 `[VISUAL]` 块中保留**两个** Asset 路径：

```markdown
> [VISUAL]
> **Slide**: W01_S01g
> *   **Asset**: ![VT100 终端](../public/slides/W01_S01g_real.jpg)
> *   **Asset (AI fallback)**: ![概念插画](../public/slides/W01_S01g.png)
> **Source**: Wikimedia Commons, CC BY-SA (Fair Use for Education)
> **Scene**: DEC VT100 终端实物照片，Therac-25 操作台
```

H5/PPT 渲染引擎**优先读取** `_real` 版本；不存在时自动 fallback 到 AI 版本。

### 5.3 Source 字段

下载真实素材后，**必须**在 VISUAL 块中添加 `**Source**` 字段注明来源与许可：

```
**Source**: Wikimedia Commons, CC BY-SA 4.0 / Fair Use for Education
**Source**: Microsoft Official Press Kit, 2018
**Source**: 新华社/央视新闻, 2020-11-21
```

### 5.4 素材锁定 (Asset Locking)

当用户审慎决定某个 VISUAL 块**不需要**替换为真实素材时，在 Source 字段中标记 `Locked` 并附注理由：

```markdown
> **Source**: `Locked` -- AI 概念图已充分传达教学意图，无需替换真实素材
> **Source**: `Locked` -- 此处为抽象模型图解，非具名实体
> **Source**: `Locked` -- 视频素材已审慎评估，当前方案最优
```

**效果**：
- `scan_real_assets.py` 将在层0立即跳过，不产出搜索建议
- `video-downloader` 的确认门禁将尊重此标记
- 控制台输出 `锁 跳过 N 个人工锁定的位置`
- 未来 Agent 会话不会再主动为该位置寻找替代素材

**解锁**：删除 Source 行中的 `Locked` 关键词即可恢复扫描。

---

## 6. 参考资源

| 文件 | 说明 |
|:---|:---|
| [scripts/scan_real_assets.py](scripts/scan_real_assets.py) | 扫描引擎核心脚本 |
| [scripts/visual_block_io.py](scripts/visual_block_io.py) | VISUAL 块结构化读写共享模块 |
| [scripts/download_and_stitch.py](scripts/download_and_stitch.py) | URL 批量下载 + 多图拼接引擎 |
| [scripts/inject_assets.py](scripts/inject_assets.py) | Markdown 双轨注入引擎 |
| `/source_images` 工作流 | 端到端的真实图片采购管线 |
| `script_format/SKILL.md` §3 | VISUAL 块字段规范（Asset/Source 字段） |
| `rule_visual_generation.md` | AI 文生图协议（与本技能互补） |
