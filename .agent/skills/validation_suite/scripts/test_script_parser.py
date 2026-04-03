#!/usr/bin/env python3
"""
test_script_parser.py — script_parser.py 正则统一化单元测试

验证目标:
1. _field_re 工厂函数对三路匹配和 freeform 模式的正确性
2. _extract 辅助函数的提取逻辑
3. 所有 **Field**: 正则的三种写法（反引号/双引号/裸文本）一致性
4. 对现有脚本的回归验证
"""

import sys
import os
import tempfile
import textwrap

# 确保能导入 script_parser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from script_parser import (
    _field_re, _extract,
    RE_SLIDE_FIELD, RE_LAYOUT_FIELD, RE_SCENE_FIELD, RE_ASSET_FIELD,
    RE_ACTIVITY_TYPE, RE_ACTIVITY_DURATION, RE_ACTIVITY_DESC,
    parse_script, BlockType,
)


# ============================================================
# 1. _field_re 工厂函数测试
# ============================================================

def test_field_re_three_way_backtick():
    """三路模式：反引号包裹"""
    p = _field_re("Test")
    m = p.search("**Test**: `hello world`")
    assert m is not None
    assert _extract(m) == "hello world"


def test_field_re_three_way_doublequote():
    """三路模式：双引号包裹"""
    p = _field_re("Test")
    m = p.search('**Test**: "hello world"')
    assert m is not None
    assert _extract(m) == "hello world"


def test_field_re_three_way_bare():
    """三路模式：裸文本"""
    p = _field_re("Test")
    m = p.search("**Test**: hello_world")
    assert m is not None
    assert _extract(m) == "hello_world"


def test_field_re_freeform():
    """freeform 模式：匹配含空格的任意文本"""
    p = _field_re("Test", freeform=True)
    m = p.search("**Test**: hello world with spaces")
    assert m is not None
    assert _extract(m, freeform=True) == "hello world with spaces"


def test_field_re_freeform_trailing_space():
    """freeform 模式：去除末尾空格"""
    p = _field_re("Test", freeform=True)
    m = p.search("**Test**: hello   ")
    assert m is not None
    assert _extract(m, freeform=True) == "hello"


# ============================================================
# 2. 具体字段正则测试
# ============================================================

def test_slide_field_all_formats():
    """Slide 字段三种写法"""
    for text, expected in [
        ("**Slide**: `W01_S01`", "W01_S01"),
        ('**Slide**: "W01_S01"', "W01_S01"),
        ("**Slide**: W01_S01", "W01_S01"),
    ]:
        m = RE_SLIDE_FIELD.search(text)
        assert m is not None, f"未匹配: {text}"
        assert _extract(m) == expected, f"提取错误: {text} → {_extract(m)}"


def test_layout_field_all_formats():
    """Layout 字段三种写法"""
    for text, expected in [
        ("**Layout**: `Comparison`", "Comparison"),
        ('**Layout**: "Diagram"', "Diagram"),
        ("**Layout**: Split", "Split"),
    ]:
        m = RE_LAYOUT_FIELD.search(text)
        assert m is not None, f"未匹配: {text}"
        assert _extract(m) == expected


def test_asset_field_all_formats():
    """Asset 字段三种写法（修复验证）"""
    for text, expected in [
        ("**Asset**: `visuals/assets/W01/W01_S01.png`", "visuals/assets/W01/W01_S01.png"),
        ('**Asset**: "visuals/assets/W01/W01_S01.png"', "visuals/assets/W01/W01_S01.png"),
        ("**Asset**: visuals/assets/W01/W01_S01.png", "visuals/assets/W01/W01_S01.png"),
    ]:
        m = RE_ASSET_FIELD.search(text)
        assert m is not None, f"未匹配: {text}"
        assert _extract(m) == expected


def test_activity_type_all_formats():
    """Type 字段三种写法（Bug 修复验证）"""
    for text, expected in [
        ("**Type**: `Practice`", "Practice"),
        ('**Type**: "QA"', "QA"),
        ("**Type**: Workshop", "Workshop"),
    ]:
        m = RE_ACTIVITY_TYPE.search(text)
        assert m is not None, f"未匹配: {text}"
        assert _extract(m) == expected


def test_activity_duration_all_formats():
    """Duration 字段三种写法（Bug 修复验证）"""
    for text, expected in [
        ("**Duration**: `5min`", "5min"),
        ('**Duration**: "30s"', "30s"),
        ("**Duration**: 3min", "3min"),
    ]:
        m = RE_ACTIVITY_DURATION.search(text)
        assert m is not None, f"未匹配: {text}"
        assert _extract(m) == expected


def test_scene_field_with_spaces():
    """Scene 字段：freeform 含空格和中文"""
    text = "**Scene**: 可用性准则对应表，三列：准则名称、对应可用性维度、测量方式。"
    m = RE_SCENE_FIELD.search(text)
    assert m is not None
    assert _extract(m, freeform=True) == "可用性准则对应表，三列：准则名称、对应可用性维度、测量方式。"


def test_activity_desc_with_chinese():
    """Desc 字段：freeform 含中文"""
    text = "**Desc**: 用户画像生成练习，使用 Empathy Map"
    m = RE_ACTIVITY_DESC.search(text)
    assert m is not None
    assert _extract(m, freeform=True) == "用户画像生成练习，使用 Empathy Map"


# ============================================================
# 3. 集成测试：解析包含各种格式的 VISUAL 和 ACTIVITY 块
# ============================================================

