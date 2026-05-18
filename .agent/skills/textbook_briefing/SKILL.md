---
name: textbook-briefing
description: |
  教材精读文章（Brief）的格式规范与生成引擎。定义 Brief 的增强模板结构（YAML Frontmatter、
  Figure-Hash 映射表、带唯一 ID 的检查清单）、质量门限和存放规范。
  当 /extract_textbook 工作流执行教材提取、或 /write Phase 1 Step 2.4 读取 briefs/ 目录、
  或用户提到「教材精读」「提取知识点」「Brief」时触发。
---

# 技能：教材精读引擎 (Textbook Briefing)

## TL;DR

教材精读文章（Brief）= 教材原文的结构化提取产物，存放于 `weeks/WXX/briefs/B0N_*.md`。
每篇含五大结构块：教材位置 → 核心知识提取 → 关键图表索引（含 Hash 路径）→ 易混淆辨析 → 对照检查表（含 CHK-ID）。
产物服务于 `/write` 的知识参照和 `/audit` 的覆盖率验证。

---

## §1 Brief 的定位与职责边界

| 维度 | Brief（教材精读） | Note（网络调研） | Script（逐字稿） |
|:---|:---|:---|:---|
| **内容来源** | 教材原文（忠实提取） | 网络搜索/论文 | 综合叙事（教材+调研+人文） |
| **语言风格** | 学术精准，中英双语术语 | 调研备忘，简明扼要 | 口语化，课堂叙事 |
| **存放位置** | `weeks/WXX/briefs/` | `knowledge/notes/` | `weeks/WXX/src/` |
| **Hub 类型** | `type: brief` | `type: note` | 不入 Hub |
| **下游消费者** | `/write` 写作参照 | `/write` 素材补充 | 教师/H5/PPT |

> **核心原则**：Brief 是教材的「忠实代理人」——它不做叙事加工，不添加隐喻故事，不裁剪为课堂语言。它的价值在于**完整、精确、可溯源**。叙事转化是 `/write` 工作流的职责。

---

## §2 Brief 增强模板

每篇 Brief 必须包含以下结构块：

### 2.1 YAML Frontmatter（机器可读元数据）

```yaml
---
week: W03                    # 周次标识
brief_id: B01                # Brief 编号（B + 两位数字）
title: "数据抽象导论——What 框架"  # 中文标题
textbook: "书名, 作者, 年份"     # 教材全称
chapters: ["2.1", "2.2"]     # 覆盖的章节编号列表
line_range: [1, 225]          # 教材 Markdown 文件中的行范围（可选）
source_path: "knowledge/textbook/...chapter_*.md"  # 教材源文件路径
covers_modules: ["M01", "M02"]  # 映射到哪些逐字稿模块
status: draft                 # draft | done | verified
---
```

**必填字段**：`week`, `brief_id`, `title`, `textbook`, `chapters`, `covers_modules`, `status`
**可选字段**：`line_range`, `source_path`, `textbook_mapping`（当来源非直接教材章节时）

### 2.2 教材位置

```markdown
## 教材位置
- 原著：作者, *书名*, 年份
- 章节：Chapter N — 章节标题
- 范围：N.M - N.K (Lines X - Y)
```

### 2.3 核心知识提取

- 按教材原始章节结构（`###` = 节，`####` = 子节）逐段展开
- 保留教材原文的**英文术语**（括号标注）
- 标注**教材经典锚点**（原文中特别适合教学的例子或思想实验）
- 必要时引用教材 Figure 编号（如「参见 Figure 2.2」）

### 2.4 关键图表索引（含可执行路径）

```markdown
## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig N.M | 图注文本 | `images/<hash>.jpg` (L行号) | ✅/❌ |
```

**规则**：
- **教材原文路径**必须包含实际的 hash 文件名和行号，可截断为 `images/<前8位>...`
- **迁移状态**：`✅ 已迁移` / `❌ 待迁移` / `N/A`（非教材原图）
- 如果教材图已迁移到 `public/textbook/`，追加已迁移路径列

### 2.5 易混淆概念辨析

列出本章节中学生最容易混淆的概念对，格式：

```markdown
- **概念A vs 概念B**：一句话区分 + 教学风险说明。
```

### 2.6 与逐字稿的对照检查表（含唯一 ID）

