#!/usr/bin/env python3
import os
import glob
import yaml
from pathlib import Path
import shutil

class CustomDumper(yaml.SafeDumper):
    pass

def represent_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

CustomDumper.add_representer(str, represent_str)

def migrate_course(course_dir):
    course_path = Path(course_dir)
    course_exp_yaml = course_path / "course_experiments.yaml"
    if not course_exp_yaml.exists():
        print(f"Skipping {course_dir}: No course_experiments.yaml found.")
        return

    with open(course_exp_yaml, 'r', encoding='utf-8') as f:
        master_data = yaml.safe_load(f)

    if not master_data or 'experiments' not in master_data:
        print(f"Skipping {course_dir}: 'experiments' key missing.")
        return

    exp_dir = course_path / "practices" / "experiments"
    if not exp_dir.exists():
        print(f"Skipping {course_dir}: {exp_dir} not found.")
        return

    experiments_list = master_data['experiments']
    exp_dict = {str(exp['id']): exp for exp in experiments_list}

    for exp_file in glob.glob(str(exp_dir / "exp_*.yaml")):
        with open(exp_file, 'r', encoding='utf-8') as f:
            local_data = yaml.safe_load(f)
        
        if not local_data or 'exp_id' not in local_data:
            continue
        
        exp_id = str(local_data['exp_id'])
        if exp_id in exp_dict:
            master_exp = exp_dict[exp_id]
            # Merge master_exp into local_data, prioritizing master_exp for overlapping keys
            for k, v in master_exp.items():
                if k == 'id':
                    continue # handled by exp_id
                local_data[k] = v
            
            # Reorder keys to make meta data appear before steps
            ordered_keys = ['exp_id', 'name', 'type', 'hours', 'group_size', 'requirement', 'summary', 'method_theory', 'objectives', 'equipment', 'requirements', 'methods', 'conclusions', 'steps', 'analysis_prompts', 'grading_rubric']
            
            new_data = {}
            for k in ordered_keys:
                if k in local_data:
                    new_data[k] = local_data[k]
            for k, v in local_data.items():
                if k not in new_data:
                    new_data[k] = v
            
            # Write back
            with open(exp_file, 'w', encoding='utf-8') as f:
                yaml.dump(new_data, f, Dumper=CustomDumper, allow_unicode=True, sort_keys=False, width=120)
            print(f"Updated {exp_file}")

    # Remove course_experiments.yaml from course.yaml includes if applicable
    course_yaml_path = course_path / "course.yaml"
    if course_yaml_path.exists():
        with open(course_yaml_path, 'r', encoding='utf-8') as f:
            course_yaml_data = yaml.safe_load(f)
        if isinstance(course_yaml_data, dict) and "includes" in course_yaml_data:
            if "course_experiments.yaml" in course_yaml_data["includes"]:
                course_yaml_data["includes"].remove("course_experiments.yaml")
                with open(course_yaml_path, 'w', encoding='utf-8') as f:
                    yaml.dump(course_yaml_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
                print(f"Removed course_experiments.yaml from {course_yaml_path} includes")

    # Move original to backup
    backup_path = course_path / "course_experiments.yaml.bak"
    shutil.move(course_exp_yaml, backup_path)
    print(f"Renamed {course_exp_yaml} to .bak")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        migrate_course(sys.argv[1])
    else:
        print("Usage: migrate_experiments.py <course_dir>")
