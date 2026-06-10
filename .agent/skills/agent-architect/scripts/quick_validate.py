#!/usr/bin/env python3
"""
Agent Extension Validator — 自动检测并校验 Rule / Skill 格式。

用法:
    quick_validate.py <path>

    path 为文件时 → 校验为 Rule（.agent/rules/xxx.md）
    path 为目录时 → 校验为 Skill（.agent/skills/xxx/）
"""

import sys
import re
import yaml
from pathlib import Path


def validate_rule(rule_path):
    """校验 Rule 文件的 frontmatter 和基本结构。"""
    rule_path = Path(rule_path)

    if not rule_path.exists():
        return False, "文件不存在"

    if not rule_path.is_file():
        return False, "路径不是文件"

    content = rule_path.read_text(encoding='utf-8')

    # Q1: 文件大小
    if len(content) > 12000:
        return False, f"文件超过 12,000 字符（当前 {len(content)} 字符）"
    if len(content) > 9600:
        print(f"⚠️ 预警：文件已达 {len(content)} 字符（上限 12,000 的 {len(content)*100//12000}%）")

    # Frontmatter 存在性
    if not content.startswith('---'):
        return False, "未找到 YAML frontmatter"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "frontmatter 格式无效"

    try:
        fm = yaml.safe_load(match.group(1))
        if not isinstance(fm, dict):
            return False, "frontmatter 必须是 YAML 字典"
    except yaml.YAMLError as e:
        return False, f"YAML 解析错误：{e}"

    # Q2: trigger 字段
    VALID_TRIGGERS = {'always', 'model_decision', 'glob', 'manual'}
    trigger = fm.get('trigger')
    if not trigger:
        return False, "缺少 'trigger' 字段"
    if trigger not in VALID_TRIGGERS:
        return False, f"trigger 值 '{trigger}' 无效，必须为：{', '.join(VALID_TRIGGERS)}"

    # Q2: description 字段
    desc = fm.get('description', '')
    if not desc or not isinstance(desc, str):
        return False, "缺少 'description' 字段或格式错误（必须为非空字符串）"
    if len(desc) > 100:
        print(f"⚠️ 预警：description 长度 {len(desc)} 字符，建议 ≤ 100 字")

    # Q3: glob 模式时检查 globs 字段
    if trigger == 'glob':
        if 'globs' not in fm:
            # 检查是否误用了单数 'glob' 字段
            if 'glob' in fm:
                return False, "❌ 致命错误：使用了 'glob'（单数）作为字段名，必须用 'globs'（复数列表）——当前写法会导致规则静默失效！"
            return False, "trigger 为 'glob' 时必须提供 'globs' 字段"

        globs = fm['globs']
        if not isinstance(globs, list):
            return False, f"'globs' 必须是 YAML 列表（当前类型：{type(globs).__name__}）"

        # Q4: 检查每个 glob 模式
        for g in globs:
            if not isinstance(g, str):
                return False, f"glob 模式必须是字符串，发现：{type(g).__name__}"

    # 检查禁止字段
    if 'name' in fm:
        return False, "Rule frontmatter 禁止使用 'name' 字段（那是 Skill 的字段）"

    # Q5: 文件名规范
    if not rule_path.name.startswith('rule_'):
        print(f"⚠️ 预警：文件名 '{rule_path.name}' 不符合 'rule_<功能域>.md' 规范")

    return True, "✅ Rule 校验通过"


def validate_skill(skill_path):
    """校验 Skill 的 frontmatter 和目录结构。"""
    skill_path = Path(skill_path)

    # 检查 SKILL.md 存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md 未找到"

    content = skill_md.read_text(encoding='utf-8')

    if not content.startswith('---'):
        return False, "未找到 YAML frontmatter"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "frontmatter 格式无效"

    try:
        fm = yaml.safe_load(match.group(1))
        if not isinstance(fm, dict):
            return False, "frontmatter 必须是 YAML 字典"
    except yaml.YAMLError as e:
        return False, f"YAML 解析错误：{e}"

    # 允许的字段
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    unexpected = set(fm.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        # 特殊检查：是否误用了 Rule 字段
        rule_fields = unexpected & {'trigger', 'globs', 'glob'}
        if rule_fields:
            return False, (
                f"发现 Rule 专属字段 {rule_fields}。"
                f"如果要创建 Rule，应放在 .agent/rules/ 目录下而非 Skills 目录。"
            )
        return False, f"frontmatter 中有未知字段：{', '.join(sorted(unexpected))}"

    # 必需字段
    if 'name' not in fm:
        return False, "缺少 'name' 字段"
    if 'description' not in fm:
        return False, "缺少 'description' 字段"

    name = fm.get('name', '')
    if not isinstance(name, str):
        return False, f"name 必须是字符串，当前类型：{type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"name '{name}' 必须是 kebab-case（小写字母、数字和连字符）"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"name '{name}' 不能以连字符开头/结尾或包含连续连字符"
        if len(name) > 64:
            return False, f"name 过长（{len(name)} 字符），上限 64 字符"

    desc = fm.get('description', '')
    if not isinstance(desc, str):
        return False, f"description 必须是字符串，当前类型：{type(desc).__name__}"
    desc = desc.strip()
    if desc:
        if '<' in desc or '>' in desc:
            return False, "description 不能包含尖括号（< 或 >）"
        if len(desc) > 1024:
            return False, f"description 过长（{len(desc)} 字符），上限 1024 字符"

    # SKILL.md 行数检查
    line_count = content.count('\n') + 1
    if line_count > 500:
        print(f"⚠️ 预警：SKILL.md 有 {line_count} 行，建议 ≤ 500 行（拆分到 references/）")

    return True, "✅ Skill 校验通过"


def main():
    if len(sys.argv) != 2:
        print("用法: quick_validate.py <path>")
        print()
        print("  path 为文件 → 校验为 Rule")
        print("  path 为目录 → 校验为 Skill")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        print(f"🔍 检测为 Rule 文件：{target.name}")
        valid, msg = validate_rule(target)
    elif target.is_dir():
        print(f"🔍 检测为 Skill 目录：{target.name}")
        valid, msg = validate_skill(target)
    else:
        print(f"❌ 路径不存在：{target}")
        sys.exit(1)

    print(msg)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()