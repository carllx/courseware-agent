---
name: knaflic-storytelling-with-data-graphify
description: Provide comprehensive workflows and heuristics derived from storytelling-with-data. Use when executing domain-specific tasks, evaluating patterns, or needing deep structural checklists.
---

# knaflic-storytelling-with-data Workflows & Guides

This skill provides a structured, progressive disclosure architecture. 
Please route to the specific workflow below based on your current goal.

## Quick Start
如果你是第一次调用此技能，或者不知道该用哪个具体的工作流，请仔细梳理你的目标，然后查阅下面的核心工作流：

## Core Workflows (工作流体系)

- **foreword**
  ➡️ [foreword Guide](references/workflows/foreword.md)

- **chapter 06 Bad graphs are everywhere**
  ➡️ [chapter 06 Bad graphs are everywhere Guide](references/workflows/chapter_06_bad_graphs_are_ever.md)

- **chapter 16 Who, what, and how**
  ➡️ [chapter 16 Who, what, and how Guide](references/workflows/chapter_16_who__what__and_how.md)

- **chapter 28 Graphs**
  ➡️ [chapter 28 Graphs Guide](references/workflows/chapter_28_graphs.md)

- **chapter 3 clutter is your enemy!**
  ➡️ [chapter 3 clutter is your enemy! Guide](references/workflows/chapter_3_clutter_is_your_enem.md)

- **chapter 49 Size**
  ➡️ [chapter 49 Size Guide](references/workflows/chapter_49_size.md)

- **chapter 55 Accessibility part2**
  ➡️ [chapter 55 Accessibility part2 Guide](references/workflows/chapter_55_accessibility_part2.md)

- **chapter 62 Model visual #3 100% stacked bars**
  ➡️ [chapter 62 Model visual #3 100% stacked bars Guide](references/workflows/chapter_62_model_visual__3_100.md)

- **chapter 75 Lesson 2 choose an appropriate display**
  ➡️ [chapter 75 Lesson 2 choose an appropriate display Guide](references/workflows/chapter_75_lesson_2_choose_an_.md)

- **chapter 86 CASE STUDY 5 Alternatives to pies**
  ➡️ [chapter 86 CASE STUDY 5 Alternatives to pies Guide](references/workflows/chapter_86_case_study_5_altern.md)


## 渐进式知识检索 (Progressive Knowledge Retrieval)

> [!WARNING]  
> 原书核心概念已编译为高密度的知识图谱。**切勿使用 `view_file` 或 `read_file` 等工具尝试读取原始的大型文本块**，否则会导致严重的上下文溢出（Context Bloat）与截断。本技能严格遵循渐进式披露（Progressive Disclosure）原则。

当你在工作流中遇到未知的专属术语，或需要深挖某个模式的理论依据时，请强制使用以下知识检索工具：

### 1. 专属 MCP 工具 (首选，无 Shell 权限也能使用)
如果你的环境启用了 MCP (Model Context Protocol)，请直接调用 `graphify_query` 工具（通过 `call_mcp_tool` 指定 `server_name="graphify-mcp"`，或直接调用原生加载的 `mcp_graphify-mcp_graphify_query`）。
* 参数：`query="你要查询的概念或问题"`, `graph_path="<绝对路径>/graphify-out/graph.json"`
* 优势：安全沙盒环境可用，不依赖 `run_command`，结果精准限制在 Token 预算内。

### 2. 本地 Bash 脚本 (如果 MCP 工具不可用且你有 Shell 权限)
当你需要理解 "Why" 并且有 `run_command` 权限时执行：
```bash
bash scripts/query_theory.sh "为什么我们需要采用这种设计模式？"
```

### 3. 用户引导
当你需要用户确认深奥的设计概念时，请建议用户通过 UI 发送命令：`您可以输入 /graphify query "<在此处替换你的概念>" --budget 1500 来探索该术语的图谱关联。`

### ⚠️ 极限受限环境降级方案 (Fallback)
如果 MCP 与 Bash 都被禁用，请直接使用内置的 `grep_search` 或 `view_file` 工具检索 `references/workflows/` 目录下的 Markdown 文件。**绝对禁止对 `graph.json` 直接执行 `view_file` 尝试完整加载整个文件！**
