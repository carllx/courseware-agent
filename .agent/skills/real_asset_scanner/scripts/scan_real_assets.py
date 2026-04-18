#!/usr/bin/env python3
"""
逐字稿网络素材需求扫描引擎 (Real-Asset Sourcing Scanner)

扫描 Markdown 逐字稿中的 [VISUAL] 块和正文，识别适合从网络搜索/下载真实素材
（而非 AI 文生图）的视觉位置。

架构：三层实体识别
  层1: Gazetteer — 课程级外部词典 (scanner_entities.yaml)，精确匹配，最高优先级
  层2: 结构模式 — 通用正则（大写多词组 / 连字符型号 / CamelCase），课程无关
  层3: 上下文信号 — Scene 字段 S1-S6 关键词检测

用法:
    python scan_real_assets.py [脚本目录或单个.md文件]
    
输出:
    sourcing_checklist.yaml — 按优先级排序的待办清单
"""

import re
import sys
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ═══════════════════════════════════════════════════════════
# 层3: 上下文信号 — Scene 字段关键词模式 (S1-S6, 课程无关)
# ═══════════════════════════════════════════════════════════

# S1: 历史事件信号
RE_HISTORY = re.compile(
    r'(真实|实录|纪实|档案|历史|原版|original|authentic|real\b|archival)',
    re.IGNORECASE
)

# S2: 产品实物信号 (Scene 字段)
RE_PRODUCT = re.compile(
    r'(实物|实体|产品照|封面|特写|俯视图|设备|原型机|prototype|hardware|device)',
    re.IGNORECASE
)

# S3: 人物肖像信号
RE_PORTRAIT = re.compile(
    r'(肖像|portrait|档案照|面容|pose|headshot|本人)',
    re.IGNORECASE
)

# S4: UI 截图信号
RE_UI = re.compile(
    r'(界面截图|screenshot|操作界面|真实界面|UI\s*截|real\s*UI)',
    re.IGNORECASE
)

# S5: 显式禁止 AI 信号
RE_NO_AI = re.compile(
    r'(严禁.*(?:AI|生成|图像)|禁止.*生成|避免.*AI|真实.*引用|严禁利用)',
    re.IGNORECASE
)

# S6: 著作/书籍封面信号
RE_BOOK = re.compile(
    r'(封面|书籍|著作|教材|专著|原版.*cover|book\s*cover|出版)',
    re.IGNORECASE
)

# ═══════════════════════════════════════════════════════════
# 层2: 通用结构模式 — 课程无关的具名实体特征检测
# ═══════════════════════════════════════════════════════════

# 通用停用词：排除被大写多词组模式误捕获的常见短语
ENTITY_STOPWORDS = {
    # 英文功能词组合
    'The Great', 'In This', 'On The', 'At The', 'For The',
    'With The', 'And The', 'But The', 'From The', 'Into The',
    'Visual Perception', 'Cognitive Load', 'Information Processing',
    'Data Visualization', 'User Experience', 'Design Thinking',
    'Machine Learning', 'Deep Learning', 'Natural Language',
    'Open Source', 'Real Time', 'High Resolution',
    'Case Study', 'Best Practice', 'Key Point',
    # 常见教学术语
    'Slide Show', 'Story Time', 'Check Point',
    'Quick Review', 'Pop Quiz', 'Think About',
    # 编程语言/技术术语（非具名实体）
    'JavaScript', 'TypeScript', 'Python', 'Java',
    'HTML', 'CSS', 'React', 'Angular', 'Vue',
}

# P1: 英文大写多词组专名 (≥2 词, 首字母大写)
#     匹配: "Florence Nightingale", "Charles Minard", "Don Norman"
#     排除: 以常见介词/冠词开头的短语
RE_CAPITALIZED_NAME = re.compile(
    r'\b(?!(?:The|In|On|At|For|With|And|But|Or|If|So|As|To|By|Of|Is|It|We|Do|No|Up)\s)'
    r'([A-Z][a-z]{1,15}(?:\s+(?:de|von|van|la|el|al|bin|Le|Des|Du)\s+)?'
    r'[A-Z][a-z]{1,15}(?:\s+[A-Z][a-z]{1,15}){0,2})\b'
)

