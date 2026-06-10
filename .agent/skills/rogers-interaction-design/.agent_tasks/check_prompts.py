import json

with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json', 'r') as f:
    tasks = json.load(f)

for i in range(6):
    print(f"Task {i} output: {tasks[i]['output_file']}")
    print(f"Task {i} prompt length: {len(tasks[i]['prompt'])}")
    print(f"Task {i} context length: {len(tasks[i]['context'])}")
