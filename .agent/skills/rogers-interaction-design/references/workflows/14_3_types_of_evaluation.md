# 评估类型 (Types of Evaluation) 交互设计工作流

## Prerequisites & Context (前提条件与上下文)

**WHY (为什么进行分类评估)**: 
在交互设计中，没有一种万能的评估方法。根据评估环境（Setting）、用户参与度（Participants' involvement）和控制程度（Level of control），我们需要选择不同类型的评估方法。正确匹配评估类型与项目阶段，能帮助我们以最优的成本暴露出系统的可用性问题（Usability problems）和深层的用户体验（User experience）反馈。

**WHEN (何时使用)**:
当你的原型或产品需要验证其有效性、可用性或用户满意度时；当面临地理限制或疫情等不可抗力需要开展远程评估（Remote evaluation）时。

**Deep Dive (深度探索)**:
如需了解关于三大评估类别的理论背景和早期远程评估历史（如 Hartson et al., 1996），请通过以下指令进行动态查询：
```bash
bash scripts/query_theory.sh "What are the pros and cons of the three broad categories of evaluation in interaction design?"
bash scripts/query_theory.sh "How did remote evaluation evolve since the 1990s and during the COVID-19 pandemic?"
```

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

我们将评估分为三大类。执行评估前，必须根据当前产品的成熟度和研究目标，在以下三者间做出选择：

### 1. 受控环境评估 (Controlled Settings)
**适用场景**：验证特定假设、测试具体功能、收集精准的可用性指标（如任务完成时间、错误率）。
- **执行方法**：可用性测试 (Usability testing)、受控实验 (Experiments)。
- **操作步骤**：
  1. 招募目标用户在可用性实验室 (Usability labs) 或隔离环境中进行测试。
  2. 严格控制环境变量，给用户分配标准化任务。
  3. 观察和测量用户的具体行为（如点击流、视线追踪）。
- **优势/劣势**：非常擅长发现可量化的可用性问题，但在捕捉真实的“使用情境 (Context of use)”方面表现较差。

### 2. 自然环境评估 (Natural Settings / In-the-wild)
**适用场景**：了解产品在真实世界中的使用方式、用户在不受控状态下的真实情感与行为反馈。
- **执行方法**：实地研究 (In-the-wild studies)、在线社区观察。
- **操作步骤**：
  1. 将产品/原型投放至公共场所或用户的自然生活/工作环境中。
  2. 尽可能不干预用户的操作，收集长期的、定性的使用数据。
- **优势/劣势**：能极好地展现真实情境下的技术使用情况，但极其耗时，且实施难度较高。

### 3. 无直接用户参与的评估 (Settings not directly involving participants)
**适用场景**：时间紧迫、预算有限，或在产品极早期阶段需要快速排除基础可用性障碍时。
- **执行方法**：启发式评估 (Heuristic evaluation)、认知走查 (Cognitive walkthroughs)、模型预测与分析 (Analytics)。
- **操作步骤**：
  1. 邀请专家或研究人员（而非真实用户）作为评估者。
  2. 根据既定规则（如尼尔森十大可用性原则）对界面进行审查。
  3. 利用分析工具（Analytics）追踪已上线系统的大规模点击数据。
- **优势/劣势**：快速、低成本，能迅速追踪网站使用情况，但无法揭示用户行为背后的“原因（Why）”和“情感（How users feel）”，容易遗漏不可预测的交互问题。

### 附加策略：远程评估 (Remote Evaluation)
以上三大类评估均可结合“远程”模式开展。利用网络与数字监控工具，可突破地域和时区限制，甚至能够同时支持超大规模（如 100,000+ 参与者）的数据收集。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 在实验室环境（Controlled Settings）中找不到致命的用户体验问题，但产品上线后依然遭到用户抱怨：
  - **THEN** 说明脱离了使用情境。应立即启动一次小规模的“自然环境评估 (In-the-wild)”，以观察真实环境干扰因素（如噪音、多任务处理）对交互的影响。
- **IF** 经费紧张且招募不到足够的目标用户：
  - **THEN** 优先采用“无直接用户参与的评估”，让内部专家进行启发式审查。
  - **DEEP DIVE**：
    ```bash
    bash scripts/query_theory.sh "What are the best methods for conducting evaluation without direct user involvement?"
    ```
- **IF** 需要知道用户为何点击某个按钮（Why），但目前的 Analytics 工具只能显示点击次数：
  - **THEN** 停止仅依赖 Analytics 的评估，转向受控实验室进行“放声思考 (Think-aloud)”可用性测试。

## Verification Checklists (验证清单)

- [ ] 评估前是否已明确团队需要解决的是“可用性障碍（Usability）”还是“真实情境体验（Context of use）”？
- [ ] 选择评估类型时，是否已经权衡了时间成本、参与者招募难度和环境控制力？
- [ ] 是否根据当前条件评估了引入“远程评估 (Remote Evaluation)”的可能性？
- [ ] (如果使用无用户参与的评估) 是否选择了经验丰富的专家来执行审查，而非新手？
- [ ] (如果使用 Analytics) 是否清楚分析工具只能提供行为数据，而不能代替情感反馈？