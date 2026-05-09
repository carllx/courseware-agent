#!/usr/bin/env python3
"""
Markdown 素材批量注入引擎 (Asset Injection Engine)

消费 download_report.yaml 或 sourcing_checklist.yaml，
批量更新 Markdown 脚本中的 [VISUAL] 块。

用法:
    # 从下载报告注入（download_and_stitch.py 的产物）
    python inject_assets.py <download_report.yaml> --src-dir <src/> 

    # 从清单直接注入（需 disposition + real_path 字段）
    python inject_assets.py <sourcing_checklist.yaml> --src-dir <src/>

    # 预览模式（不实际修改文件）
    python inject_assets.py <report.yaml> --src-dir <src/> --dry-run

依赖: visual_block_io.py（同目录共享模块）
"""

import sys
import yaml
from pathlib import Path

# 导入共享的 VISUAL 块读写模块
sys.path.insert(0, str(Path(__file__).parent))
from visual_block_io import (
    scan_all_blocks,
    inject_dual_track_asset,
    inject_lock,
    batch_inject,
)


def load_injection_map_from_report(report_path: Path) -> dict:
    """
    从 download_report.yaml 构建注入映射。
    仅处理 status=success 的条目。
    """
    with open(report_path, 'r', encoding='utf-8') as f:
        items = yaml.safe_load(f) or []

    injection_map = {}
    for item in items:
        slide_id = item.get("slide", "")
        status = item.get("status", "")
        output_path = item.get("output_path", "")

        if status != "success" or not output_path:
            continue

        # 将绝对路径转换为相对路径（相对于 src/）
        # 实际路径由 batch_inject 在运行时解析
        abs_path = Path(output_path)
        # 推断相对路径：从 public/ 开始
        try:
            # 在路径中查找 "public" 段
            parts = abs_path.parts
            pub_idx = None
            for i, p in enumerate(parts):
                if p == "public":
                    pub_idx = i
                    break
            if pub_idx is not None:
                rel_path = "../" + "/".join(parts[pub_idx:])
            else:
                rel_path = f"../public/slides/{abs_path.name}"
        except Exception:
            rel_path = f"../public/slides/{abs_path.name}"

        # 根据文件扩展名判断来源类型
        ext = abs_path.suffix.lower()
        if ext == '.png' and '_real' in abs_path.stem:
            source_text = "AI Generated"
        else:
            source_text = "Web Source"

        injection_map[slide_id] = {
            "real_path": rel_path,
            "source": source_text,
            "disposition": "download",
        }

    return injection_map


def load_injection_map_from_checklist(checklist_path: Path) -> dict:
    """
    从 sourcing_checklist.yaml 构建注入映射。
    支持 disposition 字段路由（download/generate/lock/skip）。
    """
    with open(checklist_path, 'r', encoding='utf-8') as f:
        items = yaml.safe_load(f) or []

    injection_map = {}
    for item in items:
        slide_id = item.get("slide", "")
        if not slide_id:
            continue

        disposition = item.get("disposition", "")
        if not disposition:
            # 未填写 disposition 的条目跳过
            continue

        entry = {"disposition": disposition}

        if disposition == "download":
            target = item.get("target_path", "")
            entry["real_path"] = target
            entry["source"] = "Web Source"

        elif disposition == "generate":
            target = item.get("target_path", "")
            entry["real_path"] = target
            entry["source"] = "AI Generated"

        elif disposition == "lock":
            entry["lock_reason"] = item.get("lock_reason", "AI 素材足以满足教学需求")

        # disposition == "skip" 直接传递

        injection_map[slide_id] = entry

    return injection_map


def main():
    if len(sys.argv) < 2:
        print("用法: python inject_assets.py <report_or_checklist.yaml> --src-dir <src/>")
        print("  可选: --dry-run  预览模式")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)

    # 解析 --src-dir
    src_dir = None
    if "--src-dir" in sys.argv:
        idx = sys.argv.index("--src-dir")
        if idx + 1 < len(sys.argv):
            src_dir = Path(sys.argv[idx + 1])
    
    if not src_dir:
        # 尝试从输入文件的父目录推断
        src_dir = input_path.parent
    
    if not src_dir.is_dir():
        print(f"❌ 源目录不存在: {src_dir}")
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv

    # 判断输入类型并加载注入映射
    with open(input_path, 'r', encoding='utf-8') as f:
        first_item = yaml.safe_load(f)
    
    if not first_item:
        print("❌ 输入文件为空")
        sys.exit(1)

    # 重新加载（safe_load 已消费流）
    if isinstance(first_item, list) and first_item:
        sample = first_item[0]
        if "status" in sample and "output_path" in sample:
            # download_report.yaml 格式
            print(f"📄 检测到下载报告格式: {input_path.name}")
            injection_map = load_injection_map_from_report(input_path)
        else:
            # sourcing_checklist.yaml 格式
            print(f"📄 检测到采购清单格式: {input_path.name}")
            injection_map = load_injection_map_from_checklist(input_path)
    else:
        print("❌ 无法识别输入格式")
        sys.exit(1)

    print(f"📁 源目录: {src_dir}")
    print(f"📋 待处理条目: {len(injection_map)}")

    if dry_run:
        print("\n🔍 预览模式 (--dry-run)，不会修改文件:")
        for slide_id, spec in injection_map.items():
            disp = spec.get("disposition", "?")
            if disp == "download":
                print(f"  📥 {slide_id} → {spec.get('real_path', '?')}")
            elif disp == "generate":
                print(f"  🎨 {slide_id} → {spec.get('real_path', '?')}")
            elif disp == "lock":
                print(f"  🔒 {slide_id} → {spec.get('lock_reason', '?')}")
            elif disp == "skip":
                print(f"  ⏭️  {slide_id}")
        return

    # 执行批量注入
    stats = batch_inject(src_dir, injection_map)

    # 输出注入报告
    report_path = input_path.parent / "injection_report.yaml"
    with open(report_path, 'w', encoding='utf-8') as f:
        yaml.dump(stats, f, allow_unicode=True, default_flow_style=False)

    print(f"\n📄 注入报告: {report_path}")


if __name__ == "__main__":
    main()
