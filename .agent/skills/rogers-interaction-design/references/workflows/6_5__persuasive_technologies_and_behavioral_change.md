# Workflow: 劝导式技术与行为改变设计 (Persuasive Technologies and Behavioral Change)

## 1. Prerequisites & Context (前提条件与上下文)

**WHY (为什么需要本工作流)**:
交互设计不再仅仅是让工具“好用 (usable)”，越来越多地，它被用来干预和改变用户的思想和行为——这就是**劝导式设计 (Persuasive Design)**。从电商的一键下单、运动追踪器中的虚拟宠物（如Pokémon Pikachu的反馈循环），到情绪记录App、ASMR解压视频，以及试图读取用户面部表情的“情感计算(Affective Computing)”，设计师手中握有强大的行为塑造能力。本工作流旨在指导设计师如何有效地使用劝导机制，同时坚守伦理边界。

**WHEN (何时使用本工作流)**:
- 设计健康、健身、环保或学习类应用，目标是培养用户长期习惯时。
- 开发旨在提升心理健康（如情绪追踪日记、VR情绪探索空间、ASMR解压工具）的干预性产品。
- 在系统中引入“情感AI (Emotion AI)”，例如根据用户表情推荐内容或投放广告。

**Deep Dive (理论深潜)**:
如需了解关于劝导式设计的理论框架（如 Fogg 的模型），或情感计算在道德层面的深入探讨，请让 Agent 运行：
```bash
# 获取BJ Fogg的劝导式设计理论(Persuasive Design)和改变习惯的机制
bash scripts/query_theory.sh "Explain BJ Fogg's persuasive design principles and how technology interventions change people's habits."
# 探讨让技术“读取和分析用户情绪”的伦理边界和隐私影响
bash scripts/query_theory.sh "What are the ethical implications of using facial expression analysis to filter online content or ads based on a user's mood?"
```

---

## 2. Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 步骤 1: 选择合适的劝导机制 (Select Persuasive Mechanisms)
通过以下策略组合（Nudging/Cajoling），吸引注意力并改变行为：
1. **阻力最小化**：如亚马逊的一键购买（One-click），移除所有中间摩擦力，诱导直接行动。
2. **正向激励与情感绑定**：设计具备情感属性的反馈物。如 Nintendo Pikachu 计步器，将枯燥的“步数”转换为虚拟宠物的“健康/能量”。当用户运动达标，宠物给予正反馈；若不运动，宠物会“生气(sulking)”。利用人类对数字宠物的依恋（Emotional attachment）来实现行为说服。
3. **趣味性干预 (Playfulness)**：如著名的“钢琴楼梯 (Piano Staircase)”案例，将沉闷的任务（爬楼梯、扔垃圾）转化为有趣的探索，通过游戏化驱动行为改变。

### 步骤 2: 设计心理/情绪干预工具 (Designing for Mental Well-being)
1. **记录与反思闭环 (Double Act of Recording and Reflecting)**：情绪追踪类应用（如 Echo, Daylio）不应仅仅是一个数据记录器。必须包含“反思”机制，例如用堆叠的表情卡片定期提示用户回顾过去，以帮助他们从积极经历中吸取力量。
2. **多感官解压 (ASMR & VR)**：探索视觉之外的感知。利用高保真音频（如切菜、水流声）触发自主感觉经络反应 (ASMR)；或利用 VR（如 Mood Worlds）让用户在 3D 空间中绘画，将抽象情绪具象化，从而引导情绪释放。

### 步骤 3: 确立情感识别的伦理红线 (Establish Emotion AI Ethics)
当系统能够通过面部识别或文本情绪分析来推断用户感受时：
1. **透明度**：必须让用户明确知道“系统正在读取我的情绪”。
2. **克制推荐**：虽然人类朋友可以根据你的心情建议你“去公园走走”，但机器基于抓取的情绪来推送特定广告或改变信息流算法（Filter bubbles），很容易被视为**毛骨悚然 (Creepy) 和侵犯隐私**。不要滥用情绪数据进行商业变现。

---

## 3. If/Then Troubleshooting Logic (If/Then 故障排除逻辑)

*   **IF** 用户在使用健康习惯打卡App时，一开始热情很高但几周后迅速流失，**THEN** 说明系统依赖的是浅层的“外在动机 (Extrinsic motivation，如单纯的积分)”。需要通过引入社会认同（Social proof）或类似虚拟宠物的“情感维系 (Emotional attachment)”来建立内在动机。
*   **IF** 采用游戏化、奖励或惩罚（如应用中的虚拟形象发脾气）来劝导用户时，用户感到被操纵甚至卸载软件，**THEN** 说明劝导机制跨越了界限，变成了“胁迫 (Coercion)”。设计中需提供退出机制（Opt-out），或者允许用户自行设定目标的严厉程度。
*   **IF** 情绪追踪应用中的提示（Reminders）使得本就心情低落的用户感到烦躁，**THEN** 提示频率或时机存在问题。应当利用上下文感知（Context-aware），在用户相对放松的时间（如下班后）温柔地请求记录，而非在工作高峰期弹出。

---

## 4. Verification Checklists (验证清单)

- [ ] 是否清晰定义了产品试图改变的目标行为，并确保其对用户自身是有益的（而非仅仅服务于商业 KPI）？
- [ ] 劝导机制（如提醒、奖励、惩罚）是否适度，有没有越界成为“强迫/操纵”？
- [ ] 若应用涉及情绪日记或追踪，是否闭环了“记录”与“回顾/反思”两个环节？
- [ ] 情感反馈系统的拟人化（如宠物的喜怒哀乐）是否准确映射了用户行为，并且没有引发负面的罪恶感？
- [ ] 如果技术收集了用户的情绪数据（表情、声音、文本），是否获得了明确授权，且算法逻辑对用户透明？
