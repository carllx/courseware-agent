#!/bin/bash
# [DEPRECATED] 此快捷方式已整合至「📦 导出.command」
echo ""
echo "⚠️  此快捷方式已整合至 📦 导出.command（选择类型 [2] TTS）"
echo "   3 秒后自动跳转..."
sleep 3
exec "$(cd "$(dirname "$0")" && pwd)/📦 导出.command"
