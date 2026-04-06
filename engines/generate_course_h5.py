#!/usr/bin/env python3
"""
generate_course_h5.py — 通用 H5 课件预览生成器 (Workspace 级) v2.0

支持两种模式:
  1. 单讲模式（向后兼容）:
     python engines/generate_course_h5.py <课程目录> <脚本相对路径>

  2. 全量模式 (扫描指定课程或全工作区所有内容生成 manifest):
     python engines/generate_course_h5.py <课程目录> --all
     python engines/generate_course_h5.py --all   (扫描 workspace 所有课程)

输出:
  - 单讲模式: <课程>/build/h5_preview/public/slides.json（兼容旧版）
  - 全量模式: build/h5_preview/public/courses/<courseId>/W01.json ...
              build/h5_preview/public/courses/manifest.json
"""

import sys
import json
import re
import shutil
import glob
import subprocess
from pathlib import Path
from datetime import datetime

# --- 路径设置 ---
CWD = Path.cwd()

PARSER_DIR = CWD / ".agent" / "skills" / "validation_suite" / "scripts"
sys.path.insert(0, str(PARSER_DIR))

from script_parser import parse_script, BlockType, ScriptBlock  # noqa: E402

H5_TEMPLATE_DIR = CWD / "engines" / "h5_template"


# ============================================================
# 主题加载（保持不变）
# ============================================================

def _hex_to_rgb(hex_color: str) -> str:
    """将 #RRGGBB 转为 'R, G, B' 字符串。"""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return "128, 128, 128"
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _is_dark_theme(bg_hex: str) -> bool:
    """根据 bg_base 亮度判断是否为暗色主题。"""
    h = bg_hex.lstrip("#")
    if len(h) != 6:
        return False
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    hsp = (0.299 * r * r + 0.587 * g * g + 0.114 * b * b) ** 0.5
    return hsp < 127.5


def _build_theme(palette: dict, typo: dict) -> dict:
    """从 palette/typography 构建完整主题字典。"""
    primary = palette.get("primary", "#B85042")
    secondary = palette.get("secondary", "#5B7B6F")
    bg_base = palette.get("bg_base", palette.get("canvas", "#F5F0EB"))

    return {
        "bg": bg_base,
        "bgSurface": palette.get("bg_surface", palette.get("card", "#FFFFFF")),
        "bgElevated": palette.get("bg_elevated", palette.get("section_bg", "#EDE7E0")),
        "bgDark": palette.get("bg_dark", palette.get("cover_bg", "#2D2926")),
        "primary": primary,
        "secondary": secondary,
        "accent": palette.get("tertiary", palette.get("accent", "#C9A96E")),
        "info": palette.get("info", "#6B8FAD"),
        "textOnDark": palette.get("text_on_dark", bg_base),
        "primaryLight": palette.get("primary_light", primary),
        "primaryMuted": palette.get("primary_muted", "#8C3A30"),
        "success": palette.get("success", secondary),
        "warning": palette.get("warning", palette.get("tertiary", "#C9A96E")),
        "error": palette.get("error", primary),
        "border": palette.get("border", "#D6CFC7"),
        "text": palette.get("text_main", palette.get("text_primary", "#2D2926")),
        "textSecondary": palette.get("text_secondary", "#6B635C"),
        "textMuted": palette.get("text_muted", "#A39B93"),
        "primaryRgb": _hex_to_rgb(primary),
        "secondaryRgb": _hex_to_rgb(secondary),
        "isDark": _is_dark_theme(bg_base),
        "fontTitle": typo.get("font_en_display", typo.get("heading_font", "Playfair Display")),
        "fontBody": typo.get("font_en_body", typo.get("body_font", "Inter")),
        "fontTitleCn": typo.get("font_cn_display", typo.get("heading_font_cn", "Noto Serif SC")),
        "fontBodyCn": typo.get("font_cn_body", typo.get("body_font_cn", "Noto Sans SC")),
    }


def load_theme(course_path: Path) -> dict:
    """从 course.yaml 解析引用或从 visual_system.yaml 加载主题色。"""
    import yaml

    # 1. 尝试从 course.yaml 中读取 @theme 引用
    course_yaml_path = course_path / "course.yaml"
    if course_yaml_path.exists():
        try:
            course_config = yaml.safe_load(course_yaml_path.read_text(encoding="utf-8"))
            theme_ref = course_config.get("agent", {}).get("standards", {}).get("visual_system", "")
            if theme_ref.startswith("@theme:"):
                theme_name = theme_ref.replace("@theme:", "")
                # 解析全局主题库路径
                global_theme_path = CWD / ".agent" / "styles" / f"theme_{theme_name}.yaml"
                if global_theme_path.exists():
                    raw = yaml.safe_load(global_theme_path.read_text(encoding="utf-8"))
                    palette = raw.get("palette", raw.get("color_system", {}).get("palette", {}))
                    typo = raw.get("typography", {})
                    return _build_theme(palette, typo)
        except Exception as e:
            print(f"Warning: Failed to parse course.yaml for theme reference: {e}")

    # 2. 兼容旧有局部查询路径
    search_paths = [
        course_path / "visual_system.yaml",
        course_path / "styles" / "visual_system.yaml",
    ]

    for p in search_paths:
        if p.exists():
            raw = yaml.safe_load(p.read_text(encoding="utf-8"))
            palette = raw.get("palette", raw.get("color_system", {}).get("palette", {}))
            typo = raw.get("typography", {})
            return _build_theme(palette, typo)

    return _build_theme({}, {})


# ============================================================
# 源映射：compiled.md → 源文件行号回馈
# ============================================================

