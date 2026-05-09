#!/usr/bin/env python3
"""
cleanup_stale_assets.py — H5 课件废弃资产扫描与清理工具

功能：
  1. 扫描所有课程脚本（src/*.md）中的 [VISUAL] 块，提取被引用的图片/视频路径
  2. 扫描所有课程脚本中的 TTS 指纹（通过 manifest.json 记录的段落文本哈希提取实际被引用的指纹）
  3. 对比 public/slides/、public/videos/、tts/ 目录下的实际文件
  4. 识别：
     a) 废弃的视觉素材：存在于 public/ 中但未被任何脚本引用的图片/视频
     b) 废弃的 TTS 音频：存在于 tts/ 中但与当前脚本内容不匹配的 .aac 文件
     c) 重复的 TTS 文件：同一指纹同时有带后缀和不带后缀版本
  5. 报告可回收空间，支持 --dry-run（默认）和 --delete 模式

用法：
  python cleanup_stale_assets.py                    # 干跑模式，只报告
  python cleanup_stale_assets.py --delete            # 实际删除（移入 _trash/）
  python cleanup_stale_assets.py --course 交互产品开发  # 只扫描指定课程
  python cleanup_stale_assets.py --week W01          # 只扫描指定周次

数据流分析：
  脚本 src/*.md 中的 [VISUAL] 块引用 → ../public/slides/XXX.png 或 ../public/videos/XXX.mp4
  H5 构建系统从脚本解析 → JSON → 引用 ttsFp（段落文本的 8 字符哈希 + 字符数后缀）
  TTS manifest.json 记录所有已合成的指纹 → 对应 tts/*.aac 文件

作者：课程 Agent 自动生成
"""

import os
import re
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict

# ============ 配置 ============
WORKSPACE = Path(__file__).parent
COURSES = ["交互产品开发", "信息可视化"]
VISUAL_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif'}
VIDEO_EXTS = {'.mp4', '.webm', '.mov', '.avi'}
MEDIA_EXTS = VISUAL_EXTS | VIDEO_EXTS
TTS_EXTS = {'.aac', '.mp3'}


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='H5 课件废弃资产扫描与清理工具')
    parser.add_argument('--delete', action='store_true',
                        help='实际删除废弃文件（移入 _trash/ 目录）')
    parser.add_argument('--course', type=str, default=None,
                        help='只扫描指定课程（如：交互产品开发）')
    parser.add_argument('--week', type=str, default=None,
                        help='只扫描指定周次（如：W01）')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='输出详细信息')
    return parser.parse_args()


def find_weeks(course_dir: Path, week_filter: str = None) -> list:
    """查找课程下的所有周次目录"""
    weeks_dir = course_dir / "weeks"
    if not weeks_dir.exists():
        return []
    weeks = []
    for d in sorted(weeks_dir.iterdir()):
        if d.is_dir() and d.name.startswith('W'):
            if week_filter and not d.name.startswith(week_filter):
                continue
            weeks.append(d)
    return weeks


def extract_visual_refs(script_path: Path) -> set:
    """
    从 Markdown 脚本中提取所有 [VISUAL] 块引用的资产路径。
    
    匹配模式：
      - ![描述](../public/slides/XXX.png)
      - ![描述](../public/videos/XXX.mp4)
    
    返回相对于 week 目录的标准化文件名集合（如 slides/W01_S00.png）
    """
    refs = set()
    try:
        content = script_path.read_text(encoding='utf-8')
    except Exception:
        return refs

    # 匹配 Markdown 图片/视频引用：![alt](path)
    pattern = r'!\[.*?\]\(\.\./public/((?:slides|videos)/[^)]+)\)'
    for match in re.finditer(pattern, content):
        ref_path = match.group(1)
        refs.add(ref_path)

    return refs


def extract_tts_fingerprints_from_manifest(manifest_path: Path) -> set:
    """
    从 TTS manifest.json 中提取所有有效的指纹。
    
    manifest 格式：
    {
      "segments": {
        "820e7f61_88": { "durationMs": ..., "size": ..., "cachedAt": ... },
        ...
      }
    }
    
    注意：有些指纹有两个版本（如 077c32c1 和 077c32c1_65），
    这通常是旧版→新版的过渡产物。我们收集所有被 manifest 记录的指纹。
    """
    fps = set()
    if not manifest_path.exists():
        return fps
    try:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
        segments = data.get('segments', {})
        fps = set(segments.keys())
    except Exception:
        pass
    return fps


