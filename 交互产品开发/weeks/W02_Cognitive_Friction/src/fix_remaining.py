import re

def insert_visual(filepath, search_str, visual_block):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if search_str in content:
        # Check if already inserted to prevent duplication
        if visual_block in content:
            print(f"Already fixed in {filepath}")
            return
        content = content.replace(search_str, visual_block + "\n\n" + search_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed in {filepath}")
    else:
        print(f"NOT FOUND in {filepath}")

# M03
v7 = """> [VISUAL]
> **Slide**: w02-slide-18_1
> **Layout**: `Center`
> **Scene**: 家用插座的错误隐喻：一个抽象的墙壁插座孔里涌出水流的画面，展示直觉认知与物理真实的偏差。
> **List**: 心理直觉：电力如水流 | 物理真实：闭合回路
> **Text**: 错误但有用的心理模型"""
insert_visual('M03_三种模型的战争.md', '再比如**家用插座模型**。', v7)

v8 = """> [VISUAL]
> **Slide**: w02-slide-20_1
> **Layout**: `Split`
> **Scene**: 两股力量的拉扯。左侧是冰冷的底层代码库（机器逻辑），右侧是直观的照片时间流（人类心理），设计师的手正将表现层界面用力推向右侧。
> **List**: 机器的真理：哈希路径 | 人类的直觉：时间与地点回忆
> **Text**: 体验设计的最高使命"""
insert_visual('M03_三种模型的战争.md', '**而在这个时代，最顶尖的体验设计，其唯一使命就是将表现模型死命地推向用户心理模型的那一端。**', v8)

# M04
v9 = """> [VISUAL]
> **Slide**: w02-slide-23_1
> **Layout**: `Center`
> **Scene**: 软盘图标的演变：从真实的物理软盘（1990s）渐渐模糊、失去细节，变成一个纯粹的抽象带缺口方块（现代UI）。
> **List**: 原型存在的隐喻 | 原型灭绝后的符号遗迹化
> **Text**: Skeuomorph decay：隐喻的遗迹化"""
insert_visual('M04_隐喻的双刃剑.md', '对 Z 世代来说，那根本不是什么隐喻了', v9)

v10 = """> [VISUAL]
> **Slide**: w02-slide-26_1
> **Layout**: `Center`
> **Scene**: 一张被打乱的扑克牌墙：原本按顺序排列的卡片突然被一只代表“算法”的无形之手洗牌重组。
> **List**: 物理世界的连续性 | 算法干预后的逻辑撕裂
> **Text**: 从认知脚手架到认知陷阱"""
insert_visual('M04_隐喻的双刃剑.md', '这种"非线性卡片"的代价是显而易见的：你失去了"我刷到哪', v10)

# M05
v11 = """> [VISUAL]
> **Slide**: w02-slide-28_1
> **Layout**: `Comparison`
> **Scene**: 对比画面。左侧是用户在两个应用间来回切换背诵验证码的繁琐操作；右侧是系统级悬浮的“一键填充”胶囊按钮。
> **List**: 强迫回忆：极易出错的背诵 | 识别提取：系统接管识别负担
> **Text**: 把凭空提取换成看见即选择"""
insert_visual('M05_记忆负荷与认知过载.md', '请看大屏幕上的左右对比：左侧是用户从短信弹窗里凭空背诵一', v11)

v12 = """> [VISUAL]
> **Slide**: w02-slide-31_1
> **Layout**: `Center`
> **Scene**: 外部认知的隐喻。人类的大脑连接着几根虚拟导线，导线连接着外部的纸笔便签、计算器屏幕、以及地图导航图标。
> **List**: 外部化：释放工作记忆 | 计算卸载：外包计算任务 | 认知追踪：降低标记负担
> **Text**: 借用工具扩展大脑的能力"""
insert_visual('M05_记忆负荷与认知过载.md', '讲到这里，你可能会觉得人类的大脑太弱了——注意力窄、记忆', v12)

v13 = """> [VISUAL]
> **Slide**: w02-slide-33_1
> **Layout**: `Center`
> **Scene**: 侦探放大镜与手术刀组合的图形。背景隐约浮现四个图标：鸿沟、心理模型、隐喻、认知负荷。
> **List**: 猎手寻踪：捕捉日常摩擦 | 诊断解构：四把理论手术刀
> **Text**: 将理论变为剖析现实的手术刀"""
insert_visual('M05_记忆负荷与认知过载.md', '好。你们刚才吸收了大量抽象的认知理论。现在，是时候把这些', v13)

v14 = """> [VISUAL]
> **Slide**: w02-slide-35_1
> **Layout**: `Grid`
> **Scene**: 四块完整的核心拼图严丝合缝地拼接在一起。四块拼图分别带有微型标志：漏斗（认知限制）、深渊（鸿沟）、三齿轮（模型冲突）、旧磁带（隐喻老化）。
> **List**: 漏斗与便签桌 | 执行与评估鸿沟 | 三模型大战 | 老化的双刃剑
> **Text**: 破防心智摩擦的四大元凶"""
insert_visual('M05_记忆负荷与认知过载.md', '由于时间关系，我们的系统学习就到这里。在过去两小时里，我', v14)

