---
description: 使用通用生成器从 Markdown 脚本自动生成课程 PPT
---

# /ppt 工作流 (通用自动化版)

本工作流使用 workspace 级 `engines/generate_course_ppt.js` 通用生成器，可直接将 Markdown 脚本及其 `[VISUAL]` / `[SPEECH]` 标签转换为标准 PPTX 文件。

## 前置条件

1. **环境**: Node.js 环境已就绪。
2. **依赖**: workspace 根目录下已运行 `npm install` (确保 `pptxgenjs`, `js-yaml`, `image-size` 已安装)。
3. **配置**: 课程目录或其 `styles/` 子目录下存在 `visual_system.yaml`（可选 — 无则使用默认低保真主题）。

## 执行步骤

### Step 1: 准备资源

确保脚本中的 Visual Asset 路径正确，且文件存在于素材目录中（V5 架构：`weeks/W0X/public/slides/`，旧架构：`weeks/W0X/assets/slides/`）。

**使用 `grep_search` 工具检查脚本中引用的图片（`Asset` 字段）是否存在于物理路径中。**

### Step 1.5: 内容完备性预检 (Bullet Sync Check)

在生成 PPT 之前，运行脚本规范验证器确认无合规问题：

```bash
/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/validation_suite/scripts/validate_spec.py \
  --course "<课程>"
```

### Step 2: 运行生成器

在 **workspace 根目录** 下运行通用生成脚本。

**格式**:
`node engines/generate_course_ppt.js <课程目录> <脚本相对路径>`

**示例**:
```bash
# weeks/ 架构（信息可视化）
node engines/generate_course_ppt.js 信息可视化 weeks/W01_Visual_Perception/package.yaml


```

> **功能特性**: 
> 1. **智能比例修复**: 自动读取图片原始尺寸，在 Layout 容器内保持长宽比缩放。
> 2. **备注清洗**: 自动移除 `[SPEECH]` 中的 Markdown 标记和知识标签，保留纯演讲稿。
> 3. **主题适配**: 自动加载 `visual_system.yaml`，无则使用默认低保真主题。
> 4. **真正的 Grid/Quote 布局**: 卡片网格和金句布局有独立渲染。
> 5. **Heading 提取 (v3)**: 从脚本 `###` 标题行自动提取幻灯片标题，分离图片 prompt 和演示标题。
> 6. **字号自适应 (v3)**: 标题根据长度自动调整字号（≤10 字 28pt / ≤18 字 24pt / >18 字 20pt），避免溢出。
> 7. **Grid 智能降级 (v3)**: 无 `List` 数据但有 Asset 图片时，自动切换为居中大图模式。

### Step 3: 输出与验证 (QA)

输出文件位于 `<课程>/build/presentations/<脚本名>_Presentation_Gen.pptx`。

建议使用 LibreOffice 转换为图片进行视觉验收：

```bash
mkdir -p /tmp/ppt_qa

/opt/anaconda3/envs/mybase/bin/python \
  .agent/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf "<课程>/build/presentations/<脚本名>_Presentation_Gen.pptx" --outdir /tmp/ppt_qa

pdftoppm -jpeg -r 150 /tmp/ppt_qa/*.pdf /tmp/ppt_qa/slide
```

确认：
1. **图片比例**: Logo、截图等非正方形素材是否保持原样。
2. **配色**: 是否符合 `visual_system.yaml`（或默认低保真主题）。
3. **备注**: Speaker Notes 是否清晰易读（无标签、无 Markdown 杂质）。

### Step 4 (可选): 逆向同步 Notes

如果在 PowerPoint 中直接编辑了 Presentation Notes，可逆向同步回 Markdown 脚本：

```bash
# 先 dry-run 查看差异
/opt/anaconda3/envs/mybase/bin/python engines/sync_notes_back.py \
  --pptx "<课程>/build/presentations/<脚本名>_Presentation_Gen.pptx" \
  --script "<课程>/weeks/W0X_Name/package.yaml" \
  --dry-run

# 确认无误后实际同步（自动创建带时间戳的 .bak 备份）
/opt/anaconda3/envs/mybase/bin/python engines/sync_notes_back.py \
  --pptx "<课程>/build/presentations/<脚本名>_Presentation_Gen.pptx" \
  --script "<课程>/weeks/W0X_Name/package.yaml"

# 可选：自定义额外保护标签 + 详细日志
/opt/anaconda3/envs/mybase/bin/python engines/sync_notes_back.py \
  --pptx "<课程>/build/presentations/<脚本名>_Presentation_Gen.pptx" \
  --script "<课程>/weeks/W0X_Name/package.yaml" \
  --extra-tags NOTE REF HINT -v
```

> **安全特性**:
> 1. 🛡️ **保护块**: 自动识别并保留 `[TECH NOTE]`、`[ACTIVITY]`、`[STAGE NOTE]` 等结构化块，仅替换纯 Speech 行。
> 2. 💾 **时间戳备份**: 每次同步自动生成 `.bak_YYYYMMDD_HHMMSS.md` 备份，不覆盖历史。
> 3. 🏷️ **可扩展标签**: 通过 `--extra-tags` 追加自定义保护标签。
> 4. 📝 **详细日志**: `-v` 开启 DEBUG 级别日志输出。

## 故障排除

- **Warning: Asset not found**: 检查素材目录下是否有对应图片（V5 架构：`weeks/W0X/public/slides/`，旧架构：`weeks/W0X/assets/slides/`），或脚本中 `Asset:` 路径是否正确。
- **Warning: color not valid**: 检查 `visual_system.yaml` 格式是否标准 (应包含 top-level `palette`)。
- **Error: Cannot find module 'image-size'**: 请在 workspace 根目录运行 `npm install`。
- **逆向同步数量不匹配**: PPT 增删了幻灯片，需手动对齐 Slide 数量后重试。
- **读取 PPT/脚本失败**: 检查文件是否损坏或路径是否正确，加 `-v` 查看详细错误。

