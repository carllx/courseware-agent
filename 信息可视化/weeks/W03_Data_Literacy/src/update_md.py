import re
import os

b03_path = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/briefs/B03_任务抽象_Why框架.md"
with open(b03_path, 'r') as f:
    b03_content = f.read()

# Replace .jpg with .png in B03 for the specific files
b03_content = b03_content.replace("Fig3.1_Task_Abstraction.jpg", "Fig3.1_Task_Abstraction.png")
b03_content = b03_content.replace("Fig3.2_动作的三层拆解.jpg", "Fig3.2_动作的三层拆解.png")
b03_content = b03_content.replace("Fig3.5_Derive差值图.jpg", "Fig3.5_Derive差值图.png")
b03_content = b03_content.replace("Fig3.6_Targets详细树状图.jpg", "Fig3.6_Targets详细树状图.png")
b03_content = b03_content.replace("Fig3.11_Derive_Tree.jpg", "Fig3.11_Derive_Tree.png")

with open(b03_path, 'w') as f:
    f.write(b03_content)
print("Updated B03")

m03_path = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/src/M03_Why_意图识别与重塑魔法.md"
with open(m03_path, 'r') as f:
    m03_content = f.read()

# First replace .jpg with .png for the M03 text
m03_content = m03_content.replace("Fig3.1_Task_Abstraction.jpg", "Fig3.1_Task_Abstraction.png")
m03_content = m03_content.replace("Fig3.2_动作的三层拆解.jpg", "Fig3.2_动作的三层拆解.png")
m03_content = m03_content.replace("Fig3.5_Derive差值图.jpg", "Fig3.5_Derive差值图.png")
m03_content = m03_content.replace("Fig3.6_Targets详细树状图.jpg", "Fig3.6_Targets详细树状图.png")
m03_content = m03_content.replace("Fig3.11_Derive_Tree.jpg", "Fig3.11_Derive_Tree.png")

# Now, we need to merge "> *   **Asset**: ![预览]..." and "> *   **Resource**: ![Munzner Fig...]..."
# The user's pattern: remove Asset line if it's ![预览], and make Resource line into Asset line.
def merge_asset_resource(match):
    # match.group(0) is the entire block including Asset and Resource
    resource_line = match.group(2)
    # Convert "Resource" to "Asset"
    new_asset_line = resource_line.replace("**Resource**:", "**Asset**:")
    return new_asset_line

# Find lines like:
# > *   **Asset**: ![预览](../public/slides/S26_Analyze_Layer.png)
# > *   **Resource**: ![Munzner Fig3.1](../public/textbook/Fig3.1_Task_Abstraction.png)
pattern = r'(> \*\s+\*\*Asset\*\*:\s+!\[预览\]\[.*?\]\n|> \*\s+\*\*Asset\*\*:\s+!\[预览\]\(.*?\)\n)(> \*\s+\*\*Resource\*\*:\s+!\[Munzner.*?\]\(.*?\)\n)'
m03_content = re.sub(pattern, merge_asset_resource, m03_content)

# Also there might be cases where Asset and Resource are separated by other lines, but usually they are adjacent.
# Let's check if there are any remaining "Resource: ![Munzner"
remaining_resources = re.findall(r'> \*\s+\*\*Resource\*\*:\s+!\[Munzner.*?\n', m03_content)
for res in remaining_resources:
    # If any remaining, we just replace "**Resource**:" with "**Asset**:" and remove any preceding Asset: ![预览]
    pass

with open(m03_path, 'w') as f:
    f.write(m03_content)
print("Updated M03")
