import re
import os
import glob

def audit_file(filepath):
    print(f"=== Auditing {os.path.basename(filepath)} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Part E: TTS Safety
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('>'): continue # Skip quotes
        if re.search(r'[\u4e00-\u9fa5]\s*（[A-Za-z0-9\s-]+）', line) or re.search(r'[\u4e00-\u9fa5]\s*\([A-Za-z0-9\s-]+\)', line):
            print(f"  [TTS WARN] Line {i+1}: {line}")
            
    # Part B-6: Comprehension Checkpoints
    chunks = re.split(r'> \[ACTIVITY\].*?(?=\n\n|> \[|\Z)', content, flags=re.DOTALL)
    for i, chunk in enumerate(chunks):
        chunk_clean = re.sub(r'> \[VISUAL\].*?(?=\n\n|\Z)', '', chunk, flags=re.DOTALL)
        chunk_clean = re.sub(r'^---.*?---\n', '', chunk_clean, flags=re.DOTALL)
        chunk_clean = re.sub(r'^>.*?\n', '', chunk_clean, flags=re.MULTILINE)
        chars = len(re.findall(r'[\u4e00-\u9fff]', chunk_clean))
        if chars > 3000:
            print(f"  [CHECKPOINT ERROR] Chunk {i}: {chars} chars without ACTIVITY")
        elif chars > 2000:
            print(f"  [CHECKPOINT WARN] Chunk {i}: {chars} chars without ACTIVITY")

for f in sorted(glob.glob('M0[345]*.md')):
    audit_file(f)

