#!/usr/bin/env python3
"""
逐字稿网络素材需求扫描引擎 (Real-Asset Sourcing Scanner)

扫描 Markdown 逐字稿中的 [VISUAL] 块和正文，识别适合从网络搜索/下载真实素材
（而非 AI 文生图）的视觉位置。

用法:
    python scan_real_assets.py [脚本目录或单个.md文件]
    
输出:
    sourcing_checklist.yaml — 按优先级排序的待办清单
"""

import re
import sys
import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── 规则 R1: Scene 字段关键词模式 ───

# 历史事件信号
RE_HISTORY = re.compile(
    r'(真实|实录|纪实|档案|历史|原版|original|authentic|real\b|archival)',
    re.IGNORECASE
)

# 产品实物信号
RE_PRODUCT = re.compile(
    r'(实物|实体|产品照|封面|特写|俯视图|设备|原型机|prototype|hardware|device)',
    re.IGNORECASE
)

# 人物肖像信号
RE_PORTRAIT = re.compile(
    r'(肖像|portrait|档案照|面容|pose|headshot|本人)',
    re.IGNORECASE
)

# UI 截图信号
RE_UI = re.compile(
    r'(界面截图|screenshot|操作界面|真实界面|UI\s*截|real\s*UI)',
    re.IGNORECASE
)

# 显式禁止 AI 信号
RE_NO_AI = re.compile(
    r'(严禁.*(?:AI|生成|图像)|禁止.*生成|避免.*AI|真实.*引用|严禁利用)',
    re.IGNORECASE
)

# 著作/书籍封面信号
RE_BOOK = re.compile(
    r'(封面|书籍|著作|教材|专著|原版.*cover|book\s*cover|出版)',
    re.IGNORECASE
)

# ─── 规则 R2: 正文具名实体模式 ───

# 品牌+型号（英文实体，可能跟随中文"遥控器"等）
RE_BRAND_MODEL = re.compile(
    r'(?:Apple\s+USB\s+Mouse|TiVo|Xbox\s+(?:Adaptive|自适应)|'
    r'GRiD\s+Compass|Therac-25|DEC\s+VT100|iMac\s+G3|'
    r'Tesla\s+Model\s+[3SXY]|Boeing\s+737\s*MAX|'
    r'SAP\s+(?:ERP|S/4)|Spotify|Instagram|'
    r'About\s+Face|Interaction\s+Design|Lean\s+UX|'
    r'Dropbox)',
    re.IGNORECASE
)

# 年份+事件
RE_YEAR_EVENT = re.compile(
    r'\b(19[0-9]{2}|20[0-2][0-9])\s*年?\s*(?:.*?(?:事故|事件|灾难|坠毁|宕机|演示|发布|推出))',
    re.IGNORECASE
)

# 人名+职衔
RE_PERSON = re.compile(
    r'(?:Don\s*Norman|Alan\s*Cooper|Douglas\s*Engelbart|Bill\s*Moggridge|'
    r'Bill\s*Verplank|Yvonne\s*Rogers|Harry\s*Brignull|'
    r'Drew\s*Houston|Nick\s*Swinmurn|张小龙|新乡重夫)',
    re.IGNORECASE
)

# ─── 规则 R3: 媒体类型暗示 ───
RE_VIDEO_HINT = re.compile(r'▶️|播放.*素材|播放.*影像|播放.*视频')
RE_CASE_DATE = re.compile(
    r'\[CASE\s*STUDY\].*?(\d{4}\s*年|\d+\s*名.*?(?:死亡|遇难|事故))',
    re.DOTALL
)


@dataclass
class VisualBlock:
    """解析后的 [VISUAL] 块"""
    slide_id: str = ""
    layout: str = ""
    asset_path: str = ""
    scene: str = ""
    text: str = ""
    list_items: str = ""
    source: str = ""       # Source 字段（External/Wikimedia 等标记为已有真实来源）
    source_file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class SourcingItem:
    """一条待搜索素材的记录"""
    slide: str
    module: str
    signals: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    description: str = ""
    scene: str = ""
    search_queries: list = field(default_factory=list)
    target_path: str = ""
    priority: str = "medium"  # high / medium / low
    current_asset: str = ""
    no_ai_flag: bool = False
    already_real: bool = False  # 当前素材已经是真实下载而非 AI 生图


