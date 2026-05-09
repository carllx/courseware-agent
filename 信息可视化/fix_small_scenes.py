import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

slides_to_micro_prune = {
    "S14_Gestalt_Proximity": "示例。",
    "S15_Kanizsa_Triangle_And_Space": "留白。",
    "S16b_Figure_Ground_Symmetry": "图底。",
    "S18_Software_Evolution": "演变。",
    "S16_Gestalt_Continuity": "连续。" # if any
}

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for sid, micro_scene in slides_to_micro_prune.items():
        block_regex = r"(> \[VISUAL\]\n(?:> \*[^\n]+\n)*?(?:> \*\s+\*\*Slide\*\*: `?" + sid + r"`?.*?\n)(?:> \*[^\n]+\n)*)"
        def micro_prune_scene(match):
            block = match.group(0)
            return re.sub(r"(> \*\s+\*\*Scene\*\*:\s*)([^\n]+)\n", r"\g<1>" + micro_scene + "\n", block)
            
        content = re.sub(block_regex, micro_prune_scene, content)
        
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Micro-pruned scenes in {filename}")

