#!/bin/bash

for i in {0..5}; do
    echo "Processing task $i..."
    OUTPUT_FILE=$(python3 -c "import json; data=json.load(open('.agent_tasks/synthesis_tasks.json')); print(data[$i]['output_file'])")
    echo "Output file: $OUTPUT_FILE"
    
    # Create the output directory if it doesn't exist
    mkdir -p "$(dirname "$OUTPUT_FILE")"

    # Combine prompt and context and pass to claude
    cat task_${i}_prompt.txt task_${i}_context.txt | claude -p "Based on the provided prompt and context, output ONLY the requested Markdown workflow. Do not include any conversational filler." --tools "" > "$OUTPUT_FILE"
    
    echo "Completed task $i"
done
