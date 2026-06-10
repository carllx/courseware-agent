# Workflow: 设计社交游戏与在线社区体验 (Designing Social Games and Online Communities)

## 1. Prerequisites & Context (前提条件与上下文)

**WHY (为什么需要本工作流)**:
社交游戏 (Social Games) 的核心不仅是游戏机制，更在于创造玩家之间的“连接”——无论是竞争、协作、同侪压力还是纯粹的陪伴。从增强面对面互动（如基于Alexa的家庭游戏），到基于游戏频道的实时聊天社区（如 Discord + Fortnite），再到极简主义的抽象沟通（如游戏《风之旅人 Journey》），以及 Twitch 等平台上的游戏直播（Live Streaming），设计师必须有策略地引导玩家间的社交互动和社群构建。

**WHEN (何时使用本工作流)**:
- 开发在线多人游戏，并设计其中的沟通机制（文本、语音或非语言线索）时。
- 为游戏外围构建社交和观赛体验（如直播平台交互、Discord频道社区）时。
- 设计辅助技术（如 PeopleLens）以通过技术干预增强物理世界中的“社交存在感”时。

**Deep Dive (理论深潜)**:
如需了解评估游戏社交性的理论启发式或特定游戏案例分析，请让 Agent 运行：
```bash
# 获取 Matt Richetti 关于评估社区型游戏社交性的三个启发式原则
bash scripts/query_theory.sh "Explain Matt Richetti's three heuristics for assessing how community-based and social a game is."
# 获取游戏直播(Live Streaming)社区中双向交流和较小社区动态的理论分析
bash scripts/query_theory.sh "Describe the role of two-way communication and community sense in live streaming platforms like Twitch according to Taylor (2018)."
```

---

## 2. Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 步骤 1: 评估与设定社交互动属性 (Apply Richetti's Heuristics)
在设计社交游戏机制时，首先通过这三个维度定位产品的社交深度：
1. **时间维度 (Synchronous vs. Asynchronous)**：
   - 玩家是实时同步交流（如语音开黑），还是异步轮流行动？同步互动需要考虑不同技能水平玩家的融合（例如：新手提问区 vs 高手吹水区）。
2. **关系对称性 (Symmetrical vs. Asymmetrical)**：
   - 建立关系需要双方同意（如双向互关/加好友），还是可以单边建立（如单向关注/订阅）？
3. **关系强度 (Strong vs. Weak ties)**：
   - 游戏旨在建立长期的深度关系（如同一个公会多年的战友），还是瞬时、短暂的交集（如随机匹配的单局队友）？

### 步骤 2: 设计沟通通道与摩擦力 (Designing Communication Channels)
并非越丰富的沟通渠道越好。有意识地设计“沟通摩擦”能产生独特的体验。
1. **多层级通道**：像 Discord 一样，提供从大厅文字广播、群组语音，到特定频道内的“耳语 (Whisper)”功能的层级。
2. **极简抽象沟通**：参考游戏《风之旅人 (Journey)》的做法，如果想要营造纯粹的陪伴感和友善氛围，可以**彻底剥夺**文字和语音能力，仅提供一种抽象符号（如音乐钟声）作为唯一沟通手段。这能有效消除网络喷子 (Trolls)，让玩家在共同探索中产生深层的情感共鸣。
3. **技术介导的物理社交**：如果是线下游戏，可以引入语音助手（如 Alexa 玩石头剪刀布），将技术作为“裁判”或“节拍器”，让玩家视线离开屏幕，重新聚焦在彼此身上，从而促进物理家庭/朋友的社交黏性。

### 步骤 3: 设计直播与观战社区 (Live Streaming Ecosystems)
对于游戏直播（如 Twitch/YouTube）或观战模式：
1. **强化双向沟通机制**：赋予弹幕和聊天室影响主播行为的能力（如“下注”、“打赏惩罚”、“挑战主播”），将观众从被动接收者转化为主动参与者。
2. **小社区的归属感保护**：大主播虽然流量高，但小主播（几十人观看）的聊天室往往具有更高的“社区认同感”和互动率。在平台级设计时，需提供机制让用户更容易发现并沉淀到这些类似“周末公园球赛”的亲密小社区中。

---

## 3. If/Then Troubleshooting Logic (If/Then 故障排除逻辑)

*   **IF** 游戏内的同步聊天区充斥着老玩家对新手的敌意（Toxic behavior），**THEN** 说明系统的“强弱关系”混合不当。应当根据技能等级或行为评分隔离频道，或者引入极简的“非语言点赞/感谢系统”以冲淡恶意交流。
*   **IF** 直播平台的观众反馈参与感低、只像在看传统电视，**THEN** 缺乏有效的“破壁 (Fourth-wall breaking)”机制。需引入观众可触发的屏幕特效、投票改变游戏走向、或是专属指令机器人。
*   **IF** 物理环境中的特殊群体（如视障儿童）无法捕捉社交线索导致被孤立，**THEN** 设计者应当引入增强现实或基于音频的“技术社交存在感 (Technological social presence)”工具（如 PeopleLens），将视觉视线转化为空间音频反馈，重建社交参与的心理地图。

---

## 4. Verification Checklists (验证清单)

- [ ] 是否已明确定义游戏内社交关系的时间性、对称性和强弱属性？
- [ ] 游戏内的沟通系统是否符合游戏想要传达的情感基调？（例如，是否需要故意限制文字语音以防止破坏氛围？）
- [ ] 若游戏包含直播/旁观模式，是否为观众提供了直接影响或与游戏/主播互动的机制？
- [ ] 系统是否提供了足够细粒度的沟通控制选项（如屏蔽、耳语、频道分组）来保护玩家免受骚扰？
- [ ] 对于共处一室的物理社交游戏，技术的引入是否起到了促进“人与人对视”的作用，而不是让人们都埋头看屏幕？
