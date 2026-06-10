import re

file_path = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W07_Project_Design/src/M02_国际神作的避坑与反思.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

blocks = content.split('> [VISUAL]')
new_content = blocks[0]
for i in range(1, len(blocks)):
    block = blocks[i]
    lines = block.split('\n')
    asset_counter = 1
    new_lines = []
    for line in lines:
        if re.match(r'^>\s*\*\s*!\[', line):
            if asset_counter == 1:
                line = re.sub(r'^>\s*\*\s*', '> **Asset**: ', line)
            else:
                line = re.sub(r'^>\s*\*\s*', f'> **Asset {asset_counter}**: ', line)
            asset_counter += 1
        new_lines.append(line)
    new_content += '> [VISUAL]' + '\n'.join(new_lines)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
