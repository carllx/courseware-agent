#!/usr/bin/env python3
"""
视觉信标对齐检查 (Visual Signaling Sync Validator)

基于 Mayer Signaling Principle 的内容类型分流模型检查脚本中
[VISUAL] 块的 List 字段与其后 Speech 段落的对齐质量。

内容类型分流：
  - 结构性枚举 → 必须有 List（≤4字/项）
  - 操作性步骤 → 必须有 List
  - 论证性递进 → 禁止有 List（冗余效应风险）
  - 修辞性排比 → 绝对禁止 List（杀死情感冲击力）

用法:
    python validate_visual_text_sync.py --course "交互产品开发"
    python validate_visual_text_sync.py --course "交互产品开发" --week 1
    python validate_visual_text_sync.py --course "交互产品开发" --week 2 --legacy
"""

import os
import sys
import re
import argparse
from pathlib import Path

# 确保能 import 同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_parser import (
    parse_script, BlockType, get_workspace_root,
    get_scripts_dir, list_script_files, list_script_files_for_week,
)


# ============================================================
# 内容类型分类器 (Content Type Classifier)
# ============================================================

# 结构性枚举特征词：定义/框架/分类等学术结构
_RE_STRUCTURAL_KEYWORDS = re.compile(
    r'(?:定义|框架|分类|维度|原则|标准|阶段|类型|层次|要素|模型|'
    r'评分|考核|任务|指标|规则|方法论|理论|公式|组件|属性|参数|'
    r'特征|条件|要求|功能|模式|'
    r'(?:分为|分成|包括|包含|由.*组成|划分为)\s*(?:[\d一二三四五六七八九十]+))',
)

# 操作性步骤特征词：动作动词开头
_RE_OPERATIONAL_KEYWORDS = re.compile(
    r'(?:Step|步骤|打开|选择|点击|输入|导出|新建|拖入|上传|下载|'
    r'复制|粘贴|删除|创建|设置|配置|切换|提交|发送|保存|运行|'
    r'启动|安装|执行|观察|记录|标注)',
)

# 修辞性排比特征词：情感渲染/排比结构
_RE_RHETORICAL_KEYWORDS = re.compile(
    r'(?:它让|它使|它把|让.*让.*让|使.*使.*使|'
    r'既.*又.*既.*又|不是.*而是.*不是.*而是|'
    r'没有.*没有.*没有|有的.*有的.*有的)',
)

# 论证性递进特征词：逻辑连接词
_RE_ARGUMENTATIVE_KEYWORDS = re.compile(
    r'(?:首先|其次|再次|最后|第一|第二|第三|第四|'
    r'一是|二是|三是|四是|'
    r'一方面|另一方面|此外|再者|不仅.*而且)',
)

# 通用并列要点检测（保留原有逻辑）
_RE_NUMBERED_LIST = re.compile(
    r'(?:第[一二三四五六七八九十\d]+[个种类点步条项]|'
    r'[一二三四五六七八九十]\s*[是为、]|'
    r'(?:\d+[\.\\)、）])\s*[\u4e00-\u9fff])',
)

_RE_PARALLEL_ITEMS = re.compile(
    r'(?:首先|其次|再次|最后|第一|第二|第三|第四|'
    r'一是|二是|三是|四是)',
)


def _count_structural_items(text: str) -> int:
    """统计 Speech 文本中的结构化并列要点数量。"""
    count = 0
    count += len(_RE_NUMBERED_LIST.findall(text))
    count += len(_RE_PARALLEL_ITEMS.findall(text))
    return count


