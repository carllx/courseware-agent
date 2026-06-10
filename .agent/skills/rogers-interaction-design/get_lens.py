import json
with open("/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json") as f:
    data = json.load(f)
for i in range(6):
    print(f"Task {i}: prompt len={len(data[i]['prompt'])}, context len={len(data[i]['context'])}")
