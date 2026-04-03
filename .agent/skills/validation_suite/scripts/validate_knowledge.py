#!/usr/bin/env python3
"""
validate_knowledge.py — 知识枢纽健康检查 (Knowledge Hub Validator)

检查六项：
  C1: knowledge_hub.yaml 是否存在且格式合法
  C2: hub 行数是否满足性能约束（< 200 行）
  C3: textbook/note 条目的 source 文件是否实际存在
  C4: notes/ 目录下是否存在没有 hub 条目的孤立文件
  C5: hub 中是否有多个条目指向同一 source 文件（重复路径）
  C6: textbook/ 子目录的章节文件是否均有 hub 条目（覆盖率）

用法:
    python validate_knowledge.py --course "交互产品开发"
    python validate_knowledge.py --course "信息可视化" --strict
"""

import argparse
import os
import sys

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# 行数硬约束（超出则性能告警；--strict 模式下直接 FAIL）
HUB_LINE_WARN = 300
HUB_LINE_HARD = 400


def find_workspace(script_dir: str) -> str:
    """向上找到有 .agent/ 的工作区根目录。"""
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, ".agent")):
        return cwd
    # 从脚本路径上溯
    candidate = os.path.abspath(os.path.join(script_dir, "../../../../"))
    if os.path.isdir(os.path.join(candidate, ".agent")):
        return candidate
    return cwd


def check_hub_exists(hub_path: str) -> tuple[bool, str]:
    """C1: hub 文件是否存在且格式合法。"""
    if not os.path.exists(hub_path):
        return False, f"knowledge_hub.yaml 不存在：{hub_path}"
    if not HAS_YAML:
        return False, "PyYAML 未安装：pip install pyyaml"
    try:
        with open(hub_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict) or "entries" not in data:
            return False, "knowledge_hub.yaml 格式错误：缺少 entries 键"
        return True, f"hub 存在，共 {len(data['entries'])} 个条目"
    except yaml.YAMLError as e:
        return False, f"YAML 解析失败：{e}"


def check_hub_size(hub_path: str, strict: bool) -> tuple[bool, str]:
    """C2: hub 行数是否满足性能约束。"""
    with open(hub_path, encoding="utf-8") as f:
        lines = f.readlines()
    n = len(lines)
    if n <= HUB_LINE_WARN:
        return True, f"行数 {n}（良好，建议上限 {HUB_LINE_WARN}）"
    elif n <= HUB_LINE_HARD:
        msg = f"行数 {n}（⚠️ 超出建议上限 {HUB_LINE_WARN}，请考虑精简 summary 或迁移旧条目）"
        return not strict, msg
    else:
        return False, f"行数 {n}（❌ 超出硬约束 {HUB_LINE_HARD}，agent 加载开销过大）"


