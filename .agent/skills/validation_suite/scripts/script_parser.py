#!/usr/bin/env python3
"""
通用课程脚本解析器 (Universal Script Parser)

将 Markdown 脚本文件解析为结构化 ScriptBlock 列表，供验证器和导出器消费。
支持新规范的 > [VISUAL]、> [ACTIVITY]、知识标签等块类型。

用法（作为模块导入）：
    from script_parser import parse_script, BlockType
    blocks = parse_script("实习指导/scripts/S01_Mobilization.md")
"""

import re
import os
import yaml
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


class BlockType(Enum):
    """脚本块类型"""
    SPEECH = "speech"        # 正文（可朗读内容）
    VISUAL = "visual"        # > [VISUAL] 块
    ACTIVITY = "activity"    # > [ACTIVITY] 块（实践/问答/测试/演示）
    TAG = "tag"              # 知识标签 > [TECH NOTE] 等
    HEADER = "header"        # ## 标题行
    META = "meta"            # > **Role**: 等元数据行
    SLIDE_REF = "slide_ref"  # > **[SLIDE: xxx]** 旧格式引用
    SEPARATOR = "separator"  # --- 分隔线
    EMPTY = "empty"          # 空行


@dataclass
class ScriptBlock:
    """脚本中的一个结构化块"""
    block_type: BlockType
    content: str                           # 原始文本内容
    line_start: int                        # 起始行号（1-indexed）
    line_end: int                          # 结束行号（1-indexed）
    metadata: dict = field(default_factory=dict)
    # metadata 可能包含:
    #   slide_id, layout, scene, asset  (VISUAL 块)
    #   activity_type, duration, desc   (ACTIVITY 块)
    #   tag_name                        (TAG 块)
    #   slide_ref_id                    (SLIDE_REF 块)
    #   level                           (HEADER 块)


# ===== 正则模式 =====

# 知识标签白名单
KNOWN_TAGS = {
    "TECH NOTE", "WARNING", "DID YOU KNOW",
    "STORY TIME", "PHILOSOPHY", "CASE STUDY", "LIFE CONNECT",
    "TEACHING MOMENT",
    "VISUAL", "ACTIVITY",
    "!NOTE", "!TIP", "!IMPORTANT", "!WARNING", "!CAUTION"
}

# 口头叙事型标签（ADR 022）：教师会在课堂上完整讲述的内容，
# 应计入讲授字数和 PPT Speaker Notes。
# 参考型标签（TECH NOTE / WARNING）：补充性技术细节，教师可酌情跳过。
ORAL_TAGS = {
    "STORY TIME", "CASE STUDY", "LIFE CONNECT",
    "PHILOSOPHY", "DID YOU KNOW", "TEACHING MOMENT",
}

# 有效 Layout 类型（与 .agent/skills/pptx/layouts.md 保持同步）
VALID_LAYOUTS = {
    # 正式标签 (21 种)
    "Title", "Section", "Agenda", "Split", "Icons",
    "Grid", "Full", "Table", "Comparison", "Dashboard",
    "Stat", "Timeline", "Poll", "Workshop", "Quote",
    "CTA", "Code", "Diagram", "Image", "Screenshot", "List",
    # 弃用别名（向后兼容，validate 时不报错但输出警告）
    "Card", "Cards", "Full Screen", "CodeBlock",
    "Triple-Column", "Three-Column", "Quadrant", "Flow",
    "Canvas", "Chat-Bubble", "Template-Card", "Spectrum",
    "Text", "Chart", "Video",
}

# 有效 ACTIVITY 类型
VALID_ACTIVITY_TYPES = {"Practice", "QA", "Quiz", "Demo", "Discussion", "Workshop", "Warm-up"}

