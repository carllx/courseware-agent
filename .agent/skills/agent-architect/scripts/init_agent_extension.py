#!/usr/bin/env python3
"""
Agent Extension Initializer — 统一生成 Rule / Workflow / Skill 的脚手架。

用法:
    init_agent_extension.py <name> --path <path> --type <rule|workflow|skill>

示例:
    init_agent_extension.py security_governance --path .agent/rules --type rule
    init_agent_extension.py deploy --path .agent/workflows --type workflow
    init_agent_extension.py pdf-editor --path .agent/skills --type skill
"""

import sys
from pathlib import Path

# ============================================================
# 模板定义 (中文)
# ============================================================

RULE_TEMPLATE_GLOB = """---
trigger: glob
description: 当<触发条件>时，<核心行为>。
globs:
  # ⚠️ 优先用 **/ 替代 */，防止目录层级变更后静默失效
  - "**/<匹配模式>"
---

# 规则：<中文名> (<English Name>)

## TL;DR (预检阶段专用)
<2-3 行核心要点速记>

> **核心原则**: <一句话设计哲学>

---

## §1 <分节标题>
...

## 禁止行为
- ❌ ...
"""

RULE_TEMPLATE_MODEL = """---
trigger: model_decision
description: 当<触发条件>时，必须<核心行为>。
---

# 规则：<中文名> (<English Name>)

**生效范围**: 当 Agent 需要<具体操作>时。

## 强制前置步骤 (Pre-flight)
在<操作>**之前**，Agent 必须：
1. ...
2. ...

## 执行协议
...

## 禁止行为
- ❌ ...
"""

RULE_TEMPLATE_ALWAYS = """---
trigger: always
description: <一句话说明这条规则持续约束什么行为>
---

# 规则：<中文名> (<English Name>)

## 核心原则
- **原则 1**: ...
- **原则 2**: ...

## 强制约束
1. ...
2. ...

## 禁止行为
- ❌ ...
"""

WORKFLOW_TEMPLATE = """---
description: <一句话说明该命令做什么>
---

## 前置条件
- <确认必要的先决条件>

## 步骤

1. <第一步操作>
2. <第二步操作>
3. <第三步操作>
"""

SKILL_TEMPLATE = """---
name: {skill_name}
description: <说明该技能做什么 + 何时触发。包含具体的触发场景和文件类型。中文撰写。>
---

# {skill_title}

## 概述

<1-2 句话说明该技能的核心能力>

## 主要功能

### 功能 1
<描述>

### 功能 2
<描述>

## 资源

本技能包含以下可选资源目录：

### scripts/
可执行脚本（Python/Bash 等），用于执行特定的自动化操作。

### references/
参考文档，按需加载到上下文中辅助决策。

### assets/
输出资产（模板/图片/字体等），不加载到上下文，直接用于最终产物。

---

**不需要的资源目录应删除。**
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 示例辅助脚本。

替换为实际实现或按需删除。
"""

def main():
    print("{skill_name} 示例脚本")
    # TODO: 添加实际逻辑

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 参考文档

此为占位参考文档。替换为实际内容或按需删除。

## 何时使用参考文档

- 详细的 API 文档
- 复杂的多步工作流指南
- 超出 SKILL.md 适合篇幅的信息
- 仅在特定场景才需要的内容

## 结构建议

### API 参考示例
- 概述
- 认证
- 端点 + 示例
- 错误码

### 工作流指南示例
- 前置条件
- 分步指引
- 常见模式
- 故障排除
"""


def title_case_name(name):
    """将连字符/下划线名称转为标题格式。"""
    return ' '.join(word.capitalize() for word in name.replace('-', '_').split('_'))


def init_rule(name, path):
    """生成 Rule 文件。"""
    # 确保文件名符合 rule_xxx.md 规范
    if not name.startswith('rule_'):
        filename = f"rule_{name}.md"
    else:
        filename = f"{name}.md"

    target = Path(path).resolve() / filename

    if target.exists():
        print(f"❌ 错误：文件已存在：{target}")
        return None

    # 默认使用 model_decision 模板（最常用）
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(RULE_TEMPLATE_MODEL)
    print(f"✅ 已创建 Rule：{target}")
    print(f"\n💡 提示：默认使用 model_decision 模板。")
    print(f"   如需其他触发模式，请修改 frontmatter 的 trigger 字段。")
    print(f"   可选：always / model_decision / glob / manual")
    return target


def init_workflow(name, path):
    """生成 Workflow 文件。"""
    filename = f"{name}.md"
    target = Path(path).resolve() / filename

    if target.exists():
        print(f"❌ 错误：文件已存在：{target}")
        return None

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(WORKFLOW_TEMPLATE)
    print(f"✅ 已创建 Workflow：{target}")
    print(f"   用户触发方式：/{name}")
    return target


def init_skill(name, path):
    """生成 Skill 目录结构。"""
    skill_dir = Path(path).resolve() / name

    if skill_dir.exists():
        print(f"❌ 错误：目录已存在：{skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 已创建 Skill 目录：{skill_dir}")
    except Exception as e:
        print(f"❌ 创建目录失败：{e}")
        return None

    skill_title = title_case_name(name)

    # SKILL.md
    skill_md = skill_dir / 'SKILL.md'
    skill_md.write_text(SKILL_TEMPLATE.format(
        skill_name=name,
        skill_title=skill_title
    ))
    print("✅ 已创建 SKILL.md")

    # scripts/
    scripts_dir = skill_dir / 'scripts'
    scripts_dir.mkdir()
    example = scripts_dir / 'example.py'
    example.write_text(EXAMPLE_SCRIPT.format(skill_name=name))
    example.chmod(0o755)
    print("✅ 已创建 scripts/example.py")

    # references/
    refs_dir = skill_dir / 'references'
    refs_dir.mkdir()
    ref_doc = refs_dir / 'reference.md'
    ref_doc.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
    print("✅ 已创建 references/reference.md")

    # assets/
    assets_dir = skill_dir / 'assets'
    assets_dir.mkdir()
    print("✅ 已创建 assets/ (空目录)")

    return skill_dir


def main():
    if len(sys.argv) < 6 or '--path' not in sys.argv or '--type' not in sys.argv:
        print("用法: init_agent_extension.py <name> --path <path> --type <rule|workflow|skill>")
        print()
        print("示例:")
        print("  init_agent_extension.py security_governance --path .agent/rules --type rule")
        print("  init_agent_extension.py deploy --path .agent/workflows --type workflow")
        print("  init_agent_extension.py pdf-editor --path .agent/skills --type skill")
        sys.exit(1)

    name = sys.argv[1]
    path_idx = sys.argv.index('--path') + 1
    type_idx = sys.argv.index('--type') + 1
    path = sys.argv[path_idx]
    ext_type = sys.argv[type_idx]

    if ext_type not in ('rule', 'workflow', 'skill'):
        print(f"❌ 错误：无效类型 '{ext_type}'，必须为 rule / workflow / skill")
        sys.exit(1)

    print(f"🚀 初始化 {ext_type}：{name}")
    print(f"   位置：{path}")
    print()

    handlers = {
        'rule': init_rule,
        'workflow': init_workflow,
        'skill': init_skill,
    }

    result = handlers[ext_type](name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
