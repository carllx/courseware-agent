import os
import re
import glob
import json

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W03_Product_Insights/src"
public_slides_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W03_Product_Insights/public/slides"

def parse_markdown():
    missing_visuals = []
    
    for filename in sorted(os.listdir(src_dir)):
        if not filename.startswith("M") or not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(src_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        i = 0
        while i < len(lines):
            line = lines[i]
            if "> [VISUAL]" in line:
                block_lines = []
                start_i = i
                while i < len(lines) and lines[i].startswith(">"):
                    block_lines.append(lines[i].strip())
                    i += 1
                
                block_content = "\n".join(block_lines)
                
                # Exclusions
                if "no_ai_flag: true" in block_content or \
                   "[TEXTBOOK-REF]" in block_content or \
                   "Source**: Textbook" in block_content or \
                   "**Source**: Textbook" in block_content:
                    continue
                
                # Extract fields
                slide_match = re.search(r'\*\*Slide\*\*: `?(w\d+-slide-[a-zA-Z0-9_]+)`?', block_content)
                if not slide_match:
                    # try without strict format
                    slide_match = re.search(r'\*\*Slide\*\*: `?([^\n`]+)`?', block_content)
                
                slide_id = slide_match.group(1).strip() if slide_match else None
                
                scene_match = re.search(r'\*\*Scene\*\*: (.*)', block_content)
                scene = scene_match.group(1).strip() if scene_match else ""
                
                text_match = re.search(r'\*\*Text\*\*: (.*)', block_content)
                text = text_match.group(1).strip() if text_match else ""
                
                asset_match = re.search(r'\*\*Asset\*\*: !\[.*?\]\((.*?)\)', block_content)
                asset_path = asset_match.group(1).strip() if asset_match else ""
                
                if not slide_id:
                    print(f"Warning: No SlideID found in block in {filename}:\n{block_content}\n")
                    continue
                
                # Check physical existence
                pattern = os.path.join(public_slides_dir, f"{slide_id}.*")
                matching_files = glob.glob(pattern)
                
                physical_exists = False
                correct_asset = False
                
                for pf in matching_files:
                    ext = os.path.splitext(pf)[1].lower()
                    if ext in ['.png', '.jpg', '.jpeg', '.webp']:
                        physical_exists = True
                        expected_path = f"../public/slides/{os.path.basename(pf)}"
                        if expected_path in asset_path:
                            correct_asset = True
                        break
                        
                if not (physical_exists and correct_asset):
                    missing_visuals.append({
                        "file": filename,
                        "slide_id": slide_id,
                        "scene": scene,
                        "text": text,
                        "has_physical": physical_exists,
                        "has_asset_tag": bool(asset_match)
                    })
            else:
                i += 1
                
    return missing_visuals

if __name__ == "__main__":
    gaps = parse_markdown()
    print(json.dumps(gaps, ensure_ascii=False, indent=2))
