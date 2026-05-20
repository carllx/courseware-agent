#!/usr/bin/env python3
"""
使用 Pandoc (md→html) + Playwright (html→pdf) 管线将 Markdown 转换为 PDF。
支持中文、Emoji、代码块高亮、内嵌图片。
"""
import subprocess, sys, os, pathlib, tempfile, shutil

# ─── 配置 ───────────────────────────────────────────
BASE = pathlib.Path(__file__).parent
FILES = [
    ("学生版_AI访谈陪练实操指南.md",        "学生版_AI访谈陪练实操指南.pdf"),
    ("教师版_JTBD访谈陪练终端系统提示词.md", "教师版_JTBD访谈陪练终端系统提示词.pdf"),
]

# 内嵌 CSS：中文字体、代码块样式、打印分页控制
CUSTOM_CSS = """
<style>
  body {
    font-family: "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;
    font-size: 14px;
    line-height: 1.8;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 30px;
    color: #1a1a1a;
  }
  h1 { font-size: 1.8em; border-bottom: 2px solid #333; padding-bottom: 8px; }
  h2 { font-size: 1.4em; margin-top: 1.6em; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
  h3 { font-size: 1.15em; margin-top: 1.2em; }
  blockquote {
    border-left: 4px solid #3b82f6;
    margin: 1em 0;
    padding: 8px 16px;
    background: #f0f6ff;
    color: #1e3a5f;
  }
  code {
    font-family: "Menlo", "SF Mono", "Fira Code", monospace;
    background: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 0.9em;
  }
  pre {
    background: #1e1e2e;
    color: #cdd6f4;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.85em;
    line-height: 1.5;
    page-break-inside: avoid;
  }
  pre code { background: none; color: inherit; padding: 0; }
  img { max-width: 100%; height: auto; }
  hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
  ul, ol { padding-left: 1.8em; }
  li { margin-bottom: 0.3em; }
  @media print {
    body { padding: 0; }
    pre { page-break-inside: avoid; }
    h2, h3 { page-break-after: avoid; }
  }
</style>
"""

def md_to_html(md_path: pathlib.Path) -> str:
    """使用 Pandoc 将 Markdown 转为独立 HTML（内嵌图片资源）。"""
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        tmp_path = tmp.name

    cmd = [
        "pandoc", str(md_path),
        "-o", tmp_path,
        "--standalone", "--embed-resources",
        f"--resource-path={md_path.parent}",
        "--metadata", f"title={md_path.stem}",
        "-V", "lang=zh-CN",
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    html = pathlib.Path(tmp_path).read_text("utf-8")
    os.unlink(tmp_path)

    # 注入自定义 CSS（在 </head> 前插入）
    html = html.replace("</head>", CUSTOM_CSS + "\n</head>")
    return html


def html_to_pdf_playwright(html_content: str, pdf_path: pathlib.Path):
    """使用 Playwright Chromium 将 HTML 打印为 PDF。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("⚠️  playwright 未安装，尝试安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        from playwright.sync_api import sync_playwright

    # 写入临时 HTML 文件
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
        f.write(html_content)
        tmp_html = f.name

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"file://{tmp_html}", wait_until="networkidle")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
                print_background=True,
            )
            browser.close()
    finally:
        os.unlink(tmp_html)


def main():
    for md_name, pdf_name in FILES:
        md_path = BASE / md_name
        pdf_path = BASE / pdf_name

        if not md_path.exists():
            print(f"❌ 文件不存在：{md_path}")
            continue

        print(f"📄 正在处理：{md_name}")
        print(f"   1/2 Pandoc: md → html ...")
        html = md_to_html(md_path)

        print(f"   2/2 Playwright: html → pdf ...")
        html_to_pdf_playwright(html, pdf_path)

        size_kb = pdf_path.stat().st_size / 1024
        print(f"   ✅ 完成：{pdf_name} ({size_kb:.0f} KB)")

    print("\n🎉 全部转换完成！")


if __name__ == "__main__":
    main()
