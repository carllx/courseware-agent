import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = re.split(r'(> \[VISUAL\].*?(?=\n\n|\n> \[|\Z))', content, flags=re.DOTALL)
    
    for i in range(0, len(chunks), 2):
        chunk = chunks[i]
        chunk_clean = re.sub(r'> \[.*?\].*?(?=\n\n|\Z)', '', chunk, flags=re.DOTALL)
        chunk_clean = re.sub(r'^---.*?---\n', '', chunk_clean, flags=re.DOTALL)
        chunk_clean = re.sub(r'^>.*?\n', '', chunk_clean, flags=re.MULTILINE)
        chars = len(re.findall(r'[\u4e00-\u9fff]', chunk_clean))
        if chars > 250:
            print(f"--- GAP in {filepath} Chunk {i//2} ({chars} chars) ---")
            print(chunk.strip())
            print("-" * 40)

import glob
for f in sorted(glob.glob('M*.md')):
    process_file(f)
