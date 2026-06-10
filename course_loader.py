#!/usr/bin/env python3
"""
course_loader.py — 课程数据透明合并层

从课程目录加载完整的课程数据。支持两种格式：
  1. 旧版单体 course.yaml（直接返回）
  2. 新版索引式 course.yaml + 多个 course_*.yaml 子文件（深度合并后返回）

核心 API:
  load_course(course_dir)        → dict  # 完整课程数据
  load_course_section(course_dir, section) → dict  # 按域加载

设计原则:
  - 零外部依赖（仅 pyyaml + pathlib）
  - 向后兼容：旧格式无 includes 字段时直接返回
  - 返回的字典结构与旧版 yaml.safe_load() 完全一致

ADR-044 Phase 1 实施工件。
"""

import yaml
from pathlib import Path
from typing import Union


import re

def _load_experiments_dynamic(course_dir: Path) -> list:
    """动态从 practices/experiments/ 目录下加载单个实验 YAML 并合并"""
    exp_dir = course_dir / "practices" / "experiments"
    if not exp_dir.exists():
        return []
    
    experiments = []
    for exp_file in exp_dir.glob("exp_*.yaml"):
        with open(exp_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict):
                continue

            exp_id = data.get("exp_id") or data.get("id")
            if exp_id is None:
                raise ValueError(f"缺少实验 ID: 文件 {exp_file.name} 缺失 'exp_id' 或 'id' 字段")
                
            match = re.search(r'\d+', str(exp_id))
            if not match:
                raise ValueError(f"无效的实验 ID: 文件 {exp_file.name} 的标识符 '{exp_id}' 不包含任何数字，无法用于排序")
            
            # 向后兼容：旧汇总表用 id 字段，增量表用 exp_id 字段
            if "id" not in data:
                data["id"] = exp_id
            
            data["_sort_key"] = int(match.group())
            experiments.append(data)
    
    experiments.sort(key=lambda x: x.pop("_sort_key"))
    return experiments


# 域到子文件的映射（用于 load_course_section 的按需加载）
SECTION_FILE_MAP = {
    "meta": "course_meta.yaml",
    "calendar": "course_calendar.yaml",
    "objectives": "course_objectives.yaml",
    "textbooks": "course_textbooks.yaml",
    "experiments": "course_experiments.yaml",
    "assessment": "course_assessment.yaml",
}

# 域到顶层键的映射（用于从旧格式中过滤特定域）
SECTION_KEYS_MAP = {
    "meta": ["course", "teacher", "student_analysis", "semester_config", "agent"],
    "calendar": ["calendar"],
    "objectives": ["objectives"],
    "textbooks": ["textbooks"],
    "experiments": ["experiments"],
    "assessment": ["assessment_methods", "exams"],
}

# 新格式索引文件中不参与合并的保留键
_RESERVED_KEYS = {"_schema_version", "includes"}


def load_course(course_dir: Union[str, Path]) -> dict:
    """
    从课程目录加载完整的课程数据。

    1. 读取 course_dir/course.yaml 索引文件
    2. 若含 includes 字段，解析列表并深度合并所有子文件
    3. 返回与旧版单文件完全相同的字典结构

    向后兼容：如果 course.yaml 不含 includes 字段，
    直接作为传统单文件返回。

    参数:
        course_dir: 课程根目录路径（如 "信息可视化/"）

    返回:
        配置字典（与旧版 yaml.safe_load() 结果结构相同）

    异常:
        FileNotFoundError: course.yaml 或子文件不存在
        ValueError: 子文件间存在重复键
        yaml.YAMLError: YAML 解析失败
    """
    course_dir = Path(course_dir)
    index_path = course_dir / "course.yaml"

    if not index_path.exists():
        raise FileNotFoundError(f"课程配置文件缺失: {index_path}")

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = yaml.safe_load(f)

    if not isinstance(index_data, dict):
        return index_data or {}

    # 旧格式检测：无 includes 字段 → 直接返回
    if "includes" not in index_data:
        return index_data

    # 新格式：合并所有子文件
    includes = index_data["includes"]
    if not isinstance(includes, list) or not includes:
        raise ValueError(
            f"course.yaml 的 includes 字段格式无效（期望非空列表）: {index_path}"
        )

    result = {}

    # 索引文件本身的非保留键也参与合并（允许少量内联数据）
    for key, value in index_data.items():
        if key not in _RESERVED_KEYS:
            result[key] = value

    # 逐个加载并合并子文件
    for include_filename in includes:
        sub_path = course_dir / include_filename
        if not sub_path.exists():
            raise FileNotFoundError(
                f"课程子文件缺失: {sub_path}\n"
                f"  期望文件: {include_filename}\n"
                f"  索引文件: {index_path}\n"
                f"  提示: 请检查 course.yaml 的 includes 列表"
            )

        with open(sub_path, "r", encoding="utf-8") as f:
            sub_data = yaml.safe_load(f)

        if not sub_data or not isinstance(sub_data, dict):
            continue

        # 检查重复键
        overlap = set(result.keys()) & set(sub_data.keys())
        if overlap:
            raise ValueError(
                f"子文件 {include_filename} 包含与其他子文件重复的顶层键: {overlap}\n"
                f"  合并规则要求所有子文件的顶层键互不重复"
            )

        result.update(sub_data)

    # 新格式：动态组装实验数据 (Decentralized SSOT)
    dynamic_exps = _load_experiments_dynamic(course_dir)
    if dynamic_exps:
        result["experiments"] = dynamic_exps

    return result