# P2: 连字符技术标识 (品牌-型号 / 技术代号)
#     匹配: "Therac-25", "Boeing-737", "VT-100", "S/4HANA"
RE_HYPHENATED_ID = re.compile(
    r'\b([A-Z][a-zA-Z]*-\d+[A-Za-z]*)\b'
)

# P3: CamelCase / 混合大小写产品名
#     匹配: "TiVo", "iMac", "iPad", "YouTube", "GitHub", "D3"
#     排除: 常见缩写如 "Hz", "MHz"
RE_CAMELCASE = re.compile(
    r'\b([a-z]+[A-Z][a-zA-Z]+)\b'
)

# P4: 全大写缩写 + 空格 + 标识 (≥2 字母)
#     匹配: "DEC VT100", "IBM PC", "SAP ERP", "AWS S3"
RE_ACRONYM_PRODUCT = re.compile(
    r'\b([A-Z]{2,6}\s+[A-Z][a-zA-Z0-9]+(?:\s+[A-Z0-9][a-zA-Z0-9]*)?)\b'
)

# P5: 中文书名号/引号包裹的专名
#     匹配: 《可视化数据》、《About Face》、「交互设计精髓」
RE_CHINESE_TITLE = re.compile(
    r'[《「]([^》」]{2,30})[》」]'
)

# ─── 辅助匹配：年份+事件/媒体类型暗示 ───

RE_YEAR_EVENT = re.compile(
    r'\b(19[0-9]{2}|20[0-2][0-9])\s*年?\s*(?:.*?(?:事故|事件|灾难|坠毁|宕机|演示|发布|推出))',
    re.IGNORECASE
)

RE_VIDEO_HINT = re.compile(r'▶️|播放.*素材|播放.*影像|播放.*视频')


# ═══════════════════════════════════════════════════════════
# 层1: Gazetteer — 课程级外部词典加载
# ═══════════════════════════════════════════════════════════

