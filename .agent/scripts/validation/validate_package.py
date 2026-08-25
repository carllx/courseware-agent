#!/usr/bin/env python3
"""
validate_package.py — V5 Package 架构校验器

校验 package.yaml 的完整性与一致性：
1. 必填字段存在性（week / status / segments）
2. segments[].src 指向的文件是否存在
3. segment ID 唯一性
4. 编译通过性（可选，通过 --compile 触发）

用法:
    python validate_package.py --course "信息可视化"
    python validate_package.py --file "信息可视化/weeks/W01_Visual_Perception/package.yaml"
    python validate_package.py --course "信息可视化" --compile
"""

import os
import sys
import argparse
import yaml
from pathlib import Path

# 确保能 import 同目录模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
from script_parser import get_workspace_root


REQUIRED_FIELDS = ["week", "segments"]
RECOMMENDED_FIELDS = ["topic", "title", "status", "objectives"]


def validate_single_package(yaml_path: str, compile_check: bool = False) -> dict:
    """校验单个 package.yaml，返回结果字典。"""
    result = {
        "path": yaml_path,
        "errors": [],      # CRITICAL
        "warnings": [],     # WARN
        "info": [],         # INFO
    }

    if not os.path.exists(yaml_path):
        result["errors"].append(f"文件不存在: {yaml_path}")
        return result

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        result["errors"].append(f"YAML 解析失败: {e}")
        return result

    pkg_dir = os.path.dirname(os.path.abspath(yaml_path))

    # 1. 必填字段检查
    for field in REQUIRED_FIELDS:
        if field not in config:
            result["errors"].append(f"缺少必填字段: {field}")

    for field in RECOMMENDED_FIELDS:
        if field not in config:
            result["warnings"].append(f"缺少推荐字段: {field}")

    # 2. segments 完整性检查
    segments = config.get("segments", [])
    if not segments:
        result["errors"].append("segments 阵列为空或缺失")
        return result

    seen_ids = set()
    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            result["errors"].append(f"segments[{i}] 不是字典类型: {seg}")
            continue

        seg_id = seg.get("id", "")
        seg_src = seg.get("src", "")

        # ID 唯一性
        if not seg_id:
            result["warnings"].append(f"segments[{i}] 缺少 id 字段")
        elif seg_id in seen_ids:
            result["errors"].append(f"segments ID 重复: {seg_id}")
        else:
            seen_ids.add(seg_id)

        # src 文件存在性
        if not seg_src:
            result["errors"].append(f"segments[{i}] (id={seg_id}) 缺少 src 路径")
        else:
            full_path = os.path.join(pkg_dir, seg_src)
            if not os.path.exists(full_path):
                result["errors"].append(
                    f"segments[{i}] (id={seg_id}) 源文件不存在: {seg_src}"
                )
            else:
                size = os.path.getsize(full_path)
                if size == 0:
                    result["warnings"].append(
                        f"segments[{i}] (id={seg_id}) 源文件为空: {seg_src}"
                    )
                else:
                    result["info"].append(
                        f"segments[{i}] (id={seg_id}) → {seg_src} ({size:,} bytes)"
                    )

    # 3. 目录结构完整性
    src_dir = os.path.join(pkg_dir, "src")
    public_dir = os.path.join(pkg_dir, "public")
    build_dir = os.path.join(pkg_dir, ".build")

    if not os.path.isdir(src_dir):
        result["errors"].append("缺少 src/ 目录")
    if not os.path.isdir(public_dir):
        result["warnings"].append("缺少 public/ 目录（视觉资产存放区）")
    if not os.path.isdir(build_dir):
        result["info"].append(".build/ 目录不存在（首次编译后自动创建）")

    # 4. src/ 中未注册的孤立文件检测
    if os.path.isdir(src_dir):
        registered_files = {
            os.path.basename(seg.get("src", ""))
            for seg in segments
            if isinstance(seg, dict) and seg.get("src")
        }
        for f in sorted(os.listdir(src_dir)):
            if f.endswith('.md') and f not in registered_files:
                result["warnings"].append(
                    f"src/ 中存在未注册的 Markdown 文件: {f}"
                )

    # 5. 编译验证（可选）
    if compile_check:
        import subprocess
        workspace = get_workspace_root()
        dumptext = os.path.join(workspace, "engines", "dumptext.py")
        if os.path.exists(dumptext):
            proc = subprocess.run(
                [sys.executable, dumptext, yaml_path, "--mode", "full"],
                capture_output=True, text=True,
            )
            if proc.returncode != 0:
                result["errors"].append(
                    f"编译失败:\n{proc.stdout}\n{proc.stderr}"
                )
            else:
                compiled = os.path.join(pkg_dir, ".build", "compiled.md")
                if os.path.exists(compiled):
                    size = os.path.getsize(compiled)
                    result["info"].append(
                        f"编译成功: .build/compiled.md ({size:,} bytes)"
                    )
                else:
                    result["errors"].append("编译器报告成功但产物不存在")
        else:
            result["warnings"].append(f"编译器不存在: {dumptext}")

    return result


def main():
    parser = argparse.ArgumentParser(description="V5 Package 架构校验器")
    parser.add_argument("--course", help="课程目录名")
    parser.add_argument("--file", help="直接指定 package.yaml 路径")
    parser.add_argument("--compile", action="store_true",
                        help="同时验证编译通过性")
    args = parser.parse_args()

    workspace = get_workspace_root()
    targets = []

    if args.file:
        targets.append(args.file)
    elif args.course:
        weeks_dir = os.path.join(workspace, args.course, "weeks")
        if os.path.exists(weeks_dir):
            for entry in sorted(os.listdir(weeks_dir)):
                pkg = os.path.join(weeks_dir, entry, "package.yaml")
                if os.path.exists(pkg):
                    targets.append(pkg)
        if not targets:
            print(f"⚠️  课程 {args.course} 下未找到任何 package.yaml（可能全部为旧架构）")
            sys.exit(0)
    else:
        print("❌ 请指定 --course 或 --file")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"  V5 Package 架构校验报告")
    print(f"{'='*50}")
    print(f"  目标: {len(targets)} 个 package.yaml")
    print(f"{'='*50}\n")

    total_errors = 0
    total_warnings = 0

    for target in targets:
        result = validate_single_package(target, args.compile)
        rel_path = os.path.relpath(target, workspace)

        icon = "✅" if not result["errors"] else "❌"
        print(f"{icon} {rel_path}")

        for err in result["errors"]:
            print(f"   🔴 {err}")
            total_errors += 1
        for warn in result["warnings"]:
            print(f"   🟡 {warn}")
            total_warnings += 1
        for info in result["info"]:
            print(f"   ℹ️  {info}")
        print()

    # 汇总
    print(f"{'─'*50}")
    if total_errors == 0:
        print(f"✅ 校验通过 | {total_warnings} 个警告")
    else:
        print(f"❌ 校验失败 | {total_errors} 个错误, {total_warnings} 个警告")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
