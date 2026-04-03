# Known Issues — 课程数据层漏洞备忘录

> [!NOTE]
> **文件职责**：记录所有经人工审查或 Agent 审计发现的、属于 `2025-2026-2 课程/` 目录层的数据漏洞。  
> **受众**：课程 Agent（Antigravity 实例）与教师（林昕）。  
> **变更规则**：每条 Issue 修复后必须标注 `状态: ✅ 已修复 (日期)` 并注明 commit/修改摘要，**不得删除记录**。

---

## 格式说明

```
### ISSUE-NNN: 标题
- 发现时间: YYYY-MM-DD
- 状态: 🔴 待修复 | 🟡 待讨论 | ✅ 已修复
- 级别: 高危 / 中危 / 低危
- 影响范围: 受影响的文件和生成流程
- 问题描述: ...
- 复现路径: ...
- 修复方案: ...
```

---

## 信息可视化 (`信息可视化/course.yaml`)

### ISSUE-001: 游戏班 W10-W18 的 `calendar` 条目完全缺失

- **发现时间**: 2026-02-24
- **状态**: ✅ 已修复 (2026-02-24)
- **修复摘要**: 采用「差异声明层」方案（方案 B）——课程侧在 `classes[游戏班]` 新增 `excluded_weeks: [16]` 和 `session_time_overrides`，calendar[] 保持 W1-W8 不变；教务侧升级生成器实现偏移映射、跳过停课周和时长裁剪。
- **影响范围**: `信息可视化/course.yaml` → `calendar` 节；`gen_lessonplan_xml.py`（游戏班教案无法生成）；`gen_schedule_xml.py`（进度表周次不完整）
- **问题描述**:  
  `calendar` 仅有 W1–W8 共 8 个条目，匹配**影视班**上课周次（第 1-8 周）。  
  然而 `classes` 中**游戏班**定义了两段排课：
  - 10-13 周：`1-5节`（4 周）  
  - 14-18 周：`2-5节`（5 周，节次不同）  

  合计**游戏班需要 W10–W18 共 9 周的教学进度**，YAML 中完全空白。

- **复现路径**:  
  执行 `generate.py` 时指定游戏班，教案生成器因 `calendar` 缺项而跳过或报错。

- **修复方案**:  
  在 `calendar` 末尾追加 W10–W18 条目（共 9 条）。由于两个班教学内容基本相同，W10-W18 可复用 W1-W8 内的相应周次结构并调整周次编号，同时注意：
  - W14-W18 的游戏班节次为 `2-5节`（少 1-5 节中第 1 节课），需在对应 lessons 的总分钟数中扣除约 45 min，或在 `teaching_method` / `steps` 中注明内容删减策略。
  - `hours_theory` 与 `hours_practice` 需匹配实际该段周次的可用时间。

---

### ISSUE-002: `hours.total` 未区分双班学时，产生歧义

- **发现时间**: 2026-02-24
- **状态**: 🟡 待讨论
- **级别**: 高危
- **影响范围**: `信息可视化/course.yaml` → `hours`；大纲/进度表学时统计页
- **问题描述**:  
  `hours: {total: 40, theory: 20, practice: 20}` 表示**一个班级**的完整学时。  
  然而本课程同时开设两个班：
  - 影视班：W1-W8，约 40 学时
  - 游戏班：W10-W18，亦约 40 学时（其中 W14-W18 节次为 2-5 节，实际少 5 节课 = -5×45min）

  当前 `hours.total: 40` 的语义不清晰——它既可能表示"任意一个班"，也可能被生成器误读为"课程总学时 = 40（而非 80）"。

- **修复方案（待教师确认）**:  
  方案 A：在 `hours` 下增加 `per_class: true` 标注，明确 40 为单班学时。  
  方案 B：在 `classes` 条目中各自补充 `hours_override: {total, theory, practice}`，覆盖顶层 `hours`。  
  方案 C：保持现状，在 `CONTRIBUTING.md` 或 Schema 文档中注释「多班课程 `hours` 表示单班学时」惯例，并在 `/audit` 中增加检查。

  > [!IMPORTANT]
  > 本 Issue 的修复方向需教师和教务材料 Agent 双向确认，再统一规范。修复前生成器维持现有行为（使用顶层 `hours` 值）。

---

## 交互产品开发 (`交互产品开发/course.yaml`)

### ISSUE-003: `classes[0]` 缺失 `week_range` 字段

- **发现时间**: 2026-02-24
- **状态**: ✅ 已修复 (2026-02-24)
- **修复摘要**: 在 `交互产品开发/course.yaml` `classes[0]` 末尾追加 `week_range: "1-15"`，依据课表截图第1-15周。
- **级别**: 高危
- **影响范围**: `交互产品开发/course.yaml` → `course.classes[0]`；`gen_schedule_xml.py`（课表缺周次范围）；`gen_lessonplan_xml.py`（教案封面上课周次为空）
- **问题描述**:  
  `信息可视化` 的每个 `classes` 条目均含 `week_range` 字段，而 `交互产品开发` 的 `classes` 仅有：
  ```yaml
  - name: 2023级数字媒体艺术影视班
    schedule_time: 周三2-5节
    classroom: 温泉校区 2实107
    # ← week_range 缺失
  ```
  生成进度表/教案封面时「上课周次」字段将为空或报错。  
  对照课表截图，实际上课周次为 **1-15 周**。

