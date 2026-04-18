#!/usr/bin/env python3
"""
aeneas-ng 转录/对齐桥接脚本

功能：
- 自动检测 aeneas-ng 安装路径并动态加载
- 根据是否提供逐字稿，自动路由到 transcribe() 或 align() 模式
- 支持环境自检模式 (--check-env)

依赖：
- aeneas-ng (通过 sys.path 动态加载)
- stable-ts, faster-whisper, jieba (aeneas-ng 的依赖)

使用示例：
    # 纯转录（无逐字稿）
    python transcribe_video.py --audio lecture.mp3 --output output.srt

    # 对齐（有逐字稿）
    python transcribe_video.py --audio lecture.mp3 --transcript script.md --output output.srt

    # 环境自检
    python transcribe_video.py --check-env
"""
import sys
import argparse
import json
from pathlib import Path

# aeneas-ng 项目路径（硬编码，与 SKILL.md 保持一致）
AENEAS_NG_PATH = "/Users/yamlam/Downloads/aeneas-ng-api"

# 外置硬盘模型路径
EXTERNAL_MODEL_PATH = "/Volumes/T7-carllx2T/pyvideotrans-models"
FALLBACK_MODEL_PATH = str(Path.home() / ".cache" / "aeneas-ng")


def check_environment():
    """
    环境自检：验证所有依赖是否可达

    Returns:
        dict: 各项检查结果
    """
    results = {}

    # 检查 aeneas-ng 可达性
    try:
        sys.path.insert(0, AENEAS_NG_PATH)
        from aligner import Aligner  # noqa: F401
        results["aeneas_ng"] = {"status": "OK", "path": AENEAS_NG_PATH}
    except ImportError as e:
        results["aeneas_ng"] = {"status": "FAIL", "error": str(e)}

    # 检查模型路径
    if Path(EXTERNAL_MODEL_PATH).exists():
        results["model_path"] = {"status": "OK", "path": EXTERNAL_MODEL_PATH}
    else:
        results["model_path"] = {
            "status": "WARN",
            "message": f"外置硬盘未挂载，将回退到 {FALLBACK_MODEL_PATH}",
        }

    # 检查 ffmpeg
    import shutil

    ffmpeg_path = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    if Path(ffmpeg_path).exists():
        results["ffmpeg"] = {"status": "OK", "path": ffmpeg_path}
    else:
        results["ffmpeg"] = {"status": "FAIL", "error": "ffmpeg 未找到"}

    # 检查 Python 依赖
    for pkg in ["stable_whisper", "jieba", "faster_whisper"]:
        try:
            __import__(pkg)
            results[pkg] = {"status": "OK"}
        except ImportError:
            results[pkg] = {"status": "FAIL", "error": f"{pkg} 未安装"}

    return results


def load_aeneas_ng():
    """
    动态加载 aeneas-ng 模块

    Returns:
        Aligner 类
    """
    if AENEAS_NG_PATH not in sys.path:
        sys.path.insert(0, AENEAS_NG_PATH)

    try:
        from aligner import Aligner
        return Aligner
    except ImportError as e:
        print(f"[错误] 无法加载 aeneas-ng: {e}", file=sys.stderr)
        print(f"[提示] 请确认 {AENEAS_NG_PATH} 存在且依赖已安装", file=sys.stderr)
        sys.exit(1)


def clean_transcript(text: str) -> str:
    """
    清洗逐字稿文本，去除 Markdown 标记和元数据

    Args:
        text: 原始逐字稿文本

    Returns:
        清洗后的纯文本
    """
    import re

    lines = text.split("\n")
    cleaned = []

    for line in lines:
        # 跳过 YAML frontmatter
        if line.strip() == "---":
            continue
        # 跳过 Markdown 标题标记（保留文本）
        line = re.sub(r"^#{1,6}\s+", "", line)
        # 跳过 [VISUAL] / [ACTIVITY] 等标记块
        if re.match(r"^\[(?:VISUAL|ACTIVITY|STORY TIME|INSIGHT)\]", line.strip()):
            continue
        # 跳过空行和纯标记行
        if not line.strip():
            continue
        # 跳过 ** 加粗的元数据行（如 **Scene**: ...）
        if re.match(r"^\*\*\w+\*\*\s*[:：]", line.strip()):
            continue

        cleaned.append(line.strip())

    return "\n".join(cleaned)


