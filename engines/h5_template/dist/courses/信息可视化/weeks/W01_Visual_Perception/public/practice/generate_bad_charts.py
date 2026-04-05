import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as patches
import matplotlib

# Set font for Chinese characters if possible, or fallback to sans-serif
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

output_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Generate Spaghetti Chart
plt.figure(figsize=(10, 6), dpi=150)
np.random.seed(42)
x = range(1, 13)
for i in range(15):
    # random walk
    y = np.cumsum(np.random.randn(12) * 10) + 100
    # very similar colors to make it chaotic
    color = plt.cm.tab20(i % 20)
    # or just shades of blue/purple
    color = (np.random.uniform(0.1, 0.4), np.random.uniform(0.3, 0.6), np.random.uniform(0.6, 0.9))
    plt.plot(x, y, linewidth=2, color=color, alpha=0.7)

plt.title("2024 各业务线年度趋势总览 (内部机密)", fontsize=16, pad=15)
plt.ylabel("业务指标数值", fontsize=12)
plt.xlabel("月份", fontsize=12)
plt.xticks(x, [f"{m}月" for m in x])
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "bad_chart_spaghetti.png"))
plt.close()

# 2. Generate Dashboard Disaster
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#F0F2F5')

# identical dark blue box style
box_color = '#1E3A8A'
text_color = 'white'

# Draw 4 identical looking boxes but with wrong spacing and grouping
# Box 1: Sales (Top Left)
rect1 = patches.Rectangle((0.5, 5.5), 4, 4, facecolor=box_color, edgecolor='none')
ax.add_patch(rect1)
ax.text(2.5, 7.5, "东部大区销售额\n\n¥2,345,600", color=text_color, fontsize=16, ha='center', va='center', fontweight='bold')

# Box 2: Returns (Top Right, very close to Box 1)
rect2 = patches.Rectangle((4.8, 5.5), 4, 4, facecolor=box_color, edgecolor='none')
ax.add_patch(rect2)
ax.text(6.8, 7.5, "紧急退货工单数\n\n⚠️ 1,204 件", color=text_color, fontsize=16, ha='center', va='center', fontweight='bold')

# Box 3: Sales (Bottom Left, far away from Top Left)
rect3 = patches.Rectangle((0.5, 0.5), 4, 3.5, facecolor=box_color, edgecolor='none')
ax.add_patch(rect3)
ax.text(2.5, 2.25, "南部大区销售额\n\n¥1,890,200", color=text_color, fontsize=16, ha='center', va='center', fontweight='bold')

# Box 4: Returns (Bottom Right, far away from Top Right)
rect4 = patches.Rectangle((5.5, 0.5), 4, 4.5, facecolor=box_color, edgecolor='none')
ax.add_patch(rect4)
ax.text(7.5, 2.75, "退货超时预警\n\n🚨 345 件", color=text_color, fontsize=16, ha='center', va='center', fontweight='bold')

plt.title("商业综合管理仪表盘 v1.0", fontsize=18, pad=20, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "bad_chart_dashboard_layout.png"))
plt.close()

print("Images generated successfully.")
