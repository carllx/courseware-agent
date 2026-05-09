#!/bin/bash
# ============================================================
# 🔍 体检 — 全景课程健康度仪表盘
#
# 整合旧版：快速审计 + 视觉断链检查 + 时长估算 + 废弃资产扫描
#
# 管线流程：
#   1. 项目结构验证
#   2. 规范合规性检查
#   3. 视觉素材完整性（含断链）
#   4. 时长 & 退化检测
#   5. 废弃资产扫描
#   6. 构建新鲜度检测
#   → 输出全景仪表盘 + 磁盘报告
#   → 发现废弃资产时提示清理
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "🔍 课程健康度体检"

# 选择课程
select_course
echo ""

# ---- 状态收集器 ----
step_names=("项目结构验证" "规范合规性" "视觉完整性" "时长退化检测" "废弃资产" "构建新鲜度")
step_status=()
step_detail=()
has_failure=0

cd "$ROOT_DIR" || exit 1

# ---- Step 1: 项目验证 ----
divider
echo -e "${BOLD}[1/6] 项目结构验证${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_project.py" --course "$COURSE"
step_status+=("$?")
step_detail+=("")
echo ""

# ---- Step 2: 规范合规性 ----
divider
echo -e "${BOLD}[2/6] 规范合规性检查${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_spec.py" --course "$COURSE"
step_status+=("$?")
step_detail+=("")
echo ""

# ---- Step 3: 视觉素材完整性（含断链） ----
divider
echo -e "${BOLD}[3/6] 视觉素材完整性（断链检查）${NC}"
divider
visual_output=$("$PYTHON" "$VALIDATE_DIR/validate_visuals.py" --course "$COURSE" 2>&1)
visual_exit=$?
echo "$visual_output"
broken_count=$(echo "$visual_output" | grep -c '❌' 2>/dev/null || echo "0")
step_status+=("$visual_exit")
if [ "$visual_exit" -ne 0 ]; then
    step_detail+=("${broken_count} 断链")
else
    step_detail+=("")
fi
echo ""

# ---- Step 4: 时长估算 + 退化检测 ----
divider
echo -e "${BOLD}[4/6] 时长估算 & 退化检测${NC}"
divider
"$PYTHON" "$VALIDATE_DIR/validate_script_length.py" --course "$COURSE" --module-breakdown
step_status+=("$?")
step_detail+=("")
echo ""

# ---- Step 5: 废弃资产扫描 ----
divider
echo -e "${BOLD}[5/6] 废弃资产扫描${NC}"
divider
if [ -f "$CLEANUP_SCRIPT" ]; then
    stale_output=$("$PYTHON" "$CLEANUP_SCRIPT" --course "$COURSE" 2>&1)
    stale_exit=0
    
    # 提取废弃文件数量
    stale_media=$(echo "$stale_output" | grep '废弃视觉素材' | grep -o '[0-9]* 个' | head -1)
    stale_tts_dup=$(echo "$stale_output" | grep '重复 TTS' | grep -o '[0-9]* 个' | head -1)
    reclaimable=$(echo "$stale_output" | grep '可回收总空间' | sed 's/.*可回收总空间: //')
    
    if echo "$stale_output" | grep -q '可回收总空间: 0 B'; then
        info "无废弃资产 ✅"
        step_detail+=("")
        STALE_ASSET_FOUND=0
    else
        warn "发现可回收资产: 视觉 ${stale_media:-0}, 重复TTS ${stale_tts_dup:-0}"
        echo -e "  ${DIM}可回收空间: ${reclaimable:-未知}${NC}"
        step_detail+=("${reclaimable}")
        stale_exit=2  # 警告级别（非失败）
        STALE_ASSET_FOUND=1
    fi
    step_status+=("$stale_exit")
else
    warn "cleanup_stale_assets.py 未找到，跳过"
    step_status+=(0)
    step_detail+=("跳过")
    STALE_ASSET_FOUND=0
fi
echo ""

# ---- Step 6: 构建新鲜度检测 ----
divider
echo -e "${BOLD}[6/6] 构建新鲜度检测${NC}"
divider
check_build_freshness
if [ "$BUILD_FRESH" -eq 0 ]; then
    step_status+=(0)
    step_detail+=("")
else
    step_status+=(2)  # 警告级别
    step_detail+=("需重建")
fi
echo ""

# ---- 全景仪表盘 ----
divider
echo ""
echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║          📋 课程健康度仪表盘                    ║${NC}"
echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"

for i in "${!step_names[@]}"; do
    local_status="${step_status[$i]}"
    local_detail="${step_detail[$i]}"
    
    if [ "$local_status" -eq 0 ]; then
        icon="🟢"
        label="PASSED"
        color="$GREEN"
    elif [ "$local_status" -eq 2 ]; then
        icon="🟡"
        label="WARN  "
        color="$YELLOW"
    else
        icon="🔴"
        label="FAILED"
        color="$RED"
        has_failure=1
    fi
    
    detail_str=""
    [ -n "$local_detail" ] && detail_str=" ($local_detail)"
    
    printf "${BOLD}${CYAN}║${NC}  %s [%d/6] %-18s ${color}%-8s${NC}%-10s ${BOLD}${CYAN}║${NC}\n" \
        "$icon" "$((i+1))" "${step_names[$i]}" "$label" "$detail_str"
done

echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
disk_usage_report "$COURSE"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$has_failure" -eq 0 ]; then
    info "全部检查项通过 ✅"
else
    warn "存在未通过的检查项，请查看上方详细输出"
fi

# ---- 废弃资产清理提示 ----
if [ "$STALE_ASSET_FOUND" -eq 1 ]; then
    echo ""
    echo -ne "${BOLD}发现废弃资产，是否立即清理？(y/N): ${NC}"
    read -r do_cleanup
    if [[ "$do_cleanup" =~ ^[Yy]$ ]]; then
        run_cleanup_delete "$COURSE"
    fi
fi

# 体检型命令 → 保持窗口
pause
