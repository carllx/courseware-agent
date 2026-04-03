---
description: 根据脚本中的 [VISUAL] 块批量生成视觉资产
---

# /generate_assets 工作流

> **输入**: 脚本文件路径（如 `实习指导/weeks/S01_Mobilization/src/M01.md` 或 `信息可视化/weeks/W01_Visual_Perception/package.yaml`）
> **输出**: 脚本同级 `assets/slides/` 或 `<课程>/weeks/*/assets/slides/` 中的图片文件

## Step 0: 课程根目录定位 (必须首先执行)

从输入的脚本文件路径推断课程根目录：
-   **新架构**：脚本路径格式为 `<课程>/weeks/W0X_Name/package.yaml`，课程根目录 = 脚本文件所在目录的**上两级**
-   验证：课程根目录下必须存在 `course.yaml`

```
例: 输入 "实习指导/weeks/S01_Mobilization/src/M01_Topic.md"
     → 课程根目录 = "实习指导/"
例: 输入 "信息可视化/weeks/W01_Visual_Perception/package.yaml"
     → 课程根目录 = "信息可视化/"
     → 验证 "信息可视化/course.yaml" 是否存在
```

> [!IMPORTANT]
> 如果 `course.yaml` 不存在，**立即终止**并提示用户先运行 `/new_course` 创建课程配置。

## Step 0.5: 字数达标门控 (前置检查)

