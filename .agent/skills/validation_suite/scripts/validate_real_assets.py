#!/usr/bin/env python3
"""
真实素材覆盖率验收引擎 (Real Asset Coverage Validator)

验证 sourcing_checklist 中标记为 download/generate 的条目
是否已成功落盘并注入 Markdown 脚本。

用法:
    python validate_real_assets.py --course "交互产品开发" --week W02
    python validate_real_assets.py --checklist <sourcing_checklist.yaml> --src-dir <src/>

检查项:
  V1: target_path 指向的物理文件是否存在
  V2: Markdown 中是否已注入 _real Asset 行
  V3: AI fallback 行是否保留
  V4: Source 字段是否已更新
  V5: Locked 标记的一致性

输出:
  控制台报告 + exit code（0=全部通过, 1=存在问题）
"""

import sys
import yaml
from pathlib import Path

# 导入共享的 VISUAL 块读写模块
SCANNER_SCRIPTS = Path(__file__).parent.parent.parent / "real_asset_scanner" / "scripts"
sys.path.insert(0, str(SCANNER_SCRIPTS))

try:
    from visual_block_io import parse_visual_blocks, scan_all_blocks
except ImportError:
    print("⚠️  无法导入 visual_block_io，尝试独立运行模式")
    parse_visual_blocks = None
    scan_all_blocks = None


def find_course_week(course_name: str, week_id: str) -> tuple[Path, Path] | None:
    """
    在工作区中定位课程的教学周目录。
    返回 (src_dir, public_slides_dir) 元组。
    """
    workspace = Path("/Users/yamlam/Downloads/2025-2026-2 课程")
    course_dir = workspace / course_name

    if not course_dir.exists():
        print(f"❌ 课程目录不存在: {course_dir}")
        return None

    weeks_dir = course_dir / "weeks"
    if not weeks_dir.exists():
        print(f"❌ weeks 目录不存在: {weeks_dir}")
        return None

    # 查找匹配的周次目录
    week_upper = week_id.upper()
    for d in sorted(weeks_dir.iterdir()):
        if d.is_dir() and d.name.upper().startswith(week_upper):
            src_dir = d / "src"
            public_slides = d / "public" / "slides"
            if src_dir.exists():
                return src_dir, public_slides

    print(f"❌ 未找到匹配的周次目录: {week_id}")
    return None


def validate_from_checklist(checklist_path: Path, src_dir: Path) -> dict:
    """
    从 sourcing_checklist.yaml 执行验证。
    返回验证结果字典。
    """
    with open(checklist_path, 'r', encoding='utf-8') as f:
        items = yaml.safe_load(f) or []

    # 建立 VISUAL 块索引
    block_index = {}
    if scan_all_blocks:
        block_index = scan_all_blocks(src_dir)

    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "details": [],
    }

    actionable = [
        it for it in items
        if it.get("disposition") in ("download", "generate")
    ]
    locked = [it for it in items if it.get("disposition") == "lock"]

    results["total"] = len(actionable) + len(locked)

    # ─── V1 + V2 + V3 + V4: 验证 download/generate 条目 ───
    for item in actionable:
        slide_id = item.get("slide", "?")
        target_path = item.get("target_path", "")
        disposition = item.get("disposition", "")
        detail = {"slide": slide_id, "checks": [], "status": "pass"}

        # V1: 物理文件是否存在
        if target_path:
            abs_path = (src_dir / target_path).resolve()
            if abs_path.exists():
                size_kb = abs_path.stat().st_size / 1024
                detail["checks"].append(f"✅ V1: 文件存在 ({size_kb:.0f}KB)")
            else:
                detail["checks"].append(f"❌ V1: 文件不存在 → {abs_path}")
                detail["status"] = "fail"
        else:
            detail["checks"].append("❌ V1: 无 target_path")
            detail["status"] = "fail"

        # V2 + V3 + V4: Markdown 注入验证
        if slide_id in block_index:
            _, block = block_index[slide_id]

            # V2: 主 Asset 是否指向 _real
            if '_real' in block.asset_path:
                detail["checks"].append("✅ V2: 主 Asset 已指向 _real")
            else:
                detail["checks"].append(f"❌ V2: 主 Asset 仍为 {block.asset_path}")
                detail["status"] = "fail"

            # V3: AI fallback 是否保留
            if block.asset_fallback_path:
                detail["checks"].append("✅ V3: AI fallback 已保留")
            else:
                detail["checks"].append("⚠️  V3: 无 AI fallback 行（可能未实现双轨）")
                if detail["status"] == "pass":
                    detail["status"] = "warn"

            # V4: Source 字段是否已更新
            if block.source:
                if disposition == "download" and any(kw in block.source.lower() for kw in ('web', 'external', 'source')):
                    detail["checks"].append("✅ V4: Source 已标记为外部来源")
                elif disposition == "generate" and 'generated' in block.source.lower():
                    detail["checks"].append("✅ V4: Source 已标记为 AI Generated")
                else:
                    detail["checks"].append(f"⚠️  V4: Source 内容待确认 → {block.source[:40]}")
            else:
                detail["checks"].append("⚠️  V4: 无 Source 字段")
                if detail["status"] == "pass":
                    detail["status"] = "warn"
        else:
            detail["checks"].append(f"❌ V2-V4: slide_id={slide_id} 未在脚本中找到")
            detail["status"] = "fail"

        results["details"].append(detail)
        if detail["status"] == "pass":
            results["passed"] += 1
        elif detail["status"] == "warn":
            results["warnings"] += 1
            results["passed"] += 1  # 警告仍算通过
        else:
            results["failed"] += 1

    # ─── V5: 验证 lock 条目 ───
    for item in locked:
        slide_id = item.get("slide", "?")
        detail = {"slide": slide_id, "checks": [], "status": "pass"}

        if slide_id in block_index:
            _, block = block_index[slide_id]
            if block.source and 'locked' in block.source.lower():
                detail["checks"].append("✅ V5: Locked 标记一致")
            else:
                detail["checks"].append(f"⚠️  V5: Source 未包含 Locked 标记 → {block.source[:40] if block.source else '空'}")
                detail["status"] = "warn"
                results["warnings"] += 1
        else:
            detail["checks"].append(f"⚠️  V5: slide_id={slide_id} 未在脚本中找到")
            detail["status"] = "warn"
            results["warnings"] += 1

        results["details"].append(detail)
        if detail["status"] == "pass":
            results["passed"] += 1

    return results


