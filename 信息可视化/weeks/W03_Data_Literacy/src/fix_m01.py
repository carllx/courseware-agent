import re

with open('/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/src/M01_为什么你的_AI_画不出一张正常的图.md', 'r') as f:
    content = f.read()

# Fix DEGEN modifiers
replacements = {
    "极其厉害的": "高级",
    "极其口语化": "口语化",
    "极其粗糙": "粗糙",
    "彻底错位、毫无空间逻辑的黑色曲解乱阵": "错位且失去空间逻辑的黑色图表",
    "极其荒诞": "荒诞",
    "狂暴地求和求平均": "执行求和求平均",
    "极其可笑地": "错误地",
    "极其恐怖的视觉终极遮蔽绝症": "严重的视觉遮蔽（Overplotting）",
    "彻底彻底掩盖掉": "彻底掩盖掉",
    "极度冗余": "冗余",
    "极度杂乱无章": "杂乱",
    "极其严苛彻底": "严苛",
    "极度理智": "理智",
    "极其流利地": "流畅地",
    "绝世兵器": "精良工具",
    "史诗级": "重要",
    "极度安静": "安静",
    "彻底崩溃": "崩溃",
    "极其典型": "典型",
    "令人作呕的": "复杂的",
    "极度平整": "平整",
    "极度丝滑": "顺畅",
    "疯狂流": "流",
    "死死用极高倍放大镜": "用放大镜",
    "完完全全遗失": "遗失",
    "彻底洞悉": "洞悉",
    "极简瘦长的纯净直列": "瘦长的直列"
}

for k, v in replacements.items():
    content = content.replace(k, v)

# Fix missing Text / List in VISUAL blocks
def add_text_list(match):
    block = match.group(0)
    if "**Text**:" not in block and "**List**:" not in block:
        # Extract caption or scene to make a text
        caption_match = re.search(r'\*\s+\*\*Caption\*\*:\s+"([^"]+)"', block)
        if caption_match:
            text = caption_match.group(1)
        else:
            text = "核心视觉信息"
        
        layout_match = re.search(r'\*\s+\*\*Layout\*\*:\s+`([^`]+)`', block)
        layout = layout_match.group(1) if layout_match else "Full"
        
        insert_str = f'\n> *   **List**: ["{text}"]' if layout in ["Grid", "Comparison"] else f'\n> *   **Text**: "{text}"'
        
        # Insert before Asset
        block = re.sub(r'\n>\s+\*\s+\*\*Asset\*\*:', f'{insert_str}\n> *   **Asset**:', block)
    
    # Grid also needs List if it only has Text
    if "Layout**: `Grid`" in block and "**List**:" not in block:
        text_match = re.search(r'\*\s+\*\*Text\*\*:\s+"([^"]+)"', block)
        if text_match:
            text = text_match.group(1)
            block = re.sub(r'\n>\s+\*\s+\*\*Text\*\*:\s+"[^"]+"', f'\n> *   **List**: ["{text}"]', block)
            
    return block

content = re.sub(r'> \[VISUAL\][\s\S]*?> \*\s+\*\*Asset\*\*:.*?\n', add_text_list, content)

# Fix heading and block orders
# S01_Title_W03 should have a heading before it
if "### 1.0" not in content:
    content = content.replace("> [VISUAL]\n> *   **Slide**: `S01_Title_W03`", "### 1.0 引言：看不见的冰山\n\n> [VISUAL]\n> *   **Slide**: `S01_Title_W03`")

# S06 before 1.3 -> move after 1.3
def move_visual_after_heading(content, slide_id, heading_prefix):
    # Match the entire VISUAL block
    pattern_visual = r'(> \[VISUAL\]\n> \*\s+\*\*Slide\*\*: `' + slide_id + r'`[\s\S]*?> \*\s+\*\*Asset\*\*:.*?\n)'
    visual_match = re.search(pattern_visual, content)
    if visual_match:
        visual_block = visual_match.group(1)
        # Match the heading
        heading_pattern = r'(### ' + heading_prefix + r'[^\n]+\n\n)'
        heading_match = re.search(heading_pattern, content)
        if heading_match and visual_block in content[:heading_match.start()]:
            # Remove from original
            content = content.replace(visual_block + '\n', '')
            # Insert after heading
            content = content.replace(heading_match.group(1), heading_match.group(1) + visual_block + '\n')
    return content

content = move_visual_after_heading(content, "S06_The_Machine_View", "1.3")
content = move_visual_after_heading(content, "S07_Data_Shape_Concept", "1.4")
content = move_visual_after_heading(content, "S10_LLM_Prompt_Hierarchy", "1.5")

# Ensure Speech length for S01
if "欢迎来到数据可视化核心框架体系理论的第三周" in content:
    content = content.replace("各位同学，欢迎来到数据可视化核心框架体系理论的第三周", "同学们好，在这座巨大的冰山面前，我们看到水面上五光十色的漂亮图表。但这仅仅是表象，水面之下是庞大且错综复杂的原始数据表，这才是决定可视化成败的核心。\n\n各位同学，欢迎来到数据可视化核心框架体系理论的第三周")

with open('/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/src/M01_为什么你的_AI_画不出一张正常的图.md', 'w') as f:
    f.write(content)
