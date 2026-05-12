import re

text = """> [VISUAL]
> *   **Slide**: `S08_The_Black_Museum`
> *   **Asset**: ![预览](../public/slides/S08_The_Black_Museum_real.png)
> *   **Asset (AI fallback)**: ![预览](../public/slides/S08_The_Black_Museum.png)
> *   **Layout**: `Grid`
> *   **Scene**: 大屏幕上仿佛推开了一扇生锈的铁门，展现出一个暗黑风格的画廊，墙壁上挂着三幅令人不适的真实图表标本：一个是用3D饼图强行展示卡路里占比，一个是用雷达图强行闭合营养指标，一个是比较任务却用了3D堆叠柱状图。每幅图下方贴着红色的"犯罪档案编号"标签。
> *   **Text**: "The Black Museum：信息犯罪现场"
> *   **List**:
> *     - 标本A: 3D饼图面积越权与遮挡
> *     - 标本B: 雷达图强行闭合独立指标
> *     - 标本C: 3D堆叠柱状图透视失真
> *   **Source**: AI Generated"""

block_lines = text.split('\n')
RE_BLOCKQUOTE = re.compile(r'^>\s?(.*)')

inner_lines = []
for bl in block_lines:
    m = RE_BLOCKQUOTE.match(bl)
    inner_lines.append(m.group(1) if m else bl[1:].strip())

in_list_field = False
for inner_i, il in enumerate(inner_lines):
    il_s = il.strip()
    if not il_s or il_s.startswith('[VISUAL]'): continue
    is_field_line = bool(re.match(r'^[\*\s]*\*\*[^\*]+\*\*[:：]', il_s))
    if is_field_line:
        in_list_field = bool(re.match(r'^[\*\s]*\*\*List\*\*[:：]', il_s))
        continue
    if in_list_field and re.match(r'^[\-\*\+]\s+', il_s):
        continue
    
    print(f"❌ Error at {inner_i}: {il_s}")
