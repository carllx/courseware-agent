import os

file_path = '/Users/yamlam/Downloads/myskills/.agent/skills/d3/references/d3-scale.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by '## ' but keep the delimiter
parts = content.split('\n## ')

# The first part is everything before the first '## '
header = parts[0]
blocks = parts[1:]

scale_blocks = []
chromatic_blocks = []

for block in blocks:
    if 'https://d3js.org/d3-scale-chromatic' in block:
        chromatic_blocks.append('## ' + block)
    else:
        scale_blocks.append('## ' + block)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(header + '\n' + '\n'.join(scale_blocks))

chromatic_path = '/Users/yamlam/Downloads/myskills/.agent/skills/d3/references/d3-scale-chromatic.md'
with open(chromatic_path, 'w', encoding='utf-8') as f:
    f.write('# D3 - Scale Chromatic\n\n' + '\n'.join(chromatic_blocks))

print("Successfully decoupled d3-scale-chromatic.")
