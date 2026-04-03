# 知识查询与存档协议 (Knowledge Protocol)

> **导语**：此协议原属全局规则。现已降级为 Librarian 技能的执行参考手册，仅在 `/write` 工作流首阶段或调用 `search_knowledge.py` 时激活使用。

---

## 核心原则：三层漏斗，最小上下文

知识检索必须遵循「**按需深挖、最小加载**」原则。严禁将 `index.json` 或整本教材直接加载到上下文。

```
Layer 1  knowledge_hub.yaml   ← 整体加载一次（< 200 行）
            ↓  summary 不够 → 执行 Layer 2
Layer 2  search_knowledge.py  ← 关键词检索，返回 < 20 行 JSON
            ↓  需要原文 → 执行 Layer 3
Layer 3  view_file(StartLine, EndLine)  ← 精确读取段落（+20 行缓冲）
```

---

## 六条铁律

### Rule K-0：一认知目标，一条目（颗粒度原则）

**知识库中每一条目应对应一个独立的「认知目标」（Cognitive Objective），而非一整章教材。**

*   凡支撑超过 **30 分钟讲授深度**的知识主题，必须单独建立 Hub 条目，并在 `knowledge/notes/` 目录建立对应的笔记文件。
*   严禁将「整章教材」的所有知识点压缩为一条 `textbook` 记录。
*   在 `/write` 执行前，若发现本单元的 Hub 标签数 < 本单元核心理论节点数，**必须先拆分，再写作**。

### Rule K-0.1：正反维度双覆盖（Dual-Polarity Rule）

当教材同一节中存在「正面 vs 负面」「理想 vs 反模式」「Do vs Don't」的对照结构时，**必须同时提取两面**，不可只摘录正面。

| 教材结构 | ❌ 只提正面 | ✅ 正反双覆盖 |
|:--|:--|:--|
| UX Goals: Desirable vs Undesirable | 只列 Delightful/Inspiring | 同时列 Frustrating/Creepy/Deceptive |
| Design Principles: Use vs Misuse | 只讲约束保护用户 | 同时讲暗黑模式（约束剥削用户）|
| Models: Success vs Failure | 只讲表现模型对齐 | 同时讲四宗罪（表现模型失败的后果）|

---

### Rule K-1：Hub 单次加载
在 `/write` 开始时**读取 `knowledge_hub.yaml` 一次**，存入工作内存。整个写作过程中不得重复读取。

### Rule K-2：摘要优先，按需深挖
先用 hub 中的 `summary` 判断：
| 场景 | summary 够用？ | 行动 |
|:---|:---|:---|
| 模块字数预算 **< 1500 字** | ✅ 是 | 直接使用摘要，不展开深挖 |
| 模块字数预算 **≥ 1500 字** | ❌ 否（强制） | **必须执行 Layer 2 `search_knowledge.py`** |
| 需要具体数据/引用/案例 | ❌ 否 | 执行 `search_knowledge.py` |

### Rule K-2.1：拓展性知识主动获取（Proactive Enrichment）
当 Hub 条目命中，但以下**任一**条件成立时，**仍需启动 `narrative_archaeologist` 深度搜索**：
1.  该认知目标的讲授时长 ≥ 30 分钟
2.  对应模块无任何人文层标签
3.  `/write` Step 2.8 字数预算 ≥ 3000 字但 Hub 支撑不足
4.  该模块可用独立案例数 < 2 且模块预算 ≥ 2000 字
5.  该目标无任何跨学科桥接素材且模块预算 ≥ 2500 字

**优先搜索中国本土应用案例、起缘轶事、著名跨界案例等。**

### Rule K-2.2：叙事丰满度自动触发
当以下**任一**条件成立时强制执行搜索：
1. 模块预算 ≥ 2000 字，且 Hub 全部为 `textbook`（无调研补充）
2. 模块预算 ≥ 3000 字，且素材表中独立案例 < 2
3. 可用素材估算覆盖率 < 70%

### Rule K-3：精确段落提取
使用 `view_file` **必须指定 `StartLine` 和 `EndLine`**，不可省略。并在 end_line 基础上加 20 行作为缓冲。

### Rule K-4：存档触发
当 `search_web` 结果被采用于写作，或 `tracking.md` 条目验证成功时，**必须调用 `archive_web.py` 存盘**。

### Rule K-5：缺口追加 tracking
在 hub 中确认无命中时，必须将缺口追加至 `<课程>/knowledge/tracking.md`。

### Rule K-6：Layer 2 降级策略
当检索脚本故障时，**不准用 summary 硬写**，而是：
1. 用 Hub 中 source 定位原文件
2. `view_file_outline` 扫大纲行号
3. 用 `view_file(Start/End)` 提取具体段落

---

## Hub 维护规范与性能边界

| 字段 | 最大长度 |
|:---|:---|
| `summary` | ≤ 150 字 |
| `tags` | 不超过 5 个标签 |
| 整个 `knowledge_hub.yaml` | 严格上限 200 行 |

**瘦身与序列化 (Hub Compression)：**
当逼近 200 行时，执行以下动作：
1. 全局删除所有 `query_hint`。
2. 移除所有冗余的 `type: tracking`。
3. 对大量结构相同的基础切片使用 **YAML Array-Flow 或 JSON 行内联**，大幅缩减行数。
4. 若还超标，下架低频 textbook 条目进入 notes 归档。
