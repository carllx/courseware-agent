#!/usr/bin/env python3
"""
extract_week.py — 从 course.yaml 运行时提取指定周的教学信息

用法:
    python extract_week.py --week N [--section calendar|objectives|experiments|practice-context|all]
    python extract_week.py --week N --include-concepts

输出到 stdout，供 Agent 工作流按需加载，替代全量加载 51KB course.yaml。
ADR-021 Phase 1 实施工件。ADR-043 扩展 experiments / practice-context / concepts。
"""

import argparse
import os
import sys
import yaml


def load_course(path="course.yaml"):
    """加载课程配置（支持拆分架构 + 巨石文件回退）。

    优先检测 course_meta.yaml + course_calendar.yaml 等拆分文件，
    若存在则合并加载；否则回退到 course.yaml 巨石文件。
    """
    course_dir = os.path.dirname(os.path.abspath(path))

    # 拆分文件清单
    split_files = [
        "course_meta.yaml",
        "course_calendar.yaml",
        "course_objectives.yaml",
        "course_experiments.yaml",
        "course_assessment.yaml",
        "course_textbooks.yaml",
    ]

    meta_path = os.path.join(course_dir, "course_meta.yaml")
    calendar_path = os.path.join(course_dir, "course_calendar.yaml")

    if os.path.exists(meta_path) and os.path.exists(calendar_path):
        merged = {}
        for fname in split_files:
            fpath = os.path.join(course_dir, fname)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                if data:
                    merged.update(data)
        return merged

    # 回退到巨石文件
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


def extract_experiments(data, exp_ids=None):
    """提取实验定义子集。若 exp_ids 为 None 则返回全部实验。"""
    experiments = data.get("experiments", [])
    if exp_ids is None:
        return experiments
    return [e for e in experiments if e.get("id") in exp_ids]


def load_concepts(course_dir, concept_ids=None):
    """从 concept_registry.yaml 加载概念注册表（可选过滤）。"""
    registry_path = os.path.join(course_dir, "concept_registry.yaml")
    if not os.path.exists(registry_path):
        return None
    with open(registry_path, "r", encoding="utf-8") as f:
        reg = yaml.safe_load(f)
    concepts = reg.get("concepts", [])
    if concept_ids is None:
        return concepts
    return [c for c in concepts if c.get("id") in concept_ids]


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
        choices=["calendar", "objectives", "experiments", "practice-context", "all"],
        help="提取的内容段（默认: all）"
    )
    parser.add_argument(
        "--path", "-p", type=str, default="course.yaml",
        help="course.yaml 文件路径（默认: 当前目录下的 course.yaml）"
    )
    parser.add_argument(
        "--include-concepts", action="store_true",
        help="追加 concept_registry.yaml 中的概念子集"
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

    # 提取 calendar（除纯 experiments 模式外均需要）
    cal = None
    if args.section != "experiments":
        cal = extract_calendar(data, args.week)
        if cal is None:
            print(f"错误: 未找到第 {args.week} 周的 calendar 条目", file=sys.stderr)
            sys.exit(1)

    output = {}
    course_dir = os.path.dirname(os.path.abspath(args.path))

    if args.section == "experiments":
        # 纯实验提取模式
        output["experiments"] = extract_experiments(data)

    elif args.section == "practice-context":
        # 一站式实践设计上下文
        output["calendar"] = cal
        supported = cal.get("supported_objectives", [])
        obj = extract_objectives(data, supported)
        if obj:
            output["objectives"] = obj
        # 提取关联实验
        exp_id = cal.get("exp_id")
        if exp_id:
            output["experiments"] = extract_experiments(data, [exp_id])
        output["course_meta"] = extract_course_meta(data)
        # 自动包含 concepts
        concepts = load_concepts(course_dir)
        if concepts:
            output["concepts"] = concepts

    else:
        # 原有逻辑
        if args.section in ("calendar", "all"):
            output["calendar"] = cal

        if args.section in ("objectives", "all"):
            supported = cal.get("supported_objectives", [])
            obj = extract_objectives(data, supported)
            if obj:
                output["objectives"] = obj

        if args.section == "all":
            output["course_meta"] = extract_course_meta(data)

    # 可选追加 concepts
    if args.include_concepts and "concepts" not in output:
        concepts = load_concepts(course_dir)
        if concepts:
            output["concepts"] = concepts

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
