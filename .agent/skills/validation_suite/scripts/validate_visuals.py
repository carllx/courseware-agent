#!/usr/bin/env python3
"""
视觉素材完整性检查 (Visual Asset Validator)

检查脚本中引用的 Slide ID 是否在 visuals/assets/ 中有对应的物理文件。

用法:
    python validate_visuals.py --course "实习指导"
"""

import os
import sys
import argparse
from pathlib import Path

# 确保能 import 同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_parser import (
    parse_script, BlockType, get_workspace_root,
    get_scripts_dir, get_visuals_dir, get_weeks_asset_dirs,
    list_script_files, list_script_files_for_week,
)


def collect_visual_refs(scripts_dir: str, script_files: list[str]) -> list[dict]:
    """
    从所有脚本中收集 VISUAL 块引用。
    支持多资产模型：每个 Asset/Resource 路径独立生成一条记录。
    返回: [{"slide_id": ..., "layout": ..., "asset": ..., "file": ..., "line": ...}, ...]
    """
    refs = []
    for fname in script_files:
        fpath = os.path.join(scripts_dir, fname)
        blocks = parse_script(fpath)
        for b in blocks:
            if b.block_type == BlockType.VISUAL:
                # 优先使用多资产数组，回退到单 asset
                asset_list = b.metadata.get("assets", [])
                if not asset_list and b.metadata.get("asset"):
                    asset_list = [b.metadata["asset"]]

                if asset_list:
                    for idx, asset_path in enumerate(asset_list):
                        refs.append({
                            "slide_id": b.metadata.get("slide_id", ""),
                            "layout": b.metadata.get("layout", ""),
                            "asset": asset_path,
                            "asset_index": idx,
                            "scene": b.metadata.get("scene", ""),
                            "file": fname,
                            "line": b.line_start,
                        })
                else:
                    # 无资产引用的 VISUAL 块也记录（用于缺失检测）
                    refs.append({
                        "slide_id": b.metadata.get("slide_id", ""),
                        "layout": b.metadata.get("layout", ""),
                        "asset": "",
                        "scene": b.metadata.get("scene", ""),
                        "file": fname,
                        "line": b.line_start,
                    })
            elif b.block_type == BlockType.SLIDE_REF:
                # 旧格式也收集
                refs.append({
                    "slide_id": b.metadata.get("slide_ref_id", ""),
                    "layout": "",
                    "asset": "",
                    "scene": b.content,
                    "file": fname,
                    "line": b.line_start,
                    "legacy": True,
                })
    return refs


def collect_physical_assets(visuals_dir: str, weeks_dirs: list[str] = None) -> list[str]:
    """递归收集所有物理文件名。
    
    同时扫描：
    - visuals/assets/ (旧架构)
    - weeks/*/assets/ (新架构)
    """
    assets = []
    # 旧架构：visuals/assets/
    if os.path.exists(visuals_dir):
        for root, dirs, files in os.walk(visuals_dir):
            for f in files:
                if f.startswith('.'):
                    continue
                rel = os.path.relpath(os.path.join(root, f), visuals_dir)
                assets.append(rel)
    # 新架构：weeks/*/assets/
    if weeks_dirs:
        for week_asset_dir in weeks_dirs:
            if not os.path.exists(week_asset_dir):
                continue
            for root, dirs, files in os.walk(week_asset_dir):
                for f in files:
                    if f.startswith('.'):
                        continue
                    rel = os.path.relpath(os.path.join(root, f), week_asset_dir)
                    assets.append(rel)
    return assets


from typing import Optional

def match_slide_id(slide_id: str, physical_files: list[str]) -> Optional[str]:
    """
    检查物理文件中是否有匹配 Slide ID 前缀的文件。
    返回匹配的文件名，或 None。
    """
    if not slide_id:
        return None
    lower_id = slide_id.lower()
    for f in physical_files:
        fname = os.path.basename(f).lower()
        if fname.startswith(lower_id + ".") or fname.startswith(lower_id + "_"):
            return f
    return None


