#!/usr/bin/env python3
"""
validate_runner.py — H5 Craft-room 统一验证管线入口

在 Vite P1 管线中被调用，串行执行验证器并输出结构化 JSON。
遵循 audit.md 的 Q3 短路规则：字数未达标时隐藏视觉检查。

用法:
    python validate_runner.py --course "交互产品开发" --week 3

输出:
    JSON 到 stdout，格式：
    {
        "course": "交互产品开发",
        "week": 3,
        "timestamp": "...",
        "validators": {
            "length": { "status": "pass|warn|fail", "modules": [...] },
            "visuals": { "status": "pass|warn|fail", "missing": [...], "orphaned": [...] },
            "spec": { "status": "pass|warn|fail", "errors": [...], "warnings": [...] }
        },
        "gateLevel": 0|1|2  // 渐进门控级别
    }
"""

import sys
import os
import json
import argparse
from datetime import datetime

# 确保同目录模块可导入
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from script_parser import (
    parse_script, BlockType, get_workspace_root,
    get_scripts_dir, get_visuals_dir, get_weeks_asset_dirs,
    list_script_files_for_week, list_script_files,
    load_course_config,
)


def run_length_validator(scripts_dir: str, files: list[str], cn_cpm: int) -> dict:
    """执行字数验证，返回结构化结果。"""
    # 直接导入核心函数，避免解析 CLI 输出
    from validate_script_length import analyze_modules, detect_dilution
    import math

    modules_result = []
    count_pass = count_warn = count_fail = 0

    for fname in files:
        fpath = os.path.join(scripts_dir, fname)
        if not os.path.exists(fpath):
            continue

        modules = analyze_modules(fpath, cn_cpm)
        if not modules:
            continue

        for mod in modules:
            fill = mod.get("fill_ratio")
            dilution = detect_dilution(mod)

            if fill is not None:
                if fill >= 1.0:
                    status = "pass"
                    count_pass += 1
                elif fill >= 0.8:
                    status = "warn"
                    count_warn += 1
                else:
                    status = "fail"
                    count_fail += 1
            elif mod.get("is_exempt", False):
                status = "exempt"
            else:
                status = "unknown"

            # 人文标签密度
            oral_tags = mod.get("oral_tag_count", 0)
            budget = mod.get("budget_chars", 0)
            cn_count = mod.get("cn_count", 0)
            if budget:
                required_tags = math.ceil(budget / 2000)
            elif cn_count > 1000:
                required_tags = math.ceil(cn_count / 2000)
            else:
                required_tags = 0

            modules_result.append({
                "file": fname,
                "module": mod["name"],
                "cnCount": mod["cn_count"],
                "budget": mod.get("budget_chars"),
                "fillRatio": round(fill, 3) if fill is not None else None,
                "status": status,
                "oralTags": oral_tags,
                "requiredTags": required_tags,
                "tagDeficit": max(0, required_tags - oral_tags),
                "isDiluted": dilution.get("is_diluted", False),
                "isDegenerated": dilution.get("is_degenerated", False),
                "degenReasons": dilution.get("degen_reasons", []),
                "isDraft": mod.get("status") == "draft",
            })

    # 汇总状态
    if count_fail > 0:
        overall = "fail"
    elif count_warn > 0:
        overall = "warn"
    else:
        overall = "pass"

    return {
        "status": overall,
        "summary": {"pass": count_pass, "warn": count_warn, "fail": count_fail},
        "modules": modules_result,
    }


def run_visuals_validator(course_name: str, scripts_dir: str,
                          files: list[str], week: int = None) -> dict:
    """执行视觉素材验证，返回结构化结果。"""
    from validate_visuals import collect_visual_refs, collect_physical_assets, match_slide_id

    workspace = get_workspace_root()
    visuals_dir = get_visuals_dir(workspace, course_name)
    weeks_dirs = get_weeks_asset_dirs(workspace, course_name)
    if week is not None:
        week_prefix = f"W{week:02d}_"
        weeks_dirs = [d for d in weeks_dirs if week_prefix in d]

    refs = collect_visual_refs(scripts_dir, files)
    physical = collect_physical_assets(visuals_dir, weeks_dirs)

    matched = []
    missing = []
    referenced_files = set()

    for ref in refs:
        asset_path = ref.get("asset", "")
        sid = ref.get("slide_id", "")

        if asset_path:
            full_path = os.path.join(visuals_dir, asset_path)
            if os.path.exists(full_path):
                referenced_files.add(asset_path)
                matched.append(ref)
                continue
            found = False
            for wdir in (weeks_dirs or []):
                candidate = os.path.join(wdir, asset_path)
                if os.path.exists(candidate):
                    referenced_files.add(asset_path)
                    matched.append(ref)
                    found = True
                    break
                for prefix in ["public/", "assets/"]:
                    if asset_path.startswith(prefix):
                        stripped = asset_path[len(prefix):]
                        if os.path.exists(os.path.join(wdir, stripped)):
                            referenced_files.add(asset_path)
                            matched.append(ref)
                            found = True
                            break
                if found:
                    break
            if found:
                continue

        match = match_slide_id(sid, physical)
        if match:
            referenced_files.add(match)
            matched.append(ref)
        else:
            missing.append(ref)

    orphaned = [f for f in physical if f not in referenced_files]

    return {
        "status": "fail" if missing else ("warn" if orphaned else "pass"),
        "summary": {
            "total": len(refs),
            "matched": len(matched),
            "missing": len(missing),
            "orphaned": len(orphaned),
        },
        "missing": [
            {
                "slideId": m.get("slide_id", ""),
                "asset": m.get("asset", ""),
                "file": m.get("file", ""),
                "line": m.get("line", 0),
            }
            for m in missing
        ],
        "orphaned": orphaned[:20],  # 限制输出量
    }


