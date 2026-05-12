#!/usr/bin/env python3
"""
教师备课套件生成器 (Teacher's Cheat Sheet Generator)

从 Markdown 逐字稿自动生成：
1. Visual-First 双轨骨架卡片（30 秒扫读版）
2. SCQA 冷热情绪弧线图（ASCII）
3. 灵魂锚词故事线
4. 段落推进率诊断 (IAR)
5. 渐进脱稿提示（5 级）

用法:
    python generate_cheat_sheet.py <脚本路径> [--level N] [--diagnose]
    
    --level N     输出指定渐进脱稿层级 (1-5)，默认输出全部概览
    --diagnose    输出段落推进率诊断（IAR 分析 + 问题标记）
    --output DIR  输出目录（默认打印到终端）

依赖: script_parser.py（同目录）
"""

import sys
import os
import re
import argparse
from pathlib import Path

# 将 script_parser 所在目录加入搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent))
from script_parser import parse_script, BlockType, ScriptBlock, strip_markdown


# ===== 常量 =====

# 标签 → 温度映射（来自研究报告 §方法4）
HOT_TAGS = {"STORY TIME", "CASE STUDY", "LIFE CONNECT", "PHILOSOPHY", "DID YOU KNOW"}
COLD_TAGS = {"TEACHING MOMENT", "TECH NOTE", "WARNING"}
RHYTHM_TAGS = {"ACTIVITY", "PACING"}

# 标签 → 颜色映射（来自研究报告 §方法4 色彩编码方案）
TAG_COLORS = {
    "TEACHING MOMENT": ("🟡", "黄", "🧊冷：必须逐字精确的顿悟金句"),
    "STORY TIME":      ("🟢", "绿", "🔥热：感性火花，可大白话发散"),
    "CASE STUDY":      ("🟢", "绿", "🔥热：案例实证，记核心数据"),
    "LIFE CONNECT":    ("🟢", "绿", "🔥热：生活共鸣，可自由展开"),
    "PHILOSOPHY":      ("🟢", "绿", "🔥热：哲学思辨，记核心命题"),
    "TECH NOTE":       ("🔵", "蓝", "🧊冷：技术锚定，精确术语"),
    "WARNING":         ("🔵", "蓝", "🧊冷：操作警告，精确表述"),
    "DID YOU KNOW":    ("🔵", "蓝", "🔥热：认知惊喜，趣味触发"),
    "ACTIVITY":        ("🟣", "紫", "节奏断点/身体参与"),
    "PACING":          ("🟣", "紫", "演讲乐谱/情绪走位"),
}

# Layout → 记忆宫殿空间映射（来自研究报告 §方法2）
LAYOUT_PALACE = {
    "Center": "🏛️ 开阔大厅（聚焦核心概念）",
    "Split": "🚪 双面长廊（论据 A vs B）",
    "Comparison": "🚪 双面长廊（正反对照）",
    "Grid": "🪟 四窗展览室（多要点并列）",
    "Full": "🎬 沉浸影院（情感冲击/全屏画面）",
    "Screenshot": "🖥️ 操作台（实操演示）",
    "Quote": "📜 语录厅（金句引言）",
    "CTA": "🎯 行动号召台",
    "Flow": "🔄 流程走廊",
    "Title": "🚩 入口门厅",
}


def get_layout_palace(layout: str) -> str:
    """获取 Layout 对应的记忆宫殿空间描述。"""
    return LAYOUT_PALACE.get(layout, f"📍 {layout}")


def get_temperature(block: ScriptBlock) -> str:
    """判断块的温度属性：🔥热/🧊冷/—。"""
    tag = block.metadata.get("tag_name", "")
    if tag in HOT_TAGS:
        return "🔥"
    if tag in COLD_TAGS:
        return "🧊"
    if tag in RHYTHM_TAGS:
        return "🟣"
    return ""


def chinese_char_count(text: str) -> int:
    """统计中文字符数（含中文标点）。"""
    return len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))


# ===== 结构提取 =====

class ModuleInfo:
    """一个教学模块（## 级别）的结构化信息。"""
    def __init__(self, title: str, level: int, line_start: int):
        self.title = title
        self.level = level
        self.line_start = line_start
        self.sections = []       # (title, level, line_start) 的 H3/H4 列表
        self.visuals = []        # (slide_id, layout, scene_summary, line_start) 列表
        self.visual_blocks = []  # 完整 ScriptBlock 列表（用于视觉记忆诊断）
        self.tags = []           # (tag_name, temperature, content_preview, line_start) 列表
        self.activities = []     # (desc, duration, line_start) 列表
        self.speech_blocks = []  # ScriptBlock 列表
        self.paragraphs = []     # (text, char_count, classification) 列表


def extract_modules(blocks: list[ScriptBlock]) -> list[ModuleInfo]:
    """将 ScriptBlock 列表组织为 ModuleInfo 树。"""
    modules = []
    current_module = None

    for b in blocks:
        if b.block_type == BlockType.HEADER:
            level = b.metadata.get("level", 1)
            if level == 2:
                current_module = ModuleInfo(b.content, level, b.line_start)
                modules.append(current_module)
            elif level in (3, 4) and current_module:
                current_module.sections.append((b.content, level, b.line_start))
        
        elif b.block_type == BlockType.VISUAL and current_module:
            sid = b.metadata.get("slide_id", "??")
            layout = b.metadata.get("layout", "??")
            scene = b.metadata.get("scene", "")
            # 截取 Scene 前 40 字作为摘要
            scene_summary = scene[:40] + "..." if len(scene) > 40 else scene
            current_module.visuals.append((sid, layout, scene_summary, b.line_start))
            current_module.visual_blocks.append(b)  # 保留完整 block 用于视觉记忆诊断
        
        elif b.block_type == BlockType.ACTIVITY and current_module:
            desc = b.metadata.get("desc", b.content[:30])
            dur = b.metadata.get("duration_raw", "??")
            current_module.activities.append((desc, dur, b.line_start))
        
        elif b.block_type in (BlockType.SPEECH, BlockType.TAG) and current_module:
            tag = b.metadata.get("tag_name", "")
            if tag:
                temp = get_temperature(b)
                preview = strip_markdown(b.content)[:50]
                current_module.tags.append((tag, temp, preview, b.line_start))
            if b.block_type == BlockType.SPEECH:
                current_module.speech_blocks.append(b)
                text = strip_markdown(b.content)
                if text.strip():
                    cc = chinese_char_count(text)
                    # 存储原始内容(b.content)，用于加粗标记检测；cc 基于清洗后文本
                    current_module.paragraphs.append((b.content.strip(), cc, ""))

    return modules


