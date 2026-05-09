import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the first ### heading
    match = re.search(r'\n(###\s+[^\n]+)\n', content)
    if match:
        heading = match.group(1)
        # Find the first VISUAL block
        visual_match = re.search(r'(> \[VISUAL\].*?> \*\s+\*\*Asset\*\*:[^\n]+\n)', content, flags=re.DOTALL)
        if visual_match:
            visual_pos = visual_match.start()
            heading_pos = match.start()
            if heading_pos > visual_pos:
                print(f"File {filename}: Heading is below first Visual. Attempting to swap or move...")
                # We can move the heading to right after the BUDGET line or TEACHING MOMENT
                # Let's see if we can do this systematically or just prune the Scene
                
