import yaml
import re
import os

yaml_file = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/course_textbooks.yaml"
toc_file = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017/toc_list.txt"

with open(yaml_file, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

with open(toc_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

toc_list = []
pattern = re.compile(r'^#\s*Chapter\s+(\d+)\.\s*(.*)')
for line in lines:
    match = pattern.match(line)
    if match:
        chap_num = int(match.group(1))
        chap_title = match.group(2).strip()
        toc_list.append({
            "chapter": chap_num,
            "title": chap_title,
            "title_en": chap_title
        })

new_book = {
    "title": "Interactive Data Visualization for the Web",
    "author": "Scott Murray",
    "publisher": "O'Reilly Media, Inc.",
    "year": "2017",
    "type": "reference",
    "citation": "Scott Murray. Interactive Data Visualization for the Web[M]. O'Reilly Media, Inc., 2017.",
    "toc": toc_list
}

data["textbooks"].append(new_book)

with open(yaml_file, "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, sort_keys=False)

print("Updated course_textbooks.yaml")
