import yaml
import os
import glob

hub_path = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/knowledge/knowledge_hub.yaml"
textbook_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/knowledge/textbook"

with open(hub_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# Collect existing sources
existing_sources = set()
for entry in data.get('entries', []):
    if 'source' in entry:
        existing_sources.add(entry['source'])

# Find all markdown files in textbook
all_md_files = glob.glob(os.path.join(textbook_dir, "**/*.md"), recursive=True)

missing_files = []
for md_file in all_md_files:
    rel_path = os.path.relpath(md_file, "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/")
    if rel_path not in existing_sources:
        missing_files.append(rel_path)

# Append missing files to entries
for mf in missing_files:
    # generate a simple id based on filename
    basename = os.path.basename(mf)
    name_no_ext = os.path.splitext(basename)[0]
    book_name = mf.split('/')[-2] if '/' in mf else 'unknown'
    short_book = book_name[:10].replace(' ', '_')
    
    entry = {
        'id': f"auto-{short_book}-{name_no_ext}",
        'type': 'textbook',
        'tags': ['auto-added'],
        'summary': f"自动导入章节: {name_no_ext}",
        'source': mf
    }
    data['entries'].append(entry)

# Write back without query_hints
# Since pyyaml drops comments and might change formatting, let's just do text replacement for query_hint if we can,
# but using yaml dump is safer. Let's filter query_hint from dicts.
for entry in data.get('entries', []):
    if 'query_hint' in entry:
        del entry['query_hint']

with open(hub_path, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print(f"Added {len(missing_files)} missing entries. Removed query_hints.")
