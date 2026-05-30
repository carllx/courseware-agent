#!/usr/bin/env python3
"""
inject_budget.py — 为脚本批量注入 BUDGET/STATUS 注释行

功能：
  对指定课程下所有缺失 BUDGET 注释的脚本，基于 course.yaml 的
  steps[].minutes 配置和模块标题中的时间标注，自动计算并注入
  <!-- BUDGET: N chars | SLIDES: ≥M | STATUS: done/pending --> 注释行。

  v2 增量模式（默认）：逐模块检查，已有 BUDGET 的模块跳过，
  缺失的模块才注入。支持 ## PART 结构和活动模块豁免。

用法:
    python inject_budget.py --course "交互产品开发"           # 增量注入
    python inject_budget.py --course "交互产品开发" --dry-run  # 试运行，只打印
    python inject_budget.py --course "交互产品开发" --week 1   # 仅处理指定周次
"""

import os
import sys
import re
import math
import argparse
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_parser import (
    get_workspace_root, get_scripts_dir,
    list_script_files, load_course_config,
)

# 语速常量（与 validate_script_length.py 一致）
DELIVERY_SPEEDS = {
    "video_essay": 160,
    "lecture": 180,
    "workshop": 140,
}
DEFAULT_CN_CPM = 180

# 活动/实践模块关键词（标题中含这些关键词的模块视为非讲授模块）
ACTIVITY_KEYWORDS = [
    '实践', '实验', '作业', '练习', 'Exp', 'Assignment', 'Checklist',
    '工坊', '实战准备', '课后', '综合演练', '收官', '启动', '收尾',
    'Self-Verification', '演练', '课堂总结',
]


def get_cn_cpm(course_config: dict) -> int:
    """从 course.yaml 获取语速。"""
    mode = course_config.get("course", {}).get("delivery_mode", "lecture")
    return DELIVERY_SPEEDS.get(mode, DEFAULT_CN_CPM)


def extract_week_number(filename: str) -> int | None:
    """从文件名提取周次号。"""
    m = re.match(r'W(\d+)_', filename)
    return int(m.group(1)) if m else None


def get_week_steps(course_config: dict, week_num: int) -> list[dict] | None:
    """从 course.yaml 获取指定周次的 steps 配置。"""
    calendar = course_config.get("calendar", [])
    for entry in calendar:
        if entry.get("week") == week_num:
            lessons = entry.get("lessons", [])
            if lessons:
                return lessons[0].get("steps", [])
    return None


def count_cn_chars(text: str) -> int:
    """统计中文字符数（粗略，用于 STATUS 判定）。"""
    lines = text.split('\n')
    cn_count = 0
    in_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('> [VISUAL]') or stripped.startswith('> [ACTIVITY]'):
            in_block = True
            continue
        if in_block:
            if stripped.startswith('>'):
                continue
            else:
                in_block = False
        if (stripped.startswith('<!--') or stripped.startswith('#') or
            stripped == '---' or stripped == ''):
            continue
        if stripped.startswith('>'):
            stripped = stripped.lstrip('>').strip()
        cn_count += len(re.findall(r'[\u4e00-\u9fff]', stripped))
    return cn_count


def is_activity_module(title: str) -> bool:
    """判断模块标题是否为活动/实践类（非讲授）。"""
    for kw in ACTIVITY_KEYWORDS:
        if kw.lower() in title.lower():
            return True
    return False


