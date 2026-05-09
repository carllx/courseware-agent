# 脚本撰写规范

> 本文档是逐字稿 `.md` 文件的格式参考手册。所有脚本应严格遵循以下规范。

## 文件命名

- **按章节编号**: `S01_Mobilization.md`、`S02_BasePromo.md`
- **按周次编号**: `W01_Intro.md`、`W02_Basics.md`
- **结构图**: `00_structure_map.md`（固定名称）

## 文件头格式 (Frontmatter)

> **v2.1 (ADR 007)**: Frontmatter 仅包含服务于**脚本写作与大纲结构**的字段。
> 教案索引字段（`supported_objectives`、`task`、结构化 `teaching_requirements`、`steps`）的 SSOT 在 `course.yaml`，**不写入 frontmatter**。

```yaml
---
week: 5
topic: "交互设计与工具入门"           # 对应 course.yaml 的周主题
title: "工具的博物馆：从生态选型到..."  # 本节课的具体标题
theory_hours: 2                    # 理论学时
practice_hours: 3                  # 实践学时
objectives:                        # 教学目标（对应 course.yaml lessons）
  - "理解可视化工具生态"
  - "掌握RAWGraphs进阶用法"
created: 2026-02-19
status: draft                      # draft | review | final
---
```

**字段说明**：
*   `week`: (必填) 整数，对应教学周次。
*   `topic`: (必填) 本周的宏观主题。
*   `title`: (可选) 本课时的具体标题，如不填则默认为文件名。
*   `theory_hours` / `practice_hours`: (可选) 用于生成大纲的学时统计。
*   `objectives`: (可选) 列表，生成大纲中的 `objectives`。

> [!CAUTION]
> **禁止在 frontmatter 中添加教案相关字段**，如 `supported_objectives`、`task`、结构化 `teaching_requirements`、`steps`。这些字段的唯一消费者是教案生成器，不是脚本写作工作流，放在 frontmatter 中只会增加 Agent 处理时的 Token 负担。详见 ADR 007。

### 内容标题
Frontmatter 之后，必须紧跟一级标题（H1）：

```markdown
# 标题内容 (通常与 Frontmatter title 一致)
```

## `> [VISUAL]` 块

> 定义一张 Slide 的内容和布局。**替代已废弃的 `Slide_Database.md`**。

### 格式

```markdown
> [VISUAL]
> *   **Slide**: `S01_Timeline_Matrix`
> *   **Layout**: `Diagram`
> *   **Scene**: 三阶段实习时间轴与关键任务对比图
> *   **Asset**: `S01_Intro/S01_Timeline_Matrix_ai.png`
```

### 字段说明

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| **Slide** | ✅ | Slide ID，全局唯一。格式：`Sxx_PascalCase` |
| **Layout** | ✅ | 排版类型，从有效列表中选取 |
| **Scene** | ✅ | 画面描述，一行中文 |
| **Asset** | 可选 | 物理文件的相对路径（相对于 `visuals/assets/`） |

### 有效 Layout 列表 (语义别名版)

> 📗 编写脚本时，请务必查看 **[VISUAL_LAYOUT_CATALOG.md](./VISUAL_LAYOUT_CATALOG.md)** 获取每种排版所对应的语法范例与底层渲染结果对照。
> 详见 [VISUAL_LAYOUT_SPEC.md](./VISUAL_LAYOUT_SPEC.md) 和 [.agent/skills/script_format/layouts_v2.md](../.agent/skills/script_format/layouts_v2.md)。

为保持写作流畅，本系统采用**语义化版式名称**。作者写明版式诉求即可，底层引擎将通过三层解析系统自动匹配最佳空间网格与内容组件。合法 Layout 限定为以下 12 项：

| 基础空间网格 | 复合教学场景 (语义宏) |
|:---|:---|
| `Center` (居中排版) | `CTA` (行动号召), `Agenda` (大纲目录) |
| `Split` (极简双栏) | `Quote` (金句展示), `Workshop` (指导工坊) |
| `Grid` (常规矩阵) | `Comparison` (红绿对比) |
| `Full` (沉浸满屏) | `Screenshot` (带设备的截图), `Poll` (互动轮询) |
| `Flow` (节点流线) | - |

*(注：不再支持手动定义特定的 List、CodeBlock、Table 等内容类型相关的 Layout，当 `[VISUAL]` 块中存在相应的 `List`, `Code` 字段时，引擎会自动启用特定组件。原有的 20 多种混淆名称现已被强制拦截)*

### 放置规则

`> [VISUAL]` 块应放在**对应正文段落之前**：

