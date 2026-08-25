---
week: W04
brief_id: B01
title: "商业产出与假设声明"
textbook: "《精益 UX》，Jeff Gothelf, Josh Seiden，2022"
chapters: ["5", "6", "10"]
source_path: "knowledge/textbook/Gothelf_J_Lean_UX_Designing_Great_Products_with_Ag/chapter_13_Chapter_10_Box_6_Hypotheses.md"
covers_modules: ["M01", "M02"]
status: done
---

## 教材位置
- 原著：Jeff Gothelf, Josh Seiden, *《精益 UX》*, 2022
- 章节：Chapter 5, 6, 10
- 范围：全文

## 核心知识提取

### 商业问题与产出 (Chapter 5 & 6)
- **商业问题陈述 (Business Problem Statement)**：不应包含具体解决方案。它提供挑战、锚定客户视角、界定约束，并提供成功衡量标准（KPI或客户期望的行为变化）。
- **领先指标 vs 滞后指标**：
  - 滞后指标 (Lagging Indicators)：高管关注的影响指标 (Impact Metrics) 如利润、市占率。
  - 领先指标 (Leading Indicators)：一线团队需要寻找的具体客户行为变化——“如果方案有效，人们的行为会有什么不同？” 这种变化就是我们要追求的**商业产出 (Business Outcomes)**。所有选项都应以**动词**开头。
- **用户行为度量模型**：
  - 海盗指标 (AARRR)：获取、激活、留存、收入、推荐。
  - 指标山峰 (Metrics Mountain)：描述用户克服阻力攀登至高价值用户的过程（参见 Figure 6-2）。
- **产出到影响的映射**：通过白板将团队战术级工作（产出）连接至战略目标（影响），建立团队全局观（参见 Figure 6-3, 6-4）。

### 假设的定义与模板 (Chapter 10)
- **假设 (Hypothesis)**：基于有限证据做出的设定或拟议的解释，作为进一步调查的起点。在 Lean UX 中，它将商业问题、画像和潜在解决方案融合。
- **假设声明模板**：
  - We believe we will achieve **[this business outcome]**（我们相信会实现**[某个业务成果]**）
  - If **[these personas]**（如果**[这些角色]**）
  - Attain **[this benefit/user outcome]**（获得**[这个利益/用户成果]**）
  - With **[this feature or solution]**（通过**[这个功能或解决方案]**）
- **细化焦点**：假设应该足够具体以便测试。避免使用诸如“更好的用户体验”等模糊词汇。

### 优先级排序 (Prioritizing Hypotheses)
- **假设优先级画布 (Hypothesis Prioritization Canvas)**：一个 2x2 矩阵（参见 Figure 10-4），横轴为风险 (Risk)，纵轴为感知价值 (Perceived Value)。
  - **象限 1 (高风险，高价值)**：**重点测试**的假设。
  - **象限 2 (低风险，高价值)**：直接构建并发布，发布后测量。
  - **象限 3 (低风险，低价值)**：仅构建基础设施，不做创新测试。
  - **象限 4 (高风险，低价值)**：直接抛弃。

## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig 6-1 | Box 2 of the Lean UX Canvas: Business Outcomes | `images/assets/lux3_0601.webp` | ✅ 已迁移 (`/public/textbook/Fig_6-1.webp`) |
| Fig 6-2 | Metrics Mountain | `images/assets/lux3_0602.webp` | ✅ 已迁移 (`/public/textbook/Fig_6-2.webp`) |
| Fig 6-3 | Connecting outcomes to impacts | `images/assets/lux3_0603.webp` | ✅ 已迁移 (`/public/textbook/Fig_6-3.webp`) |
| Fig 6-4 | King's outcome-to-impact map | `images/assets/lux3_0604.webp` | ✅ 已迁移 (`/public/textbook/Fig_6-4.webp`) |
| Fig 10-1 | Box 6 of the Lean UX Canvas: Hypotheses | `images/assets/lux3_1001.webp` | ✅ 已迁移 (`/public/textbook/Fig_10-1.webp`) |
| Fig 10-2 | A hypothesis table | `images/assets/lux3_1002.webp` | ✅ 已迁移 (`/public/textbook/Fig_10-2.webp`) |
| Fig 10-3 | Working on the hypothesis chart | `images/assets/lux3_1003.webp` | ✅ 已迁移 (`/public/textbook/Fig_10-3.webp`) |
| Fig 10-4 | The Hypothesis Prioritization Canvas | `images/assets/lux3_1004.webp` | ✅ 已迁移 (`/public/textbook/Fig_10-4.webp`) |

## 易混淆概念辨析

- **假设 (Hypotheses) vs 敏捷用户故事 (Agile User Stories)**：
  - 敏捷用户故事往往在实操中退化为“能否快速交付功能”。
  - 假设将“行为改变（商业产出）”作为成功定义，交付功能只是测试的开始。

## 与逐字稿的对照检查表

- [ ] `CHK-B01-01`: 必须区分滞后指标（Impact）与领先指标（Outcome），强调寻找用户行为的变化。
  - 关键词: `滞后指标`, `领先指标`, `行为变化`
  - 预期出现模块: M02
- [ ] `CHK-B01-02`: 必须清晰讲解"假设"的四段式模板（业务成果-角色-用户利益-功能）。
  - 关键词: `假设声明`, `业务成果`, `用户成果`
  - 预期出现模块: M02
- [ ] `CHK-B01-03`: 必须介绍并应用假设优先级矩阵（风险×价值）。
  - 关键词: `优先级`, `高风险`, `高价值`
  - 预期出现模块: M03
