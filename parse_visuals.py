import re
import yaml
from pathlib import Path

# Load theme
with open('.agent/styles/theme_academic_minimal.yaml', 'r') as f:
    theme = yaml.safe_load(f)
    
prompt_variants = theme['style']['prompt_variants']
base_en = theme['style']['prompt_templates']['base_en']
suffix_negative = theme['style']['prompt_templates']['suffix_negative']

# Read M02
with open('交互产品开发/weeks/W02_Cognitive_Friction/src/M02_意图与反馈的断裂.md', 'r') as f:
    content = f.read()

# Extract VISUAL blocks
blocks = re.split(r'> \[VISUAL\]', content)[1:]
for b in blocks:
    slide_match = re.search(r'\*\*\s*Slide\*\*\s*:\s*(.+)', b)
    layout_match = re.search(r'\*\*\s*Layout\*\*\s*:\s*`?([A-Za-z]+)`?', b)
    scene_match = re.search(r'\*\*\s*Scene\*\*\s*:\s*(.+)', b)
    
    if slide_match and scene_match:
        slide = slide_match.group(1).strip()
        layout = layout_match.group(1).strip() if layout_match else 'Title'
        scene = scene_match.group(1).strip()
        
        # Don't generate if it's explicitly a real photo or video
        if 'real' in scene.lower() or '照片' in scene or '视频' in scene:
            continue
            
        print(f"Slide: {slide}")
        print(f"Layout: {layout}")
        print(f"Scene: {scene}")
        print("-" * 20)
