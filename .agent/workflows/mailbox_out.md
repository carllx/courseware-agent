---
description: 向其他 Agent 发送任务单或 RFC——通用版本，支持项目内和跨项目通信。
---

# 邮箱发件 (Mailbox Out)

> 向其他 Agent 发送任务委托（MSG）或协商讨论（RFC）。
> **配套工作流**：`/mailbox_in` — 接收并处理共享邮箱中的消息。

---

## 前置：身份声明

执行本工作流前，当前对话必须已声明 Agent 身份。若用户未声明，先询问。
声明后，以下步骤中 `{MY_IDENTITY}` 代指该身份。

## 变量

| 变量 | 来源 | 说明 |
|:-----|:-----|:-----|
| `{MY_IDENTITY}` | 对话开始时用户声明 | 当前 Agent 身份 |
| `{TARGET}` | 发件时指定 | 目标 Agent 身份 |
| `{MAILBOX_PATH}` | `mailbox.yaml` 的 `mailbox_path` 字段 | 邮箱根目录路径 |

> **默认路径提示**：课程工作区项目的共享邮箱位于 `/Users/yamlam/Downloads/cross_agent_mailbox/`。若首次使用找不到 `mailbox.yaml`，先搜索此路径。

---

## 步骤 0：同步 INDEX（前置，每次必做）

在发件前先刷新共享邮箱状态，避免重复发送已有 MSG：

1. 读取 `{MAILBOX_PATH}/mailbox.yaml` 获取邮箱路径
2. 读取 `{MAILBOX_PATH}/INDEX.md`
3. 扫描 `active/` 目录中所有 `.md` 文件的 frontmatter
4. 比对差异并写回 INDEX.md（规则同 `/mailbox_in` 步骤 0）
5. **去重检查**：检查当前请求的主题是否与 `active/` 中已有 MSG 重叠。若重叠，向用户确认是追加到现有 MSG 还是新建。

---

## 步骤 1：路由判定（可选）

> 此步骤仅在本项目存在 `.agent/workflows/routing_rules.md` 时执行。
> 若不存在该文件，直接跳到步骤 2。

读取 `routing_rules.md`，按其中的归属判定表分类修改请求：
- 归属本端的 → 直接执行，不发邮件
- 归属对端或双端协同的 → 继续步骤 2

---

## 步骤 2：编写 MSG/RFC 并投递

### 2.1 获取下一个 MSG/RFC ID

读取 `{MAILBOX_PATH}/mailbox.yaml` 的 `next_msg_id` / `next_rfc_id`。

### 2.2 创建邮箱消息

路径：`{MAILBOX_PATH}/active/{YYYY-MM-DD}_{MY_ABBR}_{ID}_{主题关键词}.md`

- `{MY_ABBR}` 为发送方自选缩写

#### MSG 模板（任务委托）

```yaml
---
id: MSG-{ID}
from: {MY_IDENTITY}
to: {TARGET}
created: {YYYY-MM-DD}
priority: {P0/P1/P2}
status: pending
read_by: []
depends_on: []
---
```

```markdown
# 任务单：{标题}

> **发件方**：{MY_IDENTITY}
> **收件方**：{TARGET}
> **创建时间**：{YYYY-MM-DD}
> **优先级**：{P0/P1/P2}
> **背景**：{简述为什么需要对方执行}

## 当前状态
{描述当前进展、已有数据或已尝试的方案}

## 请执行的任务
### 任务 N：{标题} {⭐ 如果关键}
{详细说明，含期望的 Before/After}

## 验证方法
{如何确认任务完成}

## 上下文引用（收件方必读）
- **相关课程**：{课程名称}
- **目标文件**：{需要修改/创建的文件路径}
- **已有知识**：{knowledge_hub.yaml 中相关条目 ID，或"无"}
- **结果存放**：{调研/产出结果应存放的路径和格式}
- **关键 ADR**：{与本任务相关的 ADR 编号，或"无"}
```

#### RFC 模板（协商讨论）

```yaml
---
id: RFC-{ID}
from: {MY_IDENTITY}
to: {TARGET}
created: {YYYY-MM-DD}
priority: {P0/P1/P2}
status: pending
read_by: []
depends_on: []
---
```

```markdown
# RFC：{议题标题}

## 问题描述
{当前面临的问题}

## 方案列表
| 方案 | 优点 | 缺点 | 本端倾向 |
|:-----|:-----|:-----|:---------|

## 请对方评估
{希望对方回复的具体问题}
```

### 2.3 更新 INDEX.md

在活跃消息表中新增对应行。

### 2.4 递增 ID 计数器

更新 `{MAILBOX_PATH}/mailbox.yaml` 中 `next_msg_id` 或 `next_rfc_id` 的值。

---

## 步骤 3：通知用户

- 📨 **MSG/RFC 已投递**：文件路径和摘要
- 📋 **路由判定结果**（若执行了步骤 1）：哪些项本端执行、哪些已委托
- ❓ **待确认**：需用户裁决的问题

---

## 注意事项

- **身份隔离**：发件人 `from` 始终使用 `{MY_IDENTITY}`
- **INDEX 必同步**：投递后立即更新 INDEX.md 和 mailbox.yaml
- **项目路由规则**：若存在 `routing_rules.md`，跨项目任务必须遵循其中定义的归属约束和修改禁令
