import os
import re
import json

src_dir = "."
public_slides_dir = "../public/slides"
results = []

for file in sorted(os.listdir(src_dir)):
    if file.startswith("M") and file.endswith(".md"):
        path = os.path.join(src_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        blocks = re.findall(r'>\s*\[VISUAL\].*?(?=\n(?:[^>]|$))', content, re.DOTALL)
        for block in blocks:
            asset_match = re.search(r'\*\s*\*\*Asset(?: \d+)?\*\*:.*?\]\((.*?)\)', block)
            scene_match = re.search(r'\*\s*\*\*Scene\*\*:\s*(.*)', block)
            slide_match = re.search(r'\*\s*\*\*Slide\*\*:\s*`(.*?)`', block)
            
            asset_path = ""
            if asset_match:
                asset_path = asset_match.group(1).strip()
                
            basename = os.path.basename(asset_path) if asset_path else ""
            full_path = os.path.join(public_slides_dir, basename) if basename else ""
            
            is_missing = not os.path.exists(full_path) if full_path else True
            is_small = False
            
            if not is_missing and full_path:
                size = os.path.getsize(full_path)
                if size < 15 * 1024:
                    is_small = True
            
            if is_missing or is_small:
                scene = scene_match.group(1).strip() if scene_match else ""
                slide = slide_match.group(1).strip() if slide_match else "Unknown"
                results.append({
                    "file": file,
                    "slide": slide,
                    "asset": basename,
                    "is_missing": is_missing,
                    "is_small": is_small,
                    "scene": scene,
                    "block": block.strip()
                })

print(json.dumps(results, indent=2, ensure_ascii=False))
