#!/bin/bash
# ============================================================
# _lib.sh — 快捷方式共享函数库
# 提供路径定位、课程选择菜单、颜色常量等公共能力
# ============================================================

# ---- 颜色常量 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # 重置

# ---- 路径定位 ----
# 自动定位到 workspace 根目录（shortcuts/ 的父目录）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Python 解释器
PYTHON="/opt/anaconda3/envs/mybase/bin/python"

# 验证套件脚本目录
VALIDATE_DIR="$ROOT_DIR/.agent/skills/validation_suite/scripts"

# ---- 工具函数 ----

# 带 emoji 和颜色的标题横幅
banner() {
    local title="$1"
    local width=50
    echo ""
    echo -e "${CYAN}$(printf '═%.0s' $(seq 1 $width))${NC}"
    echo -e "${BOLD}  $title${NC}"
    echo -e "${CYAN}$(printf '═%.0s' $(seq 1 $width))${NC}"
    echo ""
}

# 成功信息
info() {
    echo -e "${GREEN}✓${NC} $1"
}

# 警告信息
warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 错误信息
error() {
    echo -e "${RED}✗${NC} $1"
}

# 分隔线
divider() {
    echo -e "${DIM}$(printf '─%.0s' $(seq 1 50))${NC}"
}

# 等待按键（防止终端立即关闭，通常用于查报错）
pause() {
    echo ""
    divider
    echo -e "${DIM}按任意键关闭窗口...${NC}"
    read -n 1 -s -r
}

# 成功时的流畅关闭（不卡顿体验）
auto_close() {
    echo ""
    divider
    echo -e "${GREEN}✅ 成功完成 (终端窗将在 3 秒后隐步关闭)${NC}"
    sleep 3
}


# 探测最近活跃的课程（基于源文件 mtime，而非历史缓存）
# 返回：最近有文件变动的课程目录名
detect_active_course() {
    local most_recent_course=""
    local most_recent_time=0
    for course_name in "$@"; do
        local latest_mtime
        latest_mtime=$(find "$ROOT_DIR/$course_name" \
            \( -name '*.md' -o -name '*.yaml' \) \
            -not -path '*/build/*' -not -path '*/node_modules/*' \
            -exec stat -f '%m' {} + 2>/dev/null | sort -rn | head -1)
        if [ -n "$latest_mtime" ] && [ "$latest_mtime" -gt "$most_recent_time" ]; then
            most_recent_time="$latest_mtime"
            most_recent_course="$course_name"
        fi
    done
    # 输出结果供调用方捕获
    echo "$most_recent_course"
}

# 将 epoch 秒差转为人类可读的时间描述
humanize_elapsed() {
    local diff=$1
    if [ "$diff" -lt 60 ]; then
        echo "${diff} 秒前"
    elif [ "$diff" -lt 3600 ]; then
        echo "$((diff / 60)) 分钟前"
    elif [ "$diff" -lt 86400 ]; then
        echo "$((diff / 3600)) 小时前"
    else
        echo "$((diff / 86400)) 天前"
    fi
}

