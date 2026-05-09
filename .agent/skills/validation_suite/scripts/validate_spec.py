#!/usr/bin/env python3
"""
脚本规范合规性检查 (Script Specification Validator)

检查脚本是否符合新规范：知识标签、VISUAL 块、ACTIVITY 块、Layout 类型等。

用法:
    python validate_spec.py --course "实习指导"
    python validate_spec.py --course "实习指导" --file S01_Mobilization.md
"""

import os
import sys
import re
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_parser import (
    parse_script, BlockType, get_workspace_root,
    get_scripts_dir, list_script_files, list_script_files_for_week,
    KNOWN_TAGS, VALID_LAYOUTS, VALID_ACTIVITY_TYPES,
    strip_markdown,
)

# ===== 新增检查项所需常量 =====

# 占位符残留检测模式
PLACEHOLDER_PATTERNS = [
    re.compile(r'自动生成的'),
    re.compile(r'请替换为'),
    re.compile(r'\[待补充\]'),
    re.compile(r'\[TODO\]', re.IGNORECASE),
    re.compile(r'\[TBD\]', re.IGNORECASE),
    re.compile(r'此处插入'),
]

# VISUAL 字段关键词（用于字段顺序检测）
VISUAL_FIELD_KEYWORDS = ['Layout', 'Scene', 'Slide', 'Asset', 'Text', 'List']

# 修辞黑名单——强信号修辞词组
# 与 validate_script_length.py 的 DEGENERATION_MARKERS（程度词）互补
RHETORIC_BLACKLIST = [
    '当场休克', '天灵盖', '万劫不复', '长征二号',
    '糖衣剧毒', '提线木偶', '无情的铁锤', '直冲天灵盖',
    '核弹级别', '毁灭性打击', '灵魂暴击',
]


