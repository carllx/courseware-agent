#!/bin/bash
# [DEPRECATED] 此快捷方式已整合至「📱 预览.command」
echo ""
echo "⚠️  此快捷方式已整合至 📱 预览.command"
echo "   3 秒后自动跳转..."
sleep 3
exec "$(cd "$(dirname "$0")" && pwd)/📱 预览.command"
