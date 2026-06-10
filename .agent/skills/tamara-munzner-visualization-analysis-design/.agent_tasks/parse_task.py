import json
with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/visualization-analysis-design/.agent_tasks/synthesis_tasks.json') as f:
    data = json.load(f)
    task = data[1]
    with open('task.json', 'w') as out:
        json.dump(task, out, indent=2, ensure_ascii=False)
