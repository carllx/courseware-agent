import re
import sys
from pathlib import Path

src_dir = Path("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src")
target_slides = ["S00d3_Vibe_Prompt_Reality", "S07_Ancient_Recordings", "S09_Data_Graphics_Nightingale", "S10_Big_Data_Interaction", "S16_New_Gestalt_Intro", "S16a_CommonRegion", "S16b_Connectedness", "S18b_Workflow_Comparison", "S21ba_GUI_Pain", "S21bb_Agent_Architecture"]

for p in src_dir.glob("*.md"):
    text = p.read_text('utf-8')
    # Find all blocks starting with > [VISUAL] until the next double newline that isn't part of the block
    blocks = re.findall(r'> \[VISUAL\].*?(?=\n(?:[^>]|$))', text, re.DOTALL)
    for block in blocks:
        for t in target_slides:
            if t in block:
                print(f"=== {t} ===")
                print(block.strip())
                print()
