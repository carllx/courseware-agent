import os

src_dir = "/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W03_Product_Insights/src"

def insert_after(filename, search_string, insert_string):
    path = os.path.join(src_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if search_string in content:
        # Check if already inserted
        if insert_string.strip()[:20] in content:
            print(f"Already inserted in {filename}")
            return
        content = content.replace(search_string, search_string + "\n" + insert_string + "\n")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Success in {filename}")
    else:
        print(f"Failed to find target in {filename}: {search_string[:50]}...")

def insert_before(filename, search_string, insert_string):
    path = os.path.join(src_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if search_string in content:
        if insert_string.strip()[:20] in content:
            print(f"Already inserted in {filename}")
            return
        content = content.replace(search_string, "\n" + insert_string + "\n" + search_string)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Success in {filename}")
    else:
        print(f"Failed to find target in {filename}: {search_string[:50]}...")

# M01
insert_before("M01_复习_从认知摩擦到商业洞察.md",
"> 创始团队给资本讲的故事非常动听：现代城市人渴望喝新鲜",
"""> [VISUAL]
> **Slide**: w03-slide-04_juicero_pitch
> **Layout**: Split
> **Scene**: 左侧是极简高科技的 Juicero 机器和波浪动效 App 界面，右侧是极度讨厌清洗榨汁机的城市白领
> **Text**: 完美的执行：用最顶级的科技美学包装伪需求
> """)

# M05
insert_before("M05_讲授三_敏捷痛点发掘与_Problem_Statement.md",
"> 那个名叫小美的女白领（**目标用户**）",
"""> [VISUAL]
> **Slide**: w03-slide-30_garage_story
> **Layout**: Center
> **Scene**: 屏幕上打出巨大的 POV 填空题，对应小美深夜在车库翻找钥匙的恐惧
> **Text**: 用 POV 公式套用深夜车库场景
> """)

insert_before("M05_讲授三_敏捷痛点发掘与_Problem_Statement.md",
"> 在这个敏捷发掘的阶段，产品经理手里必须握着一种",
"""> [VISUAL]
> **Slide**: w03-slide-34_leading_indicators
> **Layout**: Split
> **Scene**: 左侧是代表"死亡判决"的滞后营收数据，右侧是代表"预警雷达"的早期用户行为测试
> **Text**: 生存法则：寻找预判翻车的先导雷达
> **List**: 滞后指标 (Lagging): 看到即死亡 (如销量、利润) | 先导指标 (Leading): 预判趋势的早期雷达 (如原型点击率)
> """)

# M06
insert_before("M06_实践与小结_微调研沙局与_Exp1_启动.md",
"所以，接下来的时间，我要把你们直接扔进角斗场。",
"""
> [VISUAL]
> **Slide**: w03-slide-36_arena
> **Layout**: Center
> **Scene**: 屏幕上闪现巨大的倒计时沙漏和严酷的实战角斗场背景
> **Text**: 停止纸上谈兵，下沉到真实的泥泞中去
""")

insert_before("M06_实践与小结_微调研沙局与_Exp1_启动.md",
"> 然后，带着这个鲜血淋漓的痛点，跑回这间教室。",
"""> [VISUAL]
> **Slide**: w03-slide-36_activity_rules
> **Layout**: List
> **Scene**: 严格的微调研沙局倒计时与纪律清单
> **Text**: 微调研沙局的三大约束
> **List**: 1. 禁用熟人与预设脚本 | 2. 必须完成3次连环 5-Why 追问 | 3. 必须带回一个"连本人都未察觉的深层痛点"
> """)

insert_before("M06_实践与小结_微调研沙局与_Exp1_启动.md",
"在下周之前，各组必须完成队伍的最终集结",
"""
> [VISUAL]
> **Slide**: w03-slide-37_exp1_brief
> **Layout**: Center
> **Scene**: 血红色的实验任务简报封面：代号 EXP.01 "荒野与猎物"
> **Text**: 长线实战启动：告别模拟，走向真实战场
""")

insert_before("M06_实践与小结_微调研沙局与_Exp1_启动.md",
"> 但当他们站上讲台准备接受膜拜时，我的第一个问题就直接把他们钉死在了十字架上。",
"""> [VISUAL]
> **Slide**: w03-slide-38_failure_case
> **Layout**: Split
> **Scene**: 左侧是装帧精美、堆满图表的问卷报告；右侧是一个空荡荡的大学社团活动室和无人问津的报名表
> **Text**: 死于大楼里的完美报告
> """)

# M03
insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"群体极化现象，让你们花大价钱雇来的焦点小组",
"""
> [VISUAL]
> **Slide**: w03-slide-08_groupthink
> **Layout**: Center
> **Scene**: 一只巨大的狮子在会议室咆哮，周围的小绵羊全部在低头附和
> **Text**: 焦点小组的灾难：群体极化与意见领袖霸权
""")

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"想象一下一百年前的人类学家，他们为了搞清楚南太平洋某个孤岛上的土著",
"""
> [VISUAL]
> **Slide**: w03-slide-10_ethnography
> **Layout**: Split
> **Scene**: 左侧是现代人类学家在非洲原始部落记录笔记，右侧是互联网产品经理在杂乱的车间里观察工人
> **Text**: 田野调查的降维打击：从部落到现代工厂
""")

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"只有真正的**民族志式的实地观察**，才能捕获",
"""
> [VISUAL]
> **Slide**: w03-slide-11_nurse_case
> **Layout**: Split
> **Scene**: 会议室里优雅喝咖啡提需求的护士长 vs 急诊室凌晨三点满手是血戴着手套疯狂点不中按钮的崩溃护士
> **Text**: 场景摧毁了假设：无菌手套与 16 像素下拉菜单的惨烈碰撞
""")

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"> 结果，在录像回放中，他们发现了极其颠覆常识的生理真相。",
"""> [VISUAL]
> **Slide**: w03-slide-11_ideo_toothbrush
> **Layout**: Comparison
> **Scene**: 成年人灵巧的手指捏着细牙刷 vs 儿童像握拳头一样死死握住粗牙刷的X光透视图
> **Text**: 肌肉发育的隐藏真相：儿童与成人的物理差异
> """)

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"如果你在我的项目里敢问出这三个该死的问题，我会立刻把你开除",
"""
> [VISUAL]
> **Slide**: w03-slide-13
> **Layout**: Center
> **Scene**: 极度傲慢的产品经理像法官一样拿着问卷拷问用户
> **Text**: 诱导性审问：永远不要让用户对"未来"进行假设
> **List**: 错误案例1：你会更喜欢它吗？ | 错误案例2：你觉得这个定价合理吗？ | 错误案例3：你会觉得效率提升了吗？
""")

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"（绝大多数平庸的产品经理到这一步就停了",
"""
> [VISUAL]
> **Slide**: w03-slide-14_why1
> **Layout**: Split
> **Scene**: 崩溃摔键盘的用户与只顾着记下"加个进度条"的平庸产品经理
> **Text**: 5-Why 追问的浅层陷阱：停留在代码故障层
""")

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"全场死寂。各位看清楚发生了什么吗",
"""
> [VISUAL]
> **Slide**: w03-slide-14_why4
> **Layout**: Center
> **Scene**: 极度委屈的设计师看着满是马赛克的设计稿流泪
> **Text**: 连环追问的灵魂终点：挖出技术限制背后的人性屈辱
""")

insert_before("M03_讲授一_反直觉定性调研与问题发掘.md",
"人在接受访谈时，他的大脑总是试图去构建一个逻辑严密、",
"""
> [VISUAL]
> **Slide**: w03-slide-14_wrapup
> **Layout**: Center
> **Scene**: 用场景时间线死死钉住飘忽不定的访谈谎言
> **Text**: 记忆篡改对抗术：截断虚伪的高级反击
""")

