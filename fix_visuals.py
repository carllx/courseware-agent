import re

file_path = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W07_Project_Design/src/M02_国际神作的避坑与反思.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'^>\s*Scene:\s*', '> **Scene**: ', content, flags=re.MULTILINE)
content = re.sub(r'^>\s*Text:\s*', '> **Text**: ', content, flags=re.MULTILINE)
content = re.sub(r'^>\s*List:\s*', '> **List**: ', content, flags=re.MULTILINE)

blocks = content.split('> [VISUAL]')
new_content = blocks[0]
for i in range(1, len(blocks)):
    block = blocks[i]
    if '**Slide**:' not in block:
        match = re.search(r'> \*\*Text\*\*: (.*?)$', block, flags=re.MULTILINE)
        slide_title = match.group(1).strip() if match else f'Slide {i}'
        new_content += '> [VISUAL]\n> **Slide**: ' + slide_title + block
    else:
        new_content += '> [VISUAL]' + block

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
