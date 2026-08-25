---
description: 将脚本导出为 TTS 纯文本、审阅 Word 文档或词汇表
---

# /export 工作流

> **输入**: 课程名 + 脚本路径
> **输出**: TTS 纯文本 / 审阅 Word 文档 / 词汇表

## 输出规范

所有导出产物遵循统一命名：`<课程ID>_<周次ID>_<产物类型>.<后缀>`

| 产物类型 | 命名示例 | 输出位置 |
|---------|---------|---------|
| TTS 标准 | `<课程>_W01_TTS.txt` | `build/tts/` |
| TTS 盲读 | `<课程>_W01_TTS_blind.txt` | `build/tts/` |
| 审阅 Word | `<课程>_W01_Review.docx` | `build/artifacts/<周次>/` |
| 词汇表 | `<课程>_Vocabulary.md` | `build/tts/` |

> [!NOTE]
> 当前脚本仍使用旧命名输出，后续迭代将对齐统一规范。以下命令为当前可用版本。

---

## 导出模式

### 模式 A: TTS 纯文本导出
生成纯朗读文本（`.txt`）。

> [!NOTE]
> H5 预览引擎已内置段落级动态 TTS 合成（ADR 039），无需预导出文本文件。
> 此模式现主要用于：外部 TTS 工具批量合成、离线备份、录音员参考底稿。

**A1: 标准模式**（含 `[SLIDE #N]` 标记）— 供录音员参考换页节奏或审计溯源。
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_script_length.py \
  --course "<课程>" --dump-text
```
输出至 `<课程>/build/tts/<周次名>.txt`。

**A2: 盲读模式**（纯朗读文本）— 直接喂 TTS 引擎，无视觉标记。
```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_script_length.py \
  --course "<课程>" --dump-text --blind-mode
```
输出至 `<课程>/build/tts/<周次名>_blind.txt`。

> [!NOTE]
> `--dump-text` 可单独使用（标准模式）或与 `--blind-mode` 联用（盲读模式），均可同时追加 `--dump-vocab`。

### 模式 B: 审阅文档导出
生成带视觉标记的格式化 Word 文档（`.docx`），供人工阅读检查。

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/export_tools/scripts/export_review_docx.py \
  --course "<课程>" --all
```
输出至 `<课程>/build/presentations/review/` 目录。

### 模式 C: 词汇表提取
按章节提取英文术语表。

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_script_length.py \
  --course "<课程>" --dump-vocab
```
输出 `<课程>/build/tts/Vocabulary_List.md`。

---

## 管线总览

完整的课件产物矩阵（所有输出方式）：

| 产物 | 触发命令 | 关系 |
|------|---------|------|
| 🌐 H5 交互课件 | `/h5` | 独立管线 |
| 📊 品牌 PPTX | `/ppt`（一键全链路） | 自动含 NFU 封装 |
| 🔊 TTS 文本 | `/export --dump-text` | 独立管线 |
| 📄 审阅 Word | `/export --review` | 独立管线 |
| 📋 词汇表 | `/export --dump-vocab` | 独立管线 |
