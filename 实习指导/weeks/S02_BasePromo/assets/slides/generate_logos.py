import os
from PIL import Image, ImageDraw, ImageFont

# --- Config ---
BASE_DIR = "/Users/yamlam/Downloads/2025-2026-2 课程/实习指导"
ASSETS_DIR = os.path.join(BASE_DIR, "visuals/assets/S02_BasePromo")
OUTPUT_DIR = ASSETS_DIR

# Design System
BG_COLOR = "#0F1923"
SURFACE_COLOR = "#1B2A41"
PRIMARY_COLOR = "#00D2D3"
TEXT_MAIN = "#FFFFFF"
TEXT_SECONDARY = "#A8C0D8"

WIDTH, HEIGHT = 1920, 1080

# Fonts (macOS verified)
FONT_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"

# Company Data
COMPANIES = [
    {
        "id": "yueyou",
        "card_name": "S02_Base_Yueyou.png",
        "name": "霍尔果斯悦游网络科技有限公司",
        "label": "动漫游戏开发 / 技术服务",
        "keywords": ["游戏联运", "美术外包", "技术支持"],
        "logo_path": os.path.join(ASSETS_DIR, "logo_yueyou.png")
    },
    {
        "id": "coco",
        "card_name": "S02_Base_Coco.png",
        "name": "广州口可口可软件科技有限公司",
        "label": "软件开发 / 互动娱乐",
        "keywords": ["VR/AR/MR/XR", "元宇宙", "94项软著 21项专利"],
        "logo_path": os.path.join(ASSETS_DIR, "logo_coco.jpg")
    },
    {
        "id": "yuanxiang",
        "card_name": "S02_Base_Yuanxiang.png",
        "name": "广州市原象信息科技有限公司",
        "label": "整合营销 / 数字广告",
        "keywords": ["数字营销", "4A标准", "全链路追踪"],
        "logo_path": os.path.join(ASSETS_DIR, "logo_yuanxiang.jpg")
    },
    {
        "id": "xzc",
        "card_name": "S02_Base_XZC.png",
        "name": "广州新众创科技有限公司",
        "label": "网络技术 / 软件开发",
        "keywords": ["软件开发", "人工智能", "全流程交付"],
        "logo_path": os.path.join(ASSETS_DIR, "logo_xzc.png")
    },
    {
        "id": "mingjiang",
        "card_name": "S02_Base_MingJiang.png",
        "name": "郑州名匠网络科技有限公司广州分公司",
        "label": "游戏美术外包 / 3D 制作",
        "keywords": ["高精度美术", "动作捕捉", "3D角色动作"],
        "logo_path": os.path.join(ASSETS_DIR, "logo_mingjiang.jpg")
    }
]

def create_card(company):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Background Surface (Card)
    card_margin = 150
    draw.rounded_rectangle([card_margin, card_margin, WIDTH - card_margin, HEIGHT - card_margin], radius=30, fill=SURFACE_COLOR, outline=PRIMARY_COLOR, width=3)
    
    try:
        font_h1 = ImageFont.truetype(FONT_BOLD, 60)
        font_h2 = ImageFont.truetype(FONT_REGULAR, 40)
        font_body = ImageFont.truetype(FONT_REGULAR, 30)
    except:
        font_h1 = font_h2 = font_body = ImageFont.load_default()

    # 2. Logo Placement
    try:
        logo = Image.open(company["logo_path"]).convert("RGBA")
        logo.thumbnail((400, 400), Image.Resampling.LANCZOS)
        logo_x = card_margin + 50
        logo_y = card_margin + 100
        img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Error loading logo for {company['id']}: {e}")

    # 3. Text Info
    text_x = card_margin + 500
    draw.text((text_x, card_margin + 100), company["name"], font=font_h1, fill=PRIMARY_COLOR)
    draw.text((text_x, card_margin + 200), f"标签: {company['label']}", font=font_h2, fill=TEXT_MAIN)
    
    y_offset = 350
    draw.text((text_x, card_margin + y_offset), "核心业务与特点:", font=font_h2, fill=TEXT_SECONDARY)
    y_offset += 70
    for kw in company["keywords"]:
        draw.text((text_x + 30, card_margin + y_offset), f"• {kw}", font=font_body, fill=TEXT_MAIN)
        y_offset += 50

    output_path = os.path.join(OUTPUT_DIR, company["card_name"])
    img.save(output_path)
    print(f"Generated: {output_path}")

def create_composite():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 70)
        font_name = ImageFont.truetype(FONT_REGULAR, 24)
    except:
        font_title = font_name = ImageFont.load_default()

    draw.text((WIDTH//2 - 250, 80), "重点实习基地概览", font=font_title, fill=PRIMARY_COLOR)
    
    # Grid for logos
    box_w = 300
    box_h = 300
    gap = 50
    start_x = (WIDTH - (box_w * 5 + gap * 4)) // 2
    
    for i, company in enumerate(COMPANIES):
        x = start_x + i * (box_w + gap)
        y = 400
        
        draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=15, fill=SURFACE_COLOR, outline=PRIMARY_COLOR, width=2)
        
        try:
            logo = Image.open(company["logo_path"]).convert("RGBA")
            logo.thumbnail((240, 240), Image.Resampling.LANCZOS)
            offset_x = (box_w - logo.width) // 2
            offset_y = (box_h - logo.height) // 2
            img.paste(logo, (x + offset_x, y + offset_y), logo if logo.mode == 'RGBA' else None)
        except Exception as e:
            print(f"Error in composite for {company['id']}: {e}")
            
        short_name = company["name"][:8] + "..." if len(company["name"]) > 10 else company["name"]
        draw.text((x + 20, y + box_h + 20), short_name, font=font_name, fill=TEXT_MAIN)

    output_path = os.path.join(OUTPUT_DIR, "S02_Base_Logos.png")
    img.save(output_path)
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    for c in COMPANIES:
        create_card(c)
    create_composite()
