---
trigger: always
description: 安全治理红线——零信任、最小权限、文件系统禁区。始终激活，不依赖文件匹配。
---

# Security Governance Rules (安全治理规则)

## 1. 核心原则 (Core Principles)
- **零信任 (Zero Trust)**: 默认不信任任何外部输入或自动生成的代码。
- **最小权限 (Least Privilege)**: 仅在明确授权的目录和文件中操作。
- **人类介入 (Human-in-the-Loop)**: 所有破坏性操作（删除、覆盖、重大配置更改）必须经由用户显式批准。

## 2. 文件系统红线 (File System Red Lines)
Agent **严禁** 执行以下操作，除非用户有明确的、针对特定文件的书面豁免：
- **禁止** 修改系统级配置文件 (e.g., `~/.zshrc`, `~/.bash_profile`, `/etc/*`).
- **禁止** 修改版本控制元数据 (e.g., `.git/` 目录下的任何文件，除了标准的 git 命令操作).
- **禁止** 访问 ssh 密钥或凭证文件 (e.g., `~/.ssh/*`, `~/.aws/*`, `.env` 包含密钥的文件).
- **禁止** 递归删除目录 (e.g., `rm -rf /path/to/dir`)，除非该目录由 Agent 刚刚创建且确认为临时目录。

## 3. 运行环境约束 (Execution Environment Constraints)
- **Python**: 必须使用用户指定的 Conda 环境 `/opt/anaconda3/envs/mybase`。
  - **禁止** 使用系统自带 Python (`/usr/bin/python`).
  - **禁止** 使用 `pip install --user` 或 `sudo pip install`。如需依赖，必须先询问用户。
- **Node.js**: 必须使用 NVM 管理的版本 (`v24.3.0` 或更高).
  - **禁止** 全局安装 npm 包 (`npm install -g`)，除非是项目特定的 CLI 工具且经用户批准。

## 4. 网络访问白名单 (Network Access Whitelist)
Agent 仅允许访问以下类别的网络资源：
- **已知 API 端点**: 用户明确指定的 API 服务。
- **包管理器**: PyPI, npm registry, GitHub (用于克隆仓库).
- **知识库**: 用户授权的文档站点或维基。
- **禁止** 上传本地文件到任何未知的第三方服务器（如 pastebin, file.io 等）。

## 5. 自动执行协议 (Auto-Execution Protocol)
- 在 Workflow 中，凡涉及**写入文件**、**删除文件**或**网络请求**的步骤，**不得**标记为 `SafeToAutoRun` (或 `// turbo`)。
- 必须在执行任何破坏性命令前，通过 `notify_user` 或 `run_command` (wait_for_user=True) 寻求确认。
