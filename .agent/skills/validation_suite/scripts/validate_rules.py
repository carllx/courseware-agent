#!/usr/bin/env python3
"""
Rules Frontmatter 合规性验证器 (validate_rules.py)

检查 .agent/rules/*.md 的 YAML frontmatter 是否符合 Antigravity IDE 规范。

检查项:
  1. 每个文件必须有有效的 YAML frontmatter
  2. trigger 字段必须存在且值为 always | model_decision | glob
  3. trigger: glob 时，globs 字段必须存在且为 list 类型
  4. trigger: model_decision 时，description 字段必须存在
  5. description 字段推荐始终存在
  6. 非标准字段会触发 WARN
  7. 单文件大小 ≤ 12,000 字符

用法:
    python validate_rules.py [--rules-dir <path>]
"""

import os
import sys
import re
import yaml
import argparse

# 标准字段白名单
STANDARD_FIELDS = {"trigger", "description", "globs"}
VALID_TRIGGERS = {"always", "model_decision", "glob"}
MAX_CHARS = 12_000


def parse_frontmatter(filepath: str) -> dict | None:
    """从 Markdown 文件中提取 YAML frontmatter。"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return None


def validate_rule(filepath: str) -> tuple[list[str], list[str]]:
    """验证单个规则文件，返回 (errors, warnings)。"""
    errors = []
    warnings = []
    basename = os.path.basename(filepath)

    # 检查文件大小
    with open(filepath, "r", encoding="utf-8") as f:
        char_count = len(f.read())
    if char_count > MAX_CHARS:
        errors.append(f"文件大小 {char_count} 字符，超过 {MAX_CHARS} 上限")

    # 解析 frontmatter
    fm = parse_frontmatter(filepath)
    if fm is None:
        errors.append("无有效的 YAML frontmatter（缺少 --- 分隔块或 YAML 解析失败）")
        return errors, warnings

    # 检查 trigger 字段
    trigger = fm.get("trigger")
    if trigger is None:
        errors.append("缺少 `trigger` 字段")
    elif trigger not in VALID_TRIGGERS:
        errors.append(f"`trigger: {trigger}` 无效，允许值: {VALID_TRIGGERS}")

    # 检查 description 字段
    description = fm.get("description")
    if trigger == "model_decision" and not description:
        errors.append("trigger: model_decision 模式下 `description` 字段为必填")
    elif not description:
        warnings.append("缺少 `description` 字段（推荐始终提供）")

    # 检查 globs 字段
    if trigger == "glob":
        globs = fm.get("globs")
        if globs is None:
            errors.append("trigger: glob 模式下 `globs` 字段为必填")
        elif not isinstance(globs, list):
            errors.append(
                f"`globs` 应为 YAML 数组 (list)，当前类型: {type(globs).__name__}"
            )
        elif len(globs) == 0:
            errors.append("`globs` 数组为空")

    # 检查非标准字段
    extra_fields = set(fm.keys()) - STANDARD_FIELDS
    if extra_fields:
        warnings.append(f"非标准字段: {extra_fields}")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Rules Frontmatter 合规性验证")
    parser.add_argument(
        "--rules-dir",
        default=None,
        help="规则目录路径（默认: 自动推算 .agent/rules/）",
    )
    args = parser.parse_args()

    # 推算路径
    if args.rules_dir:
        rules_dir = args.rules_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rules_dir = os.path.abspath(
            os.path.join(script_dir, *[".."] * 3, "rules")
        )

    if not os.path.isdir(rules_dir):
        print(f"❌ 目录不存在: {rules_dir}")
        sys.exit(1)

    # 扫描所有 .md 文件
    rule_files = sorted(
        [f for f in os.listdir(rules_dir) if f.endswith(".md")]
    )

    if not rule_files:
        print(f"⚠️  目录中无 .md 文件: {rules_dir}")
        sys.exit(1)

    print("🛡️  Rules Frontmatter 合规性验证")
    print("=" * 60)
    print(f"  目录: {rules_dir}")
    print(f"  文件数: {len(rule_files)}")
    print("=" * 60)

    total_errors = 0
    total_warnings = 0

    for filename in rule_files:
        filepath = os.path.join(rules_dir, filename)
        errors, warnings = validate_rule(filepath)

        if errors or warnings:
            print(f"\n📄 {filename}")
            for e in errors:
                print(f"   ❌ ERROR: {e}")
                total_errors += 1
            for w in warnings:
                print(f"   ⚠️  WARN:  {w}")
                total_warnings += 1
        else:
            print(f"   ✅ {filename}")

    # 汇总
    print(f"\n{'=' * 60}")
    print("📊 验证汇总")
    print(f"{'=' * 60}")
    print(f"  文件数: {len(rule_files)}")
    print(f"  错误:   {total_errors}")
    print(f"  警告:   {total_warnings}")

    if total_errors == 0 and total_warnings == 0:
        print("\n✨ 所有规则文件合规！")
        sys.exit(0)
    elif total_errors == 0:
        print(f"\n⚠️  有 {total_warnings} 个警告，但无错误。")
        sys.exit(0)
    else:
        print(f"\n💡 有 {total_errors} 个错误需要修复。")
        sys.exit(1)


if __name__ == "__main__":
    main()
