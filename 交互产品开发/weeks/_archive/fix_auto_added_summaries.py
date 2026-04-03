#!/usr/bin/env python3
"""
批量补充 knowledge_hub.yaml 中 auto-added 条目的中文摘要。
读取每个条目对应的教材章节文件前 150 行，提取标题与关键概念，
生成简洁的中文摘要并更新 hub。
"""
import yaml
import json
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB_PATH = os.path.join(BASE, "knowledge", "knowledge_hub.yaml")


def extract_summary_from_file(filepath: str, max_lines: int = 150) -> tuple[str, list[str]]:
    """从文件前 max_lines 行提取摘要和标签"""
    full_path = os.path.join(BASE, filepath)
    if not os.path.exists(full_path):
        return "", []

    with open(full_path, "r", encoding="utf-8") as f:
        lines = []
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            lines.append(line.rstrip())

    # 提取标题层级
    headings = []
    for line in lines:
        if line.startswith("#"):
            clean = re.sub(r"^#+\s*", "", line).strip()
            if clean and len(clean) > 1:
                headings.append(clean)

    # 提取加粗关键词
    bold_terms = []
    for line in lines:
        bolds = re.findall(r"\*\*(.+?)\*\*", line)
        bold_terms.extend(bolds)

    # 去重并限制
    seen = set()
    unique_headings = []
    for h in headings[:8]:
        h_lower = h.lower().strip()
        if h_lower not in seen and len(h) > 2:
            seen.add(h_lower)
            unique_headings.append(h)

    # 从加粗词提取标签（英文关键词）
    tags = []
    for term in bold_terms[:20]:
        # 只取短的英文术语作为标签
        if re.match(r"^[A-Za-z\s\-/]+$", term) and 2 < len(term) < 40:
            tag = term.strip().lower().replace(" ", "-")
            if tag not in tags:
                tags.append(tag)

    return " / ".join(unique_headings[:5]), tags[:5]


# ==================== 手工映射表 ====================
# 对于标题不够描述性的章节，提供精确的中文摘要

