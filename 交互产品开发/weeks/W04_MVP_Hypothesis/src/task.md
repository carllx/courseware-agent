# W04_MVP_Hypothesis 叙事素材深度调研与拓展待办清单

> **状态说明**：
> - [ ] 未开始 (Pending)
> - [~] 调研中 (Researching/Waiting for Approval)
> - [x] 已完成 (Completed & Verified)

## 模块列表
- [x] M00_课程导览.md
- [x] M01_杀死重型_Persona.md
- [x] M02_从假设到子弹_假设驱动设计.md
- [x] M03_假设优先级_风险_×_价值矩阵.md
- [x] M04_MVP_最小可行「学习工具」.md
- [x] M05_实验1_收官_调研汇报与可行性清单.md

## 执行协议纪律
1. **单步阻断与审批**：逐个模块执行，先输出诊断报告/修复计划，等待审批后修改。
2. **显式修改痕迹**：仅使用原生文件编辑 API (`multi_replace_file_content` / `replace_file_content`)。
3. **残留物管控**：临时脚本写入 `scratch/` 或 artifact 目录，不污染 `src/`。
4. **精简性约束**：3句话法则，遵守字数上限。新素材必须强关联核心概念。
5. **验证**：修改后使用 `validate_spec.py` 验证。
