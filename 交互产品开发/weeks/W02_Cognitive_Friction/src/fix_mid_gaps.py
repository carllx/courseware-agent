import os

def replace_exact(filepath, old_str, new_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {old_str[:15]} in {filepath}")
    else:
        print(f"NOT FOUND {old_str[:15]} in {filepath}")

# M02 Chunk 1
# Split before **下半圈——从屏幕到脑——属于"评估"侧**
replace_exact('M02_意图与反馈的断裂.md', 
'**下半圈——从屏幕到脑——属于"评估"侧**。', 
"""> [VISUAL]
> **Slide**: w02-slide-08_1
> **Layout**: `Center`
> **Scene**: 评估侧的放大图：屏幕闪过绿光，人的大脑正在紧张地解释反馈信号。
> **List**: 感知 | 解释 | 评估
> **Text**: 评估侧：从屏幕到大脑的反馈循环

**下半圈——从屏幕到脑——属于"评估"侧**。""")

# M02 Chunk 8
# Split before **信号标识**
replace_exact('M02_意图与反馈的断裂.md', 
'**信号标识**（Signifier）', 
"""> [VISUAL]
> **Slide**: w02-slide-09f_1
> **Layout**: `Center`
> **Scene**: 现实中的信号标识：一扇纯玻璃门贴着巨大的“推”字。
> **List**: 消除猜测 | 明确的语义指示
> **Text**: 信号标识：不仅可操作，更知道怎么操作

**信号标识**（Signifier）""")

# M02 Chunk 19
# Split before 这种方案背后的设计原则叫做**宽恕式设计（Forgiving Design）**
replace_exact('M02_意图与反馈的断裂.md', 
'这种方案背后的设计原则叫做**宽恕式设计（Forgiving Design）**', 
"""> [VISUAL]
> **Slide**: w02-slide-12_2
> **Layout**: `Center`
> **Scene**: 一张巨大的安全网接住了掉落的用户，象征撤销功能的兜底保护。
> **List**: 消除恐惧 | 可逆操作 | 建设性信任
> **Text**: 宽恕式设计：兜底而非恐吓

这种方案背后的设计原则叫做**宽恕式设计（Forgiving Design）**""")


# M03 Chunk 9
# Split before 但建立在日常物理经验上的模型
replace_exact('M03_三种模型的战争.md', 
'但建立在日常物理经验上的模型，在遭遇数字空间时', 
"""> [VISUAL]
> **Slide**: w02-slide-18_2
> **Layout**: `Center`
> **Scene**: 一个旧式的打字机键盘与现代的平滑玻璃触摸屏并置，展现物理习惯在数字时代的错位。
> **List**: 路径依赖 | 物理习惯的阻力
> **Text**: 从物理经验到数字空间的错位

但建立在日常物理经验上的模型，在遭遇数字空间时""")


# M03 Chunk 18
# Split before 在这里，你不需要发动慢思考去"寻找特定文件"
replace_exact('M03_三种模型的战争.md', 
'在这里，你不需要发动慢思考去"寻找特定文件"', 
"""> [VISUAL]
> **Slide**: w02-slide-20_2
> **Layout**: `Center`
> **Scene**: 用户正在微笑着滑动时间轴上充满回忆的照片墙，背后是被隐藏的复杂服务器矩阵。
> **List**: 浏览回忆 vs 寻找文件 | 直觉 vs 逻辑
> **Text**: 用时间尺度覆盖机器尺度

在这里，你不需要发动慢思考去"寻找特定文件" """)


# M04 Chunk 6
# Split before 更高级的死亡方式是——**概念本身被数字原生协议击杀**。
replace_exact('M04_隐喻的双刃剑.md', 
'更高级的死亡方式是——**概念本身被数字原生协议击杀**。', 
"""> [VISUAL]
> **Slide**: w02-slide-23_2
> **Layout**: `Center`
> **Scene**: 一个“保存”按钮被云端自动同步的闪电图标所取代，隐喻彻底死亡并被原生协议接管。
> **List**: 概念死亡 | 数字原生协议接管
> **Text**: 无摩擦的数字原生范式

更高级的死亡方式是——**概念本身被数字原生协议击杀**。""")


# M04 Chunk 21
# Split before 把这个观察落回今天的核心结论
replace_exact('M04_隐喻的双刃剑.md', 
'把这个观察落回今天的核心结论：', 
"""> [VISUAL]
> **Slide**: w02-slide-26_2
> **Layout**: `Center`
> **Scene**: 隐喻陷阱的示意图。用户脚下原本坚实的阶梯突然变成了由算法控制的不稳定踏板。
> **List**: 物理规律被篡改 | 隐蔽的认知偏差
> **Text**: 隐蔽的算法背叛

把这个观察落回今天的核心结论：""")

# M05 Chunk 10
# Split before ### 5.1 识别法则
replace_exact('M05_记忆负荷与认知过载.md', 
'### 5.1 识别法则：将记忆负担卸载给系统识别', 
"""> [VISUAL]
> **Slide**: w02-slide-28_2
> **Layout**: `Center`
> **Scene**: 一个人脑负重前行，系统化作机械臂接过了大脑身上的重担。
> **List**: 回想的痛楚 | 识别的轻盈
> **Text**: 核心机制：识别法则

### 5.1 识别法则：将记忆负担卸载给系统识别""")

# M05 Chunk 15
# Split before 教材指出了外部认知的三种基本形式
replace_exact('M05_记忆负荷与认知过载.md', 
'教材指出了外部认知的三种基本形式。', 
"""> [VISUAL]
> **Slide**: w02-slide-31_2
> **Layout**: `Flow`
> **Scene**: 外部认知的流转过程，从大脑内部的模糊想法，转变为便签上的文字，再到电子屏幕上的智能导航。
> **List**: 外部化 | 计算卸载 | 认知追踪
> **Text**: 外部认知的核心路径

教材指出了外部认知的三种基本形式。""")

# M05 Chunk 21
# Split before **第二阶段 · 诊断解构（15 min）**
replace_exact('M05_记忆负荷与认知过载.md', 
'**第二阶段 · 诊断解构（15 min）**', 
"""> [VISUAL]
> **Slide**: w02-slide-33_2
> **Layout**: `Center`
> **Scene**: 显微镜下的解剖图，隐喻着深入分析界面的底层结构与交互断层。
> **List**: 执行鸿沟 vs 评估鸿沟 | 表现模型 vs 实现模型
> **Text**: 用四把钥匙精准开锁

**第二阶段 · 诊断解构（15 min）**""")

# M05 Chunk 25
# Split before **第三块拼图**：Alan Cooper 的三模型大战
replace_exact('M05_记忆负荷与认知过载.md', 
'**第三块拼图**：Alan Cooper 的三模型大战。', 
"""> [VISUAL]
> **Slide**: w02-slide-35_2
> **Layout**: `Center`
> **Scene**: 三个齿轮疯狂对冲，代表三种模型间的激烈战争，火花四溅。
> **List**: 实现模型：机器真理 | 心理模型：用户朴素直觉 | 表现模型：界面伪装
> **Text**: 模型大战：弥合认知错位

**第三块拼图**：Alan Cooper 的三模型大战。""")

