# 2025-2026-2 学期课程备课工作区

> **Agent 驱动的多课程备课框架**
> 基于 Markdown 逐字稿 + 自动化验证 + PPT/TTS 生成的端到端教学内容生产线。

> [!IMPORTANT]
> **交接必读**: 请务必优先阅读 **[交接指南 (Handover Guide)](docs/Handover_Guide.md)**，了解教务材料（大纲/进度表/教案）的生成状态及已知限制（如实验文档需手动处理）。

## 项目愿景

本工作区为高校课程备课提供一套**课程无关 (Course-agnostic)** 的内容生产架构。核心思想：

- **内容与工程解耦** — 教师专注写作，Agent 负责验证、格式化、生成 PPT
- **单一事实来源 (SSOT)** — 每种信息只在一处定义，归属由消费者决定（[ADR 007](docs/ARCHITECTURE.md)）
- **一键验证** — 从标签合规到素材完整性，全链路自动化检查

## 已注册课程

| 课程 | 目录 | 类型 | 状态 |
|:---|:---|:---|:---|
| 实习指导 | `实习指导/` | project | 🟢 活跃 |
| 交互产品开发 | `交互产品开发/` | weekly | 🟢 配置完毕 (60学时) |
| 信息可视化 | `信息可视化/` | weekly | 🟢 配置完毕 (40学时) |

```text
2025-2026-2 课程/
├── README.md                       ← 你在这里
├── docs/                           # 项目文档
│   ├── ARCHITECTURE.md             #   架构与设计哲学
│   ├── SCRIPT_SPEC.md              #   脚本撰写规范
│   ├── WORKFLOWS.md                #   工作流速查手册
│   ├── CONTRIBUTING.md             #   新课程接入指南
│   └── Handover_Guide.md           #   [NEW] 备课交接与生成指南
│
├── <课程>/                          # 每门课程一个目录
│   ├── course.yaml                 #   课程元数据（必需）
│   ├── knowledge/                  #   教材 + 教纲 + 资源库 (repository)
│   ├── practices/                   #   [NEW] 实验与教学规划
│   ├── scripts/                    #   逐字稿 (.md)
│   │   ├── 00_structure_map.md     #     课程结构图
│   │   ├── S01_*.md / W01_*.md     #     各单元脚本
│   │   └── tts/                    #     TTS 导出目录
│   ├── styles/                     #   设计系统（可选）
│   │   ├── design_system.md        #     人类可读版
│   │   └── visual_system.yaml      #     机器可执行版
│   ├── visuals/assets/             #   视觉素材（按章节分槽）
│   └── delivery/                   #   交付物（PPT、审阅 docx）
│
└── .agent/                         # Agent 自动化引擎
    ├── INDEX.md                    #   工作区导航
    ├── manifest.json               #   课程注册清单
    ├── rules/                      #   全局规则（5 条）
    ├── workflows/                  #   工作流定义（6 个）
    ├── skills/                     #   技能包（6 个）
    └── templates/                  #   模板
```
- `交互产品开发/`: 已配置完毕 (CNFU002572)。包含 `practices/experiment_planning.md`。
- `信息可视化/`: 已配置完毕 (CNFU003847)。包含 `practices/experiment_planning.md`。
- `实习指导/`: 特殊 Project 课程，非标准生成流程。
- `docs/`: 存放交接与操作文档。

## 快速开始

```bash
# 生成所有文档
cd ../教务材料
python scripts/generate.py --course "交互产品开发"
python scripts/generate.py --course "信息可视化"
```

## 通用工作流

| 命令 | 说明 | 详细文档 |
|:---|:---|:---|
| `/new_course` | 创建新课程脚手架 | [CONTRIBUTING.md](docs/CONTRIBUTING.md) |
| `/write` | 撰写逐字稿 | [WORKFLOWS.md](docs/WORKFLOWS.md#write) |
| `/validate_script` | 脚本规范审查 | [WORKFLOWS.md](docs/WORKFLOWS.md#validate_script) |
| `/validate_knowledge` | 知识枢纽健康审查 | `.agent/workflows/validate_knowledge.md` |
| `/audit` | 全面质量审查 | [WORKFLOWS.md](docs/WORKFLOWS.md#audit) |
| `/ppt` | 从脚本生成 PPT | [WORKFLOWS.md](docs/WORKFLOWS.md#ppt) |
| `/export_docx` | 导出 TTS 文本 / 审阅 Word | [WORKFLOWS.md](docs/WORKFLOWS.md#export_docx) |

## 技能包

| 技能 | 说明 |
|:---|:---|
| `validation_suite` | 验证套件 — 规范检查、素材审计、知识检查、时长估算、TTS导出 |
| `script_format` | 脚本格式规范 — 知识标签、VISUAL/ACTIVITY 块、Layout 枚举 |
| `narrative_archaeologist` | 深度调研引擎 — 多轮 Web 搜索 + 质量过滤 + 锚点回归 |
| `librarian` | 知识枢纽查询引擎 — 三层漏斗自动提取与归档书本及网络知识 |
| `pptx` | PPT 生成 / 编辑 / QA |
| `docx` | Word 文档处理 |
| `pdf` | PDF 处理 |


# 1. 创建新课程
> /new_course 数字音频编辑

# 2. 将教材放入知识库
cp 教材.pdf 数字音频编辑/knowledge/textbook/

# 3. 编辑课程配置
vi 数字音频编辑/course.yaml

# 4. 撰写逐字稿
> /write 数字音频编辑 S01

# 5. 验证脚本
> /validate_script 数字音频编辑

# 6. 生成 PPT
> /ppt 数字音频编辑 S01_Intro
```

## 环境要求

| 工具 | 版本 | 用途 |
|:---|:---|:---|
| Python | 3.10+ (`/opt/anaconda3/envs/mybase`) | 验证脚本、文档处理 |
| Node.js | v24+ (NVM 管理) | PPT 生成 (pptxgenjs) |
| `python-docx` | pip | Word 文档生成 |
| Pandoc | 3.5 | 文档格式转换 |

## 文档索引

- **[架构与设计哲学](docs/ARCHITECTURE.md)** — 三层解耦、数据流、规则系统
- **[脚本撰写规范](docs/SCRIPT_SPEC.md)** — VISUAL/ACTIVITY 块、知识标签、命名规则
- **[工作流速查手册](docs/WORKFLOWS.md)** — 6 个 `/` 命令的完整参数与示例
- **[新课程接入指南](docs/CONTRIBUTING.md)** — 从零接入新课程的全流程
- **[交接指南 (Handover Guide)](docs/Handover_Guide.md)** — 2025-2026-2 学期备课交接说明
