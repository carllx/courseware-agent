# 参考文献与学术检索 (References & Bibliography) 工作流

## Prerequisites & Context (前提条件与上下文)

**WHY (为什么需要参考文献工作流)**: 
《交互设计》(Interaction Design) 涵盖了庞大且深入的理论、前沿实证研究和经典模型。在执行高级 Agent 任务（如编写新的设计启发式评估报告、建立理论框架）时，必须通过追溯权威学术文献来保证论点的严谨性和客观性。本工作流旨在指导 Runtime Agent 如何在此概念集群（包含大量从A到Z的参考文献节点）中进行学术溯源、引文验证和理论深度提取。

**WHEN (何时使用)**:
当你需要为设计决策提供学术背书时；当在其他工作流中遇到指示（如 `query_theory.sh`）需要深入挖掘特定的心理学模型、社会计算理论或人机交互（HCI）经典论文时；当你需要生成带有标准学术引用的综合报告时。

**Deep Dive (深度探索)**:
在处理数百条包含如 Fitts' Law、Distributed Cognition、Living Labs 等主题的文献库时，如果需要理解某些引用文献的完整背景，请执行：
```bash
bash scripts/query_theory.sh "Summarize the key findings from Rogers et al. (2011) regarding Interaction Design Gone Wild."
```

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

由于参考文献库极为庞大，Agent 不应一次性读取所有文献条目。应遵循以下渐进式披露（Progressive Disclosure）原则进行检索与应用：

### 阶段一：关键词定位与检索策略
**目标**：从海量文献堆（Chunk 000）中精确抽取出相关的论文或书籍。
- **构建检索词**：根据用户的设计问题，提取核心词（例如：“Distributed Cognition”, “Fitts’ Law”, “Accessibility”）。
- **执行正则检索**：使用 grep 或文件搜索工具，在 `references/` 目录下搜索核心词，锁定目标作者和年份（如 "Blandford, A.", "Rogers, Y."）。
- **分析文献类型**：辨别检索到的条目是经典著作（如 *Case Study Research*）、顶级会议（如 CHI, CSCW, UbiComp），还是行业报告。

### 阶段二：学术知识点的动态提取
**目标**：仅仅找到文献标题是不够的，必须进一步获取文献所支撑的理论内容。
- **调用深度查询**：
  获取文献条目后，向知识库发起查询以理解文献的实际应用。例如，如果检索到 `Yin R. K. (2018) Case Study Research and Applications`，应当继续询问系统该文献在交互设计评估中的应用范式。
  ```bash
  bash scripts/query_theory.sh "How is Yin's Case Study Research method applied to natural settings evaluation?"
  ```

### 阶段三：学术证据向设计指南的转化
**目标**：将学术结论转化为可操作的设计启发式（Heuristics）。
- **剥离学术黑话**：将诸如“社会化环境下的认知分布模型”转化为具体的 UI/UX 检查清单（例如：“系统是否在物理界面和数字界面之间合理地分布了认知负荷？”）。
- **格式化引文**：在生成的最终交付物（如调研报告、架构设计）中，务必附带标准的 APA 格式引用，以增强产出物的可信度。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 检索特定的学者（例如 "Rogers, Y."）返回了过多的文献条目（数十条）：
  - **THEN** 缩小检索范围。结合年份（如 2011, 2012）或研究领域（如 "Wild Theory", "Pervasive Computing"）进行二次过滤。
- **IF** 在当前的 Reference Chunk 中找不到关于最新技术（如 Voice Control 或 AI 交互）的文献：
  - **THEN** 注意当前文本数据库的时间截断点（如涵盖至 2022 年）。若缺乏最新数据，应结合 `search_web` 技能，通过外部网络搜索最新的 ACM/IEEE 会议论文进行补充。
- **IF** 论文标题极长或存在拼写截断（如 `Yeratziotis, A., and Zaphiris, P. (2018) A Heuristic Evaluation for Deaf Web User Experience (HEADWUX)`）：
  - **THEN** 提取核心首字母缩写（如 HEADWUX）作为新的检索键，以获取该启发式评估法的具体步骤和指标。

## Verification Checklists (验证清单)

- [ ] 是否在给出强烈的理论断言前，查阅了对应的学术出处？
- [ ] 提取的文献是否准确关联到了正确的研究领域（如将 Fitts' Law 关联至注视输入/Gaze input 或控制设备设计）？
- [ ] 动态提取理论时，是否将庞大的学术块精简为了对当前设计任务有直接帮助的 1-2 条规则？
- [ ] 是否确保了所有在工作流中引用的文献都在最终报告中留存了标准的学术溯源标记？