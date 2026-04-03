---
description: 扫描共享邮箱中发给当前 Agent 的待处理消息，按优先级展示并引导处理。
---

# 邮箱收件 (Mailbox In)

> 扫描共享邮箱中发往当前 Agent 的活跃消息，展示待办清单。
> **配套工作流**：`/mailbox_out` — 向其他 Agent 发送任务单或 RFC。

## 前置：身份声明

执行本工作流前，当前对话必须已声明 Agent 身份。若用户未声明，先询问：

```
请先声明你的 Agent 身份，例如：
  "我是 课程工作区"          ← 项目级身份，接收所有发给该项目的消息
  "我是 W03写作"            ← 任务级身份，仅接收精确匹配的消息
  "我是 课程工作区.调研助手"  ← 混合写法也可以

你的身份将决定 /mailbox_in 过滤哪些消息给你。
```

声明后，以下步骤中 `{MY_IDENTITY}` 代指该身份。

---

## 变量

| 变量 | 来源 | 说明 |
|:-----|:-----|:-----|
| `{MY_IDENTITY}` | 对话开始时用户声明 | 当前 Agent 身份 |
| `{MAILBOX_PATH}` | `mailbox.yaml` 的 `mailbox_path` 字段 | 邮箱根目录路径 |

---

## 步骤

### 0. 同步 INDEX（前置，每次必做）

在扫描消息前，先从目录实际内容重建 INDEX 的本端视图，确保状态最新：

1. 读取 `{MAILBOX_PATH}/mailbox.yaml` 获取邮箱路径
2. 读取 `{MAILBOX_PATH}/INDEX.md`
3. 扫描 `active/`、`rfc/` 和 `resolved/` 目录下所有 `.md` 文件的 frontmatter
4. **比对差异**：
   - 目录中有但 INDEX 未记录的文件 → 新消息，追加到 INDEX
   - INDEX 中记录为 active 但文件已移至 `resolved/` → 更新 INDEX 状态
   - frontmatter 的 `status` / `priority` 与 INDEX 不一致 → 以 frontmatter 为准
5. **写回 INDEX.md**

> [!IMPORTANT]
> 此步骤确保即使对方 Agent 已发送新消息或更新了状态，你都能看到最新情况。

### 1. 过滤本端消息

只显示满足以下条件的消息：
- `to` 字段**精确匹配** `{MY_IDENTITY}`
- 且 `status` 不为 `resolved`

### 2. 按优先级排序

按 `priority` (P0 > P1 > P2) 和 `created` (最早优先) 排序。

### 3. 展示待办清单

格式：
```
📬 {MY_IDENTITY} 收件箱 — N 条待处理消息（INDEX 已同步 ✅）

[P0] MSG-001: OBE 合规性二次审查 (来自 教务材料, 2026-02-26)
     状态: pending | 依赖: 无
```

空收件箱输出：`📬 {MY_IDENTITY} 收件箱为空，没有待处理消息。（INDEX 已同步 ✅）`

### 4. 处理消息

1. 将 frontmatter `status` 改为 `in_progress`
2. `read_by` 追加 `{MY_IDENTITY}`
3. **立即更新 INDEX.md** 对应行
4. 读取 `original` 字段指向的原始文件获取完整内容
   - ⚠️ 若原始文件不存在，使用邮箱副本中的摘要执行，并在回复中标注"`original` 引用断链"
5. 按任务要求执行
6. 执行消息中附带的验证命令确认完成

### 5. 完成后归档 + 同步 INDEX（后置，每次必做）

1. 将 frontmatter `status` 改为 `resolved`，添加 `resolved_date`
2. 将文件从 `active/` 移入 `resolved/`
3. **更新 INDEX.md**：活跃表 → 已关闭表

### 6. 过期消息提醒

扫描时若发现 `status: pending` 且 `created` 距今 **> 7 天** 的消息，输出提醒：

```
⚠️ MSG-002 已挂起 8 天（创建于 2026-02-19），建议优先处理或与发送方确认是否仍需执行。
```

---

## 发送消息给其他 Agent

如需向其他 Agent 发送消息（如任务委托、RFC、反馈），使用 `/mailbox_out` 工作流。

也可以在此快捷发送：

1. 读取 `{MAILBOX_PATH}/mailbox.yaml` 获取下一个可用 MSG/RFC ID
2. 在 `active/` 中创建新文件：`{YYYY-MM-DD}_{MY_ABBR}_{ID}_{主题关键词}.md`
   - `{MY_ABBR}` 为发送方自选缩写（如 KC、JW、W03 等）
3. frontmatter 必含：`id`, `from: {MY_IDENTITY}`, `to: {目标Agent}`, `created`, `priority`, `status: pending`
4. **立即更新 INDEX.md**：新增行
5. **递增 `mailbox.yaml` 中的 ID 计数器**

## 注意事项

- **身份隔离**：只处理 `to` 匹配当前 Agent 身份的消息
- **原文不动**：邮箱消息仅在 frontmatter 层面更新状态
- **回复追加**：在消息文件末尾追加 `## 回复` 区块
- **INDEX 必同步**：任何对邮箱文件的增/删/改操作后必须同步更新 INDEX.md
- **项目路由规则**：若本项目存在 `.agent/workflows/routing_rules.md`，跨项目消息的处理还需遵循该文件的约束