# ===== 输出生成 =====

def _get_section_range(sections, idx):
    """获取第 idx 个 section 的行号范围 [start, next_start)。"""
    start = sections[idx][2]  # line_start
    if idx + 1 < len(sections):
        end = sections[idx + 1][2]
    else:
        end = float('inf')
    return start, end


def generate_skeleton(modules: list[ModuleInfo], script_name: str) -> str:
    """生成 Visual-First 双轨骨架卡片。"""
    lines = []
    lines.append(f"# 📋 骨架卡片：{script_name}")
    lines.append(f"# （30 秒扫读版 — 标题即脉络，Slide 即记忆宫殿）\n")

    for mod in modules:
        lines.append(f"## {mod.title}")
        lines.append("")

        if not mod.sections:
            # 无 H3/H4 标题时，直接列出所有 Visuals
            for sid, layout, scene, _ in mod.visuals:
                palace = get_layout_palace(layout)
                lines.append(f"  🔴 [{layout}: {scene}]")
                lines.append(f"     {palace}")
            lines.append("")
            continue

        for sec_idx, (sec_title, sec_level, sec_line) in enumerate(mod.sections):
            indent = "  " if sec_level == 4 else ""
            prefix = "├──" if sec_level == 3 else "│   └──"
            sec_start, sec_end = _get_section_range(mod.sections, sec_idx)

            # 输出此 Section 范围内的 VISUAL（按行号就近关联）
            for sid, layout, scene, vis_line in mod.visuals:
                if sec_start <= vis_line < sec_end:
                    palace = get_layout_palace(layout)
                    lines.append(f"{indent}  🔴 [{layout}: {scene}]")
                    lines.append(f"{indent}     {palace}")

            lines.append(f"{indent}{prefix} {sec_title}")

            # 输出此 Section 范围内的标签（按行号就近关联）
            for tag_name, temp, preview, tag_line in mod.tags:
                if sec_start <= tag_line < sec_end:
                    if tag_name in HOT_TAGS or tag_name in COLD_TAGS:
                        lines.append(f"{indent}│       {temp} [{tag_name}] {preview[:40]}")

        # 活动
        for desc, dur, _ in mod.activities:
            lines.append(f"  🟣 ACTIVITY: {desc} ({dur})")

        # 模块头部的 Visuals（在第一个 section 之前）
        first_sec_line = mod.sections[0][2] if mod.sections else float('inf')
        for sid, layout, scene, vis_line in mod.visuals:
            if vis_line < first_sec_line:
                palace = get_layout_palace(layout)
                lines.insert(-len(mod.activities) if mod.activities else len(lines),
                             f"  🔴 [{layout}: {scene}]")

        lines.append("")

    return "\n".join(lines)


def generate_anchor_words(modules: list[ModuleInfo]) -> str:
    """为每个 H3 块提取灵魂锚词，串联为故事线。"""
    lines = []
    lines.append("# 🔑 灵魂锚词故事线\n")
    lines.append("> 每个 ### 块的核心提取为 ≤4 字的关键词。")
    lines.append("> 串联后应构成逻辑故事线，而非随机拼凑。\n")

    for mod in modules:
        lines.append(f"## {mod.title}")
        anchors = []
        for sec_title, sec_level, _ in mod.sections:
            if sec_level == 3:
                # 提取标题中的核心关键词
                # 去掉编号前缀（如 "1.1 "）
                clean = re.sub(r'^\d+\.\d+\s*', '', sec_title)
                # 标题格式通常是「断言：详细描述」
                # 取冒号前的断言式概括作为锚词（更精炼）
                if '：' in clean:
                    anchor_raw = clean.split('：')[0]
                elif ':' in clean:
                    anchor_raw = clean.split(':')[0]
                else:
                    anchor_raw = clean
                # 从中文文本中提取核心名词短语（≤4字）
                anchor_raw = anchor_raw.strip()
                cn_chars = re.findall(r'[\u4e00-\u9fff]', anchor_raw)
                if len(cn_chars) >= 2:
                    anchor = ''.join(cn_chars[:4])
                else:
                    anchor = anchor_raw[:6]
                anchors.append(anchor)
                lines.append(f"  {sec_title}")
                lines.append(f"    \u2192 \u951a\u8bcd\uff1a\u300c{anchor}\u300d")

        if anchors:
            chain = " \u2192 ".join(f"\u300c{a}\u300d" for a in anchors)
            lines.append(f"\n  📖 故事线：{chain}")
        lines.append("")

    return "\n".join(lines)


