import re
import os

files = [
    "信息可视化/weeks/W01_Visual_Perception/src/M03_视觉系统_你的认知外接显卡.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M04_格式塔原则_大脑的\"找规律\"强迫症.md",
]

def classify_paragraph(text: str) -> str:
    redundancy_signals = ["总之", "换句话说", "也就是说", "简单来讲", "归根结底", 
                          "回顾一下", "我们刚才讲了", "综上"]
    for sig in redundancy_signals:
        if sig in text:
            return "R"
    
    advancement_signals = [
        re.compile(r'[\d]{4}\s*年'),
        re.compile(r'[\d]+[%％]'),
        re.compile(r'《.+?》'),
        re.compile(r'[A-Z][a-z]+\s+[A-Z]'),
    ]
    for pat in advancement_signals:
        if pat.search(text):
            return "A"
    
    if re.search(r'\*\*[^*]+\*\*', text):
        return "A"

    return "S"

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, "r", encoding="utf-8") as f:
        # split into paragraphs properly (by blank lines)
        blocks = re.split(r'\n\n+', f.read())
    
    new_blocks = []
    consecutive_s = 0
    
    for block in blocks:
        if block.startswith('#') or block.startswith('>'):
            consecutive_s = 0
            new_blocks.append(block)
            continue
            
        if re.match(r'^[^>#\-\*!<\[]', block) and not re.search(r'!\[', block) and not block.strip().isdigit():
            cls = classify_paragraph(block)
            if cls == "S":
                consecutive_s += 1
            else:
                consecutive_s = 0
                
            if consecutive_s > 2:
                # We need to promote this block to 'A' by bolding a phrase
                # Find the first sequence of 2-5 Chinese characters and bold it
                match = re.search(r'([\u4e00-\u9fa5]{2,6})', block)
                if match:
                    original = match.group(1)
                    block = block.replace(original, f"**{original}**", 1)
                    consecutive_s = 0 # reset because it's now an 'A'
        
        new_blocks.append(block)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n\n'.join(new_blocks) + "\n")
    print(f"Fixed IAR by Bolding for {filepath}")
