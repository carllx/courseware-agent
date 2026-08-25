---
description: "逐字稿综合审查与修复（Subagent 串行协同版，支持单模块/周次目录）。替代原有的 prompts.md 手动工作流。"
---
# 逐字稿综合审查与修复 (/revise)

## 🎯 目标与机制

此工作流用于对指定的教学模块（或整个周次目录）执行深度的“脱水降维重写”与“质量审查”。
你（当前的主控 Agent）将扮演 **Orchestrator（调度员）**，绝不亲自进行文本修改或诊断。你需要使用 `define_subagent` 动态定义专业子代理，并使用 `invoke_subagent` 依次唤起它们。

**对于整个周次的遍历处理，必须遵循“无状态隔离（阅后即焚）”原则。**

## 📝 流程执行规范

当用户输入 `/revise <路径>`（路径可为具体文件如 `M01_xxx.md`，或一个周次目录如 `weeks/W06_*/src/`）时，执行以下步骤：

### Phase 1: 准备工作 (Orchestrator 初始化与循环策略)

1. 创建或更新全局 `task.md` 跟踪状态。
2. 分析目标路径。如果是目录，请通过 `list_dir` 工具获取该目录下所有后缀为 `.md` 的教学模块列表。
3. **主控外层循环启动**：按文件顺序依次对每个模块独立执行 Phase 2 的流水线。**必须等上一个模块的视觉装配彻底完成后，再进入下一个模块的 Phase 2。**

### Phase 2: 串行审查流 (单模块 Subagent Pipeline)

对于每一个独立的模块 `{CURRENT_MODULE_PATH}`：

> **核心隔离纪律**：无论是第几个模块，主控必须使用 `invoke_subagent` 唤起**全新**的子代理实例，确保其获得最干净的注意力。禁止使用 `send_message` 复用旧的子代理会话。必须在派发任务时告知子代理该文件的**总行数 (Total Lines)**，并提醒其完整阅读避免截断。

#### Step 2.0: 自动化基线扫描 (Orchestrator 亲自执行)
- **动作**：主控调用终端工具运行以下脚本，并将输出结果暂存，在后续派发任务时作为 Context 喂给子代理：
  1. `python .agent/scripts/validation/validate_script_length.py "<脚本路径>" --module-breakdown`（获取字数和密度退化情况）
  2. `python .agent/scripts/validation/validate_visual_text_sync.py "<脚本路径>"`（获取 Signaling Sync 信标错误）
  3. （可选）`python .agent/skills/cheat_sheet_generator/scripts/generate_cheat_sheet.py "<脚本路径>" --diagnose`（获取骨架链与段落推进率）

#### Step 2.1: 认知排雷专家 (Cognitive Auditor)
- **动作**：使用 `define_subagent` 动态定义名为 `cognitive_auditor` 的子代理。
  - **Description**: 专职以学生视角扫描视听矛盾、逻辑断裂和解法超界。100%注意力放在逻辑上，屏蔽文本排版和视觉素材的干扰。
  - **System Prompt**: 
    你是 `cognitive_auditor` 认知排雷专家。**在开始审查模块前，你必须首先使用 `view_file` 工具读取 `.agent/rules/rule_student_empathy_guard.md`、`.agent/skills/cognitive_walkthrough/SKILL.md` 以及 `docs/NARRATIVE_ARCHITECTURE.md` 的全文，严格以其标准执行。**
    请确保完整阅读目标模块（行号 1 到 总行数），按时间顺序逐段“听课”，捕捉体验逻辑层漏洞。特别注意：若模块完全缺乏情感共鸣点（Emotional Spark），请预警 `[NO_EMOTIONAL_SPARK]` 建议后续触发素材挖掘。
    **【重要输出规范】**：你不能只提出抽象建议。对于需要修复的逻辑断层，你必须在诊断报告中直接提供可供主控实施落盘的代码块，明确标注精准的 `Target Content` 和对应的 `Replacement Content`。
  - **Tool Permissions**: 赋予文件读取权限 (`enable_write_tools=false`)。
- **唤起**：使用 `invoke_subagent` 派遣它审查 `{CURRENT_MODULE_PATH}`。
- **审批**：等待返回报告。将报告展示给用户并**停下等待审批**。
- **修复**：用户批准后，**主控 Agent（你）**使用文件修改工具严格依据专家输出的 Patch 执行落盘修复，严禁主控自我重写发散。

#### Step 2.2: 叙事外科医生 (Narrative Surgeon)
- **动作**：使用 `define_subagent` 动态定义名为 `narrative_surgeon` 的子代理。
  - **Description**: 专职文本冗余清理、Mayer一致性检查、SCQA 叙事弧线修复以及 Signaling 信标修复。
  - **System Prompt**: 
    你是 `narrative_surgeon` 叙事外科医生。**在开始前，必须使用 `view_file` 工具读取 `.agent/rules/rule_coherence_audit.md` 和 `.agent/rules/rule_visual_signaling.md`。**
    主控会为你提供自动化基线扫描中发现的 Signaling 缺失或冗余数据。请结合该数据：
    1. 揪出修辞废话与 Mayer 冲突点。
    2. 修复 Signaling 信标（List 字段规范）。
    **【重要输出规范】**：你必须在最终的诊断报告中直接输出精确的改写文本块（明确提供可以直接匹配的 `Target Content` 及其重写后的 `Replacement Content`），使主控能够免思考直接打补丁。
  - **Tool Permissions**: 赋予文件读取权限 (`enable_write_tools=false`)。