def process_script(file_path: str, steps: list[dict] | None, cn_cpm: int,
                   dry_run: bool = False) -> dict:
    """
    处理单个脚本文件，增量注入 BUDGET 注释。

    v2 策略（增量模式）：
    1. 逐模块检查：已有 BUDGET 注释的模块跳过
    2. 标题含时间标注 → 直接使用
    3. 标题无时间标注 → fallback：从 steps 总时长减去已标注模块时长，
       除以无标注模块数，均分给每个无标注模块
    4. 活动/实践模块（标题含关键词或 fallback 后仍为 0 分钟）→
       注入 <!-- BUDGET: 0 chars | TYPE: activity | STATUS: exempt -->
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # ===== 第一遍：预扫描所有模块标题，收集时间信息 =====
    # 同时支持 ## Module / ## 模块 / ## PART 结构
    module_headers = []  # [(line_index, title, annotated_minutes or None, has_budget)]
    for idx, line in enumerate(lines):
        if re.match(r'^## ', line) and not re.match(r'^### ', line):
            title = line[3:].strip()
            time_match = re.search(r'约?\s*(\d+)\s*(?:分钟|min(?:utes?)?)', title)
            annotated_min = int(time_match.group(1)) if time_match else None
            # 检查标题后 1-3 行内是否已有 BUDGET 注释（标题和 BUDGET 间可能隔空行）
            has_budget = False
            for look_ahead in range(1, 4):
                if idx + look_ahead < len(lines) and '<!-- BUDGET:' in lines[idx + look_ahead]:
                    has_budget = True
                    break
            module_headers.append((idx, title, annotated_min, has_budget))

    if not module_headers:
        return {'file': os.path.basename(file_path), 'status': 'no_modules', 'count': 0, 'exempt': 0}

    # 统计已有 BUDGET 和缺失 BUDGET 的模块数
    missing_count = sum(1 for _, _, _, has in module_headers if not has)
    if missing_count == 0:
        return {'file': os.path.basename(file_path), 'status': 'skip',
                'reason': f'全部 {len(module_headers)} 个模块已有 BUDGET'}

    # ===== 计算 fallback 分配（仅对无时间标注且无 BUDGET 的模块）=====
    total_steps_min = sum(s.get('minutes', 0) for s in steps) if steps else 0
    annotated_total = sum(m for _, _, m, _ in module_headers if m is not None)
    # 无标注模块 = 无时间标注 AND 无已有 BUDGET
    unannotated_needing = [(idx, t, m, h) for idx, t, m, h in module_headers
                           if m is None and not h]
    unannotated_count = len(unannotated_needing)

    if unannotated_count > 0 and total_steps_min > 0:
        remaining_min = max(total_steps_min - annotated_total, 0)
        fallback_min_per_module = remaining_min / unannotated_count
    else:
        fallback_min_per_module = 0

    # ===== 第二遍：注入 BUDGET 注释 =====
    new_lines = []
    modules_injected = 0
    modules_exempt = 0
    header_idx = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        if re.match(r'^## ', line) and not re.match(r'^### ', line):
            if header_idx < len(module_headers):
                _, title, annotated_min, has_budget = module_headers[header_idx]
                header_idx += 1

                # 已有 BUDGET → 跳过
                if has_budget:
                    i += 1
                    continue

                # 确定模块分钟数
                module_minutes = annotated_min if annotated_min is not None else fallback_min_per_module

                # 确定下一个模块的起始行
                next_module_line = module_headers[header_idx][0] if header_idx < len(module_headers) else len(lines)

                # 判断是否为活动模块
                title_is_activity = is_activity_module(title)

                if title_is_activity:
                    # 活动/实践模块 → 注入豁免标记
                    budget_line = '<!-- BUDGET: 0 chars | TYPE: activity | STATUS: exempt -->'
                    new_lines.append(budget_line)
                    modules_exempt += 1
                    modules_injected += 1

                    if dry_run:
                        print(f"  🏷️  {title[:50]}")
                        print(f"     {budget_line} [活动模块]")
                elif module_minutes and module_minutes > 0:
                    # 讲授模块 → 计算 BUDGET
                    activity_min = 0
                    j = i + 1
                    while j < next_module_line:
                        if '**Duration**' in lines[j]:
                            act_m = re.search(r'(\d+)\s*min', lines[j])
                            if act_m:
                                activity_min += int(act_m.group(1))
                        j += 1

                    net_minutes = max(module_minutes - activity_min, 0)
                    budget_chars = int(net_minutes * cn_cpm)
                    slide_min = math.ceil(net_minutes / 3) if net_minutes > 0 else 0

                    # 统计模块实际字数来判定 STATUS
                    module_text = lines[i + 1:next_module_line]
                    cn_count = count_cn_chars('\n'.join(module_text))

                    # STATUS 判定
                    if budget_chars > 0:
                        ratio = cn_count / budget_chars
                        status = 'done' if ratio >= 0.8 else 'pending'
                    else:
                        ratio = 0
                        status = 'done'

                    budget_line = f'<!-- BUDGET: {budget_chars} chars | SLIDES: ≥{slide_min} | STATUS: {status} -->'
                    new_lines.append(budget_line)
                    modules_injected += 1

                    if dry_run:
                        pct = f"{ratio*100:.0f}%" if budget_chars > 0 else "-"
                        src_label = "" if annotated_min is not None else " [均分]"
                        print(f"  💉 {title[:50]}")
                        print(f"     {budget_line}{src_label}")
                        print(f"     实际: {cn_count} 字 | 填充: {pct} | 净时长: {net_minutes:.0f}min")
                else:
                    # 无法推算时间，也不是活动模块 → 用实际字数 fallback
                    module_text = lines[i + 1:next_module_line]
                    cn_count = count_cn_chars('\n'.join(module_text))
                    if cn_count > 0:
                        # 基于实际字数反推时长
                        est_min = cn_count / cn_cpm
                        slide_min = math.ceil(est_min / 3) if est_min > 0 else 0
                        budget_line = f'<!-- BUDGET: {cn_count} chars | SLIDES: ≥{slide_min} | STATUS: pending -->'
                    else:
                        budget_line = '<!-- BUDGET: 0 chars | TYPE: activity | STATUS: exempt -->'
                        modules_exempt += 1
                    new_lines.append(budget_line)
                    modules_injected += 1

                    if dry_run:
                        print(f"  ⚡ {title[:50]}")
                        print(f"     {budget_line} [字数反推]")

        i += 1

    if not dry_run and modules_injected > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

    return {
        'file': os.path.basename(file_path),
        'status': 'injected' if modules_injected > 0 else 'no_change',
        'count': modules_injected,
        'exempt': modules_exempt,
    }


def main():
    parser = argparse.ArgumentParser(description="批量注入 BUDGET/STATUS 注释")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不修改文件")
    parser.add_argument("--week", type=int, default=None, help="仅处理指定周次")
    args = parser.parse_args()

    workspace = get_workspace_root()
    scripts_dir = get_scripts_dir(workspace, args.course)
    course_config = load_course_config(workspace, args.course)
    cn_cpm = get_cn_cpm(course_config)

    if not os.path.exists(scripts_dir):
        print(f"❌ 脚本目录不存在: {scripts_dir}")
        sys.exit(1)

    files = list_script_files(scripts_dir)

    if args.week is not None:
        week_prefix = f"W{args.week:02d}_"
        files = [f for f in files if f.startswith(week_prefix)]

    if not files:
        print("⚠️ 未找到脚本文件。")
        sys.exit(0)

    mode_label = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{mode_label}💉 BUDGET 注入 v2（增量）  |  课程: {args.course}  |  语速: {cn_cpm} 字/分钟")
    print("=" * 60)

    total_injected = 0
    total_skipped = 0
    total_no_time = 0

    # 加载全量 calendar 用于 steps 查询（通过 load_course_config 自动支持拆分架构）
    full_config = load_course_config(workspace, args.course)
    full_calendar = full_config.get('calendar', [])

    for fname in files:
        fpath = os.path.join(scripts_dir, fname)
        week_num = extract_week_number(fname)

        # 获取本周 steps
        steps = None
        if week_num and full_calendar:
            for entry in full_calendar:
                if entry.get('week') == week_num:
                    lessons = entry.get('lessons', [])
                    if lessons:
                        steps = lessons[0].get('steps', [])
                    break

        print(f"\n📄 {fname}" + (f"  (W{week_num})" if week_num else ""))
        result = process_script(fpath, steps, cn_cpm, dry_run=args.dry_run)

        if result['status'] == 'skip':
            print(f"  ⏭️  跳过: {result['reason']}")
            total_skipped += 1
        elif result['status'] == 'injected':
            exempt_note = f"（含 {result.get('exempt', 0)} 个活动豁免）" if result.get('exempt', 0) > 0 else ""
            print(f"  ✅ 注入 {result['count']} 个 BUDGET 注释{exempt_note}")
            total_injected += result['count']
        else:
            print(f"  ⚠️  无可注入的模块")
            total_no_time += 1

    print(f"\n{'=' * 60}")
    print(f"  📊 汇总: 注入 {total_injected} | 跳过 {total_skipped} | 无模块 {total_no_time}")
    if args.dry_run:
        print(f"  ℹ️  试运行模式，未修改任何文件。移除 --dry-run 执行实际注入。")


if __name__ == "__main__":
    main()
