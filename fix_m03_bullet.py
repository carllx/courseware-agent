import re

filepath = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src/M03_视觉系统_你的认知外接显卡.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("第一行第一列，第一行第二列", "第1行第1列，第1行第2列")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("M03 Bullet Fix applied!")
