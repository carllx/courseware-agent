import re
import os

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

slides = [
    "S07_Ancient_Recordings",
    "S09_Data_Graphics_Nightingale",
    "S10_Big_Data_Interaction",
    "S16_New_Gestalt_Intro",
    "S16a_CommonRegion",
    "S16b_Connectedness",
    "S18b_Workflow_Comparison",
    "S21ba_GUI_Pain",
    "S21bb_Agent_Architecture"
]

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    filepath = os.path.join(src_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    modified = False

    for sid in slides:
        pattern = r"(> \*\s+\*\*Slide\*\*: `" + sid + r"`.*?\n(?:> \*\s+.*?\n)*)"
        
        def repl(match):
            block = match.group(1)
            # Check if Asset already exists
            if "**Asset**:" in block or "**Asset 1**:" in block:
                return block
            # Add Asset right after Slide by default, or just append it to the block
            # Let's append to the end of the metadata block
            new_asset = f"> *   **Asset**: ![预览](../public/slides/{sid}.png)\n"
            return block + new_asset

        new_content = re.sub(pattern, repl, content)
        if new_content != content:
            content = new_content
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")

