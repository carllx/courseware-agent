#!/bin/bash
# ============================================================
# 📊 时长估算 — 查看全部脚本的模块字数/时长/填充率
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "📊 脚本时长估算"

# 选择课程
select_course
echo ""

# ---- 运行时长估算 ----
divider
echo -e "${BOLD}模块字数 & 时长 & 填充率${NC}"
divider
cd "$ROOT_DIR" || exit 1
"$PYTHON" "$VALIDATE_DIR/validate_script_length.py" --course "$COURSE" --module-breakdown || { error "时长估算异常中断"; pause; exit 1; }
echo ""

info "时长估算完成 ✅"
# 信息获取型命令 → 保持窗口等待用户阅读
pause
