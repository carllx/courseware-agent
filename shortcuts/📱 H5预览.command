#!/bin/bash
# ============================================================
# 📱 H5预览 — 全量生成数据 + 启动 Vite 预览服务器
# 自动打开浏览器访问 http://localhost:5173
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "📱 H5 交互式课件预览"

# ---- Step 1: 智能处理 H5 数据（mtime 校验） ----
cd "$ROOT_DIR" || exit 1
MANIFEST="build/h5_preview/public/courses/manifest.json"

if [ -f "$MANIFEST" ]; then
    manifest_mtime=$(stat -f '%m' "$MANIFEST")
    # 扫描所有课程源文件中最新的修改时间（排除构建产物）
    source_mtime=$(find "$ROOT_DIR" -maxdepth 4 \
        \( -name '*.md' -o -name 'course.yaml' \) \
        -not -path '*/build/*' -not -path '*/node_modules/*' -not -path '*/.agent/*' \
        -exec stat -f '%m' {} + 2>/dev/null | sort -rn | head -1)
    
    if [ -n "$source_mtime" ] && [ "$source_mtime" -gt "$manifest_mtime" ]; then
        divider
        echo -e "${YELLOW}[1/3] 快照已过期 — 检测到源文件有新变动，正在增量重编译...${NC}"
        divider
        "$PYTHON" engines/generate_course_h5.py --all
    else
        divider
        echo -e "${BOLD}[1/3] 快照校验通过 ⚡️ 源文件无变动，跳过重编译${NC}"
        echo -e "${DIM}(得益于热重载技术，随后编辑将达到秒级刷新)${NC}"
        divider
    fi
else
    divider
    echo -e "${BOLD}[1/3] 检测到初次启动，正在生成全集 H5 数据...${NC}"
    divider
    "$PYTHON" engines/generate_course_h5.py --all
fi
echo ""

# ---- Step 2: 安装依赖（仅首次） ----
cd "$ROOT_DIR/build/h5_preview" || exit 1

if [ ! -d "node_modules" ]; then
    divider
    echo -e "${BOLD}[2/3] 首次运行，安装 npm 依赖...${NC}"
    divider
    npm install
    echo ""
else
    info "[2/3] 依赖已就绪，跳过安装"
fi

# ---- Step 3: 启动预览服务器 ----
divider
echo -e "${BOLD}[3/3] 启动 Vite 开发服务器${NC}"
divider
echo -e "${GREEN}🌐 浏览器将自动打开 http://localhost:5173${NC}"
echo -e "${DIM}按 Ctrl+C 停止服务器${NC}"
echo ""

# 延迟 2 秒后打开浏览器（等待服务器启动）
(sleep 2 && open http://localhost:5173) &

# 启动 dev server（这会阻塞终端直到 Ctrl+C）
npm run dev
