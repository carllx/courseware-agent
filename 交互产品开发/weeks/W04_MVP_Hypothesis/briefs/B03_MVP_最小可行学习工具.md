---
week: W04
brief_id: B03
title: "MVP：最小可行性学习工具"
textbook: "《精益 UX》，Jeff Gothelf, Josh Seiden，2022"
chapters: ["12"]
source_path: "knowledge/textbook/Gothelf_J_Lean_UX_Designing_Great_Products_with_Ag/chapter_15_Chapter_12_Box_8_MVPs_and_Experiments.md"
covers_modules: ["M04", "M05"]
status: done
---

## 教材位置
- 原著：Jeff Gothelf, Josh Seiden, *《精益 UX》*, 2022
- 章节：Chapter 12 — Box 8: MVPs and Experiments
- 范围：全文

## 核心知识提取

### MVP 的重新定义
- **核心提问**："我们需要做的**最少的工作量**是什么，以便学到下一个最重要的事情？（What’s the least amount of work we need to do to learn the next most important thing?）"
- **MVP (Minimum Viable Product) 定义澄清**：
  - 常见的错误认知："能发布出门的最快版本"、"充满妥协的丑陋版本"、"功能最少的可用版本"。
  - **精益 UX 中的定义**：一种**用于快速学习的小型方法**。它的首要目的不是创造价值，而是**创造学习（Create Learning）**。

### 测试价值的 MVP 指南
当你要验证解决方案是否具有商业/用户价值时：
- **直击核心**：剥离无关要素（如登录、密码找回），直接向用户呈现核心价值主张。
- **清晰的行动号召 (Call to Action)**：通过订阅、注册等方式，测量用户的真实使用或付费意愿。
- **测量行为 (Measure behavior)**：在数字产品设计中，**用户的实际行为胜过口头意见 (behavior trumps opinion)**。
- **对话探究**：在观察行为数据后，必须与用户交谈，了解他们为什么这样做。
- **不重复造轮子**：利用现成工具（邮件、微信群、表单、无代码工具）去验证，而不是上来就写代码。

### MVP 类型及案例
1. **着陆页测试 (Landing Page Test)**：
   - 用来测试市场需求。构建一个具有价值主张和 Call to Action 的网页。
   - 典型代表：Kickstarter 众筹平台上的每一个项目，实际上都是一个测试构想是否有足够多买单者的 MVP。
2. **伪功能 / 通向无处的按钮 (Feature Fake / Button to Nowhere)**：
   - 针对开发成本极高的功能，先在界面上放置入口按钮（例如 Flickr 的 "设为屏保" 按钮）。
   - 用户点击后，弹出"功能即将上线，敬请期待"的提示。通过统计点击率来验证真实需求。
3. **绿野仙踪 / 幕后人工操作 (Wizard of Oz)**：
   - 前端看起来像一个完整的自动化系统，但在幕后，所有数据和通信都由人工手动处理。
   - 案例：Amazon Echo 早期测试时，测试者向"设备"提问，幕后的人类员工通过键盘在谷歌搜索并传回答案。
4. **原型测试 (Prototyping)**：
   - 从低保真的纸面原型 (Paper Prototypes) 到交互线框图，再到高保真可交互原型以及无代码 (No-Code) MVP。

### 真相曲线 (The Truth Curve)
- **核心原则**：你为 MVP 投入的努力程度，应该与你已经掌握的证据量**成正比**。
- 如果毫无证据，只能做低成本 MVP（如画个线框）；当累积了足够多的证据，才值得投入昂贵的开发资源。

## 关键图表索引

| Figure | 教材图注 | 教材原文路径 | 迁移状态 |
|:---|:---|:---|:---|
| Fig 12-1 | Box 8 of the Lean UX Canvas: MVPs and Experiments | `images/assets/lux3_1201.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-1.webp`) |
| Fig 12-2 | Our adapted version of the Truth Curve | `images/assets/lux3_1202.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-2.webp`) |
| Fig 12-3 | An example of a Kickstarter page | `images/assets/lux3_1203.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-3.webp`) |
| Fig 12-4 | Feature fake found in Flickr’s Apple TV app | `images/assets/lux3_1204.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-4.webp`) |
| Fig 12-5 | Screen after clicking the feature-fake button | `images/assets/lux3_1205.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-5.webp`) |
| Fig 12-6 | Feature fake on MapMyRun | `images/assets/lux3_1206.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-6.webp`) |
| Fig 12-7 | Wizard of Oz site for Taproot Foundation | `images/assets/lux3_1207.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-7.webp`) |
| Fig 12-8 | Trello board behind Wizard of Oz | `images/assets/lux3_1208.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-8.webp`) |
| Fig 12-9 | Polished solution for Taproot Foundation | `images/assets/lux3_1209.webp` | ✅ 已迁移 (`/public/textbook/Fig_12-9.webp`) |

## 易混淆概念辨析

- **传统意义的 V1 版本 vs 学习型 MVP**：
  - 传统观念认为 MVP 就是"第一期(Phase 1)"产品，必须是用代码写出来的可以用的系统。
  - 精益 UX 中的 MVP 可能只是一张纸、一封邮件或一个不可用的按钮（Feature Fake），核心是**"以最小代价获取最大认知"**。

## 与逐字稿的对照检查表

- [ ] `CHK-B03-01`: 必须澄清 MVP 的核心定义是为了"学习"而不是为了尽早发布残缺的软件。
  - 关键词: `MVP`, `学习`, `最小可行性产品`
  - 预期出现模块: M04
- [ ] `CHK-B03-02`: 需要介绍至少两种快速验证的 MVP 手法（例如 Feature Fake 或 Wizard of Oz），并用生动案例说明。
  - 关键词: `伪功能`, `绿野仙踪`, `Feature Fake`
  - 预期出现模块: M04
- [ ] `CHK-B03-03`: 需要引用或讲解"真相曲线"的概念，强调投入的资源应与手头掌握的证据成正比。
  - 关键词: `真相曲线`, `Truth Curve`, `证据`
  - 预期出现模块: M04
