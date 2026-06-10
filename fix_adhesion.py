import re

file_path = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W07_Project_Design/src/M02_国际神作的避坑与反思.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'^>\s*$', '', content, flags=re.MULTILINE)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
