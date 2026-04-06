import re

def search_textbook(file_path, keywords):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    results = []
    for i, line in enumerate(lines):
        match = re.search(r"!\[.*?\]\((images/.*?\.jpg)\)", line)
        if match:
            img = match.group(1)
            context = "".join(lines[max(0, i-3) : min(len(lines), i+4)]).lower()
            if any(k.lower() in context for k in keywords):
                context_clean = context.replace("\n", " ")
                results.append((img, context_clean))
    return results

keywords_munzner = ["unjustified", "memory", "black and white", "3d", "occlusion", "distortion", "pie", "erase"]
keywords_hao = ["墨水", "数据墨水", "tufte", "饼图", "3d", "擦除"]

print("=== Munzner ===")
munzner = search_textbook("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/Visualization Analysis & Design -- Tamara Munzner -- 2014/Visualization Analysis & Design -- Tamara Munzner -- 2014_full.md", keywords_munzner)
for img, ctx in munzner:
    print(f"{img} | {ctx[:150]}...")

print("\n=== Hao Yawei ===")
hao = search_textbook("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/信息可视化设计 -- 郝亚维张博文编著/信息可视化设计 -- 郝亚维张博文编著_full.md", keywords_hao)
for img, ctx in hao:
    print(f"{img} | {ctx[:150]}...")