def load_course_gazetteer(src_dir: Path) -> dict:
    """
    从 src_dir 向上最多遍历 3 层查找 scanner_entities.yaml。
    返回 {'brands': set, 'persons': set, 'products': set}。
    找不到时返回空集合（零配置降级）。
    """
    gazetteer = {'brands': set(), 'persons': set(), 'products': set()}
    search_dir = src_dir.resolve()

    for _ in range(4):  # src → week → weeks → course root
        candidate = search_dir / 'scanner_entities.yaml'
        if candidate.exists():
            try:
                with open(candidate, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                for key in ('brands', 'persons', 'products'):
                    if key in data and isinstance(data[key], list):
                        gazetteer[key] = set(data[key])
                print(f"  📚 加载课程词典: {candidate.relative_to(src_dir.parent.parent.parent) if src_dir.parent.parent.parent in candidate.parents else candidate.name}")
                print(f"     品牌/产品: {len(gazetteer['brands'])} | 人物: {len(gazetteer['persons'])} | 设备: {len(gazetteer['products'])}")
            except Exception as e:
                print(f"  ⚠️  词典加载失败: {e}")
            break  # 找到即停止
        search_dir = search_dir.parent
        if search_dir == search_dir.parent:
            break  # 已到根

    return gazetteer


def match_gazetteer(text: str, gazetteer: dict) -> tuple[list[str], list[str]]:
    """
    在文本中精确匹配 Gazetteer 词条。
    返回 (匹配到的实体列表, 信号类型列表)。
    """
    entities = []
    signals = []

    all_terms = {}
    for key in ('brands', 'persons', 'products'):
        for term in gazetteer.get(key, set()):
            all_terms[term] = key

    # 按长度降序匹配，避免短词吞噬长词的子串
    for term in sorted(all_terms.keys(), key=len, reverse=True):
        if term in text:
            entities.append(term)
            category = all_terms[term]
            if category == 'brands':
                signals.append('gazetteer_brand')
            elif category == 'persons':
                signals.append('gazetteer_person')
            elif category == 'products':
                signals.append('gazetteer_product')

    return list(dict.fromkeys(entities)), list(dict.fromkeys(signals))


# ═══════════════════════════════════════════════════════════
# 通用实体提取（层2 结构模式）
# ═══════════════════════════════════════════════════════════

def extract_entities_generic(text: str) -> tuple[list[str], list[str]]:
    """
    使用通用结构模式从文本中提取候选具名实体。
    返回 (候选实体列表, 信号类型列表)。
    """
    entities = []
    signals = []

    # P1: 大写多词组专名
    for m in RE_CAPITALIZED_NAME.finditer(text):
        name = m.group(1).strip()
        if name not in ENTITY_STOPWORDS and len(name) > 3:
            entities.append(name)
            signals.append('named_entity')

    # P2: 连字符技术标识
    for m in RE_HYPHENATED_ID.finditer(text):
        entities.append(m.group(1))
        signals.append('tech_identifier')

    # P3: CamelCase 产品名
    for m in RE_CAMELCASE.finditer(text):
        word = m.group(1)
        # 排除常见非实体 CamelCase（如 fontSize, backgroundColor）
        if not any(word.lower().startswith(p) for p in ('font', 'background', 'text', 'color', 'border', 'margin', 'padding')):
            entities.append(word)
            signals.append('camelcase_product')

    # P4: 缩写+标识
    for m in RE_ACRONYM_PRODUCT.finditer(text):
        candidate = m.group(1).strip()
        # 排除纯缩写短语如 "AI AND", "HTML CSS"
        if not all(c.isupper() or c.isspace() for c in candidate):
            entities.append(candidate)
            signals.append('acronym_product')

    # P5: 中文书名号专名
    for m in RE_CHINESE_TITLE.finditer(text):
        entities.append(m.group(1))
        signals.append('book_title')

    # 去重并保持顺序
    seen = set()
    unique_entities = []
    unique_signals = []
    for e, s in zip(entities, signals):
        if e not in seen:
            seen.add(e)
            unique_entities.append(e)
            unique_signals.append(s)

    return unique_entities, unique_signals


# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

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
    slide: str = ""
    module: str = ""
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
                # 剥离 Markdown 列表项标记 `*   ` 或 `-   `
                raw = re.sub(r'^[*\-]\s+', '', raw)

                if raw.startswith('**Slide**:'):
                    # 修复：剥离反引号、星号等包裹字符
                    block.slide_id = raw.split(':', 1)[1].strip().strip('`').strip('*').strip()
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


# ═══════════════════════════════════════════════════════════
# 核心分析引擎（三层优先级冲突解决）
# ═══════════════════════════════════════════════════════════

def analyze_block(block: VisualBlock, context: str, gazetteer: dict) -> Optional[SourcingItem]:
    """
    分析单个 VISUAL 块，判断是否需要真实素材。
    
    三层优先级：
      层1 Gazetteer 命中 → 可独立触发 HIGH
      层2 结构模式 + S1-S6 共振 → 可触发 HIGH
      层2 结构模式 (单独) → 仅 LOW
      层3 S1-S6 信号 (无实体) → MEDIUM
    """
    item = SourcingItem(
        slide=block.slide_id,
        module=Path(block.source_file).stem,
        scene=block.scene[:200] if block.scene else "",
        current_asset=block.asset_path,
    )

    combined = f"{block.scene} {block.text} {block.list_items} {context}"

    # ─── 层3: Scene 关键词信号检测 (S1-S6) ───
    context_signals = []

    if RE_NO_AI.search(block.scene):
        context_signals.append("explicit_no_ai")
        item.no_ai_flag = True

    if RE_HISTORY.search(block.scene):
        context_signals.append("historical_archive")

    if RE_PRODUCT.search(block.scene):
        context_signals.append("physical_product")

    if RE_PORTRAIT.search(block.scene):
        context_signals.append("person_portrait")

    if RE_UI.search(block.scene):
        context_signals.append("ui_screenshot")

    if RE_BOOK.search(block.scene) or RE_BOOK.search(block.text):
        context_signals.append("book_cover")

    # 辅助信号
    if RE_YEAR_EVENT.search(combined):
        context_signals.append("dated_event")

    if RE_VIDEO_HINT.search(context):
        context_signals.append("video_hint")

    # ─── 层1: Gazetteer 精确匹配 ───
    gaz_entities, gaz_signals = match_gazetteer(combined, gazetteer)

    # ─── 层2: 通用结构模式提取 ───
    gen_entities, gen_signals = extract_entities_generic(combined)

    # ─── 合并实体和信号 ───
    all_entities = list(dict.fromkeys(gaz_entities + gen_entities))
    all_signals = list(dict.fromkeys(context_signals + gaz_signals + gen_signals))

    item.entities = all_entities
    item.signals = all_signals

    # ─── 三层优先级冲突解决 ───
    has_gazetteer = bool(gaz_entities)
    has_context_signal = bool(context_signals)
    has_structural = bool(gen_entities)

    # 无任何信号 → 跳过
    if not all_signals:
        return None

    # explicit_no_ai 始终最高优先级
    if item.no_ai_flag:
        item.priority = "high"
    # 层1: Gazetteer 命中 → 可独立触发 HIGH
    elif has_gazetteer:
        item.priority = "high"
    # 层2 + 层3 共振 → HIGH
    elif has_structural and has_context_signal:
        item.priority = "high"
    # 层3 单独 (含强信号) → MEDIUM
    elif has_context_signal:
        strong_context = {"historical_archive", "physical_product", "person_portrait", "ui_screenshot"}
        if strong_context.intersection(context_signals):
            item.priority = "medium"
        else:
            item.priority = "low"
    # 层2 单独 (无上下文共振) → LOW
    elif has_structural:
        item.priority = "low"
    else:
        item.priority = "low"

    # ─── 生成搜索建议 ───
    item.search_queries = generate_search_queries(block, item)
    item.description = block.text or block.scene[:80] if block.scene else ""
    item.target_path = f"../public/slides/{block.slide_id}_real.png" if block.slide_id else ""

    return item


def generate_search_queries(block: VisualBlock, item: SourcingItem) -> list[str]:
    """根据实体和信号生成推荐搜索词"""
    queries = []

    for entity in item.entities[:3]:
        # 基础搜索
        queries.append(f"{entity} photo")
        queries.append(f"{entity} real image")

        # 如果是产品，加上产品图关键词
        if any(s in item.signals for s in ("physical_product", "gazetteer_product", "tech_identifier")):
            queries.append(f"{entity} product shot high resolution")

        # 如果是人物，加上肖像关键词
        if any(s in item.signals for s in ("person_portrait", "gazetteer_person", "named_entity")):
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


# ═══════════════════════════════════════════════════════════
# 目录扫描与输出
# ═══════════════════════════════════════════════════════════

def scan_directory(src_dir: Path) -> list[SourcingItem]:
    """扫描目录下所有 .md 文件"""
    results = []
    skipped_real = 0
    skipped_locked = 0
    md_files = sorted(src_dir.glob("M*.md"))

    # 加载课程级 Gazetteer（可选，找不到则零配置运行）
    gazetteer = load_course_gazetteer(src_dir)

    for md_file in md_files:
        print(f"  📖 扫描: {md_file.name}")
        blocks = parse_visual_blocks(md_file)
        print(f"     发现 {len(blocks)} 个 [VISUAL] 块")

        for block in blocks:
            # ─── 防重复四层检测 ───
            # 层0 (最高优先): Source 字段含 `Locked` — 人工决策锁定，不再搜索
            if block.source and 'locked' in block.source.lower():
                skipped_locked += 1
                continue
            # 层1: Asset 文件本身已是真实素材（格式/大小/命名）
            if is_asset_already_real(block.asset_path, md_file.parent):
                skipped_real += 1
                continue
            # 层2: Source 字段标记为外部来源（已人工确认）
            if block.source and any(kw in block.source.lower() for kw in
                    ('external', 'wikimedia', 'wikipedia', 'cc ', 'cc-by',
                     'fair use', 'press kit', '新华社', '央视', 'screenshot', 'video', 'generated realism')):
                skipped_real += 1
                continue
            # 层3: 块周围正文已有视频/音频等多媒体引用
            if has_adjacent_media(md_file, block):
                skipped_real += 1
                continue

            context = get_context_text(md_file, block)
            item = analyze_block(block, context, gazetteer)
            if item:
                results.append(item)

    if skipped_locked:
        print(f"  🔒 跳过 {skipped_locked} 个人工锁定的位置")
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
