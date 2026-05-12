import sys
import os

sys.path.append("/Users/yamlam/Downloads/2025-2026-2 课程/.agent/skills/validation_suite/scripts")

from script_parser import parse_script

# Test 1: M04 file (should pass since we fixed it)
file_path = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W03_Product_Insights/src/M04_讲授二_JTBD_框架与需求的维度剥离.md"
try:
    blocks = parse_script(file_path)
    print("Test 1 (M04): PASS (Parsed correctly)")
except ValueError as e:
    print(f"Test 1 (M04): FAILED. {e}")

# Test 2: Fake bad file with stray text
with open("fake_stray_script.md", "w") as f:
    f.write("> [VISUAL]\n> **Slide**: test\n> 这一行是夹带的私货！")

try:
    blocks = parse_script("fake_stray_script.md")
    print("Test 2 (Fake Stray): FAILED (Did not raise error)")
except ValueError as e:
    print(f"Test 2 (Fake Stray): PASS (Caught stray text). Message: {e}")

if os.path.exists("fake_stray_script.md"):
    os.remove("fake_stray_script.md")
