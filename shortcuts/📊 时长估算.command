#!/bin/bash
# [DEPRECATED] 此快捷方式已整合至「🔍 体检.command」
echo ""
echo "⚠️  此快捷方式已整合至 🔍 体检.command（时长估算为第 4 项检查）"
echo "   3 秒后自动跳转..."
sleep 3
exec "$(cd "$(dirname "$0")" && pwd)/🔍 体检.command"
