---
week: W04
brief_id: B00
title: "精益人物角色 (Proto-Persona)"
textbook: "《精益 UX》，Jeff Gothelf, Josh Seiden，2022"
chapters: ["7"]
source_path: "knowledge/textbook/Gothelf_J_Lean_UX_Designing_Great_Products_with_Ag/chapter_10_Chapter_7_Box_3_Users.md"
covers_modules: ["M01"]
status: done
---

## 教材位置
- 原著：Jeff Gothelf, Josh Seiden, *《精益 UX》*, 2022
- 章节：Chapter 7 — Box 3: Users
- 范围：全文

## 核心知识提取

### 传统 Persona 的隐患
在传统流程中，Persona 通常是漫长且昂贵的研究阶段的产出。这带来了两个问题：
1. **神圣不可侵犯**：因为投入巨大，团队往往将其视为不可更改的静态文档。
2. **知识断层 (Knowledge gap)**：通常由研究团队或外部团队创建，造成了执行研究的人与实际使用这些画像的研发团队之间的鸿沟。

### 精益转型：原型画像 (Proto-Persona)
精益 UX 改变了创建画像的操作顺序，从一次性活动变为**持续迭代的过程**（先假设，后验证）。
- **Proto-Persona** 代表了团队当前对“谁在使用我们的产品以及为什么”的**最佳猜测 (Best guess)**。
- 团队只需花几个小时草绘原型画像，而非耗费数月进行前置研究。
- 作用 1：**建立团队共识 (Shared understanding)**，确保提到“用户”时所有人脑海中的画面一致。
- 作用 2：**牢记我们不是用户 (Remembering we are not the user)**，强迫团队剥离个人偏好。

### Proto-Persona 模板结构
建议在纸上分成三个区域绘制（参见 Figure 7-3）：
- **左上方**：人物草图、姓名和角色。
- **右上方**：人口统计学与行为信息。**警告：** 避免过分强调人口统计学信息。只记录能预测其特定行为的“能产生影响的差异 (differences that make a difference)”，例如是否拥有某型号手机，而非年龄。
- **下半部**：核心细节区。记录用户的**目标、需求、期望的产出 (desired outcomes)**，以及阻碍他们实现的障碍。用户很少需要“功能”，他们需要的是达成目标。

### 早期验证的三重叩问
画像创建后，应作为招募目标进行早期验证：
1. **这个客户存在吗？(Does the customer exist?)** 如果找不到符合画像的人，需修改画像。
2. **他们有你认为的痛点吗？(Do they have the needs and obstacles you think they do?)**
3. **他们会认为解决方案有价值吗？(Would they value a solution to this problem?)** （注：如天使投资人案例，即使痛点存在，如果低频，他们仍可能拒绝使用新工具而继续沿用 Excel）。

## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig 7-1 | Box 3 of the Lean UX Canvas: Users | `images/assets/lux3_0701.webp` | ✅ 已迁移 (`/public/textbook/Fig_7-1.webp`) |
| Fig 7-2 | Dogs. We are indebted to our learned colleague... | `images/assets/lux3_0702.webp` | ✅ 已迁移 (`/public/textbook/lux3_0702.webp`) |
| Fig 7-3 | A completed proto-persona template | `images/assets/lux3_0703.webp` | ✅ 已迁移 (`/public/textbook/Fig_7-3.webp`) |
| Fig 7-4 | The banana slicer. Who buys these? | `images/assets/lux3_0704.webp` | ✅ 已迁移 (`/public/textbook/Fig_7-4.webp`) |

## 易混淆概念辨析

- **Persona vs Proto-Persona**：
  - 传统 Persona 是研究的“终点（结论）”，重构成本高。
  - Proto-Persona 是研究的“起点（假设）”，随时准备根据新数据被推翻和修正。

## 与逐字稿的对照检查表

- [ ] `CHK-B00-01`: 必须阐明抛弃“重型 Persona”的原因（知识断层、不可侵犯）。
  - 关键词: `重型`, `知识断层`, `验证`
  - 预期出现模块: M01
- [ ] `CHK-B00-02`: 需要讲解 Proto-Persona 的三分区模板，特别是下半部分的目标与障碍。
  - 关键词: `三分区`, `人口统计学`, `目标`
  - 预期出现模块: M01
- [ ] `CHK-B00-03`: 需要通过案例（如天使投资人或香蕉切片机）强调“痛点存在不代表方案有价值”的验证逻辑。
  - 关键词: `早期验证`, `存在`, `价值`
  - 预期出现模块: M01