def test_parse_visual_block_bare_asset():
    """VISUAL 块中无反引号的 Asset 路径应正确解析"""
    script = textwrap.dedent("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Split
        > **Scene**: 测试场景
        > **Asset**: visuals/assets/test/W01_S01.png

        这是一段逐字稿。
    """)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(script)
        f.flush()
        blocks = parse_script(f.name)
    os.unlink(f.name)

    visuals = [b for b in blocks if b.block_type == BlockType.VISUAL]
    assert len(visuals) == 1
    meta = visuals[0].metadata
    assert meta["slide_id"] == "W01_S01"
    assert meta["layout"] == "Split"
    assert meta["scene"] == "测试场景"
    assert meta["asset"] == "visuals/assets/test/W01_S01.png"


def test_parse_activity_block_bare_type():
    """ACTIVITY 块中无反引号的 Type/Duration 应正确解析"""
    script = textwrap.dedent("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 封面

        开场白。

        > [ACTIVITY]
        > **Type**: Practice
        > **Duration**: 5min
        > **Desc**: 测试描述

        过渡段。
    """)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(script)
        f.flush()
        blocks = parse_script(f.name)
    os.unlink(f.name)

    activities = [b for b in blocks if b.block_type == BlockType.ACTIVITY]
    assert len(activities) == 1
    meta = activities[0].metadata
    assert meta["activity_type"] == "Practice"
    assert meta["duration_raw"] == "5min"
    assert meta["duration_sec"] == 300
    assert meta["desc"] == "测试描述"


# ============================================================
# 4. 多资产解析测试（v2 升维重构）
# ============================================================

def test_multi_asset_numbered():
    """Asset 1 / Asset 2 / Asset 3 应全部收集到 assets 数组"""
    script = textwrap.dedent("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: S01_Multi
        > **Layout**: Split
        > **Scene**: 多图测试
        > **Asset 1**: visuals/assets/W01/img1.jpg
        > **Asset 2**: visuals/assets/W01/img2.jpg
        > **Asset 3**: visuals/assets/W01/img3.jpg

        这是正文。
    """)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(script)
        f.flush()
        blocks = parse_script(f.name)
    os.unlink(f.name)

    visuals = [b for b in blocks if b.block_type == BlockType.VISUAL]
    assert len(visuals) == 1
    meta = visuals[0].metadata
    assert meta["assets"] == [
        "visuals/assets/W01/img1.jpg",
        "visuals/assets/W01/img2.jpg",
        "visuals/assets/W01/img3.jpg",
    ], f"assets 不匹配: {meta['assets']}"
    assert meta["asset"] == "visuals/assets/W01/img1.jpg", "向后兼容 asset 应为首图"


def test_resource_field_as_asset():
    """**Resource** 应被归并到 assets 数组"""
    script = textwrap.dedent("""\
        > [VISUAL]
        > **Slide**: S02_Resource
        > **Layout**: Image
        > **Scene**: 测试
        > **Asset**: visuals/assets/W01/main.png
        > **Resource**: visuals/assets/W01/ref.jpg
    """)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(script)
        f.flush()
        blocks = parse_script(f.name)
    os.unlink(f.name)

    visuals = [b for b in blocks if b.block_type == BlockType.VISUAL]
    assert len(visuals) == 1
    meta = visuals[0].metadata
    assert len(meta["assets"]) == 2, f"应有 2 条资产: {meta['assets']}"
    assert meta["asset"] == "visuals/assets/W01/main.png", "向后兼容 asset 应为首条"


def test_asset_md_syntax_stripped():
    """Markdown 图片语法应被自动清洗"""
    script = textwrap.dedent("""\
        > [VISUAL]
        > **Slide**: S03_MD
        > **Layout**: Image
        > **Scene**: 测试
        > **Asset**: ![预览](../visuals/assets/W01/test.png)
    """)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(script)
        f.flush()
        blocks = parse_script(f.name)
    os.unlink(f.name)

    visuals = [b for b in blocks if b.block_type == BlockType.VISUAL]
    assert len(visuals) == 1
    meta = visuals[0].metadata
    assert meta["asset"] == "visuals/assets/W01/test.png", f"MD 语法未清洗: {meta['asset']}"
    assert meta["assets"] == ["visuals/assets/W01/test.png"]


def test_normalize_asset_path_all_formats():
    """normalize_asset_path 应处理所有输入格式"""
    from script_parser import normalize_asset_path
    cases = [
        ("visuals/assets/W01/img.png", "visuals/assets/W01/img.png"),
        ("![alt](visuals/assets/W01/img.png)", "visuals/assets/W01/img.png"),
        ("![](../visuals/assets/W01/img.png)", "visuals/assets/W01/img.png"),
        ("`visuals/assets/W01/img.png`", "visuals/assets/W01/img.png"),
        ('"visuals/assets/W01/img.png"', "visuals/assets/W01/img.png"),
        ("../../visuals/assets/W01/img.png", "visuals/assets/W01/img.png"),
        ("", ""),
    ]
    for raw, expected in cases:
        result = normalize_asset_path(raw)
        assert result == expected, f"Failed for {raw!r}: got {result!r}, expected {expected!r}"


# ============================================================
# 运行入口
# ============================================================

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
    print(f"\n{'='*40}")
    print(f"共 {passed + failed} 项 | ✅ {passed} 通过 | ❌ {failed} 失败")
    if failed:
        sys.exit(1)
