#!/bin/bash
# ============================================================
# 📄 导出审阅Word — 导出全部脚本的格式化审阅 Word 文档
# 输出至 <课程>/build/presentations/review/ 目录
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "📄 审阅 Word 文档导出"

# 选择课程
select_course
echo ""

# ---- 导出审阅文档 ----
divider
echo -e "${BOLD}导出格式化审阅 Word 文档 (--all)${NC}"
divider
cd "$ROOT_DIR" || exit 1
"$PYTHON" "$VALIDATE_DIR/export_review_docx.py" --course "$COURSE" --all
echo ""

# 显示输出位置
REVIEW_DIR="$ROOT_DIR/$COURSE/build/presentations/review"
if [ -d "$REVIEW_DIR" ]; then
    info "导出完成 ✅"
    echo -e "${DIM}输出目录: $REVIEW_DIR${NC}"
    echo ""
    echo -e "${BOLD}已生成文件:${NC}"
    ls -la "$REVIEW_DIR"/*.docx 2>/dev/null || warn "未找到 .docx 文件"
    echo ""
    
    # 提示用户是否打开目录
    echo -ne "${BOLD}是否在 Finder 中打开输出目录？(y/N): ${NC}"
    read -r open_dir
    if [[ "$open_dir" =~ ^[Yy]$ ]]; then
        open "$REVIEW_DIR"
    fi
    auto_close
else
    warn "未找到审阅输出目录"
    pause
fi

