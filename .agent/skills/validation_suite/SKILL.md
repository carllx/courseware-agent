---
name: validation-suite
description: 维护项目健康度、文档一致性和教学质量的自动化工具集合。当用户输入 /validate、检查一致性或验证链接时使用。
---

# 技能：验证套件 (Validation Suite)

## 概述

| 属性 | 值 |
|-----|-----|
| **状态** | ✅ 已实现 |
| **Python** | `python` (Requires environment with dependencies) |
| **描述** | 课程无关的脚本验证、素材审查与自动化导出工具箱。 |

## 脚本清单

所有脚本位于 `scripts/` 目录下，通过 `--course` 参数指定课程目录。

### 1. 通用解析器 (`script_parser.py`)
*   **类型**: 库模块（不直接运行）
*   **用途**: 解析 Markdown 脚本为 `ScriptBlock` 列表，供所有验证器和导出器消费。
*   **支持**: `> [VISUAL]`、`> [ACTIVITY]`、知识标签、旧 `[SLIDE:]` 引用、元数据等。

### 2. 规范合规性检查 (`validate_spec.py`)
*   **用途**: 检查标签白名单、VISUAL/ACTIVITY 块完整性、Layout 类型、Slide ID 唯一性、旧格式残留。
*   **用法**:
    ```bash
    python scripts/validate_spec.py --course "实习指导"
    python scripts/validate_spec.py --course "实习指导" --week 1
    python scripts/validate_spec.py --course "实习指导" --file S01_Mobilization.md
    ```

### 3. 视觉素材完整性 (`validate_visuals.py`)
*   **用途**: 交叉比对脚本 VISUAL 引用与素材物理文件（同时扫描 `visuals/assets/`、`weeks/*/assets/` 和 V5 `weeks/*/public/`），报告缺失和孤立素材。
*   **用法**:
    ```bash
    python scripts/validate_visuals.py --course "实习指导"
    python scripts/validate_visuals.py --course "实习指导" --week 1
    ```

### 4. 时长估算与 TTS 导出 (`validate_script_length.py`)
*   **用途**: 脚本时长预估、模块级分析、TTS 纯文本导出、英文术语表提取。
*   **模式**:
    | 标志 | 说明 |
    |:---|:---|
    | 无 | 打印时长估算表格 |
    | `--module-breakdown` | 按 `##` 模块级分析字数分布（ADR 020） |
    | `--module "<关键词>"` | 仅检查模块名含关键词的模块（模糊匹配） |
    | `--segment-check` | 配合 `--module` 使用，输出 JSON 精简格式（供 Phase A/B 中间检查点） |
    | `--week N` | 仅检查第 N 周的脚本 |
    | `--dump-text` | 导出带 Slide 标记的 `.txt` |
    | `--dump-text --blind-mode` | 导出纯朗读 `.txt` |
    | `--dump-vocab` | 按章节提取术语表 |
*   **用法**:
    ```bash
    python scripts/validate_script_length.py --course "实习指导"
    python scripts/validate_script_length.py --course "实习指导" --module-breakdown
    python scripts/validate_script_length.py --course "实习指导" --module "目标" --segment-check
    python scripts/validate_script_length.py --course "实习指导" --dump-text --blind-mode --dump-vocab
    ```

### 5. 审阅文档导出 (`export_review_docx.py`)
*   **用途**: 从脚本生成带视觉标记的 Word 文档（红=VISUAL、蓝=ACTIVITY、灰=知识标签），供人工阅读检查。
*   **输出**: `<课程>/build/presentations/review/*.docx`
*   **用法**:
    ```bash
    python scripts/export_review_docx.py --course "实习指导" --all
    python scripts/export_review_docx.py --course "实习指导" --file S01_Mobilization
    ```

### 6. 统一入口 (`validate_project.py`)
*   **用途**: 批量运行 spec → visuals → length 三个验证器，输出汇总报告。
*   **用法**:
    ```bash
    python scripts/validate_project.py --course "实习指导"
    python scripts/validate_project.py --course "实习指导" --week 1
    ```

### 7. V5 Package 架构校验 (`validate_package.py`)
*   **用途**: 校验 `package.yaml` 的字段完整性、segments 路径存在性、ID 唯一性、src/ 孤立文件检测，可选编译通过性验证。
*   **用法**:
    ```bash
    python scripts/validate_package.py --course "信息可视化"
    python scripts/validate_package.py --course "信息可视化" --compile
    python scripts/validate_package.py --file "信息可视化/weeks/W01_Visual_Perception/package.yaml"
    ```