def classify_parallel_type(text: str) -> str:
    """
    对包含 ≥3 个并列要点的 Speech 文本进行内容类型分类。

    返回:
      - "structural"    结构性枚举（定义/框架/分类等）
      - "operational"   操作性步骤（SOP/实践指引）
      - "rhetorical"    修辞性排比（情感渲染/排比句式）
      - "argumentative"  论证性递进（首先…其次…）
      - "ambiguous"     无法确定

    分类优先级: operational > structural > rhetorical > argumentative
    """
    op_score = len(_RE_OPERATIONAL_KEYWORDS.findall(text))
    st_score = len(_RE_STRUCTURAL_KEYWORDS.findall(text))
    rh_score = len(_RE_RHETORICAL_KEYWORDS.findall(text))
    ar_score = len(_RE_ARGUMENTATIVE_KEYWORDS.findall(text))

    # 操作性步骤优先：含 ≥2 个操作动词
    if op_score >= 2:
        return "operational"

    # 结构性枚举：含结构特征词
    if st_score >= 1:
        return "structural"

    # 修辞性排比：明确的排比句式
    if rh_score >= 1:
        return "rhetorical"

    # 论证性递进：逻辑连接词但无结构词
    if ar_score >= 2:
        return "argumentative"

    # 无法确定时的启发式：
    # 如果含有编号列表（第一、第二…）但无结构词，更可能是论证递进
    num_count = len(_RE_NUMBERED_LIST.findall(text))
    if num_count >= 3:
        # 检查是否有术语性名词（暗示结构性枚举）
        if st_score >= 1:
            return "structural"
        return "argumentative"

    return "ambiguous"


def _extract_visual_list(block) -> list[str]:
    """从 VISUAL 块中解析 List 字段的内容项。"""
    items = []
    if not block.metadata:
        return items
    in_list = False
    for line in block.raw_lines if hasattr(block, 'raw_lines') else []:
        line_s = line.strip()
        if line_s.startswith("**List**"):
            in_list = True
            after = line_s.replace("**List**", "").replace(":", "").strip()
            if after:
                items.extend([x.strip() for x in after.split("/") if x.strip()])
            continue
        if in_list:
            if line_s.startswith("**") or not line_s:
                in_list = False
                continue
            items.extend([x.strip() for x in line_s.split("/") if x.strip()])
    return items


def analyze_script(script_path: str, legacy_mode: bool = False) -> dict:
    """分析单个脚本文件的视觉-信标对齐状况。"""
    blocks = parse_script(script_path)

    results = {
        "file": os.path.basename(script_path),
        "total_visuals": 0,
        "visuals_with_text": 0,
        "visuals_with_list": 0,
        "heading_empty": [],            # heading 为空的 VISUAL 块
        "signaling_missing": [],        # 结构性枚举/操作步骤缺 List（🔴）
        "redundancy_warnings": [],      # 论证性递进有 List（🟡）
        "rhetorical_violations": [],    # 修辞性排比有 List（🔴）
        "signaling_ambiguous": [],      # 无法自动分类（🟡）
        "text_suggestions": [],         # Text 字段建议
        # 兼容旧版
        "bullet_sync_issues": [],
    }

    last_visual = None
    last_visual_idx = -1
    last_heading = ""

    for i, block in enumerate(blocks):
        if block.block_type == BlockType.HEADER:
            level = block.metadata.get("level", 1)
            if level in (3, 4):
                last_heading = block.content
            continue

        if block.block_type == BlockType.VISUAL:
            results["total_visuals"] += 1
            meta = block.metadata or {}

            text_val = meta.get("text", "")
            has_text = bool(text_val and text_val.strip())
            if has_text:
                results["visuals_with_text"] += 1

            raw = block.content if block.content else ""
            has_list = "**List**" in raw or bool(meta.get("list"))
            if has_list:
                results["visuals_with_list"] += 1

            # Heading 空洞检测
            slide_id = meta.get("slide_id", f"slide-{results['total_visuals']}")
            layout = meta.get("layout", "Unknown")

            if not last_heading and layout.lower() not in ("full", "image"):
                results["heading_empty"].append({
                    "slide_id": slide_id,
                    "layout": layout,
                    "line": block.line_start,
                })

            if not has_text:
                results["text_suggestions"].append({
                    "slide_id": slide_id,
                    "layout": layout,
                    "line": block.line_start,
                    "scene_preview": (meta.get("scene", ""))[:50],
                })

            last_visual = block
            last_visual_idx = i
            continue

        if block.block_type == BlockType.SPEECH and last_visual is not None:
            text = block.content or ""
            item_count = _count_structural_items(text)

            if item_count >= 3:
                v_meta = last_visual.metadata or {}
                v_raw = last_visual.content if last_visual.content else ""
                has_list = "**List**" in v_raw or bool(v_meta.get("list"))
                slide_id = v_meta.get("slide_id", "?")

                issue_base = {
                    "slide_id": slide_id,
                    "visual_line": last_visual.line_start,
                    "speech_line": block.line_start,
                    "item_count": item_count,
                    "speech_preview": text[:80],
                }

                if legacy_mode:
                    # 旧版一刀切模式：所有缺 List 都报错
                    if not has_list:
                        results["bullet_sync_issues"].append(issue_base)
                else:
                    # 新版内容类型分流模式
                    content_type = classify_parallel_type(text)
                    issue_base["content_type"] = content_type

                    if content_type in ("structural", "operational"):
                        if not has_list:
                            results["signaling_missing"].append(issue_base)
                    elif content_type == "argumentative":
                        if has_list:
                            results["redundancy_warnings"].append(issue_base)
                        # 无 List → 正确，不报错
                    elif content_type == "rhetorical":
                        if has_list:
                            results["rhetorical_violations"].append(issue_base)
                        # 无 List → 正确，不报错
                    elif content_type == "ambiguous":
                        results["signaling_ambiguous"].append(issue_base)

            # 重置（只检查紧邻的 SPEECH）
            last_visual = None
            last_visual_idx = -1

    return results


