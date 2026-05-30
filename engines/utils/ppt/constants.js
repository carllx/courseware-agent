/**
 * ppt/constants.js — PPT 布局引擎常量与映射表
 *
 * 集中管理幻灯片尺寸、视频扩展名、弃用别名、
 * 活动图标和叙事标签样式等全局常量。
 */

// ============================================================
// 幻灯片尺寸常量
// ============================================================
const CW = 10.0;   // Slide Width (inches)
const CH = 5.625;   // Slide Height (inches, 16:9)
const MARGIN = 0.6;

// ============================================================
// 视频扩展名
// ============================================================
const VIDEO_EXTS = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv'];

// ============================================================
// 弃用别名 → 正式标签映射
// ============================================================
const DEPRECATED_ALIASES = {
    'card': 'grid',
    'cards': 'grid',
    'full screen': 'full',
    'codeblock': 'code',
    'three-column': 'grid',
    'triple-column': 'grid',
    'quadrant': 'grid',
    'flow': 'timeline',
    'canvas': 'grid',
    'chat-bubble': 'split',
    'template-card': 'grid',
    'spectrum': 'diagram',
    'text': 'list',
    'chart': 'image',
    'video': 'full',
    'scene': 'image',
    'checklist': 'list',
    'process': 'timeline',
};

// ============================================================
// Activity Type → 图标映射表
// ============================================================
const ACTIVITY_ICONS = {
    'warm-up': '🎯',
    'qa': '❓',
    'practice': '🔧',
    'workshop': '🔨',
    'discussion': '💬',
    'quiz': '📝',
    'demo': '🖥️',
};
const ACTIVITY_ICON_DEFAULT = '📌';

// ============================================================
// Oral Tag → 图标 + 色调映射表
// ============================================================
const ORAL_TAG_STYLE = {
    'STORY TIME':       { icon: '📖', colorKey: 'primary' },
    'CASE STUDY':       { icon: '📋', colorKey: 'secondary' },
    'TEACHING MOMENT':  { icon: '💡', colorKey: 'tertiary' },
    'PHILOSOPHY':       { icon: '🧠', colorKey: 'primary_light' },
    'LIFE CONNECT':     { icon: '🌏', colorKey: 'secondary' },
    'DID YOU KNOW':     { icon: '🔍', colorKey: 'text_muted' },
};

// ============================================================
// F-10: 面包屑豁免集 — 全幅视觉冲击页免除面包屑干扰
// 新增全幅布局时只需在此添加，无需修改 dispatcher.js
// ============================================================
const NO_BREADCRUMB = new Set(['title', 'section', 'cta', 'quote']);

// ============================================================
// F-11: 布局坐标常量 — 消除跨模块 magic number 重复
// ============================================================
const LAYOUT = {
    RIGHT_PANE_X: 5.2,         // 右侧图片/内容区起始 x
    RIGHT_PANE_MAX_W: 4.4,     // 右侧图片最大宽度
    RIGHT_PANE_MAX_H: 4.6,     // 右侧图片最大高度
    LEFT_TEXT_W: 4.2,           // 左侧文字区宽度
    DUAL_IMG_MAX_W: 4.2,       // 双图模式单图最大宽度
    DUAL_IMG_MAX_H: 4.0,       // 双图模式单图最大高度
    CENTER_IMG_MAX_W: 8.0,     // 居中大图最大宽度
    CENTER_IMG_MAX_H: 3.8,     // 居中大图最大高度
    CARD_GAP: 0.35,            // 卡片间距
    TITLE_Y: 0.35,             // 标题 y 坐标
    TITLE_H: 0.55,             // 标题高度
    CONTENT_Y: 1.1,            // 主内容区起始 y
    FOOTER_Y: CH - 0.6,        // 底部注释 y 坐标
};

module.exports = {
    CW,
    CH,
    MARGIN,
    VIDEO_EXTS,
    DEPRECATED_ALIASES,
    ACTIVITY_ICONS,
    ACTIVITY_ICON_DEFAULT,
    ORAL_TAG_STYLE,
    NO_BREADCRUMB,
    LAYOUT,
};