def validate_single_script(file_path: str, filename: str) -> dict:
    """
    验证单个脚本文件。
    返回: {errors: [...], warnings: [...], stats: {...}}
    """
    blocks = parse_script(file_path)

    errors = []
    warnings = []

    # 统计
    tag_counts = {}
    visual_blocks = []
    activity_blocks = []
    slide_ids = []
    old_slide_refs = []

    for b in blocks:
        if b.block_type == BlockType.TAG:
            tag_name = b.metadata.get("tag_name", "UNKNOWN")
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
            # 检查白名单
            if tag_name not in KNOWN_TAGS:
                errors.append(f"L{b.line_start}: ❌ 未知标签 [{tag_name}]")
        # ADR 022 修复：口头叙事型标签被 parser 重分类为 SPEECH，
        # 需额外统计以反映真实的知识标签分布
        elif b.block_type == BlockType.SPEECH and b.metadata.get("oral_tag"):
            tag_name = b.metadata.get("tag_name", "UNKNOWN")
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1

        elif b.block_type == BlockType.VISUAL:
            visual_blocks.append(b)
            sid = b.metadata.get("slide_id", "")
            layout = b.metadata.get("layout", "")
            scene = b.metadata.get("scene", "")

            if sid:
                slide_ids.append((sid, b.line_start))
            else:
                errors.append(f"L{b.line_start}: ❌ VISUAL 块缺少 **Slide** 字段")
            if not layout:
                errors.append(f"L{b.line_start}: ❌ VISUAL 块缺少 **Layout** 字段")
            elif layout not in VALID_LAYOUTS:
                errors.append(f"L{b.line_start}: ❌ 无效 Layout 类型 `{layout}` (有效: {', '.join(sorted(VALID_LAYOUTS))})")
            if not scene:
                warnings.append(f"L{b.line_start}: ⚠️  VISUAL 块缺少 **Scene** 字段")

        elif b.block_type == BlockType.ACTIVITY:
            activity_blocks.append(b)
            atype = b.metadata.get("activity_type", "")
            duration = b.metadata.get("duration_raw", "")

            if not atype:
                errors.append(f"L{b.line_start}: ❌ ACTIVITY 块缺少 **Type** 字段")
            elif atype not in VALID_ACTIVITY_TYPES:
                errors.append(f"L{b.line_start}: ❌ 无效 Activity 类型 `{atype}` (有效: {', '.join(sorted(VALID_ACTIVITY_TYPES))})")
            if not duration:
                warnings.append(f"L{b.line_start}: ⚠️  ACTIVITY 块缺少 **Duration** 字段")

        elif b.block_type == BlockType.SLIDE_REF:
            old_slide_refs.append(b)
            errors.append(
                f"L{b.line_start}: ❌ 旧格式 [SLIDE: {b.metadata.get('slide_ref_id', '?')}] — "
                f"请迁移为 > [VISUAL] 内联块"
            )

    # Slide ID 唯一性
    seen_ids = {}
    for sid, line in slide_ids:
        if sid in seen_ids:
            errors.append(f"L{line}: ❌ 重复 Slide ID `{sid}` (首次出现于 L{seen_ids[sid]})")
        else:
            seen_ids[sid] = line

    # 知识面覆盖率
    tech_tags = sum(tag_counts.get(t, 0) for t in ["TECH NOTE", "WARNING", "DID YOU KNOW"])
    human_tags = sum(tag_counts.get(t, 0) for t in ["STORY TIME", "PHILOSOPHY", "CASE STUDY", "LIFE CONNECT"])
    teach_tags = tag_counts.get("TEACHING MOMENT", 0)

    # ===== 占位符残留检测 =====
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    for line_idx, raw_line in enumerate(raw_lines, 1):
        for pattern in PLACEHOLDER_PATTERNS:
            m = pattern.search(raw_line)
            if m:
                errors.append(
                    f"L{line_idx}: \u274c \u5360\u4f4d\u7b26\u6b8b\u7559: '{m.group()}'"
                )

    # ===== Bold 标记前导/尾随空格检测 =====
    for line_idx, raw_line in enumerate(raw_lines, 1):
        stripped = raw_line.strip()
        if not stripped.startswith('>'):
            continue
        if '**' in stripped:
            bold_pairs = re.findall(r'\*\*(.*?)\*\*', stripped)
            for bp in bold_pairs:
                if bp.startswith(' ') or bp.endswith(' '):
                    errors.append(
                        f"L{line_idx}: \u274c Bold \u6807\u8bb0\u5185\u6709\u591a\u4f59\u7a7a\u683c: '**{bp}**'"
                    )

    # ===== VISUAL 字段顺序验证 =====
    # 检测标签倒置：在 > [VISUAL] 之前出现了 > **Layout** 等字段
    for line_idx, raw_line in enumerate(raw_lines, 1):
        stripped = raw_line.strip()
        if not stripped.startswith('>'):
            continue
        # 检查是否有 VISUAL 字段但不在 VISUAL 块内
        for kw in ('Layout', 'Slide'):
            if f'**{kw}**:' not in stripped:
                continue
            # 向上搜索：最近的块起始是否为 > [VISUAL]
            found_visual_tag = False
            for back_idx in range(line_idx - 2, max(line_idx - 12, -1), -1):
                if back_idx < 0:
                    break
                back_line = raw_lines[back_idx].strip()
                if back_line.startswith('> [VISUAL]'):
                    found_visual_tag = True
                    break
                if not back_line.startswith('>'):
                    break
            if not found_visual_tag:
                errors.append(
                    f"L{line_idx}: \u274c VISUAL \u5b57\u6bb5\u987a\u5e8f\u9519\u8bef: "
                    f"'{kw}' \u51fa\u73b0\u5728 [VISUAL] \u6807\u8bb0\u4e4b\u524d"
                )

    # ===== 修辞黑名单物理拦截 =====
    for b in blocks:
        if b.block_type != BlockType.SPEECH:
            continue
        for word in RHETORIC_BLACKLIST:
            if word in b.content:
                for offset, content_line in enumerate(b.content.split('\n')):
                    if word in content_line:
                        warnings.append(
                            f"L{b.line_start + offset}: \u26a0\ufe0f  \u4fee\u8f9e\u9ed1\u540d\u5355\u547d\u4e2d: '{word}'"
                        )


    # 对每个 VISUAL 块，检查其后紧邻 SPEECH 块的字数与 Scene 描述字数的比值
    for idx, b in enumerate(blocks):
        if b.block_type != BlockType.VISUAL:
            continue
        scene = b.metadata.get("scene", "")
        slide_id = b.metadata.get("slide_id", "?")
        if not scene:
            continue  # 已在上方检查缺少 Scene 字段

        # 计算 Scene 中文字数（去除标点和空格）
        scene_text = strip_markdown(scene)
        scene_cn_chars = len(re.findall(r'[\u4e00-\u9fff]', scene_text))

        # 向后搜集紧邻的 SPEECH 块
        # 停止条件：遇到下一个 VISUAL/ACTIVITY/TAG/SEPARATOR 块，或 H3+ 子标题
        speech_chars = 0
        speech_text_all = []
        for j in range(idx + 1, len(blocks)):
            nxt = blocks[j]
            if nxt.block_type == BlockType.SPEECH:
                txt = strip_markdown(nxt.content)
                speech_text_all.append(txt)
                speech_chars += len(re.findall(r'[\u4e00-\u9fff]', txt))
            elif nxt.block_type == BlockType.HEADER:
                # H3+ 子标题意味着进入了新子话题，不再是对 VISUAL 的直接解读
                if nxt.metadata.get("level", 2) >= 3:
                    break
                # H2 标题允许继续（同级段落）
                continue
            elif nxt.block_type == BlockType.EMPTY:
                continue
            else:
                # VISUAL/ACTIVITY/TAG/SEPARATOR → 停止
                break

        # 判定
        min_threshold = max(scene_cn_chars * 2, 20)
        if speech_chars < min_threshold:
            warnings.append(
                f"L{b.line_start}: ⚠️  视觉解读深度不足 — "
                f"Slide `{slide_id}` 的 Scene 有 {scene_cn_chars} 字, "
                f"但后续 SPEECH 仅 {speech_chars} 字 "
                f"(要求 ≥ {min_threshold} 字)"
            )

    stats = {
        "tag_counts": tag_counts,
        "tech_tags": tech_tags,
        "human_tags": human_tags,
        "teach_tags": teach_tags,
        "visual_count": len(visual_blocks),
        "activity_count": len(activity_blocks),
        "old_refs": len(old_slide_refs),
        "slide_ids": [sid for sid, _ in slide_ids],
    }

    return {"errors": errors, "warnings": warnings, "stats": stats}


