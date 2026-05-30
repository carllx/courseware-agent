import json
import os
import glob
import re

brain_dir = "/Users/yamlam/.gemini/antigravity/brain/"
targets = ["M00", "M01", "M05"]

for jsonl_file in glob.glob(os.path.join(brain_dir, "*/.system_generated/logs/transcript.jsonl")):
    try:
        with open(jsonl_file, 'r') as f:
            for line in f:
                step = json.loads(line)
                if step.get("type") == "TOOL_OUTPUT" and step.get("source") == "SYSTEM":
                    content = step.get("content", "")
                    if "The following code has been modified to include a line number" in content:
                        for t in targets:
                            if f"src/{t}" in content or f"{t}_" in content:
                                print(f"Found {t} in {jsonl_file}")
                                # extract the file path
                                match = re.search(r'File Path: `file://(.*?)`', content)
                                if match:
                                    file_path = match.group(1)
                                    if t in file_path:
                                        print(f"  Path: {file_path}")
                                        # extract the lines
                                        lines = content.split("leading space.\n")[1].split("\nThe above content")[0].split('\n')
                                        file_content = []
                                        for l in lines:
                                            # remove line number prefix like "1: "
                                            l = re.sub(r'^\d+:\s?', '', l)
                                            file_content.append(l)
                                        with open(f"{t}_recovered.md", "w") as outf:
                                            outf.write("\n".join(file_content))
                                        print(f"  Saved {t}_recovered.md")
    except Exception as e:
        pass
