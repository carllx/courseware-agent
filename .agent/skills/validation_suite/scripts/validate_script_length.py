#!/usr/bin/env python3
"""
脚本时长估算 + TTS 文本导出 + 词汇提取 (Script Length Validator)

功能模式:
  默认     — 打印时长估算表格（含 ACTIVITY 预估）
  --dump-text          — 导出带 [SLIDE #N] 标记的 .txt
  --dump-text --blind-mode — 导出纯朗读 .txt（无视觉标记）
  --dump-vocab         — 按章节提取英文术语表

用法:
    python validate_script_length.py --course "实习指导"
    python validate_script_length.py --course "实习指导" --dump-text --blind-mode --dump-vocab
"""

import os
import sys
import re
import json
import math
import argparse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_parser import (
    parse_script, BlockType, strip_markdown,
    get_workspace_root, get_scripts_dir,
    list_script_files, load_course_config,
)

# ===== 语速常量 =====
# 教学标准: ~180 字/分钟 (lecture 模式)
DELIVERY_SPEEDS = {
    "video_essay": 160,  # 字/分钟
    "lecture": 180,
    "workshop": 140,
}
DEFAULT_CN_CPM = 180
AVG_EN_WPM = 130


def get_cn_cpm(course_config: dict) -> int:
    """从 course.yaml 获取语速（默认 lecture 模式）。"""
    mode = course_config.get("course", {}).get("delivery_mode", "lecture")
    return DELIVERY_SPEEDS.get(mode, DEFAULT_CN_CPM)


def format_time(seconds: float) -> str:
    """格式化秒数为 Xm Xs 格式。"""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m {s}s"


def analyze_file(file_path: str, blind_mode: bool = False) -> dict:
    """
    分析单个脚本文件。

    返回:
        cn_count: 中文字数
        en_count: 英文词数
        activity_sec: ACTIVITY 总时长（秒）
        activity_details: ACTIVITY 明细
        text_lines: 提取的文本行（用于 TTS 导出）
        slide_markers: Slide 标记列表
    """
    blocks = parse_script(file_path)

    cn_count = 0
    en_count = 0
    activity_sec = 0
    activity_details = []
    text_lines = []
    slide_counter = 0

    # TTS 清洗：需要移除的非朗读标记模式
    RE_PAUSE = re.compile(r'^\(?\s*Pause\s*:\s*\d+s\s*\)?$', re.IGNORECASE)
    RE_STAGE_DIR = re.compile(r'^（讲师口述）[：:]?\s*$')
    RE_GH_ALERT = re.compile(r'^\[!(NOTE|WARNING|CAUTION|TIP|IMPORTANT)\]')
    # 行内标签标题（blind 模式下移除），如 [CASE STUDY: 标题]
    RE_INLINE_TAG = re.compile(r'^\[([A-Z ]+?)(?::.*?)?\]\s*$')
    # Markdown 表格分隔行：|:---|:---|  或 |---|---|
    RE_TABLE_SEP = re.compile(r'^\|[\s:\-|]+\|$')

    for b in blocks:
        if b.block_type == BlockType.SPEECH:
            pure = strip_markdown(b.content)

            # 跳过空内容
            if not pure.strip():
                continue

            # 逐行过滤（内容可能含多行）
            filtered_lines = []
            for raw_line in pure.split('\n'):
                sl = raw_line.strip()
                if not sl:
                    continue
                # 跳过纯标注行 [ ... ]
                if sl.startswith("[") and sl.endswith("]"):
                    continue
                # 跳过 HTML 注释
                if sl.startswith("<!--"):
                    continue
                # 跳过 Pause 停顿指示
                if RE_PAUSE.match(sl):
                    continue
                # 跳过舞台指示（讲师口述）
                if RE_STAGE_DIR.match(sl):
                    continue
                # 跳过 GitHub 风格提示块标签
                if RE_GH_ALERT.match(sl):
                    continue
                # blind 模式下跳过行内知识标签标题
                if blind_mode and RE_INLINE_TAG.match(sl):
                    continue
                # 跳过 Markdown 表格分隔行
                if RE_TABLE_SEP.match(sl):
                    continue
                # 表格数据行：将管道符替换为逗号，使其可朗读
                if sl.startswith('|') and sl.endswith('|'):
                    sl = sl.strip('|')
                    sl = '，'.join(cell.strip() for cell in sl.split('|') if cell.strip())
                # 最终安全守卫：过滤后如果不含任何中英文字符则跳过
                if not re.search(r'[\u4e00-\u9fffa-zA-Z0-9]', sl):
                    continue
                filtered_lines.append(sl)

            if not filtered_lines:
                continue

            clean_text = '\n'.join(filtered_lines)
            cn_count += len(re.findall(r'[\u4e00-\u9fff]', clean_text))
            en_count += len(re.findall(r'[a-zA-Z0-9]+', clean_text))
            text_lines.extend(filtered_lines)

        elif b.block_type == BlockType.VISUAL:
            slide_counter += 1
            sid = b.metadata.get("slide_id", "未命名")
            if not blind_mode:
                text_lines.append(f"\n[SLIDE #{slide_counter}: {sid}]")

        elif b.block_type == BlockType.SLIDE_REF:
            slide_counter += 1
            sid = b.metadata.get("slide_ref_id", "未命名")
            if not blind_mode:
                text_lines.append(f"\n[SLIDE #{slide_counter}: {sid}]")

        elif b.block_type == BlockType.ACTIVITY:
            dur = b.metadata.get("duration_sec", 0)
            activity_sec += dur
            activity_details.append({
                "type": b.metadata.get("activity_type", "?"),
                "duration": b.metadata.get("duration_raw", "?"),
                "duration_sec": dur,
                "desc": b.metadata.get("desc", ""),
            })

        elif b.block_type == BlockType.TAG:
            # 特殊处理 [SPEECH] 标签，将其内容视为正文
            if b.metadata.get("tag_name") == "SPEECH":
                pure = strip_markdown(b.content)
                if pure.strip():
                    text_lines.append(pure.strip())
                    cn_count += len(re.findall(r'[\u4e00-\u9fff]', pure))
                    en_count += len(re.findall(r'[a-zA-Z0-9]+', pure))

    return {
        "cn": cn_count,
        "en": en_count,
        "activity_sec": activity_sec,
        "activity_details": activity_details,
        "text_lines": text_lines,
        "slides": slide_counter,
    }


