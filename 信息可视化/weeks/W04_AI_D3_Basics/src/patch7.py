import sys

file_path = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W04_AI_D3_Basics/src/M03_像素的绝对支配_D3.js.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

t7_part1 = """**数据绑定机制 (Data Join)** 是 D3 的核心创新。
通俗地说，它就像是**给每个数据分配一个专属的“像素替身”**。传统手工编程需要你亲自去控制每一个替身的生老病死，容易出错且繁琐。而 D3 的 Data Join 让替身的生命周期完全交由背后的真实数据决定——数据来了替身就出现，数据变了替身就变形，数据没了替身就自动消亡。"""

r7_part1 = """**数据绑定 (Data Join)** 是 D3 的核心创新（它解决了海量数据如何与页面视觉元素建立动态映射的难题）。
通俗地说，它就像是**为每一个数据点分配一个专属的“像素替身”**。传统的手工编程需要你亲自去控制每一个替身何时出现、何时消失，极易出错且繁琐。而 D3 的 Data Join 机制让替身的生命周期完全交由背后的真实数据全权接管——数据来了替身就出现，数据变了替身就变形，数据没了替身就自动消亡。"""


t7_part2 = """答案是 C。当数据量从 5 减少到 3 时，“肉体（旧 DOM 节点）”多于“灵魂（新数据）”。那 2 根失去数据的旧柱子会进入 Exit（离开态），必须显式调用 `.remove()` 将其彻底物理销毁，否则就会像幽灵一样占据屏幕。选项 A 处理的是数据多于节点的情境，选项 B 对应的是前 3 根正确对接的柱子。"""

r7_part2 = """答案是 C。当数据量从 5 减少到 3 时，“肉体（旧 DOM 节点）”多于“灵魂（新数据）”。那 2 根失去数据的旧柱子会进入 Exit（离开态），必须显式调用 `.remove()` 将其销毁，否则就会像幽灵一样占据屏幕（回忆本节核心：数据驱动的三态轮回机制）。选项 A 处理的是“灵魂多于肉体”的降生情境，选项 B 对应的是前 3 根正确变形的柱子。"""

t7_part3 = """在 D3 中设置属性时，通常使用箭头函数，如 `.attr('height', d => yScale(d.salary))`。
这里的 `d` (Datum) 代表绑定到当前节点的专属数据。当 D3 遍历图表元素时，`d =>` 会逐个提取数据的特定属性（如 `salary`）并传入比例尺，计算出具体的物理高度，从而实现对海量图元的批量渲染。

掌握了倒置画布、比例尺和 Data Join 三态循环后，你就能精准审查并修正 AI 生成的复杂 D3 代码。"""

r7_part3 = """在 D3 中给成千上万的替身设置属性时，我们极少写死具体数值，而是依赖**箭头函数探针**，比如 `.attr('height', d => yScale(d.salary))`。

这里的 **`d` (Datum)**，就像是挂在每个像素替身脖子上的**专属铭牌**。当 D3 的渲染引擎扫过整个图表时，`d =>` 探针会瞬间穿透每个数据点，提取出特定的值（例如 `salary`），再将其丢进比例尺中，计算出**绝对的物理像素高度**，最终在一瞬间完成对海量数据的**批量渲染**。

只要掌握这三大核心机制：向下坠落的**倒置画布**、填平落差的**比例尺**，以及掌管元素的 **Data Join 三态轮回**，你就能精准拿捏并修正 AI 生成的任何 D3 代码。"""

replacements = [
    (t7_part1, r7_part1, "Patch 7 Part 1"),
    (t7_part2, r7_part2, "Patch 7 Part 2"),
    (t7_part3, r7_part3, "Patch 7 Part 3")
]

for t, r, name in replacements:
    if t in content:
        content = content.replace(t, r)
        print(f"Applied {name}")
    else:
        print(f"Failed to find {name}!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished patching M03 Part 7.")
