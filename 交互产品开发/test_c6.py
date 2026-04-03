import yaml
import os

hub_path = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/knowledge/knowledge_hub.yaml"
textbook_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/knowledge/textbook"

with open(hub_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

hub_sources = set()
for entry in data.get('entries', []):
    src = entry.get('source', '')
    if src:
        hub_sources.add(src)

missing = []
for book_dir in sorted(os.listdir(textbook_dir)):
    book_path = os.path.join(textbook_dir, book_dir)
    if not os.path.isdir(book_path):
        continue
    for fname in sorted(os.listdir(book_path)):
        if not fname.endswith(".md"):
            continue
        if any(skip in fname for skip in ["_full", "index", "Contents", "CONTENTS", "Front_Matter",
                                           "Preface", "Acknowledgments", "Bibliography"]):
            continue
        if not fname.startswith("chapter_"):
            continue
        rel = os.path.join("knowledge", "textbook", book_dir, fname)
        rel = rel.replace("\\", "/")
        if rel not in hub_sources:
            missing.append(rel)

print(f"Missing count: {len(missing)}")
