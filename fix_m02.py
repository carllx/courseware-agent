import re

filepath = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src/M02_信息可视化的演进脉络.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("### 2.4 图形觉醒：让数字讲故事的黄金时代", "### 2.4 图形觉醒：宏观数据开启叙事黄金期")
content = content.replace("### 2.5 极致提纯：用最少元素传达最多信息", "### 2.5 极致提纯：通用视觉消除跨国语言障碍")
content = content.replace("### 2.6 数据洪流：大数据驱动的交互式可视化", "### 2.6 数据洪流：交互图表驾驭动态大数据纪元")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("M02 Fixed!")
