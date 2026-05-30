import os
import re

base_dir = "knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017"
md_file = os.path.join(base_dir, "_full.md")
toc_file = os.path.join(base_dir, "toc_list.txt")

with open(md_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# --- 1. Split _full.md into chapter files ---
chapters_content = {}
current_chapter_title = "00_Front_Matter"
current_chapter_lines = []

chapter_pattern = re.compile(r'^#\s*<span[^>]*>Chapter\s+(\d+)\.\s*</span>(.*)$', re.IGNORECASE)

for line in lines:
    match = chapter_pattern.match(line)
    if match:
        if current_chapter_lines:
            chapters_content[current_chapter_title] = current_chapter_lines
        
        chap_num = int(match.group(1))
        chap_name = match.group(2).strip().replace(" ", "_").replace("/", "_").replace(":", "")
        current_chapter_title = f"{chap_num:02d}_{chap_name}"
        current_chapter_lines = [line]
    elif line.startswith("# <span class=\"keep-together\">Appendix"):
        if current_chapter_lines:
            chapters_content[current_chapter_title] = current_chapter_lines
        current_chapter_title = "99_Appendices"
        current_chapter_lines = [line]
    else:
        current_chapter_lines.append(line)

if current_chapter_lines:
    chapters_content[current_chapter_title] = current_chapter_lines

# Write files
filename_map = {} # Maps chapter number to filename
for title, content in chapters_content.items():
    filename = f"chapter_{title}.md"
    if title.startswith("00_") or title.startswith("99_"):
        pass
    else:
        chap_num = int(title.split("_")[0])
        filename_map[chap_num] = filename

    filepath = os.path.join(base_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(content)

# --- 2. Generate index.md from user's toc_list.txt ---
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

with open(toc_file, "r", encoding="utf-8") as f:
    toc_lines = f.readlines()

index_lines = ["# Table of Contents\n\n> Generated from source TOC\n\n"]
current_filename = "chapter_00_Front_Matter.md"

chap_num_pattern = re.compile(r'^#\s*Chapter\s+(\d+)\.')

for line in toc_lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith("# "):
        match = chap_num_pattern.match(line)
        if match:
            chap_num = int(match.group(1))
            current_filename = filename_map.get(chap_num, "unknown.md")
        title_text = line[2:].strip()
        index_lines.append(f"- [{title_text}]({current_filename})\n")
    elif line.startswith("## "):
        title_text = line[3:].strip()
        slug = slugify(title_text)
        index_lines.append(f"  - [{title_text}]({current_filename}#{slug})\n")
    elif line.startswith("### "):
        title_text = line[4:].strip()
        slug = slugify(title_text)
        index_lines.append(f"    - [{title_text}]({current_filename}#{slug})\n")

with open(os.path.join(base_dir, "index.md"), "w", encoding="utf-8") as f:
    f.writelines(index_lines)

print("Chapters split and index.md generated successfully.")
