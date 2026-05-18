---
description: 为指定课程的教学周从教材中精读提取知识 Brief 文章（含 Figure 映射与检查清单）
---

# /extract_textbook 工作流

> **输入**: 课程名 + 教学周（如 `信息可视化 W03`）
> **输出**: `<课程>/weeks/<教学周>/briefs/` 目录（B0N 文章 + _manifest.yaml + Hub 更新）
> **技能依赖**: `textbook-briefing`（格式规范）、`librarian`（Hub 查询）

## 前置条件

- `course.yaml` 中目标周次的 `calendar.lessons` 已配置教材章节引用
- `knowledge/textbook/` 下存在至少一本已转换的教材（含 `chapter_*.md` + `images/`）
- 目标周的逐字稿**不要求**已完成（Brief 可先于逐字稿独立生产）

---

## 步骤

### Step 1: 定位教材章节

```bash
# 提取目标周的教学信息
/opt/anaconda3/envs/mybase/bin/python \
  <课程>/extract_week.py --week N
```

从输出中获取本周对应的教材章节列表。如果 `course.yaml` 未配置 `textbook_chapters`，则：
1. 读取本周的 `objectives` 和 `steps` 配置
2. 对照 `knowledge_hub.yaml` 中的 `type: textbook` 条目，定位覆盖这些目标的教材章节

**产物**：教材章节清单（书名 + 章节编号 + 文件路径）

### Step 2: 规划 Brief 拆分

基于教材章节清单，决定如何拆分为 Brief 文章：

| 拆分策略 | 条件 | 说明 |
|:---|:---|:---|
| 一章一篇 | 章节 ≤ 8000 字 | 默认策略 |
| 一章多篇 | 章节 > 8000 字 | 按 `§N.M` 子节边界拆分 |
| 多章合一 | 多个短章节服务同一模块 | 合并为一篇，标注多章节 |
| 非教材来源 | 补充论文/标准 | 标注 `textbook_mapping` 字段 |

**产物**：Brief 拆分方案表

```markdown
| Brief ID | 标题 | 来源章节 | 映射模块 |
|:---|:---|:---|:---|
| B01 | xxx | Munzner Ch2 §2.1-2.4 | M01, M02 |
| B02 | xxx | Munzner Ch2 §2.5-2.7 | M02 |
```

> 需用户确认拆分方案后继续。

### Step 3: 逐章精读与提取

对每个 Brief，按以下流程提取：

1. **加载教材章节**：`view_file(chapter_*.md, StartLine, EndLine)`，每次 ≤ 200 行
2. **按 `textbook-briefing` §2 模板**逐节提取知识点
3. **标注教材经典锚点**：特别适合教学的例子、思想实验、反直觉结论
4. **双语术语标注**：首次出现的专业术语标注英文原文

// turbo
### Step 4: Figure 映射

对每个 Brief 覆盖的教材章节：

1. 执行 `grep_search("![](images/", chapter_*.md)` 提取所有图片引用
2. 阅读每张图的上下文图注，确定 Figure 编号
3. 建立 Figure 编号 ↔ Hash 文件名映射表
4. 评估每张图的教学价值（是否值得迁移到 `public/textbook/`）

**产物**：写入 Brief 的「关键图表索引」表

### Step 5: 教材图迁移（可选）

对图表索引中标记为「值得迁移」的 Figure：

1. 创建 `<教学周>/public/textbook/` 目录（如不存在）
2. 复制教材原图并语义重命名：`FigN.M_描述.jpg`
3. 用 `view_file` 验证图片内容与预期一致
4. 更新 Brief 中的迁移状态为 `✅ 已迁移`

> **遵循** `rule_textbook_sourcing.md` 和 `rule_asset_placement_guard.md`。

### Step 6: 编写检查清单

为每篇 Brief 编写 ≥ 3 个 `CHK-B0N-NN` 检查项：

- 每项对应一个**独立的教学知识点**（非笼统的「是否讲清楚了」）
- 必须包含 ≥ 2 个可 grep 的关键词（中英文均可）
- 标注预期出现的逐字稿模块

### Step 7: 生成 _manifest.yaml

按 `textbook-briefing` §3 规范生成清单文件，包含：
- 教材覆盖率统计
- Brief → Module 映射矩阵
- Figure 迁移进度
- 检查清单汇总

### Step 8: 更新 knowledge_hub.yaml

为每篇 Brief 在 Hub 中追加/更新条目：

```yaml
- id: wNN-bNN-描述
  type: brief
  parent_chapter: <父章节 ID>
  week: WNN
  tags: [...]
  summary: 一句话摘要
  source: weeks/WNN_*/briefs/B0N_*.md
  figures: [FigN.M, ...]
  checklist_count: N
```

### Step 9: 质量自检

对照 `textbook-briefing` §4 质量门限逐项检查：

- [ ] Q1: Frontmatter 完整
- [ ] Q2: 章节覆盖完整
- [ ] Q3: 术语双语标注
- [ ] Q4: Figure 索引完整
- [ ] Q5: 检查清单 ≥ 3 项
- [ ] Q6: 关键词 ≥ 2 个/项
- [ ] Q7: 文件大小 ≤ 15000 字符

### Step 10: 收尾 (Epilogue)

> **引用**: `.agent/workflows/_epilogue.md`。执行 E1（更新 briefing）。

---

## 与 /write 的协作关系

```
/extract_textbook W03        /write W03
     │                           │
     ├─ 生成 briefs/             │
     ├─ 更新 Hub                 │
     └─ ✅ 完成                  │
                                 ├─ Phase 1 Step 2.4:
                                 │  读取 briefs/_manifest.yaml
                                 │  ⚠️ 若无 briefs/ → 警告（软门控）
                                 ├─ Phase 2: 引用 briefs/ 写作
                                 └─ Phase 3: CHK-ID 自动验证
```

## 参数说明

| 参数 | 必填 | 说明 |
|:---|:---|:---|
| 课程名 | ✅ | 如 `信息可视化`、`交互产品开发` |
| 教学周 | ✅ | 如 `W03`、`W01` |
| `--migrate-figures` | 可选 | 同时执行教材图迁移（默认 yes） |
| `--skip-hub` | 可选 | 跳过 Hub 更新（用于批量操作后统一更新） |
