from PIL import Image, ImageDraw

images = [
    "m03_culture_confidence.png",
    "m03_data_derivation.png",
    "m03_overdraw_crisis.png",
    "m03_topology_disassembly.png",
    "m03_tibetan_data_flow.png",
    "m03_emotion_axis.png",
    "m03_color_funnel.png",
    "m03_topology_transition.png"
]

b_class_images = [
    "m03_p5_mesh_detail.png",
    "m03_kimbap_hd.png"
]

out_dir = "信息可视化/weeks/W07_Project_Design/assets/slides"
out_dir_b = "信息可视化/weeks/W07_Project_Design/public/slides"

import os
os.makedirs(out_dir, exist_ok=True)
os.makedirs(out_dir_b, exist_ok=True)

for img_name in images:
    img = Image.new('RGB', (1280, 720), color = (73, 137, 137))
    d = ImageDraw.Draw(img)
    d.text((50,360), "A-CLASS PLACEHOLDER: " + img_name, fill=(255,255,0))
    img.save(f"{out_dir}/{img_name}")

for img_name in b_class_images:
    img = Image.new('RGB', (1280, 720), color = (137, 73, 73))
    d = ImageDraw.Draw(img)
    d.text((50,360), "B-CLASS PLACEHOLDER: " + img_name, fill=(255,255,0))
    img.save(f"{out_dir_b}/{img_name}")

print("Placeholders generated.")
