#!/bin/bash
# ============================================================
# 🚀 发布 — 一键生产构建管线
#
# 新增快捷方式（填补旧架构中 Build 无入口的空白）
#
# 管线流程：
#   1. 废弃资产清理（自动检测+可选清理）
#   2. 生成全集 H5 JSON
#   3. SSG 生产构建（vite build + build-ssg.js）
#   4. 产物验证门禁（preflight --verify）
#   → 构建成功后提示后续操作（Agent 部署）
#
# 注：Git 推送 + Netlify 部署因需要 SSH/代理配置，
#     仍由 Agent 工作流（/publish）处理，不在此脚本中执行。
# ============================================================

# 加载共享库
source "$(cd "$(dirname "$0")" && pwd)/_lib.sh"

banner "🚀 生产构建管线"

cd "$ROOT_DIR" || exit 1

# ---- Step 1: 废弃资产预检 ----
divider
echo -e "${BOLD}[1/4] 废弃资产预检${NC}"
divider

if [ -f "$ROOT_DIR/cleanup_stale_assets.py" ]; then
    stale_output=$("$PYTHON" "$ROOT_DIR/cleanup_stale_assets.py" 2>&1)
    
    if echo "$stale_output" | grep -q '可回收总空间: 0 B'; then
        info "无废弃资产 ✅"
    else
        reclaimable=$(echo "$stale_output" | grep '可回收总空间' | sed 's/.*可回收总空间: //')
        warn "发现废弃资产，可回收空间: ${reclaimable}"
        echo -ne "${BOLD}构建前是否清理？(Y/n): ${NC}"
        read -r do_cleanup
        if [[ -z "$do_cleanup" || "$do_cleanup" =~ ^[Yy]$ ]]; then
            "$PYTHON" "$ROOT_DIR/cleanup_stale_assets.py" --delete
            info "废弃资产已清理"
        else
            info "跳过清理，继续构建"
        fi
    fi
else
    info "清理脚本不存在，跳过"
fi
echo ""

# ---- Step 2: 生成全集 H5 JSON ----
divider
echo -e "${BOLD}[2/4] 生成全集 H5 数据 (--all)${NC}"
divider
"$PYTHON" engines/generate_course_h5.py --all
if [ $? -ne 0 ]; then
    error "H5 数据生成失败！"
    pause
    exit 1
fi
info "H5 数据生成完成"
echo ""

# ---- Step 2.5: 确保符号链接 ----
ensure_symlink

# ---- Step 3: SSG 生产构建 ----
divider
echo -e "${BOLD}[3/4] SSG 生产构建 (vite build + 资产转码)${NC}"
divider

cd "$ROOT_DIR/build/h5_preview" || { error "构建目录不存在"; pause; exit 1; }

# 确保依赖
if [ ! -d "node_modules" ]; then
    echo -e "${DIM}安装 npm 依赖...${NC}"
    npm install
fi

# 显式清理旧 dist/（防止跨次构建幽灵文件残留）
if [ -d "dist" ]; then
    echo -e "${DIM}清理旧 dist/ 产物...${NC}"
    rm -rf dist
fi

npm run build
if [ $? -ne 0 ]; then
    error "SSG 构建失败！请检查上方错误输出"
    pause
    exit 1
fi
info "SSG 构建完成"
echo ""

# ---- Step 4: 产物验证门禁 ----
divider
echo -e "${BOLD}[4/4] 构建产物验证${NC}"
divider
bash scripts/preflight.sh --mode verify
verify_result=$?

echo ""

if [ "$verify_result" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}"
    echo "  ╔═══════════════════════════════════════════╗"
    echo "  ║  🎉 构建成功！dist/ 已就绪可部署          ║"
    echo "  ╚═══════════════════════════════════════════╝"
    echo -e "${NC}"
    
    DIST_SIZE=$(du -sh dist/ 2>/dev/null | cut -f1)
    echo -e "  📦 产物大小: ${BOLD}${DIST_SIZE}${NC}"
    echo -e "  📂 路径: ${DIM}$ROOT_DIR/build/h5_preview/dist/${NC}"
    echo ""
    echo -e "  ${DIM}后续操作:${NC}"
    echo -e "  ${DIM}  • 在 IDE 中输入 /deploy_netlify 部署到 Netlify${NC}"
    echo -e "  ${DIM}  • 在 IDE 中输入 /git_sync 推送源码到 GitHub${NC}"
    echo -e "  ${DIM}  • 在 IDE 中输入 /publish 一键全流程发布${NC}"
else
    error "产物验证失败 — 禁止部署，请检查上方错误"
fi

pause