def generate_emotional_arc(modules: list[ModuleInfo]) -> str:
    """生成 SCQA 冷热情绪弧线图（ASCII）。"""
    lines = []
    lines.append("# 🌡️ 冷热情绪弧线\n")
    lines.append("> 🔥 = 感性火花（故事/案例/哲学）  🧊 = 精准结论（金句/技术）  🟣 = 节奏断点\n")

    for mod in modules:
        lines.append(f"## {mod.title}")
        lines.append("")
        
        # 收集事件序列
        events = []
        for b in mod.speech_blocks:
            tag = b.metadata.get("tag_name", "")
            temp = get_temperature(b)
            if temp:
                preview = strip_markdown(b.content)[:25].replace("\n", " ")
                events.append((temp, tag, preview))

        for desc, dur, _ in mod.activities:
            events.append(("\ud83d\udfe3", "ACTIVITY", desc))

        if not events:
            lines.append("  （无冷热标签检测到）")
            lines.append("")
            continue

        # 绘制简化弧线
        arc_line = "  "
        label_line = "  "
        for temp, tag, preview in events:
            if temp == "🔥":
                arc_line += "  ╱╲  "
                label_line += f" {tag[:8]:^6s}"
            elif temp == "🧊":
                arc_line += "  ╲╱  "
                label_line += f" {tag[:8]:^6s}"
            elif temp == "🟣":
                arc_line += "  ⟳   "
                label_line += f" {'活动':^6s}"

        lines.append(f"  温度 ▲")
        lines.append(f"  🔥  │{arc_line}")
        lines.append(f"  ──  │{'─' * len(arc_line)}")
        lines.append(f"  🧊  │")
        lines.append(f"      └{'─' * len(arc_line)}→ 时间")
        lines.append(f"       {label_line}")
        lines.append("")

    return "\n".join(lines)


def _extract_cn_chars(text: str) -> list[str]:
    """提取文本中的所有中文字符（用于跨段落重叠检测）。"""
    return re.findall(r'[\u4e00-\u9fff]', text)


def classify_paragraph(text: str, prev_text: str = "") -> str:
    """对段落进行 A/S/R 分类（v2 — 修复 6 项已知漏洞）。
    
    A(推进)：引入新概念/新证据/新案例 
    S(支撑)：对已有概念的展开、举例
    R(冗余)：换角度重述/总结套话
    
    v2 变更日志：
    - Bug1: 冗余信号词仅在段首 30 字或独立成句时匹配（防引语陷阱误杀）
    - Bug2: 追加中文人名和括号英文名的推进信号
    - Bug3: 追加因果连接词作为内容级推进信号
    - Bug4: 百分比数据需附带变化动词上下文
    - Bug5: 利用 prev_text 做跨段落中文字符重叠检测
    - Bug6: IAR 公式改为加权版本（在 generate_iar_diagnosis 中实现）
    """
    clean_text = strip_markdown(text) if text else ""
    
    # === Bug5: 跨段落隐性重述检测 ===
    # 如果当前段的前 20 个中文字符与上一段的前 20 个重叠率 > 70%，判定为隐性重述
    if prev_text:
        curr_chars = _extract_cn_chars(clean_text)[:20]
        prev_chars = _extract_cn_chars(strip_markdown(prev_text))[:20]
        if len(curr_chars) >= 8 and len(prev_chars) >= 8:
            overlap = len(set(curr_chars) & set(prev_chars))
            overlap_rate = overlap / min(len(set(curr_chars)), len(set(prev_chars)))
            if overlap_rate > 0.70:
                return "R"
    
    # === Bug1: 冗余信号词 — 段首 30 字约束 ===
    # 仅当信号词出现在段落开头 30 字以内时才判定为冗余，防止引语中的误杀
    redundancy_signals = ["总之", "换句话说", "也就是说", "简单来讲", "归根结底", 
                          "回顾一下", "我们刚才讲了", "综上"]
    head_30 = clean_text[:30]
    for sig in redundancy_signals:
        if sig in head_30:
            return "R"
    
    # === 推进信号检测 ===
    advancement_signals = [
        re.compile(r'[\d]{4}\s*年'),       # 年份
        re.compile(r'《.+?》'),            # 书名号引用
        # Bug2: 追加英文人名的多种出现形式
        re.compile(r'[A-Z][a-z]+\s+[A-Z]'),              # 标准英文人名 (Richard Thaler)
        re.compile(r'[\u4e00-\u9fff]{1,2}·[\u4e00-\u9fff]'),  # 中文音译名 (丹尼尔·卡尼曼)
        re.compile(r'（[A-Z][a-z]+[\s\w]*）'),              # 括号内英文全名 （Richard Thaler）
    ]
    for pat in advancement_signals:
        if pat.search(text):
            return "A"
    
    # Bug4: 百分比数据需附带变化动词上下文
    pct_match = re.search(r'[\d]+[%％]', text)
    if pct_match:
        # 在百分比前后 15 字范围内检查是否有变化动词
        start = max(0, pct_match.start() - 15)
        end = min(len(text), pct_match.end() + 15)
        context = text[start:end]
        change_verbs = ["增长", "下降", "暴跌", "提升", "减少", "超过", "达到",
                        "上升", "降低", "翻倍", "占比", "比例", "份额", "增加"]
        if any(v in context for v in change_verbs):
            return "A"
    
    # 新概念引号标记（**粗体**通常标记新术语）
    if re.search(r'\*\*[^*]+\*\*', text):
        return "A"
    
    # Bug3: 因果连接词作为内容级推进信号
    # 段首出现因果/转折连接词，通常意味着新论点的引入
    causal_signals = ["因此", "所以", "这意味着", "这就是为什么", "这就是",
                      "但是", "然而", "可是", "不过", "恰恰相反"]
    head_15 = clean_text[:15]
    for sig in causal_signals:
        if head_15.startswith(sig):
            return "A"

    return "S"


