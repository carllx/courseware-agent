import matplotlib.pyplot as plt
import numpy as np

# Set up the figure for 16:9 ratio (1920x1080 at 100dpi)
fig, axes = plt.subplots(30, 30, figsize=(19.2, 10.8), dpi=100)

# Colors based on theme_data_ink_swiss
bg_color = '#FFFFFF'
dot_color = '#000000'
border_color = '#E0E0E0'

fig.patch.set_facecolor(bg_color)
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.1, hspace=0.1)

# Generate 900 tiny scatter plots
for i in range(30):
    for j in range(30):
        ax = axes[i, j]
        # random data
        x = np.random.rand(15)
        y = np.random.rand(15)
        
        ax.scatter(x, y, s=1, color=dot_color, alpha=0.6, edgecolors='none')
        
        # Apply strict grid formatting
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor(bg_color)
        
        for spine in ax.spines.values():
            spine.set_color(border_color)
            spine.set_linewidth(0.5)

# Save the figure
out_path = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W04_AI_D3_Basics/public/slides/S03f_Curse_of_Dimensionality_Python.png'
plt.savefig(out_path, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0.1)
print(f"Successfully generated {out_path}")
