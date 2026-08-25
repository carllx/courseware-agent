#!/usr/bin/env python3
"""
课程端本地 steps 校验脚本 (validate_steps.py)
覆盖 audit.md F14 (C-1~C-4) + F2 (阶段完整性) 规则。
独立于教务端审计脚本，可在修改 course.yaml 后立即运行。

用法:
  python scripts/validate_steps.py                         # 扫描工作区全部课程
  python scripts/validate_steps.py 信息可视化              # 扫描指定课程
  python scripts/validate_steps.py --strict                # 严格模式 (±0 容差)
"""
import yaml
import os
import sys
import argparse
from pathlib import Path

# ───────────────────────────────────────────
# 常量定义
# ───────────────────────────────────────────

# stage 归属分类（与教务端 _THEORY_STAGE_KEYWORDS / _PRACTICE_STAGE_KEYWORDS 对齐）
THEORY_STAGES = {'复习', '导入', '讲授', '演示'}
PRACTICE_STAGES = {'实践', '练习', '训练', '总结', '小结'}

# F2: 常规周应包含的 5 个 stage 种类
FULL_STAGES = {'复习', '导入', '讲授', '实践', '小结'}
W1_STAGES = {'导入', '讲授', '实践', '小结'}  # 首周豁免复习

# 阈值（与教务端 Gate-2 / 审计 C-2 对齐）
WARN_HOURS_DEV = 0.5     # 理论/实践偏差 > 0.5h → WARN
CRIT_HOURS_DEV = 1.0     # 理论/实践偏差 > 1.0h → CRITICAL
WARN_TOTAL_PCT = 0.15    # 总分钟偏差 > 15% → WARN
C3_THEORY_LIMIT = 30     # 纯实践周理论 stage 上限 (分钟)

# 输出颜色
class C:
    OK = '\033[92m'
    WARN = '\033[93m'
    CRIT = '\033[91m'
    DIM = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'


# ───────────────────────────────────────────
# 核心校验逻辑
# ───────────────────────────────────────────

def classify_minutes(steps: list) -> tuple:
    """将 steps 按 stage 分类，返回 (理论分钟数, 实践分钟数, 未知stage列表)"""
    theory_min = 0
    practice_min = 0
    unknown = []
    for step in steps:
        stage = step.get('stage', '')
        mins = step.get('minutes', 0) or 0
        if stage in THEORY_STAGES:
            theory_min += mins
        elif stage in PRACTICE_STAGES:
            practice_min += mins
        else:
            unknown.append((stage, mins))
    return theory_min, practice_min, unknown


