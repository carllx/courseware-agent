import os
import glob
import shutil
import re

brain_dir = "/Users/yamlam/.gemini/antigravity/brain/07eb3abd-f8f3-48f3-9578-757b433d5630"
src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W03_Product_Insights/src"
public_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W03_Product_Insights/public/slides"

mappings = {
    "slide_four_juicero": "w03-slide-04_juicero_pitch",
    "slide_five_sony": "w03-slide-05_sony_twist",
    "slide_six_walmart": "w03-slide-06_walmart",
    "slide_seven_thaler": "w03-slide-07_thaler",
    "slide_fourteen_dialogue": "w03-slide-14_dialogue",
    "slide_eighteen_alt": "w03-slide-18_alt",
    "slide_twenty_medical": "w03-slide-20_medical_social",
    "slide_twentytwo_coffee": "w03-slide-22_coffee",
    "slide_twentythree_war": "w03-slide-23_coffee_war"
}

# 1. Copy files
print("Copying files...")
for prefix, slide_id in mappings.items():
    matches = glob.glob(os.path.join(brain_dir, f"{prefix}_*.png"))
    if matches:
        source_file = sorted(matches)[-1] # get the latest
        target_file = os.path.join(public_dir, f"{slide_id}.png")
        shutil.copy2(source_file, target_file)
        print(f"Copied {os.path.basename(source_file)} to {slide_id}.png")
    else:
        print(f"Warning: No generated image found for prefix {prefix}")

# 2. Inject into markdown
print("\nInjecting into markdown...")
for filename in os.listdir(src_dir):
    if not filename.startswith("M") or not filename.endswith(".md"):
        continue
    
    filepath = os.path.join(src_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # We need to find `> [VISUAL]` blocks and process them.
    # We will use regex to find blocks and replace them if they match our SlideIDs.
    
    blocks = re.split(r'(> \[VISUAL\]\n)', content)
    new_content = blocks[0]
    
    for i in range(1, len(blocks), 2):
        header = blocks[i]
        body = blocks[i+1]
        
        # Determine where this block ends (first empty line or non-`>` line)
        lines = body.split('\n')
        block_lines = []
        rest_lines = []
        in_block = True
        
        for line in lines:
            if in_block and (line.startswith('>') or line.strip() == ''): # allow empty lines if they are between > lines? Actually the visual block shouldn't have empty lines without >
                if line.strip() == '' and not block_lines:
                    # just started body, wait it should start with >
                    rest_lines.append(line)
                    in_block = False
                    continue
                if not line.startswith('>'):
                    in_block = False
                    rest_lines.append(line)
                    continue
                block_lines.append(line)
            else:
                in_block = False
                rest_lines.append(line)
        
        block_text = '\n'.join(block_lines)
        
        # Check if it matches any of our slide IDs
        matched_slide = None
        for slide_id in mappings.values():
            if f"**Slide**: `{slide_id}`" in block_text or f"**Slide**: {slide_id}" in block_text:
                matched_slide = slide_id
                break
        
        if matched_slide:
            # We found a block that needs injection/replacement
            new_asset_line = f"> *   **Asset**: ![预览](../public/slides/{matched_slide}.png)"
            
            # Check if it already has an Asset line
            if "**Asset**:" in block_text:
                # Replace existing Asset line
                block_text = re.sub(r'> \*\s*\*\*Asset\*\*:.*', new_asset_line, block_text)
                block_text = re.sub(r'> \*\*Asset\*\*:.*', new_asset_line, block_text)
            else:
                # Inject after Layout or Slide
                if "**Layout**:" in block_text:
                    block_text = re.sub(r'(> \*\*Layout\*\*:.*)', r'\1\n' + new_asset_line, block_text)
                else:
                    block_text = re.sub(r'(> \*\*Slide\*\*:.*)', r'\1\n' + new_asset_line, block_text)
                    
            print(f"Injected/Updated {matched_slide} in {filename}")
        
        new_content += header + block_text + ('\n' + '\n'.join(rest_lines) if rest_lines else '')
        
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

print("Injection complete.")