def _build_source_map(compiled_path: Path) -> list[dict]:
    """解析 compiled.md 中的 BEGIN/END 标记，构建源文件映射表。

    返回:
        [{"src_rel": "src/M01_xxx.md", "src_abs": Path, "compiled_start": int, "compiled_end": int}, ...]
        按 compiled_start 升序排列。
    """
    if not compiled_path.exists():
        return []

    week_dir = compiled_path.parent.parent  # .build/ 的父目录即教学周目录
    lines = compiled_path.read_text(encoding="utf-8").splitlines()
    source_map = []
    current_entry = None

    for i, line in enumerate(lines, 1):  # 1-indexed
        begin_m = re.match(r'^<!-- ### BEGIN (.+?) ### -->$', line)
        if begin_m:
            rel_path = begin_m.group(1).strip()
            current_entry = {
                "src_rel": rel_path,
                "src_abs": (week_dir / rel_path).resolve(),
                "compiled_start": i + 1,  # BEGIN 标记本身不含内容，下一行才是
            }
            continue
        end_m = re.match(r'^<!-- ### END (.+?) ### -->$', line)
        if end_m and current_entry:
            current_entry["compiled_end"] = i - 1  # END 标记前一行
            source_map.append(current_entry)
            current_entry = None

    return source_map


def _apply_source_map(manifest: dict, source_map: list[dict]) -> None:
    """后处理：将 manifest 中所有段落的 srcPath/srcLStart/srcLEnd 从
    compiled.md 行号回馈为源 M0X.md 文件的真实路径和行号。

    直接原地修改 manifest，无返回值。
    """
    for section in manifest.get("sections", []):
        for para in section.get("paragraphs", []):
            ls = para.get("srcLStart")
            le = para.get("srcLEnd")
            if ls is None:
                continue
            for entry in source_map:
                if entry["compiled_start"] <= ls <= entry["compiled_end"]:
                    offset = entry["compiled_start"] - 1
                    para["srcPath"] = str(entry["src_abs"])
                    para["srcLStart"] = ls - offset
                    para["srcLEnd"] = le - offset
                    break


# ============================================================
# ScriptBlock → slides.json 转化
# ============================================================

def extract_visual_list(visual_block: ScriptBlock) -> list:
    """从 VISUAL 块的原始内容中提取 List 字段。"""
    items = []
    content = visual_block.content
    in_list = False
    for line in content.split("\n"):
        line_s = line.strip()
        if "**List**:" in line_s:
            after = line_s.split("**List**:")[-1].strip()
            if after:
                items = [x.strip() for x in after.split("/") if x.strip()]
                return items
            in_list = True
            continue
        if in_list:
            if line_s.startswith("**") and "**:" in line_s:
                in_list = False
                continue
            m = re.match(r"^[\*\-\+]\s+(.*)", line_s)
            if m:
                inner_text = m.group(1).strip()
                if inner_text.startswith("**") and "**:" in inner_text:
                    in_list = False
                    continue
                items.append(inner_text)
            elif line_s and not line_s.startswith("**"):
                pass
            else:
                in_list = False
    return items


