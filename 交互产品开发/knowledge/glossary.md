# 交互产品开发 — 核心术语对照表 (Glossary)

> 本表收录课程高频核心术语的中英文对照与简要定义，按教学周序排列。

---

## 基础概念 (W1–W2)

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| 交互设计 | Interaction Design (IxD) | 设计支持人们日常工作和生活的交互式产品的学科，关注人与技术之间的对话方式 |
| 用户体验 | User Experience (UX) | 用户在使用产品或系统过程中的整体感受，涵盖情感、认知和行为维度 |
| 可用性 | Usability | 产品可以被特定用户在特定场景中有效、高效且满意地使用的程度 |
| 可用性目标 | Usability Goals | 有效性 (Effectiveness)、效率 (Efficiency)、安全性 (Safety)、效用性 (Utility)、可学习性 (Learnability)、易记性 (Memorability) |
| 体验目标 | User Experience Goals | 超越功能层面的感性目标，如趣味性、满意度、美感、动机激发等 |
| 心智模型 | Mental Model | 用户基于已有经验对系统运作方式的内在认知表征 |
| 实施模型 | Implementation Model | 系统/软件实际的工程运作方式，通常与用户心智模型存在差距 |
| 表现模型 | Represented Model | 设计师通过界面呈现给用户的系统工作方式，好的设计应尽量贴近心智模型 |
| 界面隐喻 | Interface Metaphor | 借用现实世界事物的概念来帮助用户理解数字界面元素及其行为 |
| 认知负荷 | Cognitive Load | 用户在完成任务时工作记忆承受的信息处理负担 |
| 格式塔原则 | Gestalt Principles | 人类视知觉的组织规律（接近、相似、闭合、连续、共同命运等） |
| 执行鸿沟 | Gulf of Execution | 用户意图与界面所允许操作之间的不匹配程度 (Norman) |
| 评估鸿沟 | Gulf of Evaluation | 系统反馈与用户预期之间的不匹配程度 (Norman) |
| 示能性 | Affordance | 物品属性所暗示的可操作方式，无需说明即可感知 |

## 敏捷洞察与MVP (W3–W4)

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| 精益用户体验 | Lean UX | 将精益创业方法论融入 UX 设计流程，强调假设验证与快速迭代 |
| 待办任务法 | Jobs-to-be-Done (JTBD) | 聚焦用户在特定情境下试图达成的目标（"任务"），而非用户画像本身 |
| 假设驱动设计 | Hypothesis-Driven Design | 将产品假设转化为可验证命题，通过最小实验验证或推翻 |
| 极简人物志 | Proto-Persona | 基于团队假设快速构建的轻量用户画像，无需大规模调研 |
| 最小可行产品 | Minimum Viable Product (MVP) | 以最低成本实现核心功能的产品版本，用于测试市场假设 |
| MoSCoW 法 | MoSCoW Method | 功能优先级划分法：Must Have / Should Have / Could Have / Won't Have |
| 价值主张 | Value Proposition | 产品为目标用户创造的核心价值承诺 |

## 架构与系统设计 (W5–W6)

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| 目标导向设计 | Goal-Directed Design | Cooper 提出的以用户目标而非任务为中心的设计方法论 |
| 状态机 | State Machine | 描述系统所有可能状态及其转换条件的数学模型，交互设计中用于梳理页面流 |
| 交互编排 | Orchestration | About Face 中和谐交互的 14 条策略，确保界面行为的整体协调性 |
| 附加税 | Excise | 界面强加给用户的非目标操作负担（导航/模态/权限申请等） |
| 心流 | Flow | Csikszentmihalyi 提出的最优体验状态，任务难度与技能水平动态平衡 |
| 盒模型 | Box Model | CSS 布局基础：Content → Padding → Border → Margin 四层嵌套 |
| 弹性布局 | CSS Flexbox | 一维弹性容器布局模型，Figma AutoLayout 的前端对应物 |
| 自动布局 | AutoLayout (Figma) | Figma 中的响应式容器系统，映射 CSS Flex 的方向/间距/对齐属性 |
| 原子设计 | Atomic Design | Brad Frost 提出的五层组件拆解体系：原子→分子→有机体→模板→页面 |
| 设计令牌 | Design Token | 将颜色、间距、字重等设计属性抽象为可复用的语义化变量 |

## 视觉重构 (W7–W8)

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| 信息层级 | Visual Hierarchy | 通过尺寸、字重、颜色、空间等手段引导用户注意力先后顺序 |
| HSL 色彩系统 | HSL (Hue-Saturation-Lightness) | 基于色相/饱和度/亮度的直觉化调色模型，替代传统 HEX |
| 高程系统 | Elevation System | 用阴影深度表示 UI 元素与画布的距离层级（通常 5 级） |
| 暗黑模式 | Dark Pattern | 利用界面设计诱导用户做出非预期行为的欺骗性手法 |
| 空状态 | Empty State | 界面首次加载/数据为空/搜索无结果时的兜底呈现 |
| 防错设计 | Error Prevention | 通过约束、默认值和确认机制从源头减少用户犯错机会 |
| 宽容度设计 | Forgiveness / Undo | 允许用户撤销操作或从错误中轻松恢复的设计策略 |

## AI 原型与动效 (W9–W11)

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| Vibe Coding | Vibe Coding | Andrej Karpathy 提出的理念：设计师以自然语言指挥 AI 生成代码，聚焦"感觉"而非逻辑 |
| 结构化提示词 | Structured Prompt | 按 RCPVU 等框架组织的系统级指令，用于驱动 AI 精准生成 UI |
| 微交互 | Microinteraction | Dan Saffer 提出的四要素框架（触发/规则/反馈/循环模式）下的细粒度交互细节 |
| 混合保真度 | Mixed Fidelity | 同一原型中部分使用高保真（代码）、部分使用低保真（Figma 串联）的降级策略 |
| 缓动函数 | Easing Function | 控制动画加速度曲线的数学函数（ease-in / ease-out / cubic-bezier） |

## 评估与复盘 (W12–W14)

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| 启发式评估 | Heuristic Evaluation | Nielsen 提出的专家检查法，以 10 条可用性原则为标尺系统查找界面缺陷 |
| Nielsen 十大原则 | Nielsen's 10 Usability Heuristics | 系统可见性/匹配/用户控制/一致性/防错/识别优于记忆/灵活/美学/帮助恢复/帮助文档 |
| 出声思考法 | Think-Aloud Protocol | 要求测试者在操作时持续外化思维过程的定性测试方法 |
| 并发出声思考 | Concurrent Think-Aloud (CTA) | 用户边操作边说出想法，实时捕获认知过程 |
| 回溯出声思考 | Retrospective Think-Aloud (RTA) | 任务完成后用户回看录屏并解释行为决策 |
| 严重度量表 | Severity Rating Scale | 0–4 级缺陷严重度评定（0=无问题 ~ 4=灾难性） |
| 亲和图 | Affinity Diagram | 将零散测试发现按主题归类聚合的质性分析方法 |
| 系统可用性量表 | System Usability Scale (SUS) | Brooke 提出的 10 题标准化可用性评分问卷，满分 100 分 |
| 闭环叙事 | Closure Narrative | 作品集复盘的三幕结构：冲突铺设 → 设计挣扎 → 量化结果 |
