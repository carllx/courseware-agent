# 工作流速查手册

> 所有 `/` 命令的完整参数、示例调用与输出说明。

## 快速索引

| 我想做… | 用这个命令 |
|:---|:---|
| 创建一门新课程 | [`/new_course`](#new_course) |
| 写一份逐字稿 | [`/write`](#write) |
| 检查脚本是否合规 | [`/validate_script`](#validate_script) |
| 检查知识枢纽完整性 | [`/validate_knowledge`](#validate_knowledge) |
| 全面审查脚本质量 | [`/audit`](#audit) |
| 生成 PPT | [`/ppt`](#ppt) |
| 导出 TTS 文本或审阅 Word | [`/export`](#export) |
| 检查跨 Agent 邮箱待办消息 | [`/mailbox_in`](#mailbox_in) |

---

## `/new_course`

> 创建新课程的标准目录结构和配置文件。

**参数**: 课程的中文名称

**示例**:
```
/new_course 数字音频编辑
```

**执行内容**:
1. 创建标准目录结构（knowledge/scripts/visuals/delivery）
2. 从模板复制 `course.yaml`
3. 创建骨架文件（结构图、术语表、实验规划等）
4. 注册到 `manifest.json` 和 `INDEX.md`

**输出**: `<课程名>/` 目录及全部骨架文件

---

## `/write`

> 为指定课程的教学单元撰写逐字稿。

**参数**: 课程名 + 教学单元 ID

**示例**:
```
/write 实习指导 S01
/write 交互产品开发 W03
```

**执行内容**:
1. 读取 `course.yaml` 获取知识库入口和教师风格
2. 加载结构图、知识库、叙事规范
3. **深度调研** — 激活 `narrative_archaeologist` 技能，对核心知识点执行多轮网络搜索（广搜→深挖→锚点回归），产出调研备忘录
4. 遵循 `script_format` 规范，基于调研成果进行写作
5. **预算注入** — 在生成脚本时，按模块自动注入由 `inject_budget.py` 计算的字数边界注释（`<!-- BUDGET: ... -->`）
6. Visual-First 双轨结构，Slide 定义内联到 `> [VISUAL]` 块
7. 自检：运行时长估算 + 知识面覆盖率检查

**输出**: `<课程>/scripts/<单元ID>_<名称>.md`

**关键约束**:
- 必须遵循 `rule_narrative_standards.md` 叙事规范
- 至少使用 1 个人文层知识标签，内容**必须基于深度调研成果**
- 每 3 分钟设计一个留白

---

## `/validate_script`

> 审查脚本的规范合规性。

**参数**: 课程名（可选：指定单个脚本）

**示例**:
```
/validate_script 实习指导
/validate_script 实习指导 S01_Mobilization.md
```

**执行内容**:
1. **规范合规性** — 标签白名单、VISUAL/ACTIVITY 块字段完整性、Layout 类型、Slide ID 唯一性、旧格式检测
2. **视觉素材** — 交叉比对脚本引用与 `visuals/assets/` 物理文件
3. **时长估算** — 中文字数、英文词数、预估总时长
4. **叙事抽查** — Agent 人工判断过渡、反翻译腔、朗读节奏

**输出**: 终端打印审查报告 + 结论（Pass / Needs Revision）

**底层脚本**:
```bash
python .agent/skills/validation_suite/scripts/validate_spec.py --course "课程名"
python .agent/skills/validation_suite/scripts/validate_visuals.py --course "课程名"
python .agent/skills/validation_suite/scripts/validate_script_length.py --course "课程名"
```

---

## `/validate_knowledge`

> 审查课程 `knowledge/` 目录的完整性、性能约束及 hub 条目一致性。

**参数**: 课程名（可选：`--strict` 开启严格性能约束）

**示例**:
```
/validate_knowledge 交互产品开发
/validate_knowledge 交互产品开发 --strict
```

**执行内容**:
1. **C1**: `knowledge_hub.yaml` 存在且格式合法
2. **C2**: hub 行数 < 200 行（建议 < 150），保障 Agent 上下文性能
3. **C3**: 所有 `textbook`/`note` 条目的 `source` 文件实际存在
4. **C4**: `notes/` 目录下无孤立文件（每个 file 必须在 hub 有对应条目）

**输出**: 终端打印健康检查报告（✅ / ❌）

**底层脚本**:
```bash
python .agent/skills/validation_suite/scripts/validate_knowledge.py --course "课程名"
```

---

## `/audit`

> 全面质量审查（逻辑 + 教学 + 语言）。

**参数**: 课程名 + 脚本文件

**示例**:
```
/audit 实习指导 S01_Mobilization
```

**执行内容**:
1. 运行 `validate_project.py` 自动化预检
2. 叙事完整性审查（视觉同步、指示代词、逻辑断层）
3. 教学质量审查（费曼检查、颗粒化复述、脆弱性提问）
4. 语言合规审查（本地化分级、Chinglish、标点间距）
5. **深度知识面审查**（仅在 `--deep` 模式懒加载启用，检查标签多样性、测试点绑定等）

> 注：`/audit` 提供三级拆分。默认模式为 Standard（节省 50% Token），若需触发深度排查（Part D+G），需附带 `--deep` 以分离加载 `audit_deep.md` 和 `audit_courseyaml.md`。

**输出**: 审计报告（Pass / Fail / Needs Revision）

**底层脚本**:
```bash
python .agent/skills/validation_suite/scripts/validate_project.py --course "课程名"
```

---

## `/ppt`

> 从逐字稿自动生成课程 PPT。

**参数**: 课程名 + 脚本文件名

**示例**:
```
/ppt 实习指导 S01_Mobilization
```

**执行内容**:
1. 预检 — 提取脚本中所有 `> [VISUAL]` 块，验证字段完整性
2. 资产检查 — 确认 `Asset` 引用的物理文件就绪
3. 生成 — 按 Layout → PPT 版式映射表生成 Slide
4. QA — 转 PDF 截图检查质量

**输出**: `<课程>/delivery/<脚本名>_Presentation.pptx`

---

## `/export`

> 导出 TTS 文本、审阅 Word 文档或词汇表。

**参数**: 课程名 + 导出模式

**三种模式**:

### 模式 A: TTS 纯文本
```
/export 实习指导 --tts
```
导出两种 TTS 文本至 `<课程>/scripts/tts/`：
- **标准模式** (`<脚本名>.txt`)：含 `[SLIDE #N]` 标记，供录音员参考或审计溯源
- **盲读模式** (`<脚本名>_blind.txt`)：纯朗读文本，直接喂 TTS 引擎

### 模式 B: 审阅文档
```
/export 实习指导 --review
```
带视觉标记的 `.docx`（红=VISUAL，蓝=ACTIVITY，灰=知识标签），输出至 `<课程>/delivery/review/`。

### 模式 C: 词汇表
```
/export 实习指导 --vocab
```
按章节提取英文术语表，输出 `<课程>/scripts/tts/Vocabulary_List.md`。

**底层脚本**:
```bash
# TTS 标准模式
python .agent/skills/validation_suite/scripts/validate_script_length.py --course "课程名" --dump-text
# TTS 盲读模式
python .agent/skills/validation_suite/scripts/validate_script_length.py --course "课程名" --dump-text --blind-mode
# 审阅
python .agent/skills/validation_suite/scripts/export_review_docx.py --course "课程名" --all
# 词汇
python .agent/skills/validation_suite/scripts/validate_script_length.py --course "课程名" --dump-vocab
```

---

## `/mailbox_in`

> 检查跨 Agent 共享邮箱中发往课程工作区的待处理消息。

**参数**: 无

**示例**:
```
/mailbox_in
```

**执行内容**:
1. 同步 INDEX — 扫描 `active/`、`rfc/`、`resolved/` 重建本端视图
2. 过滤 `to: 课程工作区` 且 `status ≠ resolved` 的消息
3. 按优先级（P0 > P1 > P2）和创建时间排序
4. 展示待办清单，提示用户选择处理哪条消息
5. 处理完成后归档消息到 `resolved/` 并更新 INDEX

**输出**: 终端展示待办消息清单

**邮箱路径**: `/Users/yamlam/Downloads/cross_agent_mailbox/`

**相关规则**: `.agent/rules/rule_cross_agent_protocol.md`
