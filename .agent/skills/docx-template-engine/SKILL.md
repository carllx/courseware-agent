---
name: docx-template-engine
description: 基于 Python 的极简 4 步 Word (.docx) 模板数据填充与格式转换工具
---

# docx-template-engine

本技能提供了一个标准化的工作流，用于将结构化数据填充至 Word (.docx) 模板文件中。

## 极简 4 步工作流

1. **解析 (Parsing)**：
   审查给定的 DOCX 模板，识别其中的占位符及需要替换的变量位置。
2. **暂存数据 (Staging Data)**：
   构造需要填充的结构化 JSON 数据，并将其暂存为临时文件（如 `data.json`）。该数据必须严格遵守 `references/data_schema.md` 中的规范。
3. **填充引擎 (Filling Engine)**：
   编写并执行 Python 脚本来完成模板的填充与保存。
   **必须指定执行环境**：`/opt/anaconda3/envs/mybase/bin/python`
4. **可选格式转换 (Optional Format Conversion)**：
   如果最终目标并非 DOCX 格式，可以调用系统现有的转换工具（例如 Pandoc 或 textutil）将填充完成的文档转换为目标格式。

## 强约束规范

- **运行环境强依赖**：所有的 Python 脚本执行必须显式调用 `/opt/anaconda3/envs/mybase/bin/python`，以确保依赖库（如 `python-docx`）正确加载。
- **数据规范**：参考 `references/data_schema.md`。必须保证在数据传输和暂存阶段不存在 `null` 值或未定义的 null 状态。
