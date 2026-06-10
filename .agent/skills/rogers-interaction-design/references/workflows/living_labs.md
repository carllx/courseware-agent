# 生活实验室 (Living Labs) 交互设计工作流

## Prerequisites & Context (前提条件与上下文)

**WHY (为什么使用 Living Labs)**: 
传统的可用性实验室（Usability labs）难以捕捉人们在日常生活中长期使用某项技术的习惯、作息和微小变化。Living Labs（生活实验室）提供了一种在高度贴近真实生活的环境中（或是直接将传感器嵌入真实生活环境），长期跟踪和评估系统使用情况的方法。它特别适合那些需要数月甚至更长时间才能体现价值的技术，比如智能家居、适老化设施或大型城市场景。

**WHEN (何时使用)**:
当你需要评估的不是单一的交互界面，而是一个环境系统、空间体验或者复杂的物联网生态；当你关注用户的长期行为习惯变化、作息偏差或是特定社群（如独居老人、残障人士）的独立生活情况时。

**Deep Dive (深度探索)**:
欲深入了解 Living Labs 的演进历史（如早期的 Aware Home 案例）、传感器部署方案和伦理挑战，请通过以下指令进行动态查询：
```bash
bash scripts/query_theory.sh "What are the key differences between early custom-built Living Labs and modern embedded sensor networks in users' actual homes?"
bash scripts/query_theory.sh "How is PEARL (Person-Environment-Activity Research Laboratory) structured for large-scale user experience studies?"
```

## Comprehensive Guide & Best Practices (综合指南与最佳实践)

Living Labs 的构建和执行比传统测试复杂得多，涉及多学科合作、大型硬件部署以及长期的监控数据分析。

### 阶段一：场景定义与受众招募
**目标**：确定研究规模是“微观居住空间”还是“宏观城市设施”。
- **目标设定**：明确是测试单体智能家居、环境辅助系统（Ambient-assisted homes），还是大型公共空间（如火车站台、城镇广场）。
- **参与者筛选**：寻找愿意长期参与实验的家庭或个人。由于隐私问题，招募过程需极其透明，提供明确的伦理协议（Consent forms）。

### 阶段二：传感器与跟踪设备部署
**目标**：构建非侵入式的数据捕捉网络。
- **设备配置**：
  - 隐形追踪：部署动作捕捉系统、加速度计、环境传感器。
  - 生理与视觉追踪：在适当的触点使用眼动仪（Eye trackers）甚至是脑部扫描仪。
- **环境仿真 (针对大型实验室如 PEARL)**：精确控制空间内的细微变量，如灯光、色彩、音效和空间布局，以便在产品实际落地前进行严格受控的大型仿真测试。

### 阶段三：长周期监控与数据分析
**目标**：捕捉行为的基线（Routines）并识别偏差（Deviations）。
- **持续监测**：利用自动化系统收集数周或数月的数据。
- **异常识别**：对于环境辅助应用（如看护老人），建立基准线并编写警报逻辑，在发生异常行为或意外事故时能实时向看护人发送提醒。
- **跨学科分析**：工程师、研究员和数据科学家共同协作，将海量原始数据转化为对“用户怎么做、为什么这么做、以及情感反应如何”的深入理解。

### 阶段四：创新网络与商业化协作
**目标**：将实验室转变为生态系统。
- **Stakeholder 协同**：将 Living Lab 打造成一个聚集开发人员、社区居民、商业机构和研究人员的创新平台。利用实验室设施和基础设施，展开商业研发合作。

## If/Then Troubleshooting Logic (故障排除逻辑)

- **IF** 发现很难说服家庭搬入定制化的 Living Lab 居住数月（如早期的 Aware Home 困境）：
  - **THEN** 改变策略，将传感器网络无缝嵌入到用户现有的真实住宅中（In-situ deployment），而不是要求他们迁移。
- **IF** 监测过程中产生了海量杂乱的传感器数据，难以提取交互意义：
  - **THEN** 采用机器学习或异常检测算法来首先建立用户的常规行为基线（Routine baseline），只对显著偏离基线的数据段进行深入的人工视频回溯或面谈。
- **IF** 在构建大型公共空间原型时预算超标：
  - **THEN** 考虑与提供基础设施的商业化创新网络（Innovation networks）或学术型超级实验室（如 PEARL）进行合作，而不是从零搭建。
  - **DEEP DIVE**:
    ```bash
    bash scripts/query_theory.sh "What are the best practices for collaborating in commercial Living Lab innovation networks?"
    ```

## Verification Checklists (验证清单)

- [ ] 是否确认了测试目标必须依赖长周期（Weeks/Months）数据，而不能通过短期实验室测试完成？
- [ ] 所有的传感器部署是否在技术上保证了对参与者日常生活的干扰降至最低（Non-intrusive）？
- [ ] 是否具备充足的存储和计算资源来应对数月级别的多模态数据收集？
- [ ] 伦理协议是否详尽覆盖了长期音频/视频监控的隐私风险，并提供了退出机制？
- [ ] 是否在实验室中引入了多学科团队（包含工程师、数据分析师、设计人员）共同解读数据？