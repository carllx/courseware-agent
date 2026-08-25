#!/usr/bin/env python3
"""
cleanup_stale_assets.py — H5 课件废弃资产扫描与清理工具（重构版）
"""

import os
import sys
import json
import shutil
import argparse
import datetime
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path(__file__).parent.resolve()
sys.path.insert(0, str(WORKSPACE / '.agent' / 'scripts' / 'core'))
from script_parser import parse_script, normalize_asset_path

VISUAL_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif'}
VIDEO_EXTS = {'.mp4', '.webm', '.mov', '.avi'}
MEDIA_EXTS = VISUAL_EXTS | VIDEO_EXTS
TTS_EXTS = {'.aac', '.mp3'}


def parse_args():
    parser = argparse.ArgumentParser(description='H5 课件废弃资产扫描与清理工具')
    parser.add_argument('--delete', action='store_true',
                        help='实际删除废弃文件（移入各个课程的 _trash/ 目录）')
    parser.add_argument('--course', type=str, default=None,
                        help='只扫描指定课程（如：交互产品开发）')
    parser.add_argument('--week', type=str, default=None,
                        help='只扫描指定周次（如：W01）')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='输出详细信息')
    return parser.parse_args()


def find_courses(workspace_dir: Path):
    courses = []
    for d in workspace_dir.iterdir():
        if d.is_dir() and (d / 'weeks').exists():
            courses.append(d)
    return sorted(courses)

def find_weeks(course_dir: Path, week_filter: str = None) -> list:
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

def collect_refs_from_week(week_dir: Path):
    refs = set()
    errors = []
    src_dir = week_dir / 'src'
    if not src_dir.exists():
        return refs, errors
    for md_file in src_dir.glob('*.md'):
        try:
            blocks = parse_script(str(md_file))
            for b in blocks:
                if getattr(b.block_type, 'value', b.block_type) == 'visual':
                    asset = b.metadata.get('asset', '')
                    if asset:
                        norm = normalize_asset_path(asset)
                        if norm:
                            # 剥离 public/ 或 assets/ 前缀，与 scan_visuals 的 key 格式对齐
                            for prefix in ('public/', 'assets/'):
                                if norm.startswith(prefix):
                                    norm = norm[len(prefix):]
                                    break
                            refs.add(norm)
                    assets = b.metadata.get('assets', [])
                    for a in assets:
                        norm = normalize_asset_path(a)
                        if norm:
                            for prefix in ('public/', 'assets/'):
                                if norm.startswith(prefix):
                                    norm = norm[len(prefix):]
                                    break
                            refs.add(norm)
        except Exception as e:
            err_msg = f"解析异常: {md_file.name} - {e}"
            print(f"      ⚠️ {err_msg}")
            errors.append(err_msg)
    return refs, errors

def scan_visuals(week_dir: Path, refs: set):
    stale = []
    public_dir = week_dir / 'public'
    for subdir_name in ['slides', 'videos']:
        subdir = public_dir / subdir_name
        if not subdir.exists():
            continue
        for root, dirs, files in os.walk(subdir):
            root_path = Path(root)
            if 'textbook' in root_path.parts:
                continue
            for f in files:
                fpath = root_path / f
                if fpath.suffix.lower() in MEDIA_EXTS:
                    rel_path = fpath.relative_to(public_dir)
                    rel_key = str(rel_path).replace('\\', '/')
                    if rel_key not in refs:
                        stale.append({
                            'path': fpath,
                            'rel_key': rel_key,
                            'size': fpath.stat().st_size,
                        })
    return stale

def scan_build(week_dir: Path, refs: set):
    stale = []
    build_dir = week_dir / '.build'
    
    posters_dir = build_dir / '_video_posters'
    if posters_dir.exists():
        for f in posters_dir.glob('*_poster.png'):
            name = f.name.replace('_poster.png', '')
            original_video = f"videos/{name}.mp4"
            if original_video not in refs:
                stale.append({
                    'path': f,
                    'size': f.stat().st_size,
                    'reason': f'源视频 {original_video} 未被引用'
                })
                
    pptx_dir = build_dir / '_video_pptx'
    if pptx_dir.exists():
        for f in pptx_dir.glob('*.mp4'):
            name = f.stem
            original_video = f"videos/{name}.mp4"
            if original_video not in refs:
                stale.append({
                    'path': f,
                    'size': f.stat().st_size,
                    'reason': f'源视频 {original_video} 未被引用'
                })
    return stale

def extract_tts_fingerprints_from_manifest(manifest_path: Path) -> set:
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
    files = {}
    if not tts_dir.exists():
        return files
    for f in tts_dir.iterdir():
        if f.suffix.lower() in TTS_EXTS and f.name != 'manifest.json':
            files[f.stem] = f
    return files

