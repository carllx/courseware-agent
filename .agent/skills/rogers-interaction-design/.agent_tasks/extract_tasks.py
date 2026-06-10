import json, os

output_dir = '/Users/yamlam/.gemini/antigravity/brain/d05ba123-b94c-4a55-9bd9-c5b3600ed89f/scratch'
os.makedirs(output_dir, exist_ok=True)

with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json', 'r') as f:
    tasks = json.load(f)

for i in range(6, 12):
    task = tasks[i]
    with open(f'{output_dir}/task_{i}.txt', 'w') as f:
        f.write(f"OUTPUT_FILE: {task.get('output_file', '')}\n")
        f.write(f"PROMPT: {task.get('prompt', '')}\n")
        f.write(f"CONTEXT: {task.get('context', '')}\n")
