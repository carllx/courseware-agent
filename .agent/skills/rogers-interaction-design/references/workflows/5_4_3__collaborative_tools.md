# Workflow: 设计协作工具与未来全息通讯 (Designing Collaborative Tools and Holographic Communication)

## 1. Prerequisites & Context (前提条件与上下文)

**WHY (为什么需要本工作流)**:
随着远程办公和在线学习的普及，设计数字协作平台不仅是功能层面的“工具堆砌”（如聊天+网盘），更需要创造“共在感 (Co-presence)”和对彼此行为的“工作感知 (Awareness)”。从共享日历 (Shared Calendars)、频道化聊天 (Slack)、无限白板 (Miro)，到未来的“盒中人”全息投影 (People-in-a-Box) 和 Metaverse 3D虚拟空间，设计师必须理解如何通过技术手段跨越时空限制，营造出色的互动体验。

**WHEN (何时使用本工作流)**:
- 开发在线协作白板、项目管理工具或文档协同编辑软件时。
- 为团队（如软件开发团队、学生项目组）设计异步和同步结合的数字通讯工具。
- 探索下一代通讯方式（如 3D 虚拟形象、AR/VR 全息通话）的体验设计。

**Deep Dive (理论深潜)**:
如需了解关于元宇宙愿景、Web3或具体的协作系统案例研究（如 UCL 教授的 Miro 看板教学法），请让 Agent 运行：
```bash
# 查询关于Metaverse演进、Slack的使用模式以及数字白板在教育中的具体案例
bash scripts/query_theory.sh "Provide insights on the use of Slack in software teams and how Miro is used to create awareness and a feeling of being together in online classes."
```

---

## 2. Comprehensive Guide & Best Practices (综合指南与最佳实践)

### 步骤 1: 构建数字“共在感”与行为透明度
在设计如 Miro、Figma 等无限白板和协同文档时，核心目标是**让人们感觉到彼此**。
1. **实时游标与标识 (Live Cursors & Labels)**：显示参与者的多色光标及名字。即使不发一言，看着几十个光标同时在画布上移动，也能立刻建立“我们在同一个地方工作”的强烈共鸣。
2. **制定空间使用规范**：提供清晰的模版和数字便利贴（Sticky Notes）颜色规范（例如：黄色代表学生互评，橙色代表导师反馈）。
3. **支持空间漫游**：允许用户在庞大画布中自由缩放 (Zoom in/out)、平移，而不是强制所有人盯着同一个视图，以此模拟现实中“逛展板”的体验。

### 步骤 2: 设计跨时空的工作流工具 (Asynchronous & Synchronous)
对于 Slack、Google Calendar 等工具，必须平衡“连接”与“打扰”。
1. **多维度通讯**：支持工作讨论（正式频道）、非正式社交交流以及工具集成（如代码部署通知）。
2. **状态与可用性管理**：让开发者或员工能够挂起工具（Leave it open），并轻松设置/查看他人的“有空/忙碌 (Availability)”状态。
3. **群组协调与邀请机制**：对于共享日历，优化冲突解决机制，避免用户的日历被过多的“待定邀请”塞满引发焦虑。

### 步骤 3: 探索下一代通讯：体积视频与“盒中人” (Volumetric Video)
在设计 3D 头像或全息显示器（如 Proto 的 3D 显示盒）时，超越传统 2D 视频会议的瓶颈：
1. **深度与光影 (Depth and Shadows)**：通过盒子内部件的 LED 补光和阴影追踪（Shadow tracking），提供真实的体积感。这比仅仅把 3D 模型放在平铺屏幕上更能欺骗大脑的感知系统。
2. **尺寸心理学 (Scale Psychology)**：设计时需评估“等身大 (Life-size)”与“微缩版 (Miniature)”全息投影的心理差异。等身大会带来强烈的压迫感或真实感，而微缩版则可能改变沟通的权力动态或显得更像桌面玩具。

---

## 3. If/Then Troubleshooting Logic (If/Then 故障排除逻辑)

*   **IF** 团队在使用无边界数字白板（如 Miro）时感到迷失方向，或者不知道应该看哪里，**THEN** 设计中缺乏导航锚点。需要增加“跟随某人 (Follow me)”功能或设置固定的视角书签 (View bookmarks)。
*   **IF** Slack 等实时聊天工具导致团队成员感到信息过载或“始终在线”的压力，**THEN** 系统缺乏异步工作机制的保护。需增强通知免打扰设定、工作时间过滤，并鼓励将核心决策沉淀到文档而非流动聊天流中。
*   **IF** 用户在全息/3D投影（如 Proto 或 Metaverse）中交谈时觉得对方“没有眼神交流”或“像僵尸”，**THEN** 说明摄像头的捕捉位置与视线映射存在物理偏差。需优化隐藏式摄像头的布局（如在盒子顶部或屏幕后方）以实现眼球对视 (Eye-contact)。

---

## 4. Verification Checklists (验证清单)

- [ ] 协作工具是否提供了显示用户在线状态、实时操作光标等增强“共在感”的功能？
- [ ] 系统是否同时很好地支持了“同步(实时同框协作)”与“异步(事后评论/离线编辑)”两种工作模式？
- [ ] 信息流平台（如企业聊天）是否具备合理的信噪比控制机制以防止通知疲劳？
- [ ] 对于 3D 虚拟环境或全息设备，是否有效处理了光影、深度感知与视线对齐（Eye-gaze）等关键视觉线索？
- [ ] 对于数字画布工具，是否提供了降低学习成本的模版和操作规范说明（如颜色编码）？
