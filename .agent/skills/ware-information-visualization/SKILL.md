---
name: ware-information-visualization
description: Provide comprehensive workflows and heuristics derived from ware-information-visualization. Use when executing domain-specific tasks, evaluating patterns, or needing deep structural checklists.
---

# ware-information-visualization Workflows & Guides

This skill provides a structured, progressive disclosure architecture. 
Please route to the specific workflow below based on your current goal.

## Quick Start
如果你是第一次调用此技能，或者不知道该用哪个具体的工作流，请仔细梳理你的目标，然后查阅下面的核心工作流：

## Core Workflows (工作流体系)

- **Cover image**
  ➡️ [Cover image Guide](references/workflows/cover_image.md)

- **Chapter One. Foundations for an Applied Science of Data Visualization**
  ➡️ [Chapter One. Foundations for an Applied Science of Data Visualization Guide](references/workflows/chapter_one__foundations_for_a.md)

- **014 Costs and Benefits of Visualization**
  ➡️ [014 Costs and Benefits of Visualization Guide](references/workflows/014_costs_and_benefits_of_visu.md)

- **020 The Eye part3**
  ➡️ [020 The Eye part3 Guide](references/workflows/020_the_eye_part3.md)

- **027 Monitor Illumination and Monitor Surroun**
  ➡️ [027 Monitor Illumination and Monitor Surroun Guide](references/workflows/027_monitor_illumination_and_m.md)

- **034 Color Appearance part2**
  ➡️ [034 Color Appearance part2 Guide](references/workflows/034_color_appearance_part2.md)

- **Chapter Five. Visual Salience: Finding and Reading Data Glyphs**
  ➡️ [Chapter Five. Visual Salience: Finding and Reading Data Glyphs Guide](references/workflows/chapter_five__visual_salience_.md)

- **047 The Searchlight Metaphor and Cortical Ma part2**
  ➡️ [047 The Searchlight Metaphor and Cortical Ma part2 Guide](references/workflows/047_the_searchlight_metaphor_a.md)

- **053 Perception of Transparency with Uniform**
  ➡️ [053 Perception of Transparency with Uniform Guide](references/workflows/053_perception_of_transparency.md)

- **062 Depth Cue Theory part5**
  ➡️ [062 Depth Cue Theory part5 Guide](references/workflows/062_depth_cue_theory_part5.md)

- **070 Judging the Relative Movements of Self W**
  ➡️ [070 Judging the Relative Movements of Self W Guide](references/workflows/070_judging_the_relative_movem.md)

- **079 3D Glyphs**
  ➡️ [079 3D Glyphs Guide](references/workflows/079_3d_glyphs.md)

- **088 The Nature of Language part3**
  ➡️ [088 The Nature of Language part3 Guide](references/workflows/088_the_nature_of_language_par.md)

- **100 Conclusion**
  ➡️ [100 Conclusion Guide](references/workflows/100_conclusion.md)

- **111 The Process**
  ➡️ [111 The Process Guide](references/workflows/111_the_process.md)

- **123 Dynamic Queries**
  ➡️ [123 Dynamic Queries Guide](references/workflows/123_dynamic_queries.md)


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
