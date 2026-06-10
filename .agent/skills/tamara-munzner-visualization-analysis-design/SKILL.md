---
name: tamara-munzner-visualization-analysis-design
description: Provide comprehensive workflows and heuristics derived from visualization-analysis-design. Use when executing domain-specific tasks, evaluating patterns, or needing deep structural checklists.
---

# visualization-analysis-design Workflows & Guides

This skill provides a structured, progressive disclosure architecture. 
Please route to the specific workflow below based on your current goal.

## Quick Start
如果你是第一次调用此技能，或者不知道该用哪个具体的工作流，请仔细梳理你的目标，然后查阅下面的核心工作流：

## Core Workflows (工作流体系)

- **第 5 章：标记与通道 (Marks and Channels)**
  ➡️ [第 5 章：标记与通道 (Marks and Channels) Guide](references/workflows/__5__________marks_and_channel.md)

- **Contents**
  ➡️ [Contents Guide](references/workflows/contents.md)

- **1.6 Why Show the Data in Detail?**
  ➡️ [1.6 Why Show the Data in Detail? Guide](references/workflows/1_6_why_show_the_data_in_detai.md)

- **Datasets**
  ➡️ [Datasets Guide](references/workflows/datasets.md)

- **Attributes**
  ➡️ [Attributes Guide](references/workflows/attributes.md)

- **Network Data**
  ➡️ [Network Data Guide](references/workflows/network_data.md)

- **Query**
  ➡️ [Query Guide](references/workflows/query.md)

- **5.5 Channel Effectiveness**
  ➡️ [5.5 Channel Effectiveness Guide](references/workflows/5_5_channel_effectiveness.md)

- **$\textcircled{ \div}$ Express Values**
  ➡️ [$\textcircled{ \div}$ Express Values Guide](references/workflows/__textcircled___div___express_.md)

- **7.6 Spatial Axis Orientation**
  ➡️ [7.6 Spatial Axis Orientation Guide](references/workflows/7_6_spatial_axis_orientation.md)

- **Example: Multidimensional Transfer Functions**
  ➡️ [Example: Multidimensional Transfer Functions Guide](references/workflows/example__multidimensional_tran.md)

- **Encode Map**
  ➡️ [Encode Map Guide](references/workflows/encode_map.md)

- **10.3.4 Colorblind-Safe Colormap Design**
  ➡️ [10.3.4 Colorblind-Safe Colormap Design Guide](references/workflows/10_3_4_colorblind_safe_colorma.md)

- **Example: Bird’s-Eye Maps**
  ➡️ [Example: Bird’s-Eye Maps Guide](references/workflows/example__bird_s_eye_maps.md)

- **12.5 Superimpose Layers**
  ➡️ [12.5 Superimpose Layers Guide](references/workflows/12_5_superimpose_layers.md)


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
