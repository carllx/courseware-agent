import json

with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json', 'r') as f:
    tasks = json.load(f)

for i in range(1, 6):
    print(f"Task {i} top_node: {tasks[i]['top_node']}")