def print_report(results: dict):
    """打印验证报告"""
    total = results["total"]
    passed = results["passed"]
    failed = results["failed"]
    warnings = results["warnings"]

    print(f"\n{'='*50}")
    print(f"  📊 真实素材覆盖率验证报告")
    print(f"{'='*50}")
    print(f"  总条目:     {total}")
    print(f"  ✅ 通过:    {passed}")
    print(f"  ⚠️  警告:    {warnings}")
    print(f"  ❌ 失败:    {failed}")
    coverage = (passed / total * 100) if total > 0 else 0
    print(f"  📈 覆盖率:  {coverage:.0f}%")
    print(f"{'='*50}")

    # 仅显示有问题的条目
    issues = [d for d in results["details"] if d["status"] != "pass"]
    if issues:
        print(f"\n  🔍 问题明细:")
        for d in issues:
            icon = "❌" if d["status"] == "fail" else "⚠️ "
            print(f"    {icon} [{d['slide']}]")
            for check in d["checks"]:
                if not check.startswith("✅"):
                    print(f"       {check}")
    elif total > 0:
        print(f"\n  🎉 所有素材验证通过！")


def main():
    checklist_path = None
    src_dir = None
    course_name = None
    week_id = None

    # 解析命令行参数
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--checklist" and i + 1 < len(args):
            checklist_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--src-dir" and i + 1 < len(args):
            src_dir = Path(args[i + 1])
            i += 2
        elif args[i] == "--course" and i + 1 < len(args):
            course_name = args[i + 1]
            i += 2
        elif args[i] == "--week" and i + 1 < len(args):
            week_id = args[i + 1]
            i += 2
        else:
            i += 1

    # 模式 1: --course + --week
    if course_name and week_id:
        result = find_course_week(course_name, week_id)
        if not result:
            sys.exit(1)
        src_dir, _ = result
        checklist_path = src_dir / "sourcing_checklist.yaml"

    # 验证参数
    if not checklist_path or not checklist_path.exists():
        print(f"❌ 清单文件不存在: {checklist_path}")
        print("用法:")
        print('  python validate_real_assets.py --course "交互产品开发" --week W02')
        print("  python validate_real_assets.py --checklist <path> --src-dir <path>")
        sys.exit(1)

    if not src_dir:
        src_dir = checklist_path.parent

    print(f"🔍 验证清单: {checklist_path.name}")
    print(f"📁 源目录:   {src_dir}")

    results = validate_from_checklist(checklist_path, src_dir)
    print_report(results)

    # exit code
    sys.exit(1 if results["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