def generate_iar_diagnosis(modules: list[ModuleInfo]) -> str:
    """生成段落推进率诊断报告（v2 — 含加权 wIAR）。
    
    v2 变更：引入加权 wIAR，连续 S 段权重递减。
    同时输出原始 IAR 和 wIAR，供 L2 语义仲裁参照。
    """
    lines = []
    lines.append("# 🔬 段落推进率诊断 (IAR v2)\n")
    lines.append("> A=推进(新概念/新证据)  S=支撑(展开/举例)  R=冗余(重述/套话)")
    lines.append("> IAR = (A+S)/(A+S+R)  |  wIAR = 加权版（连续S降权）")
    lines.append("> ⚠️ IAR 仅为 L1 快检层，不具备语义仲裁能力。详见 rule_iar_interpretation.md\n")

    issues_found = []

    for mod in modules:
        lines.append(f"## {mod.title}")
        
        if not mod.paragraphs:
            lines.append("  （无正文段落）\n")
            continue

        a_count, s_count, r_count = 0, 0, 0
        consecutive_s = 0
        prev_text = ""
        para_results = []
        
        # Bug6: 加权 wIAR 累计器
        weighted_positive = 0.0  # A×1.0 + S×权重
        total_weight_base = 0    # 总段落数（用于 wIAR 分母）

        for i, (text, cc, _) in enumerate(mod.paragraphs):
            cls = classify_paragraph(text, prev_text)
            
            if cls == "A":
                a_count += 1
                consecutive_s = 0
                weighted_positive += 1.0
            elif cls == "S":
                s_count += 1
                consecutive_s += 1
                # Bug6: 连续 S 段权重递减 — 前 2 段 0.7，第 3 段起 0.3
                s_weight = 0.7 if consecutive_s <= 2 else 0.3
                weighted_positive += s_weight
            else:
                r_count += 1
                consecutive_s = 0
                # R 段不贡献正向分数
            
            total_weight_base += 1

            flag = ""
            if cls == "R":
                flag = " ⚠️ [冗余]"
            if consecutive_s > 2:
                flag = " ⚠️ [停滞: 连续支撑>2]"

            preview = text[:35].replace("\n", " ")
            para_results.append(f"  {'🟢' if cls=='A' else '🟡' if cls=='S' else '🔴'} [{cls}] {preview}…{flag}")
            prev_text = text

        total = a_count + s_count + r_count
        iar = (a_count + s_count) / total if total > 0 else 0
        wiar = weighted_positive / total_weight_base if total_weight_base > 0 else 0
        
        # 状态判定以 wIAR 为主
        status = "✅" if wiar >= 0.75 else "⚠️" if wiar >= 0.60 else "❌"

        lines.append(f"  IAR = {iar:.2f}  |  wIAR = {wiar:.2f} {status}  (A:{a_count} S:{s_count} R:{r_count})")
        lines.append("")
        lines.extend(para_results)

        if wiar < 0.75:
            issues_found.append(f"  {mod.title}: wIAR={wiar:.2f} {status}")

        lines.append("")

    if issues_found:
        lines.append("---")
        lines.append("## ⚠️ 需要关注的模块\n")
        lines.extend(issues_found)
    
    return "\n".join(lines)


def generate_skeleton_health(modules: list[ModuleInfo]) -> str:
    """骨架链健康检查：标题逻辑自洽性 + 冷热覆盖完整性。
    
    来源：rule_script_clarity.md §1（骨架链提取）+ audit.md Part B-5（冷热标注）
    """
    lines = []
    lines.append("# 🩺 骨架链健康检查\n")
    lines.append("> 检查标题串联后的逻辑自洽性和冷热覆盖完整性。\n")

    issues = []

    for mod in modules:
        lines.append(f"## {mod.title}")
        lines.append("")

        if not mod.sections:
            lines.append("  （无 H3/H4 标题）\n")
            continue

        # 1. 骨架链提取
        h3_titles = [t for t, lv, _ in mod.sections if lv == 3]
        chain = " → ".join(h3_titles) if h3_titles else "（空）"
        lines.append(f"  **骨架链**: {chain}")
        lines.append("")

        # 2. 冷热覆盖检查
        has_hot = False
        has_cold = False
        for tag_name, temp, _, _ in mod.tags:
            if tag_name in HOT_TAGS:
                has_hot = True
            if tag_name in COLD_TAGS:
                has_cold = True

        if not has_hot:
            lines.append("  ⚠️ [NO_HEAT] 模块无任何🔥热节点（缺少冲突/痛点/共情切入）")
            issues.append((mod.title, "NO_HEAT", "补充 [STORY TIME]、[CASE STUDY] 或 [LIFE CONNECT] 标签段落"))
        if not has_cold:
            lines.append("  ⚠️ [NO_COLD] 模块无任何🧊冷节点（缺少精准结论/教学金句）")
            issues.append((mod.title, "NO_COLD", "补充 [TEACHING MOMENT] 或 [TECH NOTE] 标签段落"))

        # 3. 标题语义重叠粗检（基于中文字符重叠率）
        for i in range(len(h3_titles)):
            for j in range(i + 1, len(h3_titles)):
                chars_i = set(re.findall(r'[\u4e00-\u9fff]', h3_titles[i]))
                chars_j = set(re.findall(r'[\u4e00-\u9fff]', h3_titles[j]))
                if chars_i and chars_j:
                    overlap = len(chars_i & chars_j) / min(len(chars_i), len(chars_j))
                    if overlap > 0.7:
                        lines.append(f"  ⚠️ [SKELETON_OVERLAP] 标题语义疑似重叠：")
                        lines.append(f"     - \"{h3_titles[i]}\"")
                        lines.append(f"     - \"{h3_titles[j]}\"")
                        issues.append((mod.title, "SKELETON_OVERLAP", f"合并或重命名重叠标题：{h3_titles[i]} / {h3_titles[j]}"))

        if has_hot and has_cold and not any(t == mod.title for t, _, _ in issues):
            lines.append("  ✅ 冷热覆盖完整，骨架链健康")

        lines.append("")

    return "\n".join(lines)


