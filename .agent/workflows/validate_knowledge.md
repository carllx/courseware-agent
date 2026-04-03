---
description: 审查课程 knowledge/ 目录的完整性、性能约束及 hub 条目一致性
---

# /validate_knowledge 工作流

> **输入**: 课程名（必填）；可选 `--strict` 开启严格行数模式
> **输出**: 终端打印健康检查报告（✅ / ❌）
>
> **集成说明**: 本工作流已被 `/write` Step 0 和 `/audit` Quick Step 2 (`validate_project.py`) 自动调用。独立运行仅用于手动排查知识库问题。

## 覆盖检查项

| 检查 | 内容 | 性质 |
|:---|:---|:---|
| **C1** | `knowledge_hub.yaml` 存在且 YAML 格式合法 | 结构完整性 |
| **C2** | hub 行数 < 200（建议 < 150） | **性能约束** |
| **C3** | 所有 `textbook`/`note` 条目的 `source` 文件实际存在 | 数据一致性 |
| **C4** | `notes/` 目录下无孤立文件（每个 note 需有 hub 条目） | 数据一致性 |

## 执行步骤

### Step 1: 运行健康检查

```bash
# 从 Workspace 根目录运行：
# 标准模式（行数超出建议值只告警）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_knowledge.py \
  --course "<课程名>"

# 严格模式（行数超出 200 行即视为失败）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_knowledge.py \
  --course "<课程名>" --strict
```

### Step 2: 解读报告

```
✅ C1 hub 存在性与格式: hub 存在，共 16 个条目
✅ C2 hub 行数约束: 行数 125（良好）
❌ C3 source 文件完整性: 
   [ch05-marks-channels] source 不存在：knowledge/textbook/...
✅ C4 notes 孤立文件: 无孤立 notes 文件
```

### Step 3: 修复指引

| 错误类型 | 修复方法 |
|:---|:---|
| C1 hub 不存在 | 参考已有课程 `knowledge_hub.yaml` 创建 |
| C2 行数超出 | 精简 `summary`；批量删除所有 `query_hint` 字段；或使用 YAML 的 Array-Flow/JSON 行内格式将大批量同类新条目压缩序列化至单行。 |
| C3 source 路径失效 | 核对 `textbook/` 目录内实际文件名后修正 hub 中 source 字段 |
| C4 孤立 notes | 在 `knowledge_hub.yaml` 中补充对应 `note` 类型条目 |

### Step 4: 整合到全量验证（可选）

如需与脚本验证一并运行，使用全量入口：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_project.py \
  --course "<课程名>"
```

> **注**：`validate_project.py` 已注册 `validate_knowledge.py`，会自动执行上述检查。
