import sys
import os
import glob

sys.path.append("/Users/yamlam/Downloads/2025-2026-2 课程/.agent/skills/validation_suite/scripts")
from script_parser import parse_script

courses = [
    "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发",
    "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化"
]

failed_files = []
total_files = 0

for course in courses:
    pattern = os.path.join(course, "weeks", "*", "src", "*.md")
    files = glob.glob(pattern)
    for f in files:
        if os.path.basename(f).startswith('.'):
            continue
        total_files += 1
        print(f"Parsing: {f}", flush=True)
        try:
            parse_script(f)
        except ValueError as e:
            failed_files.append((f, str(e)))
        except Exception as e:
            failed_files.append((f, f"Other Error: {e}"))

with open("/Users/yamlam/Downloads/2025-2026-2 课程/scan_results.txt", "w") as out:
    if not failed_files:
        out.write("No errors found.\n")
    for f, err in failed_files:
        out.write(f"File: {f}\nError: {err}\n\n")

print(f"Total processed: {total_files}, Total failures: {len(failed_files)}")