# ─── AI 生图 vs 真实素材 启发式判定 ───
# AI 生成的 PNG 通常在 350KB-950KB 之间 (1024x1024 等标准尺寸)
# 真实照片/截图通常显著偏小(<200KB) 或偏大(>1MB), 或是 JPG/GIF 格式
AI_PNG_SIZE_RANGE = (350_000, 950_000)


def is_asset_already_real(asset_path: str, src_dir: Path) -> bool:
    """启发式判断现有素材是否已经是网络下载的真实图片而非 AI 生图"""
    if not asset_path:
        return False
    # 解析相对路径
    resolved = (src_dir / asset_path).resolve()
    if not resolved.exists():
        return False

    size = resolved.stat().st_size
    suffix = resolved.suffix.lower()

    # GIF / MP4 / JPG 等格式几乎 100% 是真实素材
    if suffix in ('.gif', '.mp4', '.webm', '.jpg', '.jpeg', '.webp'):
        return True

    # 文件名含 _real 后缀
    if '_real' in resolved.stem:
        return True

    # PNG 但大小明显不在 AI 生成的典型区间内
    if suffix == '.png':
        lo, hi = AI_PNG_SIZE_RANGE
        if size < lo or size > hi:
            return True  # 偏小=截图/下载图, 偏大=高分辨率照片

    return False


# ─── 正文上下文多媒体检测 ───
# 匹配 VISUAL 块前后正文中的视频/音频/GIF 嵌入链接
RE_MEDIA_LINK = re.compile(
    r'\]\(([^)]+\.(?:mp4|webm|mov|gif|mp3|wav|ogg|m4a|vtt))\)',
    re.IGNORECASE
)


def has_adjacent_media(filepath: Path, block: 'VisualBlock', radius: int = 5) -> bool:
    """检测 VISUAL 块上下 radius 行的正文中是否已有视频/音频等多媒体引用"""
    lines = filepath.read_text(encoding='utf-8').split('\n')
    # 向下检测（块结束后的正文）
    start = block.line_end  # line_end 是 1-indexed 的下一行
    end = min(len(lines), block.line_end + radius)
    # 向上检测（块开始前的正文）
    up_start = max(0, block.line_start - 1 - radius)
    up_end = block.line_start - 1
    
    context = '\n'.join(lines[start:end]) + '\n' + '\n'.join(lines[up_start:up_end])
    return bool(RE_MEDIA_LINK.search(context))


def parse_visual_blocks(filepath: Path) -> list[VisualBlock]:
    """从 Markdown 文件中解析所有 [VISUAL] 块"""
    text = filepath.read_text(encoding='utf-8')
    lines = text.split('\n')
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        # 检测 [VISUAL] 标记
        if '[VISUAL]' in line:
            block = VisualBlock(source_file=str(filepath), line_start=i + 1)
            # 向后扫描收集块内容
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('>'):
                raw = lines[j].strip().lstrip('> ').strip()

                if raw.startswith('**Slide**:'):
                    block.slide_id = raw.split(':', 1)[1].strip()
                elif raw.startswith('**Layout**:'):
                    block.layout = raw.split(':', 1)[1].strip().strip('`')
                elif ('**Asset**:' in raw or '**Asset ' in raw) and not block.asset_path:
                    # 仅提取第一个出现的 Asset（忽略后续的 AI fallback）
                    m = re.search(r'\(([^)]+)\)', raw)
                    if m:
                        block.asset_path = m.group(1)
                elif raw.startswith('**Scene**:'):
                    block.scene = raw.split(':', 1)[1].strip()
                elif raw.startswith('**Text**:'):
                    block.text = raw.split(':', 1)[1].strip()
                elif raw.startswith('**List**:'):
                    block.list_items = raw.split(':', 1)[1].strip()
                elif raw.startswith('**Source**:'):
                    block.source = raw.split(':', 1)[1].strip()
                j += 1

            block.line_end = j
            blocks.append(block)
            i = j
        else:
            i += 1

    return blocks