def clean_speech_text(text: str) -> str:
    """清洗演讲稿文本。"""
    text = re.sub(r"\*?\*?\(Pause:.*?\)\*?\*?", "", text)
    text = re.sub(r"（讲师口述）[：:]?", "", text)
    # 过滤 HTML 注释行（BUDGET / STATUS 等元数据注释）
    text = re.sub(r'^\s*<!--.*?-->\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_scqa_role(tag_name: str, activity_type: str = None) -> str:
    """根据 tag_name 和 activity_type 推断当前段落的 SCQA 角色。"""
    if not tag_name:
        return "none"
    t = tag_name.upper()
    if t == "LIFE CONNECT": return "s"
    if t in ["CASE STUDY", "WARNING", "STORY TIME", "DID YOU KNOW", "!WARNING", "!CAUTION", "!IMPORTANT"]: return "c"
    if t in ["PACING", "QA"]: return "q"
    if t == "ACTIVITY" and activity_type in ["QA", "Quiz", "Warm-up", "Discussion"]: return "q"
    if t in ["TECH NOTE", "PHILOSOPHY", "TEACHING MOMENT", "NOTE", "!NOTE", "!TIP", "ACTIVITY"]: return "a"
    return "none"


def _compute_tts_fingerprint(text: str) -> str:
    """计算 TTS 段落指纹（DJB2 hash，与前端 fingerprint.js 算法一致）。

    基于完整文本内容（标准化空白后），8 位十六进制。
    """
    if not text:
        return '00000000'
    normalized = ' '.join(text.strip().split())
    if not normalized:
        return '00000000'
    h = 5381
    for ch in normalized:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    # V-04: 附加文本长度，增强抗碰撞性（hash_len 格式）
    return f"{h:08x}_{len(normalized)}"


# 中文字符正则（与 validate_script_length.py 保持一致）
_RE_CN_CHAR = re.compile(r'[\u4e00-\u9fff]')
# BUDGET 注释正则
_RE_BUDGET = re.compile(r'<!--\s*BUDGET:\s*(\d+)\s*chars')


def _count_cn_chars(text: str) -> int:
    """统计文本中的中文字数（与验证器使用相同算法）。"""
    return len(_RE_CN_CHAR.findall(text))


# ============================================================
# ARC-01: 模块层级构建 (modules + subSections)
# ============================================================

# 模块色相调色板（黄金角旋转，确保相邻模块最大感知区分度）
_MODULE_HUES = [210, 35, 150, 280, 330, 50, 190, 100]

# 模块图标推断规则
_MODULE_ICON_PATTERNS = [
    (r'课前|准备|Warm.?up|Pre.?class|Introduction', '🧰'),
    (r'课后|作业|任务|Assignment|Homework', '📋'),
    (r'Checklist|验证|Review|复习|自检', '✅'),
    (r'实验|Lab|Workshop|实践|实战', '🔬'),
    (r'案例|Case|Project|项目|设计', '🎯'),
    (r'练习|Exercise|Practice|活动', '✏️'),
]


def _infer_module_icon(title: str) -> str:
    """根据模块标题关键词推断语义图标。"""
    for pattern, icon in _MODULE_ICON_PATTERNS:
        if re.search(pattern, title, re.IGNORECASE):
            return icon
    return '📖'


def _truncate_module_title(text: str, max_len: int = 12) -> str:
    """截断模块标题，去除 'Module N:' 前缀后保留核心语义。"""
    cleaned = re.sub(r'^Module\s*\d+\s*[:：]\s*', '', text)
    # 去除时长标注 (XX 分钟)
    cleaned = re.sub(r'\s*\(\d+\s*分钟\)\s*$', '', cleaned)
    if len(cleaned) > max_len:
        return cleaned[:max_len] + '…'
    return cleaned


def _build_modules_layer(manifest: dict) -> None:
    """后处理：从扁平 sections 构建 modules 层级元数据（原地修改）。

    向后兼容：sections[] 保持不变，modules[] 为新增可选字段。
    前端通过 manifest.modules?.length > 0 判断是否启用层级导航。
    """
    modules = []
    prev_title = None

    for idx, section in enumerate(manifest["sections"]):
        section["moduleIdx"] = idx

        # 推断过渡提示（语义编码线索）
        transition = None
        if prev_title and idx > 0:
            prev_short = _truncate_module_title(prev_title)
            curr_short = _truncate_module_title(section["title"])
            transition = f"从「{prev_short}」到「{curr_short}」"

        modules.append({
            "id": f"M{idx}",
            "title": section["title"],
            "colorHue": _MODULE_HUES[idx % len(_MODULE_HUES)],
            "heroIcon": _infer_module_icon(section["title"]),
            "transitionHint": transition,
            "sectionId": section["id"],
            "subSectionCount": len(section.get("subSections", [])),
        })
        prev_title = section["title"]

    manifest["modules"] = modules


def _enrich_section_stats(section: dict) -> None:
    """为 section 注入口述字数统计（原地修改）。

    仅统计 type 为 speech 或 oral_tag 类型的段落，
    与 validate_script_length.py 的统计口径一致。
    """
    oral_types = {"speech"}  # speech 类型包括普通口述和 oral_tag
    # oral_tag 在 generate 中被映射为 tag_name.lower()，如 story_time, case_study
    # 它们都不是 tech_note / activity，所以用排除法更稳健
    exclude_types = {"activity", "tech_note"}

    oral_char_count = 0
    for para in section.get("paragraphs", []):
        if para.get("type") not in exclude_types:
            oral_char_count += _count_cn_chars(para.get("text", ""))

    section["oralCharCount"] = oral_char_count
    section["estimatedMinutes"] = round(oral_char_count / 180, 1)

    budget = section.get("budgetChars")
    if budget and budget > 0:
        section["fillRatio"] = round(oral_char_count / budget, 2)
    else:
        section["fillRatio"] = None


def find_image(course_path: Path, asset_field: str) -> str | None:
    """查找视觉素材文件，返回相对路径或 None。
    
    支持三种架构：
    - 旧架构: visuals/assets/W0X_Name/S00.png
    - 新架构 (weeks/): assets/slides/S00.png (相对于教学周目录)
    - V5 架构 (weeks/): public/slides/S00.png (相对于教学周目录)
    """
    if not asset_field:
        return None
    # 兼容 Markdown 图片语法 ![alt](path) 及链接语法 [text](path)
    md_match = re.match(r'!?\[.*?\]\((.+?)\)', asset_field)
    if md_match:
        asset_field = md_match.group(1)
    # 规范化相对路径（去除 ../../ 等前缀）
    asset_field = re.sub(r'^(\.\./)+', '', asset_field)
    full_path = course_path / asset_field
    if full_path.exists():
        mapped = asset_field.replace("visuals/assets/", "visuals/", 1)
        return mapped
    # V5 架构：在 weeks/*/public/ 下搜索
    if asset_field.startswith("public/"):
        for week_dir in sorted((course_path / "weeks").glob("W*")):
            candidate = week_dir / asset_field
            if candidate.exists():
                rel = candidate.relative_to(course_path)
                return str(rel)
    # 新架构：在 weeks/*/assets/ 下搜索
    if asset_field.startswith("assets/"):
        for week_dir in sorted((course_path / "weeks").glob("W*")):
            candidate = week_dir / asset_field
            if candidate.exists():
                rel = candidate.relative_to(course_path)
                return str(rel)
    # 旧架构 fallback
    alt_path = course_path / "visuals" / "assets" / Path(asset_field).name
    if alt_path.exists():
        return f"visuals/{Path(asset_field).name}"
    # 最终 fallback：按文件名在 weeks/ 下搜索
    if (course_path / "weeks").exists():
        for found in (course_path / "weeks").rglob(Path(asset_field).name):
            if found.is_file():
                return str(found.relative_to(course_path))
    return None


def blocks_to_h5_json(
    blocks: list[ScriptBlock],
    course_name: str,
    script_name: str,
    course_path: Path,
    theme: dict,
    script_file_path: Path,
) -> dict:
    """将 ScriptBlock 列表转化为 H5 预览 JSON。

    纯渲染职责，不处理源映射。源映射由 _apply_source_map() 后处理完成。
    v2.1: 增加 oralCharCount / budgetChars / fillRatio / estimatedMinutes 注入。
    """

    # 读取原始文件行，用于解析 BUDGET 注释
    # （BUDGET 注释位于 ## 标题行的下一行，解析器不会将其捕获为 block）
    try:
        _raw_lines = script_file_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        _raw_lines = []

    # TTS 路径：新架构 build/tts/ 优先，旧架构 tts/ fallback
    tts_dir = course_path / "build" / "tts"
    if not tts_dir.exists():
        tts_dir = course_path / "tts"
    audio_path = tts_dir / "audio" / f"{script_name}.mp3"
    if not audio_path.exists():
        audio_path = tts_dir / "audio" / f"{script_name}_blind.mp3"
    srt_path = tts_dir / "srt" / f"{script_name}.srt"

    media = {
        "audio": f"tts/audio/{audio_path.name}" if audio_path.exists() else None,
        "srt": f"tts/srt/{script_name}.srt" if srt_path.exists() else None,
    }

    manifest = {
        "version": "2.1",
        "generated": datetime.now().isoformat(),
        "course": course_name,
        "dirName": course_path.name,   # V-01 fix: 物理目录名 — SSG 用此字段做路径寻址
        "script": script_name,
        "theme": theme,
        "media": media,
        "sections": [],
    }

    current_section = None
    current_slide = None
    last_heading = ""
    speech_counter = 0
    current_subsections = []  # ARC-01: 追踪 H3 级别的子节

    for block in blocks:
        if block.block_type == BlockType.HEADER:
            level = block.metadata.get("level", 1)
            if level == 2:
                if current_section:
                    # ARC-01: 保存当前 section 的子节列表
                    current_section["subSections"] = current_subsections
                    current_subsections = []
                    _enrich_section_stats(current_section)
                    manifest["sections"].append(current_section)
                section_id = f"mod-{len(manifest['sections']) + 1}"

                # 解析标题行后的 BUDGET 注释
                budget_chars = None
                header_line_idx = block.line_start - 1  # 0-indexed
                # 向后扫描最多 3 行寻找 BUDGET 注释
                for offset in range(1, 4):
                    peek_idx = header_line_idx + offset
                    if peek_idx < len(_raw_lines):
                        bm = _RE_BUDGET.search(_raw_lines[peek_idx])
                        if bm:
                            budget_chars = int(bm.group(1))
                            break
                        # 遇到非注释/非空行则停止搜索
                        stripped = _raw_lines[peek_idx].strip()
                        if stripped and not stripped.startswith("<!--"):
                            break

                current_section = {
                    "id": section_id,
                    "title": block.content,
                    "slides": [],
                    "paragraphs": [],
                    "firstSrtCueIdx": None,
                    "budgetChars": budget_chars,
                }
                current_slide = None
                last_heading = ""
            elif level == 3:
                last_heading = block.content
                # ARC-01: 记录 H3 子节边界（用于前端细粒度导航）
                if current_section is not None:
                    current_subsections.append({
                        "id": f"sub-{len(current_subsections) + 1}",
                        "title": block.content,
                        "startParagraph": len(current_section["paragraphs"]),
                        "startSlide": len(current_section["slides"]),
                    })
            continue

        if current_section is None:
            current_section = {
                "id": "mod-0",
                "title": script_name,
                "slides": [],
                "paragraphs": [],
                "firstSrtCueIdx": None,
            }

        if block.block_type == BlockType.VISUAL:
            meta = block.metadata
            slide_id = meta.get("slide_id", f"slide-{len(current_section['slides']) + 1}")
            layout = meta.get("layout", "Image")
            scene = meta.get("scene", "")
            text_val = meta.get("text", "")

            # 多资产支持：优先使用 assets[] 数组，回退到单 asset
            asset_list = meta.get("assets", [])
            if not asset_list and meta.get("asset"):
                asset_list = [meta["asset"]]

            # 解析所有图片路径
            images = [find_image(course_path, a) for a in asset_list]
            images = [img for img in images if img]  # 过滤 None

            slide_list = extract_visual_list(block)

            current_slide = {
                "id": slide_id,
                "layout": layout,
                "text": text_val,
                "heading": last_heading or "",
                "scene": scene,
                "image": images[0] if images else None,      # 向后兼容
                "images": images,                              # 新字段：全部图片
                "assetExpected": asset_list or None,
                "list": slide_list if slide_list else None,
                "paragraphStart": len(current_section["paragraphs"]),
            }
            current_section["slides"].append(current_slide)
            last_heading = ""
            continue

        if block.block_type == BlockType.SPEECH:
            text = clean_speech_text(block.content)
            if not text:
                continue

            tag_name = block.metadata.get("tag_name", None)
            is_oral = block.metadata.get("oral_tag", False)
            para_type = tag_name.lower().replace(" ", "_") if is_oral and tag_name else "speech"

            cue_idx = speech_counter
            speech_counter += 1

            if current_section["firstSrtCueIdx"] is None:
                current_section["firstSrtCueIdx"] = cue_idx

            current_section["paragraphs"].append({
                "type": para_type,
                "tag": tag_name,
                "scqaRole": get_scqa_role(tag_name),
                "text": text,
                "ttsFp": _compute_tts_fingerprint(text),
                "srtCueIdx": cue_idx,
                "srcPath": str(script_file_path.resolve()),
                "srcLStart": block.line_start,
                "srcLEnd": block.line_end,
            })
            continue

        if block.block_type == BlockType.ACTIVITY:
            meta = block.metadata
            activity_type = meta.get("activity_type", "Practice")
            current_section["paragraphs"].append({
                "type": "activity",
                "tag": "ACTIVITY",
                "scqaRole": get_scqa_role("ACTIVITY", activity_type),
                "activityType": activity_type,
                "duration": meta.get("duration_raw", ""),
                "desc": meta.get("desc", ""),
                "text": block.content,
                "ttsFp": "00000000",
                "srtCueIdx": None,
                "srcPath": str(script_file_path.resolve()),
                "srcLStart": block.line_start,
                "srcLEnd": block.line_end,
            })
            continue

        if block.block_type == BlockType.TAG:
            tag_name = block.metadata.get("tag_name", "NOTE")
            current_section["paragraphs"].append({
                "type": "tech_note",
                "tag": tag_name,
                "scqaRole": get_scqa_role(tag_name),
                "text": block.content,
                "ttsFp": "00000000",
                "srtCueIdx": None,
                "srcPath": str(script_file_path.resolve()),
                "srcLStart": block.line_start,
                "srcLEnd": block.line_end,
            })
            continue

    if current_section:
        # ARC-01: 保存最后一个 section 的子节列表
        current_section["subSections"] = current_subsections
        _enrich_section_stats(current_section)
        manifest["sections"].append(current_section)

    # ARC-01: 构建 modules 层级元数据
    _build_modules_layer(manifest)

    return manifest


# ============================================================
# H5 模板实例化
# ============================================================

_SYNC_EXCLUDE = {"node_modules", ".DS_Store", "package-lock.json"}
_SYNC_PROTECT_PUBLIC = {"slides.json", "visuals", "tts", "courses"}


def _sync_template_to_instance(h5_dir: Path):
    """增量同步：对比模板与实例的文件修改时间。"""
    updated = 0
    for src in H5_TEMPLATE_DIR.rglob("*"):
        if any(part in _SYNC_EXCLUDE for part in src.parts):
            continue
        rel = src.relative_to(H5_TEMPLATE_DIR)
        if rel.parts[0] == "public" and len(rel.parts) > 1 and rel.parts[1] in _SYNC_PROTECT_PUBLIC:
            continue
        dest = h5_dir / rel
        if src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue
        if dest.exists() and src.stat().st_mtime <= dest.stat().st_mtime:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        updated += 1
    if updated:
        print(f"   🔄 同步 {updated} 个更新文件")


def ensure_h5_instance(target_dir: Path) -> Path:
    """确保目标目录下有 h5_preview 实例。"""
    h5_dir = target_dir / "build" / "h5_preview"

    if not H5_TEMPLATE_DIR.exists():
        print(f"❌ H5 模板目录不存在: {H5_TEMPLATE_DIR}")
        sys.exit(1)

    if h5_dir.exists() and (h5_dir / "package.json").exists():
        _sync_template_to_instance(h5_dir)
        return h5_dir

    print(f"📦 初始化 H5 预览实例: {h5_dir.relative_to(CWD)}")
    h5_dir.mkdir(parents=True, exist_ok=True)

    for item in H5_TEMPLATE_DIR.iterdir():
        if item.name in _SYNC_EXCLUDE:
            continue
        dest = h5_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    print("   ✅ 模板复制完成")
    return h5_dir


def create_symlinks(h5_dir: Path, course_path: Path, course_id: str):
    """创建 public/courses/<courseId>/ 下的符号链接。
    
    支持两种架构：
    - 旧架构: visuals/assets/ 直接挂载
    - 新架构 (weeks/): 为每个 weeks/W0X/assets/ 创建独立链接
    """
    course_public = h5_dir / "public" / "courses" / course_id
    course_public.mkdir(parents=True, exist_ok=True)

    # visuals → 课程视觉素材（旧架构）
    visuals_link = course_public / "visuals"
    visuals_target = course_path / "visuals" / "assets"
    if not visuals_link.exists() and visuals_target.exists():
        try:
            visuals_link.symlink_to(visuals_target)
            print(f"   🔗 链接 {course_id}/visuals → {visuals_target.relative_to(CWD)}")
        except OSError as e:
            print(f"   ⚠️  符号链接失败: {e}")

    # weeks → 新架构的教学周目录（H5 前端可通过此链接访问 weeks/W0X/assets/）
    weeks_target = course_path / "weeks"
    weeks_link = course_public / "weeks"
    if not weeks_link.exists() and weeks_target.exists():
        try:
            weeks_link.symlink_to(weeks_target)
            print(f"   🔗 链接 {course_id}/weeks → {weeks_target.relative_to(CWD)}")
        except OSError as e:
            print(f"   ⚠️  符号链接失败: {e}")

    # tts → TTS 音频目录（新架构 build/tts/ 优先，旧架构 tts/ fallback）
    tts_link = course_public / "tts"
    tts_target = course_path / "build" / "tts"
    if not tts_target.exists():
        tts_target = course_path / "tts"
    if not tts_link.exists() and tts_target.exists():
        try:
            tts_link.symlink_to(tts_target)
            print(f"   🔗 链接 {course_id}/tts → {tts_target.relative_to(CWD)}")
        except OSError as e:
            print(f"   ⚠️  符号链接失败: {e}")


def create_legacy_symlinks(h5_dir: Path, course_path: Path):
    """为旧版单讲模式创建传统符号链接。"""
    public_dir = h5_dir / "public"
    public_dir.mkdir(exist_ok=True)

    visuals_link = public_dir / "visuals"
    visuals_target = course_path / "visuals" / "assets"
    if not visuals_link.exists() and visuals_target.exists():
        try:
            visuals_link.symlink_to(visuals_target)
        except OSError:
            pass

    tts_link = public_dir / "tts"
    tts_target = course_path / "build" / "tts"
    if not tts_target.exists():
        tts_target = course_path / "tts"
    if not tts_link.exists() and tts_target.exists():
        try:
            tts_link.symlink_to(tts_target)
        except OSError:
            pass


# ============================================================
# 课程发现与批量生成
# ============================================================

def discover_courses() -> list[dict]:
    """扫描 workspace 下所有含 course.yaml 的目录，返回课程信息列表。"""
    import yaml

    courses = []
    for cy in sorted(CWD.glob("*/course.yaml")):
        course_path = cy.parent
        try:
            raw = yaml.safe_load(cy.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"   ⚠️  解析 {cy} 失败: {e}")
            continue

        course_info = raw.get("course", {})
        structure = raw.get("structure", {})
        struct_type = structure.get("type", "weekly")

        course_id = course_info.get("id", course_path.name)
        course_name = course_info.get("name", course_path.name)

        # V-01 防护: 断言 id 与物理目录名一致，防止 SSG 路径寻址分歧
        if course_id != course_path.name:
            print(f"   ⚠️  警告: 课程 '{course_name}' 的 id '{course_id}' 与目录名 '{course_path.name}' 不一致！")
            print(f"      SSG 构建管线依赖物理目录名，id 不匹配可能导致资产丢失。")
            print(f"      建议：在 course.yaml 中将 id 设置为 '{course_path.name}'")

        # 发现脚本文件 — 支持两种架构
        scripts = []

        # 新架构优先: weeks/W0X/package.yaml 或 script.md
        weeks_dir = course_path / "weeks"
        if weeks_dir.exists():
            for week_dir in sorted(weeks_dir.glob("W*")):
                if (week_dir / "package.yaml").exists():
                    scripts.append(week_dir / "package.yaml")
                elif (week_dir / "script.md").exists():
                    scripts.append(week_dir / "script.md")

        # 旧架构回退: scripts/W*.md 或 scripts/S*.md
        if not scripts:
            scripts_dir = course_path / "scripts"
            if struct_type == "weekly":
                scripts = sorted(scripts_dir.glob("W*.md"))
            elif struct_type == "phasic":
                scripts = sorted(scripts_dir.glob("S*.md"))
            else:
                scripts = sorted(scripts_dir.glob("*.md"))

        courses.append({
            "id": course_id,
            "name": course_name,
            "path": course_path,
            "dir_name": course_path.name,
            "structure_type": struct_type,
            "scripts": scripts,
            "semester": course_info.get("semester", ""),
        })

    return courses


def _auto_compile_if_needed(script_path: Path) -> Path:
    """自动处理分片编译：支持 V5架构 (yaml) 及 V4兼容架构 (script.md + include)。"""
    is_yaml = script_path.suffix in ['.yaml', '.yml']

    if is_yaml:
        # V5 架构逻辑
        build_dir = script_path.parent / ".build"
        compiled_path = build_dir / "compiled.md"
        src_dir = script_path.parent / "src"
        needs_recompile = not compiled_path.exists()
        
        if not needs_recompile:
            compiled_mtime = compiled_path.stat().st_mtime
            if script_path.stat().st_mtime > compiled_mtime:
                needs_recompile = True
            elif src_dir.exists():
                for seg_file in src_dir.glob("*.md"):
                    if seg_file.stat().st_mtime > compiled_mtime:
                        needs_recompile = True
                        break

    else:
        # V4 向后兼容逻辑
        content = script_path.read_text(encoding="utf-8")
        if not re.search(r"<!--\s*include:\s*.+?\s*-->", content):
            return script_path

        compiled_path = script_path.with_name(script_path.stem + "_compiled.md")
        segments_dir = script_path.parent / "_segments"
        needs_recompile = not compiled_path.exists()

        if not needs_recompile:
            compiled_mtime = compiled_path.stat().st_mtime
            if script_path.stat().st_mtime > compiled_mtime:
                needs_recompile = True
            elif segments_dir.exists():
                for seg_file in segments_dir.glob("*.md"):
                    if seg_file.stat().st_mtime > compiled_mtime:
                        needs_recompile = True
                        break

    if needs_recompile:
        print(f"   🔄 检测到源码更新，自动编译 {script_path.name}...")
        dumptext = Path.cwd() / "engines" / "dumptext.py"
        cmd = [sys.executable, str(dumptext), str(script_path), "--mode", "full"]
        if not is_yaml:
            cmd.extend(["--output", str(compiled_path)])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ❌ 编译失败:\n{result.stderr}\n{result.stdout}")
            return script_path
    else:
        print(f"   ✅ 使用已缓存的编译产物: {compiled_path.name}")

    return compiled_path


def generate_single_script(
    course_path: Path, course_name: str, script_path: Path, theme: dict,
    *, skip_compile: bool = False,
) -> dict:
    """解析单个脚本文件，返回 H5 JSON 数据。

    参数:
        skip_compile: 为 True 时跳过 dumptext.py 编译，直接解析源文件。
                      用于 Fragment Mode 的快速迭代。
    """
    if script_path.stem in ["package", "script", "compiled"]:
        script_name = script_path.parent.name
    else:
        script_name = script_path.stem

    if skip_compile:
        actual_path = script_path
    else:
        actual_path = _auto_compile_if_needed(script_path)
    blocks = parse_script(str(actual_path))

    visual_count = sum(1 for b in blocks if b.block_type == BlockType.VISUAL)
    speech_count = sum(1 for b in blocks if b.block_type == BlockType.SPEECH)

    manifest = blocks_to_h5_json(
        blocks, course_name, script_name, course_path, theme, actual_path,
    )

    # 后处理：源映射回馈（compiled.md → 源 M0X.md 行号）
    if not skip_compile and actual_path.name == "compiled.md" and actual_path.parent.name == ".build":
        source_map = _build_source_map(actual_path)
        if source_map:
            _apply_source_map(manifest, source_map)
            print(f"   🗺️  源映射: {len(source_map)} 个片段 → copy-locator 指向源文件")

    total_slides = sum(len(s["slides"]) for s in manifest["sections"])
    total_paragraphs = sum(len(s["paragraphs"]) for s in manifest["sections"])

    # 统计视觉完整度
    slides_with_image = 0
    slides_total = 0
    for sec in manifest["sections"]:
        for slide in sec["slides"]:
            slides_total += 1
            if slide.get("image"):
                slides_with_image += 1

    print(f"   📖 {script_name}: {len(manifest['sections'])} 模块, {total_slides} slides, "
          f"{total_paragraphs} 段落, 图片 {slides_with_image}/{slides_total}")

    return manifest


def build_week_summary(manifest: dict) -> dict:
    """从完整 manifest 中提取 week 摘要信息（供 workspace manifest 索引使用）。"""
    total_slides = sum(len(s["slides"]) for s in manifest["sections"])
    total_paragraphs = sum(len(s["paragraphs"]) for s in manifest["sections"])

    slides_with_image = 0
    slides_total = 0
    for sec in manifest["sections"]:
        for slide in sec["slides"]:
            slides_total += 1
            if slide.get("image"):
                slides_with_image += 1

    return {
        "script": manifest["script"],
        "sections": len(manifest["sections"]),
        "slides": total_slides,
        "paragraphs": total_paragraphs,
        "hasAudio": manifest["media"].get("audio") is not None,
        "hasSrt": manifest["media"].get("srt") is not None,
        "visualCoverage": f"{slides_with_image}/{slides_total}",
    }


def run_batch_mode(course_dirs: list[str] | None = None):
    """批量模式: 生成所有（或指定）课程的全部讲次。"""
    print("=" * 60)
    print("🚀 H5 全量生成模式")
    print("=" * 60)
    print()

    # 发现课程
    all_courses = discover_courses()
    if not all_courses:
        print("❌ workspace 中未找到任何课程 (含 course.yaml 的目录)")
        sys.exit(1)

    # 过滤（如果指定了特定课程）
    if course_dirs:
        all_courses = [c for c in all_courses if c["dir_name"] in course_dirs]

    print(f"📚 发现 {len(all_courses)} 门课程:")
    for c in all_courses:
        script_count = len(c["scripts"])
        print(f"   • {c['name']} ({c['dir_name']}) — {c['structure_type']} — {script_count} 讲")
    print()

    # 创建 workspace 级 H5 实例
    h5_dir = ensure_h5_instance(CWD)
    courses_data_dir = h5_dir / "public" / "courses"
    courses_data_dir.mkdir(parents=True, exist_ok=True)

    workspace_manifest = {
        "version": "2.0",
        "generated": datetime.now().isoformat(),
        "courses": [],
    }

    for course in all_courses:
        course_path = course["path"]
        course_id = course["id"]
        course_name = course["name"]
        scripts = course["scripts"]

        if not scripts:
            print(f"⏭️  {course_name}: 无脚本文件，跳过")
            workspace_manifest["courses"].append({
                "id": course_id,
                "name": course_name,
                "dirName": course["dir_name"],
                "structureType": course["structure_type"],
                "semester": course["semester"],
                "weeks": [],
            })
            continue

        print(f"\n{'─' * 40}")
        print(f"📌 处理课程: {course_name} ({len(scripts)} 讲)")
        print(f"{'─' * 40}")

        # 加载主题
        theme = load_theme(course_path)
        print(f"   🎨 主题: 主色 {theme['primary']} | 底色 {theme['bg']}")

        # 创建符号链接
        create_symlinks(h5_dir, course_path, course_id)

        # 课程级数据目录
        course_data_dir = courses_data_dir / course_id
        course_data_dir.mkdir(parents=True, exist_ok=True)

        course_manifest_entry = {
            "id": course_id,
            "name": course_name,
            "dirName": course["dir_name"],
            "structureType": course["structure_type"],
            "semester": course["semester"],
            "theme": theme,
            "weeks": [],
        }

        for script_path in scripts:
            if script_path.stem in ["package", "script", "compiled"]:
                script_name = script_path.parent.name
            else:
                script_name = script_path.stem
            try:
                manifest = generate_single_script(course_path, course_name, script_path, theme)

                # 保存分讲 JSON
                week_file = course_data_dir / f"{script_name}.json"
                with open(week_file, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=2)

                # 添加到课程索引
                summary = build_week_summary(manifest)
                course_manifest_entry["weeks"].append(summary)

            except Exception as e:
                print(f"   ❌ {script_name} 生成失败: {e}")
                course_manifest_entry["weeks"].append({
                    "script": script_name,
                    "error": str(e),
                })

        workspace_manifest["courses"].append(course_manifest_entry)

    # 保存全局 manifest
    manifest_path = courses_data_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(workspace_manifest, f, ensure_ascii=False, indent=2)

    # 汇总
    print()
    print("=" * 60)
    total_courses = len(workspace_manifest["courses"])
    total_weeks = sum(len(c["weeks"]) for c in workspace_manifest["courses"])
    print(f"🎉 生成完毕! 共 {total_courses} 门课程, {total_weeks} 讲")
    print(f"   索引: {manifest_path.relative_to(CWD)}")
    print()
    print("下一步:")
    print(f"  cd {h5_dir.relative_to(CWD)}")
    print("  npm install  # (首次)")
    print("  npm run dev")
    print("=" * 60)


def run_fragment_mode(course_dir: str, fragment_path: str):
    """片段模式：直接渲染单个 M0X.md 文件，跳过 compiled.md 编译。

    复用 generate_single_script(skip_compile=True)，仅负责：
    - 路径解析与 CLI 输出
    - H5 实例初始化与 JSON 写入
    """
    course_path = CWD / course_dir
    fragment = Path(fragment_path)
    if not fragment.is_absolute():
        fragment = CWD / fragment_path
    if not fragment.exists():
        fragment = course_path / fragment_path
    if not fragment.exists():
        print(f"❌ 片段文件不存在: {fragment_path}")
        sys.exit(1)

    module_name = fragment.stem
    week_name = fragment.parent.parent.name if fragment.parent.name == "src" else module_name

    print(f"🔬 片段模式 (Fragment Mode)")
    print(f"   课程: {course_dir} | 教学周: {week_name} | 片段: {module_name}")
    print()

    theme = load_theme(course_path)

    # 核心：复用 generate_single_script，skip_compile=True 跳过编译
    manifest = generate_single_script(
        course_path, course_dir, fragment, theme, skip_compile=True,
    )
    manifest["mode"] = "fragment"
    manifest["fragment"] = {
        "module": module_name, "week": week_name,
        "srcFile": str(fragment.resolve()),
    }

    # 写入 H5 实例
    h5_dir = ensure_h5_instance(CWD)
    create_symlinks(h5_dir, course_path, course_path.name)

    fragments_dir = h5_dir / "public" / "courses" / course_path.name / "fragments"
    fragments_dir.mkdir(parents=True, exist_ok=True)
    output_path = fragments_dir / f"{module_name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 兼容 slides.json（旧版 App.jsx）
    slides_json_path = h5_dir / "public" / "slides.json"
    with open(slides_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"🎉 片段保存: {output_path.relative_to(CWD)}")
    print(f"💡 copy-locator-btn 直接指向: {fragment.resolve()}")
    print(f"\n下一步: cd {h5_dir.relative_to(CWD)} && npm run dev")


def run_rebuild_week(course_dir: str, changed_file: str):
    """热重载模式：从变更的 .md 文件反推所属教学周，仅重建该周 JSON。

    由 Vite 热重载插件自动调用，设计目标：
    - 快速（仅重编译一个教学周，非全课程）
    - 正确（生成的 JSON 路径与 LessonViewer 一致）
    - 兼容（同时写入 slides.json 供旧版 App.jsx 使用）
    """
    import yaml

    course_path = CWD / course_dir
    changed = Path(changed_file)
    if not changed.is_absolute():
        changed = CWD / changed_file
    changed = changed.resolve()

    if not changed.exists():
        print(f"❌ 变更文件不存在: {changed}")
        sys.exit(1)

    # 反推教学周目录: .../weeks/W0X_xxx/src/M0X.md → .../weeks/W0X_xxx/
    if changed.parent.name == "src":
        week_dir = changed.parent.parent
    else:
        week_dir = changed.parent

    week_name = week_dir.name

    # 找到编译入口文件
    package_yaml = week_dir / "package.yaml"
    script_md = week_dir / "script.md"
    if package_yaml.exists():
        script_path = package_yaml
    elif script_md.exists():
        script_path = script_md
    else:
        print(f"❌ 未找到 {week_name} 的编译入口 (package.yaml 或 script.md)")
        sys.exit(1)

    print(f"🔥 热重载模式 (Rebuild Week)")
    print(f"   课程: {course_dir} | 教学周: {week_name} | 触发: {changed.name}")

    # 读取课程名称
    course_name = course_dir
    course_yaml_path = course_path / "course.yaml"
    if course_yaml_path.exists():
        try:
            config = yaml.safe_load(course_yaml_path.read_text(encoding="utf-8"))
            course_name = config.get("course", {}).get("name", course_dir)
        except Exception:
            pass

    theme = load_theme(course_path)

    # 核心：重用 generate_single_script（含编译 + 解析 + 源映射）
    manifest = generate_single_script(course_path, course_name, script_path, theme)

    # 写入 workspace 级 H5 实例
    h5_dir = ensure_h5_instance(CWD)
    create_symlinks(h5_dir, course_path, course_path.name)

    course_data_dir = h5_dir / "public" / "courses" / course_path.name
    course_data_dir.mkdir(parents=True, exist_ok=True)

    week_file = course_data_dir / f"{week_name}.json"
    with open(week_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 兼容 slides.json（旧版 App.jsx）
    slides_json_path = h5_dir / "public" / "slides.json"
    with open(slides_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"🎉 热重载完成: {week_file.relative_to(CWD)}")


def run_legacy_mode(course_dir: str, script_rel_path: str):
    """旧版单讲模式（完全向后兼容）。"""
    course_path = CWD / course_dir
    script_path = course_path / script_rel_path
    if script_path.stem in ["package", "script", "compiled"]:
        script_name = script_path.parent.name
    else:
        script_name = script_path.stem

    if not script_path.exists():
        print(f"❌ 脚本文件不存在: {script_path}")
        sys.exit(1)

    print(f"📌 课程: {course_dir}")
    print(f"📖 脚本: {script_rel_path}")
    print()

    theme = load_theme(course_path)
    print(f"🎨 加载主题")
    print(f"   主色: {theme['primary']} | 底色: {theme['bg']}")
    print(f"   字体: {theme['fontTitle']} / {theme['fontBody']}")
    print()

    print(f"📖 解析 {script_name}...")
    blocks = parse_script(str(script_path))
    print(f"   共 {len(blocks)} 个块")

    visual_count = sum(1 for b in blocks if b.block_type == BlockType.VISUAL)
    speech_count = sum(1 for b in blocks if b.block_type == BlockType.SPEECH)
    activity_count = sum(1 for b in blocks if b.block_type == BlockType.ACTIVITY)
    print(f"   VISUAL: {visual_count} | SPEECH: {speech_count} | ACTIVITY: {activity_count}")
    print()

    manifest = blocks_to_h5_json(blocks, course_dir, script_name, course_path, theme, script_path)

    total_slides = sum(len(s["slides"]) for s in manifest["sections"])
    total_paragraphs = sum(len(s["paragraphs"]) for s in manifest["sections"])
    print(f"✅ 生成 H5 数据:")
    print(f"   模块: {len(manifest['sections'])}")
    print(f"   Slide: {total_slides}")
    print(f"   段落: {total_paragraphs}")
    print()

    h5_dir = ensure_h5_instance(course_path)
    create_legacy_symlinks(h5_dir, course_path)

    output_path = h5_dir / "public" / "slides.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"🎉 保存成功: {output_path.relative_to(CWD)}")
    print()
    print("下一步:")
    print(f"  cd {h5_dir.relative_to(CWD)}")
    print("  npm install  # (首次)")
    print("  npm run dev")


# ============================================================
# 主入口
# ============================================================

def main():
    args = sys.argv[1:]

    if not args:
        print("❌ 用法:")
        print("  单讲: python engines/generate_course_h5.py <课程目录> <脚本路径>")
        print("  全量: python engines/generate_course_h5.py --all")
        print("  指定: python engines/generate_course_h5.py <课程目录> --all")
        print("  片段: python engines/generate_course_h5.py <课程目录> --fragment <M0X.md路径>")
        print("  热重载: python engines/generate_course_h5.py <课程目录> --rebuild-week <M0X.md路径>")
        sys.exit(1)

    # 热重载模式检测（优先于片段模式）
    if "--rebuild-week" in args:
        rw_idx = args.index("--rebuild-week")
        if rw_idx == 0 or rw_idx + 1 >= len(args):
            print("❌ 热重载模式: python engines/generate_course_h5.py <课程目录> --rebuild-week <M0X.md路径>")
            sys.exit(1)
        course_dir = args[0]
        changed_file = args[rw_idx + 1]
        run_rebuild_week(course_dir, changed_file)
        return

    # 片段模式检测
    if "--fragment" in args:
        frag_idx = args.index("--fragment")
        if frag_idx == 0 or frag_idx + 1 >= len(args):
            print("❌ 片段模式: python engines/generate_course_h5.py <课程目录> --fragment <M0X.md路径>")
            sys.exit(1)
        course_dir = args[0]
        fragment_path = args[frag_idx + 1]
        run_fragment_mode(course_dir, fragment_path)
        return

    # 全量模式检测
    if "--all" in args:
        args_without_all = [a for a in args if a != "--all"]
        if args_without_all:
            # 指定课程的全量模式
            run_batch_mode(args_without_all)
        else:
            # workspace 全量模式
            run_batch_mode()
        return

    # 单讲模式（向后兼容）
    if len(args) < 2:
        print("❌ 单讲模式需要: python engines/generate_course_h5.py <课程目录> <脚本路径>")
        sys.exit(1)

    run_legacy_mode(args[0], args[1])


if __name__ == "__main__":
    main()
