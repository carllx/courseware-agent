import os

with open("W09_AI原型协作结构化.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

head_lines = lines[:89]
tail_lines = lines[407:]

middle_text = """
> [CASE STUDY]
> **当组件库遇见超大模型**
> 很多人依然有疑虑：凭什么用自然语言让 LLM 工具写出来的代码，就不再是以前导出工具拉出来的垃圾呢？让我们看看像 v0 这样的先进体系在底层到底如何执行了这场降维打击。
> 传统的代码导出插件，看设计图就像盲人摸象，它眼里只有死板生硬的一根根分离的网格线。而 v0 却截然不同，它是在孜孜不倦地去**阅读、消化并疯狂理解**世界上最优秀的那些开源抽象组件库（比如 shadcn/ui 和极其系统化的 Tailwind CSS）。
> 当你对大模型随意地描述：“给我一个企业级的数据仪表盘（Dashboard）”时，它深层神经网路里立刻浮现出来的并不是几百个等待填充色彩的零散空洞矩形方块，而是令人叹为观止的组合系统：“哦，这个商业推演场景极其庞大，它必然需要组合一个极强交互性的 Recharts 图表聚合组件库、还要布置三个带异步状态轮询的统计数据面板，并且最外层必须要严丝合缝地套上一个高可用性的响应式 Dashboard Layout 栅格结构”。
> 这意味着，AI 绝不是在帮你枯燥地“画图”，而是在充当一名绝顶干练的极客包工头，疯狂地帮你**拼装工业级的标准预制件**。那些繁复的无障碍访问属性标签 (ARIA 指南)，在电光火石之间，就被部署完毕。
> 
> 但是，如果它用的全都是无聊预制件，你们的设计价值究竟体现在哪里？
> 这就是为什么我们在前面必须要建立起那一套极高保真的私人 Design Token 清单系统的根本原因！那些生成的默认组件，虽然结构稳固，但是毫无例外全都是极其冰冷、粗糙且全然丧失灵魂的工业标准件。
> 作为交互产品架构师，你的真正致命武器，就是果断祭出你的 Token 字典表，将这套灰白色的开源通用骨架，用你们独有的颜色冷暖韵律表、高低材质阴影特征（Tokens参数集）进行强行注入与**霸权覆盖**。你是一个牢牢掌握着视觉配方的灵魂调色师。

> [STORY TIME]
> **血泪警示录：一个按键圆角修改所引发的全盘崩溃**
> 过去如果设计总监想要把所有按钮的 4px 圆角改为 8px，在 Figma 里只需要 3 秒。但是前端开发人员要在代码海里找出所有写死的 (Hard-coded) 老旧按钮，逐个修改并回归测试，往往需要耗费数十乃至上百小时，而且最后依然会漏掉几个深埋的组件，导致线上严重事故。这就是原本极其不对等的心智修改成本灾难。而在 Vibe Coding 的体系下，一条全局语义命令：“将 primary button 的 border-radius token 修改为 md 并映射到 8px”，大模型瞬间就会完成重构验证，工业生产力发生了断代跃迁。

> [TEACHING MOMENT]
> **打破魔法错觉：被转移的脑力劳动**
> 记住，不要把 AI 当成仙女教母，它的生成能力绝对不是能够凭空将你脑中模糊的幻想具象化的魔法。
> Vibe Coding 并不是降低了技术门槛，它只是巧妙地掩盖了复杂度。它把传统属于人类的"体力劳动"以 90% 的比例削减了；但同时，它把"脑力劳动"以 300% 的程度成倍地挤压回了你的脑子里。

> [VISUAL]
> **Slide**: M1-05_The_Magic_Myth
> **Layout**: `Split`
> **Scene**: 左侧是典型的外行输入：“帮我生成一个类似淘宝的超酷炫主页”。右侧是 AI 吐出来的灾难代码图示：颜色混乱、无响应式断点、空载状态报错（被戏称为“弗兰肯斯坦的怪物”）。
> **知识节点**: `vibe-coding-human-ai-collaboration`

想象一下，你对 v0 甩出一句外行至极的 Prompt：“帮我生成一个炫酷的电商主页。”
AI 会怎么做？它是一个极度渴望讨好你的实习生，但它同时有着极差的审美和金鱼般的系统规划记忆。由于缺乏来自于你的严密规则约束，它会从它看过的上百万个开源项目里，随机抽取一些看着不错的按钮和卡片强行缝合起来交给你。乍一看五颜六色，稍微一点全部崩溃。这就是失控的 AI 副驾驶带你入坑。

> [VISUAL]
> **Slide**: M1-06_Shift_of_Labor
> **Layout**: `Chart`
> **Scene**: Vibe Coding 模式下的努力重定向图表。显示人类精力的消耗曲线：底层代码实现（暴跌），而前期的 System Design 系统设计（剧增）与后期的 QA 把控检验（剧增）。
> **知识节点**: `vibe-coding-human-ai-collaboration`

所以，我们要如何在这种巨变中活下来？
你必须要建立起一种**控制大于依赖**的审视心态。工具可以把代码这件脏活累活外包出去，但系统的品味、对于可用性底线的守护，这永远只能长在你们自己的骨头里。
为了能够向 AI 这个强大的但偶发失控的交响乐团下达精确的指挥手势，我们就必须抛弃那种诗意、模糊的自然语言。我们要用一套极度结构化的语言体系与它对话。
接下来，我们将进入第二模块：如何打造一套毫无歧义的结构化 Prompt 咒语。

---

## 模块 2：讲授(上) — Prompt 工程与跟 AI 的精确沟通法 (约 35 分钟)
<!-- BUDGET: 6300 chars | SLIDES: ≥12 | STATUS: pending -->
<!-- MATERIAL_BUDGET: prompt-engineering-ui, IDC: Speech Act Theory (J.L. Austin) -->

正如我们在上一模块结尾所说，现在我们要用一套极度结构化的语言体系与大模型对话。从绘图员变成指挥家，你需要掌握的第一门核心外语，就是结构化 Prompt 咒语。

> [VISUAL]
> **Slide**: M2-01_Haircut_Tragedy
> **Layout**: `Image`
> **Scene**: 一张极其生动、令人捧腹的理发店惨剧网络梗图。左边标着“顾客的要求：要有呼吸感、少年感、显脸小”；右边标着“理发师的最终交付：如同被狗啃过一样的精神小伙平头”。
> **知识节点**: `prompt-engineering-ui`

> [LIFE CONNECT]
> **理发店的跨服沟通悲剧**
> 想象一下你周末去理发店的经历。你在椅子上坐下，随意给出一个典型失败的 Prompt：“师傅，给我随便修修，剪个有少年感的发型，别太短。”结果四十分钟后，你看着镜子里的精神西瓜头，陷入了沉默。
> 为什么？因为“少年感”是一个极其主观、且没有任何物理定量定义的模糊意象。如果你是个懂得结构化表达的聪明人，你应该给出绝对定量且具备空间约束的指令：“第一、两边推平拉高梯队；第二、顶部保留 3 厘米基础长度；第三、刘海不规则碎剪且底线不可遮盖眉毛。”听到定量参数，任何理发师都不可能发生毁灭性降级偏差。

在屏幕里跟大语言模型沟通复杂业务逻辑和界面需求，跨服沟通的灾难率比理发店还要高一百倍。如果你试图继续用日常白话要求“生成一个质感高级的按钮”，AI 面临这种空洞输入，只能依靠底层权重发散匹配，胡拼乱凑出一坨五颜六色、充满违和元素拼接的 UI 灾难现场。

> [VISUAL]
> **Slide**: M2-02_Speech_Act_Theory
> **Layout**: `Split`
> **Scene**: 左侧是牛津大学哲学家 J.L. 奥斯汀 (J.L. Austin) 和著作《How to Do Things with Words》；右侧是对 Prompt 指令本质的哲学解构——从描述性语言升级为创造现实的行动性语言。
> **Search**: `John Langshaw Austin How to Do Things with Words Speech Act Theory`
> **知识节点**: `prompt-engineering-ui`

> [PHILOSOPHY]
> **跨学科降维：Prompt 的哲学本质是「言语行为」**
> 我们借用语言哲学的核武器级理论来重塑人机沟通的认知。英国哲学家 J.L. 奥斯汀在其巨著《如何以言行事》中提出了「言语行为理论 (Speech Act Theory)」。
> 奥斯汀指出，语言不仅用于“描述 (Describe)”客观事实，绝大多数时候，语言本身就是一种极具因果杀伤力的“行为 (Action)”，即“施事行为 (Illocutionary Act)”。当法官敲下法槌宣判“你有罪”，或神父在婚礼上宣告“结为夫妻”时，这句话在说出口的瞬间，**直接且强力地改变了物理与法理世界的现实状态**！
> 今天你们狂敲 Prompt 时也是如此。系统提示字眼绝不是在描述虚幻的图片，它本身就是一套系统建构执行法则。按下回车，AI 瞬间利用代码改变了前端生态的现实。指令如果松散无力，就会召唤出极度混乱的畸形代码世界。

怎么保证庞大规模指令不出差错？我们需要依靠铁血工业框架：**RCPVU 五层控制指令集**。

> [VISUAL]
> **Slide**: M2-03_RCPVU_Global_Framework
> **Layout**: `Triple-Column`
> **Scene**: 展示 RCPVU 系统指令体系层级结构。R (Role) / C (Context) / P (Platform) / V (Visual Style) / U (UI Components)。
> **知识节点**: `prompt-engineering-ui`

你必须要像一个极度冷静、容不得半点沙子的偏执暴君系统架构师一样，雷打不动、按部就班地从宏观世界到微观原子世界，向 AI 下达强制性纪律：

> [VISUAL]
> **Slide**: M2-04_RCPVU_RC
> **Layout**: `Image`
> **Scene**: 放大展示 RCPVU 的前两层—— Role 与 Context 指令。
> **知识节点**: `prompt-engineering-ui`

第一层，**Role（身份劫持层）**。绝不能让 AI 保持默认助理嘴脸。起手第一句必须是洗脑覆盖：“你现在是十五年硅谷大厂经验的前端重架构工程师，代码极度严谨，绝不使用内联样式”。把你面前这张白纸模型脑中的发散知识树，果决截肢，把它的注意力（Attention）死死锁定在“高保真工程代码域”的绝对禁区。你必须以极其高傲的态度，劫持其最高人格系统。

第二层，**Context（系统逻辑设定层）**。你不能光说“做个列表”，而要给商业骨架：“这是一家面临存活转化压力的 B端 SaaS 系统首屏工作台，为应对极高数据密度，空间利用率是唯一核心诉求”。没有这条纪律定调，AI 就会盲目使用奢侈的留白破坏信息架构。

> [VISUAL]
> **Slide**: M2-05_RCPVU_P
> **Layout**: `Image`
> **Scene**: 放大展示 Platform 层（技术约束）。
> **知识节点**: `prompt-engineering-ui`

第三层，**Platform（技术土壤层）**。在代码兵工厂，不能让它瞎猜技术栈：“严格全量使用 React 18 配合 Tailwind CSS V3 底座！强制依赖 Shadcn/ui 为基础组件支撑系”。如果不强制约束架构底座去要一个“弹窗”，AI 可能会用 z-index 写个绝对定位 div，不仅丢失了 ESC 快捷关闭，还缺失了 `aria-modal="true"` 的屏幕阅读器焦点陷阱保护，成了劣质炸弹。

> [VISUAL]
> **Slide**: M2-06_RCPVU_V_and_Tokens
> **Layout**: `Split`
> **Scene**: 左（❌业余指令）：清爽蓝色主按钮。右（✅工程法典）：主按钮底色锁定 primary-600(#2563EB)，圆角映射 radius-md(8px)，禁用态不透明度压至50%。
> **知识节点**: `prompt-engineering-ui`

第四层，也是决定命脉的一层，**V (Visual Style) 视觉风格纪律层**。
此时前几周的极密高保真 Design Tokens 数据法则终于派上用场！你要下令：“主操作按钮必须百分之百绑定唯一关键变量 `primary-600`，圆角 Token=radius-md(8px)！”如果不给 Tokens 映射双语对照词典（Mapping Table）去指定紫色 `brand-core-accent`，那前端没有这个类名，AI 就会笨拙地写入内联样式 `style={{color: '#8B5CF6'}}`，沦为切换暗黑模式时最刺眼的跨系统毒瘤。这层不仅需要传递意图，更是桥接设计与开发间距跨纬度巴别塔的一块核心法典神圣基石。

> [VISUAL]
> **Slide**: M2-07_RCPVU_U_Components
> **Layout**: `List`
> **Scene**: U Components 分解展示：导航头、信息阵列、控制盘。
> **知识节点**: `prompt-engineering-ui`

最后一层深潜，**U（UI Components）实体构件集结册**。
带有极度防具洁癖的框架思维去告知：“于屏幕顶域满幅铺设主导大容器；左侧内嵌挂载主标志；正区铺开标准三束产品阵列卡片瀑布流”。在这极度纯净的 U 层内，抛弃感性形容词与交互行为，输出立体具备重量的物理工程拆解点位结构图指令！

> [VISUAL]
> **Slide**: M2-08_Three_Stage_Iteration_Flow
> **Layout**: `Flow`
> **Scene**: 揭示三阶段分段迭代全景推演景：Scaffold (骨架) -> Skin (皮肤) -> Interaction (交互)。
> **知识节点**: `prompt-engineering-ui`, `book-refactoring-ui`

> [STORY TIME]
> **反面教材：一波流生成的核爆惨案**
> 有些新手妄图用极其宏大几千字的混合 Prompt 完成包含架构、状态、动画所有任务的界面生成，按下回车两分钟后看似华彩极佳，但实质是“弗兰肯斯坦的怪物”。在向投资方演示遭遇随机非预期边界连击时，系统因为状态机彻底混编断裂和极度幻觉并发引发底层崩溃。这就是没有精密分段所造成的彻底坠机死难恶果代价。

想要完美降服 AI 副驾驶，别妄图单点一波流！你必须采用如同在刀尖上做手术般的系统性**三级精密阶梯式逼近战法**：

> [VISUAL]
> **Slide**: M2-09_Iteration_Stage_1_Scaffold
> **Layout**: `Image`
> **Scene**: 骨架期：全是一片绝对死气沉沉的黑白网格辅助线。
> **知识节点**: `prompt-engineering-ui`

**第一步，死守底座建立框架 (Stage 1: Scaffold Build)。**
这阶段别谈色彩！“大容器分三列，带4:3图片占位符”。冷酷地盯住微观到全局断点缩放下的极大稳固性，地基死死立稳保证绝不溃败脱轨。

> [VISUAL]
> **Slide**: M2-10_Iteration_Stage_2_Skin
> **Layout**: `Split`
> **Scene**: 左侧是生硬灰色骨架；右侧是一场 Token 强杀覆盖执行展现血肉丰满的成品态。
> **知识节点**: `prompt-engineering-ui`

**第二步，强权注入超级品牌皮肤法典 (Stage 2: Token Skin Super-Injection)。**
待架构不破，请出霸权覆盖：“核心高光色挂靠 `primary-600`，内边距加锁安全地带 `space-4`！”骨架顷刻血肉丰满。

> [VISUAL]
> **Slide**: M2-11_Iteration_Stage_3_Interaction
> **Layout**: `Image`
> **Scene**: 光标移动至刚寂静的卡片上产生极细腻上凸位浮升，泛出阴影。
> **知识节点**: `prompt-engineering-ui`, `book-refactoring-ui`

**第三步，隐藏微交互反馈激活动态注入 (Stage 3: Advanced Vitality State)。**
也就是注入神经元级的微互动：“悬停 Hover 时卡片上浮 2px，伴生漫扩散 diffuse-shadow 光晕。”这正是《Refactoring UI》极力传承的精要准则——**先有骨架盘，再为其强行镀上具有生机的视觉血肉表现层和深层行为逻辑反馈。**

"""

with open("W09_AI原型协作结构化.md", "w", encoding="utf-8") as f:
    f.writelines(head_lines)
    f.write(middle_text + "\n")
    f.writelines(tail_lines)

print("File reconstructed successfully.")
