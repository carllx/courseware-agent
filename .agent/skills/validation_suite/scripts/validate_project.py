#!/usr/bin/env python3
"""
项目级统一验证入口 (Project Validator)

批量运行所有验证器，输出汇总报告。

用法:
    python validate_project.py --course "实习指导"
"""

import os
import sys
import subprocess
import time
import argparse


def run_validator(python: str, script_path: str, description: str,
                  extra_args: list[str] = None, cwd: str = None) -> bool:
    """运行单个验证脚本。"""
    print(f"\n🚀 {description}")
    print(f"   [Script]: {os.path.basename(script_path)}")

    start = time.time()
    cmd = [python, script_path] + (extra_args or [])

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        duration = time.time() - start

        # 打印输出
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")

        if result.returncode == 0:
            print(f"   ✅ 通过 ({duration:.2f}s)")
            return True
        else:
            if result.stderr:
                print(f"   --- 错误 ---")
                for line in result.stderr.strip().split('\n'):
                    print(f"   {line}")
            print(f"   ❌ 未通过 ({duration:.2f}s)")
            return False

    except Exception as e:
        print(f"   ❌ 执行异常: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="项目级统一验证")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--week", type=int, default=None,
                        help="仅验证指定周次（如 --week 1），跳过全局验证器")
    args = parser.parse_args()

    # 路径设置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 推算工作区根目录
    workspace = os.path.abspath(os.path.join(script_dir, *(['..'] * 4)))
    python = sys.executable

    print("🛡️  项目验证套件")
    print("=" * 60)
    print(f"  课程: {args.course}")
    if args.week is not None:
        print(f"  范围: 第 {args.week} 周")
    print(f"  Python: {python}")
    print("=" * 60)

    course_args = ["--course", args.course]
    week_args = ["--week", str(args.week)] if args.week is not None else []

    validators = []

    # 周次模式下跳过全局验证器（与特定周无关）
    if args.week is None:
        validators.append(
            (os.path.join(script_dir, "validate_steps.py"),
             "教学环节时长与规范检查", [args.course, "--root", workspace]))
        validators.append(
            (os.path.join(script_dir, "sync_syllabus.py"),
             "教学大纲同步检查", course_args + ["--check"]))

    validators.extend([
        (os.path.join(script_dir, "validate_spec.py"),
         "规范合规性检查", course_args + week_args),
        (os.path.join(script_dir, "validate_visuals.py"),
         "视觉素材完整性", course_args + week_args),
        (os.path.join(script_dir, "validate_script_length.py"),
         "时长与节奏分析", course_args + week_args + ["--module-breakdown"]),
    ])

    if args.week is None:
        validators.append(
            (os.path.join(script_dir, "validate_knowledge.py"),
             "知识枢纽健康检查", course_args))

    validators.append(
        (os.path.join(script_dir, "validate_package.py"),
         "V5 Package 架构校验", course_args + ["--compile"]))

    validators.append(
        (os.path.join(script_dir, "validate_practice.py"),
         "实践活动 YAML 校验 (ADR 043)", course_args + week_args))

    results = []
    for script, desc, extra in validators:
        if not os.path.exists(script):
            print(f"\n⚠️  脚本不存在: {script}")
            results.append((desc, False))
            continue
        success = run_validator(python, script, desc, extra, cwd=workspace)
        results.append((desc, success))

    # 汇总
    print(f"\n{'='*60}")
    print("📊 验证汇总")
    print(f"{'='*60}")

    all_passed = True
    for desc, success in results:
        status = "✅ 通过" if success else "❌ 未通过"
        print(f"  {status} | {desc}")
        if not success:
            all_passed = False

    if all_passed:
        print(f"\n✨ 所有检查已通过！")
        sys.exit(0)
    else:
        print(f"\n💡 部分检查未通过，请查看上方详细日志。")
        sys.exit(1)


if __name__ == "__main__":
    main()
