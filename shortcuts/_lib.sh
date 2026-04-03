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
