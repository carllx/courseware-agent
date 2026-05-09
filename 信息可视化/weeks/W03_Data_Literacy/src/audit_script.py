import re
import os
import glob

def strip_markdown(text):
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'>\s+', '', text)
    return text

def count_chinese_chars(text):
    text = strip_markdown(text)
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'(> \[VISUAL\]|> \[ACTIVITY\])', content)
    
    current_gap_text = ""
    current_gap_lines = []
    
    last_visual_pos = 0
    current_visual_has_list = False
    
    lines = content.split('\n')
    
    print(f"\n--- Analyzing {os.path.basename(filepath)} ---")
    
    current_visual_block = None
    speech_since_last_visual = []
    speech_chars = 0
    start_line = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if '> [VISUAL]' in line:
            # check gap before this
            if speech_chars > 250:
                print(f"[VISUAL_GAP] Lines {start_line}-{i}: {speech_chars} chars without visual.")
            
            # extract visual block
            visual_block_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith('>'):
                visual_block_lines.append(lines[j])
                j += 1
            visual_text = '\n'.join(visual_block_lines)
            has_list = '**List**' in visual_text or '**List**:' in visual_text or '**List**：' in visual_text
            
            # analyze previous speech for lists if previous visual didn't have list
            list_items = re.findall(r'(?:^|\n)\s*(?:\d+\.|-|\*)\s+.*', '\n'.join(speech_since_last_visual))
            if len(list_items) >= 3 and not current_visual_has_list and current_visual_block is not None:
                print(f"[BULLET_SYNC_FAIL] Found list in speech (Lines {start_line}-{i}) but previous VISUAL block didn't have **List**.")
                
            current_visual_block = visual_text
            current_visual_has_list = has_list
            speech_since_last_visual = []
            speech_chars = 0
            i = j
            start_line = i
            continue
            
        elif '> [ACTIVITY]' in line:
            # activity block, ignore text length
            j = i + 1
            while j < len(lines) and lines[j].startswith('>'):
                j += 1
            i = j
            start_line = i
            continue
            
        else:
            if not line.startswith('>'): # avoid metadata or other blockquotes if any? actually just standard text
                speech_since_last_visual.append(line)
                speech_chars += count_chinese_chars(line)
        i += 1

    # Check last segment
    if speech_chars > 250:
        print(f"[VISUAL_GAP] Lines {start_line}-{len(lines)}: {speech_chars} chars without visual.")
    
    list_items = re.findall(r'(?:^|\n)\s*(?:\d+\.|-|\*)\s+.*', '\n'.join(speech_since_last_visual))
    if len(list_items) >= 3 and not current_visual_has_list and current_visual_block is not None:
        print(f"[BULLET_SYNC_FAIL] Found list in speech (Lines {start_line}-{len(lines)}) but previous VISUAL block didn't have **List**.")


for f in sorted(glob.glob('/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/src/M*.md')):
    analyze_file(f)

