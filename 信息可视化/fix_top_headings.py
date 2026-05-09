import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there is a VISUAL block before the first ###
    match = re.search(r'\n(###\s+[^\n]+)\n', content)
    if match:
        heading_pos = match.start()
        visual_match = re.search(r'> \[VISUAL\]', content)
        if visual_match:
            visual_pos = visual_match.start()
            if visual_pos < heading_pos:
                # Add an intro heading right before the first VISUAL block
                # that is above the first ###
                print(f"Adding Intro heading to {filename} at pos {visual_pos}")
                content = content[:visual_pos] + "### 0.1 课前引言\n\n" + content[visual_pos:]
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
