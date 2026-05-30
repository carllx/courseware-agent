import re
import shutil
import os

source_file = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017/chapter_03_Technology_Fundamentals.md'
source_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017/images'
dest_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W04_AI_D3_Basics/public/textbook'

os.makedirs(dest_dir, exist_ok=True)

with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

figures = []
for i, line in enumerate(lines):
    img_match = re.search(r'src="images/([^"]+)"', line)
    if img_match:
        hash_name = img_match.group(1)
        # Look ahead for caption
        caption = "Unknown"
        fig_num = f"Fig3.{len(figures)+1}"
        for j in range(i, min(i+5, len(lines))):
            cap_match = re.search(r'Figure 3-(\d+)\.?\s*(?:</span>)?([^<]*)', lines[j])
            if cap_match:
                fig_num = f"Fig3.{cap_match.group(1)}"
                caption = cap_match.group(2).strip()
                break
        
        semantic_name = f"{fig_num}_{caption.replace(' ', '_')[:30].replace('/', '_')}.png"
        shutil.copy(os.path.join(source_dir, hash_name), os.path.join(dest_dir, semantic_name))
        figures.append((fig_num, caption, hash_name, i+1, semantic_name))

for fig in figures:
    print(f"| {fig[0]} | {fig[1]} | `images/{hash_name[:8]}...jpg` (L{fig[3]}) | ✅ `public/textbook/{fig[4]}` |")
