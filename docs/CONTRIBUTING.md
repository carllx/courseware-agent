# 新课程接入指南

> 从零接入一门新课程的全流程。

## 前提条件

| 依赖 | 说明 |
|:---|:---|
| Python 3.10+ | `/opt/anaconda3/envs/mybase/bin/python` |
| `python-docx` | `pip install python-docx` |
| Node.js 24+ | NVM 管理，用于 PPT 生成 |
| 教材文件 | PDF / DOCX / 扫描件 |
| 教学大纲 | 学校下发的课程标准文件 |

## 接入步骤

### Step 1: 创建脚手架

```
/new_course 数字音频编辑
```

Agent 自动创建标准目录结构：

```text
数字音频编辑/
├── course.yaml
├── knowledge/
│   ├── textbook/
│   └── glossary.md
├── practices/
│   └── experiment_planning.md
├── scripts/
│   └── 00_structure_map.md
├── visuals/
│   └── assets/
└── delivery/
```

### Step 2: 配置 `course.yaml`

`course.yaml` 包含两层职责：**备课工作流配置**（本工作区使用）和 **教务材料生成数据**（Schema 2.2，供 `教务材料/scripts/generate.py` 消费）。

#### 2a. 备课工作流字段

```yaml
course:
  id: digital_audio                    # 英文标识（唯一）
  name: 数字音频编辑                    # 中文名称
  semester: 2025-2026-2
  instructor: 张老师
  hours: 48                            # 总学时（简写，仅备课用）
  delivery_mode: workshop              # 语速模式

structure:
  type: weekly                         # weekly | project
  units:
    - id: W01
      name: 课程导论
    # ... 按周次列出所有教学单元

knowledge:
  entry_points:
    - knowledge/glossary.md

agent:
  style: "styles/design_system.md"     # 课程设计系统（可选）
  standards: "styles/visual_system.yaml"  # 机器可执行配置（可选）
  extra_rules: []
  extra_skills: []
```

#### 2b. 教务材料生成字段 (Schema 2.2)

> [!IMPORTANT]
> 若需通过 `generate.py` 生成大纲/进度表/教案等教务文档，以下字段**必填**。
> 完整 Schema 定义见 `教务材料/00_Data_Context/Spec_Global.md` §4。

