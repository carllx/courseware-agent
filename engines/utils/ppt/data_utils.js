/**
 * ppt/data_utils.js — PPT 布局引擎共享工具函数
 *
 * 提供数据解析、图片尺寸计算、标题提取等公共能力，
 * 供所有 renderers_*.js 和 dispatcher.js 调用。
 */
const path = require('path');
const fs = require('fs');
const { imageSize: sizeOf } = require('image-size');

// ============================================================
// 工厂函数（防止 pptxgenjs 对象变异）
// ============================================================
const cardShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.08 });

// ============================================================
// 图片尺寸计算
// ============================================================

/**
 * 安全读取图片宽高比并计算最终缩放尺寸
 * @param {string} assetPath - 图片文件绝对路径
 * @param {number} maxW - 最大宽度 (inches)
 * @param {number} maxH - 最大高度 (inches)
 * @returns {{ w: number, h: number }} 最终缩放后的尺寸
 */
function fitImage(assetPath, maxW, maxH) {
    let finalW = maxW;
    let finalH = maxH;
    try {
        const dims = sizeOf(fs.readFileSync(assetPath));
        const ar = dims.width / dims.height;
        if (ar > (maxW / maxH)) {
            finalH = maxW / ar;
        } else {
            finalW = maxH * ar;
        }
    } catch (e) {
        console.warn(`⚠️  图片尺寸读取失败 ${path.basename(assetPath)}: ${e.message}，fallback 为 1:1`);
        finalW = Math.min(maxW, maxH);
        finalH = finalW;
    }
    return { w: finalW, h: finalH };
}

// ============================================================
// 标题提取与自适应
// ============================================================

/**
 * 提取幻灯片标题
 * 优先级：headline/text (作者显式指定) > H4 (指令标题) > H3 (断言标题) > sceneSummary(scene)
 */
function extractTitle(visual) {
    // 1. 优先使用 [VISUAL] 块中作者显式指定的标题
    const raw = visual.headline || visual.text || '';
    let titleStr = '';
    if (raw) titleStr = raw.replace(/^"|"$/g, '').replace(/\\n/g, '\n');
    // 2. 退化为微观行动指令 (H4)
    else if (visual.h4) titleStr = visual.h4;
    // 3. 退化为宏观断言结构 (H3 / Parser 默认 heading)
    else if (visual.h3) titleStr = visual.h3;
    else if (visual.heading) titleStr = visual.heading;
    // 4. 用 Slide 字段作为标题
    else if (visual.slide) titleStr = visual.slide;
    // 5. 最后 fallback 到 scene 截取
    else titleStr = sceneSummary(visual.scene);

    if (typeof titleStr === 'string') {
        titleStr = titleStr.replace(/\*\*/g, '').replace(/__/g, '');
    }
    return titleStr;
}

/**
 * 根据标题长度自适应字号
 * @param {string} title
 * @returns {number} 字号
 */
function adaptiveTitleSize(title) {
    if (!title) return 28;
    if (title.length <= 10) return 28;
    if (title.length <= 18) return 24;
    return 20;
}

/**
 * 从 Scene 提取简短标题（第一个句号/逗号之前的内容）
 */
function sceneSummary(scene, maxLen = 30) {
    if (!scene) return '';
    const cut = scene.replace(/^"|"$/g, '');
    const end = cut.search(/[。，；：\n]/);
    if (end > 0 && end < maxLen) return cut.substring(0, end);
    return cut.length > maxLen ? cut.substring(0, maxLen) + '…' : cut;
}

// ============================================================
// 颜色辅助
// ============================================================

/**
 * 安全获取颜色（带 fallback）
 */
function getC(theme, key, fallback) {
    return theme.C[key] || fallback || 'CCCCCC';
}

// ============================================================
// 列表数据解析
// ============================================================

/**
 * 解析 List 字符串为数组
 * 支持 "A / B / C" 或 "A · B · C" 或 "A, B, C" 格式
 */
function parseListString(list) {
    // 1. 若已预处理为数组，跳过拆分直接进入冒号解析
    if (Array.isArray(list)) {
        return list.map(item => {
            if (typeof item !== 'string') return item;
            const colonMatch = item.match(/^([^:：]+)[:：]\s*(.+)$/);
            if (colonMatch) {
                return { title: colonMatch[1].trim(), desc: colonMatch[2].trim() };
            }
            return item;
        });
    }
    if (typeof list !== 'string') return [];

    // 2. 字符串输入：执行分隔符拆分
    let parts = [];
    // 优先级分隔策略：
    //   1) 若包含 "|" → 仅按 "|" 拆分（保护内容中固有的 · / 等符号）
    //   2) 否则尝试 / 或 · 分隔
    //   3) 否则尝试 "Digit." 编号格式
    //   4) 最后尝试逗号 / 顿号
    if (list.includes('|')) {
        parts = list.split(/\s*\|\s*/).map(s => s.trim()).filter(Boolean);
    }
    if (parts.length <= 1) {
        parts = [];
        const bySep = list.split(/\s*[\/·]\s*/).map(s => s.trim()).filter(Boolean);
        if (bySep.length > 1) {
            parts = bySep;
        } else {
            const byNum = list.split(/(?=\d+\.)/).map(s => s.replace(/^\d+\.\s*/, '').trim()).filter(Boolean);
            if (byNum.length > 1) {
                parts = byNum;
            } else {
                const byComma = list.split(/[,，、]\s*/).map(s => s.trim()).filter(Boolean);
                if (byComma.length > 1) {
                    parts = byComma;
                } else {
                    parts = [list];
                }
            }
        }
    }

    // 3. Map to {title, desc} if a colon is present
    return parts.map(part => {
        if (typeof part !== 'string') return part;
        const colonMatch = part.match(/^([^:：]+)[:：]\s*(.+)$/);
        if (colonMatch) {
            return {
                title: colonMatch[1].trim(),
                desc: colonMatch[2].trim()
            };
        }
        return part;
    });
}

/**
 * 解析 Comparison 数据
 * 支持 "正面: A/B/C vs 反面: D/E/F" 格式
 */
function parseComparisonData(list) {
    if (typeof list !== 'string') return null;
    const vsMatch = list.match(/^(.+?)(?:\s+vs\s+|\s*\|\s*)(.+)$/i);
    if (!vsMatch) return null;

    function parseSide(str) {
        const colonMatch = str.match(/^([^:：]+)[:：]\s*(.+)$/);
        if (colonMatch) {
            return {
                label: colonMatch[1].trim(),
                items: colonMatch[2].split(/[\/,，、]/).map(s => s.trim()).filter(Boolean),
            };
        }
        return { label: '', items: str.split(/[\/,，、]/).map(s => s.trim()).filter(Boolean) };
    }

    return { left: parseSide(vsMatch[1]), right: parseSide(vsMatch[2]) };
}

module.exports = {
    cardShadow,
    fitImage,
    extractTitle,
    adaptiveTitleSize,
    sceneSummary,
    getC,
    parseListString,
    parseComparisonData,
};
