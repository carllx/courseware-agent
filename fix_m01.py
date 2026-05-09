import re

filepath = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src/M01_我们为什么需要可视化？.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 替换 H3 标题
content = content.replace("### 1.1 概念溯源：信息可视化解决的是认知映射问题", "### 1.1 概念溯源：可视化直击认知映射痛点")
content = content.replace("### 1.2 视觉降熵：图形设计有效消除了数据的不确定性", "### 1.2 视觉降熵：图形设计消除数据不确定性")
content = content.replace("### 1.3 均值陷阱：盲目信任统计模型易导致决策失误", "### 1.3 均值陷阱：盲信统计模型诱发决策灾难")
content = content.replace("### 1.4 算法反噬：当商业帝国被均值蒙蔽", "### 1.4 算法反噬：商业帝国惨遭均值模型蒙蔽")

# 替换锚词
content = content.replace("那些是信息吗？", "那些是**信息**吗？")
content = content.replace("本质上是一次**有损压缩**。\n\n当你用计算公式将错综复杂的原始数据压缩为一个“平均数”或“方差”时", "本质上是一次**有损压缩**。\n\n当你用计算公式将错综复杂的原始数据**有损压缩**为一个“平均数”或“方差”时")
content = content.replace("是助推器上的橡胶 O 型环（O-ring）在罕见低温下", "是助推器上的**橡胶 O 型环（O-ring）**在罕见低温下")
content = content.replace("先驱爱德华·塔夫特（Edward Tufte）在其著作", "先驱**爱德华·塔夫特（Edward Tufte）**在其著作")
content = content.replace("降到了打破记录的 29 华氏度（零下1度）。火箭工程师", "迎来了**极寒温度**，气温降到了打破记录的 29 华氏度（零下1度）。火箭工程师")
content = content.replace("而是把数据画成一张最基础的散点图", "而是把数据画成一张最基础的**散点图**")
content = content.replace("瞬间提取两组变量的相关性", "瞬间提取**两组变量的相关性**")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("M01 Fixed!")
