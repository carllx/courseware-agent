import os
import glob
import re

textbook_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook"
md_files = glob.glob(f"{textbook_dir}/**/*.md", recursive=True)

for file in md_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    images = re.findall(r'!\[.*?\]\((.*?)\)', content)
    for img in images:
        if 'images/' in img:
            print(f"Found image: {img} in {os.path.basename(file)}")

