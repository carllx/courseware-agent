import json
import sys

def main():
    idx = int(sys.argv[1])
    with open('/Users/yamlam/Downloads/carllx-skills/.agent/skills/interaction-design-Rogers/.agent_tasks/synthesis_tasks.json', 'r') as f:
        tasks = json.load(f)
    
    task = tasks[idx]
    print(f"OUTPUT_FILE: {task['output_file']}")
    print(f"PROMPT: {task['prompt']}")
    print(f"CONTEXT: {task['context']}")

if __name__ == '__main__':
    main()
