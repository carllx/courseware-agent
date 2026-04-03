import os
import re
import yaml
import shutil
import glob
from pathlib import Path
import sys

def process_directory(base_dir):
    script_path = os.path.join(base_dir, "script.md")
    if not os.path.exists(script_path):
        print(f"Skipping {base_dir}, no script.md found.")
        return
    
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Parse frontmatter
    match = re.search(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        print(f"Failed to find frontmatter in {script_path}")
        return
    
    fm_text = match.group(1)
    body = match.group(2)
    
    try:
        fm = yaml.safe_load(fm_text)
    except Exception as e:
        print(f"Error parsing YAML in {script_path}: {e}")
        return
    
    print(f"Processing: {base_dir}")
    # Create src dir
    src_dir = os.path.join(base_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    
    # 2. Split body
    # Regex splits by "## 模块 X" or "## Module X"
    parts = re.split(r'\n##\s+(?:模块|Module)\s+(\d+)[：:]?\s*', '\n' + body)
    
    m00_content = parts[0].strip()
    segments = []
    
    # Write M00
    m00_path = os.path.join(src_dir, "M00_课程导览.md")
    
    # Replace links in M00
    m00_content = re.sub(r'\]\((\.\/)?assets\/', '](../public/', m00_content)
    m00_content = re.sub(r'src=["\'](\.\/)?assets\/', 'src="../public/', m00_content)
    
    with open(m00_path, "w", encoding="utf-8") as f:
        f.write(m00_content + "\n")
    
    segments.append({"id": "M00", "src": "src/M00_课程导览.md"})
    
    # Process other parts
    for i in range(1, len(parts), 2):
        mod_numstr = parts[i]
        mod_num = int(mod_numstr)
        mod_text = parts[i+1]
        
        lines = mod_text.strip().split('\n')
        title_line = lines[0]
        rest = '\n'.join(lines[1:])
        
        clean_title = re.sub(r'\(.*?\)|（.*?）', '', title_line)
        clean_title = re.sub(r'[ \-—:：/\\+?？]+', '_', clean_title).strip('_')
        
        filename = f"M{mod_num:02d}_{clean_title}.md"
        filepath = os.path.join(src_dir, filename)
        
        full_mod_text = f"## 模块 {mod_num}: {title_line}\n{rest}\n"
        full_mod_text = re.sub(r'\]\((\.\/)?assets\/', '](../public/', full_mod_text)
        full_mod_text = re.sub(r'src=["\'](\.\/)?assets\/', 'src="../public/', full_mod_text)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_mod_text)
            
        segments.append({"id": f"M{mod_num:02d}", "src": f"src/{filename}"})
        
    # 3. Create package.yaml
    package_data = {
        "week": fm.get("week", ""),
        "topic": fm.get("title", ""),
        "title": fm.get("title", ""),
        "theory_hours": fm.get("theory_hours", 3),
        "practice_hours": fm.get("practice_hours", 2),
        "objectives": fm.get("objectives", []),
        "created": fm.get("created", "2026-03-30"),
        "status": "ready",
        "tags": fm.get("tags", []),
        "delivery_mode": fm.get("delivery_mode", "Lecture + Workshop"),
        "core_theories": fm.get("core_theories", []),
        "segments": segments
    }
    
    package_path = os.path.join(base_dir, "package.yaml")
    with open(package_path, "w", encoding="utf-8") as f:
        yaml.dump(package_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
    # 4. Rename assets -> public
    assets_dir = os.path.join(base_dir, "assets")
    public_dir = os.path.join(base_dir, "public")
    if os.path.exists(assets_dir):
        if not os.path.exists(public_dir):
            os.rename(assets_dir, public_dir)
        else:
            print(f"Warning: both assets and public exist in {base_dir}! Contents not moved automatically.")
            
    # 5. Backup script.md
    bak_path = script_path + ".bak"
    os.rename(script_path, bak_path)
    
    print(f"Success for {base_dir}!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python refactor_modules.py <target_directory_which_contains_W0X>")
        sys.exit(1)
        
    base_dir = sys.argv[1]
    
    # Process the direct folder if it has script.md, or children matching W*
    if os.path.exists(os.path.join(base_dir, "script.md")):
        process_directory(base_dir)
    else:
        for d in glob.glob(os.path.join(base_dir, "W*")):
            if os.path.isdir(d):
                process_directory(d)

if __name__ == "__main__":
    main()
