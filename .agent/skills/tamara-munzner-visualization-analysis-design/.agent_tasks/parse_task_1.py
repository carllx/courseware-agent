import json

with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/visualization-analysis-design/.agent_tasks/synthesis_tasks.json') as f:
    data = json.load(f)
    
task = data[1]
print("OUTPUT FILE:", task["output_file"])
print("PROMPT LENGTH:", len(task["prompt"]))
print("CONTEXT LENGTH:", len(task["context"]))
with open('task1_context.txt', 'w') as out:
    out.write(task["context"])
