#!/bin/bash
# ============================================================
# 📦 导出 — 安全交付管线（质量门禁 + 统一导出入口）
#
# 整合旧版：导出审阅 Word + 导出 TTS 文本
#
# 管线流程：
#   1. 选择课程
#   2. 导出前质量快检（断链 + 规范门禁）
#   3. 交互式选择导出类型（Word / TTS / 全部）
#   4. 执行导出 → Finder 打开输出目录
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "📦 安全导出管线"

# 选择课程
select_course
echo ""

# ---- Step 1: 质量门禁 ----
divider
quick_gate "$COURSE"
gate_result=$?

if [ "$gate_result" -ne 0 ]; then
    echo ""
    error "质量门禁未通过 — 导出已中止"
    echo -e "${DIM}请先运行 🔍 体检.command 查看详细问题${NC}"
    pause
    exit 1
fi
echo ""

# ---- Step 2: 选择导出类型 ----
divider
select_export_type
echo ""

cd "$ROOT_DIR" || exit 1

# ---- Step 3: 执行导出 ----
REVIEW_DIR="$ROOT_DIR/$COURSE/build/presentations/review"
TTS_DIR="$ROOT_DIR/$COURSE/build/tts"

if [ "$EXPORT_TYPE" = "word" ] || [ "$EXPORT_TYPE" = "all" ]; then
    divider
    echo -e "${BOLD}📄 导出审阅 Word 文档...${NC}"
    divider
    "$PYTHON" "$VALIDATE_DIR/export_review_docx.py" --course "$COURSE" --all
    echo ""
fi

if [ "$EXPORT_TYPE" = "tts" ] || [ "$EXPORT_TYPE" = "all" ]; then
    divider
    echo -e "${BOLD}📝 导出 TTS 盲读文本...${NC}"
    divider
    "$PYTHON" "$VALIDATE_DIR/validate_script_length.py" --course "$COURSE" --dump-text --blind-mode
    echo ""
fi

# ---- Step 4: 结果展示 ----
divider
info "导出完成 ✅"
echo ""

# 展示生成的文件
if [ "$EXPORT_TYPE" = "word" ] || [ "$EXPORT_TYPE" = "all" ]; then
    if [ -d "$REVIEW_DIR" ]; then
        echo -e "${BOLD}📄 Word 文档:${NC}"
        ls -la "$REVIEW_DIR"/*.docx 2>/dev/null | while read -r line; do
            echo -e "  ${DIM}$line${NC}"
        done
        echo ""
    fi
fi

if [ "$EXPORT_TYPE" = "tts" ] || [ "$EXPORT_TYPE" = "all" ]; then
    if [ -d "$TTS_DIR" ]; then
        echo -e "${BOLD}📝 TTS 文本:${NC}"
        ls -la "$TTS_DIR"/*_blind.txt 2>/dev/null | while read -r line; do
            echo -e "  ${DIM}$line${NC}"
        done
        echo ""
    fi
fi

# 提示打开目录
OUTPUT_DIR="$REVIEW_DIR"
[ "$EXPORT_TYPE" = "tts" ] && OUTPUT_DIR="$TTS_DIR"

if [ -d "$OUTPUT_DIR" ]; then
    echo -ne "${BOLD}是否在 Finder 中打开输出目录？(Y/n): ${NC}"
    read -r open_dir
    if [[ -z "$open_dir" || "$open_dir" =~ ^[Yy]$ ]]; then
        open "$OUTPUT_DIR"
    fi
fi

auto_close
