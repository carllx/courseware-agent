# RFC: A/B Practice Exam Schema Integration

## 背景 (Context)

在《2025-2026-2 课程》项目中，针对实践类课程的期末考核，通常采用大作业（实操项目）而非传统的闭卷理论考试。为配合“教务材料”工作区中 Assessment Generator 的升级重构，生成能够防作弊、双轨并行（A/B 卷）的实操类试卷，我们需要在当前课程项目的 YAML 数据源中引入结构化的 `practice_*` 字段。

本 RFC 定义了相关的 Schema 设计与存放位置规范，指导如何将 A/B 卷元数据嵌入现有的单一事实来源（SSOT）架构。

---

## 1. 架构决策

### 1.1 数据位置：`course_assessment.yaml`
尽管这些考核在性质上类似于一个大型的综合实验，但就教务系统的流转而言，它们取代了原有的期末试卷。因此，核心数据必须落在 `course_assessment.yaml` 的 `exams -> final_exam` 层级下。

### 1.2 Schema 结构
为 `final_exam` 列表项新增 `type: practice_ab` 作为类型标识，并附加 `practice_paper` 结构以承载多套试卷版本的数据。

```yaml
exams:
  final_exam:
  - name: 期末综合项目考查
    total_score: 100
    duration: 120
    type: practice_ab        # 试卷类型：A/B版实操卷
    practice_paper:
      core_tech_points:
        - 第一条核心技术要求
        - 第二条核心技术要求
      submission_format: 作品源码及文档提交格式要求
      ab_versions:
        A:
          theme: A卷创作主题
          scenario_details: A卷详细的应用场景约束与发挥空间说明
        B:
          theme: B卷创作主题
          scenario_details: B卷详细的应用场景约束与发挥空间说明
    sections: ...            # 保持原有评分维度不变
```

### 1.3 共享全局默认配置
考场纪律、反作弊条款（`practice_others`）以及统一的作业提交路径（`practice_submission_path`）具有全校/全院通用性，为避免在每门课程的配置中冗余：
- 抽取至 `.agent/config/global_assessment.yaml`。
- 下游的生成引擎（如 DocxTpl 渲染引擎）在渲染时，应同时合并课程特定的 `practice_paper` 数据与全局的 `practice_exam_defaults` 数据。

---

## 2. 实施细节

### 2.1 全局配置示例
存放于 `[2025-2026-2 课程]/.agent/config/global_assessment.yaml`：
```yaml
practice_exam_defaults:
  practice_deadline: "{{截止时间}}"
  practice_submission_path: "超星学习通。逾期未提交且未提前申请缓考将视为学生旷考/缺考，请知悉。"
  practice_others: |
    （1）{{截止时间}}，逾期未提交未提前缓考申请的，将视为自主放弃本次考核资格，并按旷考、缺考记录。
    （2）旷考、缺考或违纪作弊、抄袭（作品中所使用的主素材必须是作者原创，个别素材使用公共素材的，必须注明出处，否则视为作弊、抄袭），该门课程按照总成绩不合格处理，不允许参加重考。
    （3）重考、缓考使用的是期末正考未启用过的试题，重缓考学生不得提交过往提交过的作品（含个人或他人/队员作品），否则将作抄袭、作弊处理，成绩为0。
```

### 2.2 影响评估 (Impact)
- `course_loader.py`: 现有的加载脚本具备兼容性，能原样提取新增的字典字段。
- **下游系统**：教务材料生成器需要在检测到 `type: practice_ab` 时，切换至实操试卷生成流（调用 DocxTpl 实操模板并传入 ab_versions 数据和 global_assessment.yaml）。

---

## 3. 验收标准
1. 已在 `交互产品开发` 与 `信息可视化` 课程的 `course_assessment.yaml` 中实装此结构。
2. 已建立 `.agent/config/global_assessment.yaml` 全局配置。
3. YAML 解析无错误，Schema 扩展完全向下兼容。
