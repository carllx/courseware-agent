#!/usr/bin/env python3
"""
migrate_course_yaml.py — course.yaml 按域拆分迁移脚本

一次性脚本，批量将课程工作区中的单体 course.yaml 拆分为索引式结构。

用法:
    python migrate_course_yaml.py                    # 自动扫描并迁移所有合格课程
    python migrate_course_yaml.py --dry-run          # 预览模式（不写入）
    python migrate_course_yaml.py --course 信息可视化  # 仅迁移指定课程
    python migrate_course_yaml.py --verify-only      # 仅验证已迁移课程

ADR-044 Phase 2 实施工件。
"""

import argparse
import copy
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml


# ─── 域到文件/键的映射 ───

DOMAIN_MAP = {
    "course_meta.yaml": [
        "course", "teacher", "student_analysis", "semester_config", "agent"
    ],
    "course_objectives.yaml": ["objectives"],
    "course_textbooks.yaml": ["textbooks"],
    "course_calendar.yaml": ["calendar"],
    "course_experiments.yaml": ["experiments"],
    "course_assessment.yaml": ["assessment_methods", "exams"],
}

# CourseSchema 的必要顶层键（用于识别合格课程）
COURSESCHEMA_REQUIRED_KEYS = {"course", "teacher", "calendar"}

# 迁移时间戳
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


# ─── 颜色输出 ───

class C:
    OK = "\033[92m"
    WARN = "\033[93m"
    ERR = "\033[91m"
    DIM = "\033[90m"
    BOLD = "\033[1m"
    END = "\033[0m"


def log_ok(msg):
    print(f"  {C.OK}✅{C.END} {msg}")


def log_warn(msg):
    print(f"  {C.WARN}⚠️{C.END}  {msg}")


def log_err(msg):
    print(f"  {C.ERR}❌{C.END} {msg}")


def log_info(msg):
    print(f"  {C.DIM}ℹ️{C.END}  {msg}")


# ─── 核心逻辑 ───


def scan_courses(workspace: Path, course_filter: str = None) -> list[Path]:
    """扫描工作区下所有合格的课程目录。

    合格条件:
    - 含 course.yaml
    - course.yaml 包含 CourseSchema 必需键（course, teacher, calendar）
    - 尚未迁移（无 includes 字段）
    """
    courses = []
    for item in sorted(workspace.iterdir()):
        if not item.is_dir() or item.name.startswith((".", "_")):
            continue
        if course_filter and item.name != course_filter:
            continue

        yaml_path = item / "course.yaml"
        if not yaml_path.exists():
            continue

        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError:
            log_warn(f"YAML 解析失败，跳过: {item.name}")
            continue

        if not isinstance(data, dict):
            continue

        # 已迁移检测
        if "includes" in data:
            log_info(f"已迁移，跳过: {item.name}")
            continue

        # CourseSchema 合格检查
        if not COURSESCHEMA_REQUIRED_KEYS.issubset(data.keys()):
            missing = COURSESCHEMA_REQUIRED_KEYS - set(data.keys())
            log_info(f"非标准格式（缺少 {missing}），跳过: {item.name}")
            continue

        courses.append(item)

    return courses


def split_course_yaml(data: dict) -> dict[str, dict]:
    """将单体 course.yaml 的数据按域拆分。

    返回:
        {子文件名: 数据字典} 映射
    """
    result = {}
    assigned_keys = set()

    for filename, keys in DOMAIN_MAP.items():
        section_data = {}
        for key in keys:
            if key in data:
                section_data[key] = data[key]
                assigned_keys.add(key)
        if section_data:
            result[filename] = section_data

    # 检查遗漏键
    all_keys = set(data.keys())
    unassigned = all_keys - assigned_keys
    if unassigned:
        # 将遗漏键放入 course_meta.yaml
        if "course_meta.yaml" not in result:
            result["course_meta.yaml"] = {}
        for key in sorted(unassigned):
            result["course_meta.yaml"][key] = data[key]
        log_warn(f"以下键未在 DOMAIN_MAP 中定义，已归入 course_meta.yaml: {unassigned}")

    return result


def generate_index_yaml(includes: list[str]) -> str:
    """生成新的索引式 course.yaml 内容。"""
    lines = [
        "# course.yaml — 课程数据索引（SSOT 入口）",
        "# 拆分自原始单体 course.yaml，详见 ADR-044",
        f"# 迁移时间: {TIMESTAMP}",
        "",
        '_schema_version: "3.0"',
        "",
        "includes:",
    ]
    for inc in includes:
        # 添加注释说明每个子文件的内容
        keys_for_file = DOMAIN_MAP.get(inc, [])
        comment = " + ".join(keys_for_file) if keys_for_file else ""
        lines.append(f"  - {inc:<30s} # {comment}")

    return "\n".join(lines) + "\n"


