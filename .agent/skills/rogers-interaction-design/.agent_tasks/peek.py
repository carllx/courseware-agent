import json

with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json', 'r') as f:
    tasks = json.load(f)

for i in range(3, 6):
    print(f"--- Task {i} ---")
    print(tasks[i]['context'][:500])
