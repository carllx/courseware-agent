---
description: 将脚本导出为 TTS 纯文本、审阅 Word 文档或词汇表
---

# /export 工作流

> **输入**: 课程名 + 脚本路径
> **输出**: Word 文档 或 TTS 纯文本

## 导出模式

### 模式 A: TTS 纯文本导出
生成纯朗读文本（`.txt`）。

> [!NOTE]
> H5 预览引擎已内置段落级动态 TTS 合成（ADR 039），无需预导出文本文件。
> 此模式现主要用于：外部 TTS 工具批量合成、离线备份、录音员参考底稿。

**A1: 标准模式**（含 `[SLIDE #N]` 标记）— 供录音员参考换页节奏或审计溯源。
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" --dump-text
```
输出至 `<课程>/build/tts/<脚本名>.txt`。

**A2: 盲读模式**（纯朗读文本）— 直接喂 TTS 引擎，无视觉标记。
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" --dump-text --blind-mode
```
输出至 `<课程>/build/tts/<脚本名>_blind.txt`。

> [!NOTE]
> `--dump-text` 可单独使用（标准模式）或与 `--blind-mode` 联用（盲读模式），均可同时追加 `--dump-vocab`。

### 模式 B: 审阅文档导出
生成带视觉标记的格式化 Word 文档（`.docx`），供人工阅读检查。


```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/export_review_docx.py \
  --course "<课程>" --all
```
输出至 `<课程>/build/presentations/review/` 目录。

### 模式 C: 词汇表提取
按章节提取英文术语表。


```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_script_length.py \
  --course "<课程>" --dump-vocab
```
输出 `<课程>/build/tts/Vocabulary_List.md`。
