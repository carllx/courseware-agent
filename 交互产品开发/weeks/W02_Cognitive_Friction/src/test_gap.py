import re

content = """
> [VISUAL]
> **Slide**: w02-slide-01d_3
> **Layout**: `Center`
> **Scene**: 两把量尺的隐喻。底部一把冰冷的钢尺写着“可用性守住底线”；上方一把散发着柔和光芒的卷尺写着“用户体验决定上限”
> **List**: 可用性：底线约束 | 体验：上限突破
> **Text**: 两把尺子的度量衡

> [ACTIVITY: 脑内微演习 - 办公室咖啡机]
> **Type**: `Practice`
> **Duration**: `3min`
> **Desc**: 快速情境代入测试
> `操作`：讲师描述一个日常抓狂场景，要求学生瞬间匹配对应的设计原则失误。
> `引导词`："光背定义没用，我们来做一个 10 秒钟的体检演习。想象一下你刚入职，走向茶水间那台高级的意大利全自动咖啡机。"
> "场景 1：你按下了『浓缩』键，机器毫无反应，屏幕没亮音效也没响。你不知道它是坏了还是正在加热，于是你又按了四次，结果机器突然连续出了五杯浓缩流了一地。——这是什么原则断裂？" （**反馈缺失**）
> "场景 2：机器上有一排黑色的方形平面贴片，没有突起，没有边框。你看半天都不知道这到底是装饰性的反光板，还是可以按下去的触摸按键。——这没做到什么？" （**示能微弱/可见性差**）
> "场景 3：你终于摸清了套路，长按左边第一个键是出水。第二天换了一台同品牌不同型号的机器，你长按左边第一个键，结果喷出来的是滚烫的蒸汽烫了手。——这违背了什么原则？" （**一致性破裂**）

> [!NOTE]
> **复习段** · 本段回链 **知识目标 1**：系统理解可用性五维与体验目标四象限。

> [VISUAL]
"""

chunk_no_visual = re.sub(r'^> \[VISUAL\].*?(?=\n\n|> \[)', '', content, flags=re.DOTALL)
chunk_no_activity = re.sub(r'> \[ACTIVITY\].*?(?=\n\n|> \[|\Z)', '', chunk_no_visual, flags=re.DOTALL)
print("NO VISUAL:", chunk_no_visual)
print("NO ACTIVITY:", chunk_no_activity)
def count_chinese_chars(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))
print("Chars:", count_chinese_chars(chunk_no_activity))

