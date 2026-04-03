#!/bin/bash
# ============================================================
# 📝 导出TTS文本 — 导出全部脚本的 TTS 盲读纯文本
# 输出至 <课程>/build/tts/<脚本名>_blind.txt
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "📝 TTS 盲读文本导出"

# 选择课程
select_course
echo ""

# ---- 导出 TTS 文本 ----
divider
echo -e "${BOLD}导出盲读纯文本 (--dump-text --blind-mode)${NC}"
divider
cd "$ROOT_DIR" || exit 1
"$PYTHON" "$VALIDATE_DIR/validate_script_length.py" --course "$COURSE" --dump-text --blind-mode
echo ""

# 显示输出位置
TTS_DIR="$ROOT_DIR/$COURSE/build/tts"
if [ -d "$TTS_DIR" ]; then
    info "导出完成 ✅"
    echo -e "${DIM}输出目录: $TTS_DIR${NC}"
    echo ""
    echo -e "${BOLD}已生成文件:${NC}"
    ls -la "$TTS_DIR"/*_blind.txt 2>/dev/null || warn "未找到盲读文件"
    auto_close
else
    warn "未找到 TTS 输出目录"
    pause
fi

