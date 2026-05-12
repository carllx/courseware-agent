import os
import re

def clean_vtt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove WEBVTT header
    content = re.sub(r'WEBVTT.*?\n\n', '', content, flags=re.DOTALL)
    
    # Remove timestamps like 00:00:00.000 --> 00:00:02.000
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s-->\s\d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', content)
    
    # Remove position tags like align:start position:0%
    content = re.sub(r'align:start position:\d+%.*?\n', '', content)
    
    # Remove inline tags like <c> or <00:00:01.000>
    content = re.sub(r'<[^>]+>', '', content)
    
    # Remove empty lines and duplicates
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Simple deduplication for auto-generated subs
    clean_lines = []
    for line in lines:
        if not clean_lines or clean_lines[-1] != line:
            clean_lines.append(line)
            
    # Write back to a txt file
    out_filepath = filepath.replace('.vtt', '.txt')
    with open(out_filepath, 'w', encoding='utf-8') as f:
        f.write(' '.join(clean_lines))
    print(f"Cleaned {filepath} -> {out_filepath}")

directory = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W02_Design_Principles/research_subtitles'
for filename in os.listdir(directory):
    if filename.endswith('.vtt'):
        clean_vtt(os.path.join(directory, filename))
