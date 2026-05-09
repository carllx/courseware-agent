import re
import os

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

target_slides = [
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
    path = os.path.join(src_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    for sid in target_slides:
        match = re.search(r"> \*\s+\*\*Slide\*\*: `?" + sid + r"`?.*?\n(.*?)\n(?:> \*\s+\*\*Text\*\*|\n|###)", content, flags=re.DOTALL)
        if match:
            print(f"[{sid}] ({filename})")
            print(match.group(1).strip())
            print("---")
