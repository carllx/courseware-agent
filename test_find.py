import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "engines"))
from generate_course_h5 import find_image

course_path = Path("/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化")
print("S02:", find_image(course_path, "![《纽约时报》新冠风险地图](../public/slides/S02_NYT_Covid_Map.jpg)"))
print("S04b:", find_image(course_path, "![哈佛医学院彩虹色带误诊案例](../public/slides/S04b_Harvard_Rainbow_Disaster.png)"))
