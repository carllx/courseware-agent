---
name: knaflic-storytelling-with-data
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

当你在工作流中遇到未知的专属术语，或需要深挖某个模式的理论依据时，请强制使用以下专属检索脚本：

1. **深度理论推演 (Deep Theory Query)** (首选)：
   当你需要理解 "Why" 或更深层次的理论推演时使用。该脚本会自动将输出 Token 限制在安全阈值 (1500 tokens) 内，避免上下文爆炸：
   ```bash
   bash scripts/query_theory.sh "为什么我们需要采用这种设计模式？"
   ```

2. **单一概念解析 (Concept Explanation)**：
   仅当需要快速知晓某个具体术语或名词的定义时使用：
   ```bash
   bash scripts/lookup_concept.sh "SwinTransformer"
   ```

3. **用户引导**：当你需要用户确认深奥的设计概念时，请建议用户通过 UI 发送命令：`您可以输入 /graphify query "<在此处替换你的概念>" --budget 1500 来探索该术语的图谱关联。`
