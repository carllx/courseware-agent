import sys
sys.path.insert(0, '/Users/yamlam/Downloads/2025-2026-2 课程/.agent/skills/validation_suite/scripts')
from script_parser import parse_script, BlockType
from engines.generate_course_h5 import blocks_to_h5_json, extract_visual_list
from pathlib import Path

blocks = parse_script("/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src/M01_认知框架_你的大脑不是处理器.md")
for b in blocks:
    if b.block_type == BlockType.VISUAL:
        print(f"Slide ID: {b.metadata.get('slide_id')}")
        items = extract_visual_list(b)
        print(f"List: {items}")
