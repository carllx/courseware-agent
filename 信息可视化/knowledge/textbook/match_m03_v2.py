import re

def extract_images_for_figure(file_path, figures):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    results = {fig: [] for fig in figures}
    for i, line in enumerate(lines):
        match = re.search(r"!\[.*?\]\((images/.*?\.jpg)\)", line)
        if match:
            img = match.group(1)
            # look ahead 5 lines and behind 5 lines for figure names
            context = "".join(lines[max(0, i-5) : min(len(lines), i+6)])
            for fig in figures:
                if fig.lower() in context.lower():
                    results[fig].append(img)
    return results

figs = ["Figure 5.7", "Figure 5.11", "Figure 5.10", "Figure 5.13", "Figure 5.14", "Figure 5.15", "Figure 5.8", "Figure 10.1.", "Figure 10.13"]
res = extract_images_for_figure("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Visualization Analysis & Design -- Tamara Munzner -- 2014/Visualization Analysis & Design -- Tamara Munzner -- 2014_full.md", figs)

for fig, imgs in res.items():
    print(f"{fig}:")
    for img in set(imgs):
        print(f"  {img}")
