#!/usr/bin/env python3
"""
SRT → TTS 段落拆分脚本

功能：
- 解析 SRT/VTT 字幕文件
- 按 TTS 引擎最佳粒度合并/拆分段落
- 计算 DJB2 指纹（与 doubaotts 的 _compute_tts_fingerprint() 兼容）
- 输出 JSON manifest 供 TTS 提取和音频拼接使用

使用示例：
    python prepare_tts_segments.py --srt subtitles.zh-Hans.srt --output manifest.json
    python prepare_tts_segments.py --srt subtitles.srt --max-chars 100 --output manifest.json
"""
import argparse
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class TtsSegment:
    """TTS 段落数据结构"""

    id: int  # 段落序号（从 1 开始）
    text: str  # 段落文本
    start: float  # 起始时间（秒）
    end: float  # 结束时间（秒）
    duration: float  # 持续时间（秒）
    fingerprint: str  # DJB2 指纹
    char_count: int  # 字符数


def djb2_hash(text: str) -> str:
    """
    DJB2 哈希算法，与 doubaotts 的 _compute_tts_fingerprint() 兼容

    Args:
        text: 输入文本

    Returns:
        格式为 "{hash}_{length}" 的指纹字符串
    """
    h = 5381
    for ch in text:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return f"{h:08x}_{len(text)}"


def parse_timestamp(ts: str) -> float:
    """
    解析时间戳字符串为秒数

    支持两种格式：
    - SRT: 00:01:23,456
    - VTT: 00:01:23.456

    Args:
        ts: 时间戳字符串

    Returns:
        秒数（浮点数）
    """
    ts = ts.strip().replace(",", ".")
    parts = ts.split(":")

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])

    return hours * 3600 + minutes * 60 + seconds


def parse_srt(filepath: str) -> list[dict]:
    """
    解析 SRT 文件为段落列表

    Args:
        filepath: SRT 文件路径

    Returns:
        段落列表，每项包含 start, end, text
    """
    content = Path(filepath).read_text(encoding="utf-8")
    segments = []

    # 按空行分割字幕块
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # 解析时间戳行
        timestamp_line = lines[1]
        match = re.match(
            r"(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})",
            timestamp_line,
        )
        if not match:
            continue

        start = parse_timestamp(match.group(1))
        end = parse_timestamp(match.group(2))

        # 文本可能多行
        text_lines = lines[2:]
        text = " ".join(line.strip() for line in text_lines if line.strip())

        # 去除说话人标签 [SPEAKER_00]
        text = re.sub(r"^\[.*?\]\s*", "", text)

        if text:
            segments.append({"start": start, "end": end, "text": text})

    return segments


def parse_vtt(filepath: str) -> list[dict]:
    """
    解析 VTT 文件为段落列表

    Args:
        filepath: VTT 文件路径

    Returns:
        段落列表
    """
    content = Path(filepath).read_text(encoding="utf-8")

    # 移除 WEBVTT 头部
    content = re.sub(r"^WEBVTT.*?\n\n", "", content, flags=re.DOTALL)

    segments = []
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")

        # 查找时间戳行
        timestamp_line = None
        text_start_idx = 0

        for i, line in enumerate(lines):
            if "-->" in line:
                timestamp_line = line
                text_start_idx = i + 1
                break

        if not timestamp_line:
            continue

        match = re.match(
            r"(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})",
            timestamp_line,
        )
        if not match:
            continue

        start = parse_timestamp(match.group(1))
        end = parse_timestamp(match.group(2))

        text_lines = lines[text_start_idx:]
        text = " ".join(line.strip() for line in text_lines if line.strip())

        # 去除 VTT 说话人标签 <v Speaker>
        text = re.sub(r"<v\s+.*?>", "", text)

        if text:
            segments.append({"start": start, "end": end, "text": text})

    return segments


def merge_short_segments(
    segments: list[dict], min_chars: int = 10, max_gap: float = 1.0
) -> list[dict]:
    """
    合并过短的段落

    Args:
        segments: 原始段落列表
        min_chars: 最短字符数，低于此值尝试合并
        max_gap: 最大允许间隙（秒），超过则不合并

    Returns:
        合并后的段落列表
    """
    if not segments:
        return []

    merged = [segments[0].copy()]

    for seg in segments[1:]:
        prev = merged[-1]
        gap = seg["start"] - prev["end"]

        # 如果前一段太短且间隙不大，合并
        if len(prev["text"]) < min_chars and gap <= max_gap:
            prev["end"] = seg["end"]
            prev["text"] = prev["text"] + seg["text"]
        else:
            merged.append(seg.copy())

    return merged