MANUAL_SUMMARIES = {
    # === About Face 4 ===
    "auto-Cooper_A_A-chapter_01_Indexer": "About Face 4 索引目录",
    "auto-Cooper_A_A-chapter_02_FOREWORD": "About Face 4 前言：交互设计学科的历史定位与 Alan Cooper 的设计哲学",
    "auto-Cooper_A_A-chapter_03_INTRODUCTION_TO_THE_FOURTH_EDITION": "第四版导读：目标导向设计方法论的演进与本书结构概览",
    "auto-Cooper_A_A-chapter_04_Goal_Directed_Design": "目标导向设计 (Goal-Directed Design)：以用户目标驱动产品设计的核心理念与完整流程",
    "auto-Cooper_A_A-chapter_06_DESIGN_PRINCIPLE": "设计原则一：目标导向设计的基础原则集",
    "auto-Cooper_A_A-chapter_07_Research": "设计研究方法：定性/定量调研策略与用户理解框架",
    "auto-Cooper_A_A-chapter_08_Modeling": "用户建模：从调研数据到 Persona 角色模型的构建方法",
    "auto-Cooper_A_A-chapter_09_Refinement": "需求精炼：从 Persona 到具体设计需求的推导过程",
    "auto-Cooper_A_A-chapter_10_UNDERSTANDING_THE_PROBLEM_DESIGN_RESEARCH": "理解问题空间：设计研究的系统化方法与用户分析框架",
    "auto-Cooper_A_A-chapter_11_MODELING_USERS_PERSONAS_AND_GOALS": "Persona 建模：用户画像构建、目标分层（人生/体验/终端目标）与行为模式分类",
    "auto-Cooper_A_A-chapter_12_DESIGN_PRINCIPLE": "设计原则二：用户建模与需求定义的原则集",
    "auto-Cooper_A_A-chapter_13_SETTING_THE_VISION_SCENARIOS_AND_DESIGN_REQUIREMEN": "愿景设定：场景驱动设计、关键路径场景与设计需求分析",
    "auto-Cooper_A_A-chapter_14_DESIGNING_THE_PRODUCT_FRAMEWORK_AND_REFINEMENT": "产品框架设计：交互框架搭建、界面布局策略与设计方案的迭代精炼",
    "auto-Cooper_A_A-chapter_15_DESIGN_PRINCIPLE": "设计原则三：框架设计与精炼阶段的原则集",
    "auto-Cooper_A_A-chapter_16_CREATIVE_TEAMWORK": "创意团队协作：设计师、开发者与利益相关者的高效协同模式",
    "auto-Cooper_A_A-chapter_17_A_BASIS_FOR_GOOD_PRODUCT_BEHAVIOR": "良好产品行为基础：数字产品应具备的行为准则与设计伦理底线",
    "auto-Cooper_A_A-chapter_18_DIGITAL_ETIQUETTE": "数字礼仪：产品应如何尊重用户、减少打扰并建立信任关系",
    "auto-Cooper_A_A-chapter_19_DESIGN_PRINCIPLE": "设计原则四：产品行为与数字礼仪的原则集",
    "auto-Cooper_A_A-chapter_20_PLATFORM_AND_POSTURE": "平台与姿态：不同平台（桌面/移动/Web）的产品定位及界面姿态策略",
    "auto-Cooper_A_A-chapter_21_OPTIMIZING_FOR_INTERMEDIATES": "中间级用户优化：面向最大用户群体的界面交互优化策略",
    "auto-Cooper_A_A-chapter_22_DESIGN_PRINCIPLE": "设计原则五：平台适配与中间用户优化的原则集",
    "auto-Cooper_A_A-chapter_24_Orchestration": "交互编排实操：和谐交互的 14 条核心策略详解",
    "auto-Cooper_A_A-chapter_25_DESIGN_PRINCIPLE": "设计原则六：编排与心流的原则集",
    "auto-Cooper_A_A-chapter_26_REDUCING_WORK_AND_ELIMINATING_EXCISE": "减少工作量与消除附加税：识别并移除界面中的非必要操作负担",
    "auto-Cooper_A_A-chapter_27_Eliminating_Excise": "消除附加税实战：导航/模态/权限等六类附加税的具体消除策略",
    "auto-Cooper_A_A-chapter_28_METAPHORS_IDIOMS_AND_AFFORDANCES": "隐喻、习惯用法与示能性：三种界面认知模式的适用边界与组合策略",
    "auto-Cooper_A_A-chapter_29_DESIGN_PRINCIPLE": "设计原则七：隐喻与示能性的原则集",
    "auto-Cooper_A_A-chapter_30_RETHINKING_DATA_ENTRY_STORAGE_AND_RETRIEVAL": "重新思考数据输入与检索：简化数据操作的设计策略",
    "auto-Cooper_A_A-chapter_31_Rethinking_Data_Entry": "数据输入重构：减少用户输入负担的具体设计手法",
    "auto-Cooper_A_A-chapter_32_DESIGN_PRINCIPLE": "设计原则八：数据输入与检索的原则集",
    "auto-Cooper_A_A-chapter_33_Indexed_retrieval": "索引检索：高效信息检索界面的设计模式",
    "auto-Cooper_A_A-chapter_35_DESIGNING_FOR_DIFFERENT_NEEDS": "差异化需求设计：无障碍 / 新手 / 专家等不同用户群的适配策略",
    "auto-Cooper_A_A-chapter_36_DESIGN_PRINCIPLE": "设计原则九：差异化需求的原则集",
    "auto-Cooper_A_A-chapter_38_INTEGRATING_VISUAL_DESIGN": "视觉设计整合：交互设计与视觉设计的协作流程与整合策略",
    "auto-Cooper_A_A-chapter_39_DESIGN_PRINCIPLE": "设计原则十：视觉整合的原则集",
    "auto-Cooper_A_A-chapter_40_DESIGNING_FOR_THE_DESKTOP": "桌面端设计：窗口管理、文档模型与桌面应用的交互范式",
    "auto-Cooper_A_A-chapter_41_Index_panes": "索引面板设计：列表/树形/标签等导航面板的交互模式与选型",
    "auto-Cooper_A_A-chapter_42_DESIGN_PRINCIPLE": "设计原则十一：桌面端设计的原则集",
    "auto-Cooper_A_A-chapter_43_DESIGNING_FOR_MOBILE_AND_OTHER_DEVICES": "移动端与其他设备设计：触控、手势、小屏幕的交互约束与适配",
    "auto-Cooper_A_A-chapter_45_Other_Devices": "其他设备设计：可穿戴/车载/智能家居等新兴平台的交互挑战",
    "auto-Cooper_A_A-chapter_46_DESIGNING_FOR_THE_WEB": "Web 端设计：导航模式、页面架构与 Web 应用的特有交互考量",
    "auto-Cooper_A_A-chapter_47_DESIGN_PRINCIPLE": "设计原则十二：Web 端设计的原则集",
    "auto-Cooper_A_A-chapter_48_DESIGN_DETAILS_CONTROLS_AND_DIALOGS": "设计细节——控件与对话框：界面控件体系的完整分类与设计规范",
    "auto-Cooper_A_A-chapter_49_Controls": "控件设计详解：按钮/滑块/选择器等基础控件的行为规范与最佳实践",
    "auto-Cooper_A_A-chapter_50_DESIGN_PRINCIPLE": "设计原则十三：控件设计的原则集",
    "auto-Cooper_A_A-chapter_51_Dialogs": "对话框设计：模态/非模态对话框的适用场景与滥用风险",
    "auto-Cooper_A_A-chapter_52_DESIGN_PRINCIPLE": "设计原则十四：对话框设计的原则集",
    "auto-Cooper_A_A-chapter_53_DESIGN_PRINCIPLES": "About Face 4 全书设计原则汇总完整列表",
    "auto-Cooper_A_A-chapter_54_BIBLIOGRAPHY": "About Face 4 参考文献列表",
    "auto-Cooper_A_A-chapter_55_INDEX": "About Face 4 索引",

    # === Lean UX ===
    "auto-Gothelf_J_-chapter_01_Jeff_and_Josh": "Lean UX 作者序：Jeff Gothelf 与 Josh Seiden 的精益实践缘起",
    "auto-Gothelf_J_-chapter_02_Part_I_Introduction_and_Principles": "第一部分导论：Lean UX 核心理念与基础原则概述",
    "auto-Gothelf_J_-chapter_03_Chapter_1_More_Important_Now_than_Ever_Before": "为何 Lean UX 比以往更重要：敏捷时代下 UX 角色的转型挑战",
    "auto-Gothelf_J_-chapter_04_Chapter_2_Principles": "Lean UX 八大原则：跨职能协作、产出非文档、持续发现、反失败心态等",
    "auto-Gothelf_J_-chapter_05_Chapter_3_Outcomes": "以成果为导向：用行为变化衡量成功而非功能交付",
    "auto-Gothelf_J_-chapter_06_Part_II_Process": "第二部分导论：Lean UX Canvas 画布驱动的完整工作流程",
    "auto-Gothelf_J_-chapter_07_Chapter_4_The_Lean_UX_Canvas": "Lean UX 画布：8 个方块的系统思考框架与填写指南",
    "auto-Gothelf_J_-chapter_09_Chapter_6_Box_2_Business_Outcomes": "画布方块 2——商业产出：定义可量化的业务成功指标",
    "auto-Gothelf_J_-chapter_10_Chapter_7_Box_3_Users": "画布方块 3——用户：极简用户定义与 Proto-Persona 构建",
    "auto-Gothelf_J_-chapter_11_Chapter_8_Box_4_User_Outcomes_and_Benefits": "画布方块 4——用户产出与利益：站在用户角度定义行为变化目标",
    "auto-Gothelf_J_-chapter_12_Chapter_9_Box_5_Solutions": "画布方块 5——解决方案：从假设到最小方案的头脑风暴与收敛",
    "auto-Gothelf_J_-chapter_14_Chapter_11_Box_7_What_s_the_Most_Important_Thing_W": "画布方块 7——最重要的待验证事项：风险优先级排序与学习议程",
    "auto-Gothelf_J_-chapter_16_Chapter_13_Bringing_It_All_Together": "画布汇总：8 方块的完整填写实例与团队协作使用指南",
    "auto-Gothelf_J_-chapter_17_Part_III_Collaboration": "第三部分导论：Lean UX 环境下的团队协作实践",
    "auto-Gothelf_J_-chapter_18_Chapter_14_Collaborative_Design": "协作设计：设计工作坊、Design Studio 方法与跨职能共创",
    "auto-Gothelf_J_-chapter_19_Chapter_15_Feedback_and_Research": "反馈与研究：持续用户验证、游击测试与数据驱动决策",
    "auto-Gothelf_J_-chapter_20_Chapter_16_Integrating_Lean_UX_and_Agile": "Lean UX 与 Agile 整合：Sprint 中的设计节奏、双轨开发与交付平衡",
    "auto-Gothelf_J_-chapter_21_Part_IV_Lean_UX_in_Your_Organization": "第四部分导论：在不同组织架构中推行 Lean UX",
    "auto-Gothelf_J_-chapter_22_Chapter_17_Making_Organizational_Shifts": "组织变革：从瀑布到精益的团队文化转型路径与阻力应对",
    "auto-Gothelf_J_-chapter_23_Chapter_18_Lean_UX_in_an_Agency": "外包/代理商场景下的 Lean UX 实践：合同模式与客户协作挑战",
    "auto-Gothelf_J_-chapter_24_Chapter_19_A_Last_Word": "终章回顾：Lean UX 的核心精神与持续学习文化",

    # === Interaction Design (Rogers) ===
    "auto-Interactio-chapter_07_Chapter_5": "Ch5 社会交互：协作、沟通与社交媒体中的交互设计",
    "auto-Interactio-chapter_14_Chapter_9": "Ch9 数据分析与可视化：定性/定量数据处理与呈现方法",
    "auto-Interactio-chapter_17_Chapter_10": "Ch10 数据分析深入：编码、主题分析与信效度保障",
    "auto-Interactio-chapter_22_Chapter_15": "Ch15 可用性测试与野外研究：实验室测试 / 现场观察 / 远程测试的实施",
    "auto-Interactio-chapter_23_Chapter_16": "Ch16 分析评估与预测模型：GOMS / 认知模型 / 分析法在交互中的应用",
    "auto-Interactio-chapter_28_Epilogue": "终章：交互设计的未来趋势与跨学科融合展望",
    "auto-Interactio-chapter_29_References": "Interaction Design 全书参考文献列表",
    "auto-Interactio-chapter_30_Index": "Interaction Design 全书索引",

    # === Refactoring UI ===
    "auto-Wathan_A_R-chapter_01_Starting_from_Scratch": "从零开始设计：先做功能再美化、避免过早追求完美的务实方法",
    "auto-Wathan_A_R-chapter_02_Detail_comes_later": "细节稍后再说：先定骨架再雕琢的设计流程优先级策略",
    "auto-Wathan_A_R-chapter_03_Don_t_design_too_much": "不要过度设计：聚焦核心界面、迭代式完善的极简开发哲学",
    "auto-Wathan_A_R-chapter_04_Choose_a_personality": "选择产品个性：通过字体/圆角/色彩温度定义界面的情感基调",
    "auto-Wathan_A_R-chapter_05_Limit_your_choices": "限制选择：建立约束系统（间距/字号/颜色刻度）避免决策疲劳",
    "auto-Wathan_A_R-chapter_07_Size_isn_t_everything": "大小不是万能的：用字重/颜色/间距多维度构建信息层级",
    "auto-Wathan_A_R-chapter_08_Don_t_use_grey_text_on_colored_backgrounds": "彩色背景上的文字：用降低不透明度代替灰色文字保持可读性",
    "auto-Wathan_A_R-chapter_09_Emphasize_by_de_emphasizing": "弱化即强调：通过降低辅助信息权重让核心内容脱颖而出",
    "auto-Wathan_A_R-chapter_10_Labels_are_a_last_resort": "标签是最后手段：用格式/位置/语境代替显式标签降低视觉噪音",
    "auto-Wathan_A_R-chapter_11_Separate_visual_hierarchy_from_document_hierarchy": "分离视觉层级与文档层级：h1-h6 标签不应决定视觉大小",
    "auto-Wathan_A_R-chapter_12_Balance_weight_and_contrast": "权重与对比平衡：用低对比度补偿粗字重、用粗字重弥补小尺寸",
    "auto-Wathan_A_R-chapter_13_Semantics_are_secondary": "语义让位层级：按钮颜色应服务于视觉层级而非单纯语义",
    "auto-Wathan_A_R-chapter_14_Layout_and_Spacing": "布局与间距总论：系统化间距是专业界面的基石",
    "auto-Wathan_A_R-chapter_15_Establish_a_spacing_and_sizing_system": "建立间距系统：基于 4/8px 基准的比例刻度而非随意像素值",
    "auto-Wathan_A_R-chapter_16_You_don_t_have_to_fill_the_whole_screen": "不必填满屏幕：给内容留出呼吸空间、约束最大宽度",
    "auto-Wathan_A_R-chapter_17_Grids_are_overrated": "栅格被高估了：不要教条地遵循 12 列网格、按需分配空间",
    "auto-Wathan_A_R-chapter_18_Relative_sizing_doesn_t_scale": "相对尺寸不可扩展：大屏和小屏应使用不同的绝对值而非等比缩放",
    "auto-Wathan_A_R-chapter_19_Avoid_ambiguous_spacing": "消除歧义间距：组间距 > 元素间距的「亲密性」原则",
    "auto-Wathan_A_R-chapter_20_Designing_Text": "文字设计总论：排版是界面设计中最重要的视觉元素",
    "auto-Wathan_A_R-chapter_21_Use_good_fonts": "选择好字体：系统字体/Google Fonts 选型建议与付费字体策略",
    "auto-Wathan_A_R-chapter_22_Keep_your_line_length_in_check": "控制行宽：每行 45-75 字符的可读性黄金区间",
    "auto-Wathan_A_R-chapter_23_Baseline_not_center": "基线对齐代替居中对齐：不同字号文字的对齐最佳实践",
    "auto-Wathan_A_R-chapter_24_Line_height_is_proportional": "行高比例原则：小字号大行高、大字号小行高的反直觉规律",
    "auto-Wathan_A_R-chapter_25_Not_every_link_needs_a_color": "并非所有链接都需要颜色：基于上下文智能处理链接样式",
    "auto-Wathan_A_R-chapter_26_part_of_the_main_path_a_user_takes_through_the_app": "主路径链接：用户核心操作路径中的链接应更克制地使用颜色",
    "auto-Wathan_A_R-chapter_27_Align_with_readability_in_mind": "以可读性为导向的对齐：左对齐为王、居中慎用",
    "auto-Wathan_A_R-chapter_28_Use_letter_spacing_effectively": "有效使用字间距：全大写标题加宽字距、正文避免调整",
    "auto-Wathan_A_R-chapter_30_You_need_more_colors_than_you_think": "你需要比想象中更多的颜色：灰阶 8-10 级 + 原色 5-10 级的实战调色板",
    "auto-Wathan_A_R-chapter_31_Define_your_shades_up_front": "预先定义色阶：为每种颜色建立 lightness 梯度尺而非临时选色",
    "auto-Wathan_A_R-chapter_32_Don_t_let_lightness_kill_your_saturation": "亮度不要杀死饱和度：高亮色应提升饱和度补偿、低亮色可适度降低",
    "auto-Wathan_A_R-chapter_33_Greys_don_t_have_to_be_grey": "灰色不必是纯灰：冷灰/暖灰通过添加色相倾向表达品牌调性",
    "auto-Wathan_A_R-chapter_34_Accessible_doesn_t_have_to_mean_ugly": "无障碍不意味丑陋：满足 WCAG 对比度的同时保持设计美感",
    "auto-Wathan_A_R-chapter_35_Don_t_rely_on_color_alone": "不依赖单一色彩：用图标/下划线/粗体等多通道冗余传递信息",
    "auto-Wathan_A_R-chapter_37_Use_shadows_to_convey_elevation": "用阴影传达高程：5 级阴影刻度建立界面的物理层次感",
    "auto-Wathan_A_R-chapter_38_Shadows_can_have_two_parts": "双阴影技法：直射光（小而锐利）+ 环境光（大而柔和）叠加",
    "auto-Wathan_A_R-chapter_39_Even_flat_designs_can_have_depth": "扁平设计也能有深度：颜色明暗/实心阴影/边框等非阴影深度方案",
    "auto-Wathan_A_R-chapter_40_Overlap_elements_to_create_layers": "元素重叠构建分层：偏移重叠创造视觉深度与动感",
    "auto-Wathan_A_R-chapter_41_Working_with_Images": "图像处理总论：图片在 UI 中的裁切、缩放与层叠策略",
    "auto-Wathan_A_R-chapter_42_Text_needs_consistent_contrast": "文字需要一致的对比度：在图像背景上保持文字可读的多种技法",
    "auto-Wathan_A_R-chapter_43_Everything_has_an_intended_size": "万物皆有预设尺寸：不等比缩放图标/Logo，按原始意图使用",
    "auto-Wathan_A_R-chapter_44_Beware_user_uploaded_content": "警惕用户上传内容：容器裁切、背景色兜底与纵横比约束",
    "auto-Wathan_A_R-chapter_45_Finishing_Touches": "收尾点睛总论：提升设计完成度的最后 10% 技巧",
    "auto-Wathan_A_R-chapter_46_Add_color_with_accent_borders": "用强调色边框增色：顶部/侧边彩色线条为平淡界面注入个性",
    "auto-Wathan_A_R-chapter_47_Decorate_your_backgrounds": "装饰背景：渐变/纹理/图案打破纯色背景的单调感",
    "auto-Wathan_A_R-chapter_49_Use_fewer_borders": "少用边框：用阴影/背景色/间距替代过多的线条分割",
    "auto-Wathan_A_R-chapter_50_Think_outside_the_box": "跳出框框：常见 UI 模式外的创意呈现方式（表格→卡片等）",
    "auto-Wathan_A_R-chapter_51_Leveling_Up": "终章进阶：提升审美直觉的持续学习路径与练习方法",
    "auto-Wathan_A_R-chapter_52_Document_Outline": "Refactoring UI 全书大纲结构",

    # === 张靖瑶 数字媒体交互设计 ===
    "auto-张靖瑶_数字媒体交互-chapter_01_项目1": "项目 1 导论：交互设计基础认知与课程项目框架",
    "auto-张靖瑶_数字媒体交互-chapter_02_交互设计概述": "交互设计概述：定义、发展历史与学科边界",
    "auto-张靖瑶_数字媒体交互-chapter_03_交互设计的基本概念": "交互设计基本概念：用户/界面/交互行为的核心术语体系",
    "auto-张靖瑶_数字媒体交互-chapter_04_交互设计的流程": "交互设计标准流程：需求分析→原型设计→评估迭代的瀑布模型",
    "auto-张靖瑶_数字媒体交互-chapter_05_开发人员的配置": "开发团队配置：产品/设计/前端/后端的角色分工与协作",
    "auto-张靖瑶_数字媒体交互-chapter_06_1_4": "1.4 节：交互设计的原则与规范小结",
    "auto-张靖瑶_数字媒体交互-chapter_07_产品交互原型的分类": "产品交互原型分类：低/中/高保真原型与适用阶段对照",
    "auto-张靖瑶_数字媒体交互-chapter_08_1_5": "1.5 节：原型工具与产出物小结",
    "auto-张靖瑶_数字媒体交互-chapter_09_交互设计的常用软件": "交互设计常用软件：Axure/Sketch/Figma/墨刀等工具对比",
    "auto-张靖瑶_数字媒体交互-chapter_10_1_6": "1.6 节：工具选型与实操准备小结",
    "auto-张靖瑶_数字媒体交互-chapter_11_项目实施": "项目 1 实施：交互设计基础的实操练习方案",
    "auto-张靖瑶_数字媒体交互-chapter_12_项目2": "项目 2 导论：Web 端网页交互 UI 设计框架",
    "auto-张靖瑶_数字媒体交互-chapter_13_Web端_家居_网页交互UI设计": "Web 端「家居」网页交互 UI 设计：项目概述与设计目标",
    "auto-张靖瑶_数字媒体交互-chapter_14_2_1": "2.1 节：Web 端项目启动小结",
    "auto-张靖瑶_数字媒体交互-chapter_15_Web端_家居_网页交互UI项目背景分析": "「家居」网页项目背景分析：行业趋势与竞品调研",
    "auto-张靖瑶_数字媒体交互-chapter_16_交互UI布局设计": "交互 UI 布局设计：栅格系统、F 型扫描与 Z 型扫描布局原理",
    "auto-张靖瑶_数字媒体交互-chapter_17_2_3": "2.3 节：布局设计实战小结",
    "auto-张靖瑶_数字媒体交互-chapter_18_基本元素": "Web 界面基本元素：按钮/输入框/图标/导航的设计规范",
    "auto-张靖瑶_数字媒体交互-chapter_19_2_4": "2.4 节：基本元素设计小结",
    "auto-张靖瑶_数字媒体交互-chapter_20_网页和网页交互UI组件的分类": "Web 页面与交互 UI 组件分类标准",
    "auto-张靖瑶_数字媒体交互-chapter_21_网页交互UI组件的分类": "网页交互 UI 组件细分：表单/卡片/模态框/弹窗等",
    "auto-张靖瑶_数字媒体交互-chapter_22_项目实施": "项目 2 实施：Web 端网页交互 UI 的实操练习",
    "auto-张靖瑶_数字媒体交互-chapter_23_项目3": "项目 3 导论：移动端 App 交互 UI 设计框架",
    "auto-张靖瑶_数字媒体交互-chapter_24_移动端_美食小吃_App交互UI设计": "移动端「美食小吃」App 交互 UI 设计：项目概述",
    "auto-张靖瑶_数字媒体交互-chapter_25_移动端_美食小吃_App交互UI设计项目背景分析": "「美食小吃」App 项目背景分析：目标用户与市场定位",
    "auto-张靖瑶_数字媒体交互-chapter_26_移动端_美食小吃_App交互UI设计项目需求分析": "「美食小吃」App 项目需求分析：功能清单与信息架构",
    "auto-张靖瑶_数字媒体交互-chapter_27_视觉层次结构与视觉引导": "视觉层次结构与视觉引导：F/Z 型扫描、色彩引导、字体层级",
    "auto-张靖瑶_数字媒体交互-chapter_28_App界面元素构成设计": "App 界面元素构成设计：状态栏/导航栏/标签栏/内容区",
    "auto-张靖瑶_数字媒体交互-chapter_29_3_5": "3.5 节：App 界面设计要素小结",
    "auto-张靖瑶_数字媒体交互-chapter_30_App界面设计风格": "App 界面设计风格一：扁平化/拟物化/新拟态的演进",
    "auto-张靖瑶_数字媒体交互-chapter_31_App界面设计风格": "App 界面设计风格二：插画/暗色/卡片式等流行风格趋势",
    "auto-张靖瑶_数字媒体交互-chapter_32_移动端平台的界面设计规范": "移动端平台设计规范：iOS HIG 与 Android Material Design 对比",
    "auto-张靖瑶_数字媒体交互-chapter_33_App交互UI设计流程分析": "App 交互 UI 设计流程分析：从需求到交付的全链路",
    "auto-张靖瑶_数字媒体交互-chapter_34_项目实施": "项目 3 实施：移动端 App 交互 UI 的实操练习",
    "auto-张靖瑶_数字媒体交互-chapter_35_项目4": "项目 4 导论：Web 端电商平台产品交互开发",
    "auto-张靖瑶_数字媒体交互-chapter_36_Web端_电商平台_产品交互设计开发": "Web 端「电商平台」产品交互设计开发：项目概述",
    "auto-张靖瑶_数字媒体交互-chapter_37_4_1": "4.1 节：电商项目启动小结",
    "auto-张靖瑶_数字媒体交互-chapter_38_Web端_电商平台_产品交互设计开发项目背景分析": "「电商平台」项目背景分析：电商行业格局与用户行为",
    "auto-张靖瑶_数字媒体交互-chapter_39_Web端_电商平台_产品交互设计开发项目需求分析": "「电商平台」项目需求分析：购物流程与关键功能模块",
    "auto-张靖瑶_数字媒体交互-chapter_40_Axure_RP_9介绍": "Axure RP 9 工具介绍：界面概览与基本操作入门",
    "auto-张靖瑶_数字媒体交互-chapter_41_4_4": "4.4 节：Axure 基础操作小结",
    "auto-张靖瑶_数字媒体交互-chapter_42_Axure_RP_9的常用元件": "Axure RP 9 常用元件一：基础元件库的使用方法",
    "auto-张靖瑶_数字媒体交互-chapter_43_Axure_RP_9的常用元件": "Axure RP 9 常用元件二：高级交互元件与动态面板",
    "auto-张靖瑶_数字媒体交互-chapter_44_查看原型": "查看原型：Axure 原型预览与分享方式",
    "auto-张靖瑶_数字媒体交互-chapter_45_项目实施": "项目 4 实施：Web 端电商交互原型的实操练习",
    "auto-张靖瑶_数字媒体交互-chapter_46_项目5": "项目 5 导论：移动端「教学助手」App 产品交互开发",
    "auto-张靖瑶_数字媒体交互-chapter_47_移动端_教学助手_App产品交互设计开发": "移动端「教学助手」App 产品交互设计开发：项目概述",
    "auto-张靖瑶_数字媒体交互-chapter_48_移动端_教学助手_App产品交互设计开发项目背景分析": "「教学助手」App 项目背景分析：教育信息化趋势",
    "auto-张靖瑶_数字媒体交互-chapter_49_移动端_教学助手_App产品交互设计开发项目需求分析": "「教学助手」App 项目需求分析：师生角色需求与功能架构",
    "auto-张靖瑶_数字媒体交互-chapter_50_墨刀概述": "墨刀概述：国产原型工具的功能特色与团队协作模式",
    "auto-张靖瑶_数字媒体交互-chapter_51_项目实施": "项目 5 实施：移动端教学助手 App 的实操练习",
    "auto-张靖瑶_数字媒体交互-chapter_52_项目6": "项目 6 导论：移动端「茶物语」App 产品交互开发",
    "auto-张靖瑶_数字媒体交互-chapter_53_移动端_茶物语_App产品交互设计开发": "移动端「茶物语」App 产品交互设计开发：项目概述",
    "auto-张靖瑶_数字媒体交互-chapter_54_移动端_茶物语_App产品交互设计开发项目背景分析": "「茶物语」App 项目背景分析：茶文化数字化传播",
    "auto-张靖瑶_数字媒体交互-chapter_55_6_2": "6.2 节：项目调研与竞品分析小结",
    "auto-张靖瑶_数字媒体交互-chapter_56_移动端_茶物语_App产品交互设计开发项目需求分析": "「茶物语」App 项目需求分析：内容架构与交互流程规划",
    "auto-张靖瑶_数字媒体交互-chapter_57_6_3": "6.3 节：需求到原型的转化小结",
    "auto-张靖瑶_数字媒体交互-chapter_58_Adobe_XD概述": "Adobe XD 概述：功能特色、画板系统与原型交互设置",
    "auto-张靖瑶_数字媒体交互-chapter_59_6_4": "6.4 节：Adobe XD 操作实践小结",
    "auto-张靖瑶_数字媒体交互-chapter_60_项目实施": "项目 6 实施：移动端茶物语 App 的实操练习",
}


