import sys
import time

sys.path.append("/Users/yamlam/Downloads/2025-2026-2 课程/.agent/skills/validation_suite/scripts")
from script_parser import parse_script

start = time.time()
print("Starting parse...")
try:
    parse_script("/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W01_Interaction_Basics/src/M02.5_可用性_vs_体验.md")
    print("Success")
except Exception as e:
    print(f"Error: {e}")
print(f"Time taken: {time.time() - start:.3f}s")
