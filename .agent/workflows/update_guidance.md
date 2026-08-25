---
description: 修改指导文档/规范/配置后，审计下游影响并同步更新全链路
---

# /update_guidance 工作流

> **输入**: 变更描述 + 被修改的文件路径
> **输出**: 影响分析报告 + 下游文件同步更新

## Step 0: 跨项目边界预检 (ADR 015 Guard)

在开始分析前，先判断被修改的文件是否属于**当前项目（课程工作区）**：

| 文件位置 | 处理方式 |
|:---|:---|
| 课程工作区内（`.agent/`、`<课程>/course.yaml` 等） | 直接执行本工作流 |
| 教务材料项目（`/Users/yamlam/Downloads/教务材料/`） | ⚠️ 违反 ADR 015。应改用**委托消息**（见 Step 5），由用户转达给教务端 Agent |
| 两端同时涉及 | 分离处理：课程端部分在本工作流执行，教务端部分草拟委托消息 |

> [!WARNING]
> **不要因为「顺手」而直接修改教务端文件。** 即使改动很小（如 Spec 类型声明同步），也应走委托模式。唯一例外：用户明确授权的紧急修复，事后必须在 ADR 中标注违规记录。

## Step 1: 识别变更类型

根据被修改的文件，自动判断变更类型并进入对应的检查路径：

| 变更类型 | 触发条件（修改了什么） | 检查路径 |
|:---|:---|:---|
| **A: course.yaml 结构变更** | `course.yaml` 的 `objectives`/`calendar`/`experiments`/`assessment_methods` | → §A |
| **B: 脚本格式规范变更** | `script_format/SKILL.md`、`rule_narrative_standards.md`、标签白名单 | → §B |
| **C: ADR / 全局规则变更** | `.agent/rules/rule_*.md`、`ADR.md` | → §C |
| **D: 验证器/生成器代码变更** | `scripts/validation/*.py`、`engines/*.js`、`engines/*.py`、`engines/h5_template/` | → §D |
| **E: 通用文档修改** | `README.md`、`INDEX.md`、`docs/`、skill 文档 | → §E |
| **F: 跨项目 Schema/Spec 同步** | `course_schema.py`、`Spec_*.md`、`Data_Dictionary.md` 等教务端源文件 | → §F |

> 若变更跨多个类型，按优先级 A > B > C > D > F > E 依次执行。

## Step 2: 按类型执行检查

### §A: `course.yaml` 结构变更

| # | 变更子项 | 下游影响检查 |
|---|---------|-------------|
| A1 | `objectives` 修改（desc / mappings） | ① `calendar[].supported_objectives` 引用是否仍有效 ② 脚本 frontmatter `objectives` 是否需同步 ③ `rule_training_plan_compliance.md` 观测点是否匹配 |
| A2 | `calendar[]` 结构（lessons / steps / ideology / task） | ① 对应脚本 Module 结构是否覆盖 ② frontmatter 与 `lessons.objectives` 是否一致 ③ 生成器输出（教案/进度表）是否需要重新生成 |
| A3 | `experiments[]` 修改 | ① `type` 枚举合法性（ADR 011） ② 实验报告模板是否需更新 ③ `assessment_methods` 引用是否一致 |
| A4 | `assessment_methods` 修改 | ① 大纲生成器评分表是否需重新生成 ② `final_item` 必填性检查（ADR 011） |
| A5 | `classes[]` 修改（多班配置） | ① `week_range`/`excluded_weeks` 合规性（ADR 012） ② 进度表按班各出一份 |
| A6 | `calendar[].hours_*` 数值修改 | ① 学时总和一致性（见下方自检） ② 单周物理容量红线 ③ 路演/答辩周 `hours_theory==0` ④ 已生成的进度表/教案/大纲是否需重跑 |

**A6 学时一致性自检**（每次 hours 变更后必跑）：
```bash
# 逐课程验证 calendar 学时总和 vs 声明值
/opt/anaconda3/envs/mybase/bin/python -c "
import yaml, pathlib
for p in pathlib.Path('.').glob('*/course.yaml'):
    d = yaml.safe_load(p.read_text())
    if 'calendar' not in d: continue
    cal = d['calendar']
    ht = sum(w.get('hours_theory',0) or 0 for w in cal)
    hp = sum(w.get('hours_practice',0) or 0 for w in cal)
    dt, dp = d['course']['hours']['theory'], d['course']['hours']['practice']
    ok = '✅' if ht==dt and hp==dp else '❌'
    print(f'{ok} {p.parent.name}: calendar({ht}+{hp}) vs declared({dt}+{dp})')
    # 逐周物理容量
    for w in cal:
        wk = w.get('week','?')
        t, pr = w.get('hours_theory',0) or 0, w.get('hours_practice',0) or 0
        if t+pr > 5: print(f'  ⚠️ W{wk}: {t}+{pr}={t+pr} 超 5 节红线')
"
```

