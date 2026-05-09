import re
from collections import Counter

with open('/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W02_Design_Principles/src/M05_认知审计实验室__三阶段对比实验.md', 'r') as f:
    text = f.read()

# Split into sentences or clauses
clauses = re.split(r'[。！？；\n]', text)
clauses = [c.strip() for c in clauses if len(c.strip()) > 8]

counts = Counter(clauses)
for k, v in counts.items():
    if v > 1 and not k.startswith('> *'):
        print(f"Count {v}: {k}")

