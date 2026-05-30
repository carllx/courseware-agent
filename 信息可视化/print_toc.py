import os

base_dir = "knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017"
md_file = os.path.join(base_dir, "_full.md")

with open(md_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

toc = []
for i, line in enumerate(lines):
    if line.startswith("# ") or line.startswith("## "):
        toc.append(f"{i+1}: {line.strip()}")

with open(os.path.join(base_dir, "toc_list.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(toc))

print(f"Extracted {len(toc)} headings.")
