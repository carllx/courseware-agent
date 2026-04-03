#!/usr/bin/env python3
"""
archive_web.py — 知识存档工具 (Knowledge Archiver)

用途：将 agent 通过网络搜索验证过的内容写为标准笔记（notes/），
      并自动更新 knowledge_hub.yaml（tracking → note，或新增 note）。

用法：
    python archive_web.py \\
        --course "交互产品开发" \\
        --id "fitts-law-01" \\
        --title "Fitts 定律实验证据" \\
        --tags "Fitts-law,motor-control,pointing" \\
        --source-url "https://example.com/fitts" \\
        --summary "Fitts 定律量化目标大小与距离对指向时间的影响" \\
        --content-file /tmp/note_content.md

    # 若内容通过管道传入（无 --content-file）：
    cat /tmp/note.md | python archive_web.py --course ... --id ...
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def find_course_dir(course_name: str) -> str:
    """定位课程目录（同 search_knowledge.py 逻辑）。"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../../../"))

    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, ".agent")):
        project_root = cwd

    course_dir = os.path.join(project_root, course_name)
    if not os.path.isdir(course_dir):
        raise FileNotFoundError(f"课程目录不存在：{course_dir}")
    return course_dir


def write_note(notes_dir: str, note_id: str, title: str, tags: list[str],
               source_url: str, courses: list[str], content: str) -> str:
    """写入标准格式笔记文件，返回写入路径。"""
    os.makedirs(notes_dir, exist_ok=True)

    # 文件名：id 转换为安全文件名
    safe_id = note_id.replace("/", "_").replace("\\", "_")
    note_path = os.path.join(notes_dir, f"{safe_id}.md")

    today = datetime.now().strftime("%Y-%m-%d")
    tags_yaml = json.dumps(tags, ensure_ascii=False)
    courses_yaml = json.dumps(courses, ensure_ascii=False)

    note_content = f"""---
id: {note_id}
title: {title}
tags: {tags_yaml}
source_url: {source_url}
archived_at: {today}
courses: {courses_yaml}
---

# {title}

{content}
"""
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(note_content)

    return note_path


def update_hub(hub_path: str, note_id: str, title: str, tags: list[str],
               source: str, summary: str) -> dict:
    """
    更新 knowledge_hub.yaml：
    - 若存在同 id 的 tracking 条目 → 状态改为 note，填充 source
    - 若不存在 → 新增 note 类型条目
    返回变更摘要。
    """
    if not HAS_YAML:
        return {"error": "PyYAML 未安装，无法自动更新 hub。请手动添加条目。"}

    # 读取现有 hub
    if os.path.exists(hub_path):
        with open(hub_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    entries = data.get("entries", [])

    # 查找同 id 的条目
    existing = None
    for entry in entries:
        if entry.get("id") == note_id:
            existing = entry
            break

    if existing:
        # 更新现有条目（通常是 tracking → note）
        old_type = existing.get("type", "unknown")
        existing["type"] = "note"
        existing["source"] = source
        existing["summary"] = summary or existing.get("summary", "")
        existing["tags"] = tags or existing.get("tags", [])
        existing.pop("status", None)       # 移除 tracking 状态
        existing.pop("keywords", None)     # 移除待搜索关键词
        existing.pop("link", None)         # 移除待访问链接
        existing["query_hint"] = f"view_file {source}"
        change = f"已更新：{note_id}（{old_type} → note）"
    else:
        # 新增 note 条目
        new_entry = {
            "id": note_id,
            "type": "note",
            "tags": tags,
            "summary": summary,
            "source": source,
            "query_hint": f"view_file {source}",
        }
        entries.append(new_entry)
        data["entries"] = entries
        change = f"已新增：{note_id}（note）"

    # 写回 hub
    os.makedirs(os.path.dirname(hub_path), exist_ok=True)
    with open(hub_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False,
                  sort_keys=False, indent=2)

    return {"change": change, "hub_path": hub_path}


def main():
    parser = argparse.ArgumentParser(
        description="将网络搜索结果存档为笔记，并同步更新 knowledge_hub.yaml"
    )
    parser.add_argument("--course", required=True, help="课程名称")
    parser.add_argument("--id", required=True, dest="note_id", help="知识条目唯一 ID（建议用连字符格式）")
    parser.add_argument("--title", required=True, help="笔记标题")
    parser.add_argument("--tags", default="", help="标签，逗号分隔，如 'Fitts-law,motor-control'")
    parser.add_argument("--source-url", default="", help="原始来源 URL")
    parser.add_argument("--summary", default="", help="30-60 字摘要（用于 hub 显示）")
    parser.add_argument("--courses", default="", help="共享课程，逗号分隔（默认仅当前课程）")
    parser.add_argument("--content-file", default="", help="笔记正文文件路径（不指定则从 stdin 读取）")
    args = parser.parse_args()

    # 读取笔记内容
    if args.content_file:
        if not os.path.exists(args.content_file):
            print(json.dumps({"error": f"内容文件不存在：{args.content_file}"}, ensure_ascii=False))
            sys.exit(1)
        with open(args.content_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
    else:
        content = sys.stdin.read().strip()

    if not content:
        print(json.dumps({"error": "笔记内容为空，存档中止。"}, ensure_ascii=False))
        sys.exit(1)

    try:
        course_dir = find_course_dir(args.course)
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    courses = [c.strip() for c in args.courses.split(",") if c.strip()] or [args.course]

    notes_dir = os.path.join(course_dir, "knowledge", "notes")
    hub_path = os.path.join(course_dir, "knowledge", "knowledge_hub.yaml")

    # 1. 写入笔记文件
    note_path = write_note(
        notes_dir=notes_dir,
        note_id=args.note_id,
        title=args.title,
        tags=tags,
        source_url=args.source_url,
        courses=courses,
        content=content,
    )

    # 2. 更新 hub 中的相对路径（相对于课程目录）
    rel_source = os.path.relpath(note_path, course_dir)

    hub_result = update_hub(
        hub_path=hub_path,
        note_id=args.note_id,
        title=args.title,
        tags=tags,
        source=rel_source,
        summary=args.summary,
    )

    result = {
        "status": "ok",
        "note_file": note_path,
        "hub_update": hub_result,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
