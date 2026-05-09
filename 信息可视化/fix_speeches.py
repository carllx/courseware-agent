import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

slides_to_expand = [
    "S13_Gestalt_Intro",
    "S14_Gestalt_Proximity",
    "S15_Kanizsa_Triangle_And_Space",
    "S16b_Figure_Ground_Symmetry",
    "S17_Design_Space",
    "S18_Software_Evolution",
    "S20_Vibe_Demo_Activity"
]

speech_addon = "\n这一页极其直观地向大家呈现了刚才讲到的核心概念。请大家在脑海里牢牢建立起这套全新的视觉心智框架模型。这是我们后续去解构一切复杂数字隐喻、进行高阶数据抽象表征时所必须依赖的底层基石，绝对不能含糊处理。\n"

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
            # Add the block and then the extra speech beneath it.
            # Make sure not to duplicate if it's already there
            if "这一页极其直观" not in content:
                return block + "\n" + speech_addon + "\n"
            return block + "\n\n"
            
        content = re.sub(block_regex, add_speech, content)
        
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Expanded speeches in {filename}")

