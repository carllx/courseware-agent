import re

filepath = "/Users/yamlam/Downloads/2025-2026-2 课程/信息可视化/weeks/W01_Visual_Perception/src/M00_课程导览.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 替换 H3 标题
content = content.replace("### 一、 信息可视化：从生存本能到新读图时代", "### 一、 载体演进：信息可视化打通读图时代")
content = content.replace("### 二、 理论筑基：探索感知与数据素养", "> [ACTIVITY] Type: QA | Duration: 1min | Desc: 提问互动：结合刚才的例子，你认为日常生活中最忽悠人的数据谎言形式是什么？\n\n### 二、 理论筑基：感知与素养决定可视化成败")
content = content.replace("### 三、 创作冲刺：数字导演与全链路部署", "### 三、 创作冲刺：从静态图表迈向动态全链路")
content = content.replace("### 四、 Vibe Coding：掌控直觉编程与最高架构师思维", "### 四、 范式跃迁：直觉编程重塑设计架构思维")
content = content.replace("### 五、 成绩构成：平时实验与期末作品", "### 五、 考核机制：实战产出驱动最终能力评估")

# 替换锚词
content = content.replace("建立视觉化分析的能力", "建立**视觉化分析**的能力")
content = content.replace("叫做\"理论筑基\"。", "叫做\"**理论筑基**\"。")
content = content.replace("现代声明式配置架构优秀典范", "现代**声明式配置引擎**优秀典范")
content = content.replace("底层原生指令式物理引擎框架", "底层**原生指令式物理引擎**框架")
content = content.replace("跨入\"生成艺术\"的领域。我们会学习网络拓扑，学习力导向图。", "跨入\"**生成艺术**\"的领域。我们会学习网络拓扑，学习**力导向网络**。")
content = content.replace("交互形式——滚动叙事，也就是 Scrollytelling。", "交互形式——**滚动叙事 (Scrollytelling)**。")
content = content.replace("部署到 Vercel 或者 GitHub Pages 上，向全世界公开展示", "部署到 Vercel 或者 GitHub Pages 上，完成**全链路开发部署**，向全世界公开展示")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("M00 Fixed!")
