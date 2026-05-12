---
description: 从逐字稿生成教师备课套件（骨架卡片、冷热弧线、锚词故事线、渐进脱稿）或诊断脚本质量问题（IAR 段落推进率、骨架健康、修复引导）
---

# /cheat_sheet 工作流

> **输入**: 课程名 + 教学单元 ID（如 `交互产品开发 W01`）或指定脚本文件路径
> **输出**: 教师备课套件 Markdown 文件 或 诊断报告

## 双模式分流

本工作流服务于两种**截然不同**的需求，通过参数显式切换：

| 模式 | 命令 | 心智模型 | 输出内容 |
|:---|:---|:---|:---|
| **📖 备课模式**（默认） | `/cheat_sheet <脚本>` | "我在准备上课" | 骨架卡片 + 锚词故事线 + 冷热弧线（纯引导，无警告） |
| **🔍 诊断模式** | `/cheat_sheet <脚本> --diagnose` | "我在排查脚本问题" | IAR 段落诊断 + 骨架健康检查 + 修复引导（质量审计） |

> [!IMPORTANT]
> **默认模式不输出任何 ⚠️ 标记**。教师打开备课套件时看到的应该是安心的记忆路径图，而不是审计告警。
> 排查问题必须显式使用 `--diagnose` 参数。

---

## 📖 备课模式

帮助教师「理」稿而非「背」稿。从万字逐字稿中自动提取：
1. **Visual-First 双轨骨架卡片** — 30 秒扫读版，标题即脉络，Slide 即记忆宫殿
2. **灵魂锚词故事线** — 每个 H3 块压缩为 ≤4 字关键词，串联成可记忆的逻辑链
3. **SCQA 冷热情绪弧线** — 🔥热（感性火花）vs 🧊冷（精准结论）的温度曲线

## 🔍 诊断模式

排查已有脚本的结构与叙事问题，并给出修复引导：
1. **段落推进率诊断 (IAR)** — 标记冗余段、停滞段和结构问题
2. **骨架链健康检查** — 标题逻辑自洽性 + 冷热覆盖完整性
3. **修复引导** — 每个问题标记旁附注具体修复策略
4. **视觉信标对齐诊断** — Signaling Sync 内容类型分流检测 + Text 覆盖率 + Heading 空洞检测

## 理论基础

> 详见 `../../docs/RESEARCH_SPEECH_MEMORIZATION.md`

基于认知负荷理论（Sweller）、双编码理论（Paivio）和图优效应三大认知科学原理。
核心方法：结构化框架法、记忆宫殿（Slide 排版序列）、认知分块（关键词锚定）、色彩编码系统。

---

## 步骤

### Step 1: 定位脚本文件

确认目标课程和教学周的脚本文件路径。支持两种输入：
- 整周：处理 `weeks/W0N_xxx/src/` 下所有模块
- 单模块：处理指定的 `M0X_xxx.md` 文件

### Step 2: 生成备课套件（默认模式）

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/generate_cheat_sheet.py \
  "<脚本路径>" \
  --output "<输出目录>"
```

**输出文件**: `cheat_sheet_<模块名>.md`（纯引导内容，无审计标记）

### Step 3: 诊断脚本问题（显式请求）

当需要审查已有脚本的结构问题时，使用 `--diagnose` 模式：

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/generate_cheat_sheet.py \
  "<脚本路径>" --diagnose
```

输出包含：IAR 逐段分类 + 骨架链健康检查 + 每个问题的修复策略引导。

### Step 3b: 视觉-文字对齐诊断（`--diagnose` 模式自动附加）

> 仅在 `--diagnose` 模式下执行。检查 VISUAL 块的 Text/List 字段是否与 Speech 内容对齐。

// turbo
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_visual_text_sync.py \
  --course "<课程名>" --week <周次>
```

输出包含：
*   **Signaling 缺失**：结构性枚举/操作步骤无 List → 🔴 必修；修辞排比有 List → 🔴 必移除；论证递进有 List → 🟡 建议移除
*   **Text 覆盖率**：含 Text 字段的 VISUAL 块占比（建议 ≥ 50%）→ 🟡 建议
*   **Heading 空洞**：非 Full 布局的 Slide 无标题 → 💡 提示

Agent 应将此输出与 Step 3 的 IAR 诊断合并，形成统一的诊断报告。

### Step 4: 生成指定层级的渐进脱稿提示（可选）

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/generate_cheat_sheet.py \
  "<脚本路径>" --level N
```

**五级递减**：

| Level | 内容 | 适用阶段 |
|:---|:---|:---|
| 1 | 全文逐字稿 | 首次通读 |
| 2 | 色彩标注稿（标签+首句） | 掌握冷热节奏 |
| 3 | Visual-First 骨架（Layout:Scene + 锚词） | 关键词触发训练 |
| 4 | 情绪弧线图（温度曲线+模块编号） | 宏观脉络回忆 |
| 5 | 白板模式（仅 Slide ID） | 完全脱稿，凭 PPT 画面触发 |

---

## 与 `/audit` 的协作

`/audit` Part B-5（脉络清晰度检查）可直接调用本工作流的 `--diagnose` 模式获取自动化报告，
Agent 仅需对标记为 ⚠️ 的模块执行人工复核，避免重复做手动 IAR 分类。