def validate_week(week: dict, mpp: int, strict: bool = False, is_last_week: bool = False) -> list:
    """校验单周 steps，返回 [(级别, 消息)] 列表"""
    issues = []
    wn = week.get('week', 0)
    ht = week.get('hours_theory', 0) or 0
    hp = week.get('hours_practice', 0) or 0
    total_declared = (ht + hp) * mpp

    # 收集所有 steps
    all_steps = []
    stage_sequence = []
    for lesson in week.get('lessons', []):
        for step in lesson.get('steps', []):
            all_steps.append(step)
            stage_sequence.append(step.get('stage', ''))

    if not all_steps:
        return issues  # 无 steps 数据，跳过

    theory_min, practice_min, unknown = classify_minutes(all_steps)
    total_min = theory_min + practice_min

    # ─── C-1: W1 禁止复习 ───
    if wn == 1:
        for step in all_steps:
            if step.get('stage', '') == '复习':
                issues.append(('CRITICAL', 'C-1: W1 含 stage=复习（首次课无先前内容可复习）'))

    # ─── C-2: 理论/实践 stage 分钟 vs 声明学时 ───
    if ht + hp > 0 and total_min > 0:
        t_hours = theory_min / mpp
        p_hours = practice_min / mpp
        t_dev = abs(t_hours - ht)
        p_dev = abs(p_hours - hp)

        if strict:
            # 严格模式：任何偏差都报告
            if t_dev > 0.01:
                issues.append(('WARN', f'C-2(strict): 理论 {theory_min}min={t_hours:.1f}h vs 声明 {ht}h，偏差 {t_dev:.1f}h'))
            if p_dev > 0.01:
                issues.append(('WARN', f'C-2(strict): 实践 {practice_min}min={p_hours:.1f}h vs 声明 {hp}h，偏差 {p_dev:.1f}h'))
        else:
            if t_dev > CRIT_HOURS_DEV:
                issues.append(('CRITICAL', f'C-2: 理论 {theory_min}min={t_hours:.1f}h vs 声明 {ht}h，偏差 {t_dev:.1f}h (>{CRIT_HOURS_DEV}h)'))
            elif t_dev > WARN_HOURS_DEV:
                issues.append(('WARN', f'C-2: 理论 {theory_min}min={t_hours:.1f}h vs 声明 {ht}h，偏差 {t_dev:.1f}h (>{WARN_HOURS_DEV}h)'))

            if p_dev > CRIT_HOURS_DEV:
                issues.append(('CRITICAL', f'C-2: 实践 {practice_min}min={p_hours:.1f}h vs 声明 {hp}h，偏差 {p_dev:.1f}h (>{CRIT_HOURS_DEV}h)'))
            elif p_dev > WARN_HOURS_DEV:
                issues.append(('WARN', f'C-2: 实践 {practice_min}min={p_hours:.1f}h vs 声明 {hp}h，偏差 {p_dev:.1f}h (>{WARN_HOURS_DEV}h)'))

    # ─── C-3: 纯实践周理论 stage 限制 ───
    if ht == 0 and theory_min > C3_THEORY_LIMIT:
        issues.append(('WARN', f'C-3: 纯实践周(hours_theory=0)理论 stage {theory_min}min > {C3_THEORY_LIMIT}min'))

    # ─── C-4: 总分钟一致性 ───
    if total_declared > 0:
        deviation_pct = abs(total_min - total_declared) / total_declared
        deviation_min = abs(total_min - total_declared)
        if deviation_min > mpp:
            issues.append(('CRITICAL', f'C-4: 总分钟 {total_min}min vs 预期 {total_declared}min，偏差 {deviation_min}min (>{mpp}min=1课时)'))
        elif deviation_pct > WARN_TOTAL_PCT:
            issues.append(('WARN', f'C-4: 总分钟 {total_min}min vs 预期 {total_declared}min，偏差 {deviation_pct:.0%} (>{WARN_TOTAL_PCT:.0%})'))

    # ─── F2: 阶段完整性（末周豁免） ───
    if not is_last_week:
        stage_set = set(stage_sequence)
        expected = W1_STAGES if wn == 1 else FULL_STAGES
        missing = expected - stage_set
        if missing and wn != 1:
            issues.append(('WARN', f'F2: 缺少 stage 种类: {", ".join(sorted(missing))}'))
        elif missing and wn == 1:
            extra_missing = W1_STAGES - stage_set
            if extra_missing:
                issues.append(('WARN', f'F2: W1 缺少 stage 种类: {", ".join(sorted(extra_missing))}'))

    # ─── F2 扩展: 连续重复 stage ───
    for i in range(1, len(stage_sequence)):
        if stage_sequence[i] == stage_sequence[i - 1]:
            issues.append(('WARN', f'F2: 连续重复 stage "{stage_sequence[i]}"（应合并或重新分类）'))
            break  # 只报一次

    # ─── 未知 stage ───
    for stage, mins in unknown:
        issues.append(('WARN', f'未知 stage "{stage}" ({mins}min)，未归属理论/实践'))

    return issues