def write_yaml_file(path: Path, data: dict):
    """将数据写入 YAML 文件。"""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )


def deep_compare(original: dict, merged: dict) -> list[str]:
    """深度比较两个字典，返回差异列表。"""
    diffs = []
    _deep_compare_recursive(original, merged, "", diffs)
    return diffs


def _deep_compare_recursive(a, b, path: str, diffs: list):
    """递归比较两个对象。"""
    if type(a) != type(b):
        diffs.append(f"类型不匹配 {path}: {type(a).__name__} vs {type(b).__name__}")
        return

    if isinstance(a, dict):
        a_keys = set(a.keys())
        b_keys = set(b.keys())
        for key in a_keys - b_keys:
            diffs.append(f"键缺失 {path}.{key}: 仅存在于原始数据")
        for key in b_keys - a_keys:
            diffs.append(f"键多余 {path}.{key}: 仅存在于合并数据")
        for key in a_keys & b_keys:
            _deep_compare_recursive(a[key], b[key], f"{path}.{key}", diffs)

    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"列表长度不匹配 {path}: {len(a)} vs {len(b)}")
            return
        for i, (ai, bi) in enumerate(zip(a, b)):
            _deep_compare_recursive(ai, bi, f"{path}[{i}]", diffs)

    elif a != b:
        a_repr = repr(a)[:80]
        b_repr = repr(b)[:80]
        diffs.append(f"值不匹配 {path}: {a_repr} vs {b_repr}")


def migrate_course(course_dir: Path, dry_run: bool = False) -> bool:
    """迁移单门课程的 course.yaml。

    返回:
        True = 成功, False = 失败
    """
    yaml_path = course_dir / "course.yaml"
    course_name = course_dir.name

    print(f"\n{'─' * 60}")
    print(f"{C.BOLD}📦 迁移: {course_name}{C.END}")
    print(f"   源文件: {yaml_path} ({yaml_path.stat().st_size:,} bytes)")

    # 1. 读取原始数据
    with open(yaml_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    original_data = yaml.safe_load(original_text)
    top_keys = list(original_data.keys())
    print(f"   顶层键: {', '.join(top_keys)} ({len(top_keys)} 个)")

    # 2. 按域拆分
    split_result = split_course_yaml(original_data)
    print(f"   拆分为 {len(split_result)} 个子文件:")
    for filename, section_data in split_result.items():
        keys = list(section_data.keys())
        # 估算行数
        text = yaml.dump(section_data, allow_unicode=True, default_flow_style=False)
        line_count = text.count("\n")
        print(f"     {filename:<30s} → {', '.join(keys):<40s} (~{line_count} 行)")

    if dry_run:
        log_info("预览模式 — 不写入文件")
        return True

    # 3. 备份原始文件
    backup_name = f"course.yaml.bak.{TIMESTAMP}"
    backup_path = course_dir / backup_name
    shutil.copy2(yaml_path, backup_path)
    log_ok(f"备份: {backup_name} ({backup_path.stat().st_size:,} bytes)")

    # 4. 写入子文件
    for filename, section_data in split_result.items():
        sub_path = course_dir / filename
        write_yaml_file(sub_path, section_data)
        log_ok(f"写入: {filename} ({sub_path.stat().st_size:,} bytes)")

    # 5. 生成索引式 course.yaml
    includes_list = list(split_result.keys())
    index_content = generate_index_yaml(includes_list)
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    log_ok(f"索引: course.yaml ({yaml_path.stat().st_size:,} bytes)")

    # 6. 验证：重新加载并深度对比
    print(f"\n   {C.BOLD}🔍 验证拆分完整性...{C.END}")

    # 导入 course_loader 进行验证
    workspace_root = course_dir.parent
    loader_path = workspace_root / "course_loader.py"
    if not loader_path.exists():
        log_err(f"course_loader.py 未找到: {loader_path}")
        return False

    import importlib.util
    spec = importlib.util.spec_from_file_location("course_loader", str(loader_path))
    loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loader)

    merged_data = loader.load_course(str(course_dir))

    diffs = deep_compare(original_data, merged_data)
    if diffs:
        log_err(f"深度对比发现 {len(diffs)} 处差异!")
        for diff in diffs[:10]:
            print(f"     {C.ERR}{diff}{C.END}")
        if len(diffs) > 10:
            print(f"     ... 以及 {len(diffs) - 10} 处更多差异")

        # 回滚
        print(f"\n   {C.WARN}🔄 回滚: 恢复原始 course.yaml{C.END}")
        shutil.copy2(backup_path, yaml_path)
        # 清理子文件
        for filename in split_result:
            sub_path = course_dir / filename
            if sub_path.exists():
                sub_path.unlink()
        return False

    log_ok(f"深度对比: 零差异 ✨")
    return True


