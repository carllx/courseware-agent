/**
 * ppt/renderers_media.js — 媒体展示类布局渲染器
 *
 * 包含以图片/视觉素材展示为核心的布局：
 * - renderSplit: 左文右图 / 双图 Split
 * - renderImage: 居中大图
 * - renderDiagram: 左文右图 + 步骤列表
 */
const fs = require('fs');
const { CW, CH, MARGIN, LAYOUT } = require('./constants');
const {
    fitImage,
    extractTitle,
    adaptiveTitleSize,
    sceneSummary,
    getC,
    parseListString,
} = require('./data_utils');

// ============================================================
// renderSplit — 左文右图布局 (v2: 方向修正)
// ============================================================

/**
 * renderSplit — 左文右图布局
 * 标题在左上、要点/文字在左侧、大图在右侧
 *
 * v3: 双图 Split 模式 — 当有 ≥2 张图片时，左右各放一张图
 */
function renderSplit(ctx) {
    const { slide, theme, visual, assetPath, assetPaths } = ctx;
    const F = theme.FONT;

    // ─── 双图 Split 模式 ───
    if (assetPaths && assetPaths.length >= 2) {
        const title = extractTitle(visual);

        // 顶部居中标题
        if (title) {
            slide.addText(title, {
                x: MARGIN, y: LAYOUT.TITLE_Y, w: CW - MARGIN * 2, h: LAYOUT.TITLE_H,
                fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main', '2D2926'),
                bold: true, margin: 0, align: 'center',
            });
        }

        // 左右两张图，各占约 45%
        const imgMaxW = LAYOUT.DUAL_IMG_MAX_W;
        const imgMaxH = LAYOUT.DUAL_IMG_MAX_H;
        const imgY0 = LAYOUT.CONTENT_Y;
        const panePositions = [
            { x: 0.3 },        // 左侧
            { x: CW / 2 + 0.1 }, // 右侧
        ];

        assetPaths.slice(0, 2).forEach((ap, i) => {
            const { w: finalW, h: finalH } = fitImage(ap, imgMaxW, imgMaxH);
            const paneX = panePositions[i].x;
            const centeredX = paneX + (imgMaxW - finalW) / 2;
            const centeredY = imgY0 + (imgMaxH - finalH) / 2;
            slide.addImage({ path: ap, x: centeredX, y: centeredY, w: finalW, h: finalH });
        });

        // 中间分割线装饰
        slide.addShape(ctx.pres.shapes.RECTANGLE, {
            x: CW / 2 - 0.02, y: 1.2, w: 0.04, h: 3.8,
            fill: { color: getC(theme, 'border', 'D6CFC7') },
        });

        return;
    }

    // ─── 单图模式（原有逻辑） ───

    // ─── 左侧：文字区域 ───
    const textW = 4.2;
    let y = 0.4;

    // 标题
    const title = extractTitle(visual);
    if (title) {
        slide.addText(title, {
            x: MARGIN, y: y, w: textW, h: 0.6,
            fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main', '2D2926'),
            bold: true, margin: 0,
        });
        y += 0.9;
    }

    // 列表内容（如果有结构化 list）
    const items = parseListString(visual.list);
    if (items.length > 0) {
        items.forEach((item, i) => {
            if (y + 0.5 > CH - 0.3) return; // 溢出防护
            const text = typeof item === 'string' ? item : (item.title + (item.desc ? ': ' + item.desc : ''));
            slide.addText(text, {
                x: MARGIN, y: y, w: textW, h: 0.5,
                fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
                bullet: true, valign: 'top',
            });
            y += 0.55;
        });
    } else if (visual.text && visual.headline) {
        // 如果同时有 headline(作了标题) 和 text(没作标题)，则把 text 当正文
        slide.addText(visual.text.replace(/\\n/g, '\n'), {
            x: MARGIN, y: y, w: textW, h: CH - y - 0.3,
            fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
            valign: 'top',
        });
    }

    // ─── 右侧：图片 ───
    if (assetPath) {
        const maxW = LAYOUT.RIGHT_PANE_MAX_W;
        const maxH = LAYOUT.RIGHT_PANE_MAX_H;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = LAYOUT.RIGHT_PANE_X + (maxW - finalW) / 2;
        const imgY = 0.5 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: imgY, w: finalW, h: finalH });
    }
}

// ============================================================
// renderImage — 居中大图布局
// ============================================================

/**
 * renderImage — 居中大图布局
 */
