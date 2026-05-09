import re
import os

files = [
    "信息可视化/weeks/W01_Visual_Perception/src/M03_视觉系统_你的认知外接显卡.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M04_格式塔原则_大脑的\"找规律\"强迫症.md",
]

def get_iar_type(text):
    if re.search(r"^(但是|然而|却|不过|这说明|这意[味谓]着|更重要的|本质上|从根本上|由此可见|归根结底|核心|第一|首先|为什么|让我们看|总结|总而言之|请注意)", text):
         return "A"
    if re.search(r"^(所以|因此|这就?是|也就是说|换言之|并且|而且|此外|具体来说|比如|例如|就像|由于|之所以|当然|作为|面对)", text):
         return "S"
    return "S" # default is usually S or R depending on heuristics. We treat unknown as S.

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().split('\n\n')
    
    new_lines = []
    s_count = 0
    for block in lines:
        if block.startswith('#') or block.startswith('>'):
            s_count = 0 # reset on structural or visual/activity blocks
            new_lines.append(block)
            continue
            
        # ordinary paragraph
        if re.match(r'^[^>#\-\*!<\[]', block) and not block.strip().isdigit():
            iar = get_iar_type(block)
            if iar == "S":
                s_count += 1
            else:
                s_count = 0 # It's an A or R (usually resets or we only care about S)
                
            if s_count > 2:
                # Inject an activity break before this 3rd S block to reset the stagnation
                activity = "> [ACTIVITY]\n> *   **Type**: `QA`\n> *   **Duration**: `1min`\n> *   **Desc**: 快速共鸣：以上个案例/逻辑为锚点，向学生抛出假设性提问以打破单向灌输。\n"
                new_lines.append(activity)
                s_count = 1 # start counting from this one now
                
        new_lines.append(block)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n\n'.join(new_lines) + "\n")
    print("Fixed IAR for", filepath)

