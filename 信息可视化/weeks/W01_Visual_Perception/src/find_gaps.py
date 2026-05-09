import re
with open('M03_视觉系统_你的认知外接显卡.md', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')
count = 0
for p in paras:
    if p.strip() and not p.startswith('>') and not p.startswith('#'):
        print(f"--- GAP ---")
        print(p[:100])
        count += 1
        if count > 10: break
