import sys, json
idx = int(sys.argv[1])
with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json', 'r') as f:
    tasks = json.load(f)
task = tasks[idx]
print(f"OUTPUT_FILE: {task.get('output_file', '')}")
print(f"PROMPT:\n{task.get('prompt', '')}")
print(f"CONTEXT:\n{task.get('context', '')}")
