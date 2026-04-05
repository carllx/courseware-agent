from PIL import Image
import os
import glob

WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)

frames = []
png_files = ['datasaurus_numbers.png', 'datasaurus_star.png', 'datasaurus_dino.png']

for file in png_files:
    if os.path.exists(file):
        frames.append(Image.open(file))

if frames:
    frames[0].save(
        'datasaurus_morph_dino.gif',
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=200, 
        loop=0
    )
    print("Successfully generated datasaurus_morph_dino.gif from local frames!")
else:
    print("Could not find PNG frames to generate GIF.")