**执行方法**：
```bash
# 跨课程全量 Schema 校验
/opt/anaconda3/envs/mybase/bin/python \
  "/Users/yamlam/Downloads/教务材料/scripts/audit_course_data.py" --root .
```

### §B: 脚本格式规范变更

| # | 变更子项 | 下游影响检查 |
|---|---------|-------------|
| B1 | `[VISUAL]` 块字段变更 | ① `validate_spec.py` 解析器是否适配 ② `ppt_parser.js` 是否适配 ③ `generate_course_h5.py` H5 解析器是否适配 ④ `/generate_assets` 工作流引用的字段名是否一致 |
| B1a | `dumptext.py` BEGIN/END 标记格式变更 | ① `generate_course_h5.py` 的 `_build_source_map()` 源映射正则是否适配（ADR 036） |
| B2 | Layout 枚举变更 | ① `validate_spec.py` 白名单 ② `ppt_layouts.js` 渲染器 ③ `h5_template/src/components/SlideFactory.jsx` H5 布局映射 ④ `visual_system.yaml` 的 `prompt_variants` |
| B3 | 知识标签变更 | ① `validate_spec.py` 标签白名单 ② `/audit` Part D 检查规则 |
| B4 | 叙事规范变更 | ① `/audit` Part B/C 检查标准 ② `/write` Step 3 写作规则 |

**执行方法**：
```bash
grep_search "<变更关键词>" --path .agent/ --includes "*.md,*.py,*.js"
```

### §C: ADR / 全局规则变更

1. **查阅依赖图**：先读取 `.agent/DEPENDENCY_MAP.md` 定位被修改规则的所有下游引用方
2. **精确搜索**：对依赖图未覆盖的情况，用 `grep_search` 搜索 ADR 编号或规则文件名补充
3. **分类影响**：
   - `workflows/*.md` → 更新工作流步骤描述
   - `rules/rule_*.md` → 检查规则间是否冲突
   - `skills/*/SKILL.md` → 更新技能文档
   - `scripts/validation/*.py` → 更新校验逻辑
3. **一致性验证**：确保新 ADR 的约束在所有引用处被正确反映

### §D: 验证器/生成器代码变更

| # | 检查项 |
|---|-------|
| D1 | 对应的 `Spec` 或工作流描述是否需更新（如 `/ppt`、`/h5`、`/export`） |
| D2 | 其他验证器是否调用了被修改的函数（`validate_project.py` 统一入口） |
| D3 | 命令行参数变更时，所有工作流中的示例命令是否同步更新 |
| D4 | `[VISUAL]` 块字段变更时，PPT 解析器 (`ppt_parser.js`) 和 H5 解析器 (`generate_course_h5.py`) 是否均已适配 |
| D5 | `vite-plugin-h5-hot-reload.js` 变更时：① `shouldHandle()` 正则是否匹配当前目录结构 ② Python spawn 的 CLI 参数是否与 `generate_course_h5.py` 的 `main()` 路由一致 ③ WebSocket 事件名 (`h5:reload`/`h5:error`) 是否与 `LessonViewer.jsx`/`App.jsx` 的监听器匹配（ADR 037） ④ TTS 中间件（save/manifest/audio proxy）是否在 engines/ 和 build/ 两个副本间保持同步（ADR 040） |

### §E: 通用文档修改

1. **语义变更判断**：纯 typo → 跳过影响分析；术语/规则变更 → 继续
2. **搜索旧术语**：`grep_search` 定位所有使用旧术语的文件
3. **分组处理**：`Must Update` / `Should Review` / `Safe to Ignore`
4. **批量替换**：高置信匹配直接更新，模糊匹配列出供用户确认

### §F: 跨项目 Schema/Spec 变更

当修改涉及教务端的 SSOT 文件时，需额外检查课程端与教务端的**双向一致性**：

