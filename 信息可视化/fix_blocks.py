import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Swap visual blocks that are immediately preceding a ### heading
    # A block is defined as a sequence of lines starting with `>` 
    # optionally followed by blank lines and then a `###` heading.
    pattern = re.compile(r'((?:> [^\n]*\n)+(?:\n)*(?:> [^\n]*\n)*)(###[^\n]+)\n')
    
    # Actually let's just find any `> [...]` blocks that are right above `### `
    def replacer(match):
        block = match.group(1).rstrip() + "\n"
        heading = match.group(2)
        print(f"Swapping {heading} with block")
        return f"{heading}\n\n{block}\n"
        
    for _ in range(3): # repeat to catch multiple blocks
        content = re.sub(r'((?:> [^\n]*\n\s*)+)(###[^\n]+)\n', replacer, content)

    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

