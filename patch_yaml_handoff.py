import os
import yaml

def patch_yaml(course_path, is_info_viz):
    yaml_file = os.path.join(course_path, 'course_assessment.yaml')
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    final_exam = data['exams']['final_exam'][0]
    
    # Add image paths
    ab_versions = final_exam['practice_paper']['ab_versions']
    ab_versions['A']['example_image'] = 'assets/exams/final_A_example.png'
    ab_versions['B']['example_image'] = 'assets/exams/final_B_example.png'
    
    # Update sections to 4 items
    if is_info_viz:
        final_exam['sections'] = [
            {
                'section_name': '数据抽象与编码映射',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 数据来源真实且清洗规范，成功进行了“数据到数据”的重构转换。\n2. 视觉通道映射准确，严格遵循通道有效性原则，避免过度设计。\n3. 【A卷示例】侧重微观生活数据颗粒度；【B卷示例】侧重宏观消费数据的系统性呈现。"
                }]
            },
            {
                'section_name': '视觉隐喻与认知引导',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 巧妙运用格式塔原理进行信息编排与图底分离，建立清晰视觉层级。\n2. 设计高反差属性（前注意加工）锁定核心注意力。\n3. 【A卷示例】隐喻具人文关怀与温度；【B卷示例】隐喻具客观理性与侵略性。"
                }]
            },
            {
                'section_name': '叙事结构与版式流向',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 版面具起承转合的完整叙事结构，形成闭环的故事脉络。\n2. 视线流向合理，与数据解读逻辑高度一致。\n3. 文本标签与图表视觉深度融合（Signaling）。"
                }]
            },
            {
                'section_name': '技术实现与媒介表现',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 熟练运用数字工具或手绘媒材，作品完成度极高。\n2. 【A卷示例】物理媒材肌理感契合微观叙事。\n3. 【B卷示例】交互/静态图表信息密度适中，符合专业标准。"
                }]
            }
        ]
    else:
        final_exam['sections'] = [
            {
                'section_name': '交互逻辑与信息架构',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 站点层级清晰，包含至少4个功能独立的核心页面。\n2. 导航与防错机制流畅，提供全局导航与状态提示。\n3. 【A卷示例】数字身份展馆链路闭环；【B卷示例】文化认知到互动体验链路闭环。"
                }]
            },
            {
                'section_name': '视觉表现与跨端适配',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 色彩、排版与字体体系统一，符合现代UI规范。\n2. 桌面与移动端均能保持严谨响应式比例和可用性。\n3. 【A卷示例】风格传递个人职业基调；【B卷示例】现代美学转译在地文化属性。"
                }]
            },
            {
                'section_name': 'AI协同与工程落地',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 经由Agent协作生成系统架构和前端组件，现代浏览器中无碍运行。\n2. 具备解决报错与样式偏移的Prompt控制纠偏能力。\n3. 代码语义化标签合理，满足基础A11y标准。"
                }]
            },
            {
                'section_name': '叙事体验与交付规范',
                'total_score': 25,
                'questions': [{
                    'type': '综合性',
                    'score': 25,
                    'content': "1. 页面模块按认知规律递进，包含合理微动效与反馈机制。\n2. 情绪共鸣渲染到位，实验报告能客观反思人机协作边界。\n3. 按要求完成产品走查视频及规范交付归档。"
                }]
            }
        ]
        
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

if __name__ == '__main__':
    base_dir = '/Users/yamlam/Downloads/2025-2026-2 课程'
    patch_yaml(os.path.join(base_dir, '信息可视化'), True)
    patch_yaml(os.path.join(base_dir, '交互产品开发'), False)
    
    # Create the directory structure for images so it's ready
    os.makedirs(os.path.join(base_dir, '信息可视化', 'assets', 'exams'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, '交互产品开发', 'assets', 'exams'), exist_ok=True)
    
    print("YAML patched and directories created.")
