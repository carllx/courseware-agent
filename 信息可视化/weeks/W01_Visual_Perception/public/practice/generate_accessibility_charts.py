import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as patches
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

output_dir = os.path.dirname(os.path.abspath(__file__))

# 构造数据结构：5x6 的网格
np.random.seed(42)
data = np.random.uniform(-100, 100, (5, 6))

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
# 1. Bad Chart: Pure Red/Green Heatmap
# Red is negative, Green is positive
cmap_bad = plt.cm.RdYlGn

cax = ax.matshow(data, cmap=cmap_bad, vmin=-100, vmax=100)
fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04, label="利润表现 (净利/亏损)")

ax.set_title("各区域月度利润贡献总览", pad=20, fontsize=16, fontweight='bold')
ax.set_xticks(range(6))
ax.set_xticklabels([f"Q{i+1}" if i<4 else f"Extra{i}" for i in range(6)])
ax.set_yticks(range(5))
ax.set_yticklabels([f"大区 {chr(65+i)}" for i in range(5)])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "bad_chart_accessibility_rg.png"))
plt.close()

# 2. Good Chart: Redundant Encoding (Color + Shape + Texture)
# Using ColorBrewer colorblind safe palette (PuOr or RdBu)
# Blue for profit, Orange for loss
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
cmap_good = plt.cm.PuOr

# Draw grid manually to support hatching
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 4.5)

for i in range(5):
    for j in range(6):
        val = data[i, j]
        # Normalize to 0-1 for colormap
        norm_val = (val + 100) / 200.0
        color = cmap_good(norm_val)
        
        # Determine shape and texture based on sign
        if val > 0:
            hatch = '///'
            symbol = '▲'
            text_color = 'white' if val > 50 else 'black'
        else:
            hatch = '...'
            symbol = '▼'
            text_color = 'white' if val < -50 else 'black'
            
        rect = patches.Rectangle((j-0.5, 4.5-i-1), 1, 1, facecolor=color, edgecolor='white', hatch=hatch)
        ax.add_patch(rect)
        
        # Add text symbol and value
        ax.text(j, 4.5-i-0.5, f"{symbol}\n{int(val)}", color=text_color, 
                ha='center', va='center', fontsize=12, fontweight='bold')

ax.set_title("各区域月度利润贡献总览 (无障碍优化版)", pad=20, fontsize=16, fontweight='bold')
ax.set_xticks(range(6))
ax.set_xticklabels([f"Q{i+1}" if i<4 else f"Ext{i}" for i in range(6)])
ax.set_yticks(range(5))
ax.set_yticklabels([f"大区 {chr(65+4-i)}" for i in range(5)]) # matching typical matshow order
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "good_chart_accessibility_fixed.png"))
plt.close()

print("Accessibility charts generated successfully.")