> [!CAUTION]
> **强制前置检查**：在生成任何视觉资产之前，必须先确认目标脚本的字数预算全部达标。

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程名>" --module-breakdown --week <N>
```

- 若验证器返回 exit code 1（存在严重不足模块）→ **立即终止**，提示用户先执行 `/write` DRP
- 若验证器返回 exit code 0 → 继续 Step 1

## 关键路径

| 资源 | 路径 |
|------|------|
| **设计系统 (人读)** | `course.yaml` 内 `agent.standards` 指定的全局配置 |
| **视觉系统 (机读)** | `course.yaml` `agent.standards.visual_system` 指定的相对路径 (如 `../.agent/styles/*.yaml`) |
| **生成规则** | `.agent/rules/rule_visual_generation.md` |
| **本地化规则** | `.agent/rules/rule_localization.md` |
| **脚本文件** | `<课程>/weeks/*_*/src/*.md` 或 `<课程>/weeks/W0X_Name/package.yaml` |
| **资产目录** | `<课程>/weeks/W0X_Name/assets/slides/`（新架构）或 `<课程>/weeks/*/assets/slides/`（旧架构） |

## 执行步骤

### Step 1: 读取设计系统 (强制)

// 读取 course.yaml 限定范围：仅需提取 agent.standards 字段
**使用 `grep_search` 或文件查看工具提取 `<课程>/course.yaml`** 中 `agent.standards` 的配置路径。

检查 `agent.standards` 字段：

**正常路径** — `agent.standards` 存在且非 `null`：
读取对应的 `visual_system.yaml`，提取以下高保真 Token：
-   `prompt_mappings` (所有 Layout 变体 AI 规则)
-   `palette` (色板边界: `bg_base`, `primary`, `bg_dark` 等)
-   `composition` (版式要求: `layout_engine`, `grid_behavior`)
-   `interaction` (如 `sound_ui`、`haptics`)

**异常路径** — `agent.standards` 为 `null` 或字段不存在：

> [!CAUTION]
> **⛔ 立即终止工作流。** 不得在无设计系统的情况下生成资产。
> 向用户报告：
> 1.  当前课程（`course.name`）未配置视觉系统（`agent.standards.visual_system` 为空）。
> 2.  建议用户在 `course.yaml` 中注册指向全局主题的指针（如 `../.agent/styles/theme_constructivist_dada.yaml`）。

### Step 2: 提取 Slide 定义

**使用 `grep_search` 工具全文检索** `<课程>/weeks/*_*/src/*.md` 下的 `> \[VISUAL\]` 块。

解析每个 `[VISUAL]` 块，提取：`Slide`、`Layout`、`Scene`、`Text`、`Caption`、`Asset`、`Lang`、`List`、`Resource`

### Step 3: 过滤已有资产

对比 `Asset` 字段与素材目录中的物理文件：
-   如果 `Asset` 字段指向的文件已存在 → **跳过**
-   如果 `Asset` 字段为空或文件不存在 → **列入待生成清单**

### Step 4: 逐个生成

对每个待生成的 Slide，按 `.agent/rules/rule_visual_generation.md` 新版单轨路径构建 Prompt：

```
[Scene 描述（将 [VISUAL].Scene 翻译为英文叙述）].
[prompt_mappings.Layout 提示模板（来自 yaml 的映射规则集）].
[composition 具体描述（如 layout_engine 或 border_radius 要求）].
color palette constraint: [bg_base, primary 等实际色阶强制要求].
[若原要求有明确排版文字，才添加: All visible text must be cleanly rendered in Simplified Chinese. 无排版文字时严禁添加此类字眼]
[尺寸后缀].
```

> [!CAUTION]
> **资产纯净原则**：在构建 Prompt 时，**必须且仅能**提取 `Scene` 中的视觉描述！
> 绝对禁止将 `[VISUAL]` 块中的完整中文字符（如 `包含文本 "..."`、标题、详细图文对照）喂给生图工具。如果强行渲染文字，将导致生成的插画里糊满乱码排版的文字，在后续加载入 PPT 时会与原生文字叠印冲突。产生的背景或插画必须是纯净图形资产！
> **治本之策**：默认附加 `without: text, typography, letters, words, characters, numbers`，彻底禁止文字生成幻觉。

如果 `Layout` 不在 `prompt_variants` 列表中支持，需要先映射或降维到相近的 Layout（例如 `Section` / `CTA` 映射为 `Title`，`Full` 映射为 `Image`，`Workshop` 映射为 `Split` 等）然后组装 Prompt。

**否定词处理**: 在 Prompt 末尾追加 `without: [style.negative_prompt], text, typography, letters, words, characters, numbers`。

调用 `generate_image` 生成图片。

### Step 5: 质量检查

质量检查采用**分级策略**：

**Tier A — 逐张检查**（含文字渲染或复杂布局的 Slide）：
1.  使用 `view_file` 查看图片。
2.  确认色调与 `visual_system.yaml` 的 `palette` 一致。
3.  确认画面文字语言符合要求。
4.  确认生成图片的**视觉情绪**与 `[VISUAL]` 块后首段 Speech 的**叙事情绪**一致（如 Scene 表达"压迫感"但图片给人"宁静感"，则判定不合格）。参见 `script_format/SKILL.md` §1.4 意图对齐规则。
5.  如不合格，最多重试 **2 次**。

**Tier B — 批量信任**（纯背景/氛围图，Layout 为 `Title`、`Image`）：
1.  先完成全部 Tier B 图片的生成。
2.  最后统一 `view_file` 抽检 **1-2 张**代表性图片。
3.  如抽检发现系统性色调偏差，则对全批重新生成。

### Step 6: 移动并回写

1.  将生成的图片移动到脚本同级 `assets/slides/` 下（新架构）或 `<课程>/weeks/*/assets/slides/` 下（旧架构）。若脚本有 `ID` 属性，则以 `ID.png` 命名（推荐），若只有 `Slide`，则可按 `w0X_slide_0X.png` 命名并尽量固定。
2.  回写路径至脚本对应的 `[VISUAL]` 块（**必须采用 V3 零冗余渲染写法**）：
    - **单图**: 使用 `> *   **Asset**: ![预览](../<相对路径>)`
    - **多图**: 使用 `> *   **Asset 1**: ...`、`> *   **Asset 2**: ...` 编号序列
    - **辅助参考图**: 使用 `> *   **Resource**: ![预览](../<相对路径>)`
3.  **幂等性要求**：在回写前，必须检查脚本中是否已经存在该 Slide 的 `> *   **Asset**:`（含 `Asset 1/2/3` 变体）。如果已包含正确的图片路径则跳过；如果要替换，则必须覆盖更新原有行，决不允许重复追加行破坏 Markdown 解析！

**使用 `list_dir` 检查** `<课程>/weeks/W0X_Name/public/slides/`（新架构） 或 `<课程>/weeks/*/assets/slides/`（旧架构）中实际落盘的产物。

### Step 7: 汇总报告

输出生成汇总：
-   ✅ 成功生成的 Slide 列表
-   ⏭️ 跳过的 Slide（已有资产）
-   ❌ 失败的 Slide（附原因）

### Step 8: 收尾 (Epilogue)

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）+ E3（链接验证）。
