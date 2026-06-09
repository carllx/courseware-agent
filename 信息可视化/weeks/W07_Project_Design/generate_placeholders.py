from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(text, path, bg_color, text_color):
    # 16:9 format
    img = Image.new('RGB', (1920, 1080), color=bg_color)
    d = ImageDraw.Draw(img)
    # Just draw a simple border and text
    d.rectangle([(10, 10), (1910, 1070)], outline=(218, 41, 28), width=10) # Swiss Red border
    # Try to load a font, otherwise use default
    font = None
    try:
        # Default font
        font = ImageFont.load_default(size=100)
    except Exception:
        font = ImageFont.load_default()
        
    try:
        # For newer Pillow versions, textbbox is available
        bbox = d.textbbox((0,0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except Exception:
        w, h = font.getsize(text)
        
    d.text(((1920-w)/2, (1080-h)/2), text, fill=text_color, font=font)
    img.save(path)

# M04 Assets
assets = [
    # M04 Type A
    {"file": "assets/slides/m04_s10_great_nation_tech.png", "text": "S10_Great_Nation_Tech (AI Generated)", "type": "A"},
    {"file": "assets/slides/m04_s12_2_axis_code_mapping.png", "text": "S12_2_Axis_Code_Mapping (AI Generated)", "type": "A"},
    {"file": "assets/slides/m04_s13_3_sankey_code.png", "text": "S13_3_Sankey_Code (AI Generated)", "type": "A"},
    # M04 Type B
    {"file": "public/slides/m04_s11_1_tianwen_detail.png", "text": "S11_1_Tianwen_Detail (Real Source)", "type": "B"},
    {"file": "public/slides/m04_s12_1_deepsea_axis.png", "text": "S12_1_DeepSea_Axis (Real Source)", "type": "B"},
    {"file": "public/slides/m04_s13_1_chip_nodes.png", "text": "S13_1_Chip_Nodes (Real Source)", "type": "B"},
    {"file": "public/slides/m04_s13_1_b_force_trap.png", "text": "S13_1_b_Force_Trap (Real Source)", "type": "B"},
    {"file": "public/slides/m04_s13_2_force_vs_sankey.png", "text": "S13_2_Force_Vs_Sankey (Real Source)", "type": "B"},
    
    # M05 Type A
    {"file": "assets/slides/m05_s15_action_plan.png", "text": "S15_Action_Plan (AI Generated)", "type": "A"},
    {"file": "assets/slides/m05_s16_three_principles.png", "text": "S16_Three_Principles (AI Generated)", "type": "A"},
    {"file": "assets/slides/m05_s17_nested_model_defense.png", "text": "S17_Nested_Model_Defense (AI Generated)", "type": "A"},
    {"file": "assets/slides/m05_s17_1_nested_outer.png", "text": "S17_1_Nested_Outer (AI Generated)", "type": "A"},
    {"file": "assets/slides/m05_s17_2_nested_inner.png", "text": "S17_2_Nested_Inner (AI Generated)", "type": "A"},
    # M05 Type B
    {"file": "public/slides/m05_s15_1_spaghetti_chart.png", "text": "S15_1_Spaghetti_Chart (Real Source)", "type": "B"},
    {"file": "public/slides/m05_s16_1_messy_code_pain.png", "text": "S16_1_Messy_Code_Pain (Real Source)", "type": "B"},
    {"file": "public/slides/m05_s18_one_pager_example.png", "text": "S18_One_Pager_Example (Real Source)", "type": "B"},
    
    # M06 Type A
    {"file": "assets/slides/m06_s18_critique_methodology.png", "text": "S18_Critique_Methodology (AI Generated)", "type": "A"},
    {"file": "assets/slides/m06_s18_2b_nested_model_violation.png", "text": "S18_2b_Nested_Model_Violation (AI Generated)", "type": "A"},
    # M06 Type B
    {"file": "public/slides/m06_s18_1_bad_data_mapping.png", "text": "S18_1_Bad_Data_Mapping (Real Source)", "type": "B"},
    {"file": "public/slides/m06_s18_2_critique_diagram.png", "text": "S18_2_Critique_Diagram (Real Source)", "type": "B"},
    {"file": "public/slides/m06_s18_3_data_fault_line.png", "text": "S18_3_Data_Fault_Line (Real Source)", "type": "B"}
]

for item in assets:
    if item['type'] == 'A':
        bg_color = (255, 255, 255) # white
        text_color = (0, 0, 0)
    else:
        bg_color = (245, 245, 245) # light gray for real assets
        text_color = (85, 85, 85)
    create_placeholder(item['text'], item['file'], bg_color, text_color)

print("Images generated.")