- **唤起**：使用 `invoke_subagent` 派遣它审查 `{CURRENT_MODULE_PATH}`。
- **审批**：将报告展示给用户并**停下等待审批**。
- **修复**：用户批准后，主控 Agent 严格执行 Patch 替换。

#### Step 2.3: 知识外科医生 (Knowledge Surgeon)
- **动作**：使用 `define_subagent` 动态定义名为 `knowledge_surgeon` 的子代理。
  - **Description**: 专职术语脱水平权，并严格遵循 Quiz 设计准则补全缺失的检查点。
  - **System Prompt**: 
    你是 `knowledge_surgeon` 知识外科医生。**在开始前，必须使用 `view_file` 工具读取 `.agent/rules/rule_quiz_design.md` 和 `docs/SCRIPT_SPEC.md`。**
    你的核心任务是：
    1. 寻找可以进行平权降维和生动化处理的生涩术语概念（保留术语名，跟白话解释）。
    2. 根据模块的知识流断层或主控给出的诊断标记，指出需要补充 Quiz 的位置，并强制按照 `rule_quiz_design.md` 的要求（如遮盖测试、Haladyna原则）与 `SCRIPT_SPEC.md` 中 `[ACTIVITY] Type: Quiz` 的格式生成完整的题干草案（含 Options 和 Explain）。
    **【重要输出规范】**：你必须在最终的诊断报告中直接输出精确的改写文本块（明确提供可以直接匹配的 `Target Content` 及其重写后的 `Replacement Content`），使主控能够免思考直接打补丁。
  - **Tool Permissions**: 赋予文件读取权限 (`enable_write_tools=false`)。
- **唤起**：使用 `invoke_subagent` 派遣它审查 `{CURRENT_MODULE_PATH}`。
- **审批**：将报告展示给用户并**停下等待审批**。
- **修复**：用户批准后，主控 Agent 严格执行 Patch 替换。

#### Step 2.4: 叙事素材挖掘专家 (Narrative Archaeologist) [可选步骤]
- **动作**：若 `cognitive_auditor` 在 2.1 中标记了 `[NO_EMOTIONAL_SPARK]` 且用户希望补充情感火花，则激活 `narrative-archaeologist` 技能，通过网络搜索补充相关隐喻或生动案例，写入备忘录。用户审批后由主控注入脚本。

#### Step 2.5: 视觉装配专家 (Visual Assembler)
- **动作**：使用 `define_subagent` 定义名为 `visual_assembler` 的子代理。
  - **Description**: 专职视觉资产盘点、间距核验、教材匹配和素材装配计划制定。
  - **System Prompt**: 
    你是 `visual_assembler` 视觉装配专家。**在开始前，必须使用 `view_file` 工具读取 `.agent/skills/script_format/SKILL.md` (重点提取关于视觉密度的章节)**。
    盘点目标脚本中所有 `[VISUAL]` 块。检查是否存在大于 360 字的视觉缺口，并将未就绪资产分为【A类：需AI生成】和【B类：需真实素材】。输出视觉装配清单建议。不直接修改文件。
  - **Tool Permissions**: 赋予文件读取权限 (`enable_write_tools=false`)。
- **唤起**：使用 `invoke_subagent` 派遣它核查 `{CURRENT_MODULE_PATH}`。
- **审批**：将报告展示给用户并**停下等待审批**。
- **装配**：用户批准后，主控 Agent 负责协助用户落盘资产。

## ⚠️ 通用行动纪律 (Orchestrator 必读)
1. **定量数据赋能**：主控在调度外科医生（Surgeons）时，必须将 Step 2.0 扫描出的报错信息（如超标的密度、缺失的 Signaling）直接喂入 Prompt，为 Subagent 提供明确的靶点。
2. **防静默黑盒**：Subagent 必须给出具体的替换 Patch，主控只扮演“补丁执行者”，严禁主控在未得到精确 Patch 时依靠自己去凭空重写大段核心文字。
3. **严格串行保护**：无论是单模块内部的 Cognitive -> Narrative -> Knowledge -> Visual，还是外层的 M01 -> M02 -> M03 循环，必须保持严格串行。这防止了文本行号在流水线中错位。
4. **视觉落盘防超界守则**：主控在最终协助用户生成视觉素材或填入下载链接时，**主控自身必须首先读取并牢记 `.agent/rules/rule_asset_placement_guard.md`**，确保写入的资源路径严格遵守周次级 `public/` 的目录约定，绝对不可将资产混杂到课程级公有目录下。
5. **修复前强制备份**（引用 `rule_security_governance.md` §6.4）：主控在对任一模块执行第一个 Patch 替换前，**必须先运行** `cp <脚本路径> <脚本路径>.bak` 创建备份。备份完成前，禁止调用任何文件修改工具。
6. **单次替换字数上限**：单个 `TargetContent` 不得超过 800 字。超过此长度的替换必须拆分为多个小补丁，并逐个展示给用户确认后再执行。
7. **禁止全量覆写**：严禁使用 `write_to_file Overwrite=true` 覆写已有逐字稿文件，必须使用 `replace_file_content` 或 `multi_replace_file_content` 做精确行级替换。
8. **禁止创建临时 Python 脚本操作逐字稿**（引用 `rule_security_governance.md` §6.1）：主控在修复过程中不得编写临时 Python 脚本来批量替换/删除逐字稿内容。所有修改必须通过 Agent 编辑工具逐步执行。
