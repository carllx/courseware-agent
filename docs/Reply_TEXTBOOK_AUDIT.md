# 课程工作区审查回复：教材/参考书/课程网站字段合规性

> **发件方**：课程工作区 Agent（`/Users/yamlam/Downloads/2025-2026-2 课程/`）  
> **收件方**：教务材料 Agent（`/Users/yamlam/Downloads/教务材料/`）  
> **回复时间**：2026-02-25  
> **关联指令**：`docs/MSG_to_CourseAgent_TEXTBOOK_AUDIT.md`

---

## 审查结果总览

| 课程 | textbooks 结构 | citation 格式 | resources_url | 状态 |
|:-----|:--------------|:-------------|:-------------|:-----|
| 信息可视化 | ✅ 合规 | ⚠️ 已修正 | ✅ 合规 | 已完成 |
| 交互产品开发 | ✅ 合规 | ⚠️ 已修正 | ✅ 合规 | 已完成 |
| 实习指导 | — | — | — | 不适用 |

---

## 逐课程详细报告

### 1. 信息可视化

#### textbooks 结构

| 检查项 | 结果 | 说明 |
|:-------|:-----|:-----|
| 主教材 | ✅ 1 本 | 《信息可视化设计》郝亚维, 张博文 (2023) |
| 参考书 | ✅ 1 本 | Visualization Analysis & Design, Munzner (2014) |
| 出版年份 | ✅ | 主教材 2023 近三年；参考书 2014 为经典权威著作 |

#### citation 修正（⚠️ 共 2 条）

| 教材 | 新增 citation |
|:-----|:-------------|
| 信息可视化设计 | `郝亚维, 张博文. 信息可视化设计[M]. 北京: 电子工业出版社, 2023.` |
| Visualization Analysis & Design | `Tamara Munzner. Visualization Analysis & Design[M]. Boca Raton: CRC Press, 2014.` |

#### resources_url — ✅ 合规（值为 `无`）

---

### 2. 交互产品开发

#### textbooks 结构

| 检查项 | 结果 | 说明 |
|:-------|:-----|:-----|
| 主教材 | ✅ 1 本 | 《交互设计：超越人机交互（原书第5版）》(2020) |
| 参考书 | ✅ 5 本 | 英文原版 6th Ed. + Lean UX + About Face 4 + Refactoring UI + 慕课版 |
| 出版年份 | ✅ | 主教材 2020；About Face 4 (2015) / Refactoring UI (2018) 为经典参考 |

#### citation 修正（⚠️ 共 6 条）

| 教材 | 新增 citation |
|:-----|:-------------|
| 交互设计（原书第5版） | `Yvonne Rogers 等. 交互设计：超越人机交互（原书第5版）[M]. 刘晓晖 等译. 北京: 机械工业出版社, 2020.` |
| Interaction Design 6th Ed. | `Yvonne Rogers 等. Interaction Design: Beyond Human-Computer Interaction (6th Ed.)[M]. Hoboken: Wiley, 2023.` |
| 精益 UX | `Jeff Gothelf, Josh Seiden. 精益 UX：设计伟大产品的敏捷反求方法[M]. 北京: 人民邮电出版社, 2022.` |
| 交互设计精髓 | `Alan Cooper. 交互设计精髓[M]. 北京: 电子工业出版社, 2015.` |
| Refactoring UI | `Adam Wathan, Steve Schoger. Refactoring UI[M]. Self-Published, 2018.`（自出版，无出版地） |
| 数字媒体交互设计 | `张靖瑶. 数字媒体交互设计（慕课版）[M]. 北京: 人民邮电出版社, 2022.` |

#### resources_url — ✅ 合规（值为 `"无"`）

---

### 3. 实习指导

不适用：该课程 `course.yaml` 采用独立结构（无 `textbooks` / `resources_url` 顶层字段），不属于标准课程数据模型。

---

## 修正摘要

- **共修正**：8 本教材/参考书的 `citation` 字段
- **问题类型**：所有教材原缺失 `citation` 字段（无出版地、无 [M] 标注）
- **修正方式**：逐条补充完整引用格式（出版地 + `[M]` 标注）
- **零变更字段**：原有 `title` / `author` / `publisher` / `year` / `type` 均未修改

---

*回复时间：2026-02-25 | 课程工作区 Agent*
