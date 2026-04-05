import os
import urllib.request
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import matplotlib.pyplot as plt

WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)

# 1. Resize massive pre-attentive images
def resize_image(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    img = Image.open(filename)
    if img.width > 2000 or img.height > 2000:
        print(f"Resizing {filename} from {img.width}x{img.height}...")
        img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
        img.save(filename, "PNG", optimize=True)
        print(f"Saved {filename} as {img.width}x{img.height}")
    else:
        print(f"{filename} is already a reasonable size.")

resize_image('preattentive_numbers_baseline.png')
resize_image('preattentive_numbers_highlighted.png')

def generate_anscombe_table():
    print("Generating Anscombe Four Companies table...")
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    x1 = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
    y1 = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
    x2 = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
    y2 = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
    x3 = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
    y3 = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
    x4 = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 19.0, 8.0, 8.0, 8.0]
    y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.axis('off')
    ax.axis('tight')
    
    headers = ['A厂加班', 'A厂奖金', 'B厂加班', 'B厂奖金', 'C厂加班', 'C厂奖金', 'D厂加班', 'D厂奖金']
    table_data = [headers]
    for i in range(11):
        table_data.append([str(x1[i]), str(y1[i]), str(x2[i]), str(y2[i]), str(x3[i]), str(y3[i]), str(x4[i]), str(y4[i])])
    
    table = ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)
    
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            # Color code companies
            colors = ['#2C3E50', '#2980B9', '#27AE60', '#8E44AD']
            cell.set_facecolor(colors[col // 2])
        else:
            cell.set_facecolor('#ECF0F1' if row % 2 == 0 else '#FFFFFF')
        cell.set_edgecolor('#BDC3C7')
        
    plt.title("四家大厂核心业务抽样数据评估", pad=20, fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('anscombe_four_companies.png', bbox_inches='tight', dpi=150)
    plt.close()
    print("Saved anscombe_four_companies.png")

generate_anscombe_table()

# 3. Download working Datasaurus morphing gif
def download_datasaurus_gif():
    url = "https://raw.githubusercontent.com/lockedata/datasauRus/master/vignettes/Datasaurus.gif"
    try:
        urllib.request.urlretrieve(url, 'datasaurus_morph_dino.gif')
        print("Successfully downloaded real datasaurus_morph_dino.gif")
    except Exception as e:
        print(f"Failed to download from first URL: {e}")
        # fallback URL
        try:
            url2 = "https://wesslen.github.io/dataset-examples/images/DatasaurusDozen.gif"
            urllib.request.urlretrieve(url2, 'datasaurus_morph_dino.gif')
            print("Successfully downloaded from fallback URL.")
        except Exception as e2:
            print(f"Failed fallback: {e2}")

download_datasaurus_gif()
