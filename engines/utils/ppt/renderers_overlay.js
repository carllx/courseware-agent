/**
 * ppt/renderers_overlay.js — 覆盖层/特殊页面类布局渲染器
 *
 * 包含全幅覆盖或特殊视觉效果的布局：
 * - renderTitle: 暗色全幅封面页
 * - renderCTA: 暗色收尾页
 * - renderQuote: 金句卡片
 * - renderVideoSlide: 视频嵌入专用
 */
const path = require('path');
const fs = require('fs');
const { CW, CH, MARGIN } = require('./constants');
const {
    fitImage,
    extractTitle,
    adaptiveTitleSize,
    sceneSummary,
    getC,
    parseListString,
} = require('./data_utils');

// ============================================================
// renderTitle — 暗色全幅封面页
// ============================================================

/**
 * renderTitle — 暗色全幅封面页
 * 暗底 + 顶部装饰条 + 主标题 + 副标题 + 底部学期信息
 */
function renderTitle(ctx) {
    const { pres, slide, theme, visual } = ctx;
    const F = theme.FONT;

    // 暗色背景
    slide.background = { color: getC(theme, 'bg_dark', getC(theme, 'bg_base')) };

    // 顶部装饰条
    slide.addShape(pres.shapes.RECTANGLE, {
        x: 0, y: 0, w: CW, h: 0.06,
        fill: { color: getC(theme, 'primary', 'B85042') },
    });

    const title = extractTitle(visual);

    // 上方小标签：用 Slide 名称或周次信息（不用 Scene，Scene 是生图描述）
    const slideId = visual.slide || '';
    const weekMatch = slideId.match(/^W(\d+)/);
    const topLabel = (slideId && slideId !== title) ? slideId : (weekMatch ? `W${weekMatch[1]}` : '');
    if (topLabel) {
        slide.addText(topLabel, {
            x: MARGIN, y: 1.4, w: CW - MARGIN * 2, h: 0.5,
            fontSize: 16, fontFace: F.body, color: getC(theme, 'text_muted'),
            align: 'left',
        });
    }

    // 主标题
    slide.addText(title || 'Title', {
        x: MARGIN, y: 1.9, w: CW - MARGIN * 2, h: 1.2,
        fontSize: 44, fontFace: F.title, color: getC(theme, 'text_on_dark', getC(theme, 'text_main')),
        bold: true, align: 'left', margin: 0,
    });

    // 副标题——仅当有显式 headline/text（非 scene）且不同于主标题时展示
    const subtitle = visual.headline || visual.text || '';
    if (subtitle && subtitle !== title) {
        slide.addText(subtitle, {
            x: MARGIN, y: 3.2, w: CW - MARGIN * 2, h: 0.5,
            fontSize: 14, fontFace: F.body, color: getC(theme, 'primary_light', getC(theme, 'primary')),
            align: 'left',
        });
    }

    // 底部信息
    slide.addText('Presentation', {
        x: MARGIN, y: CH - 0.8, w: CW - MARGIN * 2, h: 0.4,
        fontSize: 12, fontFace: F.body, color: getC(theme, 'text_muted'),
        align: 'left',
    });
}

// ============================================================
// renderCTA — 暗色收尾页
// ============================================================

/**
 * renderCTA — 暗色收尾页 (v2 新增)
 * 暗底 + 顶部装饰条 + 总结要点列表 + 水平分隔线 + 课后任务
 */
function renderCTA(ctx) {
    const { pres, slide, theme, visual } = ctx;
    const F = theme.FONT;

    // 暗色背景
    slide.background = { color: getC(theme, 'bg_dark', getC(theme, 'bg_base')) };

    // 顶部装饰条
    slide.addShape(pres.shapes.RECTANGLE, {
        x: 0, y: 0, w: CW, h: 0.06,
        fill: { color: getC(theme, 'primary') },
    });

    // 标题
    const title = extractTitle(visual) || '课堂总结';
    slide.addText(title, {
        x: MARGIN, y: 0.6, w: CW - MARGIN * 2, h: 0.7,
        fontSize: 36, fontFace: F.title, color: getC(theme, 'text_on_dark', getC(theme, 'text_main')),
        bold: true, margin: 0,
    });

    // 要点列表
    const items = parseListString(visual.list);
    if (items.length > 0) {
        let y = 1.5;
        items.forEach(item => {
            if (y + 0.4 > CH - 0.8) return;
            const text = typeof item === 'string' ? item : (item.title + (item.desc ? ': ' + item.desc : ''));
            slide.addText(text, {
                x: MARGIN, y: y, w: CW - MARGIN * 2, h: 0.4,
                fontSize: 16, fontFace: F.body, color: getC(theme, 'text_on_dark', getC(theme, 'text_main')),
                bullet: true, valign: 'top',
            });
            y += 0.5;
        });
    }

    // 场景/课后任务
    if (visual.scene) {
        // 分隔线
        slide.addShape(pres.shapes.RECTANGLE, {
            x: MARGIN, y: 4.3, w: CW - MARGIN * 2, h: 0.04,
            fill: { color: getC(theme, 'primary'), transparency: 50 },
        });
        slide.addText(visual.scene, {
            x: MARGIN, y: 4.5, w: CW - MARGIN * 2, h: 0.5,
            fontSize: 14, fontFace: F.body, color: getC(theme, 'primary_light', getC(theme, 'primary')),
            margin: 0,
        });
    }
}

