import sys, os
sys.path.append(".agent/skills/validation_suite/scripts")
import script_parser, validate_visuals
ws = os.path.abspath("信息可视化")
vd = script_parser.get_visuals_dir(ws)
wd = script_parser.get_weeks_asset_dirs(ws, 1)
print(validate_visuals.find_physical_file("public/slides/s14c_basketball.png", vd, wd))