| # | 检查项 |
|---|-------|
| F1 | `course_schema.py` 字段类型变更 → 对照 `Data_Dictionary.md`、各 `Spec_*.md` 中的类型声明 |
| F2 | `Spec_*.md` 数据源列变更 → 对照 `course.yaml` 实际字段名 |
| F3 | 新增/删除 Schema 字段 → 检查 ADR 008 类型约束表、`new_course.md` 模板占位 |
| F4 | **跨课程通用性检查**：变更是否对工作区内**所有课程**均适用（ADR 009 §3 跨课程一致性原则） |

> **委托消息模板**（当需要教务端修改时）：
> ```
> 发件方：课程工作区 Agent
> 收件方：教务材料 Agent
> 背景：[变更原因]
> 具体任务：[文件路径 + 修改内容]
> 验证条件：[预期审计结果]
> ```

### §G: Practice 层变更传播

> 借鉴 DAG 图传播：当上游节点 (course.yaml) 变更时，自动检查下游节点 (practice YAML) 的一致性。

| # | 变更子项 | 下游影响检查 |
|---|---------|-------------|
| G1 | `hours_practice` 变更 | ① 对应 `W0X_practice.yaml.total_minutes` 是否同步更新 ② Practice Guide 学时显示是否一致 |
| G2 | `teaching_requirements` 变更 | ① 对应 `W0X_practice.yaml.theory_prerequisites` 是否需要同步 |
| G3 | `supported_objectives` 变更 | ① 对应 `phases[].theory_link.course_objective` 是否仍指向有效目标 |
| G4 | `concept_registry.yaml` 变更（ID 重命名/删除） | ① grep 所有 `practices/*.yaml` 和 `weeks/*/practice.yaml` 中的 `concept_id` 引用 ② 标记断链 |
| G5 | `experiments[]` 变更 | ① `experiment_link`（`list[int]`）绑定 ID 是否仍有效 ② Practice Guide 中的实验引用是否需更新 |
| G6 | `extract_week.py` 模板变更 | ① `.agent/templates/extract_week.py` (SSOT) 修改后，须同步到所有课程目录的副本 ② diff 确认各副本一致 |
| G7 | `practice_schema.md` 版本升级 | ① 各课程 `practices/_schema.md` 的版本引用须同步更新 ② 运行 `validate_practice.py --all` 确认无回归 |

**执行方法**：
```bash
# 自动化校验（推荐，替代手动 grep）
/opt/anaconda3/envs/mybase/bin/python \
  .agent/scripts/validation/validate_practice.py --all

# G6: extract_week.py 跨课程同步检查
diff .agent/templates/extract_week.py 交互产品开发/extract_week.py
diff .agent/templates/extract_week.py 信息可视化/extract_week.py
```

## Step 3: 执行更新

- [ ] **更新下游文件**：按 Step 2 的检查结果逐一修改
- [ ] **跨课程同步**：对工作区内所有课程（非仅当前课程）验证一致性
- [ ] **交叉验证**：修改后运行审计脚本确认无回归
- [ ] **更新 INDEX.md**：若文件结构发生变化

## Step 4: 知识固化

- [ ] **架构决策 → ADR**：若本次变更涉及架构性选择（如类型升级、字段语义变更），必须追加 ADR 条目到 `ADR.md`
- [ ] **用户偏好 → ADR / Rules**：若用户在审批过程中表达了设计偏好（如「保持整数」「不要个位数计算」），应将其抽象为通用约束记入 ADR 或对应 rule 文件
- [ ] **规则漏洞 → 工作流自身**：若执行本工作流时发现其步骤覆盖不到的盲区，**立即更新本工作流**（自举修复）
- [ ] **新课程兼容 → `/new_course` 模板**：若引入新 ADR 约束或字段约定，确认 `/new_course` 模板中有对应占位

## Step 5: 跨项目委托（若涉及教务端）

当 Step 0 判定涉及教务端修改时，草拟委托消息并交由用户转达：

```markdown
# 委托消息：[标题]

> **发件方**：课程工作区 Agent（`/Users/yamlam/Downloads/2025-2026-2 课程/`）
> **收件方**：教务材料 Agent（`/Users/yamlam/Downloads/教务材料/`）
> **优先级**：[高/中/低]

## 背景
[简述变更原因和上下文]

## 具体任务
[列出需要教务端修改的文件和内容]

## 验证条件
[描述修改完成后的预期审计结果]
```
