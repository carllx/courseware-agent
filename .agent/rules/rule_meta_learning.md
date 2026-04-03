---
trigger: always
description: 当执行过程中发现新的架构决策、Bug 修复经验或风格反馈时，主动将知识固化到对应文档（Memory Commit）。
---

# 规则：元学习协议 (Meta-Learning Protocol)

**定义**: 当 Agent 在执行过程中获得"新知识"或做出"新决定"，必须**主动**将其固化到文档中（Memory Commit）。

## 1. 触发条件

| 场景事件 | 行动 | 目标 |
| :--- | :--- | :--- |
| **架构决策** | Record Decision | `.agent/memory/ADR.md`（全局）+ `ADR_summary.md`（同步追加一行摘要） |
| **Bug 修复** | Update Guide | 相关指南文档 |
| **知识发现** | Map Knowledge | `<课程>/knowledge/` 下对应文件 |
| **风格反馈** | Update Style | `<课程>/styles/` |
| **规则漏洞** | Patch Rules | `.agent/rules/*.md` |
| **课程定位** | Check Pedagogy| 建立新项目时强制阅读 `rule_dma_course_design.md` |
| **对话结束** | Update Briefing | `.agent/briefing.md`（更新"当前状态"和"最近活动"） |

## 2. 执行步骤

无需等待用户指令。当意识到**缺乏文档**导致犯错或犹豫时：

1.  **Stop**: 完成当前手头任务。
2.  **Reflect**: "如果下次还要做这个，我希望哪里有一份说明书？"
3.  **Update**: 读取目标文档 → 追加或修改内容。
4.  **Notify**: 告诉用户已记录。

## 3. 禁忌

*   **DON'T**: 只在对话中道歉。文档是唯一的长期记忆。
*   **DON'T**: 创建过于琐碎的规则。只记录原则性、架构性的知识。