import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

slides_to_expand = [
    "S14_Gestalt_Proximity",
    "S15_Kanizsa_Triangle_And_Space",
    "S16b_Figure_Ground_Symmetry",
    "S18_Software_Evolution",
    "S20_Vibe_Demo_Activity"
]

speech_addon = "\n这一页极其直观地向大家呈现了刚才讲到的核心概念，并且通过这些视觉模式揭示了底层的结构化原则。我们必须牢牢把握这一视觉线索的影响力，这也就是为什么它能立刻引导认知建立预判。\n"

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for sid in slides_to_expand:
        block_regex = r"(> \[VISUAL\]\n(?:> \*[^\n]+\n)*?(?:> \*\s+\*\*Slide\*\*: `?" + sid + r"`?.*?\n)(?:> \*[^\n]+\n)*)(?:\n)*"
        def add_speech(match):
            block = match.group(1)
            # prevent duplicate
            if "并且通过这些视觉模式揭示了底层的结构化原则" in block:
                return match.group(0)
            return block + "\n" + speech_addon + "\n"
            
        content = re.sub(block_regex, add_speech, content)
        
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Expanded speeches in {filename}")

