import os
import glob

src_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src'
for filepath in sorted(glob.glob(os.path.join(src_dir, 'M*.md'))):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = content.split('> [VISUAL]')
    for i, block in enumerate(blocks):
        if i == 0: continue # First chunk is before the first VISUAL
        
        # Check if no_ai_flag is present
        if 'no_ai_flag: true' not in block:
            slide_id = ''
            scene = ''
            for line in block.split('\n'):
                if line.startswith('> **Slide**:'):
                    slide_id = line.split(':', 1)[1].strip()
                if line.startswith('> **Scene**:'):
                    scene = line.split(':', 1)[1].strip()
            
            filename = os.path.basename(filepath)
            print(f"- **{filename}** | {slide_id}\n  Scene: {scene}")