def find_duplicate_tts(tts_files: dict) -> list:
    prefix_groups = defaultdict(list)
    for stem, fpath in tts_files.items():
        prefix = stem.split('_')[0] if '_' in stem else stem
        if len(prefix) == 8 and all(c in '0123456789abcdef' for c in prefix):
            prefix_groups[prefix].append((stem, fpath))
    
    duplicates = []
    for prefix, entries in prefix_groups.items():
        if len(entries) <= 1:
            continue
        
        has_suffix = [(s, f) for s, f in entries if '_' in s]
        no_suffix = [(s, f) for s, f in entries if '_' not in s]
        
        if has_suffix and no_suffix:
            for old_stem, old_path in no_suffix:
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

def scan_tts(week_dir: Path):
    tts_dir = week_dir / 'tts'
    stale_tts = []
    dup_tts = []
    if not tts_dir.exists():
        return stale_tts, dup_tts
    
    manifest_path = tts_dir / "manifest.json"
    manifest_fps = extract_tts_fingerprints_from_manifest(manifest_path)
    tts_files = scan_tts_files(tts_dir)
    
    for stem, file_path in sorted(tts_files.items()):
        if stem not in manifest_fps:
            stale_tts.append({
                'path': file_path,
                'stem': stem,
                'size': file_path.stat().st_size,
            })
            
    dup_tts = find_duplicate_tts(tts_files)
    return stale_tts, dup_tts

def scan_course_level(course_dir: Path):
    stale = []
    for d_name in ['public', 'assets']:
        d_path = course_dir / d_name
        if not d_path.exists():
            continue
        for root, dirs, files in os.walk(d_path):
            for f in files:
                fpath = Path(root) / f
                if fpath.suffix.lower() in MEDIA_EXTS or fpath.suffix.lower() in ['.tmp', '.bak']:
                    stale.append({
                        'path': fpath,
                        'size': fpath.stat().st_size,
                        'reason': '课程级目录不应存在此媒体/临时垃圾文件'
                    })
    return stale

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.1f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.1f} GB"

def move_to_trash(file_path: Path, course_dir: Path):
    trash_dir = course_dir / '_trash'
    rel = file_path.relative_to(course_dir)
    dest = trash_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(dest))

