import re
import os

files = [
    "信息可视化/weeks/W01_Visual_Perception/src/M03_视觉系统_你的认知外接显卡.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M04_格式塔原则_大脑的\"找规律\"强迫症.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M01_我们为什么需要可视化？.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M05_范式革命_Vibe_Coding_与生成的艺术.md",
]

for filepath in files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will split by \n\n
    blocks = re.split(r'\n\n+', content)
    new_blocks = []
    
    for block in blocks:
        # if it's a regular text block (not starting with >, #, -, *, ! or HTML/comment)
        if re.match(r'^[^>#\-\*!<\[]', block) and not re.search(r'!\[', block) and not block.strip().isdigit():
            if new_blocks and re.match(r'^[^>#\-\*!<\[]', new_blocks[-1]) and not re.search(r'!\[', new_blocks[-1]):
                # Merge if the combined length is not excessively long (e.g., < 400 chars)
                if len(new_blocks[-1]) + len(block) < 450:
                    new_blocks[-1] = new_blocks[-1].strip() + " " + block.strip()
                    continue
        new_blocks.append(block)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_blocks) + '\n')
    
    print(f"Processed: {filepath}")
