import re
import os

filepath = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W04_AI_D3_Basics/src/M01_空间_最昂贵的视觉通道.md"
base_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W04_AI_D3_Basics/src"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'(\>?\s*\[VISUAL\].*?)(?=\n\n|\n\>?\s*\[|\Z)', re.DOTALL)
matches = pattern.finditer(content)

to_generate = []
for match in matches:
    block = match.group(1)
    asset_match = re.search(r'\*\s+\*\*Asset\*\*(?: \d+)?:\s*(.*?)$', block, re.MULTILINE)
    
    if asset_match:
        asset_str = asset_match.group(1).strip()
        path_match = re.search(r'\[.*?\]\((.*?)\)', asset_str)
        if path_match:
            asset_path = path_match.group(1)
        else:
            asset_path = asset_str.strip('`* ')
        
        full_path = os.path.normpath(os.path.join(base_dir, asset_path))
        
        if not os.path.exists(full_path):
            # Missing! We need to generate it
            scene_match = re.search(r'\*\s+\*\*Scene\*\*:\s*(.*?)$', block, re.MULTILINE)
            scene = scene_match.group(1).strip() if scene_match else ""
            
            layout_match = re.search(r'\*\s+\*\*Layout\*\*:\s*(.*?)$', block, re.MULTILINE)
            layout = layout_match.group(1).strip().strip('`* ') if layout_match else "Image"
            
            # Extract keywords or text
            text_match = re.search(r'\*\s+\*\*Text\*\*:\s*(.*?)$', block, re.MULTILINE)
            title_match = re.search(r'\*\s+\*\*Title\*\*:\s*(.*?)$', block, re.MULTILINE)
            text = text_match.group(1).strip() if text_match else (title_match.group(1).strip() if title_match else "")
            
            to_generate.append({
                'path': full_path,
                'rel_path': asset_path,
                'scene': scene,
                'layout': layout,
                'text': text
            })

print(f"Total missing assets to generate: {len(to_generate)}")
for idx, task in enumerate(to_generate):
    print(f"Missing {idx}: {task['rel_path']}")
    print(f"Layout: {task['layout']}")
    print(f"Scene: {task['scene']}")
    print(f"Text/Title: {task['text']}")
    print("---")