def check_sources_exist(hub_path: str, course_dir: str) -> tuple[bool, list[str]]:
    """C3: textbook/note 条目的 source 文件是否实际存在于课程目录。"""
    with open(hub_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    missing = []
    for entry in data.get("entries", []):
        etype = entry.get("type", "")
        if etype not in ("textbook", "note"):
            continue
        source = entry.get("source", "")
        if not source:
            continue
        # source 路径可能含 "..." 简写（用于 textbook 显示），跳过
        if "..." in source:
            continue
        full_path = os.path.join(course_dir, source)
        if not os.path.exists(full_path):
            missing.append(f"  [{entry.get('id')}] source 不存在：{source}")

    if missing:
        return False, missing
    return True, []


def check_orphan_notes(hub_path: str, course_dir: str) -> tuple[bool, list[str]]:
    """C4: notes/ 目录下是否存在没有 hub 条目的孤立文件。"""
    notes_dir = os.path.join(course_dir, "knowledge", "notes")
    if not os.path.isdir(notes_dir):
        return True, []  # 目录不存在说明还没有笔记，无孤立

    with open(hub_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 收集 hub 中所有 note 条目的 id
    hub_ids = {e["id"] for e in data.get("entries", []) if e.get("type") == "note"}

    orphans = []
    for fname in os.listdir(notes_dir):
        if not fname.endswith(".md"):
            continue
        note_id = fname[:-3]  # 去掉 .md 后缀
        if note_id not in hub_ids:
            orphans.append(f"  notes/{fname}（在 hub 中无对应条目）")

    if orphans:
        return False, orphans
    return True, []


def check_duplicate_sources(hub_path: str) -> tuple[bool, list[str]]:
    """C5: hub 中是否有多个条目指向同一 source 文件（重复路径）。"""
    with open(hub_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    seen: dict[str, str] = {}  # source -> first entry id
    duplicates = []
    for entry in data.get("entries", []):
        source = entry.get("source", "")
        if not source:
            continue
        eid = entry.get("id", "?")
        if source in seen:
            duplicates.append(
                f"  [{eid}] 与 [{seen[source]}] 同时指向：{source}"
            )
        else:
            seen[source] = eid

    if duplicates:
        return False, duplicates
    return True, []


def check_textbook_coverage(hub_path: str, course_dir: str) -> tuple[bool, list[str]]:
    """C6: textbook/ 子目录中的章节 md 文件是否均有对应的 hub 条目。
    
    只扫描以 chapter_ 开头的 .md 文件，跳过 _full.md、index.md 等汇总文件。
    如果某本教材有 book-* 聚合入口（source 指向 index.md），则跳过该教材的
    逐章覆盖率检查——聚合入口即代表整本教材已被索引。
    """
    textbook_dir = os.path.join(course_dir, "knowledge", "textbook")
    if not os.path.isdir(textbook_dir):
        return True, []  # 无教材目录，跳过

    with open(hub_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 收集所有 hub source 路径的文件名集合（相对于课程目录）
    hub_sources: set[str] = set()
    # 收集有聚合入口（index.md）的教材子目录名
    covered_books: set[str] = set()
    for entry in data.get("entries", []):
        src = entry.get("source", "")
        if src:
            hub_sources.add(src)
            # 如果 source 指向 index.md，标记该教材目录为已覆盖
            if src.endswith("/index.md") and src.startswith("knowledge/textbook/"):
                book_subdir = src.split("/")[2]  # knowledge/textbook/<book_dir>/index.md
                covered_books.add(book_subdir)

    # 主教材通过 ch* 条目手动索引关键章节，不要求全量覆盖
    meta = data.get("meta", {})
    main_tb_dir = meta.get("textbook_dir", "")
    if main_tb_dir.startswith("knowledge/textbook/"):
        main_book_subdir = main_tb_dir.split("/")[2] if "/" in main_tb_dir else ""
        if main_book_subdir:
            covered_books.add(main_book_subdir)

    missing = []
    for book_dir in sorted(os.listdir(textbook_dir)):
        book_path = os.path.join(textbook_dir, book_dir)
        if not os.path.isdir(book_path):
            continue
        # 跳过有聚合入口的教材——逐章覆盖非必需
        if book_dir in covered_books:
            continue
        for fname in sorted(os.listdir(book_path)):
            if not fname.endswith(".md"):
                continue
            # 跳过汇总文件、目录文件
            if any(skip in fname for skip in ["_full", "index", "Contents", "CONTENTS", "Front_Matter",
                                               "Preface", "Acknowledgments", "Bibliography"]):
                continue
            if not fname.startswith("chapter_"):
                continue
            rel = os.path.join("knowledge", "textbook", book_dir, fname)
            rel = rel.replace("\\", "/")  # Windows 兼容
            if rel not in hub_sources:
                missing.append(f"  {rel}")

    if missing:
        return False, [f"以下 {len(missing)} 个章节文件缺少 hub 条目："] + missing
    return True, []


def main():
    parser = argparse.ArgumentParser(
        description="知识枢纽健康检查 — 验证 hub 完整性与性能约束"
    )
    parser.add_argument("--course", required=True, help="课程目录名，如「交互产品开发」")
    parser.add_argument("--strict", action="store_true",
                        help="严格模式：行数超出建议上限也视为失败")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace = find_workspace(script_dir)
    course_dir = os.path.join(workspace, args.course)

    if not os.path.isdir(course_dir):
        print(f"❌ 课程目录不存在：{course_dir}")
        sys.exit(1)

    hub_path = os.path.join(course_dir, "knowledge", "knowledge_hub.yaml")

    print(f"🔍 知识枢纽健康检查")
    print(f"   课程: {args.course}")
    print(f"   模式: {'严格' if args.strict else '标准'}")
    print("-" * 50)

    all_passed = True
    results = []

    # C1: 存在性与格式
    ok, msg = check_hub_exists(hub_path)
    results.append(("C1 hub 存在性与格式", ok, [msg]))
    if not ok:
        # C1 失败，后续检查无法运行
        for label, passed, details in results:
            icon = "✅" if passed else "❌"
            print(f"{icon} {label}: {details[0]}")
        print("\n❌ C1 失败，跳过后续检查。")
        sys.exit(1)

    # C2: 行数约束
    ok, msg = check_hub_size(hub_path, args.strict)
    results.append(("C2 hub 行数约束", ok, [msg]))
    if not ok:
        all_passed = False

    # C3: source 文件存在性
    ok, missing = check_sources_exist(hub_path, course_dir)
    if ok:
        results.append(("C3 source 文件完整性", True, ["所有 source 路径有效"]))
    else:
        results.append(("C3 source 文件完整性", False, missing))
        all_passed = False

    # C4: 孤立 notes 文件
    ok, orphans = check_orphan_notes(hub_path, course_dir)
    if ok:
        results.append(("C4 notes 孤立文件", True, ["无孤立 notes 文件"]))
    else:
        results.append(("C4 notes 孤立文件", False, orphans))
        all_passed = False

    # C5: 重复 source 路径
    ok, dups = check_duplicate_sources(hub_path)
    if ok:
        results.append(("C5 source 重复路径", True, ["无重复"]))
    else:
        results.append(("C5 source 重复路径", False, dups))
        all_passed = False

    # C6: textbook 章节覆盖率
    ok, coverage_missing = check_textbook_coverage(hub_path, course_dir)
    if ok:
        results.append(("C6 textbook 覆盖率", True, ["所有章节均有 hub 条目"]))
    else:
        results.append(("C6 textbook 覆盖率", False, coverage_missing))
        all_passed = False

    # 输出报告
    for label, passed, details in results:
        icon = "✅" if passed else "❌"
        print(f"{icon} {label}: {details[0]}")
        for extra in details[1:]:
            print(f"   {extra}")

    print("-" * 50)
    if all_passed:
        print("✨ 知识枢纽健康！")
        sys.exit(0)
    else:
        print("💡 存在问题，请修复后重新运行。")
        sys.exit(1)


if __name__ == "__main__":
    main()