```yaml
course:
  name: 数字音频编辑                    # 课程全称
  code: CNFU00XXXX                     # 课程代码
  semester: 2025-2026-2
  nature: 专业选修课                    # 五选一: 专业必修课/专业选修课/公共必修课/公共选修课/实践课程
  credits: 2.0
  department: 设计学院
  major: 数字媒体艺术
  classes:                             # 至少一个班级
    - name: 24数字媒体艺术
      schedule_time: 周三2-5节          # 格式: 周X N-M节，须与教务系统核对
      classroom: 温泉校区 XXX
      # week_range: "1-8"              # 可选: 仅在多班级不同周次时需要
      # official_weeks: 8              # 可选: 教务注册周数（ADR 012），仅多班时必填
      # excluded_weeks: [16]           # 可选: 法定假期停课周，进度表生成器跳过该日期，并自动进行偏移映射（ADR 013）
  hours:
    total: 48                          # 必须 = theory + practice
    theory: 24
    practice: 24
    # per_class: true                  # 可选: 多班课程表示单班学时（ADR 012）

teacher:
  name: 张老师
  title: 专任教师
  department: 数字媒体艺术

objectives:                            # ⚠️ ADR 010: 每维度 ≥3 条，必须使用 mappings 格式
  knowledge:
    - index: 1
      desc: 掌握...
      mappings:
        - requirement: "2 专业知识"       # 须与人培方案精确对应
          point: "2.1 基础知识掌握"
          support_level: H               # H/M/L
    - index: 2
      desc: 理解...
      mappings:
        - requirement: "2 专业知识"
          point: "2.2 跨学科知识整合"
          support_level: M
    - index: 3
      desc: 了解...
      mappings:
        - requirement: "2 专业知识"
          point: "2.3 全流程创作能力"
          support_level: M
  ability:
    - index: 1
      desc: 能够...
      mappings:
        - requirement: "4 实际应用能力"
          point: "4.1 专业技术实现能力"
          support_level: M
    - index: 2
      desc: 能够...
      mappings:
        - requirement: "3 创造性思维"
          point: "3.2 独立创意思考与原创设计"
          support_level: M
    - index: 3
      desc: 能够...
      mappings:
        - requirement: "4 实际应用能力"
          point: "4.2 设计验证与迭代能力"
          support_level: M
  quality:
    - index: 1
      desc: 具备...
      mappings:
        - requirement: "5 信息能力"
          point: "5.2 信息收集与筛选"
          support_level: L
    - index: 2
      desc: 具备...
      mappings:
        - requirement: "5 信息能力"
          point: "5.1 信息素养与数据伦理"
          support_level: M
    - index: 3
      desc: 具备...
      mappings:
        - requirement: "6 沟通表达"
          point: "6.1 专业表达能力"
          support_level: M

semester_config:
  start_date: "2026-03-02"

calendar:                              # 每周条目
  - week: 1
    topic: 课程导论
    content: 课程介绍与环境准备
    hours_theory: 2                    # ∑ 须 = hours.theory
    hours_practice: 2                  # ∑ 须 = hours.practice
    teaching_requirements: "..."       # ⚠️ 必须是 str (ADR 008), 以"通过本章学习"开头
    focus: "..."
    difficulty: "..."
    ideology: "..."
    teaching_method: "..."
    # --- 教案索引字段 (ADR 007: SSOT 在 course.yaml，不经过 frontmatter) ---
    supported_objectives: ["知识1", "能力1"]  # 本周支撑的课程目标
    task: "作业描述..."                       # 周作业
    teaching_requirements:             # 结构化教学要求（教案生成器使用）
      knowledge: "..."
      ability: "..."
      quality: "..."
      method: "..."
    lessons:
      - topic: ...
        objectives: [...]
        steps:                         # 教学环节摘要（教案生成器使用）
          - stage: 复习
            summary: "..."
            minutes: 10

textbooks:
  - title: "教材名"
    author: "作者"
    publisher: "出版社"
    year: "2024"
    type: textbook                     # textbook | reference

exams: {}                              # 即使考查课也必须有最小结构
```

#### 字段速查

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `course.id` | 备课 | 英文标识符，全局唯一 |
| `course.name` | ✅ | 中文课程名 |
| `course.code` | 教务 | 课程代码（如 CNFU003847） |
| `course.semester` | ✅ | 学期标识 |
| `course.nature` | 教务 | 五选一课程性质 |
| `course.credits` | 教务 | 学分 |
| `course.classes` | 教务 | 班级列表（含 `schedule_time`, 可选 `week_range`/`official_weeks`/`excluded_weeks`）（ADR 012） |
| `course.hours` | ✅ | 备课用简写 `48` 或教务用结构 `{total, theory, practice}` |
| `course.delivery_mode` | 可选 | `lecture`(180字/分) / `workshop`(140字/分) / `video_essay`(160字/分) |
| `objectives` | 教务 | **ADR 010**: 三类目标，每维度 ≥3 条，使用 `mappings: [{requirement, point, support_level}]` 数组格式 |
| `calendar` | 教务 | 每周教学日历 |
| `textbooks` | 教务 | 教材列表 |
| `exams` | 教务 | 考核结构（ADR 004 要求必填） |
| `semester_config` | 教务 | 含 `start_date` 用于日期计算 |
| `structure.type` | 备课 | `weekly`（按周次）或 `project`（按项目阶段） |
| `structure.units` | 备课 | 教学单元列表 |
| `knowledge.entry_points` | 备课 | Agent 加载知识的入口文件列表 |
| `agent.style` | 可选 | 设计系统人类可读版路径 |
| `agent.standards` | 可选 | 设计系统机器可执行版路径 |

### Step 3: 填充知识库

```bash
# 放入教材
cp 教材.pdf 数字音频编辑/knowledge/textbook/

# 放入教材
cp 教材.pdf 数字音频编辑/knowledge/textbook/

# 编写术语表（可选，Agent 写作时也会生成）
vi 数字音频编辑/knowledge/glossary.md
```



### Step 4: 实验规划 (New)
> [!NOTE]
> 实验文档目前需手动或半自动化制作。

编辑 `practices/experiment_planning.md`，规划实验项目（名称、类型、学时、内容），作为后续生成实验指导书的依据。