def main():
    parser = argparse.ArgumentParser(description="脚本规范合规性检查")
    parser.add_argument("--course", required=True, help="课程目录名")
    parser.add_argument("--file", help="指定单个脚本文件名（可选）")
    parser.add_argument("--week", type=int, default=None,
                        help="仅检查指定周次的脚本（如 --week 1）")
    args = parser.parse_args()

    workspace = get_workspace_root()
    scripts_dir = get_scripts_dir(workspace, args.course)

    if not os.path.exists(scripts_dir):
        print(f"❌ 脚本目录不存在: {scripts_dir}")
        sys.exit(1)

    if args.file:
        files = [args.file]
    elif args.week is not None:
        files = list_script_files_for_week(scripts_dir, args.week)
    else:
        files = list_script_files(scripts_dir)

    if not files:
        print(f"⚠️  未找到脚本文件: {scripts_dir}")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    print(f"\n{'='*60}")
    print(f"  脚本规范合规性报告")
    print(f"{'='*60}")
    print(f"  课程: {args.course}")
    if args.week is not None:
        print(f"  范围: 第 {args.week} 周")
    print(f"  脚本数: {len(files)}")
    print(f"{'='*60}")

    for fname in files:
        fpath = os.path.join(scripts_dir, fname)
        if not os.path.exists(fpath):
            print(f"\n❌ 文件不存在: {fname}")
            total_errors += 1
            continue

        result = validate_single_script(fpath, fname)
        errors = result["errors"]
        warns = result["warnings"]
        stats = result["stats"]

        status = "✅" if not errors else "❌"
        print(f"\n{status} {fname}")
        print(f"  VISUAL: {stats['visual_count']} | ACTIVITY: {stats['activity_count']} | 旧引用: {stats['old_refs']}")

        # 知识面
        if stats["tag_counts"]:
            print(f"  知识标签: 技术层={stats['tech_tags']} | 人文层={stats['human_tags']} | 教学层={stats['teach_tags']}")
        else:
            print(f"  知识标签: 无")

        if not stats["activity_count"] and stats["visual_count"] > 0:
            warns.append("⚠️  该脚本有 VISUAL 块但无 ACTIVITY 块 — 考虑添加教学活动环节")

        if stats["human_tags"] == 0 and stats["visual_count"] > 0:
            warns.append("⚠️  人文层标签为 0 — 建议至少添加 1 个人文标签")

        for e in errors:
            print(f"  {e}")
        for w in warns:
            print(f"  {w}")

        total_errors += len(errors)
        total_warnings += len(warns)

    # 汇总
    print(f"\n{'='*60}")
    if total_errors == 0:
        print(f"✅ 规范合规性检查通过 ({total_warnings} 个警告)")
    else:
        print(f"❌ 发现 {total_errors} 个错误, {total_warnings} 个警告")
    print(f"{'='*60}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
