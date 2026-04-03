import os
import random
import matplotlib.pyplot as plt

WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)

def generate_matrices():
    # Set fixed seed so both images have identical numbers
    random.seed(42)
    rows, cols = 15, 25
    
    # Generate random single digits (0-9) avoiding too many 3s
    digits = [str(random.choice([0, 1, 2, 4, 5, 6, 7, 8, 9])) for _ in range(rows * cols)]
    
    # Insert exactly 8 '3's at random positions
    threes_indices = random.sample(range(rows * cols), 8)
    for idx in threes_indices:
        digits[idx] = '3'
        
    grid = [digits[i * cols:(i + 1) * cols] for i in range(rows)]
    
    # Generate Baseline Image
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.axis('off')
    ax.axis('tight')
    
    for r in range(rows):
        for c in range(cols):
            ax.text(c, rows - 1 - r, grid[r][c], 
                    ha='center', va='center', fontsize=20, color='#333333', family='sans-serif')
            
    ax.set_xlim(-1, cols)
    ax.set_ylim(-1, rows)
    plt.tight_layout()
    plt.savefig('preattentive_numbers_baseline.png', bbox_inches='tight', dpi=150, transparent=False, facecolor='white')
    plt.close()
    
    # Generate Highlighted Image
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.axis('off')
    ax.axis('tight')
    
    for r in range(rows):
        for c in range(cols):
            val = grid[r][c]
            if val == '3':
                ax.text(c, rows - 1 - r, val, 
                        ha='center', va='center', fontsize=22, color='#E74C3C', weight='bold', family='sans-serif')
            else:
                ax.text(c, rows - 1 - r, val, 
                        ha='center', va='center', fontsize=20, color='#95A5A6', family='sans-serif')
            
    ax.set_xlim(-1, cols)
    ax.set_ylim(-1, rows)
    plt.tight_layout()
    plt.savefig('preattentive_numbers_highlighted.png', bbox_inches='tight', dpi=150, transparent=False, facecolor='white')
    plt.close()
    print("Regenerated both preattentive_numbers images successfully!")

generate_matrices()
