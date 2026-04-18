#!/usr/bin/env python3
"""
TTS 音频片段拼接 + 视频混流脚本

功能：
- 读取 TTS manifest（由 prepare_tts_segments.py 生成）
- 按时间轴拼接 TTS 音频片段，用静音填充间隙
- 可选：与原始视频混流输出最终产物
- 可选：调用 aeneas-ng align() 进行二次校准

依赖：
- ffmpeg (音频拼接和视频混流)
- pydub (音频操作，可选)

使用示例：
    # 纯音频拼接
    python merge_tts_audio.py --manifest manifest.json --tts-dir ./tts/ --output merged.aac

    # 与视频混流 (WebM 输出)
    python merge_tts_audio.py --manifest manifest.json --tts-dir ./tts/ --video original.mp4 --output final.webm

    # 与视频混流 (MP4 输出)
    python merge_tts_audio.py --manifest manifest.json --tts-dir ./tts/ --video original.mp4 --output final.mp4
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# ffmpeg 路径
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"


def get_audio_duration(filepath: str) -> float:
    """
    获取音频文件时长（秒）

    Args:
        filepath: 音频文件路径

    Returns:
        时长（秒）
    """
    cmd = [
        FFPROBE,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        filepath,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return 0.0


def generate_silence(duration: float, output: str, sample_rate: int = 44100):
    """
    生成指定时长的静音音频文件

    Args:
        duration: 时长（秒）
        output: 输出文件路径
        sample_rate: 采样率
    """
    cmd = [
        FFMPEG,
        "-f", "lavfi",
        "-i", f"anullsrc=r={sample_rate}:cl=mono",
        "-t", str(duration),
        "-c:a", "aac",
        "-b:a", "64k",
        "-y", output,
    ]

    subprocess.run(cmd, capture_output=True, check=True)


def build_concat_list(
    manifest_data: dict, tts_dir: str, temp_dir: str
) -> tuple[list[str], float]:
    """
    构建 ffmpeg concat 列表，按时间轴排列 TTS 片段和静音间隙

    Args:
        manifest_data: TTS manifest 数据
        tts_dir: TTS 音频片段目录
        temp_dir: 临时文件目录

    Returns:
        (片段文件路径列表, 总时长)
    """
    segments = manifest_data["segments"]
    pieces = []  # 最终的音频片段列表（按时间顺序）
    current_time = 0.0

    for seg in segments:
        seg_start = seg["start"]
        fingerprint = seg["fingerprint"]

        # 查找对应的 TTS 音频文件
        tts_file = None
        tts_path = Path(tts_dir)

        # 尝试多种命名模式
        candidates = [
            tts_path / f"{fingerprint}.aac",
            tts_path / f"{fingerprint}.mp3",
            tts_path / f"{fingerprint}.wav",
            tts_path / f"seg_{seg['id']:04d}.aac",
            tts_path / f"seg_{seg['id']:04d}.mp3",
        ]

        for candidate in candidates:
            if candidate.exists():
                tts_file = str(candidate)
                break

        if not tts_file:
            print(f"[警告] 段落 {seg['id']} 的 TTS 音频未找到 (指纹: {fingerprint}), 跳过")
            continue

        # 如果与上一段之间有间隙，插入静音
        gap = seg_start - current_time
        if gap > 0.05:  # 间隙 > 50ms 才插入静音
            silence_file = str(Path(temp_dir) / f"silence_{seg['id']}.aac")
            generate_silence(gap, silence_file)
            pieces.append(silence_file)
            current_time += gap

        # 添加 TTS 音频
        pieces.append(tts_file)
        tts_duration = get_audio_duration(tts_file)
        current_time += tts_duration

    return pieces, current_time


def concat_audio(pieces: list[str], output: str, temp_dir: str):
    """
    使用 ffmpeg concat 协议拼接音频文件

    Args:
        pieces: 音频片段路径列表
        output: 输出文件路径
        temp_dir: 临时文件目录
    """
    if not pieces:
        print("[错误] 无可用音频片段", file=sys.stderr)
        sys.exit(1)

    # 创建 concat 列表文件
    concat_list = Path(temp_dir) / "concat_list.txt"
    with open(concat_list, "w") as f:
        for piece in pieces:
            # ffmpeg concat 格式要求转义单引号
            escaped = str(Path(piece).resolve()).replace("'", "'\\''")
            f.write(f"file '{escaped}'\n")

    # 执行拼接
    cmd = [
        FFMPEG,
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "aac",
        "-b:a", "128k",
        "-y", output,
    ]

    subprocess.run(cmd, capture_output=True, check=True)


def mux_video_audio(video: str, audio: str, output: str):
    """
    将音频混流到视频中

    根据输出文件扩展名自动选择编码：
    - .webm → VP9 + Opus
    - .mp4 → H.264 + AAC (copy)

    Args:
        video: 原始视频文件路径
        audio: 合成的音频文件路径
        output: 最终输出路径
    """
    output_ext = Path(output).suffix.lower()

    if output_ext == ".webm":
        cmd = [
            FFMPEG,
            "-i", video,
            "-i", audio,
            "-map", "0:v:0",  # 取视频流
            "-map", "1:a:0",  # 取新音频流
            "-c:v", "libvpx-vp9", "-crf", "35", "-b:v", "0",
            "-row-mt", "1", "-cpu-used", "4",
            "-c:a", "libopus", "-b:a", "64k",
            "-y", output,
        ]
    else:
        # MP4 输出
        cmd = [
            FFMPEG,
            "-i", video,
            "-i", audio,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",  # 视频流直接复制（不重新编码）
            "-c:a", "aac", "-b:a", "128k",
            "-y", output,
        ]

    print(f"[merge-tts] 混流中: {output}")
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="TTS 音频片段拼接 + 视频混流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--manifest", type=str, required=True, help="TTS manifest JSON 文件路径"
    )
    parser.add_argument(
        "--tts-dir", type=str, required=True, help="TTS 音频片段目录"
    )
    parser.add_argument(
        "--video", type=str, help="原始视频文件 (可选，提供则执行混流)"
    )
    parser.add_argument(
        "--output", "-o", type=str, required=True, help="输出文件路径"
    )

    args = parser.parse_args()

    # 读取 manifest
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"[错误] Manifest 文件不存在: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    meta = manifest_data.get("meta", {})

    print(f"[merge-tts] 加载 manifest: {meta.get('total_segments', '?')} 段")
    print(f"[merge-tts] TTS 目录: {args.tts_dir}")

    with tempfile.TemporaryDirectory(prefix="video-tts-") as temp_dir:
        # 构建拼接列表
        pieces, total_duration = build_concat_list(manifest_data, args.tts_dir, temp_dir)
        print(f"[merge-tts] 拼接片段: {len(pieces)} 个, 预估时长: {total_duration:.1f}s")

        if args.video:
            # 模式 1: 拼接音频 → 混流到视频
            merged_audio = str(Path(temp_dir) / "merged_audio.aac")
            concat_audio(pieces, merged_audio, temp_dir)
            mux_video_audio(args.video, merged_audio, args.output)
        else:
            # 模式 2: 仅拼接音频
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            concat_audio(pieces, args.output, temp_dir)

    # 验证输出
    output_path = Path(args.output)
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        duration = get_audio_duration(args.output)
        print(f"[merge-tts] ✅ 输出完成: {args.output}")
        print(f"[merge-tts]    体积: {size_mb:.1f} MB, 时长: {duration:.1f}s")
    else:
        print(f"[merge-tts] ❌ 输出失败: 文件未生成", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
