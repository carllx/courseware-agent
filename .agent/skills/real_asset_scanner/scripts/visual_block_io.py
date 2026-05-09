#!/usr/bin/env python3
"""
VISUAL 块结构化读写模块 (Visual Block I/O)

从 scan_real_assets.py 提炼的共享基础设施。
提供 VISUAL 块的解析（读）与精确行级更新（写）能力。

读 API:
  - parse_visual_blocks(filepath) → list[VisualBlock]

写 API:
  - update_visual_block(filepath, slide_id, updates) → bool
  - inject_dual_track_asset(filepath, slide_id, real_path, source_text) → bool

设计原则:
  - 基于行号精确定位，非 regex 全文替换
  - 幂等性：已存在 _real 路径的块自动跳过
  - 仅修改指定字段，不破坏其他 VISUAL 块结构
"""

import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class VisualBlock:
    """解析后的 [VISUAL] 块"""
    slide_id: str = ""
    layout: str = ""
    asset_path: str = ""          # 第一个 Asset 行的路径
    asset_alt: str = ""           # 第一个 Asset 行的 alt 文本
    asset_fallback_path: str = "" # AI fallback Asset 路径（如有）
    scene: str = ""
    text: str = ""
    list_items: str = ""
    source: str = ""
    source_file: str = ""
    line_start: int = 0           # 1-indexed，[VISUAL] 标记所在行
    line_end: int = 0             # 1-indexed，块结束后的下一行
    no_ai_flag: bool = False
    # 各字段所在行号（1-indexed），用于精确写入
    asset_line: int = 0
    source_line: int = 0


def parse_visual_blocks(filepath: Path) -> list[VisualBlock]:
    """
    从 Markdown 文件中解析所有 [VISUAL] 块。
    
    返回按出现顺序排列的 VisualBlock 列表。
    每个 block 记录了各关键字段的行号，供写入 API 使用。
    """
    text = filepath.read_text(encoding='utf-8')
    lines = text.split('\n')
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if '[VISUAL]' in line:
            block = VisualBlock(
                source_file=str(filepath),
                line_start=i + 1  # 1-indexed
            )
            j = i + 1
            asset_count = 0
            while j < len(lines) and lines[j].strip().startswith('>'):
                raw = lines[j].strip().lstrip('> ').strip()
                # 剥离 Markdown 列表项标记
                raw_clean = re.sub(r'^[*\-]\s+', '', raw)

                if raw_clean.startswith('**Slide**:'):
                    block.slide_id = raw_clean.split(':', 1)[1].strip().strip('`').strip('*').strip()

                elif raw_clean.startswith('**Layout**:'):
                    block.layout = raw_clean.split(':', 1)[1].strip().strip('`')

                elif '**Asset**:' in raw_clean and 'fallback' not in raw_clean.lower():
                    # 主 Asset 行
                    m = re.search(r'!\[(.*?)\]\(([^)]+)\)', raw_clean)
                    if m:
                        block.asset_alt = m.group(1)
                        block.asset_path = m.group(2)
                    block.asset_line = j + 1  # 1-indexed
                    asset_count += 1

                elif '**Asset' in raw_clean and 'fallback' in raw_clean.lower():
                    # AI fallback Asset 行
                    m = re.search(r'\(([^)]+)\)', raw_clean)
                    if m:
                        block.asset_fallback_path = m.group(1)

                elif raw_clean.startswith('**Scene**:'):
                    block.scene = raw_clean.split(':', 1)[1].strip()

                elif raw_clean.startswith('**Text**:'):
                    block.text = raw_clean.split(':', 1)[1].strip()

                elif raw_clean.startswith('**List**:'):
                    block.list_items = raw_clean.split(':', 1)[1].strip()

                elif raw_clean.startswith('**Source**:'):
                    block.source = raw_clean.split(':', 1)[1].strip()
                    block.source_line = j + 1  # 1-indexed

                elif raw_clean.startswith('**no_ai_flag**:'):
                    val = raw_clean.split(':', 1)[1].strip().lower()
                    block.no_ai_flag = val in ('true', 'yes', '1')

                j += 1

            block.line_end = j  # 下一行（超出块范围）
            blocks.append(block)
            i = j
        else:
            i += 1

    return blocks


def find_block_by_slide(filepath: Path, slide_id: str) -> Optional[VisualBlock]:
    """在文件中查找指定 slide_id 的 VISUAL 块"""
    blocks = parse_visual_blocks(filepath)
    for block in blocks:
        if block.slide_id == slide_id:
            return block
    return None


