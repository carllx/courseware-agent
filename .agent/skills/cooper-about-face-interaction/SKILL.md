---
name: cooper-about-face-interaction
description: 交互设计与用户体验（UX/UI）专家，基于 Cooper 的《About Face》目标导向设计。Use when 用户需要设计软件界面、创建用户画像 (Personas)、进行用户研究、定义交互需求，或评估具体的 UI 模式（如移动端姿态、导航栏、手势等）。
---

# about-face-interaction Workflows & Guides

This skill provides a structured, progressive disclosure architecture for executing tasks. Please route to the specific workflow below based on your current goal.

## Quick Start

当用户要求“设计一个新功能”或“评估当前界面”但未指定具体步骤时，请遵循以下标准目标导向设计 (GDD) 路线：
1. **明确目标**：优先查阅 [User Goals](references/workflows/user_goals.md) 与 [Nonuser Goals](references/workflows/nonuser_goals.md)。
2. **确立角色**：参考 [Persona Hypothesis](references/workflows/persona_hypothesis.md)。
3. **消除摩擦**：在设计任何界面时，强制应用 [Eliminating Excise](references/workflows/eliminating_excise.md) 原则。
4. **概念检索**：若遇到本技能中的专有术语，请立即使用下方提供的 **Concept Retrieval** 检索引擎，严禁盲目读取原始文件。

## Core Workflows (工作流体系)

请根据你当前所处的系统设计阶段，进入对应的子工作流：

### 阶段 1：研究与建模 (Research & Modeling)
用于理解用户并在设计前建立假设。
- ➡️ [Goal-Directed Design Research Guide](references/workflows/goal_directed_design_research.md)
- ➡️ [Interview Phases Guide](references/workflows/interview_phases.md) & [Basic Methods of Ethnographic Interviewing Guide](references/workflows/basic_methods_of_ethnographic_.md)
- ➡️ [Persona Hypothesis Guide](references/workflows/persona_hypothesis.md) & [Persona Construction Process Guide](references/workflows/persona_construction_process.md)
- ➡️ [Persona Guide](references/workflows/persona.md)

### 阶段 2：需求与框架 (Requirements & Framework)
用于将研究转化为设计结构。
- ➡️ [Requirements Definition Process Guide](references/workflows/requirements_definition_proces.md)
- ➡️ [Interaction framework Guide](references/workflows/interaction_framework.md)
- ➡️ [Unified File Model Guide](references/workflows/unified_file_model.md)
- ➡️ [Service Design Framework Guide](references/workflows/service_design_framework.md)

### 阶段 3：设计原则与行为 (Design Principles & Behaviors)
用于优化交互体验和减轻用户认知负担。
- ➡️ [Eliminating Excise Guide](references/workflows/eliminating_excise.md) & [REDUCING WORK AND ELIMINATING EXCISE Guide](references/workflows/reducing_work_and_eliminating_.md)
- ➡️ [Visual Interface Design Guide](references/workflows/visual_interface_design.md)
- ➡️ [Emotional Design Guide](references/workflows/emotional_design.md)
- ➡️ [Design Values Guide](references/workflows/design_values.md)
- ➡️ [Designing for Three Levels of Experience Guide](references/workflows/designing_for_three_levels_of_.md)
- ➡️ [HSV Model Guide](references/workflows/hsv_model.md)
- ➡️ [Validation Scenarios Guide](references/workflows/validation_scenarios.md)
- ➡️ [Thought Partnership Guide](references/workflows/thought_partnership.md)

### 阶段 4：界面范式与模式 (UI Paradigms & Patterns)
用于具体平台的组件与形态设计。
- **设备姿态**：➡️ [Postures for Mobile Devices Guide](references/workflows/postures_for_mobile_devices.md), [Tablet format apps Guide](references/workflows/tablet_format_apps.md)
- **界面组件**：➡️ [Drawer Guide](references/workflows/drawer.md), [Bars Guide](references/workflows/bars.md), [Multi-Touch Gestures Guide](references/workflows/multi_touch_gestures.md), [Welcome and Help Screens Guide](references/workflows/welcome_and_help_screens.md)
- **其他**：➡️ [Interface Paradigms Guide](references/workflows/interface_paradigms.md), [3D Object Manipulation Guide](references/workflows/3d_object_manipulation.md)

## 核心概念与术语检索 (Concept Retrieval)

> [!WARNING]  
> 核心概念字典已编译为高密度的知识图谱。**切勿使用 `view_file` 工具尝试去寻找或读取全量定义文本**，否则会导致严重的上下文溢出与截断。

当你在工作流中遇到未知的交互设计术语（如 HSV Model、Excise、Orphaned Dialogs 等），或需要深挖某个模式的理论依据时，请强制使用以下专属检索脚本：

1. **精确概念解析 (Concept Explanation)**：
   执行本地 Wrapper 脚本以查询独立概念（这将在后台直接访问 `graphify-out/graph.json` 并只返回结果）：
   ```bash
   bash scripts/lookup_concept.sh "Persona"
   ```

2. **原生 Graphify 查询 (可选)**：
   如果你熟悉原生 `graphify`，可以直接在当前环境中执行：
   ```bash
   graphify query "How does Excise relate to Personas?" --graph graphify-out/graph.json
   ```

3. **用户引导**：当你需要用户确认深奥的设计概念时，请建议用户通过 UI 发送命令：`您可以输入 /graphify query "<在此处替换你的概念>" 来探索该术语的图谱关联。`
