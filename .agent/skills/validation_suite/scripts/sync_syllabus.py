#!/usr/bin/env python3
"""
Syllabus Synchronizer (sync_syllabus.py)

This script scans all markdown files in the `scripts/` directory, extracts their Frontmatter metadata,
groups them by week, and performs two functions:

1. --check mode: Compares frontmatter-derived structure with course.yaml calendar (read-only)
2. --structure-map mode: Regenerates `00_structure_map.md` from script frontmatter

Note (ADR 007): course.yaml calendar is the SSOT, maintained manually.
This script does NOT write to course.yaml.

Usage:
    python sync_syllabus.py --course "信息可视化" --check
    python sync_syllabus.py --course "信息可视化" --structure-map
"""

import os
import sys
import yaml
import glob
import re
import argparse
from typing import List, Dict, Any

def parse_frontmatter(file_path: str) -> Dict[str, Any]:
    """Extracts YAML frontmatter from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}

    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"Warning: Invalid YAML frontmatter in {os.path.basename(file_path)}: {e}")
        return {}

def generate_calendar(scripts_dir: str) -> List[Dict[str, Any]]:
    """Scans scripts and builds the calendar list."""
    calendar_map = {} # week_num -> week_data

    # Pattern to match scripts
    # We look for all .md files, assuming they are scripts if they have 'week' in frontmatter
    files = glob.glob(os.path.join(scripts_dir, "*.md"))
    
    # Sort files to ensure deterministic order (e.g. S01 before S02)
    files.sort()

    for file_path in files:
        if os.path.basename(file_path) in ["00_structure_map.md", "README.md"]:
            continue

        meta = parse_frontmatter(file_path)
        if 'week' not in meta:
            # Skip files without week info (e.g., drafts without frontmatter)
            continue
        
        # Handle week as string or int (e.g. "5 (Extension)" -> 5)
        raw_week = meta.get('week')
        try:
            # Extract first integer
            week_num = int(re.search(r'\d+', str(raw_week)).group())
        except (ValueError, AttributeError):
            print(f"Warning: Invalid week format '{raw_week}' in {os.path.basename(file_path)}. Skipping.")
            continue

        # Initialize week entry if not exists
        if week_num not in calendar_map:
            calendar_map[week_num] = {
                'week': week_num,
                'topic': meta.get('topic', 'TBD'),
                'content': [], # Will aggregate lesson titles or use explicit content
                'hours_theory': 0,
                'hours_practice': 0,
                'lessons': []
            }
        
        week_data = calendar_map[week_num]
        
        # Accumulate hours
        week_data['hours_theory'] += float(meta.get('theory_hours', 0))
        week_data['hours_practice'] += float(meta.get('practice_hours', 0))
        
        # Add lesson
        lesson = {
            'topic': meta.get('title', os.path.basename(file_path)),
            'objectives': meta.get('objectives', []),
             # steps could be extracted too, but let's keep it simple for course.yaml specific structure
             # if user wants full detail
        }
        week_data['lessons'].append(lesson)
        
        # Update week topic if not set or generic
        # (Logic: If we have multiple scripts, which one defines the week topic? 
        #  We assume the first one, or explicitly defined.)
        if week_data['topic'] == 'TBD' and 'topic' in meta:
             week_data['topic'] = meta['topic']

        # Append to content summary
        if 'title' in meta:
             week_data['content'].append(meta['title'])

    # formatting summary content
    sorted_weeks = sorted(calendar_map.keys())
    calendar_list = []
    
    for w in sorted_weeks:
        data = calendar_map[w]
        # Join content titles
        if isinstance(data['content'], list):
            data['content'] = "、".join(data['content'])
        calendar_list.append(data)

    return calendar_list

# 注意 (ADR 007): update_course_yaml 已移除。
# course.yaml calendar 由人工维护，sync_syllabus.py 不再覆盖写入。
# 参见 ADR 007 / ADR 015。

def generate_structure_map(structure_map_path: str, calendar: List[Dict[str, Any]], course_name: str):
    """Generates the read-only structure map."""
    lines = [
        f"# {course_name} - Course Structure Map",
        "",
        "> [!NOTE]",
        "> This file is AUTO-GENERATED from script files. Do NOT edit manually.",
        "> Update `scripts/*.md` frontmatter to change structure.",
        "",
        "## Syllabus Overview",
        ""
    ]
    
    for week in calendar:
        lines.append(f"### Week {week['week']}: {week['topic']}")
        lines.append(f"- **Theory**: {week['hours_theory']}h | **Practice**: {week['hours_practice']}h")
        lines.append(f"- **Content**: {week['content']}")
        lines.append("- **Lessons**:")
        for lesson in week['lessons']:
            lines.append(f"  - {lesson['topic']}")
        lines.append("")
        
    with open(structure_map_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"✅ Updated {structure_map_path}")

def main():
    parser = argparse.ArgumentParser(description="Sync Syllabus (read-only, ADR 007)")
    parser.add_argument("--course", required=True, help="Course directory name")
    parser.add_argument("--check", action="store_true",
                        help="Check if frontmatter structure matches course.yaml calendar")
    parser.add_argument("--structure-map", action="store_true",
                        help="Regenerate 00_structure_map.md from script frontmatter")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace = os.path.abspath(os.path.join(script_dir, *(['..'] * 4)))

    course_path = os.path.join(workspace, args.course)
    scripts_path = os.path.join(course_path, "scripts")
    course_yaml_path = os.path.join(course_path, "course.yaml")
    structure_map_path = os.path.join(scripts_path, "00_structure_map.md")

    if not os.path.exists(scripts_path):
        print(f"Error: Scripts directory not found: {scripts_path}")
        sys.exit(1)

    if not args.check and not args.structure_map:
        print("请指定 --check 或 --structure-map（写入 course.yaml 模式已移除，参见 ADR 007）")
        sys.exit(1)

    calendar = generate_calendar(scripts_path)
    if not calendar:
        print("⚠️ No valid scripts found with 'week' metadata.")

    if args.check:
        print(f"🔍 Checking sync status for: {args.course}")
        with open(course_yaml_path, 'r', encoding='utf-8') as f:
            current_yaml = yaml.safe_load(f)

        current_calendar = current_yaml.get('calendar', [])

        # 语义比较：只检查可比较的字段（周次覆盖 + 主题名匹配）
        yaml_weeks = {}
        for entry in current_calendar:
            w = entry.get('week')
            if w is not None:
                yaml_weeks[w] = entry.get('topic', '').strip()

        fm_weeks = {}
        for entry in calendar:
            w = entry.get('week')
            if w is not None:
                # frontmatter 可能用 title 或 topic
                topic = entry.get('topic', '').strip()
                if topic == 'TBD' or not topic:
                    # fallback: 用 lessons 的第一个 topic (= frontmatter title)
                    lessons = entry.get('lessons', [])
                    if lessons:
                        topic = lessons[0].get('topic', '').strip()
                fm_weeks[w] = topic

        issues = []
        synced = 0

        # 检查 1: 每个有脚本的周是否在 course.yaml 中存在
        for w, fm_topic in sorted(fm_weeks.items()):
            if w not in yaml_weeks:
                issues.append(f"   W{w}: 脚本存在但 course.yaml 缺少此周")
            else:
                yaml_topic = yaml_weeks[w]
                # 规范化比较（去掉空格、标点差异）
                fm_norm = re.sub(r'\s+', '', fm_topic)
                yaml_norm = re.sub(r'\s+', '', yaml_topic)
                if fm_norm == yaml_norm:
                    synced += 1
                else:
                    issues.append(f"   W{w}: 主题不匹配")
                    issues.append(f"         脚本: {fm_topic}")
                    issues.append(f"         YAML: {yaml_topic}")

        # 检查 2: course.yaml 中无脚本的周（允许，仅提示）
        yaml_only = set(yaml_weeks.keys()) - set(fm_weeks.keys())
        for w in sorted(yaml_only):
            issues.append(f"   W{w}: course.yaml 有此周但无脚本（{yaml_weeks[w]}）")

        total = len(fm_weeks)
        if not issues:
            print(f"✅ Syllabus is in sync. ({synced}/{total} 周匹配)")
            sys.exit(0)
        else:
            # 区分 ERROR 和 WARNING
            errors = [i for i in issues if '不匹配' in i or '缺少' in i]
            warnings = [i for i in issues if '无脚本' in i]
            if errors:
                print(f"❌ Syllabus is OUT OF SYNC. ({synced}/{total} 周匹配)")
                for i in issues:
                    print(i)
                sys.exit(1)
            else:
                print(f"✅ Syllabus is in sync. ({synced}/{total} 周匹配, {len(warnings)} 个提示)")
                for w in warnings:
                    print(w)
                sys.exit(0)

    if args.structure_map:
        print(f"📝 Generating structure map for: {args.course}")
        generate_structure_map(structure_map_path, calendar, args.course)


if __name__ == "__main__":
    main()
