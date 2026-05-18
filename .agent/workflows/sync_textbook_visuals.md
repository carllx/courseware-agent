---
description: 从教材知识库中提取视觉素材并插入课程脚本的标准化流程
---

# /sync_textbook_visuals 工作流

> **输入**: 目标教学周路径（如 `信息可视化/weeks/W02_Design_Principles`）
> **输出**: 教材图迁移至 `public/textbook/` + 脚本 `[VISUAL]` 块更新 + 覆盖率 Manifest

> **关联规则**: `rule_textbook_sourcing.md`（行为约束）、`rule_asset_management.md` §3.4（目录规范）

## 前置条件

- 目标教学周的 `src/*.md` 脚本已完成写作（`STATUS: done`）
- `knowledge/textbook/` 下存在至少一本已转换的教材（含 `_full.md` + `images/`）

## 步骤

### Step 0: Brief 快速通道（可选）

检查目标教学周是否存在 `briefs/` 目录：

- **若存在 `briefs/_manifest.yaml`**：
  1. 读取所有 Brief 文件的「关键图表索引」表
  2. 汇总所有 Figure 的「迁移状态」列：
     - `✅ 已迁移` → 跳过，直接进入 Step 5 验证
     - `❌ 待迁移` → 提取其 `教材原文路径` 列中的 Hash 文件名，直接进入 **Step 4 资产迁移**
  3. **跳过 Step 1-3**（Brief 已完成关键词提取、章节定位和逐图审阅）
  4. 进入 Step 4 时，使用 Brief 图表索引中的 `Figure 编号` 和 `教材原文路径` 作为输入

- **若不存在**：输出 `[INFO] 未检测到 briefs/，使用常规流程`，继续执行 Step 1-3。

> [!TIP]
> Brief 快速通道省去了“逐篇读脚本 → 提取关键词 → 定位章节 → 逐图匹配”的大量工作。如果已执行 `/extract_textbook`，强烈建议使用此通道。

### Step 1: 脚本阅读与关键词提取

逐篇阅读目标教学周 `src/` 下的全部脚本文件。对每个 `[VISUAL]` 块，记录：
- Slide ID
- Scene 描述摘要
- 脚本正文中引用的**理论概念关键词**（如 "Stevens Power Law"、"No Unjustified 3D"）

**产物**: 关键词清单（内部工作记忆，无需落盘）

> [!CAUTION]
> 禁止使用 grep 脚本替代人工阅读。必须理解每个 VISUAL 块的教学意图。

### Step 2: 教材章节定位

1. 打开教材的目录索引文件（`index.md` 或 `_full.md` 的标题结构）
2. 将 Step 1 的关键词与章节标题交叉比对
3. 列出**所有**可能包含相关插图的章节文件路径

// turbo
### Step 3: 逐图审阅

对 Step 2 定位到的每个章节：
1. 使用 `grep_search` 提取该章节中全部 `![](images/...)` 引用
2. 阅读每张图的上下文图注（Figure caption），评估与脚本 `[VISUAL]` 块的匹配度
3. 对每个 `[VISUAL]` 块做出显式处置决定：

| 状态码 | 含义 | 后续动作 |
|:---|:---|:---|
| `MATCHED` | 教材有直接对应图 | → Step 4 迁移 |
| `PARTIAL` | 有相关但非精确匹配 | 记录候选，征询用户 |
| `NO_MATCH` | 教材无对应图 | 标注已搜索章节，留待 `/generate_assets` |

### Step 4: 资产迁移

对每个 `MATCHED` 项（来自 Step 3 的审阅结果，或 Step 0 中 Brief 的「❌ 待迁移」条目）：

1. 创建目标目录 `<教学周>/public/textbook/`（如不存在）
2. 将教材原图从 `knowledge/textbook/<书名>/images/<hash>.jpg` 复制到目标目录
3. 语义重命名：`Fig<章>.<节>_<描述>.jpg`（如 `Fig6.4_3D_vs_2D_Bar_Charts.jpg`）

> **Brief 回写**：如果迁移源来自 Brief 的图表索引，迁移完成后必须回写更新 Brief 文件中对应行的迁移状态为 `✅ 已迁移`，并填写已迁移路径列。同时更新 `_manifest.yaml` 中的 `figures_migrated` 计数。

// turbo
### Step 5: 资产验证

对每张迁移的图片，必须使用 `view_file` 查看图片内容：
- 确认视觉内容与预期的 `[VISUAL].Scene` 描述大致一致
- 确认文件非损坏（非 0 字节）
- 确认存放于 `public/textbook/` 而非 `public/slides/`

### Step 6: 脚本引用更新

对每个已验证的 `MATCHED` 项，更新脚本中的 `[VISUAL]` 块：
- 如已有 AI 生成的 `Asset` → 保留原 Asset，新增 `Resource` 字段指向教材图
- 如无 Asset → 直接设置 `Asset` 为教材图路径
- 补充 `Source: Textbook` 字段

引用路径格式：`![Munzner Fig<N>](../public/textbook/<文件名>.jpg)`

### Step 7: 覆盖率清单输出

输出完整 Manifest 表，覆盖目标教学周的**全部** `[VISUAL]` 块：

```markdown
| Slide ID | 处置状态 | 教材源 | 图注 | 备注 |
|:---|:---|:---|:---|:---|
| S07d_xxx | MATCHED | Munzner Fig 6.4 | "3D bar charts..." | 已迁移 |
| S07b_xxx | NO_MATCH | — | — | 需 AI 生成 |
```

Manifest 中不允许存在未标注状态的行。

### Step 8: 收尾 (Epilogue)

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）+ E3（链接验证）。
