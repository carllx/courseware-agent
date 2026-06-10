import os
import re
from pathlib import Path

def main():
    weeks_dir = Path('weeks')
    if not weeks_dir.exists():
        return

    renamed_count = 0
    for root, dirs, files in os.walk(weeks_dir):
        for filename in files:
            new_filename = re.sub(r'实验\s*([1-9]|[一二三四五])(?:\s*\(Exp\s*[1-9]\))?', r'实践项目\1', filename)
            new_filename = re.sub(r'大实验', r'综合实践项目', new_filename)
            new_filename = re.sub(r'实验报告', r'实践报告', new_filename)
            new_filename = re.sub(r'实验指导书', r'实践指导书', new_filename)
            new_filename = re.sub(r'实验项目', r'实践项目', new_filename)
            
            if new_filename != filename:
                old_path = Path(root) / filename
                new_path = Path(root) / new_filename
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
                
    print(f"Renamed {renamed_count} files.")

if __name__ == "__main__":
    main()