def split_long_segments(segments: list[dict], max_chars: int = 200) -> list[dict]:
    """
    拆分过长的段落

    按句号/问号/感叹号等断句符拆分，保持时间戳按比例分配。

    Args:
        segments: 原始段落列表
        max_chars: 最大字符数

    Returns:
        拆分后的段落列表
    """
    result = []

    for seg in segments:
        if len(seg["text"]) <= max_chars:
            result.append(seg)
            continue

        # 按中文句号/问号/感叹号拆分
        sentences = re.split(r"(?<=[。？！.?!])", seg["text"])
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 1:
            # 无法按句号拆分，直接使用
            result.append(seg)
            continue

        # 按字符比例分配时间
        total_chars = sum(len(s) for s in sentences)
        total_duration = seg["end"] - seg["start"]
        current_start = seg["start"]

        for sentence in sentences:
            ratio = len(sentence) / total_chars
            duration = total_duration * ratio

            result.append(
                {
                    "start": current_start,
                    "end": current_start + duration,
                    "text": sentence,
                }
            )
            current_start += duration

    return result


def segments_to_manifest(segments: list[dict]) -> list[TtsSegment]:
    """
    将段落列表转换为 TTS manifest

    Args:
        segments: 段落列表

    Returns:
        TtsSegment 列表
    """
    manifest = []

    for i, seg in enumerate(segments, 1):
        duration = seg["end"] - seg["start"]
        fingerprint = djb2_hash(seg["text"])

        manifest.append(
            TtsSegment(
                id=i,
                text=seg["text"],
                start=round(seg["start"], 3),
                end=round(seg["end"], 3),
                duration=round(duration, 3),
                fingerprint=fingerprint,
                char_count=len(seg["text"]),
            )
        )

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="SRT/VTT → TTS 段落拆分",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--srt", type=str, required=True, help="字幕文件路径 (SRT 或 VTT)")
    parser.add_argument("--output", "-o", type=str, required=True, help="输出 JSON manifest 路径")
    parser.add_argument("--max-chars", type=int, default=200, help="单段最大字符数 (默认 200)")
    parser.add_argument("--min-chars", type=int, default=10, help="单段最小字符数 (默认 10)")
    parser.add_argument("--max-gap", type=float, default=1.0, help="合并间隙阈值/秒 (默认 1.0)")

    args = parser.parse_args()

    # 解析字幕文件
    filepath = args.srt
    ext = Path(filepath).suffix.lower()

    if ext == ".vtt":
        segments = parse_vtt(filepath)
    else:
        segments = parse_srt(filepath)

    if not segments:
        print(f"[错误] 未从 {filepath} 解析到任何字幕段落", file=sys.stderr)
        sys.exit(1)

    print(f"[prepare-tts] 解析到 {len(segments)} 条原始字幕")

    # 合并过短段落
    segments = merge_short_segments(segments, min_chars=args.min_chars, max_gap=args.max_gap)
    print(f"[prepare-tts] 短段合并后: {len(segments)} 条")

    # 拆分过长段落
    segments = split_long_segments(segments, max_chars=args.max_chars)
    print(f"[prepare-tts] 长段拆分后: {len(segments)} 条")

    # 生成 manifest
    manifest = segments_to_manifest(segments)

    # 统计信息
    total_chars = sum(s.char_count for s in manifest)
    total_duration = max(s.end for s in manifest) - min(s.start for s in manifest)
    avg_chars = total_chars / len(manifest) if manifest else 0

    output_data = {
        "meta": {
            "source": str(Path(filepath).name),
            "total_segments": len(manifest),
            "total_chars": total_chars,
            "total_duration_sec": round(total_duration, 2),
            "avg_chars_per_segment": round(avg_chars, 1),
        },
        "segments": [asdict(s) for s in manifest],
    }

    # 写入输出文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[prepare-tts] ✅ Manifest 已生成: {args.output}")
    print(f"[prepare-tts]    总段落: {len(manifest)}, 总字符: {total_chars}, 平均: {avg_chars:.0f} 字/段")


if __name__ == "__main__":
    main()
