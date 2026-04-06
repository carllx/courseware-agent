import urllib.request
import os

images = {
    # M01
    "S02_Metaphors_in_Vis": "教材:郝亚维-流柱图与雷达图",
    "S02b2_Frames_of_Mind_Meta_Art": "案例:Alberto_López-Frames_of_Mind",
    
    # M02
    "S03b_Marks_Hierarchy": "教材:几何递进阶梯图(0D-2D)",
    "S04_Channel_Effectiveness": "教材:Munzner-通道视觉效能排序梯队",
    "S04c_Color_Lie_Map": "案例:美国选举地图视觉谎言",
    "S04d_Magnitude_Ranking": "教材:Munzner-量化通道排名阶梯图",
    "S04e_Identity_Ranking": "教材:Munzner-标识通道排名阶梯图",
    
    # M03
    "S05_Channel_Accuracy": "教材:长度vs面积心理测试对比图",
    "S05b_Stevens_Power_Law": "教材:Stevens幂定律感知曲线",
    "S05c_Area_Volume_Illusion": "教材:面积体积错觉对比图",
    "S05d_Wealth_Bubble_Lie": "案例:苹果与小米伪3D气泡对比灾难",
    "S05f_Checker_Shadow_Illusion": "教材:阿德尔森阴影棋盘错觉",
    "S06b_Conjunction_Search_Demo": "教材:特瑞斯曼结合检索(Z字寻靶)实验图",
    "S06d_Three_Colormaps": "教材:Munzner-三大色阶不可跨界表",
    "S06e_Accessibility_ColorBrewer": "实验:红绿色盲前后温度图对比",
    "S06f_ColorBrewer_Simulator_Tools": "界面:ColorBrewer安全检测面板截图",
    
    # M04
    "S07_Data_Ink_Ratio": "概念:Tufte-Data Ink Ratio对比",
    "S07c_Erasing_Steps": "教材:Tufte著名删减四步法名场面",
    "S07d_3D_Pie_Sins": "案例:3D透视饼图反面教材",
    "S07d2_Eyes_Beat_Memory": "概念:Tufte-小多图分面示例",
    "S07e_No_Unjustified_3D": "法则:Munzner-No Unjustified 3D",
    
    # M05
    "S08_The_Black_Museum": "案例:信息犯罪黑历史3大怪图并列",
}

import urllib.parse
base_url = "https://placehold.co/1920x1080/1A191C/E6B828.png?text="

for slide, text in images.items():
    safe_text = urllib.parse.quote(f"TEXTBOOK ASSET\n\n{text}\n\n(Waiting for Manual Replacement)")
    url = base_url + safe_text
    output_path = f"public/textbook/{slide}.png"
    print(f"Downloading {output_path}...")
    try:
        urllib.request.urlretrieve(url, output_path)
    except Exception as e:
        print(f"Failed {slide}: {e}")
