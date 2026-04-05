import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image
import os

WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)

urls = [
    "https://raw.githubusercontent.com/algoplexity/DatasaurusDozen/main/DatasaurusDozen.tsv",
    "https://raw.githubusercontent.com/algoplexity/DatasaurusDozen/master/DatasaurusDozen.tsv",
    "https://raw.githubusercontent.com/hms-dbmi/Fundamentals-of-Data-Science/master/data/DatasaurusDozen.tsv",
    "https://gist.githubusercontent.com/andrewheiss/0582d2f26038e5cbaf8311bd30ebde16/raw/7b63fbedb00424fb8fe29e843c081db87b32231b/datasaurus_dozen.tsv"
]
for u in urls:
    try:
        urllib.request.urlretrieve(u, 'DatasaurusDozen.tsv')
        print(f"Successfully downloaded from {u}")
        break
    except Exception as e:
        print(f"Failed {u}: {e}")

if not os.path.exists('DatasaurusDozen.tsv'):
    print("Error: Could not obtain dataset.")
    exit(1)

df = pd.read_csv('DatasaurusDozen.tsv', sep='\t')
datasets = df['dataset'].unique()

print(f"Found datasets: {datasets}")

# We want the sequence to end with the dino for maximum impact
datasets_sorted = [d for d in datasets if d != 'dino'] + ['dino']

frames = []
for name in datasets_sorted:
    d = df[df['dataset'] == name]
    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    ax.scatter(d['x'], d['y'], color='#E67E22', alpha=0.9, s=40, edgecolors='white', linewidth=0.5)
    ax.set_title(f"Dataset: {name.capitalize()}", pad=15, fontsize=14, fontweight='bold', color='#2C3E50')
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.3)
    filename = f"tmp_{name}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    frames.append(Image.open(filename))

if frames:
    frames[0].save(
        'datasaurus_morph_dino.gif',
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=300, 
        loop=0
    )
    print("Successfully generated true datasaurus_morph_dino.gif!")
    for name in datasets:
        if os.path.exists(f"tmp_{name}.png"):
            os.remove(f"tmp_{name}.png")