```markdown
> [VISUAL]
> *   **Slide**: `S01_Doc_Checklist`
> *   **Layout**: `List`
> *   **Scene**: 实习材料提交清单（申请表、承诺书、三方协议、接收证明）

在第一阶段，你们必须搞定以下几份文件，缺一不可。
```

## `> [ACTIVITY]` 块

> 定义非讲授的教学活动环节（实践、问答、测验、演示）。

### 格式

```markdown
> [ACTIVITY]
> *   **Type**: `Practice`
> *   **Duration**: `5min`
> *   **Desc**: 学生打开 Audition，导入提供的音频素材，尝试自行完成降噪操作
```

### 字段说明

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| **Type** | ✅ | 活动类型，从有效列表中选取 |
| **Duration** | ⚠️ 建议 | 预估时长：`5min`、`30s`、`1.5min` |
| **Desc** | ✅ | 活动内容描述 |

### 有效 Type 列表

| Type | 含义 | 典型时长 |
|:---|:---|:---|
| `Practice` | 学生动手实践 | 3-10 min |
| `QA` | 问答 / 课堂讨论 | 2-5 min |
| `Quiz` | 小测验 / 知识检查 | 1-3 min |
| `Demo` | 教师现场演示 | 2-5 min |

## 知识标签

> 嵌入教学内容的知识扩展块，按**两轴分类**。
>
> 💡 **进阶：结合记忆与脱稿**
> 关于如何利用这些标签作为自动化备课工具中判断"冷热"情绪节奏的信号，以及基于逻辑重建范式（FTT/Bartlett/即兴演讲理论）的全套渐进式脱稿训练，详见 [RESEARCH_SPEECH_MEMORIZATION.md](./RESEARCH_SPEECH_MEMORIZATION.md)。

### 标签白名单

| 轴 | 标签 | 用途 |
|:---|:---|:---|
| **技术层** | `[TECH NOTE]` | 技术细节、参数说明 |
|  | `[WARNING]` | 陷阱、易错点 |
|  | `[DID YOU KNOW]` | 冷知识、技术趣闻 |
| **人文层** | `[STORY TIME]` | 历史起源、名人轶事 |
|  | `[PHILOSOPHY]` | 设计哲学、思想实验 |
|  | `[CASE STUDY]` | 真实案例分析 |
|  | `[LIFE CONNECT]` | 日常生活中的映射 |
| **教学层** | `[TEACHING MOMENT]` | 教学方法论、课堂互动 |

### 格式示例

```markdown
> [TECH NOTE]
> Audition 的降噪功能基于频谱减法 (Spectral Subtraction)。
> 核心参数是 **Noise Reduction Level** 和 **Reduce By**。
```

### 使用建议

- 每份脚本**至少 1 个人文层标签**
- 技术层标签紧跟操作步骤
- 标签可紧跟 `> [VISUAL]` 块，实现知识与画面关联

## 旧格式迁移

> ⚠️ 以下格式已废弃，`validate_spec.py` 会报告为错误。

### `[SLIDE: xxx]` → `> [VISUAL]`

```diff
- > **[SLIDE: S01_Timeline_Matrix]**
- 展示三阶段时间轴。
+ > [VISUAL]
+ > *   **Slide**: `S01_Timeline_Matrix`
+ > *   **Layout**: `Diagram`
+ > *   **Scene**: 三阶段实习时间轴与关键任务对比图
+
+ 展示三阶段时间轴。
```

### `[PACING]` → `> [ACTIVITY]`

```diff
- > [PACING] ⏸ 5min
+ > [ACTIVITY]
+ > *   **Type**: `Practice`
+ > *   **Duration**: `5min`
+ > *   **Desc**: 学生自行完成降噪操作
```

## 视觉资产命名规范

详见 [资产管理协议](../.agent/rules/rule_asset_management.md)。

### 前缀（来源标识）

| 前缀 | 含义 | 示例 |
|:---|:---|:---|
| `Sxx_` | 核心素材 | `S02_noise_reduction.png` |
| `ref_` | 参考图 | `ref_color_palette.png` |

### 后缀（生成方式）

| 后缀 | 含义 | 示例 |
|:---|:---|:---|
| `_ai` | AI 生成 | `S06_concept_ai.png` |
| `_web` | 网络搜索 | `S06_diagram_web.jpg` |
| `_cap` | 截图 | `S07_panel_cap.png` |
| `_rec` | 录屏 | `S07_demo_rec.mp4` |
| `_photo` | 实拍 | `S11_setup_photo.jpg` |