def update_visual_block(filepath: Path, slide_id: str, updates: dict) -> bool:
    """
    结构化更新 VISUAL 块的指定字段。
    
    支持的 updates 键:
      - 'asset': 新的主 Asset 路径
      - 'asset_alt': Asset 的 alt 文本（可选，默认保持原值）
      - 'asset_fallback': AI fallback Asset 路径（触发双轨模式）
      - 'source': Source 字段文本
    
    返回 True 表示已修改文件，False 表示未修改（块不存在或已是最新）。
    """
    block = find_block_by_slide(filepath, slide_id)
    if not block:
        return False

    lines = filepath.read_text(encoding='utf-8').split('\n')
    modified = False

    # ─── 更新 Asset 行 ───
    if 'asset' in updates and block.asset_line > 0:
        new_path = updates['asset']
        alt = updates.get('asset_alt', block.asset_alt or '预览')

        # 幂等性检查：如果已经指向 _real 路径，跳过
        if '_real' in block.asset_path:
            pass
        else:
            old_line_idx = block.asset_line - 1  # 0-indexed
            new_asset_line = f"> *   **Asset**: ![{alt}]({new_path})"

            # 如果需要双轨保留
            if 'asset_fallback' in updates:
                fallback_path = updates['asset_fallback']
                fallback_line = f"> *   **Asset (AI fallback)**: ![{alt}]({fallback_path})"
                lines[old_line_idx] = new_asset_line
                lines.insert(old_line_idx + 1, fallback_line)
                modified = True
                # 插入一行后，后续行号偏移 +1
                if block.source_line > block.asset_line:
                    block.source_line += 1
            else:
                lines[old_line_idx] = new_asset_line
                modified = True

    # ─── 更新 Source 行 ───
    if 'source' in updates:
        new_source = f"> **Source**: {updates['source']}"
        if block.source_line > 0:
            lines[block.source_line - 1] = new_source
            modified = True
        else:
            # 没有现有 Source 行 → 在块末尾（line_end 前一行之后）插入
            insert_pos = block.line_end - 1  # 块最后一个 > 行之后
            # 需要考虑前面可能的 asset_fallback 插入偏移
            lines.insert(insert_pos, new_source)
            modified = True

    if modified:
        filepath.write_text('\n'.join(lines), encoding='utf-8')

    return modified


def inject_dual_track_asset(
    filepath: Path,
    slide_id: str,
    real_path: str,
    source_text: str = "Web Source",
    alt_text: str = "预览"
) -> bool:
    """
    为指定 VISUAL 块注入双轨素材（_real 版 + AI fallback）。
    
    这是最常用的高级 API，封装了完整的双轨注入逻辑：
    1. 将原 Asset 降级为 AI fallback
    2. 插入新的 _real Asset 作为主路径
    3. 更新 Source 字段
    
    幂等性：如果 Asset 已指向 _real 路径，自动跳过。
    
    参数:
      filepath:    Markdown 文件路径
      slide_id:    目标 Slide ID
      real_path:   真实素材的相对路径（如 ../public/slides/xxx_real.jpg）
      source_text: Source 字段文本
      alt_text:    Asset 的 alt 文本
    
    返回 True 表示已修改，False 表示跳过。
    """
    block = find_block_by_slide(filepath, slide_id)
    if not block:
        print(f"  ⚠️  未找到 slide_id={slide_id} in {filepath.name}")
        return False

    # 幂等性：已有 _real 路径则跳过
    if '_real' in block.asset_path:
        print(f"  ⏭️  {slide_id} 已有 _real 素材，跳过")
        return False

    # 准备更新
    updates = {
        'asset': real_path,
        'asset_alt': alt_text,
        'asset_fallback': block.asset_path,  # 原路径降级为 fallback
        'source': source_text,
    }

    result = update_visual_block(filepath, slide_id, updates)
    if result:
        print(f"  ✅ {slide_id} 双轨注入完成")
    return result


