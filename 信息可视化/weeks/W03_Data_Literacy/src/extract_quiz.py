import os
import re
import glob

src_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/src'
out_file = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/practices/materials/W03/quiz_extracted_w03.txt'
week_num = '03'

md_files = sorted(glob.glob(os.path.join(src_dir, 'M*.md')))

global_q_num = 1
output_lines = []
stats = {}

for md_file in md_files:
    basename = os.path.basename(md_file)
    match = re.match(r'(M\d+)', basename)
    if not match:
        continue
    module = match.group(1)
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split content by blocks starting with > [ACTIVITY]
    # Then see if Type is Quiz
    blocks = re.split(r'(?m)^>\s*\[ACTIVITY\]\s*$', content)
    
    module_q_count = 0
    
    for block in blocks[1:]: # First item is text before first [ACTIVITY]
        # Check if Quiz
        if not re.search(r'>\s*(?:\*\s*)?\*\*Type\*\*\:\s*`Quiz`', block):
            continue
            
        module_q_count += 1
        
        # Extract fields
        def extract_field(field_name):
            # matches > **field_name**: value or > * **field_name**: value
            m = re.search(r'>\s*(?:\*\s*)?\*\*' + field_name + r'\*\*\:\s*(.*?)(?=\n>\s*(?:\*\s*)?\*\*|\n(?!\>)|$)', block, re.IGNORECASE | re.DOTALL)
            if m:
                return m.group(1).strip().strip('`')
            return None

        desc = extract_field('Desc')
        q_text = extract_field('Q')
        options_text = extract_field('Options')
        answer = extract_field('Answer')
        explain = extract_field('Explain')
        
        if not q_text or not answer:
            continue
            
        # Determine Type
        q_type = '【单选题】'
        if len(answer.replace(' ', '')) > 1 and all(c in 'ABCDEF' for c in answer.replace(' ', '')):
            q_type = '【多选题】'
        elif not options_text and answer.strip().upper() in ['对', '错', 'T', 'F', 'TRUE', 'FALSE']:
            q_type = '【判断题】'
            
        # Format Options
        formatted_options = []
        if options_text:
            opts = [o.strip() for o in options_text.split('|')]
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for i, opt in enumerate(opts):
                # Remove leading 'A.', 'A、', etc.
                opt = re.sub(r'^[A-Z][\.、\s]+', '', opt).strip()
                if i < len(letters):
                    formatted_options.append(f"{letters[i]}.{opt}")
                    
        # Construct output
        out_str = f"{global_q_num}. [W{week_num}-{module}-Q{module_q_count}]{q_type}{q_text}"
        if formatted_options:
            out_str += "\n" + "\n".join(formatted_options)
        
        answer_clean = answer.replace(' ', '')
        out_str += f"\n答案：{answer_clean}"
        
        if explain:
            # explanation could span multiple lines, remove > prefixes
            explain_clean = re.sub(r'(?m)^>\s*(?:\*\s*)?', '', explain).strip()
            out_str += f"\n答案解析：{explain_clean}"
            
        if desc:
            out_str += f"\n知识点：{desc}"
            
        output_lines.append(out_str)
        global_q_num += 1
        
    stats[module] = module_q_count

# Write output
with open(out_file, 'w', encoding='utf-8') as f:
    f.write("\n\n".join(output_lines))
    f.write("\n")

# Print summary
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"📋 Quiz 提取报告 — 信息可视化 W{week_num}")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"扫描模块数：{len(md_files)} 个")
print(f"提取题目数：{global_q_num - 1} 道\n")
print("按模块分布：")
for mod, count in stats.items():
    print(f"  {mod} — {count} 道")
print(f"\n输出文件：{out_file}")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
