---
trigger: always
description: Agent 通信协议（邮箱通信、跨项目只读铁律）。始终激活。
---

# 规则：Agent 通信协议 (Agent Communication Protocol)

> 适用场景：所有 Agent 之间的消息通信——包括跨项目任务委托和项目内多 Agent 协作。

## 核心铁律

1. **严禁直接修改教务材料项目的文件**（`/Users/yamlam/Downloads/教务材料/`）
   - 仅可**读取**教务端文件以获取任务详情或验证结果
   - 需要教务端执行修改时，必须通过共享邮箱发送 MSG

2. **所有 Agent 通信统一走共享邮箱**
   - 邮箱路径由 `mailbox.yaml` 的 `mailbox_path` 字段配置
   - 消息必须包含标准 frontmatter（`id`, `from`, `to`, `created`, `priority`, `status`）
   - 发送新消息前必须读取 `mailbox.yaml` 获取下一个可用 ID

3. **INDEX.md 必须实时同步**
   - 任何对邮箱文件的增/删/改操作后，必须立即更新 `INDEX.md`
   - 以 frontmatter 为准解决冲突

## 推荐实践

- 每次开始新工作会话前，建议执行 `/mailbox_in` 检查待办
- 处理 MSG 应按优先级排序（P0 → P1 → P2）
- 执行完 MSG 任务后，运行消息中附带的验证命令确认成果
- 完成后将消息归档到 `resolved/` 并同步 INDEX

## 与项目路由规则的关系

本规则是**通用协议层**，定义所有 Agent 必须遵守的通信规范。
各项目可在 `.agent/workflows/routing_rules.md` 中定义**项目特有的路由约束**（如跨项目修改禁令）。
