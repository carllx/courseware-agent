import os
import re

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src"

slides_to_prune = [
    "S00_Carrier_Evolution", "S00_Visual_Preference", "S00c_Practice_Intro", "S00c_W6_Scrollytelling", 
    "S00d_Toolchain_And_Vibe", "S06_Evolution_Timeline", "S09c_Pre_attentive_Channels_Full", "S10_Resource_Limitations", 
    "S10b_Change_Blindness", "S13_Gestalt_Intro", "S14_Gestalt_Proximity", "S15_Kanizsa_Triangle_And_Space", 
    "S16b_Figure_Ground_Symmetry", "S16c_Common_Fate_Motion", "S17_Design_Space", "S17b_Bounded_Rationality_Philosophy", 
    "S18_Software_Evolution", "S20_Vibe_Demo_Activity", "S21_Workshop_Overview", "S21ba_GUI_Pain"
]

for filename in os.listdir(src_dir):
    if not filename.endswith(".md"): continue
    path = os.path.join(src_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for sid in slides_to_prune:
        # Match the VISUAL block for this sid
        # We need to find `**Slide**: Sxx` and then the `**Scene**: ...` line
        block_regex = r"(> \[VISUAL\]\n(?:> \*[^\n]+\n)*?(?:> \*\s+\*\*Slide\*\*: `?" + sid + r"`?.*?\n)(?:> \*[^\n]+\n)*)"
        def prune_scene(match):
            block = match.group(0)
            def shorten_scene_line(m):
                scene_line = m.group(0)
                # Keep only up to 20 chars of the scene description
                prefix = m.group(1)
                text = m.group(2)
                if len(text) > 15:
                    return prefix + text[:15] + "..." + "\n"
                return scene_line
            # Replace Scene
            return re.sub(r"(> \*\s+\*\*Scene\*\*:\s*)([^\n]+)\n", shorten_scene_line, block)
            
        content = re.sub(block_regex, prune_scene, content)
        
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Pruned scenes in {filename}")

