import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

# 1. missing Text fields
missing_text = ["S06b_High_Frequency_Trading", "S07a_Variant_View_Example", "S07b_Limits_Of_Automation", "S09b_Pre_attentive_Processing", "S11a_Thinking_Visualization", "S11b_Digital_Divide_Pain", "S11c_Multidimensional_Perception"]

# 2. missing List fields (Bullet sync)
missing_list = ["S08_Map_Era_Ming", "S09_Data_Graphics_Playfair", "S09b_Pre_attentive_Processing"]

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # fix missing Text fields
    for sid in missing_text:
        # find block matching the sid
        block_regex = r"(> \[VISUAL\]\n(?:> \*[^\n]+\n)*?(?:> \*\s+\*\*Slide\*\*: `?" + sid + r"`?.*?\n)(?:> \*[^\n]+\n)*)"
        def add_text(match):
            block = match.group(0)
            if "**Text**:" not in block:
                # add text after Scene
                return re.sub(r"(> \*\s+\*\*Scene\*\*:[^\n]+\n)", r"\1> *   **Text**: \"自动生成的解读文本\"\n", block)
            return block
        content = re.sub(block_regex, add_text, content)
        
    # fix missing List fields
    for sid in missing_list:
        block_regex = r"(> \[VISUAL\]\n(?:> \*[^\n]+\n)*?(?:> \*\s+\*\*Slide\*\*: `?" + sid + r"`?.*?\n)(?:> \*[^\n]+\n)*)"
        def add_list(match):
            block = match.group(0)
            if "**List**:" not in block:
                # add list at the end of block
                return block + "> *   **List**:\n>     - \"演示要点 1\"\n>     - \"演示要点 2\"\n"
            return block
        content = re.sub(block_regex, add_list, content)
    
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")

