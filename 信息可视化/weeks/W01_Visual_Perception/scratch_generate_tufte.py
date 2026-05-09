import matplotlib.pyplot as plt
import numpy as np

# Data from the original Challenger O-ring dataset
# Temp (F), Damage Index
data = [
    (53, 11),
    (57, 4),
    (58, 4),
    (63, 2),
    (66, 0),
    (67, 0),
    (67, 0),
    (67, 0),
    (68, 0),
    (69, 0),
    (70, 0),
    (70, 0),
    (70, 4),
    (72, 0),
    (73, 0),
    (75, 0),
    (75, 0),
    (76, 0),
    (76, 0),
    (78, 0),
    (79, 0),
    (81, 0),
]

temp = [d[0] for d in data]
damage = [d[1] for d in data]

fig, ax = plt.subplots(figsize=(10, 6))

# Set background to white
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Scatter plot styling
ax.scatter(temp, damage, color='#5c6bc0', s=80, alpha=0.8, edgecolors='none', zorder=3)

# Annotations from Tufte's chart
# SRM 15 is at (53, 11)
ax.annotate('SRM 15', xy=(53, 11), xytext=(53, 11.5), ha='center', fontsize=10, zorder=4)
# SRM 22 is at (57, 4) - Wait, in the user's screenshot, SRM 22 is at the far right.
# Actually, let's look at the screenshot. SRM 15 is at x~53, y=11. SRM 22 is at x~75, y=4.
# Let me adjust data: there is a point at (75, 4)?
# The classic dataset: 53(11), 57(4), 58(4), 63(2), 70(4), 75(4)?
# Actually, the 75(4) is SRM 22. Let me add it.
# Let's adjust the data to match Tufte exactly if possible.
# Data points visible in thumbnail:
# 53, 11
# 57, 4
# 58, 4
# 63, 2
# 70, 4
# 75, 4 (labeled SRM 22)
# Then many at 0.
data.append((75, 4))
temp = [d[0] for d in data]
damage = [d[1] for d in data]

# Re-plot
ax.clear()
ax.scatter(temp, damage, color='#5c6bc0', s=80, alpha=0.8, edgecolors='none', zorder=3)
ax.annotate('SRM 15', xy=(53, 11), xytext=(53, 10.2), ha='center', fontsize=10, color='#333333')
ax.annotate('SRM 22', xy=(75, 4), xytext=(75, 4.5), ha='center', fontsize=10, color='#333333')

# Forecast annotation
forecast_text = "26 - 29 degree range of forecasted temperatures\n(as of January 27th, 1986) for the launch\nof space shuttle Challenger on January 28th"
ax.annotate(forecast_text, xy=(29, 0), xytext=(26, 3),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5),
            fontsize=10, color='#333333', ha='left')

# Axes limits and labels
ax.set_xlim(25, 85)
ax.set_ylim(-1, 13)
ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
ax.set_xticks(range(25, 90, 5))

ax.set_xlabel('Temperature (degrees F) of field joints at time of launch', fontsize=11, color='#333333', labelpad=10)
ax.set_ylabel('O-ring damage index', fontsize=11, color='#333333', labelpad=10)

# Grid lines
ax.grid(True, which='major', axis='both', color='#e0e0e0', linestyle='-', linewidth=0.5, zorder=1)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_color('#333333')
ax.spines['left'].set_color('#333333')
ax.spines['top'].set_color('#333333')
ax.spines['right'].set_color('#333333')

plt.tight_layout()
out_path = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/public/slides/S02c_Tufte_Mapping_real.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Saved to {out_path}")
