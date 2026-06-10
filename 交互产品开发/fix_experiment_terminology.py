import os
import re
from pathlib import Path

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace specific experiment references like 实验1(Exp1), 实验一, 实验 1
    content = re.sub(r'实验\s*([1-9]|[一二三四五])(?:\s*\(Exp\s*[1-9]\))?', r'实践项目\1', content)
    
    # Replace compound words strictly related to course assignments (avoiding 实验室, 心理学实验)
    content = re.sub(r'大实验', r'综合实践项目', content)
    content = re.sub(r'实验报告', r'实践报告', content)
    content = re.sub(r'实验指导书', r'实践指导书', content)
    content = re.sub(r'实验教学', r'实践教学', content)
    content = re.sub(r'实验项目', r'实践项目', content)
    content = re.sub(r'实验说明', r'实践说明', content)
    content = re.sub(r'实验目标', r'实践目标', content)
    content = re.sub(r'实验要求', r'实践要求', content)
    content = re.sub(r'实验总结', r'实践总结', content)
    content = re.sub(r'实验材料', r'实践材料', content)
    content = re.sub(r'实验成果', r'实践成果', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    weeks_dir = Path('weeks')
    if not weeks_dir.exists():
        print("weeks directory not found.")
        return

    modified_count = 0
    for root, _, files in os.walk(weeks_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.md.bak'):
                filepath = Path(root) / file
                if process_file(filepath):
                    modified_count += 1
                    print(f"Modified: {filepath}")
    
    print(f"\nDone. Modified {modified_count} files.")

if __name__ == "__main__":
    main()
