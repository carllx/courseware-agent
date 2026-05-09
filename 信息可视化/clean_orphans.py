import re
import os

log_path = '/tmp/q0a.log'
base_dir = '/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception'

# Collect target relative paths
targets = []
with open(log_path, 'r') as f:
    for line in f:
        if '未被任何脚本引用' in line:
            m = re.search(r'^\s*([^\s]+\.(jpg|png|gif|tsv|xlsx|py|jpeg)) —', line)
            if m:
                targets.append(m.group(1))

# Find and delete
cnt = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        for t in targets:
            if f == os.path.basename(t):
                full_path = os.path.join(root, f)
                os.remove(full_path)
                print(f"Deleted: {full_path}")
                cnt += 1
                break

print(f"Total deleted: {cnt}")
