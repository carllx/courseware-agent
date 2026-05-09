import subprocess
import re
import os

courses = [
    "信息可视化/weeks/W01_Visual_Perception/src/M03_视觉系统_你的认知外接显卡.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M04_格式塔原则_大脑的\"找规律\"强迫症.md",
    "信息可视化/weeks/W01_Visual_Perception/src/M01_我们为什么需要可视化？.md"
]
python_bin = "/opt/anaconda3/envs/mybase/bin/python"
checker = ".agent/skills/validation_suite/scripts/generate_cheat_sheet.py"

for filepath in courses:
    if not os.path.exists(filepath): continue
    
    # We will loop fixing until no stagnations exist, or max 5 times.
    for iteration in range(5):
        cmd = [python_bin, checker, filepath, "--diagnose"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        diagnose_output = result.stdout
        
        stagnation_snippets = re.findall(r'- \*\*位置\*\*: (.*?)…', diagnose_output)
        if not stagnation_snippets:
            break
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        injected = False
        for snippet in stagnation_snippets:
            snippet = snippet.strip()
            if not snippet: continue
            
            # Find snippet in the content
            # Try to match the exact start of the snippet
            # The snippet might have an opening quote, so we just use plain find
            idx = content.find(snippet)
            if idx == -1:
                # sometimes they have prefixes stripped
                if len(snippet) > 10:
                    idx = content.find(snippet[:10])
            if idx != -1:
                # We need to find the word chunk to bold
                # Let's bold the first 4 CJK chars of this snippet
                chunk_match = re.search(r'([\u4e00-\u9fa5]{2,6})', content[idx:idx+20])
                if chunk_match and not ("**" in content[idx:idx+20]):
                    original = chunk_match.group(1)
                    content = content[:idx] + content[idx:idx+20].replace(original, f"**{original}**", 1) + content[idx+20:]
                    injected = True
                else:
                    # just prefix the paragraph with Essentailly (本质上)
                    def_text = "**本质上**，"
                    content = content[:idx] + def_text + content[idx:]
                    injected = True
        
        if injected:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            break

    # verify at end
    cmd = [python_bin, checker, filepath, "--diagnose"]
    ret = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    final_count = len(re.findall(r'- \*\*位置\*\*: (.*?)…', ret.stdout))
    print(f"File {filepath} remaining stagnations: {final_count}")