def get_context_text(filepath: Path, block: VisualBlock, radius: int = 8) -> str:
    """获取 VISUAL 块周围的正文上下文"""
    lines = filepath.read_text(encoding='utf-8').split('\n')
    start = max(0, block.line_end)
    end = min(len(lines), block.line_end + radius)
    return '\n'.join(lines[start:end])


def analyze_block(block: VisualBlock, context: str) -> Optional[SourcingItem]:
    """分析单个 VISUAL 块，判断是否需要真实素材"""
    item = SourcingItem(
        slide=block.slide_id,
        module=Path(block.source_file).stem,
        scene=block.scene[:200] if block.scene else "",
        current_asset=block.asset_path,
    )

    combined = f"{block.scene} {block.text} {block.list_items} {context}"

    # ─── R1: Scene 关键词触发 ───
    if RE_NO_AI.search(block.scene):
        item.signals.append("explicit_no_ai")
        item.no_ai_flag = True
        item.priority = "high"

    if RE_HISTORY.search(block.scene):
        item.signals.append("historical_archive")

    if RE_PRODUCT.search(block.scene):
        item.signals.append("physical_product")

    if RE_PORTRAIT.search(block.scene):
        item.signals.append("person_portrait")

    if RE_UI.search(block.scene):
        item.signals.append("ui_screenshot")

    if RE_BOOK.search(block.scene) or RE_BOOK.search(block.text):
        item.signals.append("book_cover")

    # ─── R2: 正文实体识别 ───
    brands = RE_BRAND_MODEL.findall(combined)
    if brands:
        item.signals.append("brand_entity")
        item.entities.extend(list(set(brands)))

    persons = RE_PERSON.findall(combined)
    if persons:
        item.signals.append("named_person")
        item.entities.extend(list(set(persons)))

    years = RE_YEAR_EVENT.findall(combined)
    if years:
        item.signals.append("dated_event")

    # ─── R3: 媒体类型暗示 ───
    if RE_VIDEO_HINT.search(context):
        item.signals.append("video_hint")

    # ─── 判定优先级 ───
    if not item.signals:
        return None  # 无信号，跳过

    # 高优先级条件
    high_signals = {"explicit_no_ai", "historical_archive", "physical_product"}
    if item.signals and high_signals.intersection(item.signals):
        item.priority = "high"
    elif len(item.signals) >= 2:
        item.priority = "high"
    elif "ui_screenshot" in item.signals or "named_person" in item.signals:
        item.priority = "medium"
    else:
        item.priority = "low"

    # ─── 生成搜索建议 ───
    item.search_queries = generate_search_queries(block, item)
    item.description = block.text or block.scene[:80]
    item.target_path = f"../public/slides/{block.slide_id}_real.png"

    return item


def generate_search_queries(block: VisualBlock, item: SourcingItem) -> list[str]:
    """根据实体和信号生成推荐搜索词"""
    queries = []

    for entity in item.entities[:3]:
        # 基础搜索
        queries.append(f"{entity} photo")
        queries.append(f"{entity} real image")

        # 如果是产品，加上产品图关键词
        if "physical_product" in item.signals:
            queries.append(f"{entity} product shot high resolution")

        # 如果是人物，加上肖像关键词
        if "named_person" in item.signals:
            queries.append(f"{entity} portrait")

    # 如果有 UI 截图信号
    if "ui_screenshot" in item.signals and not queries:
        scene_keywords = block.scene[:50].replace("，", " ").replace("。", " ")
        queries.append(f"{scene_keywords} screenshot")

    # 如果有历史档案信号
    if "historical_archive" in item.signals and not queries:
        queries.append(f"{block.text} historical photo")
        queries.append(f"{block.text} archive image")

    return queries[:5]  # 最多 5 条建议


