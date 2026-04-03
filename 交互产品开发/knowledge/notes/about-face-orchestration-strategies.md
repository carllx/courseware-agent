# 交互编排（Orchestration）策略 — About Face Ch11

> **来源**: Cooper, A. *About Face 4*, Chapter 11: Orchestration and Flow
> **用途**: W05 理论来源 — 交互编排 14 条策略核心选讲

## 核心概念

编排 (Orchestration) = "和谐的组织" (harmonious organization)。所有界面元素必须朝着单一目标协同工作。当交互编排得当，界面本身变得几乎不可见——即交互透明性。

## 14 条和谐交互策略

1. **遵循用户心智模型 (Follow users' mental models)** — 用户按直觉理解的方式组织信息。医院系统中，医生按患者姓名索引；财务部按逾期时间排序。
2. **少即是多 (Less is more)** — 减少界面元素数量但不减少能力。Google 搜索首页 / iPod Shuffle 是经典案例。但过度简化也会导致"视觉简洁→认知复杂"。
3. **让用户指挥而非对话 (Let users direct rather than discuss)** — 交互应像使用工具（锤子钉钉），而非与机器对话。用户期望直接反馈，而非被弹框审问。
4. **提供选择而非提问 (Provide choices rather than ask questions)** — 确认弹框是审讯；工具栏/调色板是静默的选择。方向盘 vs 弹框转向的荒谬对比。
5. **工具随手可得 (Keep necessary tools close at hand)** — 工具栏/快捷键让工具触手可及。用户不应离开工位去找铅笔。
6. **提供无模态反馈 (Provide modeless feedback)** — Word 状态栏、iOS 通知中心、战斗机 HUD 都是无模态反馈。不打断心流的信息展示。
7. **为概率设计，兼顾可能 (Design for the probable but anticipate the possible)** — 关闭文档时弹"是否保存"？用户 99.9% 要保存。为小概率事件打断心流是设计失败。
8. **情境化信息 (Contextualize information)** — Tufte 法则："与什么比？" 精确字节数不如饼图直观。
9. **反映对象与应用状态 (Reflect object and application status)** — Baxter 机器人用表情传达状态。应用忙碌时应看起来忙碌。
10. **避免不必要的报告 (Avoid unnecessary reporting)** — "数据库已更新"之类的消息对非技术用户是恐怖信号。正常运行不需要通知。
11. **避免空白状态 (Avoid blank slates)** — 空界面让用户无所适从。
12. **区分命令与配置 (Differentiate between command and configuration)** — 频繁操作 vs 一次性设置应分开。
13. **隐藏弹射座椅 (Hide the ejector seat levers)** — 危险操作不应与日常操作并排。
14. **优化响应但容忍延迟 (Optimize for responsiveness but accommodate latency)** — 即时反馈优先，网络延迟时给进度指示。

## 与状态机拆解的关系

编排策略的实操落地 = 将应用拆解为有限状态集合，每个状态中只展示与当前任务相关的工具和信息，消除无关噪声。这就是"页面状态流式拆解"的理论基础。
