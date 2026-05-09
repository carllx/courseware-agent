import re
import sys

def search_images(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        match = re.search(r"!\[.*?\]\((images/.*?\.jpg)\)", line)
        if match:
            img = match.group(1)
            context = "".join(lines[max(0, i-3) : min(len(lines), i+4)]).lower()
            if "figure 2." in context or "figure 1." in context or "figure 3." in context:
                print(f"Match for {img}:")
                print(context.strip())
                print("-" * 40)

search_images("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Visualization Analysis & Design -- Tamara Munzner -- 2014/Visualization Analysis & Design -- Tamara Munzner -- 2014_full.md")
