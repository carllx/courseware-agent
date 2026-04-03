#!/usr/bin/env python3
"""
extract_week.py — 从 course.yaml 运行时提取指定周的教学信息

用法:
    python extract_week.py --week N [--section calendar|objectives|all]

输出到 stdout，供 Agent 工作流按需加载，替代全量加载 51KB course.yaml。
ADR-021 Phase 1 实施工件。
"""

import argparse
import sys
import yaml


def load_course(path="course.yaml"):
    """加载 course.yaml 并返回解析后的字典"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_calendar(data, week_num):
    """提取指定周的 calendar 条目"""
    calendar = data.get("calendar", [])
    for entry in calendar:
        if entry.get("week") == week_num:
            return entry
    return None


def extract_objectives(data, supported_ids):
    """
    根据 supported_objectives 列表（如 ["知识1", "能力2"]）
    提取匹配的 objectives 子集
    """
    if not supported_ids:
        return {}

    objectives_data = data.get("objectives", {})
    result = {}

    # 解析 supported_objectives 中的引用，如 "知识1" → (knowledge, 1)
    type_map = {
        "知识": "knowledge",
        "能力": "ability",
        "素质": "quality",
    }

    for ref in supported_ids:
        for cn_prefix, en_key in type_map.items():
            if ref.startswith(cn_prefix):
                try:
                    idx = int(ref[len(cn_prefix):])
                except ValueError:
                    continue
                items = objectives_data.get(en_key, [])
                for item in items:
                    if item.get("index") == idx:
                        if en_key not in result:
                            result[en_key] = []
                        result[en_key].append(item)
                break

    return result


def extract_course_meta(data):
    """提取课程基本元信息（名称、学期、学时配置）"""
    course = data.get("course", {})
    return {
        "name": course.get("name"),
        "semester": course.get("semester"),
        "hours": course.get("hours"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="从 course.yaml 提取指定周的教学信息"
    )
    parser.add_argument(
        "--week", "-w", type=int, required=True,
        help="目标周次（1-15）"
    )
    parser.add_argument(
        "--section", "-s", type=str, default="all",
        choices=["calendar", "objectives", "all"],
        help="提取的内容段（默认: all）"
    )
    parser.add_argument(
        "--path", "-p", type=str, default="course.yaml",
        help="course.yaml 文件路径（默认: 当前目录下的 course.yaml）"
    )
    args = parser.parse_args()

    # 加载数据
    try:
        data = load_course(args.path)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {args.path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"错误: YAML 解析失败 — {e}", file=sys.stderr)
        sys.exit(1)

    # 提取 calendar
    cal = extract_calendar(data, args.week)
    if cal is None:
        print(f"错误: 未找到第 {args.week} 周的 calendar 条目", file=sys.stderr)
        sys.exit(1)

    output = {}

    if args.section in ("calendar", "all"):
        output["calendar"] = cal

    if args.section in ("objectives", "all"):
        supported = cal.get("supported_objectives", [])
        obj = extract_objectives(data, supported)
        if obj:
            output["objectives"] = obj

    if args.section == "all":
        output["course_meta"] = extract_course_meta(data)

    # 输出 YAML
    yaml.dump(
        output,
        sys.stdout,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )


if __name__ == "__main__":
    main()