```markdown
- [ ] `CHK-B01-01`: 检查项描述
  - 关键词: `关键词1`, `关键词2`, `Keyword3`
  - 预期出现模块: M0N
```

**ID 格式**：`CHK-B<brief编号>-<两位序号>`（如 `CHK-B01-03`）
**关键词**：用于未来自动化 `grep_search` 验证逐字稿覆盖情况

---

## §3 _manifest.yaml 规范

每个教学周的 `briefs/` 目录必须包含一个 `_manifest.yaml`：

```yaml
week: W03
course: 课程名
status: complete  # incomplete | complete | verified

textbook_coverage:
  - book: "书名"
    chapters_covered: ["章节范围"]
    coverage_ratio: 0.0-1.0

mapping:
  - brief: B01_文件名
    source_chapters: "章节描述"
    covers_modules: [M01, M02]
    figure_count: N
    figures_migrated: N
    checklist_count: N

summary:
  total_briefs: N
  total_figures: N
  total_figures_migrated: N
  total_checklist_items: N
  modules_covered: [M01, M02, ...]
  modules_uncovered: []
```

---

## §4 质量门限

| # | 检查项 | 标准 |
|:--|:---|:---|
| Q1 | Frontmatter 完整性 | 所有必填字段存在且非空 |
| Q2 | 章节覆盖完整性 | 教材对应章节的每个独立小节（`###` 级）均有对应提取段落 |
| Q3 | 术语双语标注 | 首次出现的专业术语必须标注英文原文 |
| Q4 | Figure 索引完整性 | 教材章节中所有 Figure 均出现在索引表中（含 NO_MATCH 显式标注） |
| Q5 | 检查清单 ≥ 3 项 | 每篇 Brief 的检查清单不少于 3 个 CHK 条目 |
| Q6 | 检查清单关键词 | 每个 CHK 条目必须包含 ≥ 2 个可 grep 的关键词 |
| Q7 | 文件大小 | 单篇 Brief ≤ 15,000 字符（超过则按章节拆分） |

---

## §5 命名规范

| 元素 | 规范 | 示例 |
|:---|:---|:---|
| 目录名 | `briefs/` | `weeks/W03_Data_Literacy/briefs/` |
| Brief 文件名 | `B<两位编号>_<中文描述>.md` | `B01_数据抽象导论_What框架.md` |
| Brief ID | `B<两位编号>` | `B01` |
| 检查项 ID | `CHK-B<编号>-<两位序号>` | `CHK-B01-03` |
| Manifest | `_manifest.yaml`（下划线前缀） | `briefs/_manifest.yaml` |

---

## §6 Hub 集成

Brief 在 `knowledge_hub.yaml` 中的条目格式：

```yaml
- id: w03-b01-data-abstraction-what  # 推荐格式: wNN-bNN-描述
  type: brief                        # 🆕 新类型
  parent_chapter: ch02-data-abstraction  # 父章节条目 ID
  week: W03                          # 周次绑定
  tags: [tag1, tag2]
  summary: 一句话摘要
  source: weeks/W03_Data_Literacy/briefs/B01_xxx.md  # 指向 briefs/ 路径
  figures: [Fig2.2, Fig2.3]          # 覆盖的 Figure 列表
  checklist_count: 4                 # 检查项数量
```

**与 `librarian` 的交互**：`librarian` 的 Layer 1 Hub 扫描自动识别 `type: brief` 条目。当 `/write` Phase 1 检索到 brief 条目时，直接读取对应的 Brief 文件获取完整知识细节，无需再走 Layer 2/3 的教材原文检索路径（Brief 已是教材的预处理产物）。

---

## 工具调用速查

| 需求 | 工具 |
|:---|:---|
| 读取教材章节原文 | `view_file(knowledge/textbook/.../chapter_*.md, StartLine, EndLine)` |
| 提取教材图片引用 | `grep_search("![](images/", chapter_*.md)` |
| 查看教材图片内容 | `view_file(knowledge/textbook/.../images/<hash>.jpg)` |
| 迁移教材图到 public | `run_command(cp ...)` |
| 生成/更新 manifest | 手动编写 YAML |
| 更新 Hub | `multi_replace_file_content(knowledge_hub.yaml)` |
