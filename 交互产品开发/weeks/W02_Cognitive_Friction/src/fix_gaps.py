import re
import os

def count_chinese_chars(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n=== Auditing {os.path.basename(filepath)} ===")

    chunks = re.split(r'(> \[VISUAL\].*?(?=\n\n|\n> \[|\Z))', content, flags=re.DOTALL)
    
    warn_count = 0
    error_count = 0

    for i in range(0, len(chunks), 2):
        chunk = chunks[i]
        
        # Remove all other blockquotes that are special blocks > [SOMETHING]
        # and their subsequent > lines until an empty line
        chunk_clean = re.sub(r'> \[.*?\].*?(?=\n\n|\Z)', '', chunk, flags=re.DOTALL)
        
        # Remove YAML frontmatter
        chunk_clean = re.sub(r'^---.*?---\n', '', chunk_clean, flags=re.DOTALL)
        
        # Remove empty blockquotes lines
        chunk_clean = re.sub(r'^>.*?\n', '', chunk_clean, flags=re.MULTILINE)
        
        chars = count_chinese_chars(chunk_clean)
        
        if chars > 360:
            print(f"  [GAP ERROR] Chunk {i//2}: {chars} chars. Preview: {chunk_clean[:30].strip()}")
            error_count += 1
        elif chars > 250:
            print(f"  [GAP WARN] Chunk {i//2}: {chars} chars. Preview: {chunk_clean[:30].strip()}")
            warn_count += 1

    return warn_count, error_count

import glob
total_warn = 0
total_error = 0
src_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src'
for f in sorted(glob.glob(os.path.join(src_dir, 'M*.md'))):
    w, e = audit_file(f)
    total_warn += w
    total_error += e

print(f"\nTotal Warn: {total_warn}, Total Error: {total_error}")