def verify_course(course_dir: Path) -> bool:
    """验证已迁移的课程数据完整性。"""
    course_name = course_dir.name
    yaml_path = course_dir / "course.yaml"
    backup_path = None

    # 查找最近的备份文件
    for item in sorted(course_dir.iterdir(), reverse=True):
        if item.name.startswith("course.yaml.bak."):
            backup_path = item
            break

    if not backup_path:
        log_warn(f"{course_name}: 无备份文件，无法对比验证")
        return False

    print(f"\n{C.BOLD}🔍 验证: {course_name}{C.END}")
    print(f"   备份: {backup_path.name}")

    # 加载备份（原始数据）
    with open(backup_path, "r", encoding="utf-8") as f:
        original = yaml.safe_load(f)

    # 加载当前（合并后数据）
    workspace_root = course_dir.parent
    loader_path = workspace_root / "course_loader.py"

    import importlib.util
    spec = importlib.util.spec_from_file_location("course_loader", str(loader_path))
    loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loader)

    merged = loader.load_course(str(course_dir))

    diffs = deep_compare(original, merged)
    if diffs:
        log_err(f"深度对比发现 {len(diffs)} 处差异!")
        for diff in diffs[:10]:
            print(f"     {C.ERR}{diff}{C.END}")
        return False

    log_ok("深度对比: 零差异 ✨")
    return True


# ─── 主函数 ───

def main():
    parser = argparse.ArgumentParser(
        description="course.yaml 按域拆分迁移脚本 (ADR-044)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python migrate_course_yaml.py                    # 迁移所有合格课程
  python migrate_course_yaml.py --dry-run          # 预览不写入
  python migrate_course_yaml.py --course 信息可视化  # 仅迁移指定课程
  python migrate_course_yaml.py --verify-only      # 仅验证已迁移课程
        """,
    )
    parser.add_argument(
        "--course", "-c",
        help="仅处理指定课程目录名",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="预览模式：分析但不写入文件",
    )
    parser.add_argument(
        "--verify-only", "-v",
        action="store_true",
        help="仅验证已迁移的课程",
    )
    parser.add_argument(
        "--root", "-r",
        default=".",
        help="工作区根目录（默认: 当前目录）",
    )
    args = parser.parse_args()

    workspace = Path(args.root).resolve()
    print(f"{C.BOLD}course.yaml 按域拆分迁移工具{C.END}")
    print(f"工作区: {workspace}")

    if args.verify_only:
        # 验证模式
        successes = 0
        failures = 0
        for item in sorted(workspace.iterdir()):
            if not item.is_dir():
                continue
            index_path = item / "course.yaml"
            if not index_path.exists():
                continue
            with open(index_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict) or "includes" not in data:
                continue
            if args.course and item.name != args.course:
                continue

            if verify_course(item):
                successes += 1
            else:
                failures += 1

        print(f"\n{'─' * 60}")
        print(f"验证结果: {C.OK}{successes} 通过{C.END}, {C.ERR}{failures} 失败{C.END}")
        sys.exit(1 if failures > 0 else 0)

    # 迁移模式
    courses = scan_courses(workspace, args.course)

    if not courses:
        print(f"\n{C.WARN}未找到需要迁移的课程。{C.END}")
        if args.course:
            print(f"  提示: 课程 '{args.course}' 可能已迁移或不存在。")
        sys.exit(0)

    print(f"\n将迁移 {len(courses)} 门课程:")
    for c in courses:
        size = (c / "course.yaml").stat().st_size
        print(f"  • {c.name} ({size:,} bytes)")

    successes = 0
    failures = 0

    for course_dir in courses:
        if migrate_course(course_dir, dry_run=args.dry_run):
            successes += 1
        else:
            failures += 1

    # 汇总
    print(f"\n{'═' * 60}")
    mode = "预览" if args.dry_run else "迁移"
    if failures == 0:
        print(f"{C.OK}{C.BOLD}✅ {mode}完成: {successes} 门课程全部成功{C.END}")
    else:
        print(f"{C.ERR}{C.BOLD}❌ {mode}完成: {successes} 成功, {failures} 失败{C.END}")

    sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    main()
