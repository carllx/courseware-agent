import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
import os
import matplotlib

# Set font for Chinese characters if possible, or fallback to sans-serif
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

output_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# Case D: Gestalt Override (Common Region & Connectedness vs Proximity)
# -------------------------------------------------------------
def generate_override_experiment():
    print("Generating cognitive experiment charts...")
    # BAD CHART: Proximity dominates
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    
    # Draw three distinct boxes
    box_w = 1.2
    box_h = 1.2
    
    # A and B are very close
    pA = (2, 2)
    pB = (3.5, 2)
    # C is very far
    pC = (8, 2)
    
    # Draw boxes
    for p, label in zip([pA, pB, pC], ['A', 'B', 'C']):
        rect = patches.FancyBboxPatch(p, box_w, box_h, boxstyle="round,pad=0.1", fill=True, color='#457B9D', zorder=2)
        ax.add_patch(rect)
        ax.text(p[0] + box_w/2, p[1] + box_h/2, label, color='white', fontsize=24, fontweight='bold', ha='center', va='center', zorder=3)
    
    plt.title("发病状态：大脑不可救药地被“物理距离”欺骗 (A与B结盟)", fontsize=18, pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "bad_chart_gestalt_override.png"), facecolor='#F4F0E6')
    
    # GOOD CHART: Override Proximity with Common Region / Connectedness
    ax.clear()
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    
    # Draw Common Region under B and C
    region_pad = 0.4
    rect_region = patches.FancyBboxPatch((pB[0] - region_pad, pB[1] - region_pad), 
                                         (pC[0] + box_w + region_pad) - (pB[0] - region_pad), 
                                         box_h + 2*region_pad, 
                                         boxstyle="round,pad=0.2", fill=True, color='#EAE6DB', zorder=0)
    ax.add_patch(rect_region)
    ax.text((pB[0]+pC[0]+box_w)/2, pB[1] + box_h + 0.8, "最高武力：同域结界", color='#555555', fontsize=14, fontweight='bold', ha='center')
    
    # Draw Connectedness line between B and C
    ax.plot([pB[0] + box_w, pC[0]], [pB[1] + box_h/2, pC[1] + box_h/2], color='#D62828', linewidth=5, zorder=1)
    ax.text((pB[0]+box_w+pC[0])/2, pB[1] - 0.5, "霸道血脉连线", color='#D62828', fontsize=14, fontweight='bold', ha='center')
    
    # Draw the boxes exactly at the same positions
    for p, label in zip([pA, pB, pC], ['A', 'B', 'C']):
        rect = patches.FancyBboxPatch(p, box_w, box_h, boxstyle="round,pad=0.1", fill=True, color='#457B9D', zorder=2)
        ax.add_patch(rect)
        ax.text(p[0] + box_w/2, p[1] + box_h/2, label, color='white', fontsize=24, fontweight='bold', ha='center', va='center', zorder=3)
        
    plt.title("极权覆盖：无视物理距离，强压结盟 (B与C结盟)", fontsize=18, pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "good_chart_gestalt_override.png"), facecolor='#F4F0E6')
    plt.close()

# -------------------------------------------------------------
# Case E: Animation Sync (Common Fate)
# -------------------------------------------------------------
def generate_animations():
    print("Generating bad_chart_animation_chaos.gif...")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    bar_pos = [1, 2, 4, 5]
    colors = ['#457B9D', '#457B9D', '#E63946', '#E63946']
    labels = ['东区', '西区', '南区(警)', '北区(警)']
    
    def update_bad(frame):
        ax.clear()
        ax.set_ylim(0, 100)
        ax.set_xlim(0, 6)
        ax.set_xticks(bar_pos)
        ax.set_xticklabels(labels)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title("异步乱飞式加载 (动态协同摧毁排版)", pad=15)
        
        # Frame dynamics: completely chaotic
        h1 = min(80, frame * 6)
        h2 = min(60, frame * 3) # western region is super slow
        h3 = min(90, max(0, frame - 8) * 9) # starts late but fast
        h4 = min(75, max(0, frame - 2) * 4) # starts slightly late, very slow
        
        ax.bar(bar_pos, [h1, h2, h3, h4], color=colors, width=0.6)
        return []

    ani_bad = animation.FuncAnimation(fig, update_bad, frames=30, interval=100)
    ani_bad.save(os.path.join(output_dir, "bad_chart_animation_chaos.gif"), writer='pillow', dpi=100)
    plt.close()
    
    print("Generating good_chart_animation_sync.gif...")
    fig, ax = plt.subplots(figsize=(6, 4))
    def update_good(frame):
        ax.clear()
        ax.set_ylim(0, 100)
        ax.set_xlim(0, 6)
        ax.set_xticks(bar_pos)
        ax.set_xticklabels(labels)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title("同频共振式加载 (动态协同重建集群)", pad=15)
        
        # Perfect sync for same colors
        h_blue = min(1.0, frame / 15.0)
        h_red = min(1.0, max(0, frame - 5) / 15.0)
        
        # Easing out
        h_blue = 1 - (1 - h_blue)**3
        h_red = 1 - (1 - h_red)**3
        
        ax.bar(bar_pos[0:2], [80 * h_blue, 60 * h_blue], color=colors[0:2], width=0.6)
        ax.bar(bar_pos[2:4], [90 * h_red, 75 * h_red], color=colors[2:4], width=0.6)
        return []
        
    ani_good = animation.FuncAnimation(fig, update_good, frames=30, interval=100)
    ani_good.save(os.path.join(output_dir, "good_chart_animation_sync.gif"), writer='pillow', dpi=100)
    plt.close()

if __name__ == '__main__':
    generate_override_experiment()
    generate_animations()
    print("Done!")
