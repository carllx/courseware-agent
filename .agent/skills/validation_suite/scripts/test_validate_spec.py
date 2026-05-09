#!/usr/bin/env python3
"""
test_validate_spec.py — validate_spec.py 单元测试

验证目标:
1. 标签白名单/黑名单检查
2. VISUAL 块字段完整性（Slide ID、Layout、Scene）
3. Slide ID 唯一性
4. 旧 [SLIDE:] 格式残留检测
5. 视觉解读深度（Scene vs SPEECH 字数比值）
6. ACTIVITY 块字段完整性（Type、Duration）
7. 合规脚本的零错误基线

测试模式：使用 tempfile 创建临时 .md 文件，避免依赖真实课程目录。
"""

import sys
import os
import tempfile
import textwrap

# 确保能导入 validate_spec 和 script_parser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validate_spec import validate_single_script


# ============================================================
# 辅助工具
# ============================================================

def _write_temp_script(content: str) -> str:
    """将脚本内容写入临时 .md 文件，返回文件路径。"""
    f = tempfile.NamedTemporaryFile(
        mode='w', suffix='.md', delete=False, encoding='utf-8'
    )
    f.write(textwrap.dedent(content))
    f.flush()
    f.close()
    return f.name


def _validate(content: str) -> dict:
    """便捷封装：写临时文件 → 验证 → 清理 → 返回结果。"""
    path = _write_temp_script(content)
    try:
        return validate_single_script(path, os.path.basename(path))
    finally:
        os.unlink(path)


# ============================================================
# 1. 标签白名单检查
# ============================================================

def test_known_tag_pass():
    """白名单内的标签不应产生错误。"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Split
        > **Scene**: 测试场景

        这是正文内容，测试白名单标签。

        > [TEACHING MOMENT]
        > 这是教学金句。

        > [TECH NOTE]
        > 这是技术备注。
    """)
    # 不应有因标签引发的错误
    tag_errors = [e for e in result["errors"] if "未知标签" in e]
    assert len(tag_errors) == 0, f"白名单标签不应报错: {tag_errors}"


def test_unknown_tag_error():
    """未知标签应报 ❌ 错误。"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 封面

        > [FAKE TAG]
        > 这是一个伪造的标签。
    """)
    tag_errors = [e for e in result["errors"] if "未知标签" in e and "FAKE TAG" in e]
    assert len(tag_errors) >= 1, f"未知标签应报错: {result['errors']}"


# ============================================================
# 2. VISUAL 块字段完整性
# ============================================================

def test_visual_missing_slide_id():
    """VISUAL 块缺少 Slide 字段 → ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Layout**: Split
        > **Scene**: 缺少 Slide ID 的测试

        正文内容。
    """)
    slide_errors = [e for e in result["errors"] if "缺少" in e and "Slide" in e]
    assert len(slide_errors) >= 1, f"缺 Slide 应报错: {result['errors']}"


def test_visual_invalid_layout():
    """VISUAL 块使用无效 Layout → ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: InvalidLayout
        > **Scene**: 无效 Layout 测试

        正文内容。
    """)
    layout_errors = [e for e in result["errors"] if "无效 Layout" in e]
    assert len(layout_errors) >= 1, f"无效 Layout 应报错: {result['errors']}"


def test_visual_missing_scene():
    """VISUAL 块缺少 Scene 字段 → ⚠️ 警告"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Split

        正文内容。
    """)
    scene_warns = [w for w in result["warnings"] if "Scene" in w]
    assert len(scene_warns) >= 1, f"缺 Scene 应有警告: {result['warnings']}"


# ============================================================
# 3. Slide ID 唯一性
# ============================================================

def test_slide_id_duplicate():
    """重复的 Slide ID → ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_DUPE
        > **Layout**: Split
        > **Scene**: 第一个

        正文。

        > [VISUAL]
        > **Slide**: W01_DUPE
        > **Layout**: Title
        > **Scene**: 第二个（重复 ID）

        更多正文。
    """)
    dupe_errors = [e for e in result["errors"] if "重复 Slide ID" in e]
    assert len(dupe_errors) >= 1, f"重复 Slide ID 应报错: {result['errors']}"


# ============================================================
# 4. 旧格式残留检测
# ============================================================

def test_old_slide_ref_detected():
    """旧 [SLIDE: xxx] 格式 → ❌"""
    result = _validate("""\
        ## 测试模块

        > **[SLIDE: OLD_REF_01]**

        使用旧格式引用的正文。
    """)
    old_ref_errors = [e for e in result["errors"] if "旧格式" in e]
    assert len(old_ref_errors) >= 1, f"旧格式引用应报错: {result['errors']}"


# ============================================================
# 5. 视觉解读深度
# ============================================================

def test_visual_engagement_depth():
    """VISUAL 后 SPEECH 字数过少 → ⚠️"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Split
        > **Scene**: 这是一个非常详细的场景描述，包含了很多关于视觉设计原则的要点

        短。
    """)
    depth_warns = [w for w in result["warnings"] if "视觉解读深度" in w]
    assert len(depth_warns) >= 1, f"解读深度不足应有警告: {result['warnings']}"


# ============================================================
# 6. ACTIVITY 块字段完整性
# ============================================================