function renderImage(ctx) {
    const { slide, theme, visual, assetPath, assetPaths } = ctx;
    const F = theme.FONT;

    // 多图防御警告：Image 布局仅展示首图，多余资产被静默丢弃
    if (assetPaths && assetPaths.length > 1) {
        console.warn(`⚠️  [renderImage] Layout:Image 仅支持单图，但收到 ${assetPaths.length} 张。丢弃第 2+ 张。建议改用 Layout: Grid。 (Slide: ${visual.slide || '?'})`);
    }

    // 标题
    const title = extractTitle(visual);
    if (title) {
        slide.addText(title, {
            x: MARGIN, y: 0.4, w: CW - MARGIN * 2, h: 0.5,
            fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
            bold: true, margin: 0,
        });
    }

    // 居中大图
    if (assetPath) {
        const maxW = LAYOUT.CENTER_IMG_MAX_W;
        const maxH = LAYOUT.CENTER_IMG_MAX_H;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = (CW - finalW) / 2;
        const y = LAYOUT.CONTENT_Y + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
    }

    // 底部说明
    const caption = visual.caption || sceneSummary(visual.scene, 80);
    if (caption) {
        slide.addText(caption, {
            x: MARGIN, y: LAYOUT.FOOTER_Y, w: CW - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
            align: 'center',
        });
    }
}

// ============================================================
// renderDiagram — 左文右图 + 序号步骤列表
// ============================================================

/**
 * renderDiagram — 左文右图 + 序号步骤列表
 * v2: 反转为左文右图（与 Split 一致方向）
 */
function renderDiagram(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const F = theme.FONT;

    // 多图防御警告：Diagram 布局仅展示首图
    if (assetPaths && assetPaths.length > 1) {
        console.warn(`⚠️  [renderDiagram] Layout:Diagram 仅支持单图，但收到 ${assetPaths.length} 张。丢弃第 2+ 张。建议改用 Layout: Grid。 (Slide: ${visual.slide || '?'})`);
    }

    // 标题
    const title = extractTitle(visual);
    if (title) {
        slide.addText(title, {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
            bold: true, margin: 0,
        });
    }

    // ─── 左侧列表/文字 ───
    const items = parseListString(visual.list);
    if (items.length > 0) {
        const itemSpacing = Math.min(1.2, (CH - 1.6) / Math.max(items.length, 1));
        let startY = 1.2;

        items.forEach((item, i) => {
            if (startY + 0.4 > CH - 0.2) return;

            const itemTitle = typeof item === 'string' ? item : item.title;
            const itemDesc = typeof item === 'string' ? '' : (item.desc || '');

            // 左侧色条标记
            slide.addShape(pres.shapes.RECTANGLE, {
                x: MARGIN, y: startY, w: 0.08, h: itemSpacing * 0.75,
                fill: { color: i === 0 ? getC(theme, 'primary') : (i === 1 ? getC(theme, 'tertiary', getC(theme, 'warning')) : getC(theme, 'text_muted')) },
            });

            slide.addText(itemTitle, {
                x: MARGIN + 0.2, y: startY, w: 3.8, h: 0.4,
                fontSize: 18, fontFace: F.title, color: getC(theme, 'text_main'),
                bold: true, margin: 0,
            });
            if (itemDesc) {
                slide.addText(itemDesc, {
                    x: MARGIN + 0.2, y: startY + 0.4, w: 3.8, h: 0.35,
                    fontSize: 13, fontFace: F.body, color: getC(theme, 'text_secondary'),
                    margin: 0,
                });
            }
            startY += itemSpacing;
        });
    } else if (visual.text && visual.headline) {
        // 如果 text 没有被用作标题，则显示为左侧正文
        slide.addText(visual.text.replace(/\\n/g, '\n'), {
            x: MARGIN, y: 1.2, w: 4.3, h: 3.8,
            fontSize: 14, fontFace: F.body, color: getC(theme, 'text_secondary'),
            valign: 'top',
        });
    }

    // ─── 右侧图片 ───
    if (assetPath) {
        const maxW = LAYOUT.RIGHT_PANE_MAX_W;
        const maxH = LAYOUT.RIGHT_PANE_MAX_H;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = LAYOUT.RIGHT_PANE_X + (maxW - finalW) / 2;
        const y = 0.5 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
    }
}

// ============================================================
// Layout 注册表
// ============================================================

/**
 * 本模块负责的布局类型 → 渲染函数映射
 */
const LAYOUT_ENTRIES = {
    'split':      renderSplit,
    'image':      renderImage,
    'full':       renderImage,
    'screenshot': renderImage,
    'diagram':    renderDiagram,
    'timeline':   renderDiagram,
    'code':       renderSplit,
    'poll':       renderImage,
};

module.exports = { LAYOUT_ENTRIES, renderSplit, renderImage, renderDiagram };
