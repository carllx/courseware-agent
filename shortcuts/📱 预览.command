#!/bin/bash
# ============================================================
# 📱 预览 — 空间感知的增量 H5 预览管线
#
# 管线流程：
#   1. 空间感知锁定活跃课程（或全课程）
#   2. mtime 增量检测 → 按需重新生成 H5 JSON
#   3. 启动 Vite Dev Server + 自动打开浏览器
#
# 设计原则：
#   - 默认只生成活跃课程的 JSON（启动快 3-5x）
#   - 按 A 可切换全课程模式
#   - 符号链接自动维护
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "📱 H5 交互式课件预览"

# ---- 固定端口 ----
H5_PORT=5173

# ---- Step 0: 清理端口冲突 ----
EXISTING_PID=$(lsof -ti:$H5_PORT 2>/dev/null)
if [ -n "$EXISTING_PID" ]; then
    warn "端口 $H5_PORT 被占用 (PID: $EXISTING_PID)，正在释放..."
    kill -9 $EXISTING_PID 2>/dev/null
    sleep 1
    info "端口 $H5_PORT 已释放"
fi

# ---- Step 1: 空间感知 — 选择生成范围 ----
cd "$ROOT_DIR" || exit 1

# 扫描含 course.yaml 的课程
ALL_COURSES=()
while IFS= read -r dir; do
    ALL_COURSES+=("$(basename "$dir")")
done < <(find "$ROOT_DIR" -maxdepth 2 -name "course.yaml" -exec dirname {} \; | sort)

ACTIVE_COURSE=$(detect_active_course "${ALL_COURSES[@]}")
GENERATE_FLAG=""

if [ -n "$ACTIVE_COURSE" ]; then
    local_mtime=$(find "$ROOT_DIR/$ACTIVE_COURSE" \
        \( -name '*.md' -o -name '*.yaml' \) \
        -not -path '*/build/*' -not -path '*/node_modules/*' \
        -exec stat -f '%m' {} + 2>/dev/null | sort -rn | head -1)
    now_epoch=$(date +%s)
    elapsed=$((now_epoch - local_mtime))
    human_elapsed=$(humanize_elapsed "$elapsed")
    
    echo -e "${BOLD}检测到活跃课程: [${CYAN}$ACTIVE_COURSE${NC}${BOLD}] (${human_elapsed}变动)${NC}"
    echo -e "  ${DIM}[回车] 仅此课程 (快速)  |  [A] 全部课程  |  [Q] 退出${NC}"
    echo -ne "${BOLD}> ${NC}"
    read -r scope_choice
    
    case "${scope_choice}" in
        [Aa]) GENERATE_FLAG="--all"; info "模式: 全课程生成" ;;
        [Qq]) echo "已取消"; exit 0 ;;
        *)    GENERATE_FLAG="--course $ACTIVE_COURSE"; info "模式: 仅 $ACTIVE_COURSE (增量)" ;;
    esac
else
    GENERATE_FLAG="--all"
    info "未检测到明确的活跃课程，使用全课程模式"
fi
echo ""

# ---- Step 2: 按需生成 H5 JSON ----
MANIFEST="build/h5_preview/public/courses/manifest.json"

if [ -f "$MANIFEST" ]; then
    manifest_mtime=$(stat -f '%m' "$MANIFEST")
    
    # 精确的源文件变动检测
    if [ "$GENERATE_FLAG" = "--all" ]; then
        source_mtime=$(find "$ROOT_DIR" -maxdepth 4 \
            \( -name '*.md' -o -name 'course.yaml' \) \
            -not -path '*/build/*' -not -path '*/node_modules/*' -not -path '*/.agent/*' \
            -exec stat -f '%m' {} + 2>/dev/null | sort -rn | head -1)
    else
        # 仅扫描活跃课程
        source_mtime=$(find "$ROOT_DIR/$ACTIVE_COURSE" -maxdepth 4 \
            \( -name '*.md' -o -name 'course.yaml' \) \
            -not -path '*/build/*' \
            -exec stat -f '%m' {} + 2>/dev/null | sort -rn | head -1)
    fi
    
    if [ -n "$source_mtime" ] && [ "$source_mtime" -gt "$manifest_mtime" ]; then
        divider
        echo -e "${YELLOW}[1/3] 源文件有新变动，正在增量编译...${NC}"
        divider
        "$PYTHON" engines/generate_course_h5.py $GENERATE_FLAG
    else
        divider
        echo -e "${BOLD}[1/3] 快照校验通过 ⚡️ 源文件无变动，跳过编译${NC}"
        echo -e "${DIM}(热重载模式下，编辑保存后浏览器自动刷新)${NC}"
        divider
    fi
else
    divider
    echo -e "${BOLD}[1/3] 首次启动，正在生成 H5 数据...${NC}"
    divider
    "$PYTHON" engines/generate_course_h5.py $GENERATE_FLAG
fi
echo ""

# ---- Step 2.5: 确保符号链接 ----
ensure_symlink

# ---- Step 3: 安装依赖（仅首次） ----
cd "$ROOT_DIR/engines/h5_template" || exit 1

if [ ! -d "node_modules" ]; then
    divider
    echo -e "${BOLD}[2/3] 首次运行，安装 npm 依赖...${NC}"
    divider
    npm install
    echo ""
else
    info "[2/3] 依赖已就绪"
fi

# 清理 Vite 缓存
if [ -d "node_modules/.vite" ]; then
    rm -rf "node_modules/.vite"
fi

# ---- Step 4: 启动预览服务器 ----
divider
echo -e "${BOLD}[3/3] 启动 Vite 开发服务器${NC}"
divider
echo -e "${GREEN}🌐 http://localhost:${H5_PORT}${NC}"
echo -e "${DIM}按 Ctrl+C 停止${NC}"
echo ""

(sleep 2 && open http://localhost:${H5_PORT}) &
npx vite --port $H5_PORT --host
