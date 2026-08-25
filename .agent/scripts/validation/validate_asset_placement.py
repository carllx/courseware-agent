#!/usr/bin/env python3
"""
资产落位验证器 (Asset Placement Validator)

检测 V5 课程中资产文件是否被错误地存放在课程级 public/ 目录。
同时验证脚本中 [VISUAL] 块的 Asset 路径能否正确解析到周次级物理文件。

用法:
    python validate_asset_placement.py --course "信息可视化"
    python validate_asset_placement.py --course "信息可视化" --fix  # 自动迁移错位文件
"""

import os
import sys
import re
import argparse
import shutil
from pathlib import Path

# 确保能 import 同目录模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))


def get_workspace_root():
    """获取工作区根目录（脚本位于 <workspace>/.agent/scripts/validation/）"""
    return str(Path(__file__).resolve().parents[3])


def is_v5_course(course_dir: str) -> bool:
    """判断课程是否使用 V5 Package 架构（存在 weeks/*/package.yaml）"""
    weeks_dir = os.path.join(course_dir, "weeks")
    if not os.path.isdir(weeks_dir):
        return False
    for entry in os.scandir(weeks_dir):
        if entry.is_dir() and os.path.exists(os.path.join(entry.path, "package.yaml")):
            return True
    return False


def scan_course_level_public(course_dir: str) -> list[dict]:
    """
    扫描课程级 public/ 目录中不应存在的媒体文件。
    返回: [{"path": ..., "type": ..., "size_bytes": ...}, ...]
    """
    violations = []
    public_dir = os.path.join(course_dir, "public")
    if not os.path.isdir(public_dir):
        return violations

    # 视频和图片的扩展名集合
    MEDIA_EXTS = {
        ".webm", ".mp4", ".mkv", ".avi", ".mov",           # 视频
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",   # 图片
        ".vtt", ".srt",                                     # 字幕
    }
    # 垃圾文件（临时脚本、中间产物等）
    JUNK_EXTS = {".py", ".txt", ".part"}
    JUNK_PATTERNS = ["Video", "test_", "temp_", "clean_"]

    for root, dirs, files in os.walk(public_dir):
        for f in files:
            if f.startswith("."):
                continue
            ext = os.path.splitext(f)[1].lower()
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, course_dir)
            size = os.path.getsize(fpath)

            if ext in MEDIA_EXTS:
                violations.append({
                    "path": rel,
                    "abs_path": fpath,
                    "type": "media",
                    "size_bytes": size,
                })
            elif ext in JUNK_EXTS or any(p in f.lower() for p in JUNK_PATTERNS):
                violations.append({
                    "path": rel,
                    "abs_path": fpath,
                    "type": "junk",
                    "size_bytes": size,
                })

    return violations


def find_target_week_dir(course_dir: str, filename: str) -> str | None:
    """
    根据文件名中的周次前缀（如 W01_、S01_）推导应存放的周次目录。
    返回周次级 public/ 子目录的绝对路径，或 None。
    """
    weeks_dir = os.path.join(course_dir, "weeks")
    if not os.path.isdir(weeks_dir):
        return None

    # 尝试从文件名提取周次标记
    week_match = re.match(r"W(\d{2})_", filename)
    if week_match:
        week_num = week_match.group(1)
        for entry in os.scandir(weeks_dir):
            if entry.is_dir() and entry.name.startswith(f"W{week_num}_"):
                return entry.path
        return None

    # 尝试从 Slide ID 前缀（S01_, S02_）推导——需遍历各周的脚本确认归属
    slide_match = re.match(r"S(\d{2})[a-z]?_", filename)
    if slide_match:
        # Slide 前缀无法直接映射到周次，返回 None（需人工判断）
        return None

    return None


