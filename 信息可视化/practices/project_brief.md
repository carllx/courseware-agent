# 综合实践项目说明书
# 信息可视化设计 · 实验 4：综合项目实战

> [!NOTE]
> 本文档对应 `course.yaml` 中 `experiments[id:4]`（创新型，6学时），覆盖第 7–8 周全部实践内容。
> 学生最终成果计入**期末成绩（50%）**。

---

## 一、项目定位

本项目是全课程的**终极综合输出**。目标是运用前六周积累的理论（Munzner 嵌套模型、视觉编码法则）与技术能力（ECharts / D3.js Vibe Coding 工作流），围绕一个具有**人文关怀与社会价值**的真实议题，独立完成一件可在公网展示的**交互数据艺术作品**。

作品评判标准不是"代码量"，而是：

> **当观众看到你的作品，是否只感受到你传递的情感冲击，而对底层算法浑然不觉？**

---

## 二、选题方向

围绕以下**社会/文化议题**自主选题，鼓励聚焦小而真实的切口：

| 方向类别 | 参考议题示例 |
|---|---|
| **文化遗产** | 非遗技艺传承人口分布与消亡趋势 |
| **生态环境** | 近20年城市热岛、海平面、物种灭绝数据 |
| **社会人口** | 老龄化、留守儿童、城乡教育资源差异 |
| **当代情绪** | 社交媒体情感极化、睡眠危机、孤独指数 |
| **历史记忆** | 重大历史事件的时间轴与影响范围叙事 |

> [!IMPORTANT]
> **选题原则**：必须有**可获取的真实公开数据集**支撑（Kaggle / 联合国数据库 / 世界银行 / 政府开放平台）。严禁使用虚构数据。

---

## 三、Munzner 四层嵌套验证（立项必做）

在动手之前，必须完成以下四层自我 Critique：

```
层 1 — 领域情况 (Domain Situation)
    你到底想帮谁"看清"什么？受众是谁？
    
层 2 — 数据/任务抽象 (Data / Task Abstraction)
    你拥有支撑该诉求的真实数据吗？数据类型？任务类型？
    
层 3 — 视觉编码/交互 (Visual Encoding / Interaction)
    你的视觉隐喻（颜色/形状/位置/动效）是否匹配任务语义？
    
层 4 — 算法与性能 (Algorithm)
    页面在真实浏览器中能流畅渲染吗？数据量是否过大？
```

> [!WARNING]
> 任何底层的失败，都会导致外层的全面崩塌。  
> 该四层验证需在"项目一页纸"中体现，并于**第 7 周课堂 Critique 互评**中接受同学审查。

---

## 四、Vibe Coding 工程规范

**禁止一次性将所有需求扔给 AI**。必须遵循以下分步提示词接力策略：

```
Step 1  →  让 AI 生成干净的 Tidy Data（JSON / CSV）
Step 2  →  让 AI 生成孤立的静态可视化组件（D3 / ECharts 单文件）
Step 3  →  让 AI 建立空 HTML 外壳，插入 ScrollTrigger / 页面结构
Step 4  →  将组件封入外壳，人工打通数据绑定与交互 API
Step 5  →  CSS 艺术封装（Glassmorphism 风格、无衬线大字体、留白网格）
Step 6  →  部署至 GitHub Pages 或 Vercel
```

> [!TIP]
> 遇到结构性崩溃（作用域幻觉 / Z-index 坍塌 / 数据竞态），**不要把全部代码丢给模型**。  
> 精准截取问题段落，向 AI 描述具体异常，是本课程最核心的技术直觉训练。

---

## 五、时间节点

| 时间 | 里程碑 | 课内活动 |
|---|---|---|
| **第 7 周课堂** | 完成"项目一页纸"（含 Munzner 四层验证） | Workshop 选题 + Critique 互评 |
| **第 7 周课后** | 收集全部 Tidy 数据集，完成基础图表单文件原型测试 | 自主冲刺 |
| **第 8 周课堂** | 联调完毕，完成部署，进行 Final Presentation | 展示 + 互评 |

---

## 六、交付物清单

| # | 交付内容 | 格式要求 |
|---|---|---|
| 1 | **项目一页纸** | Markdown / PDF，含 Munzner 四层验证与数据源链接 |
| 2 | **源代码包** | HTML + CSS + JS + 数据文件，结构清晰，含注释 |
| 3 | **在线演示链接** | GitHub Pages 或 Vercel 公网可访问 URL |
| 4 | **课堂 Presentation** | 5分钟口头展示 + 1分钟"Best Prompt"分享 |
| 5 | **实验报告** | 含议题背景、设计决策说明、Vibe 过程反思（800字以上） |

---

## 七、评分细则

> 对应 `course.yaml → experiments[id:4]`（创新型，6学时）

| 评分维度 | 权重 | 评价要点 |
|---|---|---|
| **议题深度与数据真实性** | 20% | 选题有人文价值，数据来源可信、处理规范 |
| **视觉编码合理性** | 20% | 通道选择符合 Munzner 理论，隐喻清晰无歧义 |
| **Vibe 工作流完整性** | 20% | 提示词接力策略清晰，报告中有过程记录 |
| **交互体验与艺术感** | 20% | 作品具可操作性，排版具艺术张力 |
| **部署与独立完整性** | 10% | 成功上线，公网可访问，无严重渲染错误 |
| **Presentation 表达** | 10% | 叙事清晰，数据洞察与设计意图表达到位 |

---

## 八、参考资源

- **数据平台**：[Kaggle](https://www.kaggle.com/datasets) · [World Bank Open Data](https://data.worldbank.org/) · [国家统计局](https://www.stats.gov.cn/) · [UN Data](https://data.un.org/)
- **可视化框架**：[ECharts 示例库](https://echarts.apache.org/examples/) · [D3.js Observable](https://observablehq.com/@d3)
- **部署平台**：[GitHub Pages](https://pages.github.com/) · [Vercel](https://vercel.com/)
- **设计灵感**：[Pudding.cool](https://pudding.cool/) · [The Functional Art](http://www.thefunctionalart.com/) · [Behance · Data Visualization](https://www.behance.net/search/projects?search=data+visualization)

---

*文档版本：v1.0 | 创建：2026-02-21 | 对应课程：信息可视化设计 CNFU003847*
