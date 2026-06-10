# 设计思维 (Design Thinking) 交互设计工作流

## Prerequisites & Context (前提条件与上下文)

**WHY (为什么使用设计思维)**: 
设计思维（Design Thinking）是一种应对复杂问题解决和创新设计的以人为本（human-centered）的方法论。它侧重于理解用户的需求以及技术能为他们做什么。在交互设计中，运用设计思维能够确保设计团队维持创意心态，并将复杂的系统问题转化为具体的、可被原型化和验证的解决方案。

**WHEN (何时使用)**:
当你需要在一个项目中寻找创新切入点、应对缺乏明确定义的设计挑战、或者在一个传统上不被认为是“创意”的领域（如医疗、政府系统）推行设计实践时，应当采用设计思维工作流。

**Deep Dive (深度探索)**:
如需了解关于设计思维及其争议、核心原则的理论背景，请通过以下指令进行动态查询：
```bash
bash scripts/query_theory.sh "What are the core definitions and controversies surrounding Design Thinking?"
```

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

设计思维的过程并非死板的线性步骤，而是一个高度迭代的框架。以下是基于业界最佳实践（包含 IDEO 以及 Isabell Osann 等人的框架整合）的执行指南。

### 阶段一：观察与理解 (Observe & Understand)
**目标**：建立共识与同理心（Empathy），真正了解用户的需求、痛点和环境。
- **用户调研**：通过深度访谈、实地考察和可用性观察来收集数据。
- **痛点识别**：记录用户在当前情境下的真实困境，不要预设解决方案。
- **理论深究**：
  ```bash
  bash scripts/query_theory.sh "How to conduct effective observation in Design Thinking?"
  ```

### 阶段二：综合与定义 (Synthesize & Define)
**目标**：将杂乱的观察数据提炼为具体的设计挑战。
- **需求重构**：从“需求（desirability）”、“可行性（feasibility）”和“商业可行性（viability）”三个透镜重新审视设计挑战。
- **问题定义**：使用“How might we...” (我们如何才能...) 的句式定义一个既有挑战性又足够聚焦的问题。

### 阶段三：构思与想象 (Ideate & Imagine)
**目标**：发散思维，探索所有可能的解决方案。
- **头脑风暴**：鼓励团队成员抛出各种想法，数量优先，推迟评判。
- **创意工具**：利用草图、故事板等工具将抽象的想法具象化。

### 阶段四：原型与制作 (Prototype & Make)
**目标**：用最小的成本将想法转化为可以交互的实体或界面。
- **低保真原型**：使用纸笔或基础线框图快速构建，重点验证核心流程而非视觉细节。
- **高保真原型**：随着迭代深入，引入交互逻辑和视觉样式。
- **参考图示**：IDEO 的设计思维步骤意在迭代，而非顺序执行。参见 `../../images/77e84dbd2f979588ae913aa0e5c7b7354fae999e3cd22af4a26dc4b2fae594e1.jpg`

### 阶段五：测试与迭代 (Test & Evolve)
**目标**：通过真实用户的反馈来验证和改进原型。
- **任务驱动测试**：邀请目标用户操作原型，观察他们的行为并倾听他们的思考（Think-aloud）。
- **反馈闭环**：将测试结果直接用于改进下一次的原型迭代，必要时退回到前面的阶段。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 团队在构思阶段思维受限，无法产生具有创意的方案：
  - **THEN** 退回到“观察与理解”阶段。引入新的视角或重新进行一次简短的实地考察；参考外部领域的案例来打破思维定势。
- **IF** 最终的原型在可行性（Feasibility）或商业生存能力（Viability）上遇到重大阻碍：
  - **THEN** 重新审视问题的定义（Synthesize），确保技术团队和业务利益相关者在早期即介入并提供约束条件。
- **IF** 对设计思维这一方法的有效性或定义产生质疑（如 Activity 12.7 中的争议）：
  - **THEN** 请运行时 Agent 提取更深层的学术探讨：
    ```bash
    bash scripts/query_theory.sh "What are Jon Kolko's arguments on the divisiveness of design thinking?"
    ```

## Verification Checklists (验证清单)

- [ ] 是否在设计初期就深入了解了用户的真实需求（Desirability）？
- [ ] 问题的定义是否具有开放性，不限制潜在的解决方案？
- [ ] 头脑风暴期间是否遵守了“推迟评判”的原则？
- [ ] 原型是否能够快速构建并以低成本被丢弃？
- [ ] 测试环节是否包含了真实目标用户，并且收集了可操作的反馈？
- [ ] 解决方案是否在“需求、技术可行性、商业生存能力”三者之间取得了平衡？