def generate_anchor_coverage_diagnosis(modules: list[ModuleInfo]) -> str:
    """锚词覆盖率诊断：检查加粗标记分布密度，评估 Cloak 模式友好性。

    理论基础：RESEARCH_SPEECH_MEMORIZATION.md §方法3 认知分块与关键词锚定。
    加粗文字是 _extract_anchor() 的首要数据源，直接决定 Cloak 模式下
    anchor-chip 和行内 <strong> 锚点的可用性。
    """
    lines = []
    lines.append("# 🔗 锚词覆盖率诊断 (Cloak 模式友好性)\n")
    lines.append("> **加粗文字** 是 H5 记忆检视(Cloak)模式的核心数据源。")
    lines.append("> 覆盖率 ≥ 60% 为健康，连续无锚词间隔 ≤ 3 段为安全。\n")

    bold_re = re.compile(r'\*\*[^*]+\*\*')
    issues_found = []

    for mod in modules:
        lines.append(f"## {mod.title}")

        if not mod.paragraphs:
            lines.append("  （无正文段落）\n")
            continue

        total = len(mod.paragraphs)
        anchored = 0
        max_gap = 0
        current_gap = 0
        gap_locations = []

        for i, (text, cc, _) in enumerate(mod.paragraphs):
            if bold_re.search(text):
                anchored += 1
                if current_gap > 3:
                    gap_locations.append((i - current_gap, i - 1, current_gap))
                current_gap = 0
            else:
                current_gap += 1
                max_gap = max(max_gap, current_gap)

        # 末尾间隔
        if current_gap > 3:
            gap_locations.append((total - current_gap, total - 1, current_gap))

        coverage = anchored / total if total > 0 else 0
        status = "✅" if coverage >= 0.60 else "⚠️" if coverage >= 0.40 else "❌"

        lines.append(f"  锚词覆盖率 = {coverage:.0%} {status}  ({anchored}/{total} 段含加粗)")
        lines.append(f"  最大连续无锚词间隔 = {max_gap} 段 {'✅' if max_gap <= 3 else '⚠️ [ANCHOR_GAP]'}")

        if gap_locations:
            for start, end, gap in gap_locations:
                preview = mod.paragraphs[start][0][:25].replace("\n", " ")
                lines.append(f"    → 段落 {start+1}~{end+1} ({gap} 段无加粗)：「{preview}…」")

        if coverage < 0.60:
            issues_found.append(f"  {mod.title}: 覆盖率={coverage:.0%}")
        if max_gap > 3:
            issues_found.append(f"  {mod.title}: 连续 {max_gap} 段无锚词")

        lines.append("")

    if issues_found:
        lines.append("---")
        lines.append("## ⚠️ Cloak 模式体验风险\n")
        lines.append("> 以下模块在记忆检视模式下可能出现「记忆断层」。\n")
        lines.extend(issues_found)

    return "\n".join(lines)


# 视觉记忆诊断：Layout-内容匹配参考（研究报告 §方法2 记忆宫殿）
_LAYOUT_EXPECTS_LIST = {"Grid", "Comparison"}  # 这些 Layout 通常需要 List 字段
_LAYOUT_STRUCTURAL = {"Grid", "Comparison", "Split"}  # 对比/并列型布局
_LAYOUT_IMMERSIVE = {"Full", "Image", "Quote"}  # 沉浸/单焦点型布局


