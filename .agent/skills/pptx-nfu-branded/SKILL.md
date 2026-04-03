---
name: nfu-branded-pptx
description: "将 NFU（广州南方学院）设计学院品牌元素注入 PPTX 文件。当用户要创建或编辑课程 PPT 并需要遵循学院统一模板规范时触发。适用场景：添加 NFU 封面/结尾页、替换品牌主题色、注入校徽 Logo、应用学院字体方案。与基础 pptx skill 配合使用——本 skill 负责品牌层，pptx skill 负责底层 OOXML 操作。"
---

# NFU Branded PPTX Skill

## 核心概念

本 skill 采用 **"固定环节 + 内容合并"** 的工作模式：

1. **固定环节**（本 skill 负责生成）：封面页、回顾页、目录页、引用页、作业页、结尾页
2. **内容主体**（由其他课程 PPT 提供）：教学内容幻灯片直接从课程已有 PPT 中获取
3. **可选环节**：章节分隔页可根据课程排版需要灵活添加

最终输出 = 固定环节页 **包裹** 内容主体页，拼装为一个完整的品牌化课程 PPT。

## 资源清单

| 资源 | 路径 | 说明 |
|------|------|------|
| 设计 Token | `resources/nfu_theme.yaml` | 色板、字体、布局配置 |
| 16:9 媒体 | `resources/media/16-9/` | 背景图、Logo |
| 4:3 媒体 | `resources/media/4-3/` | 同上 |
| 品牌注入脚本 | `scripts/inject_branding.py` | Python 核心工具 |

## 快速参考

### 1. 包裹模式（推荐）— 固定环节 + 内容合并

```bash
# 将课程内容 PPT 包裹上 NFU 品牌固定环节
python .agent/skills/nfu-branded-pptx/scripts/inject_branding.py \
  --input content_slides.pptx \
  --output branded_course.pptx \
  --course-name "交互设计" \
  --course-code "D12345" \
  --teacher "张三" \
  --semester "2025-2026学年第二学期" \
  --date "2026年3月1日"
```

脚本会自动在内容 PPT 前后插入品牌固定环节页：

```
[封面页] → [回顾页] → [目录页] → [原有内容页...] → [引用页] → [作业页] → [结尾页]
```

### 2. 从 course.yaml 自动填充

```bash
python .agent/skills/nfu-branded-pptx/scripts/inject_branding.py \
  --input content.pptx \
  --output branded.pptx \
  --course-yaml path/to/course.yaml
```

### 3. 仅注入主题色（不增减幻灯片）

```bash
python .agent/skills/nfu-branded-pptx/scripts/inject_branding.py \
  --input existing.pptx \
  --output branded.pptx \
  --theme-only
```

### 4. 灵活选择固定环节

```bash
# 跳过回顾页和目录页
python .agent/skills/nfu-branded-pptx/scripts/inject_branding.py \
  --input content.pptx --output branded.pptx \
  --skip review,toc \
  --course-name "信息可视化" ...

# 添加可选的章节分隔页
python .agent/skills/nfu-branded-pptx/scripts/inject_branding.py \
  --input content.pptx --output branded.pptx \
  --sections "第1章：设计基础,第2章：用户研究" \
  --course-name "交互设计" ...
```

## 固定环节页说明

| 环节 | 默认 | 说明 |
|------|------|------|
| **封面页** | ✅ 必选 | 深灰背景 + 课程名/编号/教师/学期 + Logo |
| **回顾页** | ✅ 默认 | 浅灰背景 + 上节课知识点回顾 |
| **目录页** | ✅ 默认 | 浅灰背景 + 本节课内容概述 |
| **章节头** | ❌ 可选 | 白色简洁 + 章/节标题（通过 --sections 启用） |
| **引用页** | ✅ 默认 | 浅灰背景 + 参考文献/书籍/网址 |
| **作业页** | ✅ 默认 | 浅灰背景 + 作业要求/提交方式/截止日期 |
| **结尾页** | ✅ 必选 | 深灰背景 + 联系方式 + Logo |

## 跨项目迁移

本 skill 设计为**自包含、可迁移**的。迁移步骤：

```bash
# 复制 skill 文件夹至目标项目
cp -r .agent/skills/nfu-branded-pptx /path/to/other-project/.agent/skills/

# 即可在目标项目中使用
cd /path/to/other-project
python .agent/skills/nfu-branded-pptx/scripts/inject_branding.py ...
```

所有路径均**相对于脚本自身位置**解析，无需修改任何配置。

## 品牌规范

### 色板

| 用途 | 色值 |
|------|------|
| accent1 蓝 | `#4874CB` |
| accent2 橙 | `#EE822F` |
| accent4 绿 | `#75BD42` |
| accent6 红 | `#E54C5E` |
| 封面深灰 | `#505050` |
| 内容浅灰 | `#F5F5F5` |

### 字体

| 用途 | 字体 | 字号 |
|------|------|------|
| 封面标题 | 微软雅黑 (PingFang SC 回退) | 66pt |
| 章节标题 | 微软雅黑 | 36pt |
| 页面标题 | 微软雅黑 | 24pt |
| 正文 | 微软雅黑 | 18-20pt |

## Skill 协作

| 职责 | nfu-branded-pptx | pptx |
|------|-------------------|------|
| 品牌固定环节生成 | ✅ | ❌ |
| Logo/背景/色板 | ✅ | ❌ |
| 内容页 XML 编辑 | ❌ | ✅ |
| PptxGenJS 创建 | ❌ | ✅ |
| 视觉 QA | ❌ | ✅ |

## 依赖

- Python 3.9+
- `python-pptx` (`pip install python-pptx`)
- `PyYAML` (`pip install pyyaml`)
