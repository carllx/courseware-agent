import re

def extract_image_context(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    results = []
    for i, line in enumerate(lines):
        match = re.search(r"!\[.*?\]\((images/.*?\.jpg)\)", line)
        if match:
            img = match.group(1)
            context = "".join(lines[max(0, i-2) : min(len(lines), i+3)])
            if any(k in context.lower() for k in ["旭日图", "和弦图"]):
                context = context.replace("\n", " ")
                results.append((img, context))
    return results

print("=== Hao ===")
hao = extract_image_context("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/knowledge/textbook/信息可视化设计 -- 郝亚维张博文编著/信息可视化设计 -- 郝亚维张博文编著_full.md")
for img, ctx in hao:
    print(f"{img}\n  ==> {ctx[:200]}...")