def generate_visual_memory_diagnosis(modules: list[ModuleInfo]) -> str:
    """视觉记忆诊断：从记忆宫殿理论评估 VISUAL 块作为记忆锚点的有效性。

    理论基础：RESEARCH_SPEECH_MEMORIZATION.md
    - §方法2 记忆宫殿：Layout = 房间形态，Scene = 画面通道
    - §3.1 三维绑定表：[VISUAL].Scene 是「双编码的画面通道」
    - §3.2.A Visual-First 双轨骨架：Slide 排版 + Scene 是演讲者的第一记忆入口

    检查项：
    V1: Scene 空洞 — Scene 描述为空或过短，演讲者在该位置无画面记忆锚点
    V2: Text 缺失 — 缺少 Slide 上显示的核心论断关键词
    V3: Layout-内容错配 — 布局类型与后续 Speech 的论证结构不匹配
    V4: 视觉记忆间隔 — 连续口述字数过高却无 Slide 锚点（与 Q6 重叠但强调记忆视角）
    """
    lines = []
    lines.append("# 🎞️ 视觉记忆诊断 (Visual Memory Anchoring)\n")
    lines.append("> **Slide = 记忆宫殿的房间**。Layout 决定空间感，Scene 提供画面通道，Text 是论断锚词。")
    lines.append("> 任何一环缺失都会削弱演讲者的 Visual-First 记忆链路。\n")

    issues_found = []

    for mod in modules:
        lines.append(f"## {mod.title}")

        if not mod.visual_blocks:
            lines.append("  ⚠️ 模块无任何 VISUAL 块——记忆宫殿为空！")
            issues_found.append((mod.title, "NO_VISUAL", "模块无 VISUAL 块，无记忆宫殿房间"))
            lines.append("")
            continue

        v1_issues = []  # Scene 空洞
        v2_issues = []  # Text 缺失
        v3_issues = []  # Layout 错配

        for vb in mod.visual_blocks:
            meta = vb.metadata or {}
            sid = meta.get("slide_id", "??")
            layout = meta.get("layout", "??")
            scene = meta.get("scene", "").strip()
            text_val = meta.get("text", "").strip()

            # V1: Scene 空洞检查
            if not scene or len(scene) < 10:
                v1_issues.append((sid, layout, vb.line_start, scene))

            # V2: Text 字段缺失（Title/CTA 布局例外）
            if not text_val and layout not in ("Title", "CTA"):
                v2_issues.append((sid, layout, vb.line_start))

            # V3: Layout-内容潜在错配（启发式检查）
            # 如果布局是 Grid/Comparison 但没有 List，可能错配
            raw = vb.content if vb.content else ""
            has_list = "**List**" in raw or bool(meta.get("list"))
            if layout in _LAYOUT_EXPECTS_LIST and not has_list:
                v3_issues.append((sid, layout, vb.line_start, "结构化布局缺少 List 字段"))

        # 输出汇总
        total_v = len(mod.visual_blocks)
        v1_count = len(v1_issues)
        v2_count = len(v2_issues)
        v3_count = len(v3_issues)

        scene_coverage = (total_v - v1_count) / total_v if total_v > 0 else 0
        text_coverage = (total_v - v2_count) / total_v if total_v > 0 else 0

        lines.append(f"  Slide 总数: {total_v}")
        lines.append(f"  Scene 有效率: {scene_coverage:.0%} {'✅' if scene_coverage >= 0.90 else '⚠️'}")
        lines.append(f"  Text 覆盖率: {text_coverage:.0%} {'✅' if text_coverage >= 0.50 else '⚠️'}")

        if v1_issues:
            lines.append(f"\n  🔴 [V1] Scene 空洞 ({v1_count} 个):")
            for sid, layout, line, sc in v1_issues:
                sc_text = f"「{sc}」" if sc else "（空）"
                lines.append(f"    {sid} ({layout}) L{line} — Scene: {sc_text}")
            issues_found.append((mod.title, "SCENE_EMPTY", f"{v1_count} 个 Slide 无有效 Scene"))

        if v2_issues:
            lines.append(f"\n  🟡 [V2] Text 缺失 ({v2_count} 个):")
            for sid, layout, line in v2_issues:
                lines.append(f"    {sid} ({layout}) L{line}")
            if text_coverage < 0.50:
                issues_found.append((mod.title, "TEXT_LOW", f"Text 覆盖率仅 {text_coverage:.0%}"))

        if v3_issues:
            lines.append(f"\n  🟡 [V3] Layout 错配嫌疑 ({v3_count} 个):")
            for sid, layout, line, reason in v3_issues:
                lines.append(f"    {sid} ({layout}) L{line} — {reason}")
            issues_found.append((mod.title, "LAYOUT_MISMATCH", f"{v3_count} 个布局可能错配"))

        if not v1_issues and not v2_issues and not v3_issues:
            lines.append("  ✅ 视觉记忆锚点完整")

        lines.append("")

    if issues_found:
        lines.append("---")
        lines.append("## ⚠️ 视觉记忆风险汇总\n")
        lines.append("> 以下问题可能导致演讲者在记忆宫殿中找不到对应的「房间画面」。\n")
        for title, code, desc in issues_found:
            lines.append(f"  [{code}] {title}: {desc}")

    return "\n".join(lines)


