# Layout 规范 v2.1 — 语义别名与三层正交架构

> **状态**: Active (替代 layouts.md v1 扁平模型与 v2.0 的分离模型)
> **适用**: 交互产品开发 / 信息可视化 / 全部课程

---

## 设计原则：内紧外松 (Semantic UI vs Orthogonal Engine)

为了保持讲师编写脚本的极致流畅，本视觉系统在前端采用**语义别名**，在后端采用**三层正交模型**。这要求在编写 Markdown 时，你只需要考虑“教学场景”，而无需考虑复杂的 CSS 参数。

1. **作者不碰代码** — 隐藏 Intent 修饰符字段。
2. **场景即布局** — 填入最符合你教学直觉的预设名。
3. **内容自动渲染** — 无需声明这是“列表”还是“纯图”，填写相应字段，系统自动适配组件。

---

## 合法的 Layout 值 (12 个语义宏)

在 `[VISUAL]` 块中，`Layout` 字段仅允许填写以下 **12 个** 值之一：

| 布局/场景别名 | 描述 | 本质空间排布 (Engine Layer) |
|:---|:---|:---|
| **`Center`** | 内容水平/垂直居中对齐，单焦点视觉 | Center |
| **`CTA`** | 行动号召终页：黑底深色背景+醒目提示 | Center + cta style |
| **`Agenda`** | 带序号的议程/大纲目录样式 | Center + agenda style |
| **`Split`** | 双栏布局，左文右图或双栏对比 | Split |
| **`Quote`** | 金句卡片展示 | Split + quote component |
| **`Workshop`** | 工坊模式：带有步骤指引或计时器 | Split + workshop UI |
| **`Grid`** | 多块组合网格（3图、2×2 并列等） | Grid |
| **`Comparison`** | 左右直接对抗式的优劣/选项对比。**List 必须使用单行 `vs` 格式或 `label: items` 扁平冒号格式，严禁嵌套缩进列表** | Grid + compare theme |
| **`Full`** | 壁纸级占满全周边的沉浸大图或代码 | Full |
| **`Screenshot`** | 给截屏图片自动戴上电脑/手机外壳边框阴影 | Full + browser frame |
| **`Poll`** | 带有问卷或互动投票元素的特定版式 | Full + poll component |
| **`Flow`** | 线性流、节点连线、步骤链 | Flow |

> **提示：原有很多名词去了哪里？**
> 你不再需要 `Title` (请用 `Center`)、`List` / `Code` / `Table` (这些是内容类型，放入 `Split` 或 `Full` 中，系统会通过读取字段自动渲染)。详情见本文末尾。

---

## 字段规范表

在 `[VISUAL]` 块中包含的数据：

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| **Slide** | ✅ | Slide 标题（中文），兼作模块内唯一标识 |
| **Layout** | ✅ | 预设名，从上述 12 个合法值中选择 |
| **Scene** | ✅ | 画面的中文描述（AI 生图 / 人工预处理必须用到） |
| **Text** | 可选 | Slide 上显示的标题/关键文字 |
| **List** | 可选 | 列表内容。**单行格式**：用 `/` 分隔项；**多行格式**：`**List**:` 后换行，每项 `> - 项目`（必须保留 `>` 前缀）。**Comparison 专用格式**：每行用 `label: items` 冒号键值对，子项用顿号分隔（如 `> - ❌ 传统方法: 项目A、项目B、项目C`） |
| **Asset** | 可选 | 图片路径，推荐 MD 语法 `![预览](path)` |
| **Search** | 可选 | 网络搜索关键词（用于辅助生图） |
| **Caption** | 可选 | 注释/引用文字（渲染在底部） |
| **Code** | 可选 | 代码块内容 |

> **修改项**：Intent 字段已剥离，底层会自动根据你写的 12 种语义 Layout 推导 Intent。

### 自动推断规则 (Content Deduction)

同一个 Layout（比如 `Split`）可以展示无数种内容组合。引擎是如何知道的？
- 有 `Asset` 没文字 $\to$ 单侧图片组件
- 有 `List` 字段 $\to$ 无序列表渲染组件
- 有 `Code` 字段 $\to$ 代码高亮渲染器

**写法 A：单行 `vs` 格式**
```markdown
> [VISUAL]
> **Slide**: W01_S01h
> **Layout**: `Comparison`
> **Scene**: 左右对比：左侧"一刀切"（红色叉号），右侧"并行路径"（绿色勾号）
> **List**: ❌ 一刀切：强制消灭旧方式 / ✅ 并行路径：物理+数字双通道
```

**写法 B：多行 `label: items` 格式（含子项）**
```markdown
> [VISUAL]
> **Slide**: W01_S01h_v2
> **Layout**: `Comparison`
> **Scene**: 传统方法与现代方法的对比
> **List**:
> - ❌ 传统方法: 强制消灭旧方式、忽视过渡期、一刀切
> - ✅ 现代方法: 物理+数字双通道、渐进式迁移、用户自选
```

> ⚠️ **嵌套列表禁令**：Comparison 的 List 字段**严禁使用缩进嵌套列表**（如 `>   - 二级子项`）。SSG 构建层会将所有缩进层级拍平为一维数组，导致 H5 端触发错误的奇偶分配 fallback。

---

## 废弃旧别名名单

所有旧别名将在解析层拦截。如果遇到历史遗留遗留代码，必须按此表替换为以上 12 种预设之一：

| 废弃名字 | 理由 / 替换目标 |
|:---|:---|
| `Title`, `Section`, `Statement`, `Text`, `Stat` | 全部都是一个中间的文本焦点，请统一替换为 `Center` |
| `Image`, `Full Screen`, `Video`, `Canvas` | 请统一替换为 `Full` |
| `Card`, `Cards`, `Dashboard`, `Triple-Column`, `Quadrant`, `Quad`, `Icons`, `Template-Card` | 全部替换为 `Grid` (具体放几列通过引擎排版算法和数据的数目决断) |
| `Diagram`, `Timeline`, `Chart`, `Spectrum` | 全部替换为 `Flow` |
| `Image_Right`, `CodeBlock`, `Chat-Bubble` | 统一为 `Split` |
| `Table`, `List` | **重点错误：这不是布局，是内容。** 请改成其真实空间占据的骨架（多数情况是 `Split`，如果是单页展示则为 `Center` 或 `Grid`）|
