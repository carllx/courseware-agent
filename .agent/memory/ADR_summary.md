# ADR 速查表 (Architecture Decision Records Summary)

> 每条 ADR 一行摘要，供新 Agent 快速浏览。详情见 `ADR.md` 对应编号。
> 🗄️ **归档注意**：早期基础设施决策（ADR 001-020）已按文件体积优化策略归档至 `archive/ADR_001_020.md`。


| ADR | 日期 | 摘要 |
|:----|:-----|:-----|
| 001 | 02-21 | 实验项目三层架构：course.yaml(SSOT) → planning(拆解) → scripts(落地) |
| 002 | 02-21 | Knowledge Hub 去冗余：禁 tracking 类型，砍 query_hint |
| 003 | 02-21 | Hub 极限压缩：YAML 行内 JSON 序列化，<200 行目标 |
| 004 | 02-22 | docxtpl 延迟加载：render() 前必须 init_docx() |
| 005 | 02-22 | 评分项命名：`章节测试N`/`命题测试N`，desc 必须关联实验 |
| 006 | 02-22 | calendar 扩展字段(重难点/思政/教法)作为大纲 SSOT |
| 007 | 02-23 | 消费者导向 SSOT：教案索引字段归 course.yaml，非 frontmatter |
| 008 | 02-23 | teaching_requirements 支持 str\|dict，推荐 dict 四维结构 |
| 009 | 02-23 | calendar content 必须自带编号前缀；steps 5 阶段完整性约束 |
| 010 | 02-23 | objectives 每维度≥3条；mappings 数组为唯一权威格式 |
| 011 | 02-24 | experiments type 枚举(验证性/综合性/设计性/演示性)，类型≥3种 |
| 012 | 02-24 | 多班排课：教案按课程粒度，进度表按班；假期吸收策略 |
| 013 | 02-24 | 偏移映射必须感知空洞；嵌套循环跳过用标志变量+break |
| 014 | 02-24 | 迁移后即清；废弃目录合并后删；中文禁用 Unicode 转义 |
| 015 | 02-26 | 跨项目修改禁令：只委托不直接改；约束变更必须同步全链路 |
| 016 | 02-27 | 学时字段类型回归 int，浮点学时禁止 |
| 017 | 02-27 | 面向教务行文用`实验N(ExpN)`，技术引用保留`Exp[n]` |
| 018 | 02-27 | 本地 steps 校验脚本(validate_steps.py) 5 条规则 |
| 019 | 03-03 | PPT 引擎：scene≠标题，heading 字段引入，四级降级 |
| 020 | 03-03 | 模块化分段写作：字数预算→逐模块填充→单模块≤8100 tokens |
| 021 | 03-03 | 知识饱和度四维评估 + DRP 三级回退协议 |
| 022 | 03-03 | 知识标签分口头型(计入字数)+参考型(可跳过)两类 |
| 023 | 03-04 | 案例密度门限：≥3000字需≥2案例；教材案例提取清单必填 |
| 024 | 03-05 | Activity Type 枚举仅编码教学模式，Homework 不入枚举；SKILL.md 补齐至 7 种 |
| 025 | 03-06 | 预算正则兼容中英文；口头标签空内容不跳过；RE_TAG_START 兼容冒号后缀 |
| 026 | 03-16 | 通用 H5 课件预览系统：脚本→slides.json→React SPA；Audio-first 联动 |
| 027 | 03-19 | Agent 机制五漏洞修复：audit 三层拆分、DRP/饱和度 SSOT 化、K-2 改模块预算、Hub 放宽、K-2.2 叙事自动触发 |
| 028 | 03-20 | 反注水作弊：`> [!NOTE] 教案深度拓展` 单块≤500字；禁止源文件全盘粘贴 |
| 029 | 03-21 | Phase A/B/C 分段写作闭环 + Q3 短路 + 素材覆盖率门限 70% |
| 030 | 03-21 | .agent/ UX 重构：INDEX 补全、write 三阶段拆分、DEPENDENCY_MAP、best_practices 固化 |
| 031 | 03-26 | `planning/` → `practices/` 目录重构 + Material 对象 8 种 Type |
| 032 | 03-28 | V3 视觉资产零冗余：废绝 Preview 字段，Asset 升级为 Markdown 图片语法 |
| V3  | 03-28 | 源码与构件隔离：`delivery/` → `engines/`，课程级 `build/` + `admin/` |
| 033 | 03-29 | V5 Package 架构：`package.yaml` + `src/` + `.build/` + `public/` |
| 034 | 03-29 | 字数预算校验优先级反转：`<!-- BUDGET: X chars -->` 显式契约绝对优先 |
| 035 | 03-30 | 审计工作流 `--week` 过滤注入：4 脚本统一支持、validate_project 智能跳过、audit.md Step 0 范围解析 |
| 038 | 04-03 | H5 Craft-room 双管线架构：P0 渲染（~300ms）+ P1 异步验证（~2s）、validate_runner.py 统一入口 + Q3 门控 + ValidationContext 心流保护期 |
| 039 | 04-05 | TTS 提取自动化：油猴脚本跨域提权 + Local HTTP Proxy + TTS 指纹双端一致性 |
| 040 | 04-05 | TTS 中间件 SSOT 统一与音频静态代理：engines 中间件为唯一真相来源，支持流式后备代理 |
| 041 | 04-06 | 部署体系双门闸安全机制：强制实施构建产物新鲜度预检与分离验证（Rule+Workflow），根绝断链与历史污染 |
