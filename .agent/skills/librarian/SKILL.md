---
name: librarian
description: |
  知识枢纽查询引擎。在 /write 工作流中主动检索课程知识库，支持四层查询漏斗：
  (1) 轻量索引扫描 knowledge_hub.yaml  
  (2) 精准关键词检索 search_knowledge.py  
  (3) 精确段落提取 view_file(StartLine, EndLine)
  (4) 教材图片索引查询（扫描教材章节中的 ![](images/) 引用）
  亦负责将网络搜索结果存档为 notes/，保持 hub 持续增长。
  触发词：「查教材」「找定义」「有无资料」「搜一下 X」「教材图」「找图」以及 /write 工作流自动触发。
---

# Librarian — 知识枢纽查询引擎

> **配套规则**：知识检索的饱和度门限和素材覆盖率定义见 `.agent/rules/rule_content_depth.md` §1。

---

## §1 主索引扫描（Layer 1）

**何时触发**：进入 `/write` 的 Step 2.3，或用户明确要求查找知识。

### 操作流程

**Step 1.1 加载 hub（整个写作周期仅一次）**

```python
view_file("<课程>/knowledge/knowledge_hub.yaml")
```

**Step 1.2 按知识点匹配**

扫描所有 entries 的 `tags` 和 `summary` 字段，找出命中条目。

**Step 1.3 决策**

| 条目类型 | `summary` 够用？ | 行动 |
|:---|:---|:---|
| `textbook` / `note` | ✅ 是 | 直接引用 summary 写作 |
| `textbook` / `note` | ❌ 否 | 进入 §2 精准检索 |
| `tracking` (pending) | — | 进入 §3 网络搜索 + §4 存档 |
| 无命中 | — | 追加 tracking，进入 §3 |

---

## §2 精准关键词检索（Layer 2）

**何时触发**：hub summary 不足以满足写作需求时。

### 操作流程

```bash
# 同时搜索 hub 摘要层 + textbook 章节层
python .agent/skills/librarian/scripts/search_knowledge.py \
  --course "<课程名>" "<关键词1>" "<关键词2>"
```

**解读结果**：

```json
[
  {
    "type": "hub",
    "id": "affordance-01",
    "summary": "Norman 对可供性的经典定义...",
    "query_hint": "search_knowledge.py 'affordance'"
  },
  {
    "type": "textbook",
    "book": "Interaction Design...",
    "chapter": "3.2 Conceptual Models",
    "path": "knowledge/textbook/.../chapter_05_Chapter_3.md",
    "lines": [45, 120]
  }
]
```

→ 对 `textbook` 类型结果，取 `path` 和 `lines` 进入 §2.1。

### §2.1 精确段落提取（Layer 3）

```python
# 仅提取有效行范围，加 20 行缓冲
view_file(
    AbsolutePath="<课程>/knowledge/textbook/...",
    StartLine=45,
    EndLine=140   # end_line + 20
)
```

> **禁止** 省略 StartLine/EndLine 读整章。每次读取 ≤ 100 行。

### §2.2 教材图片索引查询（Layer 4）

**何时触发**：查询目标为视觉素材（用户提到「教材图」「找图」「有没有插图」），或 `/write` Phase 1 Step 2.4 教材图覆盖率预检时。

**操作流程**：

1. 扫描 `knowledge/textbook/<书名>/images/` 目录，统计图片总数。
2. 对目标教材的相关章节 `chapter_*.md` 执行 `grep '!\['` 提取所有图片引用及其上下文图注（Figure Caption）。
3. 评估每张图与查询关键词的匹配度。
4. 返回按相关性排序的教材图候选清单：

```markdown
| 教材 | 章节 | 图注 | 图片路径 | 匹配度 |
|:---|:---|:---|:---|:---|
```

> **关联规则**: `rule_textbook_sourcing.md` — 逐图审阅标准
> **关联工作流**: `/sync_textbook_visuals` — 完整迁移流程

---

## §3 网络搜索（仅限 tracking 或 hub 无命中）

激活 `narrative_archaeologist` 3-Pass Protocol 进行搜索。
或直接执行：

```python
search_web("<关键词> site:nngroup.com OR site:interactions.acm.org OR filetype:pdf")
read_url_content("<最佳候选 URL>")
```

**质量门限**（采用前必须满足所有条件）：
- [ ] 可查来源（非 AI 生成）
- [ ] 细节具体（有人名/时间/数据）
- [ ] 能用一句话锚点回归到课程知识点
- [ ] 对中国大学生在文化上友好

---

## §4 笔记存档（内容被采用后必须执行）

### Step 4.1 准备笔记正文

结构：
```markdown
## 核心要点
（2-5 条要点）

## 可用叙事角度
（供 script_format 使用的故事/案例角度）

## 原始引用
> "..."

## 与课程的关联
（说明此知识点与哪个教学单元/知识点对应）
```

### Step 4.2 调用存档脚本

```bash
python .agent/skills/librarian/scripts/archive_web.py \
  --course "<课程名>" \
  --id "<唯一ID，连字符格式>" \
  --title "<标题>" \
  --tags "<tag1,tag2,tag3>" \
  --source-url "<URL>" \
  --summary "<30-60字中文摘要>" \
  --content-file <笔记文件路径>
```

**结果验证**：脚本输出 `"status": "ok"` 且 `knowledge_hub.yaml` 中条目 `type` 变为 `note`。

---

## §5 待办追加

若 hub 和 textbook 均无命中，追加到 `<课程>/knowledge/tracking.md`：

```markdown
| T<序号> | <主题> | "<搜索关键词>" | <URL 或 —> | 🔍 待搜索 |
```

---

## 工具调用速查

| 需求 | 工具 |
|:---|:---|
| 加载全部摘要 | `view_file(...knowledge_hub.yaml)` |
| 关键词检索 | `search_knowledge.py --course X "关键词"` |
| 读教材段落 | `view_file(path, StartLine=N, EndLine=M)` |
| 教材图片检索 | `grep_search("!\[", chapter_*.md)` + `list_dir(images/)` |
| 存档网络内容 | `archive_web.py --course X --id Y ...` |
| 网络搜索 | `search_web(...)` + `read_url_content(...)` |

## Bundled Resources

- `scripts/search_index.py`：旧教材索引搜索（仍可用，已由 search_knowledge.py 统一封装）
- `scripts/search_knowledge.py`：统一知识搜索入口（新）
- `scripts/archive_web.py`：网络内容存档工具（新）