# 正则模式
RE_HEADER = re.compile(r'^(#{1,6})\s+(.*)')
RE_SEPARATOR = re.compile(r'^---\s*$')
RE_META = re.compile(r'^>\s+\*\*(\w+)\*\*:\s*(.*)')
RE_TAG_START = re.compile(r'^>\s+\[([A-Z ]+|![A-Z]+)(?::.*?)?\]')
RE_BLOCKQUOTE = re.compile(r'^>\s*(.*)')
RE_OLD_SLIDE_REF = re.compile(r'>\s+\*\*\[SLIDE:\s*(\S+)\]\*\*')


def _field_re(name: str, *, freeform: bool = False) -> re.Pattern:
    """生成统一的 **Field**: 正则。

    freeform=False（默认）: 三路匹配 `value` / "value" / bare_value
    freeform=True:  匹配任意文本（如 Scene/Desc，内容可含空格）
    """
    if freeform:
        return re.compile(rf'\*\*{name}\*\*:\s*(.*)')
    return re.compile(rf'\*\*{name}\*\*:\s*(?:`([^`]+)`|"([^"]+)"|(\S.*))')


def _extract(match: re.Match, *, freeform: bool = False) -> str:
    """从三路/freeform 匹配结果提取文本。"""
    if freeform:
        return match.group(1).strip()
    return next((g for g in match.groups() if g), "").strip()


def normalize_asset_path(raw: str) -> str:
    """从原始 Asset 值中提取纯净的相对路径（基于课程根目录）。

    支持以下输入格式（全部自动正规化）：
    1. 纯路径:        visuals/assets/W01/img.png
    2. MD 图片语法:   ![描述](visuals/assets/W01/img.png)
    3. MD 链接语法:   [文字](visuals/assets/W01/img.png)
    4. 带相对前缀:    ../visuals/assets/W01/img.png
    5. 反引号包裹:    `visuals/assets/W01/img.png`
    6. 双引号包裹:    "visuals/assets/W01/img.png"
    """
    if not raw:
        return ""
    s = raw.strip()
    # 剥离 MD 图片/链接语法 ![alt](path) 或 [text](path)
    md_match = re.match(r'!?\[.*?\]\((.+?)\)', s)
    if md_match:
        s = md_match.group(1).strip()
    # 剥离反引号
    if s.startswith('`') and s.endswith('`'):
        s = s[1:-1]
    # 剥离双引号
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    # 剥离前导 ../
    s = re.sub(r'^(\.\./)+', '', s)
    return s.strip()


# **Field**: 正则（通过工厂函数统一生成，保证匹配策略一致）
RE_SLIDE_FIELD = _field_re("Slide")
RE_LAYOUT_FIELD = _field_re("Layout")
RE_SCENE_FIELD = _field_re("Scene", freeform=True)
RE_TEXT_FIELD = _field_re("Text", freeform=False)
RE_ASSET_FIELD = _field_re("Asset")
RE_ACTIVITY_TYPE = _field_re("Type")
RE_ACTIVITY_DURATION = _field_re("Duration")
RE_ACTIVITY_DESC = _field_re("Desc", freeform=True)

# 多资产匹配：支持 **Asset**, **Asset 1**, **Asset 2**, **Resource** 等
RE_ASSET_MULTI_FIELD = re.compile(
    r'\*\*(?:Asset(?:\s*\d+)?|Resource)\*\*:\s*(?:`([^`]+)`|"([^"]+)"|(\S.*))',
    re.IGNORECASE,
)


def _parse_duration(text: str) -> int:
    """将时长文本解析为秒数。支持 '5min'、'30s'、'1.5min' 等格式。"""
    text = text.strip().lower()
    # 分钟
    m = re.match(r'([\d.]+)\s*min', text)
    if m:
        return int(float(m.group(1)) * 60)
    # 秒
    m = re.match(r'([\d.]+)\s*s', text)
    if m:
        return int(float(m.group(1)))
    # 纯数字，默认分钟
    m = re.match(r'^([\d.]+)$', text)
    if m:
        return int(float(m.group(1)) * 60)
    return 0


