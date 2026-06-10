# Lean UX 核心流程 (The Lean UX Process)

## Prerequisites & Context
**目的**: 将传统的需求驱动的线形开发流程转换为基于假设驱动（Hypothesis-Driven）和注重结果（Outcomes over Outputs）的敏捷迭代模型。
**适用场景**: 当团队在不确定性较高的环境中开发新功能或新产品，需要快速验证商业价值与用户价值时。

## Comprehensive Guide & Best Practices

### 1. 声明商业问题 (Declare Assumptions)
- **步骤**: 团队跨职能（设计、开发、产品）共同探讨当前的商业问题，而不是直接讨论解决方案。
- **产出**: 形成初始假设清单。
- **最佳实践**: 采用“Lean UX Canvas”作为视觉化工具，明确业务问题、目标用户、预期商业成果（Business Outcomes）和用户收益（User Outcomes）。

### 2. 制定假设 (Create Hypotheses)
- **启发式法则**: 使用标准模板转化假设：“我们相信通过为 [用户画像] 提供 [功能/体验]，能够实现 [商业结果]。我们将通过观察到 [定量/定性指标] 来证明这是真的。”
- **原则**: 优先处理风险最高、最未知的假设（Riskiest Assumptions）。

### 3. 构建 MVP (Build Minimum Viable Products)
- **核心理念**: 这里的 MVP 指的是“最小可行性实验”，而不是产品的最小功能集。目的是“学习”而非“交付”。
- **策略**: 考虑使用线框图、点击原型、落地页测试（Landing Page Test）或 Wizard of Oz 实验。
- **原则**: 以最小的工程代价获取最有效的认知（Validated Learning）。

## If/Then Troubleshooting Logic
- **如果** 团队过于纠结于高保真设计：
  - **则** 引导他们退回纸笔草图，强调当前的目标是验证假设而非最终交付。
- **如果** 业务方只关心功能上线（Outputs）：
  - **则** 使用数据指标反问：“这个功能上线后，我们期望看到用户行为发生什么改变？我们如何衡量？”将对话拉回成果（Outcomes）。

## Verification Checklists
- [ ] 是否所有利益相关者都在同一张 Lean UX Canvas 上达成共识？
- [ ] 是否已明确定义了成功指标（Success Metrics）？
- [ ] 计划构建的 MVP 是否能以最低成本验证核心假设？

> [!TIP]
> 关于假设检验背后的深层理论，请运行 `bash scripts/lookup_concept.sh "Hypothesis-Driven Design"`。
