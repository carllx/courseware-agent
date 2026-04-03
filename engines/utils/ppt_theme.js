/**
 * ppt_theme.js — PPT 设计令牌加载器
 *
 * 从 visual_system.yaml 中加载配色、字体等设计令牌，
 * 供布局引擎和主生成脚本统一调用。
 *
 * 用法:
 *   const { loadTheme } = require('./utils/ppt_theme');
 *   const theme = loadTheme('/path/to/visual_system.yaml');
 *   // theme.C.bg_base  → "0F1923"
 *   // theme.FONT.title  → "Arial Black"
 */
const fs = require("fs");
const yaml = require("js-yaml");

/**
 * 加载 visual_system.yaml 并返回标准化的设计令牌对象。
 *
 * @param {string} yamlPath - visual_system.yaml 的绝对路径
 * @returns {{ C: Record<string, string>, FONT: { title: string, body: string } }}
 */
function loadTheme(yamlPath) {
    const raw = yaml.load(fs.readFileSync(yamlPath, "utf-8"));

    // 提取 palette 并去掉 # 号（PptxGenJS 要求无 # 的 hex）
    const palette = raw?.palette || raw?.color_system?.palette || {};
    const C = {};
    for (const [key, val] of Object.entries(palette)) {
        if (typeof val === "string" && val.startsWith("#")) {
            C[key] = val.slice(1); // 去掉 #
        } else if (typeof val === "string") {
            // 跳过 rgba() 等非 hex 值
            if (!val.startsWith("rgba")) {
                C[key] = val;
            }
        }
    }

    // 提取字体 — 兼容多种 key 命名
    const typo = raw?.typography || {};
    const FONT = {
        title: typo.font_en_display || typo.title_family || typo.heading_font || "Arial Black",
        body: typo.font_en_body || typo.body_family || typo.body_font || typo.font_en_primary || "Arial",
    };

    return { C, FONT, raw };
}

/**
 * 为没有 visual_system.yaml 的课程提供默认主题（中性灰度 fallback）。
 * 保证所有渲染函数引用的颜色 key 均有值。
 * v2: 改为课程无关的中性调色板，避免偏向特定课程风格。
 */
function defaultTheme() {
    return {
        C: {
            bg_base: "F5F5F5",
            bg_dark: "1A1A1A",
            bg_surface: "FFFFFF",
            bg_elevated: "EBEBEB",
            primary: "3B82F6",
            primary_light: "60A5FA",
            primary_muted: "2563EB",
            secondary: "10B981",
            tertiary: "F59E0B",
            success: "10B981",
            warning: "F59E0B",
            error: "EF4444",
            info: "3B82F6",
            text_main: "1F2937",
            text_on_dark: "F9FAFB",
            text_secondary: "6B7280",
            text_muted: "9CA3AF",
            border: "D1D5DB",
            divider: "E5E7EB",
        },
        FONT: { title: "Arial Black", body: "Arial" },
        raw: {},
    };
}

module.exports = { loadTheme, defaultTheme };
