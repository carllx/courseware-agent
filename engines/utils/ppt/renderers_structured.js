/**
 * ppt/renderers_structured.js — 结构化数据类布局渲染器
 *
 * 包含以列表/卡片/对比等结构化数据展示为核心的布局：
 * - renderList: 编号圆形 + 左图右列表
 * - renderGrid: 卡片网格（Multi-Image / Editorial Split / 纯卡片）
 * - renderComparison: 双栏对比（含溢出切页 + 双图续页）
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
    parseComparisonData,
    cardShadow,
} = require('./data_utils');

// ============================================================
// renderList — 编号圆形 + 左图右列表布局
// ============================================================

/**
 * renderList — 编号圆形 + 左图右列表布局
 * v2: 添加编号圆形标记（而非纯 bullet）
 */
function renderList(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const F = theme.FONT;

    // 多图防御警告：List 布局仅展示首图
    if (assetPaths && assetPaths.length > 1) {
        console.warn(`⚠️  [renderList] Layout:List 仅支持单图，但收到 ${assetPaths.length} 张。丢弃第 2+ 张。建议改用 Layout: Grid。 (Slide: ${visual.slide || '?'})`);
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

    // 列表内容
    const items = parseListString(visual.list);

    if (items.length > 0) {
        const itemSpacing = Math.min(1.0, (CH - 1.6) / Math.max(items.length, 1));
        let y = 1.3;

        items.forEach((item, i) => {
            if (y + 0.5 > CH - 0.2) return; // 溢出防护

            const itemTitle = typeof item === 'string' ? item : item.title;
            const itemDesc = typeof item === 'string' ? '' : (item.desc || '');

            // 纯净圆点（不含序号文字）
            slide.addShape(pres.shapes.OVAL, {
                x: MARGIN + 0.15, y: y + 0.1, w: 0.15, h: 0.15,
                fill: { color: getC(theme, 'primary') },
            });

            // 标题
            slide.addText(itemTitle, {
                x: MARGIN + 0.6, y: y, w: 3.5, h: 0.35,
                fontSize: 18, fontFace: F.title, color: getC(theme, 'text_main'),
                bold: true, margin: 0,
            });

            // 描述
            if (itemDesc) {
                slide.addText(itemDesc, {
                    x: MARGIN + 0.6, y: y + 0.35, w: 3.5, h: 0.3,
                    fontSize: 14, fontFace: F.body, color: getC(theme, 'text_secondary'),
                    margin: 0,
                });
            }

            y += itemSpacing;
        });
    }

    // 右侧 Asset
    if (assetPath) {
        const maxW = LAYOUT.RIGHT_PANE_MAX_W;
        const maxH = 4.2;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = LAYOUT.RIGHT_PANE_X + (maxW - finalW) / 2;
        const y = 0.8 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
    }
}

// ============================================================
// renderGrid — 卡片网格布局
// ============================================================

/**
 * renderGrid — 卡片网格布局
 * v3: 消除图/卡零和博弈，支持 Editorial Split（左图右卡共生）
 */
function renderGrid(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const F = theme.FONT;

    // 标题
    const title = extractTitle(visual);
    if (title) {
        slide.addText(title, {
            x: MARGIN, y: 0.35, w: CW - MARGIN * 2, h: 0.55,
            fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
            bold: true, margin: 0,
        });
    }

    // 解析 list
    const items = parseListString(visual.list);
    const imgs = (assetPaths && assetPaths.length > 0) ? assetPaths : (assetPath ? [assetPath] : []);

    // 无图无文守卫：避免生成空白 Slide
    if (items.length === 0 && imgs.length === 0) {
        if (visual.scene) {
            slide.addText(visual.scene, {
                x: MARGIN, y: 1.0, w: CW - MARGIN * 2, h: 3.5,
                fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
                valign: 'top',
            });
        }
        return;
    }

    // ─── Multi-Image Grid 模式：多图文卡片网格 ───
    if (imgs.length > 1) {
        const count = Math.max(imgs.length, items.length);
        const cols = count <= 3 ? count : (count === 4 ? 2 : 3);
        const rows = Math.ceil(count / cols);

        const cardW = (CW - MARGIN * 2 - LAYOUT.CARD_GAP * (cols - 1)) / cols;
        const gridY = LAYOUT.CONTENT_Y;
        const gridH = CH - gridY - 0.8;
        const cardH = (gridH - LAYOUT.CARD_GAP * (rows - 1)) / rows;
        const startX = (CW - (cardW * cols + LAYOUT.CARD_GAP * (cols - 1))) / 2;

        const accents = [
            getC(theme, 'primary'),
            getC(theme, 'tertiary', getC(theme, 'warning')),
            getC(theme, 'secondary', getC(theme, 'success')),
            getC(theme, 'primary_light', getC(theme, 'primary')),
        ];

        for (let i = 0; i < count; i++) {
            const col = i % cols;
            const row = Math.floor(i / cols);
            const cx = startX + col * (cardW + LAYOUT.CARD_GAP);
            const cy = gridY + row * (cardH + LAYOUT.CARD_GAP);

            // 卡片背景
            slide.addShape(pres.shapes.RECTANGLE, {
                x: cx, y: cy, w: cardW, h: cardH,
                fill: { color: getC(theme, 'bg_surface', 'FFFFFF') },
                shadow: cardShadow(),
            });

            let currentY = cy;

            // 1. 图片部分 (占卡片高度的 45%)
            const ap = imgs[i];
            const imgAreaH = cardH * 0.45;
            if (ap && fs.existsSync(ap)) {
                const { w: finalW, h: finalH } = fitImage(ap, cardW, imgAreaH);
                const imgX = cx + (cardW - finalW) / 2;
                const imgY = cy + (imgAreaH - finalH) / 2;
                slide.addImage({ path: ap, x: imgX, y: imgY, w: finalW, h: finalH });
                currentY += imgAreaH;
            } else {
                slide.addShape(pres.shapes.RECTANGLE, {
                    x: cx, y: cy, w: cardW, h: 0.06,
                    fill: { color: accents[i % accents.length] },
                });
                currentY += 0.1;
            }

            // 2. 文字部分
            const item = items[i];
            if (item) {
                const itemTitle = typeof item === 'string' ? item : item.title;
                const itemDesc = typeof item === 'string' ? '' : (item.desc || '');

                slide.addText(itemTitle, {
                    x: cx + 0.15, y: currentY + 0.1, w: cardW - 0.3, h: 0.35,
                    fontSize: 16, fontFace: F.title, color: getC(theme, 'text_main'),
                    bold: true, margin: 0,
                });

                if (itemDesc) {
                    slide.addText(itemDesc, {
                        x: cx + 0.15, y: currentY + 0.45, w: cardW - 0.3, h: cardH - (currentY - cy) - 0.5,
                        fontSize: 13, fontFace: F.body, color: getC(theme, 'text_secondary'),
                        valign: 'top', margin: 0,
                    });
                }
            }
        }

        // 底部注释
        if (visual.scene) {
            const footNote = sceneSummary(visual.scene, 80);
            if (footNote && footNote !== title) {
                slide.addText(footNote, {
                    x: MARGIN, y: CH - 0.6, w: CW - MARGIN * 2, h: 0.35,
                    fontSize: 13, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
                    align: 'center',
                });
            }
        }
        return;
    }

    // ─── 如果只有一张图片，且 items.length 为 0，走全图 ───
    if (items.length === 0 && imgs.length === 1) {
        const ap = imgs[0];
        const maxW = LAYOUT.CENTER_IMG_MAX_W;
        const maxH = LAYOUT.CENTER_IMG_MAX_H;
        const { w: finalW, h: finalH } = fitImage(ap, maxW, maxH);
        const x = (CW - finalW) / 2;
        const y = LAYOUT.CONTENT_Y + (maxH - finalH) / 2;
        slide.addImage({ path: ap, x: x, y: y, w: finalW, h: finalH });
        return;
    }

    // ─── Editorial Split 模式：图+卡共生（单图 + 右侧列表）───
    if (imgs.length === 1 && items.length > 0) {
        const ap = imgs[0];
        const imgW = 4.0;
        const imgMaxH = 4.0;
        const { w: finalW, h: finalH } = fitImage(ap, imgW, imgMaxH);
        const imgX = MARGIN;
        const imgY = 1.1 + (imgMaxH - finalH) / 2;
        slide.addImage({ path: ap, x: imgX, y: imgY, w: finalW, h: finalH });

        // 右侧卡片区：单列纵向排列
        const cardX = MARGIN + imgW + 0.4;
        const cardAreaW = CW - cardX - MARGIN;
        const cardW = cardAreaW;
        const gridY = 1.1;
        const gridH = CH - gridY - 0.3;
        const hasDesc = items.some(item => typeof item !== 'string' && item.desc);
        const cardH = hasDesc ? Math.min(1.6, (gridH - 0.2 * (items.length - 1)) / items.length) : Math.min(1.0, (gridH - 0.2 * (items.length - 1)) / items.length);

        const accents = [
            getC(theme, 'primary'),
            getC(theme, 'tertiary', getC(theme, 'warning')),
            getC(theme, 'secondary', getC(theme, 'success')),
        ];

        items.forEach((item, i) => {
            const cy = gridY + i * (cardH + 0.2);
            if (cy + cardH > CH - 0.1) return; // 溢出防护

            slide.addShape(pres.shapes.RECTANGLE, {
                x: cardX, y: cy, w: cardW, h: cardH,
                fill: { color: getC(theme, 'bg_surface', 'FFFFFF') },
                shadow: cardShadow(),
            });
            slide.addShape(pres.shapes.RECTANGLE, {
                x: cardX, y: cy, w: cardW, h: 0.06,
                fill: { color: accents[i % accents.length] },
            });

            const itemTitle = typeof item === 'string' ? item : item.title;
            const itemDesc = typeof item === 'string' ? '' : (item.desc || '');

            slide.addText(itemTitle, {
                x: cardX + 0.15, y: cy + 0.15, w: cardW - 0.3, h: 0.35,
                fontSize: 16, fontFace: F.title, color: getC(theme, 'text_main'),
                bold: true, margin: 0,
            });
            if (itemDesc) {
                slide.addText(itemDesc, {
                    x: cardX + 0.15, y: cy + 0.5, w: cardW - 0.3, h: cardH - 0.7,
                    fontSize: 13, fontFace: F.body, color: getC(theme, 'text_secondary'),
                    valign: 'top', margin: 0,
                });
            }
        });
        return;
    }

    // ─── 纯卡片网格模式（无图）───
    const count = items.length;
    const cols = count <= 2 ? 2 : (count <= 3 ? 3 : 2);
    const rows = Math.ceil(count / cols);

    const cardW = (CW - MARGIN * 2 - LAYOUT.CARD_GAP * (cols - 1)) / cols;
    const gridY = LAYOUT.CONTENT_Y;
    const gridH = CH - gridY - 0.8;
    // 无 desc 时缩小卡片高度
    const hasDesc = items.some(item => typeof item !== 'string' && item.desc);
    const maxCardH = (gridH - LAYOUT.CARD_GAP * (rows - 1)) / rows;
    const cardH = hasDesc ? maxCardH : Math.min(maxCardH, 1.2);
    const startX = (CW - (cardW * cols + LAYOUT.CARD_GAP * (cols - 1))) / 2;

    // 色调数组
    const accents = [
        getC(theme, 'primary'),
        getC(theme, 'tertiary', getC(theme, 'warning')),
        getC(theme, 'secondary', getC(theme, 'success')),
    ];

    items.forEach((item, i) => {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const cx = startX + col * (cardW + LAYOUT.CARD_GAP);
        const cy = gridY + row * (cardH + LAYOUT.CARD_GAP);

        // 卡片背景（带阴影）
        slide.addShape(pres.shapes.RECTANGLE, {
            x: cx, y: cy, w: cardW, h: cardH,
            fill: { color: getC(theme, 'bg_surface', 'FFFFFF') },
            shadow: cardShadow(),
        });

        // 顶部色条
        slide.addShape(pres.shapes.RECTANGLE, {
            x: cx, y: cy, w: cardW, h: 0.06,
            fill: { color: accents[i % accents.length] },
        });

        const itemTitle = typeof item === 'string' ? item : item.title;
        const itemDesc = typeof item === 'string' ? '' : (item.desc || '');

        // 卡片标题
        slide.addText(itemTitle, {
            x: cx + 0.15, y: cy + 0.2, w: cardW - 0.3, h: 0.4,
            fontSize: 18, fontFace: F.title, color: getC(theme, 'text_main'),
            bold: true, margin: 0,
        });

        // 卡片描述
        if (itemDesc) {
            slide.addText(itemDesc, {
                x: cx + 0.15, y: cy + 0.7, w: cardW - 0.3, h: cardH - 1.0,
                fontSize: 14, fontFace: F.body, color: getC(theme, 'text_secondary'),
                valign: 'top', margin: 0,
            });
        }
    });

    // 底部注释
    if (visual.scene && items.length > 0) {
        const footNote = sceneSummary(visual.scene, 80);
        if (footNote && footNote !== title) {
            slide.addText(footNote, {
                x: MARGIN, y: CH - 0.6, w: CW - MARGIN * 2, h: 0.35,
                fontSize: 13, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
                align: 'center',
            });
        }
    }
}

// ============================================================
// renderComparison — 双栏对比布局
// ============================================================

/**
 * renderComparison — 双栏对比布局 (v3: 支持单图/双图/溢出切页)
 *
 * 策略矩阵（遵循 PPTX 媒介物理约束）：
 *   - 无图：纯双栏对比（原有逻辑）
 *   - 单图：上方主图（1.8" 高）+ 下方双栏下移
 *   - 双图：序列帧化 — 主页为纯文字对比，续页展示双图并排
 *   - 溢出：单列超 6 条时自动生成续页
 */
function renderComparison(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const F = theme.FONT;

    // 标题
    const title = extractTitle(visual);
    if (title) {
        slide.addText(title, {
            x: MARGIN, y: 0.35, w: CW - MARGIN * 2, h: 0.55,
            fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
            bold: true, margin: 0,
        });
    }

    // 解析双栏数据
    const data = parseComparisonData(visual.list);

    if (!data) {
        // Fallback: 如果无法解析为对比格式，退化为 Grid
        renderGrid(ctx);
        return;
    }

    // 判定图片轨道数量
    const imgs = (assetPaths && assetPaths.length > 0) ? assetPaths : (assetPath ? [assetPath] : []);
    const hasOneImg = imgs.length === 1;
    const hasTwoImg = imgs.length >= 2;

    // 布局参数根据图片情况动态调整
    const colW = 4.0;
    const colGap = 0.4;
    const lx = MARGIN;
    const rx = MARGIN + colW + colGap;
    let headerY = 1.1;

    // ─── 单图模式：上方主图 ───
    if (hasOneImg && !hasTwoImg) {
        const imgMaxW = CW - MARGIN * 2;
        const imgMaxH = 1.8;
        const { w: finalW, h: finalH } = fitImage(imgs[0], imgMaxW, imgMaxH);
        const imgX = (CW - finalW) / 2;
        slide.addImage({ path: imgs[0], x: imgX, y: 1.0, w: finalW, h: finalH });
        headerY = 1.0 + finalH + 0.2; // 双栏下移到图片下方
    }

    // 计算内容区可用高度（溢出安全阈值）
    const contentBottom = CH - 0.6; // 为底部注释留白
    const maxItemsPerCol = Math.floor((contentBottom - headerY - 0.6) / 0.5);

    // 分割条目：首页 + 续页
    const leftPage1 = data.left.items.slice(0, maxItemsPerCol);
    const leftOverflow = data.left.items.slice(maxItemsPerCol);
    const rightPage1 = data.right.items.slice(0, maxItemsPerCol);
    const rightOverflow = data.right.items.slice(maxItemsPerCol);

    // ─── 渲染双栏到当前 Slide ───
    _renderComparisonColumns(pres, slide, theme, data, leftPage1, rightPage1, lx, rx, colW, headerY);

    // 底部注释
    if (visual.scene) {
        slide.addText(sceneSummary(visual.scene, 80), {
            x: MARGIN, y: CH - 0.65, w: CW - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
            align: 'center',
        });
    }

    // ─── 溢出续页：条目过多时自动切页 ───
    if (leftOverflow.length > 0 || rightOverflow.length > 0) {
        const overflowSlide = pres.addSlide();
        overflowSlide.background = { color: getC(theme, 'bg_base', 'F5F0EB') };
        // 续页标题
        if (title) {
            overflowSlide.addText(`${title}（续）`, {
                x: MARGIN, y: 0.35, w: CW - MARGIN * 2, h: 0.55,
                fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
                bold: true, margin: 0,
            });
        }
        _renderComparisonColumns(pres, overflowSlide, theme, data, leftOverflow, rightOverflow, lx, rx, colW, 1.1);
        console.log(`   📄 [Comparison] 溢出切页：续页含 ${leftOverflow.length}+${rightOverflow.length} 条目`);
    }

    // ─── 双图续页：序列帧化 ───
    if (hasTwoImg) {
        const imgSlide = pres.addSlide();
        imgSlide.background = { color: getC(theme, 'bg_base', 'F5F0EB') };
        if (title) {
            imgSlide.addText(`${title} — 对比图示`, {
                x: MARGIN, y: 0.35, w: CW - MARGIN * 2, h: 0.55,
                fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
                bold: true, margin: 0,
            });
        }
        // 左图
        const leftImgMaxW = 4.2;
        const leftImgMaxH = 3.8;
        const left = fitImage(imgs[0], leftImgMaxW, leftImgMaxH);
        imgSlide.addImage({ path: imgs[0], x: MARGIN, y: 1.2, w: left.w, h: left.h });
        // 左图标签
        imgSlide.addText(data.left.label || '图 A', {
            x: MARGIN, y: 1.2 + left.h + 0.1, w: leftImgMaxW, h: 0.3,
            fontSize: 12, fontFace: F.body, color: getC(theme, 'secondary', '5B7B6F'),
            align: 'center', bold: true,
        });
        // 右图
        const right = fitImage(imgs[1], leftImgMaxW, leftImgMaxH);
        const rxImg = CW - MARGIN - leftImgMaxW;
        imgSlide.addImage({ path: imgs[1], x: rxImg, y: 1.2, w: right.w, h: right.h });
        // 右图标签
        imgSlide.addText(data.right.label || '图 B', {
            x: rxImg, y: 1.2 + right.h + 0.1, w: leftImgMaxW, h: 0.3,
            fontSize: 12, fontFace: F.body, color: getC(theme, 'primary', 'B85042'),
            align: 'center', bold: true,
        });
        console.log(`   📄 [Comparison] 双图序列帧化：生成对比图续页`);
    }
}

/**
 * 内部辅助：渲染对比双栏（复用于主页和溢出续页）
 *
 * @param {object} pres - PptxGenJS Presentation 实例
 * @param {object} slide - 当前 Slide 对象
 * @param {object} theme - 设计令牌 { C, FONT }
 * @param {{ left: { label: string, items: string[] }, right: { label: string, items: string[] } }} data - 解析后的对比数据
 * @param {string[]} leftItems - 左列当前页条目
 * @param {string[]} rightItems - 右列当前页条目
 * @param {number} lx - 左列 x 坐标
 * @param {number} rx - 右列 x 坐标
 * @param {number} colW - 列宽
 * @param {number} headerY - 标签栏 y 坐标
 */
function _renderComparisonColumns(pres, slide, theme, data, leftItems, rightItems, lx, rx, colW, headerY) {
    const F = theme.FONT;

    // ─── 左列标签（主题色 1）───
    slide.addShape(pres.shapes.RECTANGLE, {
        x: lx, y: headerY, w: colW, h: 0.4,
        fill: { color: getC(theme, 'secondary', getC(theme, 'success', '5B7B6F')) },
    });
    slide.addText(data.left.label || '对比项 A', {
        x: lx, y: headerY, w: colW, h: 0.4,
        fontSize: 14, fontFace: F.title, color: getC(theme, 'text_on_dark', 'FFFFFF'),
        bold: true, align: 'center', valign: 'middle', margin: 0,
    });

    // 左列内容
    let ly = headerY + 0.6;
    leftItems.forEach(item => {
        if (ly + 0.45 > CH - 0.6) return;
        slide.addText(item, {
            x: lx + 0.2, y: ly, w: colW - 0.4, h: 0.45,
            fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
            bullet: true, valign: 'top',
        });
        ly += 0.5;
    });

    // ─── 右列标签（主题色 2）───
    slide.addShape(pres.shapes.RECTANGLE, {
        x: rx, y: headerY, w: colW, h: 0.4,
        fill: { color: getC(theme, 'primary', 'B85042') },
    });
    slide.addText(data.right.label || '对比项 B', {
        x: rx, y: headerY, w: colW, h: 0.4,
        fontSize: 14, fontFace: F.title, color: getC(theme, 'text_on_dark', 'FFFFFF'),
        bold: true, align: 'center', valign: 'middle', margin: 0,
    });

    // 右列内容
    let ry = headerY + 0.6;
    rightItems.forEach(item => {
        if (ry + 0.45 > CH - 0.6) return;
        slide.addText(item, {
            x: rx + 0.2, y: ry, w: colW - 0.4, h: 0.45,
            fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
            bullet: true, valign: 'top',
        });
        ry += 0.5;
    });
}

// ============================================================
// Layout 注册表
// ============================================================

/**
 * 本模块负责的布局类型 → 渲染函数映射
 */
const LAYOUT_ENTRIES = {
    'list':       renderList,
    'icons':      renderList,
    'agenda':     renderList,
    'table':      renderList,
    'workshop':   renderList,
    'grid':       renderGrid,
    'dashboard':  renderGrid,
    'comparison': renderComparison,
};

module.exports = { LAYOUT_ENTRIES, renderList, renderGrid, renderComparison };