def main():
    args = parse_args()
    is_delete = args.delete
    
    print("=" * 60)
    print("🔍 H5 课件废弃资产扫描工具 (重构版)")
    print(f"   模式: {'⚠️  删除模式（移入各个课程的 _trash/）' if is_delete else '🔎 干跑模式（仅报告）'}")
    
    all_courses = find_courses(WORKSPACE)
    if args.course:
        target_courses = [c for c in all_courses if c.name == args.course]
    else:
        target_courses = all_courses
        
    print(f"   范围: {', '.join([c.name for c in target_courses])}")
    if args.week:
        print(f"   周次过滤: {args.week}")
    print("=" * 60)
    
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'summary': {},
        'errors': [],
        'details': {
            'course_level': {}
        }
    }
    
    global_parse_errors = []
    
    total_stale_media_count = 0
    total_stale_media_size = 0
    total_stale_tts_count = 0
    total_stale_tts_size = 0
    total_dup_tts_count = 0
    total_dup_tts_size = 0
    
    global_items_to_delete = [] # list of (item_path, course_dir)
    
    for course_dir in target_courses:
        course_name = course_dir.name
        print(f"\n{'─' * 50}")
        print(f"📚 课程: {course_name}")
        print(f"{'─' * 50}")
        
        report['details'].setdefault(course_name, {})
        
        # 扫描课程级违规资产
        course_level_stale = scan_course_level(course_dir)
        if course_level_stale:
            print(f"   ⚠️  发现课程级违规资产: {len(course_level_stale)} 个文件")
            report['details']['course_level'][course_name] = [
                {'path': str(s['path']), 'size': s['size'], 'reason': s['reason']} 
                for s in course_level_stale
            ]
            for s in course_level_stale:
                global_items_to_delete.append((s['path'], course_dir))
                total_stale_media_count += 1
                total_stale_media_size += s['size']
                if args.verbose:
                    print(f"      ❌ {s['path'].relative_to(course_dir)} ({format_size(s['size'])})")
        else:
            report['details']['course_level'][course_name] = []
        
        weeks = find_weeks(course_dir, args.week)
        if not weeks:
            print("   (未找到周次目录)")
            continue
            
        for week_dir in weeks:
            week_name = week_dir.name
            print(f"\n   📅 {week_name}")
            
            # 解析脚本收集引用
            refs, week_errors = collect_refs_from_week(week_dir)
            if week_errors:
                global_parse_errors.extend(week_errors)
            if args.verbose and refs:
                print(f"      📝 共提取 {len(refs)} 个资产引用")
                
            week_details = {}
            
            # 扫描 visuals
            stale_visuals = scan_visuals(week_dir, refs)
            week_details['stale_visuals'] = [
                {'path': str(s['path']), 'rel_key': s['rel_key'], 'size': s['size']} 
                for s in stale_visuals
            ]
            if stale_visuals:
                v_size = sum(s['size'] for s in stale_visuals)
                print(f"      🖼️  废弃视觉素材: {len(stale_visuals)} 个 ({format_size(v_size)})")
                for s in stale_visuals:
                    global_items_to_delete.append((s['path'], course_dir))
                    total_stale_media_count += 1
                    total_stale_media_size += s['size']
                    if args.verbose:
                        print(f"         ❌ {s['rel_key']} ({format_size(s['size'])})")
            
            # 扫描 build
            stale_build = scan_build(week_dir, refs)
            week_details['stale_build'] = [
                {'path': str(s['path']), 'size': s['size'], 'reason': s['reason']} 
                for s in stale_build
            ]
            if stale_build:
                b_size = sum(s['size'] for s in stale_build)
                print(f"      🛠️  废弃构建产物: {len(stale_build)} 个 ({format_size(b_size)})")
                for s in stale_build:
                    global_items_to_delete.append((s['path'], course_dir))
                    total_stale_media_count += 1
                    total_stale_media_size += s['size']
                    if args.verbose:
                        print(f"         ❌ {s['path'].name} ({format_size(s['size'])})")
                        
            # 扫描 TTS
            stale_tts, dup_tts = scan_tts(week_dir)
            week_details['stale_tts'] = [
                {'path': str(s['path']), 'stem': s['stem'], 'size': s['size']} 
                for s in stale_tts
            ]
            if stale_tts:
                t_size = sum(s['size'] for s in stale_tts)
                print(f"      🔊 废弃 TTS 音频: {len(stale_tts)} 个 ({format_size(t_size)})")
                for s in stale_tts:
                    global_items_to_delete.append((s['path'], course_dir))
                    total_stale_tts_count += 1
                    total_stale_tts_size += s['size']
                    if args.verbose:
                        print(f"         ❌ {s['stem']}.aac ({format_size(s['size'])})")
                        
            week_details['duplicate_tts'] = [
                {'old': str(d['old']), 'new': str(d['new']), 'old_stem': d['old_stem'], 'new_stem': d['new_stem'], 'size': d['size']} 
                for d in dup_tts
            ]
            if dup_tts:
                dt_size = sum(d['size'] for d in dup_tts)
                print(f"      🔄 重复 TTS 文件: {len(dup_tts)} 对 ({format_size(dt_size)})")
                for d in dup_tts:
                    global_items_to_delete.append((d['old'], course_dir))
                    total_dup_tts_count += 1
                    total_dup_tts_size += d['size']
                    if args.verbose:
                        print(f"         📋 {d['old_stem']}.aac ↔ {d['new_stem']}.aac ({format_size(d['size'])})")

            report['details'][course_name][week_name] = week_details
            
    print(f"\n{'═' * 60}")
    print("📊 汇总报告")
    print(f"{'═' * 60}")
    
    total_reclaimable = total_stale_media_size + total_stale_tts_size + total_dup_tts_size
    
    print(f"   🖼️  废弃素材与产物: {total_stale_media_count} 个文件, {format_size(total_stale_media_size)}")
    print(f"   🔊 废弃 TTS 音频: {total_stale_tts_count} 个文件, {format_size(total_stale_tts_size)}")
    print(f"   🔄 重复 TTS 文件: {total_dup_tts_count} 个文件, {format_size(total_dup_tts_size)}")
    print(f"   {'─' * 40}")
    print(f"   💾 可回收总空间: {format_size(total_reclaimable)}")
    
    report['summary'] = {
        'stale_media_count': total_stale_media_count,
        'stale_media_bytes': total_stale_media_size,
        'stale_tts_count': total_stale_tts_count,
        'stale_tts_bytes': total_stale_tts_size,
        'duplicate_tts_count': total_dup_tts_count,
        'duplicate_tts_bytes': total_dup_tts_size,
        'total_reclaimable_bytes': total_reclaimable,
    }
    report['errors'] = global_parse_errors
    
    if global_parse_errors:
        print("\n" + "!" * 60)
        print("🚨 发现脚本解析异常 (高危)！")
        print("!" * 60)
        print("由于部分文件解析失败，其包含的资源未被识别，这会导致严重误判！")
        for err in global_parse_errors:
            print(f"  - {err}")
            
        if is_delete:
            print("\n⛔ 致命错误：为防止正在使用的课件被误删，--delete 模式已强制中止！请先修复这些文件。")
            report_path = WORKSPACE / "cleanup_report.json"
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            sys.exit(2)
        else:
            print("\n⚠️ 警告：当前为干跑模式，但由于存在解析异常，上述回收报告可能包含误报。")

    if total_reclaimable == 0:
        print("\n🎉 所有资产均在使用中，无需清理！")
    else:
        if is_delete:
            print(f"\n⚠️  正在将 {len(global_items_to_delete)} 个文件移入各自课程的 _trash/ ...")
            moved = 0
            for item_path, course_dir in global_items_to_delete:
                try:
                    move_to_trash(item_path, course_dir)
                    moved += 1
                except Exception as e:
                    print(f"   ❌ 移动失败: {item_path}: {e}")
            print(f"\n✅ 已移动 {moved} 个文件至 _trash/")
        else:
            print(f"\n💡 这是干跑模式。要实际清理，请运行:")
            print(f"   python cleanup_stale_assets.py --delete")
    
    report_path = WORKSPACE / "cleanup_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n📋 详细报告已写入: {report_path.name}")

if __name__ == '__main__':
    main()