def generate_repair_guidance(modules: list[ModuleInfo]) -> str:
    """修复引导：汇总所有诊断问题，附注来自 rule_script_clarity.md 的修复策略。
    
    来源：rule_script_clarity.md §3.2 + rule_content_depth.md 缺口补救口径
    """
    lines = []
    lines.append("# 🔧 修复引导\n")
    lines.append("> 下方汇总本次诊断发现的所有问题，并附注具体修复策略。")
    lines.append("> 参照：`rule_script_clarity.md` §3 + `rule_content_depth.md` 缺口补救口径\n")

    # 修复策略映射表（来自 rule_script_clarity.md §3.2 和 rule_content_depth.md）
    REPAIR_STRATEGIES = {
        "stagnation": "在连续支撑段之间插入新推进段(A)，或将多个支撑段合并为一段",
        "redundancy": "删除含有'总之/换句话说/也就是说'的冗余句，或将冗余段重写为推进段",
        "weak_opening": "重写首段，直接进入新信息（推进段），禁止以回顾/过渡开头",
        "no_heat": "补充一个 [STORY TIME] 或 [CASE STUDY] 段落，用真实切片包裹感性火花",
        "no_cold": "补充一个 [TEACHING MOMENT] 段落，提炼出精准的教学金句",
        "overlap": "合并语义重叠的标题，或为每个标题找到差异化的维度命名",
        "low_iar": "定位冗余段(R)并删除或重写，直到 IAR ≥ 0.85",
        "anchor_gap": "在该段落的核心术语首次出现处用 **粗体** 标记，确保 Cloak 记忆检视模式下有行内锚点",
        "anchor_density_low": "该模块超过 40% 的段落无锚词，需在每个 H3 块的关键概念处补充 **加粗** 标记",
        "scene_empty": "为 VISUAL 块补充有描画力量的 Scene 描述——Scene 是记忆宫殿的'画面通道'，空 Scene 意味着演讲者在该位置没有视觉记忆锚点",
        "text_missing": "为 VISUAL 块补充 Text 字段——Text 是 Slide 上显示的核心论断关键词，用于帮助演讲者在 Cloak 模式下通过 Slide 画面触发段落回忆",
        "layout_mismatch": "当前 Layout 与 Speech 内容不匹配——布局类型决定了记忆宫殿的'房间形态'，应精准反映段落的论证结构（列表→Grid、对比→Split/Comparison、沉浸→Full）",
    }

    repair_items = []

    for mod in modules:
        if not mod.paragraphs:
            continue

        # 重跑 IAR 分类以收集问题
        consecutive_s = 0
        a_count, s_count, r_count = 0, 0, 0
        prev_text = ""

        for i, (text, cc, _) in enumerate(mod.paragraphs):
            cls = classify_paragraph(text, prev_text)
            if cls == "A":
                a_count += 1
                consecutive_s = 0
            elif cls == "S":
                s_count += 1
                consecutive_s += 1
            else:
                r_count += 1
                consecutive_s = 0

            if cls == "R":
                preview = text[:30].replace("\n", " ")
                repair_items.append((mod.title, "冗余段", preview, REPAIR_STRATEGIES["redundancy"]))
            if consecutive_s > 2:
                preview = text[:30].replace("\n", " ")
                repair_items.append((mod.title, "连续停滞", preview, REPAIR_STRATEGIES["stagnation"]))

            prev_text = text

        total = a_count + s_count + r_count
        iar = (a_count + s_count) / total if total > 0 else 0
        # 与 generate_iar_diagnosis v2 保持一致：使用 wIAR 门控
        if iar < 0.75:
            repair_items.append((mod.title, "IAR 偏低", f"IAR={iar:.2f}", REPAIR_STRATEGIES["low_iar"]))

        # 冷热覆盖
        has_hot = any(t in HOT_TAGS for t, _, _, _ in mod.tags)
        has_cold = any(t in COLD_TAGS for t, _, _, _ in mod.tags)
        if not has_hot:
            repair_items.append((mod.title, "缺少热节点", "无 🔥 标签", REPAIR_STRATEGIES["no_heat"]))
        if not has_cold:
            repair_items.append((mod.title, "缺少冷节点", "无 🧊 标签", REPAIR_STRATEGIES["no_cold"]))

        # 锚词覆盖率（Cloak 模式友好性检查）
        bold_re = re.compile(r'\*\*[^*]+\*\*')
        total_paras = len(mod.paragraphs)
        anchored_paras = sum(1 for text, _, _ in mod.paragraphs if bold_re.search(text))
        if total_paras > 0:
            coverage = anchored_paras / total_paras
            if coverage < 0.60:
                repair_items.append((mod.title, "锚词密度偏低",
                    f"覆盖率 {coverage:.0%}（{anchored_paras}/{total_paras}）",
                    REPAIR_STRATEGIES["anchor_density_low"]))
            # 检查连续无锚词间隔
            max_gap = 0
            current_gap = 0
            for text, _, _ in mod.paragraphs:
                if bold_re.search(text):
                    current_gap = 0
                else:
                    current_gap += 1
                    max_gap = max(max_gap, current_gap)
            if max_gap > 3:
                repair_items.append((mod.title, "锚词断层",
                    f"连续 {max_gap} 段无加粗标记",
                    REPAIR_STRATEGIES["anchor_gap"]))

        # 视觉记忆锻点检查（Scene 空洞 / Text 缺失 / Layout 错配）
        for vb in mod.visual_blocks:
            v_meta = vb.metadata or {}
            sid = v_meta.get("slide_id", "??")
            layout = v_meta.get("layout", "??")
            scene = v_meta.get("scene", "").strip()
            text_val = v_meta.get("text", "").strip()

            if not scene or len(scene) < 10:
                repair_items.append((mod.title, "Scene 空洞",
                    f"{sid} ({layout}) L{vb.line_start}",
                    REPAIR_STRATEGIES["scene_empty"]))

            if not text_val and layout not in ("Title", "CTA"):
                repair_items.append((mod.title, "Text 缺失",
                    f"{sid} ({layout}) L{vb.line_start}",
                    REPAIR_STRATEGIES["text_missing"]))

            raw = vb.content if vb.content else ""
            has_list = "**List**" in raw or bool(v_meta.get("list"))
            if layout in _LAYOUT_EXPECTS_LIST and not has_list:
                repair_items.append((mod.title, "Layout 错配",
                    f"{sid} ({layout}) L{vb.line_start} 缺 List",
                    REPAIR_STRATEGIES["layout_mismatch"]))

    if not repair_items:
        lines.append("✅ 未发现需要修复的问题。脚本结构健康！")
    else:
        lines.append(f"共发现 **{len(repair_items)}** 个待修复项：\n")
        for title, issue_type, context, strategy in repair_items:
            lines.append(f"### ⚠️ {title} — {issue_type}")
            lines.append(f"  - **位置**: {context}…")
            lines.append(f"  - **修复策略**: {strategy}")
            lines.append("")

    return "\n".join(lines)


