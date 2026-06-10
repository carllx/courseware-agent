# 规则模板库

按触发模式分类的可复用模板。复制即用，按需修改。

---

## 模板 A：始终激活 (always)

适用于**安全红线、全局协议**等不可协商的约束。

```markdown
---
trigger: always
description: <一句话说明这条规则持续约束什么行为>
---

# 规则：<中文名> (<English Name>)

## 核心原则
- **原则 1**: ...
- **原则 2**: ...

## 强制约束
1. ...
2. ...

## 禁止行为
- ❌ ...
- ❌ ...
```

> 现有示例：`rule_security_governance.md`（安全治理红线）、`rule_meta_learning.md`（元学习协议）

---

## 模板 B：模型判定 (model_decision)

适用于**特定操作的前置检查**（Agent 自主判断是否相关）。

```markdown
---
trigger: model_decision
description: 当<触发条件>时，必须<核心行为>。
---

# 规则：<中文名> (<English Name>)

**生效范围**: 当 Agent 需要<具体操作>时。

## 强制前置步骤 (Pre-flight)
在<操作>**之前**，Agent 必须：
1. ...
2. ...

## 执行协议
...

## 禁止行为
1. ❌ ...
2. ❌ ...
```

> 现有示例：`rule_visual_generation.md`（视觉资产生成协议）、`rule_training_plan_compliance.md`（人培合规性约束）

---

## 模板 C：Glob 匹配 (glob)

适用于**特定文件类型的编写/审查规范**。

```markdown
---
trigger: glob
description: <一句话说明对什么文件执行什么约束>。
globs:
  # ⚠️ 优先用 **/ 替代 */，防止目录层级变更后静默失效
  - ["**/weeks/*/src/*.md", "**/weeks/*/package.yaml"]
---

# 规则：<中文名> (<English Name>)

## TL;DR (预检阶段专用)
<2-3 行核心要点速记，供 Agent 快速预检>

> **适用范围**: ...
> **SSOT**：本文件为 <X> 的唯一定义点。

---

## §1 <分节标题>
...

## §2 <分节标题>
...

## 禁止行为
- ❌ ...
```

> 现有示例：`rule_narrative_standards.md`（叙事规范）、`rule_content_depth.md`（内容深度与字数防卫）、`rule_localization.md`（本地化规范）

---

## 模板 D：手动引用 (manual)

适用于**低频参考文档**，仅当用户 `@rule_xxx` 时加载。

```markdown
---
trigger: manual
description: <说明本规则提供什么参考信息，何时应手动引用>
---

# 参考：<中文名> (<English Name>)

## 概述
...

## 详细指南
...
```

---

## Body 结构最佳实践

从现有 19 条规则中提炼的通用结构模式：

| 组件 | 是否必需 | 说明 |
|:---|:---:|:---|
| **TL;DR** | glob 规则推荐 | 2-3 行核心要点速记 |
| **核心原则** | ✅ | 1 句话的设计哲学 blockquote |
| **规则条目** | ✅ | 编号的具体规则，`§N` 分节 |
| **禁止行为** | ✅ | `❌` 前缀的禁忌清单 |
| **验证方法** | 可选 | 命令行或检查表 |
| **协作规则** | 可选 | 与其他规则/文件的关系 |
| **表格速查** | 推荐 | 判定条件 + 行动的对照表 |

### 标记约定

```markdown
> **SSOT**：本文件为 <X> 的唯一定义点。           # 单一权威源声明
> [!CAUTION]                                      # 严重违规警告
> [!TIP]                                          # 优化建议
```