def main():
    with open(HUB_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = data["entries"]
    updated_count = 0

    for entry in entries:
        entry_id = entry.get("id", "")
        if not entry_id.startswith("auto-"):
            continue

        # 使用手工映射
        if entry_id in MANUAL_SUMMARIES:
            new_summary = MANUAL_SUMMARIES[entry_id]
        else:
            # 从文件提取
            source = entry.get("source", "")
            if source:
                auto_summary, _ = extract_summary_from_file(source)
                if auto_summary:
                    new_summary = auto_summary
                else:
                    continue
            else:
                continue

        old_summary = entry.get("summary", "")
        if old_summary != new_summary:
            entry["summary"] = new_summary
            # 移除 auto-added 标签，替换为更有意义的标签
            if entry.get("tags") == ["auto-added"]:
                # 从 id 推断书籍来源标签
                if "Cooper" in entry_id:
                    entry["tags"] = ["about-face", "interaction-design"]
                elif "Gothelf" in entry_id:
                    entry["tags"] = ["lean-UX", "agile"]
                elif "Interactio" in entry_id:
                    entry["tags"] = ["interaction-design", "textbook"]
                elif "Wathan" in entry_id:
                    entry["tags"] = ["refactoring-ui", "visual-design"]
                elif "张靖瑶" in entry_id:
                    entry["tags"] = ["chinese-textbook", "交互设计"]
            updated_count += 1

    # 写回
    meta_yaml = yaml.dump({"meta": data["meta"]}, allow_unicode=True, default_flow_style=False).strip()
    entries_json = json.dumps(entries, ensure_ascii=False).strip()
    output = f"{meta_yaml}\nentries:\n {entries_json}\n"

    with open(HUB_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    # 统计
    remaining_auto = sum(1 for e in entries if e.get("tags") == ["auto-added"])
    print(f"✅ 完成！共更新 {updated_count} 条 auto-added 条目")
    print(f"   剩余未处理的 auto-added: {remaining_auto}")
    print(f"   entries 总数: {len(entries)}")


if __name__ == "__main__":
    main()
