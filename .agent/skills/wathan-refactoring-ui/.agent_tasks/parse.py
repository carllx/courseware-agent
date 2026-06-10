import json

with open('qa_tasks.json', 'r') as f:
    data = json.load(f)

for i in range(40, 50):
    item = data[i]
    print(f"=== TASK {i} ===")
    print(f"File: {item.get('workflow_file')}")
    print(f"Prompt: {item.get('prompt')}")
    print(f"Context: {item.get('context')}")
    print("\n\n")