def validate_course(course_dir: Path, strict: bool = False) -> dict:
    """校验单门课程，返回 {课程名: [(周, 级别, 消息)]}"""
    # 支持拆分架构：优先读 course_meta.yaml + course_calendar.yaml
    meta_path = course_dir / 'course_meta.yaml'
    calendar_path = course_dir / 'course_calendar.yaml'
    yaml_path = course_dir / 'course.yaml'

    if meta_path.exists() and calendar_path.exists():
        # 拆分模式
        data = {}
        for fname in ['course_meta.yaml', 'course_calendar.yaml', 'course_objectives.yaml',
                      'course_experiments.yaml', 'course_assessment.yaml', 'course_textbooks.yaml']:
            fpath = course_dir / fname
            if fpath.exists():
                with open(fpath, 'r', encoding='utf-8') as f:
                    part = yaml.safe_load(f)
                if part:
                    data.update(part)
    elif yaml_path.exists():
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    else:
        return {}

    course = data.get('course', {})
    if not isinstance(course, dict):
        return {}  # 结构不完整（如实习指导），跳过
    name = course.get('name', course_dir.name)
    hours = course.get('hours', {})
    if not isinstance(hours, dict):
        return {}
    mpp = hours.get('minutes_per_period', 45)
    calendar = data.get('calendar', [])

    results = []
    total_weeks = len(calendar)
    for idx, week in enumerate(calendar):
        wn = week.get('week', 0)
        is_last = (idx == total_weeks - 1)
        issues = validate_week(week, mpp, strict, is_last_week=is_last)
        for level, msg in issues:
            results.append((wn, level, msg))

    return {name: results}


# ───────────────────────────────────────────
# 输出格式化
# ───────────────────────────────────────────

def print_results(all_results: dict) -> int:
    """打印校验结果，返回 CRITICAL 数量"""
    total_critical = 0
    total_warn = 0

    for course_name, issues in all_results.items():
        crits = sum(1 for _, l, _ in issues if l == 'CRITICAL')
        warns = sum(1 for _, l, _ in issues if l == 'WARN')
        total_critical += crits
        total_warn += warns

        if not issues:
            print(f"\n{C.OK}✅ {course_name}: 全部通过{C.END}")
        else:
            status_color = C.CRIT if crits > 0 else C.WARN
            print(f"\n{status_color}{'🔴' if crits else '🟡'} {course_name}: {crits} CRITICAL, {warns} WARN{C.END}")
            for wn, level, msg in issues:
                color = C.CRIT if level == 'CRITICAL' else C.WARN
                print(f"  {color}[{level}]{C.END} W{wn:02d}: {msg}")

    # 汇总
    print(f"\n{'─' * 50}")
    if total_critical == 0 and total_warn == 0:
        print(f"{C.OK}{C.BOLD}✅ 全部通过 — 零 CRITICAL，零 WARN{C.END}")
    elif total_critical == 0:
        print(f"{C.WARN}{C.BOLD}🟡 零 CRITICAL，{total_warn} WARN{C.END}")
    else:
        print(f"{C.CRIT}{C.BOLD}🔴 {total_critical} CRITICAL，{total_warn} WARN{C.END}")

    return total_critical


# ───────────────────────────────────────────
# 主函数
# ───────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='课程端 steps 本地校验 (F14 C-1~C-4 + F2)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python scripts/validate_steps.py                  # 扫描全部课程
  python scripts/validate_steps.py 信息可视化       # 指定课程
  python scripts/validate_steps.py --strict          # 严格模式
        '''
    )
    parser.add_argument('course', nargs='?', help='指定课程目录名（可选，默认扫描全部）')
    parser.add_argument('--strict', action='store_true', help='严格模式：任何偏差都报告')
    parser.add_argument('--root', default='.', help='工作区根目录（默认当前目录）')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    all_results = {}

    if args.course:
        # 指定课程
        course_dir = root / args.course
        if not course_dir.exists():
            print(f"❌ 课程目录不存在: {course_dir}")
            sys.exit(1)
        all_results.update(validate_course(course_dir, args.strict))
    else:
        # 扫描全部含 course_meta.yaml 或 course.yaml 的子目录
        for item in sorted(root.iterdir()):
            if item.is_dir() and (
                (item / 'course_meta.yaml').exists() or
                (item / 'course.yaml').exists()
            ):
                all_results.update(validate_course(item, args.strict))

    if not all_results:
        print("⚠️ 未找到任何课程配置文件")
        sys.exit(1)

    crits = print_results(all_results)
    sys.exit(1 if crits > 0 else 0)


if __name__ == '__main__':
    main()
