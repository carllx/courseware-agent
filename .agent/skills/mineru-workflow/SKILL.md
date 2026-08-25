---
name: mineru-workflow
description: Automates PDF to Markdown conversions using the MinerU system, manages batch processing, handles Imgur link replacements, and provides Markdown to EPUB workflows. Use this skill when the user asks to process PDFs, extract text/images from PDFs via MinerU, manage OCR tasks, or convert Markdown documents to EPUB format.
---

# Mineru Workflow

## Overview

This skill provides comprehensive workflows for processing PDFs and images into Markdown using the MinerU system. It handles batch conversion tasks, automated Imgur uploads for local images, Conda environment management for `magic-pdf`, and Pandoc conversions from Markdown to EPUB.

## Pre-Requisite Check

**IMPORTANT:** Before proceeding with ANY Mineru OCR task, you MUST explicitly ask the user:
**"是否需要生成图床 (Imgur) 版本？(默认为否，保留本地图片路径)"**
Wait for the user's confirmation before executing any local or API conversions.

## 1. Quick Start / Single File Processing

If using the local Mineru API (FastAPI backend):
1. **Health Check:** Always `curl http://localhost:8000` to check if the server is alive. If the connection is refused, inform the user they need to start the server (e.g. via `start_mac.command`).
2. Trigger the processing via the API Endpoint (see `references/mineru_api_docs.md`). The backend will automatically handle Imgur uploading if configured.

If using local command line:
1. Use `magic-pdf -p <input.pdf> -o <output_dir>`.

## 2. Batch Processing

For processing multiple PDFs within a directory, utilize the provided batch scripts (do not use default hardcoded paths; always provide exact paths):
- **Windows**: Use `scripts/batch_process_windows.ps1 <folderPath>`
- **macOS/Linux**: Use `scripts/batch_process_mac.sh <input_dir> <output_dir>`

These scripts iterate through the target directory and execute `magic-pdf` on each file. 

## 3. Image Hosting Replacement (Imgur)

If the user requested the Imgur (图床) version, and you are using the local command line (not the API), you MUST run the provided Python script to convert local image links to Imgur links AFTER the OCR process completes:
- `python scripts/convert_local_images.py <path_to_generated_markdown_file>`
This script will parse the Markdown, upload local images to Imgur, and update the links inline.

## 4. Markdown to EPUB Conversion

To convert the generated Markdown files to EPUB format, use the Pandoc workflow:
- Execute `scripts/convert_markdown_to_epub.sh <input.md> <output.epub> [cover_image] [title]`
- This leverages `pandoc` with `--epub3` and the `pandoc-crossref` filter.

## Resources

- **`references/mineru_api_docs.md`**: Contains the full architectural overview, API endpoints, and configuration details for the Mineru Scan System and Imgur integrations.
- **`scripts/convert_local_images.py`**: Python script for parsing a Markdown file, uploading local images to Imgur, and replacing the links.
- **`scripts/batch_process_windows.ps1`**: PowerShell script for batch processing PDFs.
- **`scripts/batch_process_mac.sh`**: Bash/Zsh script for batch processing PDFs on Unix-like systems.
- **`scripts/convert_markdown_to_epub.sh`**: Helper script to convert the OCR'd Markdown into EPUB using Pandoc.
