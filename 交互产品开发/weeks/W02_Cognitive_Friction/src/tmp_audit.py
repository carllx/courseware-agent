import os
import re

def count_chinese_chars(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n=== Auditing {os.path.basename(filepath)} ===")

    lines = content.split('\n')
    
    visual_indices = []
    for i, line in enumerate(lines):
        if line.startswith('> [VISUAL]'):
            visual_indices.append(i)
            
    if not visual_indices:
        print(f"  [GAP ERROR] No [VISUAL] blocks found in entire file. Total lines: {len(lines)}")
    else:
        # Check from start to first VISUAL
        first_chunk = '\n'.join(lines[0:visual_indices[0]])
        first_chunk_no_activity = re.sub(r'> \[ACTIVITY\].*?(?=\n\n|> \[|\Z)', '', first_chunk, flags=re.DOTALL)
        # remove yaml frontmatter
        first_chunk_no_activity = re.sub(r'^---.*?---\n', '', first_chunk_no_activity, flags=re.DOTALL)
        chars = count_chinese_chars(first_chunk_no_activity)
        if chars > 360:
            print(f"  [GAP ERROR] Start to first [VISUAL] (line {visual_indices[0]+1}): {chars} chars")
        elif chars > 250:
            print(f"  [GAP WARN] Start to first [VISUAL] (line {visual_indices[0]+1}): {chars} chars")
            
        for i in range(len(visual_indices) - 1):
            start = visual_indices[i]
            end = visual_indices[i+1]
            chunk = '\n'.join(lines[start:end])
            
            chunk_no_visual = re.sub(r'^> \[VISUAL\].*?(?=\n\n|> \[)', '', chunk, flags=re.DOTALL)
            chunk_no_activity = re.sub(r'> \[ACTIVITY\].*?(?=\n\n|> \[|\Z)', '', chunk_no_visual, flags=re.DOTALL)
            
            chars = count_chinese_chars(chunk_no_activity)
            if chars > 360:
                print(f"  [GAP ERROR] Between VISUAL at line {start+1} and {end+1}: {chars} chars")
            elif chars > 250:
                print(f"  [GAP WARN] Between VISUAL at line {start+1} and {end+1}: {chars} chars")

        # Check from last VISUAL to end
        last_chunk = '\n'.join(lines[visual_indices[-1]:])
        chunk_no_visual = re.sub(r'^> \[VISUAL\].*?(?=\n\n|> \[|\Z)', '', last_chunk, flags=re.DOTALL)
        chunk_no_activity = re.sub(r'> \[ACTIVITY\].*?(?=\n\n|> \[|\Z)', '', chunk_no_visual, flags=re.DOTALL)
        chars = count_chinese_chars(chunk_no_activity)
        if chars > 360:
            print(f"  [GAP ERROR] From last VISUAL at line {visual_indices[-1]+1} to end: {chars} chars")
        elif chars > 250:
            print(f"  [GAP WARN] From last VISUAL at line {visual_indices[-1]+1} to end: {chars} chars")

    # Match 3 or more bullet points or numbered list items
    list_pattern = re.compile(r'(\n(?:[-*]|\d+\.) .+(\n\s+.*)*){3,}')

    for i in range(len(visual_indices)):
        start = visual_indices[i]
        end = visual_indices[i+1] if i + 1 < len(visual_indices) else len(lines)
        
        visual_block_match = re.search(r'^> \[VISUAL\].*?(?=\n\n|> \[)', '\n'.join(lines[start:]), re.DOTALL)
        visual_block = visual_block_match.group(0) if visual_block_match else ""
        
        chunk = '\n'.join(lines[start:end])
        # Find lists in this chunk
        has_list_in_speech = bool(list_pattern.search(chunk))
        if has_list_in_speech:
            if '**List**' not in visual_block and 'List:' not in visual_block and '**List**:' not in visual_block:
                print(f"  [BULLET SYNC ERROR] Found list in speech after VISUAL at line {start+1}, but no List field in VISUAL block.")

src_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src'
for f in sorted(os.listdir(src_dir)):
    if f.startswith('M') and f.endswith('.md'):
        audit_file(os.path.join(src_dir, f))
