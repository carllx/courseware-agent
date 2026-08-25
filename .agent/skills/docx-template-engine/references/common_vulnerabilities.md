# 常见漏洞数据库 & 修复模式

> 在排查 docxtpl 模板填写问题时加载此文件。按漏洞类型索引。

## 目录

1. [标签类漏洞](#1-标签类漏洞)
2. [格式类漏洞](#2-格式类漏洞)
3. [布局类漏洞](#3-布局类漏洞)
4. [数据类漏洞](#4-数据类漏洞)
5. [特殊字符漏洞](#5-特殊字符漏洞)

---

## 1. 标签类漏洞

### V1-1 标签被 Word 拆分（Split Tags）

**症状**: 渲染后 `{{ name }}` 原样出现在输出文档中
**根因**: Word 将标签拆成多个 `<w:r>` 元素
**docxtpl 内部处理**: `patch_xml()` 使用正则 `{<something>{ → {{` 尝试修复，但对复杂拆分（中间有格式切换）无效

**修复方案**:
```
方案 A（推荐）: 运行 repair_template.py 自动合并 run
方案 B（手动）: 在 Word 中选中标签 → 清除所有格式 → 重新统一设置
方案 C（预防）: 制作模板时，先在纯文本编辑器写好标签再粘贴到 Word
```

### V1-2 循环标签错位（Misplaced Loop Tags）

**症状**: `{% for %}` / `{% endfor %}` 不在同一层级，导致渲染崩溃或输出混乱
**根因**: 循环标签跨越了表格行/段落边界

**修复方案**:
```python
# 错误：标签在段落内，但循环的是表格行
{{ name }}  {% for item in items %}
...
{% endfor %}

# 正确：使用 {%tr %} 在表格行层级循环
{%tr for item in items %}
  {{ item.name }}
{%tr endfor %}
```

### V1-3 条件标签遗留空行（Empty Conditional Lines）

**症状**: `{% if %}` 判断为假时，输出中留下空白行或空段落
**根因**: 标签本身占据了一个段落，条件跳过后空段落仍然存在

**修复方案**:
```python
# 错误
{% if awards %}
{{ awards_text }}
{% endif %}

# 正确：使用段落级标签
{%p if awards %}
{{ awards_text }}
{%p endif %}
```

---

## 2. 格式类漏洞

### V2-1 字号/字体不一致（Font Mismatch）

**症状**: 填入的数据使用了与模板不同的字号或字体
**根因**: 
- 标签的 `<w:rPr>` 与周围文字的 rPr 不一致
- 使用了 RichText 覆盖了模板样式

**调试方法**:
```bash
# 解包检查模板中标签的 rPr
python -c "
import zipfile
with zipfile.ZipFile('template.docx') as z:
    xml = z.read('word/document.xml').decode()
    # 搜索标签附近的 rPr
    import re
    for m in re.finditer(r'<w:rPr>.*?</w:rPr>.*?name', xml[:5000], re.DOTALL):
        print(m.group()[:200])
"
```

**修复方案**: 在 Word 中确保标签文本与周围文字使用完全相同的格式设置。

### V2-2 下划线丢失（Underline Loss）

**症状**: 模板中的填空下划线（如"姓名：_______"）在数据填入后消失
**根因**: 下划线定义在 `<w:rPr>` 的 `<w:u w:val="single"/>` 中，标签替换时该属性被覆盖

**修复方案**:
docxtpl 的 `resolve_listing()` 会在处理 `\n` 时复制 rPr，但前提是 rPr 在同一个 run 中。
```
方案 A: 确保标签和下划线在同一个 run 中（统一格式）
方案 B: 使用 XML 级修补，在渲染后注入 <w:u> 属性
```

### V2-3 加粗/斜体丢失（Bold/Italic Loss）

**症状**: 模板中加粗的标签填入数据后变成常规字体
**根因**: 同 V2-1，rPr 不一致

**修复方案**: 同 V2-1

---

## 3. 布局类漏洞

### V3-1 表格跨页断裂（Table Page Break）

**症状**: 原本在一页内的表格被分到两页
**根因**: 填入的数据比占位符更长，撑高了行高，导致表格总高度超过页面

**修复方案**:
```xml
<!-- 在模板的表格行属性中添加 -->
<w:trPr>
  <w:cantSplit/>  <!-- 禁止行内分页 -->
  <w:trHeight w:val="360" w:hRule="exact"/>  <!-- 固定行高 -->
</w:trPr>
```

**或在 Python 中**:
```python
# 渲染后修补行高
from docx import Document
doc = Document(output_path)
for table in doc.tables:
    for row in table.rows:
        row.height = Cm(0.8)  # 固定行高
```

### V3-2 单元格文本截断（Cell Text Truncation）

**症状**: 单元格内容被截断，只显示部分文字
**根因**: 模板使用了固定行高（`w:hRule="exact"`），但填入内容超出

**修复方案**:
```
方案 A: 改为 w:hRule="atLeast"（最小行高，允许增长）
方案 B: 在 context 中预截断长文本
方案 C: 使用 <w:fitText> 让字体自动缩放
```

### V3-3 意外空白页（Unexpected Blank Page）

**症状**: 输出文档末尾出现空白页
**根因**: 最后一个段落的分页符设置，或最后一个表格的后续段落

**修复方案**: 检查模板最后一个元素后是否有多余的空段落或分页符。

---

## 4. 数据类漏洞

### V4-1 None 字符串输出（None String）

**症状**: 输出文档中出现 "None" 文字
**根因**: context 中某个字段值为 Python `None`

**修复方案**:
```python
# 在构建 context 时做空值清理
ctx = {k: (v if v is not None else '') for k, v in ctx.items()}
```

### V4-2 列表长度不匹配（List Length Mismatch）

**症状**: 表格循环生成的行数多于或少于预期
**根因**: context 中列表的实际长度与模板预留行数不匹配

**修复方案**:
```python
# 用展平方式代替循环（适用于固定行数模板）
for i in range(MAX_ROWS):
    if i < len(items):
        ctx[f'item_{i}_name'] = items[i]['name']
    else:
        ctx[f'item_{i}_name'] = ''
```

---

## 5. 特殊字符漏洞

### V5-1 勾选框渲染错误（Checkbox Rendering）

**症状**: ☑/□ 字符显示为方块或不可见
**根因**: 模板字体不支持 Unicode 勾选符号

**修复方案**:
```python
# 确保使用支持这些字符的字体
ctx['check_first'] = '☑' if is_checked else '□'
# 或使用 Word 内置的复选框控件（更可靠但更复杂）
```

### V5-2 XML 特殊字符转义（XML Entity Escaping）

**症状**: `&`、`<`、`>` 等字符导致渲染崩溃
**根因**: 这些字符在 XML 中是保留字符

**修复方案**: docxtpl 会自动处理基本转义。但如果使用 RichText 或直接操作 XML 时需要手动转义：
```python
from xml.sax.saxutils import escape
ctx['field'] = escape(raw_text)  # & → &amp;  < → &lt;  > → &gt;
```