# 扫描根目录下含 course.yaml 的子目录，展示编号菜单
# 设置全局变量 COURSE（课程目录名）
select_course() {
    local courses=()
    
    # 扫描含 course.yaml 的子目录
    while IFS= read -r dir; do
        courses+=("$(basename "$dir")")
    done < <(find "$ROOT_DIR" -maxdepth 2 -name "course.yaml" -exec dirname {} \; | sort)
    
    if [ ${#courses[@]} -eq 0 ]; then
        error "未找到任何课程（含 course.yaml 的目录）"
        pause
        exit 1
    fi
    
    # 如果只有一门课程，自动选择
    if [ ${#courses[@]} -eq 1 ]; then
        COURSE="${courses[0]}"
        info "自动选择唯一课程: ${BOLD}$COURSE${NC}"
        return
    fi
    
    # 空间感知：基于 mtime 推导当前最活跃的课程
    local active
    active=$(detect_active_course "${courses[@]}")
    
    if [ -n "$active" ]; then
        # 计算距今多久
        local active_mtime now_epoch elapsed human_elapsed
        active_mtime=$(find "$ROOT_DIR/$active" \
            \( -name '*.md' -o -name '*.yaml' \) \
            -not -path '*/build/*' -not -path '*/node_modules/*' \
            -exec stat -f '%m' {} + 2>/dev/null | sort -rn | head -1)
        now_epoch=$(date +%s)
        elapsed=$((now_epoch - active_mtime))
        human_elapsed=$(humanize_elapsed "$elapsed")
        
        echo -ne "${BOLD}检测到最近活跃课程 [${CYAN}$active${NC}${BOLD}]（${human_elapsed}有变动），继续？(Y/n): ${NC}"
        read -r use_active
        if [[ -z "$use_active" || "$use_active" =~ ^[Yy]$ ]]; then
            COURSE="$active"
            info "已锁定活跃课程: ${BOLD}$COURSE${NC}"
            return
        fi
        echo ""
    fi
    
    # 降级：多门课程编号菜单
    echo -e "${BOLD}请选择课程:${NC}"
    echo ""
    for i in "${!courses[@]}"; do
        echo -e "  ${CYAN}[$((i+1))]${NC} ${courses[$i]}"
    done
    echo ""
    
    while true; do
        echo -ne "${BOLD}输入编号 (1-${#courses[@]}): ${NC}"
        read -r choice
        
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#courses[@]}" ]; then
            COURSE="${courses[$((choice-1))]}"
            info "已绑定: ${BOLD}$COURSE${NC}"
            return
        else
            warn "无效输入，请重新尝试"
        fi
    done
}


# ---- 管线共享函数（v2 重设计新增） ----

# 废弃资产扫描（干跑模式），设置全局变量 STALE_COUNT / STALE_SIZE
run_cleanup_scan() {
    local course_flag=""
    [ -n "${1:-}" ] && course_flag="--course $1"
    
    local output
    output=$("$PYTHON" "$ROOT_DIR/cleanup_stale_assets.py" $course_flag 2>&1)
    echo "$output"
    
    # 从输出中提取统计（匹配汇总行）
    STALE_COUNT=$(echo "$output" | grep -o '可回收总空间' | head -1)
    if echo "$output" | grep -q '可回收总空间: 0 B'; then
        STALE_ASSET_FOUND=0
    else
        STALE_ASSET_FOUND=1
    fi
}

# 执行废弃资产清理（移入 _trash/）
run_cleanup_delete() {
    local course_flag=""
    [ -n "${1:-}" ] && course_flag="--course $1"
    "$PYTHON" "$ROOT_DIR/cleanup_stale_assets.py" --delete $course_flag
}

# 构建新鲜度检测，设置全局变量 BUILD_FRESH (0=最新, 1=需重建)
check_build_freshness() {
    local preflight_script="$ROOT_DIR/build/h5_preview/scripts/preflight.sh"
    if [ ! -f "$preflight_script" ]; then
        BUILD_FRESH=1
        warn "preflight.sh 不存在，需要全量构建"
        return
    fi
    
    local output
    output=$(cd "$ROOT_DIR/build/h5_preview" && bash scripts/preflight.sh --mode check 2>&1)
    echo "$output"
    
    if echo "$output" | grep -q '✅ dist 是最新的'; then
        BUILD_FRESH=0
    else
        BUILD_FRESH=1
    fi
}

# 轻量级质量门禁（断链 + 规范），用于导出前拦截。返回 0=通过, 1=失败
quick_gate() {
    local course="$1"
    local failures=0
    
    echo -e "${BOLD}[门禁] 导出前质量快检...${NC}"
    
    # 断链检查
    "$PYTHON" "$VALIDATE_DIR/validate_visuals.py" --course "$course" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        error "视觉素材存在断链 — 请先修复后再导出"
        failures=$((failures + 1))
    else
        info "视觉素材完整性 ✅"
    fi
    
    # 规范合规（静默模式，只看退出码）
    "$PYTHON" "$VALIDATE_DIR/validate_spec.py" --course "$course" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        warn "规范合规检查存在警告（不阻止导出）"
    else
        info "规范合规性 ✅"
    fi
    
    return $failures
}

# 交互式导出类型选择菜单
# 设置全局变量 EXPORT_TYPE (word / tts / all)
select_export_type() {
    echo -e "${BOLD}请选择导出类型:${NC}"
    echo ""
    echo -e "  ${CYAN}[1]${NC} 📄 审阅 Word 文档"
    echo -e "  ${CYAN}[2]${NC} 📝 TTS 盲读文本"
    echo -e "  ${CYAN}[3]${NC} 📦 全部导出 ${DIM}(默认)${NC}"
    echo ""
    echo -ne "${BOLD}输入编号 (1-3, 回车=全部): ${NC}"
    read -r choice
    
    case "${choice:-3}" in
        1) EXPORT_TYPE="word" ;;
        2) EXPORT_TYPE="tts" ;;
        *) EXPORT_TYPE="all" ;;
    esac
}

# 确保符号链接存在（engines/h5_template/public/courses → build 数据）
ensure_symlink() {
    local ssot="$ROOT_DIR/engines/h5_template/public/courses"
    local build="$ROOT_DIR/build/h5_preview/public/courses"
    
    if [ ! -L "$ssot" ] && [ -d "$build" ]; then
        rm -rf "$ssot" 2>/dev/null
        ln -s "$build" "$ssot"
        info "符号链接已创建"
    fi
}

# 磁盘占用统计（用于体检仪表盘）
disk_usage_report() {
    local course="$1"
    local src_size tts_size pub_size
    src_size=$(du -sh "$ROOT_DIR/$course/weeks" 2>/dev/null | cut -f1 | tr -d ' ')
    tts_size=$(du -sh "$ROOT_DIR/$course/weeks"/*/tts 2>/dev/null | tail -1 | cut -f1 | tr -d ' ')
    pub_size=$(du -sh "$ROOT_DIR/$course/weeks"/*/public 2>/dev/null | tail -1 | cut -f1 | tr -d ' ')
    echo -e "  💾 磁盘: weeks ${src_size:-N/A} | tts ${tts_size:-N/A} | public ${pub_size:-N/A}"
}