def scan_script_asset_resolution(course_dir: str) -> list[dict]:
    """
    模拟 PPT 引擎的路径解析逻辑，预检每个 [VISUAL] 块的 Asset 是否在周次级物理存在。
    返回未解析的 Asset 列表。
    """
    unresolved = []
    weeks_dir = os.path.join(course_dir, "weeks")
    if not os.path.isdir(weeks_dir):
        return unresolved

    # Markdown 图片语法解析
    RE_MD_IMAGE = re.compile(r"!\[.*?\]\((.+?)\)")
    # [VISUAL] Asset 行
    RE_ASSET_LINE = re.compile(
        r"^\s*>\s*\*?\s*\*\*Asset(?:\s*\d+)?\*\*:\s*(.+)$", re.IGNORECASE
    )

    for week_entry in sorted(os.scandir(weeks_dir), key=lambda e: e.name):
        if not week_entry.is_dir():
            continue
        src_dir = os.path.join(week_entry.path, "src")
        if not os.path.isdir(src_dir):
            continue

        for md_file in sorted(os.listdir(src_dir)):
            if not md_file.endswith(".md"):
                continue
            md_path = os.path.join(src_dir, md_file)
            with open(md_path, "r", encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, 1):
                    m = RE_ASSET_LINE.match(line)
                    if not m:
                        continue
                    raw_asset = m.group(1).strip()

                    # 提取 MD 图片路径
                    md_match = RE_MD_IMAGE.search(raw_asset)
                    if md_match:
                        asset_ref = md_match.group(1).strip()
                    else:
                        asset_ref = raw_asset
                        # 去除反引号/引号
                        if asset_ref.startswith("`") and asset_ref.endswith("`"):
                            asset_ref = asset_ref[1:-1]
                        if asset_ref.startswith('"') and asset_ref.endswith('"'):
                            asset_ref = asset_ref[1:-1]

                    # 从 src/ 解析相对路径
                    resolved = os.path.normpath(os.path.join(src_dir, asset_ref))
                    if os.path.exists(resolved):
                        continue

                    # 清洗 ../ 后从周次级解析（模拟 PPT 引擎）
                    cleaned = re.sub(r"^(\.\./)+", "", asset_ref)
                    resolved_week = os.path.join(week_entry.path, cleaned)
                    if os.path.exists(resolved_week):
                        continue

                    # 检查是否意外存在于课程级
                    resolved_course = os.path.join(course_dir, cleaned)
                    location_hint = ""
                    if os.path.exists(resolved_course):
                        location_hint = f" → 🚨 该文件存在于课程级: {os.path.relpath(resolved_course, course_dir)}"

                    unresolved.append({
                        "file": f"{week_entry.name}/src/{md_file}",
                        "line": line_num,
                        "asset_ref": asset_ref,
                        "expected_at": os.path.relpath(resolved_week, course_dir),
                        "location_hint": location_hint,
                    })

    return unresolved


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"


def main():
    parser = argparse.ArgumentParser(description="资产落位验证器 (V5 课程)")
    parser.add_argument("--course", required=True, help="课程目录名（如 '信息可视化'）")
    parser.add_argument(
        "--fix", action="store_true",
        help="自动将课程级媒体文件迁移到推导出的周次级目录（仅限可推导的文件）"
    )
    args = parser.parse_args()

    workspace = get_workspace_root()
    course_dir = os.path.join(workspace, args.course)

    if not os.path.isdir(course_dir):
        print(f"❌ 课程目录不存在: {course_dir}")
        sys.exit(1)

    if not is_v5_course(course_dir):
        print(f"ℹ️  {args.course} 不是 V5 Package 架构课程，跳过检查。")
        sys.exit(0)

    print(f"\n{'='*55}")
    print(f"  资产落位验证报告")
    print(f"{'='*55}")
    print(f"  课程: {args.course}")
    print(f"  架构: V5 Package")
    print(f"{'='*55}")

    exit_code = 0

    # ── 检查 1: 课程级 public/ 污染 ──
    violations = scan_course_level_public(course_dir)
    media_violations = [v for v in violations if v["type"] == "media"]
    junk_violations = [v for v in violations if v["type"] == "junk"]

    if media_violations:
        exit_code = 1
        print(f"\n🚨 课程级 public/ 媒体文件违规 ({len(media_violations)}):")
        for v in media_violations:
            target_week = find_target_week_dir(course_dir, os.path.basename(v["path"]))
            hint = ""
            if target_week:
                # 推导出子目录类型
                sub = "videos" if any(v["path"].endswith(e) for e in [".webm", ".mp4", ".mkv", ".vtt", ".srt"]) else "slides"
                target = os.path.join(target_week, "public", sub, os.path.basename(v["path"]))
                hint = f"\n    💡 建议迁移到: {os.path.relpath(target, course_dir)}"

                if args.fix:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.move(v["abs_path"], target)
                    hint += " ✅ 已迁移"

            print(f"  ❌ {v['path']} ({format_size(v['size_bytes'])}){hint}")

    if junk_violations:
        exit_code = 1
        print(f"\n⚠️  课程级 public/ 垃圾文件 ({len(junk_violations)}):")
        for v in junk_violations:
            action = ""
            if args.fix:
                os.remove(v["abs_path"])
                action = " ✅ 已删除"
            print(f"  🗑️  {v['path']} ({format_size(v['size_bytes'])}){action}")

    # ── 检查 2: 脚本 Asset 路径解析 ──
    unresolved = scan_script_asset_resolution(course_dir)
    if unresolved:
        exit_code = 1
        print(f"\n❌ 脚本 Asset 路径无法解析 ({len(unresolved)}):")
        for u in unresolved:
            print(f"  {u['file']}:L{u['line']}")
            print(f"    引用: {u['asset_ref']}")
            print(f"    期望位置: {u['expected_at']}{u['location_hint']}")

    # ── 汇总 ──
    if exit_code == 0:
        print(f"\n✅ 资产落位验证通过！所有资产均在正确的周次级目录中。")
    else:
        total = len(media_violations) + len(junk_violations) + len(unresolved)
        print(f"\n{'─'*55}")
        print(f"  共发现 {total} 项问题。")
        if not args.fix and (media_violations or junk_violations):
            print(f"  💡 使用 --fix 自动迁移/清理可修复的项目。")
        print(f"{'─'*55}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