- **修复方案**:  
  在 `classes[0]` 末尾追加一行：
  ```yaml
      week_range: 1-15
  ```

---

### ISSUE-004: W15（路演周）`hours_theory: 2` 与 `steps` 内容矛盾

- **发现时间**: 2026-02-24
- **状态**: 🟡 待讨论
- **级别**: 中危
- **影响范围**: `交互产品开发/course.yaml` → `calendar[week=15]`；理论学时统计
- **问题描述**:  
  W15 定义 `hours_theory: 2`，但 `lessons[0].steps` 中没有 `讲授` 阶段（仅有 `导入 10min`、`实践 150min`、`小结 20min`，总计 180min），也缺少 `复习` 阶段。  
  若 `gen_schedule_xml.py` 汇总各周 `hours_theory` 之和来填写"理论总学时"，W15 的 2h 理论学时将在课时汇总表中体现，却无对应实体内容支撑。

- **修复方案（二选一，待教师确认）**:  
  - 方案 A：将 W15 的 `hours_theory` 改为 `0`，`hours_practice` 改为 `4`（全天路演为实践课时）。
  - 方案 B：保留 `hours_theory: 2`，在 `steps` 中补充一个 `讲授` 阶段（如「教师综合点评与学期总结」，约 20min），并从 `实践` 中减去相应时间。

---

## 两门课程共有问题

### ISSUE-005: `supported_objectives` 覆盖不全，存在孤立目标

- **发现时间**: 2026-02-24
- **状态**: 🟡 待讨论
- **级别**: 中危
- **影响范围**: 两门课程 `course.yaml` → `calendar[].supported_objectives`；ADR 010（`supported_objectives` 引用完整性校验）
- **问题描述**:  
  按 ADR 010 §4，所有已定义的目标编号至少须被一个 `CalendarWeek` 的 `supported_objectives` 引用。  
  当前违规情况如下：

  **信息可视化**（3×3 = 9 个目标）：
  | 目标 | 当前覆盖 | 问题 |
  |:-----|:--------|:-----|
  | 能力2（嵌套模型/全流程规划） | W7 ✅ | — |
  | 能力3（矢量精修/数据艺术） | W2 ✅ | — |
  | 知识2（Tidy Data建模） | W3 `知识1` ← 应为 `知识2` | ⚠️ **W3 引用了 `知识1`，但 W3 教学内容对应的是 `知识2`（Tidy Data）** |
  | 素质3（数据艺术/社会责任） | 无 | 🔴 **无任何周次引用** |

  **交互产品开发**（3×3 = 9 个目标）：
  | 目标 | 当前覆盖 | 问题 |
  |:-----|:--------|:-----|
  | 能力2（容器化/Design Token） | W6, W7, W8 各有 `能力1` ← 应含 `能力2` | ⚠️ **W6-W8 大量使用 Token/AutoLayout，应支撑 `能力2`** |
  | 素质2（AI 韧性/以人为本） | W9, W10, W11 各仅 `知识1` 或 `能力1` | ⚠️ **AI 工具排障周（W9-W11）最应支撑 `素质2`** |
  | 素质3（建设性批评与协作） | W12-W15 有部分 ✅ | 基本合理 |

- **修复方案**:  
  逐周核对 `lessons.objectives` 内容与 `supported_objectives` 的对应关系，补全遗漏引用。  
  可通过以下审计命令触发自动检查（待实现）：`/audit` → Part F → F11 `supported_objectives 引用完整性`。

---

### ISSUE-006: `semester_config.start_date` 为学期开始周一，生成器须正确推算上课日

- **发现时间**: 2026-02-24
- **状态**: 🟡 低优先级
- **级别**: 低危
- **影响范围**: 两门课程 `semester_config.start_date: "2026-03-02"`；任何依赖日期推算的生成脚本
- **问题描述**:  
  `2026-03-02` 为周一（学期第 1 自然周起始日），而两门课程实际上课日分别为：
  - 信息可视化：**周五**（2026-03-06 = 开学第 1 个周五）
  - 交互产品开发：**周三**（2026-03-04 = 开学第 1 个周三）

  若生成脚本以 `start_date + (week-1)*7` 作为第 `week` 周上课日，将输出 `03-02`（周一），而非正确日期。

- **修复方案**:  
  生成器（`gen_lessonplan_xml.py` / `gen_schedule_xml.py`）在推算教案日期时，需读取 `classes[n].schedule_time` 中的「周X」信息，将 `start_date` 偏移至该周对应的上课星期数再加 `(week-1)*7`。  
  **`start_date` 本身不需要改动**，这是学期基准日期的正确设定，问题在消费端。

---

