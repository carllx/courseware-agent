import re
import os
import glob

# Find all M*.md files
md_files = glob.glob('src/M*.md')
missing_slides = []

for file in md_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse VISUAL blocks
    visual_blocks = re.split(r'> \[VISUAL\]', content)[1:]
    for block in visual_blocks:
        slide_match = re.search(r'> \*\s*\*\*Slide\*\*:\s*`([^`]+)`', block)
        if slide_match:
            slide_id = slide_match.group(1).strip()
            # Check for Asset
            asset_match = re.search(r'> \*\s*\*\*Asset(?: 1)?\*\*:\s*!\[.*?\]\((.*?)\)', block)
            if asset_match:
                asset_path = asset_match.group(1).strip()
                # Check if file exists relative to src
                full_path = os.path.normpath(os.path.join('src', asset_path))
                if not os.path.exists(full_path):
                    missing_slides.append({'file': file, 'slide_id': slide_id, 'reason': f'Asset path not found: {asset_path}'})
            else:
                missing_slides.append({'file': file, 'slide_id': slide_id, 'reason': 'No Asset field'})

print(f"Found {len(missing_slides)} missing or non-existent assets:")
for m in missing_slides:
    print(f"- {m['file']}: {m['slide_id']} ({m['reason']})")
