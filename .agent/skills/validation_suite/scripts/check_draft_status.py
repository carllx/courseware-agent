#!/usr/bin/env python3
"""
check_draft_status.py — Draft 模块追踪仪表盘

扫描指定课程所有脚本中的 draft 模块，输出追踪报告。
集成点：/write Step 0（环境预检）和 /audit Step 2（Pre-Flight）。

用法:
    python check_draft_status.py --course "信息可视化"
"""

import os
import sys
import re
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_parser import get_workspace_root, get_scripts_dir, list_script_files, list_script_files_for_week


def scan_draft_modules(file_path: str) -> list[dict]:
    """扫描单个脚本文件中的 draft 模块。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 跳过 frontmatter
    fm_match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    body = content[fm_match.end():] if fm_match else content

    # 按 ## 分割模块
    module_pattern = re.compile(r'^## (.+)$', re.MULTILINE)
    splits = list(module_pattern.finditer(body))

    drafts = []
    for i, match in enumerate(splits):
        name = match.group(1).strip()
        start = match.end()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(body)
        section = body[start:end]

        # 检测 STATUS: draft
        status_match = re.search(r'<!--.*?STATUS:\s*(\w+)\s*-->', section)
        if status_match and status_match.group(1).strip().lower() == 'draft':
            # 提取 BUDGET 和实际字数
            budget_match = re.search(r'BUDGET:\s*(\d+)\s*chars', section)
            budget = int(budget_match.group(1)) if budget_match else None

            # 粗略统计中文字数（排除注释和标签块）
            cn_count = 0
            for line in section.split('\n'):
                stripped = line.strip()
                if (stripped.startswith('> [VISUAL]') or
                    stripped.startswith('> [ACTIVITY]') or
                    stripped.startswith('<!--') or
                    stripped.startswith('#') or
                    stripped == '---' or
                    stripped == ''):
                    continue
                if stripped.startswith('>'):
                    continue
                cn_count += len(re.findall(r'[\u4e00-\u9fff]', stripped))

            fill_pct = f"{cn_count / budget * 100:.0f}%" if budget else "?"
            drafts.append({
                'module': name,
                'budget': budget,
                'cn_count': cn_count,
                'fill_pct': fill_pct,
            })

    return drafts


def main():
    parser = argparse.ArgumentParser(description="Draft 模块追踪仪表盘")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--week", type=int, default=None,
                        help="仅扫描指定周次的 draft 模块（如 --week 1）")
    args = parser.parse_args()

    workspace = get_workspace_root()
    scripts_dir = get_scripts_dir(workspace, args.course)

    if not os.path.exists(scripts_dir):
        print(f"❌ 脚本目录不存在: {scripts_dir}")
        sys.exit(1)

    if args.week is not None:
        files = list_script_files_for_week(scripts_dir, args.week)
    else:
        files = list_script_files(scripts_dir)
    if not files:
        print("✅ 无脚本文件。")
        sys.exit(0)

    total_drafts = 0
    has_output = False

    for fname in files:
        fpath = os.path.join(scripts_dir, fname)
        drafts = scan_draft_modules(fpath)

        if drafts:
            if not has_output:
                print(f"\n📋 {args.course} — Draft 模块追踪")
                print("━" * 50)
                has_output = True

            print(f"\n  {fname}:")
            for d in drafts:
                budget_str = f"{d['budget']} 字" if d['budget'] else "无预算"
                print(f"    ❌ {d['module']}")
                print(f"       draft | 实际 {d['cn_count']} 字 / 预算 {budget_str} | 填充 {d['fill_pct']}")
                total_drafts += 1

    if has_output:
        print(f"\n{'━' * 50}")
        print(f"  总计: {total_drafts} 个 draft 模块待完成\n")
        sys.exit(1)
    else:
        print(f"✅ {args.course} — 无 draft 模块，所有模块均已完成。")
        sys.exit(0)


if __name__ == "__main__":
    main()
