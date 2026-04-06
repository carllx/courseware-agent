#!/usr/bin/env bash
# ============================================================
# preflight.sh — H5 课件构建管线统一预检与验证
# ============================================================
# 用法:
#   bash scripts/preflight.sh --mode check   # 构建前新鲜度检测
#   bash scripts/preflight.sh --mode verify  # 构建后产物验证
#
# 必须在 engines/h5_template 目录下运行。
# ============================================================

set -uo pipefail

MODE="${1:---mode}"
MODE_VAL="${2:-check}"

# 解析 --mode 参数（兼容 --mode check 和 --mode=check 两种格式）
if [[ "$MODE" == "--mode="* ]]; then
  MODE_VAL="${MODE#--mode=}"
elif [[ "$MODE" == "--mode" ]]; then
  MODE_VAL="${MODE_VAL}"
else
  echo "❌ 用法: bash scripts/preflight.sh --mode <check|verify>"
  exit 1
fi

# 定位工作区根目录（engines/h5_template 的上两级）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$(dirname "$ENGINE_DIR")")"
DIST_DIR="$ENGINE_DIR/dist"

# ============================================================
# 模式 A: 构建前新鲜度检测 (pre-build freshness check)
# ============================================================
run_check() {
  echo "=== 🔍 构建新鲜度预检 ==="

  # 1. dist 是否存在
  if [ ! -f "$DIST_DIR/index.html" ]; then
    echo "⚠️  dist/ 不存在或不完整 — 需要全量构建"
    echo ""
    echo "=== 结论: 需要构建 ==="
    exit 0
  fi

  echo "📅 上次构建: $(stat -f '%Sm' "$DIST_DIR/index.html")"

  # 2. 检测比上次构建更新的 TTS 音频
  TTS_NEW=$(find "$WORKSPACE_DIR"/*/weeks/*/tts/ -name "*.aac" -newer "$DIST_DIR/index.html" 2>/dev/null | wc -l | tr -d ' ')
  echo "🔊 新增 TTS 音频: ${TTS_NEW} 个文件待转码"

  # 3. 检测比上次构建更新的图片
  IMG_NEW=$(find "$WORKSPACE_DIR"/*/weeks/*/public/slides/ -name "*.png" -newer "$DIST_DIR/index.html" 2>/dev/null | wc -l | tr -d ' ')
  echo "📸 新增图片资产: ${IMG_NEW} 个文件待转码"

  # 4. 检测比上次构建更新的脚本源文件 (.md)
  MD_NEW=$(find "$WORKSPACE_DIR"/*/weeks/*/src/ -name "*.md" -newer "$DIST_DIR/index.html" 2>/dev/null | wc -l | tr -d ' ')
  echo "📝 变更脚本源文件: ${MD_NEW} 个"

  # 5. dist/assets/tts 完整性快照
  TTS_DIST=$(find "$DIST_DIR/assets/tts/" -name "*.mp3" 2>/dev/null | wc -l | tr -d ' ')
  echo "📦 dist 已有 TTS: ${TTS_DIST} 个 MP3"

  echo ""

  TOTAL=$((TTS_NEW + IMG_NEW + MD_NEW))
  if [ "$TOTAL" -eq 0 ]; then
    echo "=== ✅ dist 是最新的，无需重新构建 ==="
  else
    echo "=== ⚠️ 有 ${TOTAL} 项变更，建议执行 /build ==="
  fi
}

# ============================================================
# 模式 B: 构建后产物验证 (post-build artifact verification)
# ============================================================
run_verify() {
  echo "=== 📋 构建产物验证 ==="

  FAILURES=0

  # 1. 核心目录存在性
  if [ -d "$DIST_DIR/assets/media" ]; then
    echo "✅ assets/media"
  else
    echo "❌ assets/media 缺失"
    FAILURES=$((FAILURES + 1))
  fi

  if [ -d "$DIST_DIR/assets/tts" ]; then
    echo "✅ assets/tts"
  else
    echo "❌ assets/tts 缺失"
    FAILURES=$((FAILURES + 1))
  fi

  if [ -d "$DIST_DIR/courses" ]; then
    echo "✅ courses"
  else
    echo "❌ courses 缺失"
    FAILURES=$((FAILURES + 1))
  fi

  # 2. 统计量
  WEBP_COUNT=$(find "$DIST_DIR/assets/media/" -name '*.webp' 2>/dev/null | wc -l | tr -d ' ')
  MP3_COUNT=$(find "$DIST_DIR/assets/tts/" -name '*.mp3' 2>/dev/null | wc -l | tr -d ' ')
  JSON_COUNT=$(find "$DIST_DIR/courses/" -name '*.json' 2>/dev/null | wc -l | tr -d ' ')
  DIST_SIZE=$(du -sh "$DIST_DIR/" 2>/dev/null | cut -f1)

  echo "📸 WebP 图片: ${WEBP_COUNT} 张"
  echo "🔊 MP3 音频: ${MP3_COUNT} 段"
  echo "📄 课程 JSON: ${JSON_COUNT} 个"
  echo "📦 dist 总大小: ${DIST_SIZE}"

  echo ""

  if [ "$FAILURES" -gt 0 ]; then
    echo "=== ❌ 验证失败 — ${FAILURES} 项关键目录缺失，禁止部署 ==="
    exit 1
  fi

  if [ "$JSON_COUNT" -eq 0 ]; then
    echo "=== ❌ 验证失败 — 课程 JSON 为空，构建可能不完整 ==="
    exit 1
  fi

  echo "=== ✅ 验证通过 — dist/ 可部署 ==="
}

# ============================================================
# 路由
# ============================================================
case "$MODE_VAL" in
  check)
    run_check
    ;;
  verify)
    run_verify
    ;;
  *)
    echo "❌ 未知模式: $MODE_VAL (支持: check, verify)"
    exit 1
    ;;
esac
