---
description: 创建新课程的标准目录结构和配置文件
---

# /new_course 工作流

创建标准化的课程目录结构并注册到工作区清单。

**参数**:
*   `$1` (课程名): 课程的中文名称（即目录名）

**步骤**:

1.  **创建目录结构**
    ```bash
    mkdir -p "$1"/{knowledge/textbook,practices,weeks,build,admin}
    ```

2.  **创建 course.yaml**
    从模板复制并引导用户填写：
    ```bash
    cp .agent/templates/course.yaml.template "$1/course.yaml"
    cp .agent/templates/experiment_planning.md.template "$1/practices/experiment_planning.md"
    ```
    打开 `course.yaml` 并按模板注释逐节填写。模板已预置 ADR 005-009 所有字段占位。

    > **关键约束提醒**：
    > - **ADR 009 `content` 格式**：每行必须自带编号前缀（如 `1.1`、`2.3`），编号跨周连贯。WYSIWYG 模式下文本即最终大纲输出，旧的 `"理论: ...; \n实践: ..."` 标签格式已废弃
    > - **`chapter_title` 字段**：每周必填，格式为 `"第X章 {topic}"`，作为大纲章标题和教案 R0 的直接来源
    > - **`exp_id` 字段**：含实验内容的周次须挂载对应实验 ID（如 `exp_id: 1`），供实验日期推算
    > - **ADR 009 `lessons[].steps`**：常规周必须包含 5 阶段（复习/导入/讲授/实践/小结），首周可省略复习
    > - **ADR 008 类型约束**：`teaching_requirements` 为 `str`（纯文本）或 `dict`（推荐，含 `knowledge`/`ability`/`quality`/`method` 四维度），`supported_objectives` 必须为 `list[str]`
    > - **ADR 007**：`calendar[]` 教案索引字段直接在 `course.yaml` 维护，不经过脚本 frontmatter
    > - **ADR 005**：`normal_items.name` 为 `章节测试N`（无括号），`desc` 须先声明实验关联
    > - **ADR 010 `objectives` 约束**：每维度（knowledge/ability/quality）**≥ 3 条**，必须使用 `mappings` 数组格式，`requirement/point` 须与人培方案精确对应
    > - **ADR 012**：多班课程需在 `classes[]` 声明 `week_range`/`official_weeks`/`excluded_weeks`，教案按课程出一份、进度表按班各出一份
    > - **ADR 013**：`excluded_weeks` 生效后，生成器偏移映射自动跳过停课周，calendar 内容顺延
    > - **ADR 011 `experiments` 约束**：`type` 必须含「性」后缀（验证性/综合性/设计性/演示性），≥ 3 种类型，`group_size`/`requirement` 必填
    > - **ADR 017 实验编号命名**：`content`/`task`/`summary` 中引用实验时使用 `实验N(ExpN)` 格式
    > - **人培合规**：参照 `rule_training_plan_compliance.md`，确保 `objectives.mappings[].point` 与 `graduation_requirements.yaml` 精确一致
    > - **ADR 015 跨项目边界**：若需教务材料项目侧变更（如生成器修改），草拟委托消息，不直接修改

3.  **初始化 Practice 基础设施**

    1. 复制 practice schema 模板到新课程：
    ```bash
    cp .agent/templates/practice_schema.md "$1/practices/_schema.md"
    ```

    2. 遍历 `course.yaml` 的 `calendar[]`，为每个 `hours_practice > 0` 的周次
       生成骨架 practice YAML（`$1/practices/W0X_practice.yaml`）：
    ```yaml
    week: X
    title: "TODO: 从 course.yaml calendar[X].topic 填充"
    total_minutes: # hours_practice × 45
    theory_prerequisites: []
    experiment_link: ""
    phases: []
    homework:
      weight: ""
      deliverables: []
    ```

    3. 通知用户：
    ```
    ⚠️ 已为 N 个含实践课时的周次生成骨架 practice YAML。
    请通过 /design_practice 逐周设计实践步骤。
    ```

4.  **创建骨架文件**
    ```bash
    touch "$1/knowledge/glossary.md"
    ```

4.  **注册到 manifest.json**
    编辑 `.agent/manifest.json`，在 `courses` 数组中新增条目：
    ```json
    {
        "id": "<英文标识符>",
        "name": "<中文课程名>",
        "path": "<目录名>",
        "status": "pending"
    }
    ```

5.  **更新 INDEX.md**
    在 `.agent/INDEX.md` 的课程表格中新增一行。

6.  **通知用户**
    ```
    ✅ 课程 "$1" 脚手架已创建。
    请配置 course.yaml，将教材放入 knowledge/textbook/。
    请遵循 V5 架构：建立 weeks/W0X_Name/package.yaml，切分源文件放入 src/，并将图片素材存放于 public/。
    ```