def scan_directory(src_dir: Path) -> list[SourcingItem]:
    """扫描目录下所有 .md 文件"""
    results = []
    skipped_real = 0
    md_files = sorted(src_dir.glob("M*.md"))

    for md_file in md_files:
        print(f"  📖 扫描: {md_file.name}")
        blocks = parse_visual_blocks(md_file)
        print(f"     发现 {len(blocks)} 个 [VISUAL] 块")

        for block in blocks:
            # ─── 防重复三层检测 ───
            # 层1: Asset 文件本身已是真实素材（格式/大小/命名）
            if is_asset_already_real(block.asset_path, md_file.parent):
                skipped_real += 1
                continue
            # 层2: Source 字段标记为外部来源（已人工确认）
            if block.source and any(kw in block.source.lower() for kw in
                    ('external', 'wikimedia', 'wikipedia', 'cc ', 'cc-by',
                     'fair use', 'press kit', '新华社', '央视', 'screenshot', 'video')):
                skipped_real += 1
                continue
            # 层3: 块周围正文已有视频/音频等多媒体引用
            if has_adjacent_media(md_file, block):
                skipped_real += 1
                continue

            context = get_context_text(md_file, block)
            item = analyze_block(block, context)
            if item:
                results.append(item)

    if skipped_real:
        print(f"  ⏭️  跳过 {skipped_real} 个已拥有真实素材的位置")

    return results


def output_yaml(items: list[SourcingItem], output_path: Path):
    """输出 YAML 格式的待办清单"""
    # 按优先级排序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: priority_order.get(x.priority, 99))

    data = []
    for item in items:
        entry = {
            "slide": item.slide,
            "module": item.module,
            "priority": item.priority,
            "signals": item.signals,
            "entities": item.entities,
            "description": item.description,
            "scene_excerpt": item.scene,
            "search_queries": item.search_queries,
            "target_path": item.target_path,
            "current_asset": item.current_asset,
            "no_ai_flag": item.no_ai_flag,
        }
        data.append(entry)

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(
            data, f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )

    print(f"\n✅ 已输出 {len(data)} 条记录到: {output_path}")


def print_summary(items: list[SourcingItem]):
    """打印控制台摘要"""
    high = sum(1 for i in items if i.priority == "high")
    medium = sum(1 for i in items if i.priority == "medium")
    low = sum(1 for i in items if i.priority == "low")
    no_ai = sum(1 for i in items if i.no_ai_flag)
    books = sum(1 for i in items if "book_cover" in i.signals)

    print("\n" + "=" * 50)
    print("  📊 扫描结果汇总")
    print("=" * 50)
    print(f"  🔴 高优先级 (CRITICAL):  {high}")
    print(f"  🟡 中优先级 (ENHANCE):   {medium}")
    print(f"  🟢 低优先级 (OPTIONAL):  {low}")
    print(f"  🚫 显式禁止 AI 生成:     {no_ai}")
    print(f"  📚 著作/书籍封面:        {books}")
    print(f"  📋 总计待处理:           {len(items)}")
    print("=" * 50)

    if high > 0:
        print("\n  ⚡ 高优先级清单:")
        for item in items:
            if item.priority == "high":
                entities_str = ", ".join(item.entities[:3]) if item.entities else "N/A"
                flag = " 🚫NO-AI" if item.no_ai_flag else ""
                print(f"    • [{item.slide}] {item.description[:40]}...  "
                      f"[{', '.join(item.signals[:3])}] "
                      f"实体: {entities_str}{flag}")


def main():
    """主入口"""
    if len(sys.argv) < 2:
        # 默认扫描当前目录
        target = Path(__file__).parent
    else:
        target = Path(sys.argv[1])

    if target.is_file():
        src_dir = target.parent
        print(f"🔍 扫描单个文件: {target.name}")
    elif target.is_dir():
        src_dir = target
        print(f"🔍 扫描目录: {src_dir}")
    else:
        print(f"❌ 路径不存在: {target}")
        sys.exit(1)

    items = scan_directory(src_dir)
    print_summary(items)

    output_path = src_dir / "sourcing_checklist.yaml"
    output_yaml(items, output_path)


if __name__ == "__main__":
    main()
