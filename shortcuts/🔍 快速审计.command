#!/bin/bash
# ============================================================
# 🔍 快速审计 — 一键运行 Quick 级别全套检查
# 包含：项目验证 + 规范合规 + 视觉完整 + 时长估算 + 退化检测
# 模式：全景仪表盘（收集所有步骤状态后统一汇报）
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "🔍 快速审计 (Quick Audit)"

# 选择课程
select_course
echo ""

# ---- 状态收集器 ----
step_names=("项目结构验证" "规范合规性检查" "视觉素材完整性" "时长 & 退化检测")
step_status=()
has_failure=0

# ---- Step 1: 项目验证 ----
divider
echo -e "${BOLD}[1/4] 项目结构验证${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_project.py" --course "$COURSE"
step_status+=("$?")
echo ""

# ---- Step 2: 规范合规性 ----
divider
echo -e "${BOLD}[2/4] 规范合规性检查${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_spec.py" --course "$COURSE"
step_status+=("$?")
echo ""

# ---- Step 3: 视觉素材完整性 ----
divider
echo -e "${BOLD}[3/4] 视觉素材完整性${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_visuals.py" --course "$COURSE"
step_status+=("$?")
echo ""

# ---- Step 4: 时长估算 + 退化检测 ----
divider
echo -e "${BOLD}[4/4] 时长估算 & 退化检测${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_script_length.py" --course "$COURSE" --module-breakdown
step_status+=("$?")
echo ""

# ---- 全景仪表盘输出 ----
divider
echo ""
echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║             📋 审计仪表盘                       ║${NC}"
echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"

for i in "${!step_names[@]}"; do
    local_status="${step_status[$i]}"
    if [ "$local_status" -eq 0 ]; then
        icon="🟢"
        label="PASSED"
        color="$GREEN"
    else
        icon="🔴"
        label="FAILED"
        color="$RED"
        has_failure=1
    fi
    printf "${BOLD}${CYAN}║${NC}  %s  [%d/4] %-22s ${color}%-8s${NC} ${BOLD}${CYAN}║${NC}\n" \
        "$icon" "$((i+1))" "${step_names[$i]}" "$label"
done

echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$has_failure" -eq 0 ]; then
    info "全部审计项通过 ✅"
else
    warn "存在未通过的审计项，请查看上方各步骤的详细输出"
fi

# 信息获取型命令 → 保持窗口等待用户阅读
pause

