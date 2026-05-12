import sys
import traceback

sys.path.append("/Users/yamlam/Downloads/2025-2026-2 课程/.agent/skills/validation_suite/scripts")
from script_parser import parse_script
import signal

def handler(signum, frame):
    print("Hang detected!")
    traceback.print_stack(frame)
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(3) # 3 seconds timeout

try:
    parse_script("/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W01_Interaction_Basics/src/M02.5_可用性_vs_体验.md")
    print("Success")
except Exception as e:
    print(e)