def main():
    parser = argparse.ArgumentParser(description="视觉素材完整性检查")
    parser.add_argument("--course", required=True, help="课程目录名（如 '实习指导'）")
    parser.add_argument("--week", type=int, default=None,
                        help="仅检查指定周次的素材（如 --week 1）")
    args = parser.parse_args()

    workspace = get_workspace_root()
    scripts_dir = get_scripts_dir(workspace, args.course)
    visuals_dir = get_visuals_dir(workspace, args.course)
    weeks_dirs = get_weeks_asset_dirs(workspace, args.course)

    # --week N 过滤：仅保留目标周次的素材目录
    if args.week is not None:
        week_prefix = f"W{args.week:02d}_"
        weeks_dirs = [d for d in weeks_dirs if week_prefix in d]

    if not os.path.exists(scripts_dir):
        print(f"❌ 脚本目录不存在: {scripts_dir}")
        sys.exit(1)

    # 1. 收集脚本中的 VISUAL 引用
    if args.week is not None:
        script_files = list_script_files_for_week(scripts_dir, args.week)
    else:
        script_files = list_script_files(scripts_dir)
    refs = collect_visual_refs(scripts_dir, script_files)

    # 2. 收集物理文件（同时扫描旧架构 visuals/assets/ 和新架构 weeks/*/assets/）
    physical = collect_physical_assets(visuals_dir, weeks_dirs)

    # 3. 交叉比对
    matched = []
    missing = []
    referenced_files = set()

    for ref in refs:
        sid = ref["slide_id"]
        asset_path = ref.get("asset", "")

        # 优先检查显式 Asset 路径
        if asset_path:
            # 方式1: 直接在 visuals_dir 下查找
            full_path = os.path.join(visuals_dir, asset_path)
            if os.path.exists(full_path):
                matched.append({**ref, "matched_file": asset_path})
                referenced_files.add(asset_path)
                continue
            
            # 方式2: 在 weeks/*/public/ 或 weeks/*/assets/ 下查找
            found_in_weeks = False
            if weeks_dirs:
                for wdir in weeks_dirs:
                    candidate = os.path.join(wdir, asset_path)
                    if os.path.exists(candidate):
                        matched.append({**ref, "matched_file": asset_path})
                        referenced_files.add(asset_path)
                        found_in_weeks = True
                        break
                    # Asset 可能以 public/ 或 assets/ 开头，尝试去前缀匹配
                    for prefix in ["public/", "assets/"]:
                        if asset_path.startswith(prefix):
                            stripped = asset_path[len(prefix):]
                            candidate = os.path.join(wdir, stripped)
                            if os.path.exists(candidate):
                                matched.append({**ref, "matched_file": asset_path})
                                referenced_files.add(stripped)
                                found_in_weeks = True
                                break
                    if found_in_weeks:
                        break
            if found_in_weeks:
                continue

        # 回退到 Slide ID 前缀匹配
        match = match_slide_id(sid, physical)
        if match:
            matched.append({**ref, "matched_file": match})
            referenced_files.add(match)
        else:
            missing.append(ref)

    # 4. 检查孤立素材
    orphaned = [f for f in physical if f not in referenced_files]

    # 5. 输出报告
    print(f"\n{'='*50}")
    print(f"  视觉素材完整性报告")
    print(f"{'='*50}")
    print(f"  课程: {args.course}")
    if args.week is not None:
        print(f"  范围: 第 {args.week} 周")
    print(f"  脚本数: {len(script_files)} | VISUAL 引用: {len(refs)} | 物理文件: {len(physical)}")
    print(f"{'='*50}")

    if not os.path.exists(visuals_dir) and not weeks_dirs:
        print(f"\n⚠️  素材目录不存在: visuals/assets/ 和 weeks/*/assets/ 均未找到")
        print(f"   请创建对应目录并放入视觉素材。")

    if missing:
        print(f"\n❌ 缺失素材 ({len(missing)}):")
        for m in missing:
            layout_info = f" (Layout: {m['layout']})" if m['layout'] else ""
            legacy_tag = " [旧格式]" if m.get("legacy") else ""
            print(f"  {m['slide_id']}{layout_info} — 无匹配文件{legacy_tag}")
            print(f"    ↳ {m['file']}:L{m['line']}")

    if orphaned:
        print(f"\n⚠️  孤立素材 ({len(orphaned)}):")
        for o in orphaned:
            print(f"  {o} — 未被任何脚本引用")

    if matched:
        print(f"\n✅ 已匹配 ({len(matched)}):")
        for m in matched:
            print(f"  {m['slide_id']} → {m['matched_file']}")

    if not missing and not orphaned:
        print(f"\n✅ 视觉素材完整性检查通过！")
    elif missing:
        print(f"\n💡 建议: 为缺失素材执行采集任务，或在脚本中标注 Asset 路径。")

    # 退出码
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