def analyze_modules(file_path: str, cn_cpm: int) -> list[dict]:
    """
    按 ## (H2) 标题切分脚本为模块，对每个模块独立统计。

    返回:
        模块信息列表，每个模块包含: name, cn_count, en_count,
        activity_sec, lecture_sec, lecture_est_min, budget_minutes,
        budget_chars, fill_ratio, oral_tag_count, section_text
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按 ## 切分（跳过 frontmatter）
    fm_match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    if fm_match:
        content_body = content[fm_match.end():]
    else:
        content_body = content

    # 按 ## 标题切分
    module_pattern = re.compile(r'^## (.+)$', re.MULTILINE)
    splits = list(module_pattern.finditer(content_body))

    if not splits:
        return []

    modules = []
    for i, match in enumerate(splits):
        name = match.group(1).strip()
        start = match.end()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(content_body)
        section = content_body[start:end]

        # ===== 预算提取：从标题中提取自声明预算 =====
        # 兼容中英文格式：(约 25 分钟) / (25 min) / (25 minutes)
        budget_match = re.search(r'约?\s*(\d+)\s*(?:分钟|min(?:utes?)?)', name)
        budget_minutes = int(budget_match.group(1)) if budget_match else None

        # ===== STATUS 提取：从 BUDGET 注释中提取模块状态 =====
        status_match = re.search(r'<!--.*?STATUS:\s*(\w+)\s*-->', section)
        module_status = status_match.group(1).strip() if status_match else None

        # 统计中文字数（排除 VISUAL/ACTIVITY 块、标题、分隔符等）
        cn_count = 0
        en_count = 0
        activity_sec = 0
        oral_tag_count = 0  # 口头型知识标签计数（稀释检测用）
        speech_lines = []   # 收集讲授文本行（稀释检测用）

        in_visual = False
        in_activity = False
        in_ref_tag = False  # 参考型标签（TECH NOTE / WARNING）

        # 口头型标签：内容计入字数（ADR 022）
        oral_tag_names = {
            'STORY TIME', 'CASE STUDY', 'LIFE CONNECT',
            'PHILOSOPHY', 'DID YOU KNOW', 'TEACHING MOMENT',
        }
        # 参考型标签：内容不计入字数
        ref_tag_names = {'TECH NOTE', 'WARNING'}

        for line in section.split('\n'):
            stripped = line.strip()

            # 检测块开始
            if stripped.startswith('> [VISUAL]'):
                in_visual = True
                continue
            if stripped.startswith('> [ACTIVITY]') or stripped.startswith('> [ACTIVITY:'):
                in_activity = True
                continue

            # 检测参考型标签块开始
            if stripped.startswith('> ['):
                tag_match = re.match(r'>\s+\[([A-Z ]+?)(?::.*?)?\]', stripped)
                if tag_match:
                    tag_name = tag_match.group(1).strip()
                    if tag_name in ref_tag_names:
                        in_ref_tag = True
                        continue
                    elif tag_name in oral_tag_names:
                        oral_tag_count += 1  # 统计口头型标签数量
                        continue

            # 块内行
            if in_visual:
                if stripped.startswith('>'):
                    continue
                else:
                    in_visual = False
            if in_activity:
                if stripped.startswith('>'):
                    dur_match = re.search(r'(\d+)\s*min', stripped)
                    if dur_match:
                        activity_sec += int(dur_match.group(1)) * 60
                    continue
                else:
                    in_activity = False
            if in_ref_tag:
                if stripped.startswith('>'):
                    continue
                else:
                    in_ref_tag = False

            # 跳过非讲授内容
            if (stripped.startswith('#') or stripped == '---' or
                stripped == '' or
                re.match(r'^\*{0,2}\(?\s*Pause\s*:\s*\d+s\s*\)?\*{0,2}$', stripped, re.IGNORECASE) or
                stripped.startswith('> [') or
                stripped.startswith('<!-- ')):
                continue

            # 口头型标签块内的引用行（> 开头），提取内容计入字数
            if stripped.startswith('>'):
                stripped = stripped.lstrip('>').strip()

            # 统计字数并收集文本
            cn_count += len(re.findall(r'[\u4e00-\u9fff]', stripped))
            en_count += len(re.findall(r'[a-zA-Z0-9]+', stripped))
            speech_lines.append(stripped)

        lecture_sec = (cn_count / cn_cpm * 60) + (en_count / AVG_EN_WPM * 60)

        # ===== 预算对标计算 =====
        activity_min = activity_sec / 60
        is_activity_only = False

        # 优先从 <!-- BUDGET: X chars --> 注释中直接提取显式预算（如果存在）
        budget_comment_match = re.search(r'<!--\s*BUDGET:\s*(\d+)\s*chars', section)
        if budget_comment_match:
            budget_chars = int(budget_comment_match.group(1))
            fill_ratio = cn_count / budget_chars if budget_chars > 0 else None
            if budget_chars == 0 and activity_min > 0:
                is_activity_only = True
        elif budget_minutes is not None:
            # Fallback: 标题有时间标注 → 扣除 Activity 占用后计算讲授字数预算
            net_budget_min = max(budget_minutes - activity_min, 0)
            budget_chars = int(net_budget_min * cn_cpm)
            fill_ratio = cn_count / budget_chars if budget_chars > 0 else None
            # 当全部时间被 Activity 占用时标记为活动豁免
            is_activity_only = (net_budget_min == 0 and activity_min > 0)
        else:
            budget_chars = None
            fill_ratio = None

        # ===== 活动模块豁免检测 =====
        has_exempt_comment = bool(re.search(r'<!--.*?TYPE:\s*activity.*?STATUS:\s*exempt.*?-->', section))
        is_exempt = has_exempt_comment or is_activity_only

        modules.append({
            'name': name,
            'cn_count': cn_count,
            'en_count': en_count,
            'activity_sec': activity_sec,
            'lecture_sec': lecture_sec,
            'lecture_est_min': lecture_sec / 60,
            'total_sec': lecture_sec + activity_sec,
            'budget_minutes': budget_minutes,
            'budget_chars': budget_chars,
            'fill_ratio': fill_ratio,
            'oral_tag_count': oral_tag_count,
            'section_text': '\n'.join(speech_lines),
            'status': module_status,
            'is_exempt': is_exempt,
        })

    return modules


# ===== LLM 退化标记词表（rule_narrative_standards.md §7.4）=====
DEGENERATION_MARKERS = [
    '极其', '极度', '极点', '绝对', '毫无', '不可',
    '极端', '死死', '彻底', '极致',
]


def detect_dilution(mod: dict) -> dict:
    """
    稀释与退化检测 (Anti-Dilution + Anti-Degeneration)。

    检测"字数够但内容空"的稀释现象和 LLM 文本退化，返回辅助指标 dict：
      - oral_tag_count: 口头型知识标签数量
      - tag_coverage_ok: 知识标签覆盖率是否达标 (oral_tags >= ⌈cn_count/2000⌉)
      - avg_sentence_len: 平均句长（中文字符数）
      - long_sentences: 超长句（>40 字）数量
      - repeated_phrases: 重复短语（>=3 次、>6 字）列表
      - is_diluted: 是否疑似稀释
      - marker_density: 退化标记词密度（次/百字）
      - max_unpunctuated: 最长无标点句汉字数
      - has_cycle: 是否存在 4-gram 循环碎片
      - is_degenerated: 综合退化判定
      - degen_reasons: 退化原因列表
    """
    text = mod.get('section_text', '')
    cn_count = mod.get('cn_count', 0)
    oral_tags = mod.get('oral_tag_count', 0)

    # 1. 知识标签覆盖率（按比例：每 2000 字至少 1 个口头型标签）
    required_tags = math.ceil(cn_count / 2000) if cn_count > 0 else 0
    tag_coverage_ok = True
    if required_tags > 0 and oral_tags < required_tags:
        tag_coverage_ok = False

    # 2. 平均句长分析（按中文句末标点断句）
    sentences = re.split(r'[。！？；\n]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    cn_lens = []
    long_sentences = 0
    for s in sentences:
        cn_len = len(re.findall(r'[\u4e00-\u9fff]', s))
        if cn_len > 0:
            cn_lens.append(cn_len)
            if cn_len > 40:
                long_sentences += 1
    avg_sentence_len = sum(cn_lens) / len(cn_lens) if cn_lens else 0

    # 3. 重复短语检测（滑窗法，>6 中文字的短语）
    cn_text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    phrase_len = 7
    phrase_counts = Counter()
    if len(cn_text) >= phrase_len:
        for j in range(len(cn_text) - phrase_len + 1):
            phrase = cn_text[j:j + phrase_len]
            phrase_counts[phrase] += 1
    repeated_phrases = [
        (phrase, count) for phrase, count in phrase_counts.items()
        if count >= 3
    ]
    repeated_phrases.sort(key=lambda x: x[1], reverse=True)
    repeated_phrases = repeated_phrases[:5]

    # 4. 稀释综合判定
    is_diluted = False
    reasons = []
    if not tag_coverage_ok:
        is_diluted = True
        reasons.append(f'标签{oral_tags}/{required_tags}')
    if avg_sentence_len > 40:
        is_diluted = True
        reasons.append(f'均句{avg_sentence_len:.0f}字')
    if len(repeated_phrases) > 0:
        is_diluted = True
        reasons.append(f'{len(repeated_phrases)}组重复')

    # ===== 5. LLM 退化检测（rule_narrative_standards.md §7.4）=====

    # 5a. 极端修饰语密度（次/百字）
    marker_count = sum(text.count(w) for w in DEGENERATION_MARKERS)
    marker_density = marker_count / (cn_count / 100) if cn_count > 0 else 0

    # 5b. 最长无标点句（两个句末标点之间的最大汉字数）
    max_unpunctuated = max(
        (len(re.findall(r'[\u4e00-\u9fff]', seg)) for seg in sentences),
        default=0
    )

    # 5c. 4-gram 循环碎片检测（捕捉阶段Ⅲ退化的短循环）
    ngram4_counts = Counter()
    if len(cn_text) >= 4:
        for j in range(len(cn_text) - 3):
            ngram4_counts[cn_text[j:j + 4]] += 1
    worst_4gram = ngram4_counts.most_common(1)[0] if ngram4_counts else (None, 0)
    has_cycle = worst_4gram[1] > 8

    # 5d. 退化综合判定
    is_degenerated = False
    degen_reasons = []
    if marker_density > 6:
        is_degenerated = True
        degen_reasons.append(f'修饰语{marker_density:.1f}/百字')
    if max_unpunctuated > 400:
        is_degenerated = True
        degen_reasons.append(f'无标点{max_unpunctuated}字')
    if has_cycle:
        is_degenerated = True
        degen_reasons.append(f'4g循环×{worst_4gram[1]}')

    return {
        'oral_tag_count': oral_tags,
        'tag_coverage_ok': tag_coverage_ok,
        'avg_sentence_len': avg_sentence_len,
        'long_sentences': long_sentences,
        'repeated_phrases': repeated_phrases,
        'is_diluted': is_diluted,
        'reasons': reasons,
        # 退化检测字段
        'marker_density': round(marker_density, 1),
        'max_unpunctuated': max_unpunctuated,
        'has_cycle': has_cycle,
        'is_degenerated': is_degenerated,
        'degen_reasons': degen_reasons,
    }


def extract_vocabulary(text: str) -> list[str]:
    """从文本中提取英文术语/短语。"""
    pattern = r'(?:[a-zA-Z0-9\u00C0-\u00FF]+(?:[\s\+\-\.\/]+[a-zA-Z0-9\u00C0-\u00FF]+)*)'
    matches = re.findall(pattern, text)

    stop_words = {
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he",
        "was", "for", "on", "are", "as", "with", "his", "they", "i", "at", "be",
        "this", "have", "from", "or", "one", "had", "by", "word", "but", "not",
        "what", "all", "were", "we", "when", "your", "can", "said", "there",
        "use", "an", "each", "which", "she", "do", "how", "their", "if", "will",
        "up", "other", "about", "out", "many", "then", "them", "these", "so",
        "some", "her", "would", "make", "like", "him", "into", "time", "has",
        "look", "two", "more", "go", "see", "no", "way", "could", "my", "than",
        "first", "been", "who", "its", "now", "find", "long", "down", "day",
        "did", "get", "come", "made", "may", "part", "role", "action", "step",
        "note", "scene", "slide", "ppt", "ref", "act", "context", "tone",
        "warning", "result",
    }

    vocab = []
    for m in matches:
        m = m.strip()
        m_lower = m.lower()
        if len(m) <= 1:
            continue
        words = m.split()
        if len(words) > 6:
            continue
        if m_lower in stop_words:
            continue
        if re.match(r'^[\d\-\.\/]+$', m):
            continue
        vocab.append(m)
    return vocab


def main():
    parser = argparse.ArgumentParser(description="脚本时长估算与 TTS 导出")
    parser.add_argument("--course", default=None, help="课程目录名")
    parser.add_argument("--file", default=None,
                        help="直接指定脚本文件路径（绕过课程目录发现，支持单 segment 或 _compiled.md）")
    parser.add_argument("--dump-text", action="store_true", help="导出 TTS 纯文本")
    parser.add_argument("--blind-mode", action="store_true", help="盲读模式（无视觉标记）")
    parser.add_argument("--dump-vocab", action="store_true", help="提取英文术语表")
    parser.add_argument("--module-breakdown", action="store_true", help="按模块分析字数分布（ADR 020）")
    parser.add_argument("--week", type=int, default=None, help="仅分析指定周次的脚本（如 --week 1）")
    parser.add_argument("--speed-override", type=int, default=None,
                        help="覆盖语速常量（字/分钟），用于单课程试点")
    parser.add_argument("--module", type=str, default=None,
                        help="仅检查指定模块（模块标题的关键词匹配，配合 --module-breakdown 使用）")
    parser.add_argument("--segment-check", action="store_true",
                        help="精简 JSON 输出模式，供写作中间检查点使用（需配合 --module-breakdown）")
    args = parser.parse_args()

    # --segment-check 隐含 --module-breakdown
    if args.segment_check:
        args.module_breakdown = True

    # --file 模式：直传文件路径，不走课程发现逻辑
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        # 推断 course_config：尝试从文件路径逆推课程目录
        workspace = get_workspace_root()
        course_config = {}
        file_abs = os.path.abspath(args.file)
        if args.course:
            course_config = load_course_config(workspace, args.course)
        cn_cpm = args.speed_override if args.speed_override else get_cn_cpm(course_config)
        scripts_dir = os.path.dirname(args.file)
        files = [os.path.basename(args.file)]
    elif args.course:
        workspace = get_workspace_root()
        scripts_dir = get_scripts_dir(workspace, args.course)
        course_config = load_course_config(workspace, args.course)
        cn_cpm = args.speed_override if args.speed_override else get_cn_cpm(course_config)

        if not os.path.exists(scripts_dir):
            print(f"❌ 脚本目录不存在: {scripts_dir}")
            sys.exit(1)

        files = list_script_files(scripts_dir)
    else:
        print("❌ 必须指定 --course 或 --file 之一")
        sys.exit(1)

    # --week N 过滤：仅保留指定周次的脚本
    # 兼容两种路径格式: "W01_xxx.md" (旧) 或 "W01_xxx/script_compiled.md" (新)
    if args.week is not None:
        week_prefix = f"W{args.week:02d}_"
        files = [f for f in files if week_prefix in f]
        if not files:
            print(f"⚠️  未找到第 {args.week} 周的脚本文件（前缀 {week_prefix}）。")
            sys.exit(0)

    if not files:
        print(f"⚠️  未找到脚本文件。")
        sys.exit(0)

    # 判断模式
    is_stats_mode = not (args.dump_text or args.dump_vocab)

    if is_stats_mode:
        print(f"\n{'='*80}")
        print(f"  脚本时长估算报告  |  语速: {cn_cpm} 字/分钟")
        print(f"{'='*80}")
        print(f"{'文件':<25} | {'字数':^10} | {'Slide':^5} | {'活动时长':^8} | {'预估时长':^10}")
        print("-" * 80)

    total_cn = 0
    total_en = 0
    total_activity = 0
    total_secs = 0
    all_vocab_by_chapter = {}

    for fname in files:
        fpath = os.path.join(scripts_dir, fname)
        stats = analyze_file(fpath, blind_mode=args.blind_mode)

        speech_sec = (stats["cn"] / cn_cpm * 60) + (stats["en"] / AVG_EN_WPM * 60)
        file_total = speech_sec + stats["activity_sec"]

        if is_stats_mode:
            word_str = f"{stats['cn']}/{stats['en']}"
            act_str = format_time(stats["activity_sec"]) if stats["activity_sec"] > 0 else "-"
            print(f"{fname:<25} | {word_str:^10} | {stats['slides']:^5} | {act_str:^8} | {format_time(file_total):^10}")

        total_cn += stats["cn"]
        total_en += stats["en"]
        total_activity += stats["activity_sec"]
        total_secs += file_total

        # TTS 文本导出
        if args.dump_text and stats["text_lines"]:
            tts_dir = os.path.join(scripts_dir, "tts")
            os.makedirs(tts_dir, exist_ok=True)
            base_name = os.path.splitext(fname)[0]
            suffix = "_blind" if args.blind_mode else ""
            out_path = os.path.join(tts_dir, f"{base_name}{suffix}.txt")
            try:
                with open(out_path, 'w', encoding='utf-8') as f:
                    for line in stats["text_lines"]:
                        f.write(line + "\n")
                mode_label = "Blind" if args.blind_mode else "Standard"
                print(f"✅ [{mode_label:8s}] {out_path}")
            except Exception as e:
                print(f"❌ 写入失败 {out_path}: {e}")

        # 词汇收集
        if args.dump_vocab and stats["text_lines"]:
            chapter_vocab = set()
            for line in stats["text_lines"]:
                terms = extract_vocabulary(line)
                for t in terms:
                    chapter_vocab.add(t)
            all_vocab_by_chapter[fname] = chapter_vocab

    # 汇总
    if is_stats_mode:
        print("-" * 80)
        print(f"  讲授字数 : {total_cn} 字 (CN) / {total_en} 词 (EN)")
        print(f"  活动时长 : {format_time(total_activity)}")
        print(f"  预估总时长: {format_time(total_secs)}")

    # 模块级预算对标分析 (ADR 020 + MSG-019)
    if args.module_breakdown:
        # --segment-check 模式：仅输出 JSON，不打印表头
        segment_results = [] if args.segment_check else None

        if not args.segment_check:
            print(f"\n{'='*115}")
            print(f"  模块级预算对标分析  |  语速: {cn_cpm} 字/分钟  |  合格线: 100%  警告线: 80%")
            print(f"{'='*115}")
            print(f"{'文件':<25} | {'模块':<30} | {'实际':^6} | {'预算':^6} | {'完成率':^7} | {'标签':^7} | {'状态':^4} | {'稀释检测'}")
            print("-" * 115)

        # 汇总计数器
        count_pass = 0    # 达标
        count_warn = 0    # 偏薄
        count_fail = 0    # 严重不足
        count_unknown = 0 # 无预算
        count_exempt = 0  # 活动豁免
        count_draft = 0   # draft 模块

        for fname in files:
            fpath = os.path.join(scripts_dir, fname)
            modules = analyze_modules(fpath, cn_cpm)
            if not modules:
                if not args.segment_check:
                    print(f"{fname:<25} | {'(无模块结构)':<30} | {'-':^6} | {'-':^6} | {'-':^7} | {'-':^7} | {'-':^4} | -")
                continue

            # --module 过滤：仅保留匹配的模块
            if args.module:
                modules = [m for m in modules if args.module.lower() in m['name'].lower()]
                if not modules:
                    continue

            for mod in modules:
                mod_name = mod['name'][:28] + '..' if len(mod['name']) > 30 else mod['name']

                # ===== Draft 状态优先判定（策略 2b）=====
                is_draft = mod.get('status') == 'draft'
                if is_draft:
                    count_draft += 1

                # ===== 预算百分比判定（替换原硬编码 < 1000）=====
                if mod['fill_ratio'] is not None:
                    pct = mod['fill_ratio']
                    pct_str = f"{pct*100:.0f}%"
                    if is_draft:
                        status = "\u274c"
                        count_fail += 1
                    elif pct >= 1.0:
                        status = "\u2705"
                        count_pass += 1
                    elif pct >= 0.8:
                        status = "\u26a0\ufe0f"
                        count_warn += 1
                    else:
                        status = "\u274c"
                        count_fail += 1
                    budget_str = str(mod['budget_chars'])
                else:
                    pct_str = "-"
                    if is_draft:
                        status = "\u274c"
                        count_fail += 1
                    elif mod.get('is_exempt', False):
                        status = "🏷️"
                        count_exempt += 1
                    else:
                        status = "?"
                        count_unknown += 1
                    budget_str = "-"

                # ===== 人文标签密度判定（策略 1 + V-6 fallback）=====
                oral_tags = mod.get('oral_tag_count', 0)
                budget_chars = mod.get('budget_chars', 0)
                cn_count_mod = mod.get('cn_count', 0)
                if budget_chars:
                    required_tags = math.ceil(budget_chars / 2000)
                elif cn_count_mod > 1000:
                    # V-6 fallback：无预算但有实质内容的模块，按实际字数计算
                    required_tags = math.ceil(cn_count_mod / 2000)
                else:
                    required_tags = 0
                if required_tags > 0:
                    tag_str = f"{oral_tags}/{required_tags}"
                    if oral_tags < required_tags:
                        tag_str += " \u274c"
                else:
                    tag_str = f"{oral_tags}/-"

                # ===== 稀释 + 退化检测 =====
                dilution = detect_dilution(mod)
                dilute_parts = []
                if dilution.get('is_degenerated'):
                    dilute_parts.append(f"[DEGEN] {','.join(dilution['degen_reasons'])}")
                elif dilution['is_diluted']:
                    dilute_parts.append(f"[DILUTED?] {','.join(dilution['reasons'])}")
                if is_draft:
                    dilute_parts.append("[DRAFT]")
                dilute_str = ' '.join(dilute_parts) if dilute_parts else "-"
                if len(dilute_str) > 40:
                    dilute_str = dilute_str[:38] + '..'

                # 退化计数
                if dilution.get('is_degenerated'):
                    count_fail += 1

                # --segment-check: 收集 JSON 结果
                if args.segment_check:
                    segment_results.append({
                        'file': fname,
                        'module': mod['name'],
                        'cn_count': mod['cn_count'],
                        'budget': mod.get('budget_chars'),
                        'fill_ratio': round(mod['fill_ratio'], 3) if mod['fill_ratio'] is not None else None,
                        'deficit': max(0, (mod.get('budget_chars') or 0) - mod['cn_count']),
                        'slides': 0,  # 将在后续统计中填充
                        'oral_tags': oral_tags,
                        'status': mod.get('status', 'unknown'),
                        'is_diluted': dilution['is_diluted'],
                        'is_degenerated': dilution.get('is_degenerated', False),
                        'degen_reasons': dilution.get('degen_reasons', []),
                    })
                else:
                    print(f"{fname:<25} | {mod_name:<30} | {mod['cn_count']:^6} | {budget_str:^6} | {pct_str:^7} | {tag_str:^7} | {status:^4} | {dilute_str}")

            # 文件小计（segment-check 模式下跳过）
            if not args.segment_check:
                file_total_cn = sum(m['cn_count'] for m in modules)
                file_total_budget = sum(m['budget_chars'] for m in modules if m['budget_chars'] is not None)
                file_ratio = file_total_cn / file_total_budget if file_total_budget > 0 else None
                ratio_str = f"{file_ratio*100:.0f}%" if file_ratio is not None else "-"
                print(f"{'':25} | {'[小计]':<30} | {file_total_cn:^6} | {file_total_budget:^6} | {ratio_str:^7} | {'':^7} |      |")
                print("-" * 115)

        # --segment-check: 输出 JSON 并退出
        if args.segment_check:
            print(json.dumps(segment_results, ensure_ascii=False, indent=2))
            has_fail = any(r.get('fill_ratio') is not None and r['fill_ratio'] < 0.8
                          for r in segment_results)
            has_degen = any(r.get('is_degenerated') for r in segment_results)
            sys.exit(1 if (has_fail or has_degen) else 0)

        # 汇总行
        summary_parts = [f"达标 {count_pass}", f"偏薄 {count_warn}", f"不足 {count_fail}"]
        if count_draft > 0:
            summary_parts.append(f"Draft {count_draft}")
        if count_exempt > 0:
            summary_parts.append(f"活动豁免 {count_exempt}")
        if count_unknown > 0:
            summary_parts.append(f"无预算 {count_unknown}")
        print(f"\n  \U0001f4ca 汇总: {' / '.join(summary_parts)}")

        # 退出码：存在 ❌ 时返回非 0
        if count_fail > 0:
            print(f"\n  \u26d4 存在 {count_fail} 个严重不足模块，退出码 1")
            sys.exit(1)

    # 词汇表输出
    if args.dump_vocab and all_vocab_by_chapter:
        tts_dir = os.path.join(scripts_dir, "tts")
        os.makedirs(tts_dir, exist_ok=True)
        vocab_path = os.path.join(tts_dir, "Vocabulary_List.md")
        try:
            with open(vocab_path, 'w', encoding='utf-8') as f:
                f.write("# 课程术语表 (Vocabulary List)\n\n")
                f.write(f"从 {len(all_vocab_by_chapter)} 个章节中提取。\n")
                for fname in sorted(all_vocab_by_chapter.keys()):
                    terms = sorted(list(all_vocab_by_chapter[fname]), key=lambda x: x.lower())
                    base_name = os.path.splitext(fname)[0]
                    f.write(f"\n## {base_name}\n\n")
                    if not terms:
                        f.write("_无显著英文术语。_\n")
                    else:
                        for term in terms:
                            f.write(f"- {term}\n")
            print(f"✅ [Vocab   ] {vocab_path}")
        except Exception as e:
            print(f"❌ 词汇表写入失败: {e}")


if __name__ == "__main__":
    main()