def load_course_section(
    course_dir: Union[str, Path], section: str
) -> dict:
    """
    按需加载单个域的数据。

    相比 load_course()，此函数仅读取和解析一个子文件，
    适用于只需要特定域数据的场景（如仅获取 calendar）。

    参数:
        course_dir: 课程根目录路径
        section: 域名称，可选值:
            'calendar' | 'objectives' | 'textbooks' |
            'experiments' | 'assessment' | 'meta'

    返回:
        该域的数据字典

    异常:
        ValueError: 未知的 section 名称
        FileNotFoundError: 子文件不存在
    """
    if section not in SECTION_FILE_MAP:
        valid = ", ".join(sorted(SECTION_FILE_MAP.keys()))
        raise ValueError(f"未知的 section: '{section}'（可选: {valid}）")

    course_dir = Path(course_dir)
    index_path = course_dir / "course.yaml"

    if not index_path.exists():
        raise FileNotFoundError(f"课程配置文件缺失: {index_path}")

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = yaml.safe_load(f)

    if not isinstance(index_data, dict):
        return {}

    # 旧格式：从完整数据中按键过滤
    if "includes" not in index_data:
        keys_for_section = SECTION_KEYS_MAP.get(section, [])
        return {k: v for k, v in index_data.items() if k in keys_for_section}

    # 优先执行动态组装实验数据
    if section == "experiments":
        dynamic_exps = _load_experiments_dynamic(course_dir)
        if dynamic_exps:
            return {"experiments": dynamic_exps}

    # 新格式：直接加载对应的子文件
    filename = SECTION_FILE_MAP[section]
    sub_path = course_dir / filename

    if not sub_path.exists():
        return {}

    with open(sub_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data if isinstance(data, dict) else {}


# ===== 便捷函数 =====


def is_split_format(course_dir: Union[str, Path]) -> bool:
    """检查课程目录是否使用新的拆分格式。"""
    course_dir = Path(course_dir)
    index_path = course_dir / "course.yaml"

    if not index_path.exists():
        return False

    with open(index_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return isinstance(data, dict) and "includes" in data


def list_course_files(course_dir: Union[str, Path]) -> list[str]:
    """列出课程数据涉及的所有 YAML 文件路径（相对于课程目录）。

    旧格式返回 ['course.yaml']，新格式返回索引 + 所有子文件。
    """
    course_dir = Path(course_dir)
    index_path = course_dir / "course.yaml"

    if not index_path.exists():
        return []

    with open(index_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "includes" not in data:
        files = ["course.yaml"]
    else:
        files = ["course.yaml"] + list(data["includes"])

    # 追加动态实验文件
    exp_dir = course_dir / "practices" / "experiments"
    if exp_dir.exists():
        for exp_file in exp_dir.glob("exp_*.yaml"):
            try:
                files.append(str(exp_file.relative_to(course_dir)))
            except ValueError:
                pass

    return files


# ===== CLI 测试 =====

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(
        description="课程数据加载器 — 测试/调试工具"
    )
    parser.add_argument(
        "course_dir",
        help="课程根目录路径（如 ./信息可视化）",
    )
    parser.add_argument(
        "--section", "-s",
        choices=list(SECTION_FILE_MAP.keys()),
        help="仅加载指定域（可选）",
    )
    parser.add_argument(
        "--keys-only", "-k",
        action="store_true",
        help="仅输出顶层键名（不输出值）",
    )
    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="输出课程文件格式信息",
    )
    args = parser.parse_args()

    try:
        if args.info:
            split = is_split_format(args.course_dir)
            files = list_course_files(args.course_dir)
            print(f"格式: {'拆分式（新）' if split else '单体式（旧）'}")
            print(f"文件: {', '.join(files)}")
            sys.exit(0)

        if args.section:
            data = load_course_section(args.course_dir, args.section)
        else:
            data = load_course(args.course_dir)

        if args.keys_only:
            for key in data.keys():
                print(f"  {key}")
            print(f"\n共 {len(data)} 个顶层键")
        else:
            yaml.dump(
                data, sys.stdout,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=120,
            )

    except (FileNotFoundError, ValueError, yaml.YAMLError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
