import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib

# Set font for Chinese characters if possible, or fallback to sans-serif
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

output_dir = os.path.dirname(os.path.abspath(__file__))

def generate_pie_charts():
    print("Generating bad_chart_exploded_pie.png...")
    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    
    # Bad pie: 20 slices, exploded randomly
    np.random.seed(42)
    sizes_bad = np.concatenate([np.random.uniform(5, 15, 5), np.random.uniform(1, 3, 15)])
    explode_bad = np.random.uniform(0.1, 0.4, 20)
    
    # Chaotic colors
    colors_bad = [plt.cm.tab20(i % 20) for i in range(20)]
    
    # Remove labels directly to make it just visually chaotic without cluttering the plot area out of bounds
    wedges, texts = ax.pie(sizes_bad, explode=explode_bad, colors=colors_bad, shadow=True, startangle=140)
    
    plt.title("Q3 全球客户留存结构流失监控概览 (极度失控)", fontsize=16, pad=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "bad_chart_exploded_pie.png"), transparent=False, facecolor='#F4F0E6')
    plt.close()

    print("Generating good_chart_pie_simplified.png...")
    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    
    # Good pie: Clean donut chart, 4 slices
    sizes_good = [40, 30, 15, 15] # 15 is the "Other" category
    labels_good = ['核心高粘性区', '稳健过渡区', '濒危流失区', '其他碎片分布 (低于3%)']
    colors_good = ['#384E77', '#E6B828', '#C84B31', '#999999']
    
    # Donut chart style
    wedgeprops = dict(width=0.4, edgecolor='w', linewidth=2)
    
    wedges, texts, autotexts = ax.pie(sizes_good, labels=labels_good, colors=colors_good, autopct='%1.0f%%',
                                      startangle=90, pctdistance=0.8, textprops={'fontsize': 12, 'fontweight': 'bold'},
                                      wedgeprops=wedgeprops)
    
    # Style the text inside
    for autotext in autotexts:
        autotext.set_color('white')
        
    plt.title("Q3 客户群体阵营结构 (完形收拢重构版)", fontsize=16, pad=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "good_chart_pie_simplified.png"), transparent=False, facecolor='#F4F0E6')
    plt.close()

if __name__ == '__main__':
    generate_pie_charts()
    print("All Gestalt B images generated successfully.")