def inject_lock(
    filepath: Path,
    slide_id: str,
    reason: str = "AI 概念图已充分传达教学意图，无需替换真实素材"
) -> bool:
    """
    为指定 VISUAL 块标记 Source 为 Locked，阻止未来扫描。
    
    参数:
      filepath:  Markdown 文件路径
      slide_id:  目标 Slide ID
      reason:    锁定理由
    """
    block = find_block_by_slide(filepath, slide_id)
    if not block:
        print(f"  ⚠️  未找到 slide_id={slide_id} in {filepath.name}")
        return False

    if block.source and 'locked' in block.source.lower():
        print(f"  ⏭️  {slide_id} 已锁定，跳过")
        return False

    updates = {'source': f"Locked -- {reason}"}
    result = update_visual_block(filepath, slide_id, updates)
    if result:
        print(f"  🔒 {slide_id} 已锁定")
    return result


# ═══════════════════════════════════════════════════════════
# 批量操作工具
# ═══════════════════════════════════════════════════════════

def scan_all_blocks(src_dir: Path) -> dict[str, tuple[Path, VisualBlock]]:
    """
    扫描目录下所有 M*.md 文件，返回 {slide_id: (filepath, block)} 字典。
    用于批量操作时的快速查找。
    """
    index = {}
    for md_file in sorted(src_dir.glob("M*.md")):
        blocks = parse_visual_blocks(md_file)
        for block in blocks:
            if block.slide_id:
                index[block.slide_id] = (md_file, block)
    return index


def batch_inject(src_dir: Path, injection_map: dict[str, dict]) -> dict:
    """
    批量注入素材。
    
    injection_map 格式:
      {
        "w02-slide-07c": {
          "real_path": "../public/slides/w02-slide-07c_real.jpg",
          "source": "Web Source",
          "disposition": "download"  # download / lock / skip
        },
        "w02-slide-09e": {
          "disposition": "lock",
          "lock_reason": "承认当前使用的 AI 素材"
        },
      }
    
    返回统计:
      {"injected": [...], "locked": [...], "skipped": [...], "not_found": [...]}
    """
    # 先建立全局索引
    block_index = scan_all_blocks(src_dir)
    
    stats = {"injected": [], "locked": [], "skipped": [], "not_found": []}

    for slide_id, spec in injection_map.items():
        disposition = spec.get("disposition", "download")

        if disposition == "skip":
            stats["skipped"].append(slide_id)
            continue

        if slide_id not in block_index:
            stats["not_found"].append(slide_id)
            print(f"  ❌ {slide_id} 未在任何脚本中找到")
            continue

        filepath, _ = block_index[slide_id]

        if disposition == "lock":
            reason = spec.get("lock_reason", "AI 素材足以满足教学需求")
            if inject_lock(filepath, slide_id, reason):
                stats["locked"].append(slide_id)
            else:
                stats["skipped"].append(slide_id)

        elif disposition == "download":
            real_path = spec.get("real_path", "")
            source_text = spec.get("source", "Web Source")
            if not real_path:
                print(f"  ⚠️  {slide_id} 缺少 real_path，跳过")
                stats["skipped"].append(slide_id)
                continue
            if inject_dual_track_asset(filepath, slide_id, real_path, source_text):
                stats["injected"].append(slide_id)
            else:
                stats["skipped"].append(slide_id)

        elif disposition == "generate":
            # AI 文生图的注入路径：使用 _real 后缀（虽然是 AI 生成的高精度概念图）
            real_path = spec.get("real_path", "")
            source_text = spec.get("source", "AI Generated")
            if real_path and inject_dual_track_asset(filepath, slide_id, real_path, source_text):
                stats["injected"].append(slide_id)
            else:
                stats["skipped"].append(slide_id)

    # 打印统计
    print(f"\n{'='*40}")
    print(f"  📊 批量注入统计")
    print(f"{'='*40}")
    print(f"  ✅ 注入成功:  {len(stats['injected'])}")
    print(f"  🔒 已锁定:    {len(stats['locked'])}")
    print(f"  ⏭️  跳过:      {len(stats['skipped'])}")
    print(f"  ❌ 未找到:    {len(stats['not_found'])}")

    return stats


if __name__ == "__main__":
    # 简单的自测
    import sys
    if len(sys.argv) < 2:
        print("用法: python visual_block_io.py <src_dir_or_file>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_file():
        blocks = parse_visual_blocks(target)
        print(f"解析到 {len(blocks)} 个 VISUAL 块:")
        for b in blocks:
            print(f"  [{b.slide_id}] L{b.asset_line} asset={b.asset_path[:40]}...")
    elif target.is_dir():
        index = scan_all_blocks(target)
        print(f"索引到 {len(index)} 个 VISUAL 块")
        for sid, (fp, b) in index.items():
            print(f"  [{sid}] → {fp.name} L{b.asset_line}")