def scan_tts_files(tts_dir: Path) -> dict:
    """
    扫描 tts/ 目录下所有 .aac 文件。
    
    返回 {指纹名(不含扩展名): 文件路径}
    """
    files = {}
    if not tts_dir.exists():
        return files
    for f in tts_dir.iterdir():
        if f.suffix.lower() in TTS_EXTS and f.name != 'manifest.json':
            stem = f.stem  # 如 "820e7f61_88" 或 "077c32c1"
            files[stem] = f
    return files


def scan_media_files(public_dir: Path) -> dict:
    """
    扫描 public/slides/ 和 public/videos/ 下的所有媒体文件。
    
    返回 {相对路径（如 slides/W01_S00.png）: 文件路径}
    """
    files = {}
    for subdir_name in ['slides', 'videos']:
        subdir = public_dir / subdir_name
        if not subdir.exists():
            continue
        for f in subdir.iterdir():
            if f.is_file() and f.suffix.lower() in MEDIA_EXTS:
                rel_key = f"{subdir_name}/{f.name}"
                files[rel_key] = f
    return files


def find_duplicate_tts(tts_files: dict) -> list:
    """
    识别重复的 TTS 文件。
    
    规律：同一个 8 字符哈希前缀可能有两个文件：
      - 077c32c1.aac         (旧版，无字符数后缀)
      - 077c32c1_65.aac      (新版，带字符数后缀)
    如果两者大小完全一致，旧版即为冗余。
    """
    # 按 8 字符前缀分组
    prefix_groups = defaultdict(list)
    for stem, fpath in tts_files.items():
        # 提取 8 字符哈希前缀
        prefix = stem.split('_')[0] if '_' in stem else stem
        if len(prefix) == 8 and all(c in '0123456789abcdef' for c in prefix):
            prefix_groups[prefix].append((stem, fpath))
    
    duplicates = []
    for prefix, entries in prefix_groups.items():
        if len(entries) <= 1:
            continue
        
        # 按是否有后缀排序：无后缀的是旧版
        has_suffix = [(s, f) for s, f in entries if '_' in s]
        no_suffix = [(s, f) for s, f in entries if '_' not in s]
        
        if has_suffix and no_suffix:
            for old_stem, old_path in no_suffix:
                # 检查是否与某个带后缀版本大小一致
                old_size = old_path.stat().st_size
                for new_stem, new_path in has_suffix:
                    new_size = new_path.stat().st_size
                    if old_size == new_size:
                        duplicates.append({
                            'old': old_path,
                            'new': new_path,
                            'old_stem': old_stem,
                            'new_stem': new_stem,
                            'size': old_size,
                        })
                        break
    
    return duplicates


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.1f} GB"


def move_to_trash(file_path: Path, trash_dir: Path):
    """将文件移入 _trash/ 目录（保留相对路径结构）"""
    rel = file_path.relative_to(WORKSPACE)
    dest = trash_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(dest))


