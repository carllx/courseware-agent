import os

files_data = {
    "/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/references/workflows/acknowledgments.md": """# 致谢与协作生态系统 (Acknowledgments & Collaborative Ecosystem)

## Prerequisites & Context (前提条件与上下文)
在交互设计 (Interaction Design) 领域，任何优秀的产品或理论都不是孤立存在的，它们依赖于庞大的协作生态系统。本工作流旨在指导如何在设计过程中识别、管理并致谢各方贡献者，以维持健康的协作关系。

深入了解学术界与工业界如何进行深度协作：
`bash scripts/query_theory.sh "What are the common collaboration patterns between academia and industry in interaction design?"`

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 1. 识别核心贡献者
- **记录贡献**：在项目初期建立贡献者追踪矩阵，详细记录开发人员、研究对象、赞助商及用户的具体贡献。
- **同行评审的价值**：交互设计高度依赖同行评审。收集并整合多领域的反馈，并将其作为设计的迭代依据。

### 2. 建立跨学科协作框架
- **融合不同视角**：将认知科学 (Cognitive Science)、软件工程 (Software Engineering) 和信息系统 (Information Systems) 等领域的知识整合。
- **尊重知识产权**：在引用外部设计的图表、案例研究时，必须遵守版权和引用规范。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 团队在贡献归属上产生分歧，**THEN** 回顾项目初期的贡献者矩阵，按实际产出比例及关键决策点来划分致谢权重。
- **IF** 需要引用尚未正式发表的研究或设计，**THEN** 务必先取得原作者的书面许可，并在致谢中明确说明来源性质。

## Verification Checklists (验证清单)

### 协作与致谢清单
- [ ] 是否在文档或产品中明确列出了所有内部和外部的贡献者？
- [ ] 跨学科的知识整合是否有明确的理论引用支撑？
- [ ] 图像和案例是否符合版权要求并完成了重写 (例如相对于 workflows 目录的路径)？
""",

    "/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/references/workflows/contents.md": """# 交互设计知识架构导航 (Navigating the Interaction Design Knowledge Architecture)

## Prerequisites & Context (前提条件与上下文)
本书的目录 (Contents) 揭示了交互设计的宏观结构和渐进式知识体系。本工作流将指导 Agent 或设计师如何基于这一架构进行项目范围界定和信息检索。

如果需要深入了解特定章节的理论基础：
`bash scripts/query_theory.sh "Summarize the core concepts and theoretical structure of the textbook contents."`

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 1. 结构化知识检索
- **宏观到微观**：从宏观的“什么是交互设计”(What is Interaction Design) 开始，逐步深入到“可用性目标”(Usability Goals) 和“具体设计原则”(Design Principles)。
- **建立概念映射**：将项目需求映射到目录结构。例如，需求收集对应“理解人们”(Understanding People)，设计评估对应“评估方法”(Evaluation)。

### 2. 构建项目大纲
- **阶段划分**：参考目录结构，将项目划分为：需求分析 -> 原型设计 -> 用户测试 -> 迭代评估。
- **核心组件清单**：确保每个阶段都有明确的交付物和验证标准。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 项目迷失在细节中，无法把握整体方向，**THEN** 重新回归顶层目录架构，审视当前任务在整体知识图谱中的位置。
- **IF** 不确定下一步该采用哪种评估方法，**THEN** 查阅目录中关于“可用性与用户体验目标”的关联章节，选择最契合当前上下文的工具。

## Verification Checklists (验证清单)

### 架构验证清单
- [ ] 项目的阶段划分是否与经典的交互设计生命周期一致？
- [ ] 知识检索的范围是否覆盖了所有必要的基础理论和应用原则？
- [ ] 当需要特定理论支持时，是否已经通过查询脚本获取了详细内容？
""",

    "/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/references/workflows/w_h_a_t__i_s__i_n_t_e_r_a_c_t_.md": """# 什么是交互设计？ (What is Interaction Design?)

## Prerequisites & Context (前提条件与上下文)
交互设计 (IxD) 旨在将产品设计的重心从“软件功能堆砌”转移到“以人为本的体验”。本工作流定义了交互设计的边界、核心组成部分以及它如何超越传统的人机交互 (HCI)。

深入了解交互设计与传统软件工程的根本区别：
`bash scripts/query_theory.sh "What differentiates interaction design from software engineering and traditional HCI?"`

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 1. 确立以人为本的设计理念 (People-Centered Design)
- **明确受众**：我们设计的目标受众是“人”(People)，不仅仅是“用户”(Users)。理解他们在特定环境下的心理模型和任务需求。
- **包容性与可访问性 (Accessibility and Inclusiveness)**：设计必须兼顾不同能力、年龄和文化背景的人群。

### 2. 识别优秀与糟糕的设计
- **从失败中学习**：分析常见的设计失败案例（例如：繁琐的票务机器）。
- **设定体验目标 (Usability and UX Goals)**：将可用性（如易学性、效率）与用户体验（如愉悦感、成就感）相结合作为最终衡量标准。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 产品的技术逻辑完美，但用户反馈极差，**THEN** 检查是否忽视了目标人群的心智模型，重新进行“理解人们”(Understanding People) 的环节。
- **IF** 发现某些边缘人群无法正常使用产品，**THEN** 立即介入包容性设计原则，调整界面对比度、交互方式或提供辅助工具支持。

## Verification Checklists (验证清单)

### 核心概念清单
- [ ] 产品设计是否真正做到了以人为本，而非以功能为本？
- [ ] 是否设立了清晰的可用性目标和用户体验目标？
- [ ] 产品的可用性是否已在真实或模拟的日常环境中被测试和验证？
""",

    "/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/references/workflows/1_3__switching_to_digital.md": """# 向数字化转型：物理到数字的交互演变 (Switching to Digital)

## Prerequisites & Context (前提条件与上下文)
许多曾经依赖物理实体的活动（如纸质车票、实体日历）现已转向数字交互（如手机 App）。本工作流旨在指导如何在这种物理向数字的转移过程中，保留原有的可用性并创造新的便利性，而不是简单地将糟糕的流程电子化。

探索数字转型的历史案例与理论：
`bash scripts/query_theory.sh "What are the key usability challenges when switching a physical artifact to a digital platform?"`

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 1. 解构物理交互过程
- **识别核心动作**：在数字化之前，理解人们在物理世界中完成任务的步骤。例如，在停车收费表投币的行为，其核心是“支付并获得时间凭证”。
- **避免生搬硬套**：不要在屏幕上照搬物理界面的缺点。数字系统应消除物理流程中的摩擦（例如找零钱的麻烦）。

### 2. 提升数字体验的附加值
- **无缝衔接**：利用数字平台的特性（如定位、自动支付、云端同步）让流程更快、更简单。
- **反馈与可见性**：在数字交互中，用户无法获得物理触觉的直接反馈，因此必须提供明确的视觉或听觉反馈以确认操作（如“支付成功”的动画或震动）。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 用户在数字平台上的操作时间比在物理平台上还要长，**THEN** 审查数字化流程是否存在多余的步骤或难以理解的隐喻，精简并重构交互流。
- **IF** 老年用户在向数字工具切换时感到困难，**THEN** 确保设计保留了某些他们熟悉的认知锚点（如清晰的图标），并降低认知负荷。

## Verification Checklists (验证清单)

### 数字化转换清单
- [ ] 数字系统是否比原有的物理系统更快捷、更方便？
- [ ] 是否充分利用了数字平台的优势（自动化、实时反馈）？
- [ ] 缺失了物理触觉后，系统是否提供了足够的补偿性反馈（视觉/听觉/触觉反馈）？
""",

    "/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/references/workflows/activity_1_1.md": """# 构建以人为本的生态系统：活动 1.1 (Activity 1.1: Mapping the Human-Centered Ecosystem)

## Prerequisites & Context (前提条件与上下文)
随着技术的发展，越来越多的计算机相关领域（如网络安全、数字人文、数据科学和人类中心化 AI）开始将“人”置于核心位置。本工作流基于活动 1.1，指导如何将这些新兴领域整合到交互设计的版图之中。

如需获取关于各相关领域的理论拓展：
`bash scripts/query_theory.sh "How do fields like cybersecurity, digital humanities, and human-centered AI intersect with interaction design?"`

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 1. 跨领域的整合分析
- **以人为本的 AI (Human-Centered AI)**：在设计 AI 系统时，不仅要追求算法准确性，更要考虑其决策过程的透明度和用户的信任感。
- **网络安全的可用性 (Usable Security)**：安全机制不应以牺牲可用性为代价。设计既安全又不会引起用户反感的验证流程。

### 2. 动态更新设计版图
- **持续映射**：定期审视交互设计的知识图谱，判断是否需要将新出现的领域（如数字医疗）纳入核心关注点。
- **多学科协同**：鼓励数据科学家、安全专家与 UX 设计师之间的紧密合作，打破信息孤岛。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 新集成的 AI 功能导致用户的信任度下降，**THEN** 增加算法输出的解释性 (Explainability)，让用户理解背后的逻辑，并提供人工干预的选项。
- **IF** 系统的安全要求严重阻碍了正常的用户操作流程，**THEN** 重新评估安全策略，探索无感知认证 (Invisible Authentication) 或生物识别技术的应用。

## Verification Checklists (验证清单)

### 跨领域融合清单
- [ ] 系统中的 AI 决策过程是否对用户足够透明并建立信任？
- [ ] 安全与隐私设计是否兼顾了良好的用户体验？
- [ ] 设计团队是否包含或咨询了相关领域（如数字医疗、安全）的专家意见？
"""
}

for path, content in files_data.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {path}")

