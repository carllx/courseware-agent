import json
with open("/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json") as f:
    data = json.load(f)
for i in range(6):
    print(f"Task {i}: context lines={len(data[i]['context'].splitlines())}")
