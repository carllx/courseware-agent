from PIL import Image, ImageDraw
import sys
import os

filename = sys.argv[1]
text = sys.argv[2][:50]
os.makedirs(os.path.dirname(filename), exist_ok=True)
img = Image.new('RGB', (1920, 1080), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((100, 500), text, fill=(0,0,0))
img.save(filename)
print(f"Generated {filename}")
