#!/usr/bin/env bash
# ============================================================
# smoke_test.sh — Netlify 部署后线上冒烟测试
# ============================================================
# 用法:
#   bash scripts/smoke_test.sh                          # 使用默认站点
#   bash scripts/smoke_test.sh https://your-site.app    # 指定站点
#
# 验证项:
#   1. 首页 HTTP 200 可达
#   2. 安全头存在（X-Frame-Options 等）
#   3. 课程 manifest JSON 可加载
#   4. 随机抽样静态资产可达
# ============================================================

set -uo pipefail

SITE_URL="${1:-https://endearing-mooncake-60c90e.netlify.app}"
FAILURES=0

echo "=== 🔍 线上冒烟测试 ==="
echo "   站点: $SITE_URL"
echo ""

# ---- 1. 首页可达 ----
HTTP_CODE=$(curl -sLo /dev/null -w '%{http_code}' --max-time 10 "$SITE_URL/")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ [1/4] 首页可达 (HTTP $HTTP_CODE)"
else
    echo "❌ [1/4] 首页不可达 (HTTP $HTTP_CODE)"
    FAILURES=$((FAILURES + 1))
fi

# ---- 2. 安全头验证 ----
HEADERS=$(curl -sI --max-time 10 "$SITE_URL/")
HEADER_PASS=0
HEADER_TOTAL=3

for h in "x-frame-options" "x-content-type-options" "referrer-policy"; do
    if echo "$HEADERS" | grep -qi "$h"; then
        HEADER_PASS=$((HEADER_PASS + 1))
    else
        echo "   ⚠️  缺失安全头: $h"
    fi
done

if [ "$HEADER_PASS" -eq "$HEADER_TOTAL" ]; then
    echo "✅ [2/4] 安全头完整 ($HEADER_PASS/$HEADER_TOTAL)"
else
    echo "❌ [2/4] 安全头不完整 ($HEADER_PASS/$HEADER_TOTAL)"
    FAILURES=$((FAILURES + 1))
fi

# ---- 3. Manifest JSON 可加载 ----
MANIFEST_CODE=$(curl -sLo /dev/null -w '%{http_code}' --max-time 10 "$SITE_URL/courses/manifest.json")
if [ "$MANIFEST_CODE" = "200" ]; then
    echo "✅ [3/4] manifest.json 可加载 (HTTP $MANIFEST_CODE)"
else
    echo "❌ [3/4] manifest.json 不可达 (HTTP $MANIFEST_CODE)"
    FAILURES=$((FAILURES + 1))
fi

# ---- 4. 静态资产抽样 ----
# 测试 Vite 打包的 JS/CSS（带哈希的文件名）
ASSET_OK=0
ASSET_TOTAL=0

# index.html 中提取实际的 JS/CSS 路径
INDEX_HTML=$(curl -sL --max-time 10 "$SITE_URL/")
JS_PATH=$(echo "$INDEX_HTML" | grep -oE '/assets/index-[a-zA-Z0-9]+\.js' | head -1)
CSS_PATH=$(echo "$INDEX_HTML" | grep -oE '/assets/index-[a-zA-Z0-9]+\.css' | head -1)

for asset_path in "$JS_PATH" "$CSS_PATH"; do
    if [ -n "$asset_path" ]; then
        ASSET_TOTAL=$((ASSET_TOTAL + 1))
        ASSET_CODE=$(curl -sLo /dev/null -w '%{http_code}' --max-time 10 "${SITE_URL}${asset_path}")
        [ "$ASSET_CODE" = "200" ] && ASSET_OK=$((ASSET_OK + 1))
    fi
done

if [ "$ASSET_TOTAL" -gt 0 ] && [ "$ASSET_OK" -eq "$ASSET_TOTAL" ]; then
    echo "✅ [4/4] 核心静态资产可达 ($ASSET_OK/$ASSET_TOTAL)"
else
    echo "❌ [4/4] 核心静态资产异常 ($ASSET_OK/$ASSET_TOTAL)"
    FAILURES=$((FAILURES + 1))
fi

# ---- 结论 ----
echo ""
if [ "$FAILURES" -eq 0 ]; then
    echo "=== ✅ 冒烟测试通过 — 站点运行正常 ==="
else
    echo "=== ❌ 冒烟测试失败 — ${FAILURES} 项检查未通过 ==="
    exit 1
fi
