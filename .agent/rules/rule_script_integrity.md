---
trigger: glob
description: 当编辑逐字稿源文件时，强制执行逐字稿完整性保护——禁止静默删除标签、禁止非指定修改。
globs: ["**/weeks/*/src/*.md"]
---

# 逐字稿完整性保护 (Script Content Integrity Protection)

> **核心原则**：逐字稿（`src/M*.md`、`script.md`、`weeks/*/src/*.md`）是课程的核心教学资产，一旦被脚本错误破坏将导致不可逆的内容丢失。任何对逐字稿的修改必须走可审计、可回退的受控路径。

## §1 禁止 Agent 创建新的逐字稿写入脚本

- **❌ 严禁** Agent 在任何工作流、技能或用户请求中**新建** Python/Shell 脚本，其功能涉及对逐字稿文件执行 `open(path, 'w').write()`、`shutil.move()`、`os.rename()`、`os.remove()`、`sed -i`、`perl -i` 等直接写入/替换/删除操作。
- **❌ 严禁** Agent 创建任何包含 `re.sub()` + `f.write()` 组合的脚本来批量替换逐字稿中的正文内容（如对白、叙事段落、标题、知识标签等）。
- **❌ 严禁** Agent 在脚本中使用 `filepath.write_text()` 或 `Path.write_text()` 覆写逐字稿。
- 若用户明确要求创建此类脚本，Agent 必须**警告风险**并建议改用 Agent 编辑工具（`replace_file_content` / `multi_replace_file_content`）实现同等功能。

## §2 已审计通过的存量脚本白名单

以下脚本经 2026-05-26 安全审计验证通过，允许继续使用：

| 脚本 | 写入范围 | 安全性评估 | 保护机制 |
|:---|:---|:---|:---|
| `inject_budget.py` | 仅插入 `<!-- BUDGET: ... -->` HTML 注释行 | ✅ 不修改正文 | `--dry-run` 模式；增量跳过已有 BUDGET |
| `inject_assets.py` + `visual_block_io.py` | 仅修改 `[VISUAL]` 块的 Asset/Source 字段 | ✅ 不修改正文 | `--dry-run` 模式；幂等性（`_real` 路径跳过） |
| `refactor_modules.py` | 一次性迁移脚本（拆分 script.md → M0X.md） | ✅ 创建新文件+备份原文件 | 无工作流引用，处于休眠状态 |
| `generate_exp_docs.py` | 写入 `practices/experiments/Output/` | ✅ 不操作逐字稿 | 独立输出目录 |

> [!IMPORTANT]
> **白名单冻结**：上述脚本的写入逻辑已锁定。Agent 不得在未经用户明确批准的情况下修改这些脚本的文件写入路径或写入范围。

## §3 逐字稿修改的受控路径

所有对逐字稿正文内容的修改，**必须且只能**通过以下路径之一执行：

1. **Agent 编辑工具**：`replace_file_content` 或 `multi_replace_file_content`（带精确的 TargetContent 匹配，用户可审阅 diff）
2. **用户手动编辑**：由用户自行在编辑器中修改
3. **白名单脚本的受限写入**：仅限 §2 白名单脚本在其声明的写入范围内操作

## §4 修复前备份纪律

当 Agent 通过编辑工具对逐字稿执行批量修复（如 `/revise`、`/memory_optimize` 产生的 Patch）时：

- **强制要求**：在执行第一个 Patch 前，必须先执行 `cp <文件> <文件>.bak` 创建备份
- **单次替换上限**：单个 `TargetContent` 不得超过 800 字。超过此长度的替换视为"大段重写"，必须拆分为多个小补丁并逐个展示给用户确认
- **禁止全量覆写**：严禁使用 `write_to_file Overwrite=true` 覆写已有逐字稿文件
