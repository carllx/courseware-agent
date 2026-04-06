---
trigger: model_decision
description: 当执行 Netlify 部署（/deploy_netlify）或讨论"发布"、"上线"、"deploy"时，必须确认 dist/ 已通过构建验证门，防止资产断链。
---

# 规则：部署前构建验证门 (Pre-Deploy Build Gate)

> **核心原则**：`dist/` 是临时构建产物，其内容必须与源文件保持同步。部署前必须验证，绝不盲推。

## §1 强制约束

在执行 `npx netlify deploy` 或调用 Netlify MCP 部署工具**之前**，Agent 必须：

1. 运行 `bash engines/h5_template/scripts/preflight.sh --mode verify`
2. 仅当脚本以 exit code 0 退出（输出含 `✅ 验证通过`）时，才允许继续部署
3. 如果验证失败，引导用户先执行 `/build` 工作流

## §2 禁止行为

- ❌ 跳过 preflight 验证直接执行 `netlify deploy`
- ❌ 仅因为上次部署成功就假设当前 dist 仍有效
- ❌ 在 dist 不存在或结构不完整时执行部署
- ❌ 使用 `git add -f` 将 dist 加入版本控制
