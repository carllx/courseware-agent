#!/bin/bash
# ============================================================
# 🔗 视觉断链检查 — 检查脚本引用图片与磁盘文件的匹配度
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "🔗 视觉素材断链检查"

# 选择课程
select_course
echo ""

# ---- 运行视觉完整性检查 ----
divider
echo -e "${BOLD}交叉比对：脚本引用 vs 磁盘文件${NC}"
divider
cd "$ROOT_DIR" || exit 1
"$PYTHON" "$VALIDATE_DIR/validate_visuals.py" --course "$COURSE" || { error "检查出错"; pause; exit 1; }
echo ""

info "断链检查完成 ✅"
# 信息获取型命令 → 保持窗口等待用户阅读
pause
