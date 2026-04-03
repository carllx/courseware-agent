import os
import glob
import re
import shutil

src_dir = '/Users/yamlam/.gemini/antigravity/brain/e6d92c4e-d6b7-42dc-9a50-658bede65a46'
dst_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/visuals/assets/W06_容器工程化基础映射'
base_asset_path = 'visuals/assets/W06_容器工程化基础映射'
os.makedirs(dst_dir, exist_ok=True)

# 1. Move and rename images
images = glob.glob(os.path.join(src_dir, 'w06_*.png'))
for img in images:
    name = os.path.basename(img)
    match = re.search(r'w06_(m\d+_\w+)_', name)
    if match:
        slide_id = match.group(1).replace('_', '-').upper() # M1-01, M3-01B
        dst_path = os.path.join(dst_dir, f"{slide_id}.png")
        shutil.move(img, dst_path)
        print(f"Moved {name} to {slide_id}.png")

# 2. Update markdown
md_file = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/scripts/W06_容器工程化基础映射.md'
with open(md_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_visual = False
current_slide = None
updated_count = 0

i = 0
while i < len(lines):
    line = lines[i]
    if '> [VISUAL]' in line:
        in_visual = True
        current_slide = None
        new_lines.append(line)
        i += 1
        continue
    
    if in_visual:
        # Match Slide ID
        slide_match = re.match(r'> \*\*Slide\*\*: (M\d+-\w+)', line)
        if slide_match:
            current_slide = slide_match.group(1)
            
        # If we hit an existing Asset line, we'll replace it entirely later, skip it here if we want?
        # Better: let's track the end of the block. A block ends with an empty line or a non-quote line.
        if not line.strip().startswith('>'):
            if current_slide:
                # Add Asset line before the empty line
                asset_line = f'> **Asset**: {base_asset_path}/{current_slide}.png\n'
                # Check if previous lines already have an Asset
                has_asset = False
                for j in range(len(new_lines) - 1, -1, -1):
                    if '> [VISUAL]' in new_lines[j]:
                        break
                    if '> **Asset**:' in new_lines[j]:
                        new_lines[j] = asset_line # Replace
                        has_asset = True
                        break
                if not has_asset:
                    new_lines.append(asset_line)
                updated_count += 1
            in_visual = False
            current_slide = None

    new_lines.append(line)
    i += 1

with open(md_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Updated {updated_count} VISUAL blocks in the markdown file.")

