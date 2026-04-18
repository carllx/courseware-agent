#!/usr/bin/env python3
"""
视觉文字对齐检查 (Visual-Text Alignment Validator)

检查脚本中 [VISUAL] 块的 Text/List 字段与其后 Speech 段落的对齐质量。
涵盖：Bullet Sync 自动检测 + Text 覆盖率 + Heading 空洞检测。

用法:
    python validate_visual_text_sync.py --course "交互产品开发"
    python validate_visual_text_sync.py --course "交互产品开发" --week 1
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
# 检测规则
# ============================================================

# Bullet Sync: 识别 Speech 中的结构化要点模式
_RE_NUMBERED_LIST = re.compile(
    r'(?:第[一二三四五六七八九十\d]+[个种类点步条项]|'
    r'[一二三四五六七八九十]\s*[是为、]|'
    r'(?:\d+[\.\)、）])\s*[\u4e00-\u9fff])',
)

_RE_PARALLEL_ITEMS = re.compile(
    r'(?:首先|其次|再次|最后|第一|第二|第三|第四|'
    r'一是|二是|三是|四是)',
)


def _count_structural_items(text: str) -> int:
    """统计 Speech 文本中的结构化并列要点数量。"""
    count = 0
    # 检测编号列表
    count += len(_RE_NUMBERED_LIST.findall(text))
    # 检测并列连接词
    count += len(_RE_PARALLEL_ITEMS.findall(text))
    return count


def _extract_visual_list(block) -> list[str]:
    """从 VISUAL 块中解析 List 字段的内容项。"""
    items = []
    if not block.metadata:
        return items
    # 解析块的原始文本中的 List 字段
    in_list = False
    for line in block.raw_lines if hasattr(block, 'raw_lines') else []:
        line_s = line.strip()
        if line_s.startswith("**List**"):
            in_list = True
            # List 可能在同一行
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


def analyze_script(script_path: str) -> dict:
    """分析单个脚本文件的视觉-文字对齐状况。"""
    blocks = parse_script(script_path)
    
    results = {
        "file": os.path.basename(script_path),
        "total_visuals": 0,
        "visuals_with_text": 0,
        "visuals_with_list": 0,
        "heading_empty": [],       # heading 为空的 VISUAL 块
        "bullet_sync_issues": [],  # Bullet Sync 不匹配
        "text_suggestions": [],    # Text 字段建议
    }
    
    # 双指针：遍历 blocks，检查 VISUAL → SPEECH 对
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
            
            # 检查 List 字段（通过原始内容检查）
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
            # 检查当前 Speech 与上一个 VISUAL 的 Bullet Sync
            text = block.content or ""
            item_count = _count_structural_items(text)
            
            if item_count >= 3:
                # 有 ≥3 个并列要点，检查 VISUAL 是否有 List
                v_meta = last_visual.metadata or {}
                v_raw = last_visual.content if last_visual.content else ""
                has_list = "**List**" in v_raw or bool(v_meta.get("list"))
                
                if not has_list:
                    results["bullet_sync_issues"].append({
                        "slide_id": v_meta.get("slide_id", "?"),
                        "visual_line": last_visual.line_start,
                        "speech_line": block.line_start,
                        "item_count": item_count,
                        "speech_preview": text[:80],
                    })
            
            # 重置（只检查紧邻的 SPEECH）
            last_visual = None
            last_visual_idx = -1
    
    return results


def print_report(all_results: list[dict], course: str, week: int = None):
    """输出格式化的报告。"""
    print(f"\n{'='*60}")
    print(f"  视觉-文字对齐检查报告 (Visual-Text Sync)")
    print(f"{'='*60}")
    print(f"  课程: {course}")
    if week is not None:
        print(f"  范围: 第 {week} 周")
    print(f"{'='*60}")
    
    total_visuals = sum(r["total_visuals"] for r in all_results)
    total_with_text = sum(r["visuals_with_text"] for r in all_results)
    total_with_list = sum(r["visuals_with_list"] for r in all_results)
    total_heading_empty = sum(len(r["heading_empty"]) for r in all_results)
    total_bullet_issues = sum(len(r["bullet_sync_issues"]) for r in all_results)
    total_text_suggestions = sum(len(r["text_suggestions"]) for r in all_results)
    
    text_coverage = (total_with_text / total_visuals * 100) if total_visuals > 0 else 0
    
    print(f"\n📊 总览:")
    print(f"   VISUAL 块总数: {total_visuals}")
    print(f"   含 Text 字段: {total_with_text} ({text_coverage:.0f}%)")
    print(f"   含 List 字段: {total_with_list}")
    print(f"   Heading 空洞: {total_heading_empty}")
    print(f"   Bullet Sync 问题: {total_bullet_issues}")
    
    has_issues = False
    
    # Bullet Sync 问题
    for r in all_results:
        if r["bullet_sync_issues"]:
            has_issues = True
            print(f"\n❌ Bullet Sync 不匹配 — {r['file']}:")
            for issue in r["bullet_sync_issues"]:
                print(f"   Slide {issue['slide_id']} (L{issue['visual_line']})")
                print(f"   Speech (L{issue['speech_line']}) 包含 {issue['item_count']} 个并列要点")
                print(f"   → 但 VISUAL 块无 **List** 字段")
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
        print(f"\n✅ 视觉-文字对齐检查通过！")
    
    print(f"\n{'='*60}")
    
    # 返回退出码：Bullet Sync 问题为硬性错误
    return 1 if total_bullet_issues > 0 else 0


def main():
    parser = argparse.ArgumentParser(description="视觉-文字对齐检查")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--week", type=int, default=None, help="仅检查指定周次")
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
        result = analyze_script(fpath)
        all_results.append(result)
    
    exit_code = print_report(all_results, args.course, args.week)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