### Step 5: 编写脚本 (Scripting)

1.  **创建脚本文件**：在 `scripts/` 下创建 `Sxx_Topic.md`。
2.  **定义元数据 (Frontmatter)**：
    ```yaml
    ---
    week: 1
    topic: "课程介绍"
    title: "S01: 导论"
    theory_hours: 2
    practice_hours: 0
    created: 2026-02-19
    ---
    # ❌ 禁止在此添加 supported_objectives/task/steps 等教案字段
    # 这些字段的 SSOT 在 course.yaml（ADR 007）
    ```
3.  **大纲同步**：运行 `python .agent/skills/validation_suite/scripts/sync_syllabus.py --course "课程名"` 自动生成 `00_structure_map.md`。
```

### Step 6: 开始写作

```
/write 数字音频编辑 W01
```

### Step 7: 验证

```
/validate_script 数字音频编辑
```

确认所有检查通过后，进入下一单元。

## 目录结构检查清单

| ✅ | 目录/文件 | 说明 |
|:---|:---|:---|
| ☐ | `course.yaml` | 元数据完整 |
| ☐ | `knowledge/textbook/` | 教材已放入 |
| ☐ | `scripts/*.md` | 脚本 Frontmatter 已定义且同步 |
| ☐ | `visuals/assets/` | 目录已创建 |
| ☐ | `.agent/manifest.json` | 课程已注册 |
| ☐ | `.agent/INDEX.md` | 课程已添加到导航 |
## 代码卫生 (ADR 014)

修改 `教务材料/scripts/` 下的生成器代码时，须遵守以下清理规则：

| 规则 | 说明 |
|------|------|
| 迁移后即清 | 技术方案迁移完成后，同步清除旧 import、旧回退代码、废弃文件 |
| 禁用 `_deprecated/` | 废弃代码由 Git 历史归档，禁止重建或长期保留 `_deprecated/` 目录 |
| 可变数据外部化 | 假日/学期日期等硬编码 → `semester_calendar.yaml` 等外部数据源 |
| 中文字面量 | 中文业务字符串禁止使用 `\uXXXX` 转义，直接写中文 |
| 通用函数归位 | 纯 XML 辅助函数收归 `docx_engine.py`（1 个消费者可就地标 TODO） |
| 近重复即合并 | 发现功能高度重叠的函数立即合并，通过参数区分行为 |

## 常见问题

### Q: `weekly` 和 `project` 类型有什么区别？

- **weekly** — 按周次编号（W01, W02, W03...），适合常规学期课程
- **project** — 按阶段编号（S01, S02, S03...），适合项目制课程（如实习指导）

### Q: 可以为课程定制视觉风格吗？

可以。在 `<课程>/styles/` 下放置 `design_system.md`（人类可读版）和 `visual_system.yaml`（机器可执行版），并在 `course.yaml` 的 `agent.style` / `agent.standards` 字段中指向它们。`/write` 和 `/ppt` 工作流会自动读取。

### Q: `delivery_mode` 会影响什么？

影响 `validate_script_length.py` 的语速估算：
- `lecture` = 180 字/分（讲授型）
- `workshop` = 140 字/分（工作坊型，留更多实操时间）
- `video_essay` = 160 字/分（录播型）

### Q: 如何跨课程共享知识？

将共享资料放在工作区根目录的 `docs/` 或 `reference/` 下，在各课程的 `course.yaml` 中通过 `knowledge.entry_points` 引用。

### Q: 人文层标签为什么是必须的？

研究表明，纯技术讲授的知识留存率约 10%，而与故事/隐喻关联的知识留存率可达 65%。人文层标签（`[STORY TIME]`、`[PHILOSOPHY]` 等）确保每份脚本都有"记忆锚点"。

### Q: Agent 如何为人文层标签寻找素材？

执行 `/write` 时，Agent 会在写作前自动激活 `narrative_archaeologist` 技能执行深度调研：

1. **Search Playbook** — 为每种标签类型构造专用搜索词（中英文双语）
2. **3-Pass Protocol** — 广搜（建立候选池）→ 深挖（验证来源）→ 锚点回归（绑回技术概念）
3. **Quality Gate** — 过滤无来源、与技术无关、文化不适配的素材

调研成果直接转化为脚本中的人文层标签内容，确保有据可查。
