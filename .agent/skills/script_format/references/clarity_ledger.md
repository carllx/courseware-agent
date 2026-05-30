# §3.4.3 正文段落级"秒懂"检测（写作时强制）

> **理论基础**：Pinker 知识诅咒 + Oppenheimer 加工流畅度——Agent（和专家教师）天然无法判断"什么对新手来说是难的"，因此必须通过外部结构化产出来暴露盲点。

在 `/write` Phase 2 的 Phase C 中，Agent 必须为每个模块输出 **Clarity Ledger**（清晰度台账）——将所有加粗锚词翻译为 DMA 学生秒懂的白话版本。

**Clarity Ledger 是模块 `done` 标记的前置条件**，与字数验证、视觉密度检查同等权重。

此外，`validate_script_length.py` 的 `detect_dilution()` 函数中新增了 `ABSTRACTION_MARKERS` 词表自动检测（v3），对"数据节点"、"算法吞吐"、"二元映射"等 DMA 学生无法具象化的技术隐喻进行物理拦截，输出 `[ABSTRACT]` 标签。

详见 `write_phase2_compose.md` Phase C 费曼画板探针部分。
