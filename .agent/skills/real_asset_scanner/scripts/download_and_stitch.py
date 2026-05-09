#!/usr/bin/env python3
"""
真实素材批量下载与拼接引擎 (Download & Stitch Engine)

消费 sourcing_checklist.yaml 中用户已确认的 URL，
执行批量下载、多图拼接、命名落盘。

用法:
    python download_and_stitch.py <sourcing_checklist.yaml> [--output-dir <dir>]

输入:
    sourcing_checklist.yaml — 需包含 confirmed_urls 和 stitch_mode 字段

输出:
    - 下载并拼接后的图片文件（按 target_path 落盘）
    - download_report.yaml — 执行报告

依赖: requests, Pillow, PyYAML
"""

import os
import sys
import time
import yaml
import requests
from io import BytesIO
from pathlib import Path
from dataclasses import dataclass, field

try:
    from PIL import Image
except ImportError:
    print("❌ 需要安装 Pillow: pip install Pillow")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}

MAX_RETRIES = 5
BACKOFF_BASE = 1.5   # 指数退避基数（秒）
TIMEOUT = 15          # 请求超时（秒）
JPEG_QUALITY = 90     # JPEG 压缩质量


@dataclass
class DownloadResult:
    """单条下载任务的结果"""
    slide_id: str = ""
    status: str = "pending"       # success / failed / skipped
    output_path: str = ""
    urls_attempted: list = field(default_factory=list)
    urls_failed: list = field(default_factory=list)
    error: str = ""
    stitch_mode: str = "single"


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def download_image(url: str) -> Image.Image | None:
    """
    下载单张图片，支持指数退避重试。
    返回 PIL.Image 对象或 None（全部重试失败）。
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            # 统一转换为 RGB（排除 RGBA/P 等模式的兼容问题）
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')
            return img
        except Exception as e:
            wait = BACKOFF_BASE ** attempt
            if attempt < MAX_RETRIES - 1:
                print(f"    ⚠️  重试 {attempt+1}/{MAX_RETRIES}（{wait:.1f}s 后）: {e}")
                time.sleep(wait)
            else:
                print(f"    ❌ 下载失败: {url} — {e}")
                return None


def stitch_images(images: list[Image.Image], mode: str = "horizontal") -> Image.Image | None:
    """
    将多张图片拼接为一张。
    
    mode:
      - single:     返回第一张（不拼接）
      - horizontal: 水平拼接（等高缩放）
      - vertical:   垂直拼接（等宽缩放）
      - grid:       2×N 网格（等宽等高）
    """
    if not images:
        return None
    if len(images) == 1 or mode == "single":
        return images[0]

    if mode == "horizontal":
        min_height = min(img.height for img in images)
        resized = [
            img.resize(
                (int(img.width * min_height / img.height), min_height),
                Image.Resampling.LANCZOS
            )
            for img in images
        ]
        total_width = sum(img.width for img in resized)
        canvas = Image.new('RGB', (total_width, min_height))
        x = 0
        for img in resized:
            canvas.paste(img, (x, 0))
            x += img.width
        return canvas

    elif mode == "vertical":
        min_width = min(img.width for img in images)
        resized = [
            img.resize(
                (min_width, int(img.height * min_width / img.width)),
                Image.Resampling.LANCZOS
            )
            for img in images
        ]
        total_height = sum(img.height for img in resized)
        canvas = Image.new('RGB', (min_width, total_height))
        y = 0
        for img in resized:
            canvas.paste(img, (0, y))
            y += img.height
        return canvas

    elif mode == "grid":
        # 2列网格
        cols = 2
        cell_w = min(img.width for img in images)
        cell_h = min(img.height for img in images)
        resized = [
            img.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            for img in images
        ]
        rows = (len(resized) + cols - 1) // cols
        canvas = Image.new('RGB', (cell_w * cols, cell_h * rows), (255, 255, 255))
        for i, img in enumerate(resized):
            r, c = divmod(i, cols)
            canvas.paste(img, (c * cell_w, r * cell_h))
        return canvas

    return images[0]


def infer_stitch_mode(layout: str, url_count: int) -> str:
    """根据 Layout 字段和 URL 数量推断拼接模式"""
    if url_count <= 1:
        return "single"

    layout_lower = layout.lower().strip('`')
    if layout_lower in ("comparison",):
        return "horizontal"
    elif layout_lower in ("split",):
        return "vertical"
    elif layout_lower in ("grid",):
        return "grid"
    else:
        # 默认水平拼接
        return "horizontal"


def process_item(item: dict, base_dir: Path) -> DownloadResult:
    """处理单条清单条目"""
    result = DownloadResult(slide_id=item.get("slide", "unknown"))

    # 检查 disposition
    disposition = item.get("disposition", "download")
    if disposition != "download":
        result.status = "skipped"
        result.error = f"disposition={disposition}"
        return result

    # 获取已确认的 URL 列表
    urls = item.get("confirmed_urls", [])
    if not urls:
        result.status = "skipped"
        result.error = "无 confirmed_urls"
        return result

    # 确定目标路径
    target_path = item.get("target_path", "")
    if not target_path:
        result.status = "failed"
        result.error = "无 target_path"
        return result

    # 解析相对路径（相对于 src/ 目录）
    abs_target = (base_dir / target_path).resolve()
    abs_target.parent.mkdir(parents=True, exist_ok=True)

    # 确定拼接模式
    stitch_mode = item.get("stitch_mode", "auto")
    if stitch_mode == "auto":
        layout = item.get("layout", "")
        stitch_mode = infer_stitch_mode(layout, len(urls))
    result.stitch_mode = stitch_mode

    # 下载所有图片
    images = []
    result.urls_attempted = list(urls)
    for url in urls:
        print(f"    📥 下载: {url[:80]}...")
        img = download_image(url)
        if img:
            images.append(img)
        else:
            result.urls_failed.append(url)

    if not images:
        result.status = "failed"
        result.error = "所有 URL 下载失败"
        return result

    # 拼接
    final = stitch_images(images, stitch_mode)
    if not final:
        result.status = "failed"
        result.error = "拼接失败"
        return result

    # 保存（根据目标扩展名选择格式）
    ext = abs_target.suffix.lower()
    if ext in ('.jpg', '.jpeg'):
        final.save(str(abs_target), "JPEG", quality=JPEG_QUALITY)
    elif ext == '.png':
        final.save(str(abs_target), "PNG")
    elif ext == '.webp':
        final.save(str(abs_target), "WEBP", quality=JPEG_QUALITY)
    else:
        # 默认 JPEG
        abs_target = abs_target.with_suffix('.jpg')
        final.save(str(abs_target), "JPEG", quality=JPEG_QUALITY)

    result.status = "success"
    result.output_path = str(abs_target)
    print(f"    ✅ 已保存: {abs_target.name} ({final.width}×{final.height})")

    return result


# ═══════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法: python download_and_stitch.py <sourcing_checklist.yaml> [--output-dir <dir>]")
        sys.exit(1)

    checklist_path = Path(sys.argv[1])
    if not checklist_path.exists():
        print(f"❌ 文件不存在: {checklist_path}")
        sys.exit(1)

    # 基准目录（清单文件通常在 src/ 下）
    base_dir = checklist_path.parent

    # 可选：覆盖输出目录
    if "--output-dir" in sys.argv:
        idx = sys.argv.index("--output-dir")
        if idx + 1 < len(sys.argv):
            base_dir = Path(sys.argv[idx + 1])

    # 加载清单
    with open(checklist_path, 'r', encoding='utf-8') as f:
        items = yaml.safe_load(f) or []

    # 仅处理 disposition=download 且有 confirmed_urls 的条目
    download_items = [
        it for it in items
        if it.get("disposition", "download") == "download"
        and it.get("confirmed_urls")
    ]

    print(f"\n🔍 加载清单: {checklist_path.name}")
    print(f"   总条目: {len(items)} | 待下载: {len(download_items)}")
    print(f"   基准目录: {base_dir}\n")

    results = []
    for i, item in enumerate(download_items, 1):
        slide_id = item.get("slide", "?")
        print(f"[{i}/{len(download_items)}] 处理 {slide_id}...")
        result = process_item(item, base_dir)
        results.append(result)

    # 输出报告
    report_path = checklist_path.parent / "download_report.yaml"
    report_data = []
    for r in results:
        report_data.append({
            "slide": r.slide_id,
            "status": r.status,
            "output_path": r.output_path,
            "stitch_mode": r.stitch_mode,
            "urls_failed": r.urls_failed,
            "error": r.error,
        })

    with open(report_path, 'w', encoding='utf-8') as f:
        yaml.dump(report_data, f, allow_unicode=True, default_flow_style=False)

    # 统计
    success = sum(1 for r in results if r.status == "success")
    failed = sum(1 for r in results if r.status == "failed")
    skipped = sum(1 for r in results if r.status == "skipped")

    print(f"\n{'='*40}")
    print(f"  📊 下载报告")
    print(f"{'='*40}")
    print(f"  ✅ 成功: {success}")
    print(f"  ❌ 失败: {failed}")
    print(f"  ⏭️  跳过: {skipped}")
    print(f"  📄 报告: {report_path}")


if __name__ == "__main__":
    main()