// ============================================================
// renderQuote — 金句卡片布局
// ============================================================

/**
 * renderQuote — 金句卡片布局
 */
function renderQuote(ctx) {
    const { slide, theme, visual } = ctx;
    const F = theme.FONT;

    // 装饰性大引号
    slide.addText('"', {
        x: 0.8, y: 0.3, w: 2.0, h: 2.0,
        fontSize: 120, color: getC(theme, 'primary_muted', getC(theme, 'primary')),
        fontFace: 'Georgia', bold: true,
        transparency: 60,
    });

    // 引文
    const quoteText = visual.quote || visual.text || visual.headline || '';
    slide.addText(quoteText, {
        x: 1.2, y: 1.5, w: 7.5, h: 2.5,
        fontSize: 24, fontFace: F.body, color: getC(theme, 'text_main'),
        italic: true, valign: 'middle',
    });

    // 署名
    if (visual.scene) {
        slide.addText(`— ${visual.scene}`, {
            x: 1.2, y: 4.2, w: 7.5, h: 0.5,
            fontSize: 14, fontFace: F.body, color: getC(theme, 'text_muted'),
            align: 'right',
        });
    }
}

// ============================================================
// renderVideoSlide — 视频嵌入专用布局
// ============================================================

/**
 * renderVideoSlide — 视频嵌入专用布局
 * 使用 PptxGenJS addMedia() 嵌入 MP4 视频，poster 作为封面
 *
 * ⚠️ 特殊调用路径：本函数不通过 LAYOUT_ENTRIES 自动注册，
 *    而是由 dispatcher.js 在检测到视频资产并完成转码后直接调用。
 *    因此不受 layout 字符串分发机制控制。
 */
function renderVideoSlide(ctx) {
    const { pres, slide, theme, visual, assetPath, mp4Path } = ctx;
    const F = theme.FONT;

    // 标题
    const title = extractTitle(visual);
    if (title) {
        slide.addText(title, {
            x: MARGIN, y: 0.3, w: CW - MARGIN * 2, h: 0.5,
            fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main'),
            bold: true, margin: 0,
        });
    }

    // 视频嵌入区域（居中放置）
    const videoX = 0.8;
    const videoY = title ? 1.0 : 0.5;
    const videoW = CW - 1.6;
    const videoH = title ? 3.8 : 4.5;

    try {
        const mediaOpts = {
            type: 'video',
            path: mp4Path,
            x: videoX, y: videoY, w: videoW, h: videoH,
        };
        // 若有 poster，转为 base64 data URI 设为封面图
        // PptxGenJS addMedia cover 要求 data URI 格式: 'data:image/png;base64,...'
        if (assetPath && fs.existsSync(assetPath)) {
            try {
                const posterBuffer = fs.readFileSync(assetPath);
                const ext = path.extname(assetPath).toLowerCase().replace('.', '');
                const mimeType = ext === 'jpg' ? 'jpeg' : ext;
                mediaOpts.cover = `data:image/${mimeType};base64,${posterBuffer.toString('base64')}`;
            } catch (coverErr) {
                console.warn(`   ⚠️  [PPTX] poster base64 编码失败: ${coverErr.message}`);
            }
        }
        slide.addMedia(mediaOpts);
        console.log(`   🎥 [PPTX] 已嵌入视频: ${path.basename(mp4Path)}`);
    } catch (e) {
        // addMedia 失败时回退到 poster 图片
        console.warn(`   ⚠️  [PPTX] addMedia 失败 (${path.basename(mp4Path)}): ${e.message}`);
        if (assetPath && fs.existsSync(assetPath)) {
            const { w: finalW, h: finalH } = fitImage(assetPath, videoW, videoH);
            const imgX = videoX + (videoW - finalW) / 2;
            const imgY = videoY + (videoH - finalH) / 2;
            slide.addImage({ path: assetPath, x: imgX, y: imgY, w: finalW, h: finalH });
        }
    }

    // 底部说明（时长 + 字幕信息）
    const duration = visual.duration || '';
    const captionParts = [visual.caption || sceneSummary(visual.scene, 60)];
    if (duration) captionParts.push(`⏱ ${duration}`);
    const captionText = captionParts.filter(Boolean).join('  |  ');
    if (captionText) {
        slide.addText(captionText, {
            x: MARGIN, y: CH - 0.55, w: CW - MARGIN * 2, h: 0.3,
            fontSize: 12, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
            align: 'center',
        });
    }
}

// ============================================================
// Layout 注册表
// ============================================================

/**
 * 本模块负责的布局类型 → 渲染函数映射
 */
const LAYOUT_ENTRIES = {
    'title':   renderTitle,
    'section': renderTitle,
    'stat':    renderTitle,
    'cta':     renderCTA,
    'quote':   renderQuote,
};

module.exports = { LAYOUT_ENTRIES, renderTitle, renderCTA, renderQuote, renderVideoSlide };