def run_transcribe(audio: str, lang: str, model: str, output: str, fmt: str):
    """
    纯转录模式：无逐字稿，直接识别

    Args:
        audio: 音频/视频文件路径
        lang: 语言代码
        model: Whisper 模型大小
        output: 输出文件路径
        fmt: 输出格式 (srt/vtt/json)
    """
    Aligner = load_aeneas_ng()

    print(f"[video-tts-localizer] 纯转录模式")
    print(f"[video-tts-localizer] 音频: {audio}")
    print(f"[video-tts-localizer] 语言: {lang}, 模型: {model}")

    aligner = Aligner(model_size=model, language=lang)
    result = aligner.transcribe(audio, language=lang)

    # 按格式输出
    _export_result(result, output, fmt)

    print(f"[video-tts-localizer] ✅ 转录完成: {output}")


def run_align(audio: str, transcript: str, lang: str, model: str, output: str, fmt: str):
    """
    对齐模式：逐字稿 + 音频 → 精确时间戳

    Args:
        audio: 音频/视频文件路径
        transcript: 逐字稿文件路径
        lang: 语言代码
        model: Whisper 模型大小
        output: 输出文件路径
        fmt: 输出格式 (srt/vtt/json)
    """
    Aligner = load_aeneas_ng()

    # 读取并清洗逐字稿
    transcript_path = Path(transcript)
    raw_text = transcript_path.read_text(encoding="utf-8")

    # 如果是 Markdown 文件，清洗标记
    if transcript_path.suffix.lower() in (".md", ".markdown"):
        text = clean_transcript(raw_text)
        print(f"[video-tts-localizer] Markdown 清洗: {len(raw_text)} → {len(text)} 字符")
    else:
        text = raw_text

    print(f"[video-tts-localizer] 对齐模式 (Hybrid Match)")
    print(f"[video-tts-localizer] 音频: {audio}")
    print(f"[video-tts-localizer] 逐字稿: {transcript} ({len(text)} 字符)")

    aligner = Aligner(model_size=model, language=lang)
    result = aligner.align(audio, text, language=lang)

    # 按格式输出
    _export_result(result, output, fmt)

    # 打印热词信息
    if result.detected_hotwords:
        preview = ", ".join(result.detected_hotwords[:10])
        print(f"[video-tts-localizer] 检测到热词: {preview}")

    print(f"[video-tts-localizer] ✅ 对齐完成: {output}")


def _export_result(result, output: str, fmt: str):
    """
    按指定格式导出结果

    Args:
        result: AlignResult 对象
        output: 输出文件路径
        fmt: 输出格式
    """
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "srt":
        result.to_srt(output)
    elif fmt == "vtt":
        result.to_vtt(output)
    elif fmt == "json":
        result.to_json(output)
    else:
        # 根据文件扩展名自动判断
        ext = output_path.suffix.lower()
        if ext == ".vtt":
            result.to_vtt(output)
        elif ext == ".json":
            result.to_json(output)
        else:
            result.to_srt(output)


def main():
    parser = argparse.ArgumentParser(
        description="aeneas-ng 转录/对齐桥接脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 环境自检
  python transcribe_video.py --check-env

  # 纯转录
  python transcribe_video.py --audio lecture.mp3 --output output.srt

  # 对齐
  python transcribe_video.py --audio lecture.mp3 --transcript script.md --output output.srt
        """,
    )

    parser.add_argument("--check-env", action="store_true", help="执行环境自检")
    parser.add_argument("--audio", type=str, help="音频/视频文件路径")
    parser.add_argument("--transcript", type=str, help="逐字稿文件路径 (可选，提供则使用对齐模式)")
    parser.add_argument("--lang", type=str, default="zh", help="语言代码 (zh/en/auto)")
    parser.add_argument(
        "--model", type=str, default="large-v3-turbo", help="Whisper 模型大小"
    )
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument(
        "--format",
        type=str,
        default="auto",
        choices=["srt", "vtt", "json", "auto"],
        help="输出格式",
    )

    args = parser.parse_args()

    # 环境自检模式
    if args.check_env:
        results = check_environment()
        print(json.dumps(results, ensure_ascii=False, indent=2))
        # 如果有任何 FAIL 项，返回非零退出码
        has_fail = any(v.get("status") == "FAIL" for v in results.values())
        sys.exit(1 if has_fail else 0)

    # 正常执行模式
    if not args.audio:
        parser.error("--audio 为必需参数（除非使用 --check-env）")
    if not args.output:
        parser.error("--output 为必需参数")

    if args.transcript:
        run_align(args.audio, args.transcript, args.lang, args.model, args.output, args.format)
    else:
        run_transcribe(args.audio, args.lang, args.model, args.output, args.format)


if __name__ == "__main__":
    main()