### ISSUE-007: 端午节停课导致游戏班学时与 `hours.total` 存在隐性偏差

- **发现时间**: 2026-02-24
- **状态**: ✅ 已决策 (2026-02-24)
- **级别**: 中危
- **影响范围**: `信息可视化/course.yaml` → `classes[游戏班]`；`gen_schedule_xml.py` 学时校验；`gen_lessonplan_xml.py` 教案数量
- **问题描述**:  
  W16（2026-06-19）为**端午节**，游戏班（周五上课）当周停课，实际有效教学周由 9 周压缩至 8 周。

- **最终决策：假期吸收策略**:  
  1. **教案层**：一门课一份教案（8周统一备课），不因班别分叉
  2. **进度表层**：以班为单位输出，W16 跳过日期行，但 **不从官方总周数中扣减**
  3. **节次出入**：忽略（W14-W18 节次差异不影响教案内容），已移除 `session_time_overrides`
  4. **官方文档参数**：按教务注册值填写 → `official_weeks: 9`（游戏班）/ `official_weeks: 8`（影视班）
  5. `excluded_weeks: [16]` 保留，供进度表生成器跳过该日期行
  6. `hours.total: 40, per_class: true` 不变

### ISSUE-008: `gen_lessonplan_xml.py` 中 `excluded_weeks` 跳过逻辑 `continue` 作用域错误

- **发现时间**: 2026-02-24
- **状态**: ✅ 已修复 (2026-02-24)
- **修复摘要**: 将内层 `for cls` 的 `continue` 改为标志变量 `_skip_excluded` + `break`，在外层 `for week` 循环中 `if _skip_excluded: continue`，确保正确跳过整周教案生成。
- **级别**: 高危（隐性漏洞）
- **影响范围**: `教务材料/scripts/gen_lessonplan_xml.py` L1064-1069；含 `excluded_weeks` 声明的课程（当前仅信息可视化游戏班 W16）
- **问题描述**:  
  `excluded_weeks` 跳过逻辑中，`continue` 语句位于内层 `for cls in classes` 循环内，仅跳过当前 `cls` 迭代而非外层 `for week` 循环。当 `calendar[]` 包含 excluded 周次时，会意外为该周生成教案。  
  当前因 ISSUE-007 决策（calendar 仅含 W1-W8，不含 W16），此 Bug **未触发**，但属隐性逻辑漏洞。
- **修复方案**:  
  ```diff
  -for cls in context.get('course', {}).get('classes', []):
  -    exc = cls.get('excluded_weeks', [])
  -    if str(week_num).isdigit() and int(week_num) in [int(e) for e in exc]:
  -        print(f"    ⏭️  W{week_num} 在 excluded_weeks 中，跳过教案生成")
  -        continue
  +_skip_excluded = False
  +for cls in context.get('course', {}).get('classes', []):
  +    exc = cls.get('excluded_weeks', [])
  +    if str(week_num).isdigit() and int(week_num) in [int(e) for e in exc]:
  +        print(f"    ⏭️  W{week_num} 在 excluded_weeks 中，跳过教案生成")
  +        _skip_excluded = True
  +        break
  +if _skip_excluded:
  +    continue
  ```

---

## 修复进度追踪

| Issue | 描述 | 课程 | 级别 | 状态 |
|:------|:-----|:-----|:-----|:-----|
| ISSUE-001 | 游戏班 W10-W18 calendar 空缺 | 信息可视化 | 🔴 高危 | ✅ 已修复 (2026-02-24，差异声明层方案) |
| ISSUE-002 | `hours.total` 双班学时歧义 | 信息可视化 | 🔴 高危 | ✅ 已修复 (2026-02-24, 方案A `per_class:true`) |
| ISSUE-003 | `classes[0]` 缺 `week_range` | 交互产品开发 | 🔴 高危 | ✅ 已修复 2026-02-24 |
| ISSUE-004 | W15 理论学时 vs steps 矛盾 | 交互产品开发 | 🟡 中危 | ✅ 已修复 (2026-02-24, 方案A hours_theory:0) |
| ISSUE-005 | `supported_objectives` 覆盖不全 | 两门课程 | 🟡 中危 | ✅ 已修复 (2026-02-24, W3知识2/W5素质3/W6-8能力2/W9-11素质2) |
| ISSUE-006 | `start_date` 日期推算偏移 | 两门课程 | 🟠 低危 | 🟡 低优先级 |
| ISSUE-007 | 端午节停课游戏班学时偏差 | 信息可视化 | 🟡 中危 | ✅ 已决策（假期吸收策略） |
| ISSUE-008 | `excluded_weeks` continue 作用域错误 | 教务材料 | 🔴 高危 | ✅ 已修复 (2026-02-24) |
| ISSUE-009 | 进度表偏移映射不跳过停课周 | 教务材料 | 🔴 高危 | ✅ 已修复 (2026-02-24) |

---

*最后更新: 2026-02-24 by Antigravity（ISSUE-009 追加 + ADR 013 固化 — 会话 4917bdeb）*