def print_report(all_results: list[dict], course: str, week: int = None,
                 legacy_mode: bool = False):
    """输出格式化的报告。"""
    print(f"\n{'='*60}")
    if legacy_mode:
        print(f"  视觉-文字对齐检查报告 (Legacy Bullet Sync)")
    else:
        print(f"  视觉信标对齐检查报告 (Signaling Sync)")
    print(f"{'='*60}")
    print(f"  课程: {course}")
    if week is not None:
        print(f"  范围: 第 {week} 周")
    print(f"{'='*60}")

    total_visuals = sum(r["total_visuals"] for r in all_results)
    total_with_text = sum(r["visuals_with_text"] for r in all_results)
    total_with_list = sum(r["visuals_with_list"] for r in all_results)
    total_heading_empty = sum(len(r["heading_empty"]) for r in all_results)
    total_text_suggestions = sum(len(r["text_suggestions"]) for r in all_results)

    text_coverage = (total_with_text / total_visuals * 100) if total_visuals > 0 else 0

    print(f"\n📊 总览:")
    print(f"   VISUAL 块总数: {total_visuals}")
    print(f"   含 Text 字段: {total_with_text} ({text_coverage:.0f}%)")
    print(f"   含 List 字段: {total_with_list}")
    print(f"   Heading 空洞: {total_heading_empty}")

    has_issues = False
    has_hard_errors = False

    if legacy_mode:
        # --- 旧版报告 ---
        total_bullet = sum(len(r["bullet_sync_issues"]) for r in all_results)
        print(f"   Bullet Sync 问题: {total_bullet}")
        for r in all_results:
            if r["bullet_sync_issues"]:
                has_issues = True
                has_hard_errors = True
                print(f"\n❌ Bullet Sync 不匹配 — {r['file']}:")
                for issue in r["bullet_sync_issues"]:
                    print(f"   Slide {issue['slide_id']} (L{issue['visual_line']})")
                    print(f"   Speech (L{issue['speech_line']}) 包含 {issue['item_count']} 个并列要点")
                    print(f"   → 但 VISUAL 块无 **List** 字段")
                    print(f"   预览: \"{issue['speech_preview']}...\"")
                    print()
    else:
        # --- 新版 Signaling Sync 报告 ---
        total_missing = sum(len(r["signaling_missing"]) for r in all_results)
        total_redundancy = sum(len(r["redundancy_warnings"]) for r in all_results)
        total_rhetorical = sum(len(r["rhetorical_violations"]) for r in all_results)
        total_ambiguous = sum(len(r["signaling_ambiguous"]) for r in all_results)

        print(f"   🔴 信标缺失 (结构性枚举/操作步骤): {total_missing}")
        print(f"   🔴 修辞排比有 List: {total_rhetorical}")
        print(f"   🟡 冗余风险 (论证递进有 List): {total_redundancy}")
        print(f"   🟡 分类不确定: {total_ambiguous}")

        # 信标缺失（🔴）
        for r in all_results:
            if r["signaling_missing"]:
                has_issues = True
                has_hard_errors = True
                print(f"\n🔴 信标缺失 — {r['file']}:")
                for issue in r["signaling_missing"]:
                    ct = issue.get("content_type", "?")
                    ct_label = "结构性枚举" if ct == "structural" else "操作性步骤"
                    print(f"   Slide {issue['slide_id']} (L{issue['visual_line']})")
                    print(f"   类型: {ct_label} | Speech (L{issue['speech_line']}) 含 {issue['item_count']} 个并列要点")
                    print(f"   → VISUAL 块必须有 **List** 字段（≤4 字/项）")
                    print(f"   预览: \"{issue['speech_preview']}...\"")
                    print()

        # 修辞排比有 List（🔴）
        for r in all_results:
            if r["rhetorical_violations"]:
                has_issues = True
                has_hard_errors = True
                print(f"\n🔴 修辞排比不应有 List — {r['file']}:")
                for issue in r["rhetorical_violations"]:
                    print(f"   Slide {issue['slide_id']} (L{issue['visual_line']})")
                    print(f"   Speech (L{issue['speech_line']}) 为修辞性排比")
                    print(f"   → 文字化杀死情感冲击力，必须移除 **List** 字段")
                    print(f"   预览: \"{issue['speech_preview']}...\"")
                    print()

        # 冗余风险（🟡）
        for r in all_results:
            if r["redundancy_warnings"]:
                has_issues = True
                print(f"\n🟡 冗余效应风险 — {r['file']}:")
                for issue in r["redundancy_warnings"]:
                    print(f"   Slide {issue['slide_id']} (L{issue['visual_line']})")
                    print(f"   Speech (L{issue['speech_line']}) 为论证性递进")
                    print(f"   → 口述已充分传递，建议移除 **List** 字段")
                    print(f"   预览: \"{issue['speech_preview']}...\"")
                    print()

        # 分类不确定（🟡）
        for r in all_results:
            if r["signaling_ambiguous"]:
                has_issues = True
                print(f"\n🟡 分类不确定（需 Agent 人工判定）— {r['file']}:")
                for issue in r["signaling_ambiguous"]:
                    print(f"   Slide {issue['slide_id']} (L{issue['visual_line']})")
                    print(f"   Speech (L{issue['speech_line']}) 含 {issue['item_count']} 个并列要点")
                    print(f"   预览: \"{issue['speech_preview']}...\"")
                    print()

    # Text 字段建议
    for r in all_results:
        if r["text_suggestions"]:
            has_issues = True
            print(f"\n⚠️  Text 字段缺失 — {r['file']}:")
            for sug in r["text_suggestions"]:
                print(f"   {sug['slide_id']} ({sug['layout']}) L{sug['line']}")
                if sug['scene_preview']:
                    print(f"   Scene: \"{sug['scene_preview']}...\"")

    # Heading 空洞
    for r in all_results:
        if r["heading_empty"]:
            print(f"\n💡 Heading 空洞 — {r['file']}:")
            for h in r["heading_empty"]:
                print(f"   {h['slide_id']} ({h['layout']}) L{h['line']} — 无结构标题")

    if not has_issues:
        print(f"\n✅ 视觉信标对齐检查通过！")

    print(f"\n{'='*60}")

    # 退出码：信标缺失或修辞排比有 List → 硬性错误
    return 1 if has_hard_errors else 0


def main():
    parser = argparse.ArgumentParser(description="视觉信标对齐检查 (Signaling Sync)")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--week", type=int, default=None, help="仅检查指定周次")
    parser.add_argument("--legacy", action="store_true",
                        help="使用旧版 Bullet Sync 一刀切模式（向后兼容）")
    args = parser.parse_args()

    workspace = get_workspace_root()
    scripts_dir = get_scripts_dir(workspace, args.course)

    if not os.path.exists(scripts_dir):
        print(f"❌ 脚本目录不存在: {scripts_dir}")
        sys.exit(1)

    if args.week is not None:
        script_files = list_script_files_for_week(scripts_dir, args.week)
    else:
        script_files = list_script_files(scripts_dir)

    if not script_files:
        print(f"⚠️  未找到脚本文件")
        sys.exit(0)

    all_results = []
    for fname in script_files:
        fpath = os.path.join(scripts_dir, fname)
        result = analyze_script(fpath, legacy_mode=args.legacy)
        all_results.append(result)

    exit_code = print_report(all_results, args.course, args.week,
                             legacy_mode=args.legacy)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
