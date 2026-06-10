import json

with open('qa_tasks.json', 'r') as f:
    data = json.load(f)

for i in range(40, 50):
    item = data[i]
    context = item.get('context', '')
    
    # Simple heuristic to check for excessive theory
    # E.g., if there's a huge block of text before 'Best Practices'
    lines = context.split('\n')
    theory_lines = 0
    in_theory = False
    for line in lines:
        if 'Prerequisites' in line or '前置条件' in line or 'WHY' in line:
            in_theory = True
        elif 'Comprehensive Guide' in line or '综合指南' in line or 'Best Practices' in line:
            in_theory = False
        if in_theory:
            theory_lines += 1
            
    print(f"Task {i}: {item.get('workflow_file')} - Theory lines: {theory_lines}")