def main():
    args = parse_args()
    is_delete = args.delete
    
    # 确定扫描范围
    courses = [args.course] if args.course else COURSES
    
    print("=" * 60)
    print("🔍 H5 课件废弃资产扫描工具")
    print(f"   模式: {'⚠️  删除模式（移入 _trash/）' if is_delete else '🔎 干跑模式（仅报告）'}")
    print(f"   范围: {', '.join(courses)}")
    if args.week:
        print(f"   周次过滤: {args.week}")
    print("=" * 60)
    
    # 全局统计
    total_stale_media = []
    total_stale_tts = []
    total_dup_tts = []
    
    for course_name in courses:
        course_dir = WORKSPACE / course_name
        if not course_dir.exists():
            print(f"\n⚠️  课程目录不存在: {course_name}")
            continue
        
        print(f"\n{'─' * 50}")
        print(f"📚 课程: {course_name}")
        print(f"{'─' * 50}")
        
        weeks = find_weeks(course_dir, args.week)
        if not weeks:
            print("   (未找到周次目录)")
            continue
        
        for week_dir in weeks:
            week_name = week_dir.name
            src_dir = week_dir / "src"
            public_dir = week_dir / "public"
            tts_dir = week_dir / "tts"
            
            # 跳过没有任何资产的周次
            has_media = public_dir.exists() and any(
                (public_dir / sd).exists() for sd in ['slides', 'videos']
            )
            has_tts = tts_dir.exists() and any(
                f.suffix.lower() in TTS_EXTS for f in tts_dir.iterdir()
            ) if tts_dir.exists() else False
            
            if not has_media and not has_tts:
                continue
            
            print(f"\n   📅 {week_name}")
            
            # ──── 视觉素材扫描 ────
            if has_media:
                # 收集所有脚本引用
                all_refs = set()
                if src_dir.exists():
                    for md_file in sorted(src_dir.glob("*.md")):
                        refs = extract_visual_refs(md_file)
                        all_refs.update(refs)
                        if args.verbose and refs:
                            print(f"      📝 {md_file.name}: {len(refs)} 个资产引用")
                
                # 扫描实际文件
                actual_files = scan_media_files(public_dir)
                
                # 比较
                stale_media = []
                for rel_key, file_path in sorted(actual_files.items()):
                    if rel_key not in all_refs:
                        stale_media.append({
                            'path': file_path,
                            'rel_key': rel_key,
                            'size': file_path.stat().st_size,
                        })
                
                referenced_count = len(all_refs & set(actual_files.keys()))
                total_count = len(actual_files)
                stale_count = len(stale_media)
                stale_size = sum(s['size'] for s in stale_media)
                
                if stale_media:
                    print(f"      🖼️  视觉素材: {total_count} 个文件, "
                          f"{referenced_count} 个被引用, "
                          f"⚠️  {stale_count} 个废弃 ({format_size(stale_size)})")
                    if args.verbose:
                        for item in stale_media[:10]:
                            print(f"         ❌ {item['rel_key']} ({format_size(item['size'])})")
                        if len(stale_media) > 10:
                            print(f"         ... 还有 {len(stale_media) - 10} 个")
                    total_stale_media.extend(stale_media)
                else:
                    print(f"      🖼️  视觉素材: {total_count} 个文件, 全部被引用 ✅")
            
            # ──── TTS 音频扫描 ────
            if has_tts:
                manifest_path = tts_dir / "manifest.json"
                manifest_fps = extract_tts_fingerprints_from_manifest(manifest_path)
                tts_files = scan_tts_files(tts_dir)
                
                # 识别废弃 TTS（不在 manifest 中的文件）
                stale_tts = []
                for stem, file_path in sorted(tts_files.items()):
                    if stem not in manifest_fps:
                        stale_tts.append({
                            'path': file_path,
                            'stem': stem,
                            'size': file_path.stat().st_size,
                        })
                
                # 识别重复 TTS
                dup_tts = find_duplicate_tts(tts_files)
                
                in_manifest = len([s for s in tts_files if s in manifest_fps])
                total_tts = len(tts_files)
                stale_count = len(stale_tts)
                stale_size = sum(s['size'] for s in stale_tts)
                dup_count = len(dup_tts)
                dup_size = sum(d['size'] for d in dup_tts)
                
                if stale_tts:
                    print(f"      🔊 TTS 音频: {total_tts} 个文件, "
                          f"{in_manifest} 个在 manifest 中, "
                          f"⚠️  {stale_count} 个废弃 ({format_size(stale_size)})")
                    if args.verbose:
                        for item in stale_tts[:5]:
                            print(f"         ❌ {item['stem']}.aac ({format_size(item['size'])})")
                        if len(stale_tts) > 5:
                            print(f"         ... 还有 {len(stale_tts) - 5} 个")
                    total_stale_tts.extend(stale_tts)
                elif total_tts > 0:
                    print(f"      🔊 TTS 音频: {total_tts} 个文件, 全部有效 ✅")
                
                if dup_tts:
                    print(f"      🔄 TTS 重复: {dup_count} 对重复文件 ({format_size(dup_size)})")
                    if args.verbose:
                        for d in dup_tts[:3]:
                            print(f"         📋 {d['old_stem']}.aac ↔ {d['new_stem']}.aac "
                                  f"(各 {format_size(d['size'])})")
                    total_dup_tts.extend(dup_tts)
    
    # ============ 汇总报告 ============
    print(f"\n{'═' * 60}")
    print("📊 汇总报告")
    print(f"{'═' * 60}")
    
    total_stale_media_size = sum(s['size'] for s in total_stale_media)
    total_stale_tts_size = sum(s['size'] for s in total_stale_tts)
    total_dup_tts_size = sum(d['size'] for d in total_dup_tts)
    total_reclaimable = total_stale_media_size + total_stale_tts_size + total_dup_tts_size
    
    print(f"   🖼️  废弃视觉素材: {len(total_stale_media)} 个文件, "
          f"{format_size(total_stale_media_size)}")
    print(f"   🔊 废弃 TTS 音频: {len(total_stale_tts)} 个文件, "
          f"{format_size(total_stale_tts_size)}")
    print(f"   🔄 重复 TTS 文件: {len(total_dup_tts)} 个文件, "
          f"{format_size(total_dup_tts_size)}")
    print(f"   {'─' * 40}")
    print(f"   💾 可回收总空间: {format_size(total_reclaimable)}")
    
    if total_reclaimable == 0:
        print("\n🎉 所有资产均在使用中，无需清理！")
        return
    
    # ──── 执行删除 ────
    if is_delete:
        trash_dir = WORKSPACE / "_trash"
        trash_dir.mkdir(exist_ok=True)
        
        print(f"\n⚠️  正在将 {len(total_stale_media) + len(total_stale_tts) + len(total_dup_tts)} "
              f"个文件移入 _trash/ ...")
        
        moved = 0
        for item in total_stale_media:
            try:
                move_to_trash(item['path'], trash_dir)
                moved += 1
            except Exception as e:
                print(f"   ❌ 移动失败: {item['path']}: {e}")
        
        for item in total_stale_tts:
            try:
                move_to_trash(item['path'], trash_dir)
                moved += 1
            except Exception as e:
                print(f"   ❌ 移动失败: {item['path']}: {e}")
        
        for dup in total_dup_tts:
            try:
                move_to_trash(dup['old'], trash_dir)
                moved += 1
            except Exception as e:
                print(f"   ❌ 移动失败: {dup['old']}: {e}")
        
        print(f"\n✅ 已移动 {moved} 个文件至 {trash_dir}")
        print(f"   💡 确认无误后可手动删除 _trash/ 目录：rm -rf '{trash_dir}'")
    else:
        print(f"\n💡 这是干跑模式。要实际清理，请运行:")
        print(f"   python cleanup_stale_assets.py --delete")
        print(f"   （文件将移入 _trash/ 目录，不会直接删除）")
    
    # ──── 写入详细报告 ────
    report_path = WORKSPACE / "cleanup_report.json"
    report = {
        "summary": {
            "stale_media_count": len(total_stale_media),
            "stale_media_bytes": total_stale_media_size,
            "stale_tts_count": len(total_stale_tts),
            "stale_tts_bytes": total_stale_tts_size,
            "duplicate_tts_count": len(total_dup_tts),
            "duplicate_tts_bytes": total_dup_tts_size,
            "total_reclaimable_bytes": total_reclaimable,
        },
        "stale_media": [
            {"path": str(s['path']), "rel_key": s['rel_key'], "size": s['size']}
            for s in total_stale_media
        ],
        "stale_tts": [
            {"path": str(s['path']), "stem": s['stem'], "size": s['size']}
            for s in total_stale_tts
        ],
        "duplicate_tts": [
            {"old": str(d['old']), "new": str(d['new']),
             "old_stem": d['old_stem'], "new_stem": d['new_stem'], "size": d['size']}
            for d in total_dup_tts
        ],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n📋 详细报告已写入: {report_path.name}")


if __name__ == '__main__':
    main()
