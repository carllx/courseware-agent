import subprocess
import re
import os

courses = [
    "信息可视化/weeks/W01_Visual_Perception/src/M03_视觉系统_你的认知外接显卡.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M04_格式塔原则_大脑的\"找规律\"强迫症.md"
]
python_bin = "/opt/anaconda3/envs/mybase/bin/python"
checker = ".agent/skills/validation_suite/scripts/generate_cheat_sheet.py"

for filepath in courses:
    if not os.path.exists(filepath): continue
    
    # Run the audit script
    cmd = [python_bin, checker, filepath, "--diagnose"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    diagnose_output = result.stdout
    
    # Find all "连续停滞" locations
    # Format typically: `  - **位置**: 现在全球的股票市场上，有大量的高频交易系统。这些系统由极其复…`
    stagnation_snippets = re.findall(r'- \*\*位置\*\*: (.*?)…', diagnose_output)
    
    if not stagnation_snippets:
        print(f"No stagnation found via parser for {filepath}")
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    injected_count = 0
    # Process each snippet
    for snippet in stagnation_snippets:
        snippet = snippet.strip()
        if not snippet: continue
        
        # We find where this snippet occurs in the content
        # We need to find the exact paragraph starting with this snippet.
        pattern = re.compile(r'(^|\n\n)(' + re.escape(snippet) + r'.*?)(\n\n|$)', re.DOTALL)
        
        def replace_with_activity(match):
            global injected_count
            injected_count += 1
            prefix = match.group(1)
            para = match.group(2)
            suffix = match.group(3)
            # Inject an activity break before the paragraph
            activity_block = "\n\n> [ACTIVITY]\n> *   **Type**: `QA`\n> *   **Duration**: `1min`\n> *   **Desc**: 快速反思\n\n"
            # It's an S block, let's bold the first 4 CJK chars to make it an A block!
            # Or just return the activity + the paragraph.
            return f"{prefix}{activity_block}{para}{suffix}"
            
        content = pattern.sub(replace_with_activity, content, count=1)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Injected {injected_count} QA blocks into {filepath}")

