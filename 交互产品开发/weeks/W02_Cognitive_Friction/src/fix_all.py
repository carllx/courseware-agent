import re
import os

def insert_visual(filepath, search_str, visual_block):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if search_str in content:
        content = content.replace(search_str, visual_block + "\n\n" + search_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed in {filepath}")
    else:
        print(f"NOT FOUND in {filepath}")

# M01
v1 = """> [VISUAL]
> **Slide**: w02-slide-06_1b
> **Layout**: `Center`
> **Scene**: 头脑主动构建拼图的抽象图形：眼睛摄入杂乱无章的色块碎片，大脑将其拼合成完整的正方形
> **List**: 被动接收现实 ❌ | 主动构建秩序 ✅
> **Text**: 潜意识规则：大脑的硬件出厂配置"""
insert_visual('M01_认知框架_你的大脑不是处理器.md', '### 1.2 主观构建：感知是大脑的主动拼图机', v1)

v2 = """> [VISUAL]
> **Slide**: w02-slide-06e_1
> **Layout**: `Split`
> **Scene**: 相似性原则的反例展示。左侧是全盘蓝色的文字块（相似性被破坏），右侧是经过修正、仅超链接变蓝的排版。
> **List**: 破坏相似性：全盘滥用蓝色 | 顺应相似性：区分可点击元素
> **Text**: 相似性原则的界面灾难"""
insert_visual('M01_认知框架_你的大脑不是处理器.md', '- **相似性（Similarity）**：长得像的东西，大脑会归为同类。', v2)

v3 = """> [VISUAL]
> **Slide**: w02-slide-07c_1
> **Layout**: `Center`
> **Scene**: 脑力工作记忆的隐喻。一个极其微小且不稳定的“便签桌”，上面只能放 4 张脆弱的便签。
> **List**: 感觉记忆：0.5s | 工作记忆：暂存推理区（4个组块上限） | 长期记忆：无限但提取极慢
> **Text**: 脆弱的工作记忆瓶颈"""
insert_visual('M01_认知框架_你的大脑不是处理器.md', '1956 年，认知心理学家 George Miller', v3)

v4 = """> [VISUAL]
> **Slide**: w02-slide-07b_1
> **Layout**: `Center`
> **Scene**: 认知负荷的天平。一边是界面呈现的选项复杂度，一边是大脑的实时计算负荷，指针濒临过载红区。
> **List**: 系统固有负荷 | 视觉与决策双重负担
> **Text**: 认知负荷：系统的脑力占用率"""
insert_visual('M01_认知框架_你的大脑不是处理器.md', '早在 20 世纪 80 年代，NASA（美国宇航局）为了评估宇航员', v4)

# M02
v5 = """> [VISUAL]
> **Slide**: w02-slide-09_1
> **Layout**: `Center`
> **Scene**: 鸿沟填平的隐喻。深渊上的桥梁正在被构建，左侧是“意图”，右侧是“结果”，中间是通过设计构建的坚实桥面。
> **List**: 可供性 (Affordance) | 意符 (Signifiers) | 映射 (Mapping)
> **Text**: 填平执行鸿沟的工具箱"""
insert_visual('M02_意图与反馈的断裂.md', '如屏幕上的三连卡片所示，让我们把填平执行鸿沟的工具箱展开。', v5)

v6 = """> [VISUAL]
> **Slide**: w02-slide-12_1
> **Layout**: `Center`
> **Scene**: 轻量化反馈与心流保护的图示。温和的Toast提示悬浮在界面底部，未打断用户的核心操作流程。
> **List**: 中置弹窗：粗暴打断 | 底部Toast：温和护航
> **Text**: 温和地处理日常评估鸿沟"""
insert_visual('M02_意图与反馈的断裂.md', '现代 UX 怎样温和地处理日常评估鸿沟？', v6)