def parse_script(file_path: str) -> list[ScriptBlock]:
    """
    解析 Markdown 脚本文件为 ScriptBlock 列表。

    参数:
        file_path: 脚本文件的绝对或相对路径

    返回:
        ScriptBlock 列表，按行号顺序排列
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    blocks = []
    i = 0
    total = len(lines)

    # ----- 跳过 YAML Frontmatter -----
    if total > 0 and lines[0].strip() == '---':
        i = 1
        while i < total and lines[i].strip() != '---':
            i += 1
        if i < total:
            i += 1  # 跳过结束的 ---

    while i < total:
        line = lines[i].rstrip('\n')
        line_num = i + 1  # 1-indexed

        # ----- 空行 -----
        if not line.strip():
            i += 1
            continue

        # ----- 分隔线 -----
        if RE_SEPARATOR.match(line):
            blocks.append(ScriptBlock(
                block_type=BlockType.SEPARATOR,
                content=line,
                line_start=line_num,
                line_end=line_num,
            ))
            i += 1
            continue

        # ----- 标题 -----
        header_m = RE_HEADER.match(line)
        if header_m:
            level = len(header_m.group(1))
            blocks.append(ScriptBlock(
                block_type=BlockType.HEADER,
                content=header_m.group(2).strip(),
                line_start=line_num,
                line_end=line_num,
                metadata={"level": level},
            ))
            i += 1
            continue

        # ----- 引用块（标签、VISUAL、ACTIVITY、META、旧 SLIDE REF）-----
        if line.startswith('>'):
            block_lines = []
            block_start = line_num

            # 收集连续引用行
            while i < total and lines[i].rstrip('\n').startswith('>'):
                block_lines.append(lines[i].rstrip('\n'))
                i += 1

            block_end = block_start + len(block_lines) - 1
            raw_content = '\n'.join(block_lines)

            # 提取引用内容（去掉 > 前缀）
            inner_lines = []
            for bl in block_lines:
                m = RE_BLOCKQUOTE.match(bl)
                inner_lines.append(m.group(1) if m else bl[1:].strip())
            inner_content = '\n'.join(inner_lines)

            # 判断块类型
            first_inner = inner_lines[0].strip() if inner_lines else ""

            # (1) 先检查旧 SLIDE REF 格式
            old_ref_m = RE_OLD_SLIDE_REF.match(block_lines[0])
            if old_ref_m:
                blocks.append(ScriptBlock(
                    block_type=BlockType.SLIDE_REF,
                    content=inner_content,
                    line_start=block_start,
                    line_end=block_end,
                    metadata={"slide_ref_id": old_ref_m.group(1)},
                ))
                continue

            # (2) 检查标签
            tag_m = RE_TAG_START.match(block_lines[0])
            if tag_m:
                tag_name = tag_m.group(1).strip()

                # (2a) VISUAL 块
                if tag_name == "VISUAL":
                    meta = {}
                    asset_list = []  # 多资产收集器
                    for il in inner_lines:
                        sm = RE_SLIDE_FIELD.search(il)
                        if sm:
                            meta["slide_id"] = _extract(sm)
                        lm = RE_LAYOUT_FIELD.search(il)
                        if lm:
                            meta["layout"] = _extract(lm)
                        scm = RE_SCENE_FIELD.search(il)
                        if scm:
                            meta["scene"] = _extract(scm, freeform=True)
                        txtm = RE_TEXT_FIELD.search(il)
                        if txtm:
                            meta["text"] = _extract(txtm)
                        # 多资产匹配（Asset / Asset 1 / Asset 2 / Resource）
                        am = RE_ASSET_MULTI_FIELD.search(il)
                        if am:
                            raw_path = next((g for g in am.groups() if g), "").strip()
                            clean = normalize_asset_path(raw_path)
                            if clean:
                                asset_list.append(clean)

                    # 输出兼容层:
                    # - meta["assets"]: 完整资产列表（新 API）
                    # - meta["asset"]:  首个资产路径（向后兼容旧消费者）
                    meta["assets"] = asset_list
                    meta["asset"] = asset_list[0] if asset_list else ""

                    blocks.append(ScriptBlock(
                        block_type=BlockType.VISUAL,
                        content=inner_content,
                        line_start=block_start,
                        line_end=block_end,
                        metadata=meta,
                    ))
                    continue

                # (2b) ACTIVITY 块
                elif tag_name == "ACTIVITY":
                    meta = {}
                    for il in inner_lines:
                        tm = RE_ACTIVITY_TYPE.search(il)
                        if tm:
                            meta["activity_type"] = _extract(tm)
                        dm = RE_ACTIVITY_DURATION.search(il)
                        if dm:
                            raw = _extract(dm)
                            meta["duration_raw"] = raw
                            meta["duration_sec"] = _parse_duration(raw)
                        desc_m = RE_ACTIVITY_DESC.search(il)
                        if desc_m:
                            meta["desc"] = _extract(desc_m, freeform=True)

                    blocks.append(ScriptBlock(
                        block_type=BlockType.ACTIVITY,
                        content=inner_content,
                        line_start=block_start,
                        line_end=block_end,
                        metadata=meta,
                    ))
                    continue

                # (2c) 口头叙事型标签 -> 归为 SPEECH（计入字数）
                elif tag_name in ORAL_TAGS:
                    # 去掉标签行本身，仅保留正文内容
                    oral_lines = [l for l in inner_lines[1:] if l.strip()]
                    oral_content = '\n'.join(oral_lines)
                    # 即使标签块内无引用正文（内容在后续非引用段落中），
                    # 也需创建块以便 validate_spec.py 正确计数标签
                    blocks.append(ScriptBlock(
                        block_type=BlockType.SPEECH,
                        content=oral_content,
                        line_start=block_start,
                        line_end=block_end,
                        metadata={"tag_name": tag_name, "oral_tag": True},
                    ))
                    continue

                # (2d) 参考型标签 (TECH NOTE / WARNING) -> 保持 TAG
                else:
                    blocks.append(ScriptBlock(
                        block_type=BlockType.TAG,
                        content=inner_content,
                        line_start=block_start,
                        line_end=block_end,
                        metadata={"tag_name": tag_name},
                    ))
                    continue

            # (3) 元数据行（> **Role**: ...）
            meta_m = RE_META.match(block_lines[0])
            if meta_m:
                blocks.append(ScriptBlock(
                    block_type=BlockType.META,
                    content=inner_content,
                    line_start=block_start,
                    line_end=block_end,
                ))
                continue

            # (4) 其他引用块视为正文
            blocks.append(ScriptBlock(
                block_type=BlockType.SPEECH,
                content=inner_content,
                line_start=block_start,
                line_end=block_end,
            ))
            continue

        # ----- 正文 -----
        blocks.append(ScriptBlock(
            block_type=BlockType.SPEECH,
            content=line,
            line_start=line_num,
            line_end=line_num,
        ))
        i += 1

    return blocks


def strip_markdown(text: str) -> str:
    """去除 Markdown 格式标记，提取纯文本。"""
    # 去除粗体/斜体标记
    text = re.sub(r'(\*\*|__|_|\*)', '', text)
    # 去除代码标记
    text = re.sub(r'`', '', text)
    # 去除链接 [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # 去除有序/无序列表标记
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # 去除 HTML 注释
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text


def load_course_config(workspace_root: str, course_name: str) -> dict:
    """
    加载课程的 course.yaml 配置。

    参数:
        workspace_root: 工作区根目录
        course_name: 课程目录名

    返回:
        配置字典
    """
    yaml_path = os.path.join(workspace_root, course_name, "course.yaml")
    if not os.path.exists(yaml_path):
        print(f"⚠️  course.yaml 未找到: {yaml_path}")
        return {}

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def get_workspace_root() -> str:
    """
    从脚本位置推算工作区根目录。
    脚本位于: <workspace>/.agent/skills/validation_suite/scripts/
    """
    return str(Path(__file__).resolve().parents[4])


def get_scripts_dir(workspace_root: str, course_name: str) -> str:
    """获取课程脚本目录（兼容 scripts/ 和 weeks/ 新架构）。
    
    优先返回 weeks/ 路径（分片架构），旧架构 scripts/ 作为回退。
    """
    weeks_dir = os.path.join(workspace_root, course_name, "weeks")
    if os.path.exists(weeks_dir):
        return weeks_dir
    return os.path.join(workspace_root, course_name, "scripts")


def get_visuals_dir(workspace_root: str, course_name: str) -> str:
    """获取课程视觉素材目录。
    
    优先返回旧架构 visuals/assets/；若不存在或为空则提示消费者
    使用 get_weeks_asset_dirs() 获取新架构路径。
    """
    return os.path.join(workspace_root, course_name, "visuals", "assets")


def get_weeks_asset_dirs(workspace_root: str, course_name: str) -> list[str]:
    """获取新架构 weeks/W0X/ 下所有素材目录。
    
    兼容 V5 (public/) 和旧架构 (assets/)。
    """
    weeks_dir = os.path.join(workspace_root, course_name, "weeks")
    if not os.path.exists(weeks_dir):
        return []
    dirs = []
    for entry in sorted(os.listdir(weeks_dir)):
        week_path = os.path.join(weeks_dir, entry)
        if not os.path.isdir(week_path):
            continue
        for subdir in ["public", "assets"]:  # V5 优先
            asset_dir = os.path.join(week_path, subdir)
            if os.path.isdir(asset_dir):
                dirs.append(asset_dir)
    return dirs


def _auto_compile_week(week_dir: str) -> Optional[str]:
    """对 weeks/ 下的教学周目录自动编译分片脚本，返回可用的脚本路径。
    
    兼容 V5 (.yaml + .build/) 和 V4 (.md + _segments/)
    """
    import re as _re
    import subprocess as _sp
    
    # 尝试 V5 架构
    yaml_path = os.path.join(week_dir, "package.yaml")
    if os.path.exists(yaml_path):
        build_dir = os.path.join(week_dir, ".build")
        compiled_path = os.path.join(build_dir, "compiled.md")
        src_dir = os.path.join(week_dir, "src")
        
        needs_recompile = not os.path.exists(compiled_path)
        if not needs_recompile:
            compiled_mtime = os.path.getmtime(compiled_path)
            if os.path.getmtime(yaml_path) > compiled_mtime:
                needs_recompile = True
            elif os.path.exists(src_dir):
                for seg in os.listdir(src_dir):
                    if seg.endswith('.md') and os.path.getmtime(
                        os.path.join(src_dir, seg)) > compiled_mtime:
                        needs_recompile = True
                        break

        if needs_recompile:
            workspace = str(Path(__file__).resolve().parents[4])
            dumptext = os.path.join(workspace, "engines", "dumptext.py")
            if os.path.exists(dumptext):
                import sys as _sys
                result = _sp.run(
                    [_sys.executable, dumptext, yaml_path, "--mode", "full"],
                    capture_output=True, text=True,
                )
                if result.returncode != 0:
                    return None  # V5 编译失败
        return compiled_path if os.path.exists(compiled_path) else None

    # V4 旧架构向后兼容
    script_path = os.path.join(week_dir, "script.md")
    if not os.path.exists(script_path):
        return None

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 单体脚本：无 include 指令，直接返回
    if not _re.search(r'<!--\s*include:\s*.+?\s*-->', content):
        return script_path

    # 分片架构：检查是否需要重编译
    compiled_path = os.path.join(week_dir, "script_compiled.md")
    segments_dir = os.path.join(week_dir, "_segments")

    needs_recompile = not os.path.exists(compiled_path)
    if not needs_recompile:
        compiled_mtime = os.path.getmtime(compiled_path)
        if os.path.getmtime(script_path) > compiled_mtime:
            needs_recompile = True
        elif os.path.exists(segments_dir):
            for seg in os.listdir(segments_dir):
                if seg.endswith('.md') and os.path.getmtime(
                    os.path.join(segments_dir, seg)) > compiled_mtime:
                    needs_recompile = True
                    break

    if needs_recompile:
        # 调用 dumptext.py 编译
        workspace = str(Path(__file__).resolve().parents[4])
        dumptext = os.path.join(workspace, "engines", "dumptext.py")
        if os.path.exists(dumptext):
            import sys as _sys
            result = _sp.run(
                [_sys.executable, dumptext, script_path, "--mode", "full",
                 "--output", compiled_path],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(result.stdout)
                print(result.stderr)
                return script_path  # 编译失败，回退到原文件

    return compiled_path if os.path.exists(compiled_path) else script_path


def list_script_files(scripts_dir: str) -> list[str]:
    """列出脚本目录中所有可分析的 .md 文件。
    
    兼容两种架构：
    - 旧架构 (scripts/): 直接列出 .md 文件
    - 新架构 (weeks/): 扫描 W*/ 子目录，自动编译分片脚本后返回
    """
    if not os.path.exists(scripts_dir):
        return []

    # 新架构: weeks/ 目录
    base = os.path.basename(scripts_dir)
    if base == "weeks":
        results = []
        for entry in sorted(os.listdir(scripts_dir)):
            week_path = os.path.join(scripts_dir, entry)
            if not os.path.isdir(week_path) or not entry.startswith("W"):
                continue
            script_file = _auto_compile_week(week_path)
            if script_file:
                # 返回相对于 weeks/ 的路径 (如 W01_xxx/script_compiled.md)
                results.append(os.path.relpath(script_file, scripts_dir))
        return results

    # 旧架构: scripts/ 目录
    return sorted([
        f for f in os.listdir(scripts_dir)
        if f.endswith(".md")
        and not f.startswith("00_")
        and not f.endswith("_Report.md")
    ])


def filter_files_by_week(files: list[str], week_num: int) -> list[str]:
    """按周次编号过滤文件列表。

    兼容两种路径格式:
    - "W01_xxx.md" (旧架构)
    - "W01_xxx/.build/compiled.md" (V5 新架构)
    """
    week_prefix = f"W{week_num:02d}_"
    return [f for f in files if week_prefix in f]


def list_script_files_for_week(scripts_dir: str, week_num: int) -> list[str]:
    """列出指定周次的可分析脚本文件。

    与 list_script_files 不同，仅编译/扫描指定周次的目录，
    避免触发其他周次的 _auto_compile_week，节省编译时间和 I/O。

    兼容两种架构：
    - 旧架构 (scripts/): 按文件名前缀 W0N_ 过滤
    - 新架构 (weeks/): 仅编译 W0N_* 单个子目录
    """
    if not os.path.exists(scripts_dir):
        return []

    week_prefix = f"W{week_num:02d}_"

    # 新架构: weeks/ 目录 — 仅编译目标周次
    base = os.path.basename(scripts_dir)
    if base == "weeks":
        results = []
        for entry in sorted(os.listdir(scripts_dir)):
            if not entry.startswith(week_prefix):
                continue
            week_path = os.path.join(scripts_dir, entry)
            if not os.path.isdir(week_path):
                continue
            script_file = _auto_compile_week(week_path)
            if script_file:
                results.append(os.path.relpath(script_file, scripts_dir))
        return results

    # 旧架构: scripts/ 目录 — 按前缀过滤
    return sorted([
        f for f in os.listdir(scripts_dir)
        if f.endswith(".md")
        and f.startswith(week_prefix)
        and not f.endswith("_Report.md")
    ])


# ===== 命令行测试 =====
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python script_parser.py <脚本路径>")
        sys.exit(1)

    target = sys.argv[1]
    blocks = parse_script(target)

    for b in blocks:
        meta_str = f" | meta={b.metadata}" if b.metadata else ""
        content_preview = b.content[:60].replace('\n', '↵')
        print(f"  L{b.line_start}-{b.line_end} [{b.block_type.value:10s}] {content_preview}{meta_str}")

    print(f"\n共 {len(blocks)} 个块")
