import json
data = json.load(open('qa_tasks.json'))
for i in range(40, 43):
    print(f"=== TASK {i} ===")
    print(data[i]['context'])
    print()