def run_spec_validator(scripts_dir: str, files: list[str]) -> dict:
    """执行规范合规性验证，返回结构化结果。"""
    from validate_spec import validate_single_script

    all_errors = []
    all_warnings = []
    file_results = []

    for fname in files:
        fpath = os.path.join(scripts_dir, fname)
        if not os.path.exists(fpath):
            continue

        result = validate_single_script(fpath, fname)

        file_results.append({
            "file": fname,
            "errors": len(result["errors"]),
            "warnings": len(result["warnings"]),
            "stats": {
                "visualCount": result["stats"]["visual_count"],
                "activityCount": result["stats"]["activity_count"],
                "techTags": result["stats"]["tech_tags"],
                "humanTags": result["stats"]["human_tags"],
            },
        })

        for e in result["errors"]:
            all_errors.append({"file": fname, "message": e})
        for w in result["warnings"]:
            all_warnings.append({"file": fname, "message": w})

    return {
        "status": "fail" if all_errors else ("warn" if all_warnings else "pass"),
        "summary": {"errors": len(all_errors), "warnings": len(all_warnings)},
        "errors": all_errors[:30],
        "warnings": all_warnings[:30],
        "files": file_results,
    }


def determine_gate_level(length_result: dict) -> int:
    """渐进门控判定（遵循 audit.md Q3 短路规则）。

    返回:
        0 = 全开（字数达标，显示所有检查）
        1 = 部分开放（字数偏薄，显示视觉但标记）
        2 = 字数优先（严重不足，隐藏视觉检查结果）
    """
    if length_result["status"] == "fail":
        return 2
    elif length_result["status"] == "warn":
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="H5 Craft-room 统一验证管线")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--week", type=int, default=None, help="仅验证指定周次")
    parser.add_argument("--skip-spec", action="store_true",
                        help="跳过规范检查（加速模式）")
    args = parser.parse_args()

    workspace = get_workspace_root()
    scripts_dir = get_scripts_dir(workspace, args.course)
    course_config = load_course_config(workspace, args.course)

    # 语速常量
    cn_cpm = course_config.get("tts", {}).get("speed_override",
             course_config.get("course", {}).get("cn_cpm", 180))

    # 发现脚本
    if args.week is not None:
        files = list_script_files_for_week(scripts_dir, args.week)
    else:
        files = list_script_files(scripts_dir)

    if not files:
        # 无脚本时输出空结果
        print(json.dumps({
            "course": args.course,
            "week": args.week,
            "timestamp": datetime.now().isoformat(),
            "validators": {},
            "gateLevel": 0,
        }, ensure_ascii=False))
        return

    # 串行执行验证器
    length_result = run_length_validator(scripts_dir, files, cn_cpm)
    gate_level = determine_gate_level(length_result)

    visuals_result = run_visuals_validator(
        args.course, scripts_dir, files, args.week
    )

    spec_result = None
    if not args.skip_spec:
        spec_result = run_spec_validator(scripts_dir, files)

    # 组装输出
    output = {
        "course": args.course,
        "week": args.week,
        "timestamp": datetime.now().isoformat(),
        "validators": {
            "length": length_result,
            "visuals": visuals_result,
        },
        "gateLevel": gate_level,
    }
    if spec_result:
        output["validators"]["spec"] = spec_result

    print(json.dumps(output, ensure_ascii=False, indent=2))

    # 退出码：任一验证器 fail 则非 0
    has_fail = any(
        v.get("status") == "fail"
        for v in output["validators"].values()
    )
    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
