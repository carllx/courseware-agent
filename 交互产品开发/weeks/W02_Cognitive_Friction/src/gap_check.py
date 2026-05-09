import os
import re

def check_files(src_dir):
    files = [f for f in os.listdir(src_dir) if f.startswith('M') and f.endswith('.md')]
    for file in sorted(files):
        path = os.path.join(src_dir, file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"Checking {file}...")
        
        # Check Bullet Sync (List items must be mentioned in preceding [VISUAL] block)
        # Check Visual Gap (>360 chars without [VISUAL])
        
        visual_blocks = list(re.finditer(r'> \[VISUAL\].*?(?=> \[|$)', content, re.DOTALL))
        
        # simple gap check
        chunks = re.split(r'> \[VISUAL\].*?\n(?:\n|> )', content, flags=re.DOTALL)
        for i, chunk in enumerate(chunks):
            text_only = re.sub(r'<[^>]+>', '', chunk)
            text_only = re.sub(r'\[.*?\]\(.*?\)', '', text_only)
            text_only = re.sub(r'> \[.*?\]', '', text_only)
            text_only = re.sub(r'#.*', '', text_only)
            text_len = len(re.sub(r'\s+', '', text_only))
            if text_len > 360:
                print(f"  WARNING: Visual Gap detected ({text_len} chars) in chunk {i}")

if __name__ == '__main__':
    src_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src'
    check_files(src_dir)