def generate_progressive_levels(modules: list[ModuleInfo], level: int) -> str:
    """生成指定渐进脱稿层级的提示稿。
    
    Level 1: 全文逐字稿（原文）
    Level 2: 色彩标注稿（只看标签+首句）
    Level 3: Visual-First 骨架（Layout:Scene + 每段锚词）
    Level 4: 情绪弧线图（温度曲线+模块编号）
    Level 5: 白板模式（仅 PPT Slide ID 序列）
    """
    lines = []
    lines.append(f"# 📝 渐进脱稿 Level {level}\n")

    level_desc = {
        1: "全文逐字稿 — 完整通读，含所有 [VISUAL] 静默块",
        2: "色彩标注稿 — 只看标签颜色 + 每段首句",
        3: "Visual-First 骨架 — [Layout: Scene] + 每段 1 个锚词",
        4: "情绪弧线图 — 冷热温度曲线 + 模块标题",
        5: "白板 + PPT 画面 — 完全脱稿，仅凭 Slide 画面触发",
    }
    lines.append(f"> {level_desc.get(level, '')}\n")

    for mod in modules:
        lines.append(f"## {mod.title}\n")

        if level == 2:
            # Level 2: 标签 + 首句
            for tag_name, temp, preview, _ in mod.tags:
                color = TAG_COLORS.get(tag_name, ("", "", ""))
                lines.append(f"  {color[0]} [{tag_name}] {preview}")
            for b in mod.speech_blocks:
                text = strip_markdown(b.content).strip()
                if text and not b.metadata.get("tag_name"):
                    first_sent = text.split("。")[0] + "。" if "。" in text else text[:40]
                    lines.append(f"  ⬜ {first_sent}")
            lines.append("")

        elif level == 3:
            # Level 3: Visual + 锚词
            for sid, layout, scene, _ in mod.visuals:
                palace = get_layout_palace(layout)
                lines.append(f"  🔴 [{layout}] {scene}")

            for sec_title, sec_level, _ in mod.sections:
                if sec_level == 3:
                    clean = re.sub(r'^\d+\.\d+\s*', '', sec_title)
                    lines.append(f"  🔑 {clean}")
            lines.append("")

        elif level == 4:
            # Level 4: 弧线 + 标题
            for tag_name, temp, _, _line in mod.tags:
                if temp:
                    lines.append(f"  {temp} {tag_name}")
            for desc, dur, _ in mod.activities:
                lines.append(f"  🟣 {desc}")
            lines.append("")

        elif level == 5:
            # Level 5: 仅 Slide ID
            for sid, layout, _, _line in mod.visuals:
                lines.append(f"  📺 [{sid}] → 讲什么？")
            lines.append("")

        else:
            lines.append("  （Level 1 请直接阅读原始脚本文件）")
            lines.append("")

    return "\n".join(lines)


def generate_teacher_guide(script_name: str) -> str:
    """生成教师备课指南封面页。"""
    return f"""# 🎓 教师备课套件：{script_name}

> **核心理念**：不要「背」稿，要「理」稿。
> 所有成熟方法的共识是「理解结构」优先于「逐字背诵」。

## 使用指南

### 四步脱稿法

| 步骤 | 方法 | 产出 | 参照章节 |
|:---|:---|:---|:---|
| Step 1 | SCQA 冷热结构审视 | 每段标注冷热角色 | 📋 骨架卡片 |
| Step 2 | Visual-First 骨架提取 | 双轨骨架卡片 | 📋 骨架卡片 |
| Step 3 | Slide 记忆宫殿 + 情绪弧线 | 冷热弧线图 | 🌡️ 情绪弧线 |
| Step 4 | 渐进脱稿训练 | Level 1→5 递减 | 📝 渐进脱稿 |

### 色彩编码速查

| 颜色 | 标签 | 记忆策略 |
|:---|:---|:---|
| 🟡 黄 | `[TEACHING MOMENT]` | 🧊 死记硬背，逐字不差 |
| 🟢 绿 | `[STORY/CASE/LIFE/PHILOSOPHY]` | 🔥 记框架即可，临场自由发挥 |
| 🔵 蓝 | `[TECH NOTE/WARNING/DID YOU KNOW]` | 精确术语/参数/操作警告 |
| 🟣 紫 | `[ACTIVITY/PACING]` | 切换演讲模式，提醒身体状态 |
| 🔴 红 | `[VISUAL] Layout` | 记忆宫殿的「房间形态」 |

### Slide 即记忆宫殿

每种 Layout 对应一种空间感，大屏幕上出现特定排版时自动触发段落回忆：
- `Center` = 🏛️ 开阔大厅（聚焦一个核心概念）
- `Split` = 🚪 左右双面长廊（论据 A vs B）
- `Grid` = 🪟 四窗展览室（多要点并列）
- `Full` = 🎬 沉浸式影院（情感冲击/全屏画面）

---
"""


def main():
    parser = argparse.ArgumentParser(description="教师备课套件生成器")
    parser.add_argument("script", help="逐字稿 Markdown 文件路径")
    parser.add_argument("--level", type=int, choices=[1,2,3,4,5], default=0, 
                        help="渐进脱稿层级 (1-5)，默认输出全部概览")
    parser.add_argument("--diagnose", action="store_true", 
                        help="输出段落推进率诊断 (IAR)")
    parser.add_argument("--output", type=str, default="",
                        help="输出目录（默认打印到终端）")
    args = parser.parse_args()

    if not os.path.exists(args.script):
        print(f"❌ 文件不存在: {args.script}")
        sys.exit(1)

    # 解析脚本
    blocks = parse_script(args.script)
    modules = extract_modules(blocks)
    script_name = Path(args.script).stem

    if not modules:
        print("⚠️ 未检测到任何 ## 模块，请确认文件格式。")
        sys.exit(1)

    # 生成各部分
    outputs = []

    if args.level > 0:
        # 指定层级模式
        outputs.append(generate_progressive_levels(modules, args.level))
    elif args.diagnose:
        # 🔍 诊断模式：IAR + 骨架自洽 + 冷热覆盖 + 锚词覆盖率 + 视觉记忆 + 修复引导
        outputs.append(generate_iar_diagnosis(modules))
        outputs.append(generate_skeleton_health(modules))
        outputs.append(generate_anchor_coverage_diagnosis(modules))
        outputs.append(generate_visual_memory_diagnosis(modules))
        outputs.append(generate_repair_guidance(modules))
    else:
        # 📖 备课模式：纯引导，无审计警告
        outputs.append(generate_teacher_guide(script_name))
        outputs.append(generate_skeleton(modules, script_name))
        outputs.append(generate_anchor_words(modules))
        outputs.append(generate_emotional_arc(modules))

    result = "\n\n---\n\n".join(outputs)

    if args.output:
        os.makedirs(args.output, exist_ok=True)
        out_file = os.path.join(args.output, f"cheat_sheet_{script_name}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ 已生成: {out_file}")
    else:
        print(result)


if __name__ == "__main__":
    main()
