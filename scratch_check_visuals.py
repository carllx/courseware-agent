import os
import json
import re

base_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W02_Design_Principles"
src_dir = os.path.join(base_dir, "src")
slides_dir = os.path.join(base_dir, "public", "slides")

unready_assets = []

for filename in sorted(os.listdir(src_dir)):
    if not filename.endswith('.md') or not filename.startswith('M'):
        continue
    filepath = os.path.join(src_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_visual = False
    current_visual_lines = []
    
    for line in lines:
        if '> [VISUAL]' in line:
            in_visual = True
            current_visual_lines = []
            continue
            
        if in_visual:
            # Continue reading if the line starts with > or is just whitespace.
            # Usually blockquotes are contiguous. 
            if line.strip() == '' or line.strip() == '>':
                in_visual = False
            elif not line.lstrip().startswith('>'):
                in_visual = False
                
            if in_visual:
                current_visual_lines.append(line.strip().lstrip('>').strip())
                
        if not in_visual and current_visual_lines:
            # Process current_visual_lines
            scene_desc = ""
            img_name = None
            for v_line in current_visual_lines:
                if '**Scene**:' in v_line:
                    scene_desc = v_line.split('**Scene**:', 1)[1].strip()
                elif '**Asset**:' in v_line:
                    img_match = re.search(r'!\[.*?\]\((.*?)\)', v_line)
                    if img_match:
                        img_path_raw = img_match.group(1)
                        img_name = os.path.basename(img_path_raw)
                elif '**Slide**:' in v_line and not img_name:
                    slide_name = v_line.split('**Slide**:', 1)[1].strip().strip('`')
                    img_name = slide_name + ".png"
                    
            if img_name:
                is_ready = False
                size_kb = 0
                full_img_path = os.path.join(slides_dir, img_name)
                if os.path.exists(full_img_path):
                    size_kb = os.path.getsize(full_img_path) / 1024
                    if size_kb >= 15:
                        is_ready = True
                else:
                    for ext in ['.jpg', '.webp', '.jpeg']:
                        alt_path = os.path.join(slides_dir, img_name.rsplit('.', 1)[0] + ext)
                        if os.path.exists(alt_path):
                            size_kb = os.path.getsize(alt_path) / 1024
                            full_img_path = alt_path
                            img_name = os.path.basename(alt_path)
                            if size_kb >= 15:
                                is_ready = True
                            break
                if not is_ready:
                    unready_assets.append({
                        'file': filename,
                        'scene_desc': scene_desc,
                        'img_name': img_name,
                        'size_kb': round(size_kb, 2) if os.path.exists(full_img_path) else 0
                    })
            # Reset
            current_visual_lines = []

print(json.dumps(unready_assets, indent=2, ensure_ascii=False))
