import shutil
import os

src_dir = "/Users/yamlam/Downloads/eeeeeee"
dst_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W03_Data_Literacy/public/textbook"

mappings = {
    "3.1.png": "Fig3.1_Task_Abstraction.png",
    "3.2.png": "Fig3.2_动作的三层拆解.png",
    "3.5.png": "Fig3.5_Derive差值图.png",
    "3.6.png": "Fig3.6_Targets详细树状图.png",
    "3.10.png": "Fig3.11_Derive_Tree.png"
}

for src_name, dst_name in mappings.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_name} -> {dst_name}")
    else:
        print(f"Warning: {src_path} not found")
