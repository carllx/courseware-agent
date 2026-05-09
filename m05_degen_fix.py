import re

with open('/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W02_Design_Principles/src/M05_认知审计实验室__三阶段对比实验.md', 'r') as f:
    content = f.read()

replacements = {
    "极其不适的": "不适的",
    "极其具体的": "具体的",
    "极度的疲劳状态": "高度的疲劳状态",
    "彻底遮挡": "严重遮挡",
    "毫无意义的三维阴影": "多余的三维阴影",
    "不可饶恕的错误": "严重的错误",
    "彻底拆解": "拆解",
    "极端受限的": "受限的",
    "绝对不允许": "不允许",
    "毫无意义的雷达图": "不恰当的雷达图"
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open('/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W02_Design_Principles/src/M05_认知审计实验室__三阶段对比实验.md', 'w') as f:
    f.write(content)

print("DEGEN cleanup done")
