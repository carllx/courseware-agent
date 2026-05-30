# JSON Hooks 规格指南

## 概述

Hook 是 Antigravity IDE 的**生命周期拦截器**，允许在 Agent 的工具调用和模型推理前后插入自定义脚本。Hook 定义在 Plugin 目录的 `hooks.json` 中。

---

## hooks.json 格式

```json
{
  "hooks": [
    {
      "event": "before_tool_call",
      "match": { "toolName": "write_to_file" },
      "command": "./scripts/lint_guard.sh",
      "timeout": 30
    }
  ]
}
```

| 字段 | 类型 | 必需 | 说明 |
|:---|:---|:---:|:---|
| `event` | string | ✅ | 生命周期阶段名称（见下表） |
| `match` | object | 否 | 事件过滤条件；缺省时匹配所有同类事件 |
| `command` | string | ✅ | 要执行的脚本路径（相对于 Plugin 目录） |
| `timeout` | number | 否 | 超时秒数，默认 30s；超时后脚本被强制终止 |

---

## 生命周期阶段

| 阶段 | 触发时机 | 典型用途 |
|:---|:---|:---|
| `before_tool_call` | 工具调用**前**拦截 | 参数校验、lint 门禁、路径白名单 |
| `after_tool_call` | 工具调用**后** | 日志记录、产物后处理 |
| `before_model_call` | 模型推理**前** | 注入额外上下文、Prompt 改写 |
| `after_model_call` | 模型推理**后** | 响应过滤、安全审计 |
| `on_loop_stop` | Agent 循环**停止时** | 清理临时文件、发送通知 |

> [!NOTE]
> `before_*` 阶段的脚本若以**非零退出码**退出，将**阻止**后续操作执行。`after_*` 阶段的非零退出码仅记录警告。

---

## match 过滤条件

```json
{
  "match": {
    "toolName": "write_to_file",
    "pathPattern": "**/*.py"
  }
}
```

| 字段 | 说明 |
|:---|:---|
| `toolName` | 精确匹配工具名称 |
| `pathPattern` | Glob 模式匹配文件路径（仅对文件操作工具生效） |

缺省 `match` 时，Hook 对该阶段的**所有**事件触发。

---

## 脚本执行上下文

| 环境变量 | 说明 |
|:---|:---|
| `HOOK_EVENT` | 当前阶段名称 |
| `HOOK_TOOL_NAME` | 被拦截的工具名（仅 tool 阶段） |
| `HOOK_PAYLOAD` | JSON 格式的事件负载（通过 stdin 传入） |
| `HOOK_WORKSPACE` | 工作区根目录绝对路径 |

- **工作目录**：脚本的 cwd 为 Plugin 根目录
- **超时**：默认 30s，可通过 `timeout` 字段覆盖，硬上限 120s
- **输出**：stdout 写入 Agent 日志；stderr 输出为警告

---

## 安全约束

> [!CAUTION]
> Hook 脚本以用户权限运行，**禁止**在 Hook 中执行以下操作：

- ❌ `rm -rf` 等破坏性文件删除
- ❌ `git push --force` 等不可逆的远程操作
- ❌ 访问工作区外的敏感目录（如 `~/.ssh/`）
- ❌ 在 `before_*` Hook 中执行超过 10s 的阻塞操作

---

## 示例：代码质量门

拦截 `write_to_file` 写入 `.py` 文件时，自动运行 lint 检查：

```json
{
  "hooks": [
    {
      "event": "before_tool_call",
      "match": {
        "toolName": "write_to_file",
        "pathPattern": "**/*.py"
      },
      "command": "./scripts/python_lint.sh",
      "timeout": 15
    }
  ]
}
```

`scripts/python_lint.sh`：

```bash
#!/bin/bash
# 从 stdin 读取 payload，提取目标文件路径
TARGET=$(echo "$HOOK_PAYLOAD" | jq -r '.targetFile')
ruff check "$TARGET" --exit-non-zero-on-fix
```

> [!TIP]
> 脚本退出码为 0 → 允许写入；非零 → 阻止写入并向 Agent 返回 lint 错误。

---

## 常见陷阱

| 陷阱 | 说明 |
|:---|:---|
| 脚本无执行权限 | 必须 `chmod +x` 脚本文件 |
| 超时过长导致交互卡顿 | `before_*` 阶段建议 ≤ 15s |
| 依赖未安装的命令行工具 | 脚本应检查依赖是否存在并给出友好提示 |

---

## 质量检查表

| # | 检查项 | 标准 |
|:--|:---|:---|
| H1 | JSON 合法性 | `hooks.json` 可被 `jq .` 解析 |
| H2 | 脚本可执行 | `command` 指向的文件存在且有 `+x` 权限 |
| H3 | 无破坏性操作 | 脚本中不含 `rm -rf`、`--force` 等危险命令 |
