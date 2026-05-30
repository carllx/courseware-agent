/**
 * ppt/renderers_internal.js — 内部标签类布局渲染器
 *
 * 包含解析器自动生成的内部 Slide 类型：
 * - renderActivity: 活动指引页
 * - renderOralTag: 叙事标签提示页
 *
 * 这些布局由 [ACTIVITY] / [STORY TIME] 等标签自动触发，
 * 不走常规资产解析流程。
 */
const { CW, CH, MARGIN, ACTIVITY_ICONS, ACTIVITY_ICON_DEFAULT, ORAL_TAG_STYLE } = require('./constants');
const { getC } = require('./data_utils');

// ============================================================
// renderActivity — 活动指引页
// ============================================================

/**
 * renderActivity — 活动指引页
 * 暖色底 + 大图标 + 活动名称 + 类型/时长标签
 * 用于在 PPT 中标记课堂活动节点，提醒教师切换到互动模式
 */
function renderActivity(ctx) {
    const { pres, slide, theme, visual } = ctx;
    const F = theme.FONT;

    // 暖色背景（使用较浅的暖色调）
    const bgColor = getC(theme, 'bg_warm', getC(theme, 'bg_surface', 'FFF8F0'));
    slide.background = { color: bgColor };

    // 顶部强调色条
    slide.addShape(pres.shapes.RECTANGLE, {
        x: 0, y: 0, w: CW, h: 0.08,
        fill: { color: getC(theme, 'tertiary', getC(theme, 'warning', 'E8A838')) },
    });

    // 大图标
    const actType = (visual.activityType || '').toLowerCase();
    const icon = ACTIVITY_ICONS[actType] || ACTIVITY_ICON_DEFAULT;
    slide.addText(icon, {
        x: (CW - 2) / 2, y: 0.8, w: 2.0, h: 1.6,
        fontSize: 72, align: 'center', valign: 'middle',
    });

    // 类型 + 时长标签（右上角胶囊）
    const typeBadge = [visual.activityType || 'Activity'];
    if (visual.activityDuration) typeBadge.push(visual.activityDuration);
    const badgeText = typeBadge.join(' · ');

    // 胶囊背景
    const badgeW = Math.max(2.0, badgeText.length * 0.18 + 0.6);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: CW - badgeW - MARGIN, y: 0.3, w: badgeW, h: 0.45,
        fill: { color: getC(theme, 'tertiary', getC(theme, 'warning', 'E8A838')) },
        rectRadius: 0.15,
    });
    slide.addText(badgeText, {
        x: CW - badgeW - MARGIN, y: 0.3, w: badgeW, h: 0.45,
        fontSize: 14, fontFace: F.title, color: getC(theme, 'text_on_dark', 'FFFFFF'),
        bold: true, align: 'center', valign: 'middle', margin: 0,
    });

    // 活动名称（主标题），去除 markdown 加粗符号
    let actTitle = visual.activityDesc || visual.heading || '课堂活动';
    if (typeof actTitle === 'string') {
        actTitle = actTitle.replace(/\*\*/g, '').replace(/__/g, '');
    }
    slide.addText(actTitle, {
        x: MARGIN + 0.5, y: 2.6, w: CW - MARGIN * 2 - 1.0, h: 1.2,
        fontSize: actTitle.length > 20 ? 22 : 28,
        fontFace: F.title, color: getC(theme, 'text_main', '2D2926'),
        bold: true, align: 'center', valign: 'middle', margin: 0,
    });

    // 底部分隔线 + 上下文标记
    slide.addShape(pres.shapes.RECTANGLE, {
        x: CW / 2 - 1.5, y: 4.2, w: 3.0, h: 0.03,
        fill: { color: getC(theme, 'border', 'D6CFC7') },
    });

    // 底部上下文：所属章节
    const context = visual.h3 || visual.h2 || '';
    if (context) {
        slide.addText(context, {
            x: MARGIN, y: 4.5, w: CW - MARGIN * 2, h: 0.4,
            fontSize: 12, fontFace: F.body, italic: true,
            color: getC(theme, 'text_muted', 'AAAAAA'),
            align: 'center',
        });
    }
}

// ============================================================
// renderOralTag — 叙事标签提示页
// ============================================================

/**
 * renderOralTag — 叙事标签提示页
 * 深色底 + 左侧色条 + 标签图标 + 主题标题
 * 用于在 PPT 中标记故事/案例/金句等口头叙事节点
 */
function renderOralTag(ctx) {
    const { pres, slide, theme, visual } = ctx;
    const F = theme.FONT;

    // 深色背景
    slide.background = { color: getC(theme, 'bg_dark', '1A1A1A') };

    // 获取标签样式
    const tagName = visual.tagName || 'TEACHING MOMENT';
    const style = ORAL_TAG_STYLE[tagName] || { icon: '📌', colorKey: 'primary' };
    const accentColor = getC(theme, style.colorKey, getC(theme, 'primary', 'B85042'));

    // 左侧竖条装饰
    slide.addShape(pres.shapes.RECTANGLE, {
        x: 0, y: 0, w: 0.12, h: CH,
        fill: { color: accentColor },
    });

    // 标签类型名 + 图标（上方）
    const tagLabel = `${style.icon}  ${tagName}`;
    slide.addText(tagLabel, {
        x: MARGIN + 0.3, y: 1.2, w: CW - MARGIN * 2, h: 0.6,
        fontSize: 18, fontFace: F.body, color: accentColor,
        bold: true, align: 'left', valign: 'middle', margin: 0,
    });

    // 顶部细线（标签色）
    slide.addShape(pres.shapes.RECTANGLE, {
        x: MARGIN + 0.3, y: 1.85, w: 3.0, h: 0.04,
        fill: { color: accentColor },
    });

    // 标签标题（主题）
    const tagTitle = visual.tagTitle || visual.heading || tagName;
    const titleSize = tagTitle.length > 25 ? 26 : 32;
    slide.addText(tagTitle, {
        x: MARGIN + 0.3, y: 2.1, w: CW - MARGIN * 2 - 0.6, h: 1.8,
        fontSize: titleSize, fontFace: F.title,
        color: getC(theme, 'text_on_dark', 'FFFFFF'),
        bold: true, align: 'left', valign: 'top', margin: 0,
    });

    // 底部上下文：所属章节
    const context = visual.h3 || visual.h2 || '';
    if (context) {
        slide.addText(context, {
            x: MARGIN + 0.3, y: CH - 0.8, w: CW - MARGIN * 2, h: 0.4,
            fontSize: 12, fontFace: F.body, italic: true,
            color: getC(theme, 'text_muted', '888888'),
            align: 'left',
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
    '_activity':  renderActivity,
    '_oral_tag':  renderOralTag,
};

module.exports = { LAYOUT_ENTRIES, renderActivity, renderOralTag };
