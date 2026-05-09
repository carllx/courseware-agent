import re

log_path = "/Users/yamlam/.gemini/antigravity/brain/95382ba3-1de0-4e9c-a9ea-035699d5f625/.system_generated/logs/overview.txt"
with open(log_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Total Lines: 283" in line and "Total Bytes: 28249" in lines[i+1]:
        start_idx = i + 4
        restored_lines = []
        for j in range(start_idx, len(lines)):
            if "The above content shows the entire, complete file contents" in lines[j]:
                break
            # Remove "line_number: " prefix exactly
            match = re.match(r"^\d+: (.*)$", lines[j].rstrip('\n'))
            if match:
                restored_lines.append(match.group(1))
            else:
                restored_lines.append(lines[j].rstrip('\n'))
        
        out_path = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W02_Design_Principles/src/M03_视觉偏差的陷阱__心理学精度与视觉弹出.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(restored_lines) + "\n")
        print(f"Restored {len(restored_lines)} lines to M03.")
        break
