#!/usr/bin/env python3
"""
search_knowledge.py — 知识枢纽统一搜索入口 (Knowledge Hub Unified Search)

用途：在 /write 工作流中按关键词快速查找已索引知识，返回轻量 JSON 结果。
设计原则：结果 < 20 行，不加载完整 index.json 到内存上下文。

用法：
    python search_knowledge.py --course "交互产品开发" "affordance"
    python search_knowledge.py --course "信息可视化" "marks channels" --max 5
"""

import argparse
import json
import os
import sys

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def find_course_dir(course_name: str) -> str:
    """
    从脚本路径向上定位项目根目录，再拼接课程路径。
    支持任意工作目录调用。
    """
    # 脚本在 .agent/skills/librarian/scripts/，项目根在 ../../../../
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../../../"))

    # 若当前工作目录更像项目根目录，则优先使用
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, ".agent")):
        project_root = cwd

    course_dir = os.path.join(project_root, course_name)
    if not os.path.isdir(course_dir):
        raise FileNotFoundError(
            f"课程目录不存在：{course_dir}\n"
            f"请检查课程名称是否正确（区分大小写）。"
        )
    return course_dir


def search_hub(query_terms: list[str], hub_path: str, max_results: int) -> list[dict]:
    """
    搜索 knowledge_hub.yaml，返回摘要层命中条目。
    匹配范围：id / tags / summary 字段（大小写不敏感）。
    """
    if not os.path.exists(hub_path):
        return []

    if HAS_YAML:
        with open(hub_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    else:
        # 无 PyYAML 时回退到简单文本匹配
        with open(hub_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 简单降级：只返回文件路径提醒
        return [{"type": "hub_raw", "note": "PyYAML 未安装，请运行 pip install pyyaml", "path": hub_path}]

    entries = data.get("entries", []) if data else []
    results = []

    for entry in entries:
        # 构建可搜索文本
        searchable = " ".join([
            entry.get("id", ""),
            entry.get("summary", ""),
            " ".join(entry.get("tags", [])),
            entry.get("source", ""),
        ]).lower()

        # 所有关键词都命中才算匹配（AND 逻辑）
        if all(term.lower() in searchable for term in query_terms):
            results.append({
                "type": "hub",
                "entry_type": entry.get("type", "unknown"),
                "id": entry.get("id", ""),
                "tags": entry.get("tags", []),
                "summary": entry.get("summary", ""),
                "source": entry.get("source", ""),
                "query_hint": entry.get("query_hint", ""),
                "status": entry.get("status", None),  # tracking 条目的状态
            })
            if len(results) >= max_results:
                break

    return results


def search_textbook_index(query_terms: list[str], index_path: str, max_results: int) -> list[dict]:
    """
    搜索 index.json（教材精确章节索引）。
    此函数由脚本调用，不加载到 agent 上下文；只返回位置信息。
    """
    if not os.path.exists(index_path):
        return []

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    results = []
    for book_name, book_data in index_data.items():
        for file_entry in book_data.get("files", []):
            file_path = file_entry.get("path", "")
            for chapter in file_entry.get("chapters", []):
                title = chapter.get("title", "")
                searchable = (book_name + " " + title).lower()

                if all(term.lower() in searchable for term in query_terms):
                    results.append({
                        "type": "textbook",
                        "book": book_name,
                        "chapter": title,
                        "path": file_path,
                        "lines": [chapter.get("start_line"), chapter.get("end_line")],
                    })
                    if len(results) >= max_results:
                        return results
    return results


def main():
    parser = argparse.ArgumentParser(
        description="knowledge_hub 统一搜索 — 返回轻量 JSON 用于 /write 工作流"
    )
    parser.add_argument("query", nargs="+", help="搜索关键词（支持多词，AND 逻辑）")
    parser.add_argument("--course", required=True, help="课程名称，如「交互产品开发」")
    parser.add_argument("--max", type=int, default=8, help="每类最多返回条目数（默认 8）")
    parser.add_argument("--only", choices=["hub", "textbook"], help="仅搜索指定来源")
    args = parser.parse_args()

    try:
        course_dir = find_course_dir(args.course)
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    hub_path = os.path.join(course_dir, "knowledge", "knowledge_hub.yaml")
    index_path = os.path.join(course_dir, "knowledge", "index.json")

    results = []

    # Layer 1：轻量摘要索引 (hub)
    if args.only != "textbook":
        hub_results = search_hub(args.query, hub_path, args.max)
        results.extend(hub_results)

    # Layer 2：教材精确章节索引（仅脚本内部调用，不进入 agent 上下文）
    if args.only != "hub":
        tb_results = search_textbook_index(args.query, index_path, args.max)
        results.extend(tb_results)

    if not results:
        # 无命中时提供追踪建议
        print(json.dumps({
            "hits": 0,
            "suggestion": f"未找到关键词 {args.query} 的相关知识。",
            "action": f"可追加到 {args.course}/knowledge/tracking.md 的待办清单。",
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
