#!/usr/bin/env python3
"""
check_experiment_hours.py — 独立实验学时验证套件

独立读取指定课程目录下动态实验的 `hours` 并对账 `course_meta.yaml`。
"""

import argparse
import sys
import yaml
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="校验实验总学时")
    parser.add_argument("--course", required=True, help="课程目录路径")
    args = parser.parse_args()

    course_dir = Path(args.course)
    meta_file = course_dir / "course_meta.yaml"
    if not meta_file.exists():
        print(f"⏭️  [跳过] 未找到 {meta_file}，可能非新版课程架构。", file=sys.stderr)
        sys.exit(0)
    
    with open(meta_file, "r", encoding="utf-8") as f:
        meta_data = yaml.safe_load(f)

    try:
        expected_practice_hours = meta_data["course"]["hours"]["practice"]
    except (KeyError, TypeError):
        print(f"⚠️  [警告] {meta_file} 中未定义 course.hours.practice 字段，跳过校验。", file=sys.stderr)
        sys.exit(0)

    # 计算动态实验学时
    exp_dir = course_dir / "practices" / "experiments"
    if not exp_dir.exists():
        print(f"⏭️  [跳过] 未找到实验目录 {exp_dir}。", file=sys.stderr)
        sys.exit(0)

    actual_hours = 0
    exp_count = 0
    for exp_file in exp_dir.glob("exp_*.yaml"):
        with open(exp_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict):
                continue
            h = data.get("hours", 0)
            try:
                actual_hours += float(h)
            except ValueError:
                print(f"❌ [错误] 文件 {exp_file.name} 中 'hours' 字段非数值: {h}", file=sys.stderr)
                sys.exit(1)
            exp_count += 1

    # 允许浮点数对比
    expected_theory_hours = meta_data.get("course", {}).get("hours", {}).get("theory", 0)
    if expected_theory_hours == 0:
        if float(actual_hours) > float(expected_practice_hours):
            print(f"❌ [错误] 实验学时对账失败！全实践课程的实验总学时不可超过总实践学时。", file=sys.stderr)
            print(f"   预期 (course.hours.practice): 最大 {expected_practice_hours} 学时", file=sys.stderr)
            print(f"   实际 ({exp_count} 个动态实验求和): {actual_hours} 学时", file=sys.stderr)
            sys.exit(1)
        elif float(actual_hours) < float(expected_practice_hours):
            print(f"⚠️ [警告] 全实践课程实验学时未占满实践学时，剩余实践时间请以平时练习补足。预期 {expected_practice_hours}，实际 {actual_hours} 学时", file=sys.stderr)
    else:
        if float(actual_hours) != float(expected_practice_hours):
            print(f"❌ [错误] 实验学时对账失败！", file=sys.stderr)
            print(f"   预期 (course.hours.practice): {expected_practice_hours} 学时", file=sys.stderr)
            print(f"   实际 ({exp_count} 个动态实验求和): {actual_hours} 学时", file=sys.stderr)
            sys.exit(1)

    print(f"✅ [成功] 实验学时检查完成。总计 {exp_count} 个实验，共 {actual_hours} 学时。")
    sys.exit(0)

if __name__ == "__main__":
    main()
