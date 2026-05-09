import os
import re
import sys

def parse_time(time_str):
    parts = time_str.replace(',', '.').strip().split(':')
    if len(parts) == 3:
        h, m, s = parts
    else:
        h = 0
        m, s = parts
    try:
        return int(h) * 3600 + int(m) * 60 + float(s)
    except ValueError:
        return 0

def extract_vtt_section(start_sec, end_sec):
    files = [f for f in os.listdir('.') if "1968" in f and "en.vtt" in f]
    if not files: return
    filepath = files[0]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = re.split(r'\n\n+', content)
    output_blocks = []
    
    for block in blocks:
        lines = block.split('\n')
        time_match = None
        for i, line in enumerate(lines):
            if '-->' in line:
                time_match = line
                text_lines = lines[i+1:]
                break
        
        if time_match:
            try:
                start_str, end_str = time_match.split('-->')
                t_start = parse_time(start_str)
                t_end = parse_time(end_str)
            except:
                continue
            
            if t_end >= start_sec and t_start <= end_sec:
                clean_lines = []
                for t in text_lines:
                    t = re.sub(r'<[^>]+>', '', t).strip()
                    if 'align:' in t or 'position:' in t: continue
                    if t and t not in clean_lines:
                        clean_lines.append(t)
                
                if clean_lines:
                    output_blocks.append(f"{start_str.strip()} --> {end_str.strip()}\n" + "\n".join(clean_lines))

    final_output = ["WEBVTT\n"]
    prev_text = ""
    for block in output_blocks:
        lines = block.split('\n')
        text = " ".join(lines[1:])
        if text != prev_text:
            final_output.append(block)
            prev_text = text
            
    with open("extract.en.vtt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(final_output))

if __name__ == '__main__':
    extract_vtt_section(180, 480)
