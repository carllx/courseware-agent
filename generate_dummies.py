import os
from PIL import Image, ImageDraw, ImageText

missing = [
    "W04-01b-Qualitative-Discovery.png",
    "W04-03b-Office-Telemetry.png",
    "W04-09b-Ozzy-Vs-Charles.png",
    "W04-12-Angel-Investor-Failure.png",
    "W04-12b-Confirmation-Bias.png",
    "W04-14b-Output-Vs-Outcome.png",
    "W04-16a-Confounding-Variable.png",
    "W04-16c-Spotify-Release-Radar.png",
    "W04-17b-Amazon-Prime-Hypothesis.png",
    "W04-20a-Infrastructure-Exception.png",
    "W04-20c-Social-Friction-Risk.png",
    "W04-23b2-Dropbox-Video-MVP.png",
    "W04-23e-Wizard-Of-Oz-Examples.png",
    "W04-23f-MVP-Design-Rules.png",
    "W04-24a-Growth-Mindset.png",
    "W04-24b-Office-Ribbon-MVP.png",
    "W04-24c-Team-Assignment.png",
    "W04-24d-MoSCoW-Task.png"
]

out_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W04_MVP_Hypothesis/public/slides"
os.makedirs(out_dir, exist_ok=True)

for name in missing:
    path = os.path.join(out_dir, name)
    if not os.path.exists(path):
        img = Image.new('RGB', (800, 600), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), name, fill=(255,255,0))
        img.save(path)
        print(f"Generated {name}")

