---
id: fatal-interface-design-cases
title: 致命界面设计：交互事故案例库
tags: ["fatal-design", "Therac-25", "TMI", "Boeing-737-MAX", "human-factors", "safety"]
source_url: https://ieee.org
archived_at: 2026-03-04
courses: ["交互产品开发"]
---

# 致命界面设计：交互事故案例库

# 致命界面设计：交互事故案例库

> 来源：综合搜索（2026-03-04）
> 标签：fatal-design, Therac-25, TMI, Boeing-737-MAX, human-factors, safety
> 对应周次：W1（导入段扩展）/ W4（安全性可用性目标）

## 核心要点

### 案例 1: Therac-25 放射治疗机（1985-1987）

*   **事故概况**：加拿大原子能有限公司 (AECL) 生产的 Therac-25 放射治疗仪，在 1985-1987 年间造成至少 6 起严重辐射过量事故，3 人死亡。一名患者本应接受 180 拉德的治疗剂量，实际却被注入了**数万拉德**——正常值的 100 倍以上。
*   **界面设计缺陷**：
    - **隐晦的错误代码**：机器显示 "Malfunction 54" 等密码式错误信息，操作员无法判断严重程度
    - **"P"键陷阱**：操作员习惯了频繁的非致命报错，养成了按 "P" (Proceed) 跳过错误的肌肉记忆——但这次，跳过的是致命辐射过量
    - **虚假的"一切正常"**：屏幕显示"no dose"（无剂量），操作员以为治疗未执行，实际上患者已被过量辐射
    - **移除了物理安全锁**：前代机型 Therac-6/20 有硬件安全联锁装置来屏蔽软件Bug，Therac-25 为降本增效将其全部移除，把安全完全交给了有Bug的软件
*   **根本教训**：表现模型说"一切正常"，工程实施模型已经失控。界面欺骗了操作员的心智模型。

### 案例 2: 三哩岛核电站事故（1979）

*   **事故概况**：美国最严重的核泄漏事故。反应堆冷却水因泄压阀故障持续流失，操作员在长达 2 小时内未能正确判断阀门状态，导致核心部分熔毁。
*   **界面设计缺陷**：
    - **PORV 阀门指示灯骗局**：控制面板上的指示灯只显示"已发送关阀信号"，而不是阀门的实际物理状态。操作员看到灯亮=以为阀门关了，实际阀门卡在了打开位置
    - **红灯反直觉**：一个红色指示灯（全世界公认的"危险"信号）在这里却表示水位正常。操作员误判为水位危高，关掉了正在正常工作的紧急冷却系统
    - **圣诞树效应**：控制室约 1900 个显示器，布局混乱，颜色编码不一致，维护标签遮挡了重要指示灯
    - **Don Norman 评价**：设计心理学领域的奠基人 Don Norman 称三哩岛的控制室界面"极度令人困惑" (profoundly confusing)

### 案例 3: Boeing 737 MAX 空难（2018-2019）

*   **事故概况**：Lion Air 610 + 埃塞俄比亚航空 302，共 **346 人遇难**。
*   **MCAS 系统设计缺陷**：
    - 新型发动机改变了机体气动特性，波音添加了 MCAS 自动压低机头系统来模拟旧机型手感——目的是**避免飞行员重新培训**（降低航空公司采购成本）
    - MCAS 仅依赖**单个攻角传感器**数据，传感器故障即反复将飞机压向地面
    - **飞行员完全不知道 MCAS 的存在**——波音没有在手册中充分披露，也没有提供专项模拟训练
    - 波音假设飞行员能在 10 秒内识别并处理 MCAS 故障，实际上面对矛盾的警报洪流（失速警告 + 空速/高度冲突），飞行员的心智模型中根本没有"MCAS"这个概念
*   **根本教训**：当自动化系统的心智模型对用户完全不可见时，用户就无法在关键时刻夺回控制权。**346 条生命的代价。**

## 可用叙事角度

*   **W01 导入段**：Therac-25 是首选开场案例——"按下 P 键，就是按下了死亡按钮"。3 分钟即可讲完，震撼力极强，且直接对接后续的可见性/反馈/安全性原则和三大模型理论
*   **三哩岛**可作为"红灯≠危险"的反直觉案例，强化示能信号 (Signifier) 的重要性
*   **737 MAX** 适合 W5（心智模型匹配度）或 W11（AI/自动化系统排障）复用
*   三个案例共同论证：**"人因失误"(Human Error) 几乎总是设计失误的症状，而非原因**

## 原始引用

> "Operators were accustomed to frequent malfunctions and learned to bypass error messages by pressing 'P' (Proceed). This ingrained behavior led them to dismiss critical warnings." — MSU, IEEE
> "Don Norman has characterized the TMI control room interfaces as profoundly confusing." — Medium
> "Pilots were largely unaware of MCAS's existence or its operational specifics. Boeing assumed pilots would recognize and respond within 10 seconds." — NASA, Time

## 与课程的关联

W01 导入段扩展候选。Therac-25 天然对接 Cooper 的"四宗罪"（粗鲁的错误信息 + 强迫人像计算机思考 + 邋遢的行为 + 让人类承担苦力），可作为从体感到理论的桥梁。亦服务于人文层标签多样性需求（`[CASE STUDY]`）。
