import re

with open("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Visualization Analysis & Design -- Tamara Munzner -- 2014/chapter_06_Chapter_2.md", "r") as f:
    text = f.read()

for match in re.finditer(r"!\[.*?\]\((images/.*?\.jpg)\)", text):
    img = match.group(1)
    # Find surrounding context
    start = max(0, match.start() - 100)
    end = min(len(text), match.end() + 100)
    print(img)
    print(text[start:end].replace('\n', ' '))
    print('-'*40)