def test_activity_missing_type():
    """ACTIVITY 缺少 Type → ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 封面

        正文。

        > [ACTIVITY]
        > **Duration**: 5min
        > **Desc**: 缺少 Type 的活动
    """)
    type_errors = [e for e in result["errors"] if "缺少" in e and "Type" in e]
    assert len(type_errors) >= 1, f"缺 Type 应报错: {result['errors']}"


def test_activity_invalid_type():
    """ACTIVITY 使用无效 Type → ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 封面

        正文。

        > [ACTIVITY]
        > **Type**: InvalidType
        > **Duration**: 5min
        > **Desc**: 无效类型的活动
    """)
    type_errors = [e for e in result["errors"] if "无效 Activity 类型" in e]
    assert len(type_errors) >= 1, f"无效 Type 应报错: {result['errors']}"


# ============================================================
# 7. 合规脚本零错误基线
# ============================================================

def test_clean_script_no_errors():
    """完全合规的脚本应产生 0 错误 0 警告。"""
    result = _validate("""\
        ## 课程导览（约 5 分钟）

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 课程封面，展示课程名称和教师信息

        欢迎来到信息可视化课程。今天我们将一起探索数据可视化的基本原理，
        了解为什么可视化是理解复杂世界的终极工具。这门课将改变你看待数据的方式。

        > [TEACHING MOMENT]
        > 可视化不是让数据变好看，而是让数据变好懂。

        > [VISUAL]
        > **Slide**: W01_S02
        > **Layout**: Split
        > **Scene**: 课程大纲，左侧为周次列表，右侧为核心技能

        本学期我们将覆盖从基础感知理论到高级交互设计的完整知识谱系。
        每一周都有明确的学习目标和实践任务。在课堂上我们学原理，在课后你做项目。

        > [ACTIVITY]
        > **Type**: QA
        > **Duration**: 3min
        > **Desc**: 破冰提问：你日常生活中见过最好的可视化是什么？
    """)
    assert len(result["errors"]) == 0, f"合规脚本不应有错误: {result['errors']}"
    # 警告数也应为 0（所有字段齐全、解读深度充足）
    assert len(result["warnings"]) == 0, f"合规脚本不应有警告: {result['warnings']}"


# ============================================================
# 8. 占位符残留检测（阶段 1 新增）
# ============================================================

def test_placeholder_detected():
    """脚本中包含 [TODO] 或"自动生成的"→ ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 课程封面

        这是正文内容。[TODO] 此处插入具体案例。

        自动生成的占位符文本。
    """)
    placeholder_errors = [e for e in result["errors"] if "占位符残留" in e]
    assert len(placeholder_errors) >= 2, f"应检出至少 2 个占位符: {placeholder_errors}"


def test_placeholder_clean_pass():
    """不含占位符的脚本不应产生占位符错误。"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 课程封面

        这是完整的正文内容，没有任何占位符。
    """)
    placeholder_errors = [e for e in result["errors"] if "占位符残留" in e]
    assert len(placeholder_errors) == 0, f"无占位符不应报错: {placeholder_errors}"


# ============================================================
# 9. Bold 标记空格检测（阶段 1 新增）
# ============================================================

def test_bold_space_detected():
    """Bold 标记内有前导空格 → ❌"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > ** Scene**: 错误的空格

        正文。
    """)
    bold_errors = [e for e in result["errors"] if "Bold 标记内有多余空格" in e]
    assert len(bold_errors) >= 1, f"Bold 空格应报错: {result['errors']}"


# ============================================================
# 10. VISUAL 字段顺序验证（阶段 1 新增）
# ============================================================

def test_visual_field_order_inverted():
    """VISUAL 字段出现在 [VISUAL] 标记之前 → ❌"""
    result = _validate("""\
        ## 测试模块

        > **Layout**: Split
        > **Slide**: W01_S01
        > [VISUAL]
        > **Scene**: 倒置测试

        正文。
    """)
    order_errors = [e for e in result["errors"] if "字段顺序错误" in e]
    assert len(order_errors) >= 1, f"字段倒置应报错: {order_errors}"


# ============================================================
# 11. 修辞黑名单检测（阶段 1 新增）
# ============================================================

def test_rhetoric_blacklist_detected():
    """脚本正文含修辞黑名单词组 → ⚠️"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 测试封面

        这个设计失误简直是万劫不复的灾难，用户当场休克。
    """)
    rhetoric_warns = [w for w in result["warnings"] if "修辞黑名单" in w]
    assert len(rhetoric_warns) >= 2, f"应检出至少 2 个黑名单词: {rhetoric_warns}"


def test_rhetoric_blacklist_clean_pass():
    """不含黑名单词组的脚本不应产生修辞警告。"""
    result = _validate("""\
        ## 测试模块

        > [VISUAL]
        > **Slide**: W01_S01
        > **Layout**: Title
        > **Scene**: 测试封面

        这个设计存在明显的可用性问题，用户无法顺利完成核心任务。
    """)
    rhetoric_warns = [w for w in result["warnings"] if "修辞黑名单" in w]
    assert len(rhetoric_warns) == 0, f"无黑名单词不应有警告: {rhetoric_warns}"


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
