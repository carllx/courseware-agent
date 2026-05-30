/**
 * ppt/dispatcher.js — PPT 布局引擎主分发器
 *
 * 职责：
 * 1. 自动合并所有 renderers_*.js 的 LAYOUT_ENTRIES 构建完整路由表
 * 2. 解析资产路径（多路径候选 + 课程根级 fallback）
 * 3. 触发视频转码 + 嵌入判断
 * 4. 根据 Layout 类型分发到对应渲染函数
 * 5. 注入全局面包屑导航
 */
const path = require('path');
const fs = require('fs');
const { CW, CH, MARGIN, DEPRECATED_ALIASES, NO_BREADCRUMB } = require('./constants');
const { getC, extractTitle } = require('./data_utils');
const { isVideoAsset, extractPosterFrame, convertVideoForPptx } = require('./video');
const { renderVideoSlide } = require('./renderers_overlay');

// ============================================================
// 自动注册：合并所有渲染模块的 LAYOUT_ENTRIES
// ============================================================
const RENDERER_MODULES = [
    require('./renderers_media'),
    require('./renderers_structured'),
    require('./renderers_overlay'),
    require('./renderers_internal'),
];

/**
 * 自动构建的完整布局路由表
 * Key: 布局类型名 (lowercase)
 * Value: 渲染函数引用
 */
const LAYOUT_MAP = {};
for (const mod of RENDERER_MODULES) {
    if (mod.LAYOUT_ENTRIES) {
        // F-9: 键名冲突检测 — 防止两个模块静默覆盖同一 layout key
        for (const key of Object.keys(mod.LAYOUT_ENTRIES)) {
            if (LAYOUT_MAP[key]) {
                console.warn(`⚠️  [PPT Engine] Layout key 冲突: "${key}" 被后加载模块覆盖`);
            }
        }
        Object.assign(LAYOUT_MAP, mod.LAYOUT_ENTRIES);
    }
}

// 默认回退渲染器
const DEFAULT_RENDERER = LAYOUT_MAP['split'];
// F-7: 模块加载异常时提前报错，而非运行时抛出难以诊断的 TypeError
if (!DEFAULT_RENDERER) {
    throw new Error('[PPT Engine] FATAL: renderSplit 未注册到 LAYOUT_MAP，检查 renderers_media.js 是否加载成功');
}

// ============================================================
// 面包屑导航
// ============================================================

/**
 * 方案 A：全局富文本级联面包屑
 * 绘制于页面极右上方，展示绝对空间坐标（并保留完整的章节序列号）
 */
function renderBreadcrumb(slide, theme, visual) {
    if (!visual.h2 && !visual.h3) return;

    const parts = [];

    // 第1层：H2
    if (visual.h2) {
        parts.push({
            text: visual.h2,
            options: { fontSize: 10, fontFace: theme.FONT.body, bold: true, color: getC(theme, 'primary', '555555') }
        });
    }
    // 第2层：H3
    if (visual.h3) {
        if (parts.length > 0) parts.push({ text: '  ❯  ', options: { fontSize: 9, fontFace: theme.FONT.body, color: '999999', bold: true } });
        parts.push({
            text: visual.h3.split(/[：:]/)[0],
            options: { fontSize: 10, fontFace: theme.FONT.body, color: getC(theme, 'text_secondary', '777777'), bold: true }
        });
    }
    // 第3层：H4
    if (visual.h4) {
        if (parts.length > 0) parts.push({ text: '  ❯  ', options: { fontSize: 8, fontFace: theme.FONT.body, color: 'BBBBBB', bold: true } });
        parts.push({
            text: visual.h4.split(/[：:]/)[0],
            options: { fontSize: 9, fontFace: theme.FONT.body, color: getC(theme, 'text_muted', 'AAAAAA'), bold: false }
        });
    }

    if (parts.length > 0) {
        slide.addText(parts, {
            x: 0.6, y: 0.12, w: 8.8, h: 0.2, // 极限顶部空间
            align: 'right', valign: 'top'
        });
    }
}

// ============================================================
// 主入口：renderSlide
// ============================================================

/**
 * 根据 Layout 类型分发渲染函数
 *
 * @param {object} pres - PptxGenJS Presentation 实例
 * @param {object} slideData - { visual, speech } 结构化幻灯片数据
 * @param {object} theme - 设计令牌 { C, FONT }
 * @param {string} scriptDir - 脚本所在目录的绝对路径
 */
function renderSlide(pres, slideData, theme, scriptDir) {
    const { visual, speech } = slideData;
    let layoutType = (visual.layout || 'Split').toLowerCase().trim();

    // 弃用别名转换
    if (DEPRECATED_ALIASES[layoutType]) {
        const replacement = DEPRECATED_ALIASES[layoutType];
        console.warn(`⚠️  Deprecated layout "${visual.layout}" → use "${replacement}" instead`);
        layoutType = replacement;
    }

    // 创建 Slide
    const slide = pres.addSlide();
    slide.background = { color: getC(theme, 'bg_base', 'F5F0EB') };

    // --- 内部标签布局快速路径（_activity / _oral_tag）---
    // 这些布局没有图片资产，无需走资产解析/视频转码逻辑
    if (layoutType.startsWith('_')) {
        let notesText = speech || '';
        // 为 Quiz 类型自动向 Speaker Notes 追加结构化题目信息
        if (visual.activityType === 'Quiz' && visual.quizQuestion) {
            notesText += '\n\n━━━━━━━━━ 📝 随堂测验 ━━━━━━━━━';
            notesText += `\n❓ 题干: ${visual.quizQuestion}`;
            if (visual.quizOptions) {
                // ppt_parser 提取为用 "|" 分隔的字符串，这里拆分处理
                const opts = Array.isArray(visual.quizOptions)
                    ? visual.quizOptions
                    : String(visual.quizOptions).split('|').map(o => o.trim()).filter(Boolean);
                notesText += `\n🔹 选项:\n   - ${opts.join('\n   - ')}`;
            }
            if (visual.quizAnswer) notesText += `\n✅ 答案: ${visual.quizAnswer}`;
            if (visual.quizExplain) notesText += `\n💡 解析: ${visual.quizExplain}`;
            notesText += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━';
        }
        if (notesText.trim()) slide.addNotes(notesText.trim());
        const ctx = { pres, slide, theme, visual, assetPath: null, assetPaths: [] };
        const renderer = LAYOUT_MAP[layoutType];
        if (renderer) {
            renderer(ctx);
        } else {
            console.warn(`⚠️  未知内部布局 ${layoutType}，跳过`);
        }
        // 内部标签页面自带结构化视觉标识，免除面包屑
        return;
    }

    // 解析资源路径 — 支持多资产数组
    let assetPaths = [];
    const assetFields = visual.assets || (visual.asset ? [visual.asset] : []);
    const coursePath = path.resolve(scriptDir, '..');
    // 保留原始视频路径（用于视频嵌入判断）
    let originalVideoPaths = [];

    for (const assetRef of assetFields) {
        const candidates = [
            path.resolve(coursePath, assetRef),
            path.resolve(scriptDir, assetRef),  // weeks/W0X/ 下直接解析（新架构）
            path.resolve(scriptDir, '../visuals/assets', assetRef),
            path.resolve(scriptDir, '../visuals/assets', path.basename(assetRef)),
        ];
        let found = candidates.find(p => fs.existsSync(p)) || null;

        // 课程根级 fallback（V5 架构下本应禁止，但降级容错 + 醒目告警）
        if (!found) {
            const courseRoot = path.resolve(scriptDir, '..', '..');
            const courseRootCandidate = path.resolve(courseRoot, assetRef);
            if (fs.existsSync(courseRootCandidate)) {
                found = courseRootCandidate;
                const weekDir = path.basename(scriptDir);
                console.warn(`🚨 Asset found at COURSE-LEVEL (violates V5 self-contained package):`);
                console.warn(`   当前位置: ${path.relative(courseRoot, courseRootCandidate)}`);
                console.warn(`   应迁移到: ${weekDir}/${assetRef}`);
                console.warn(`   → 运行: python .agent/skills/validation_suite/scripts/validate_asset_placement.py --course "<课程>" --fix`);
            }
        }

        if (found) {
            assetPaths.push(found);
            if (isVideoAsset(found)) originalVideoPaths.push(found);
        } else {
            console.warn(`⚠️  Asset not found: ${assetRef}`);
        }
    }

    // 向后兼容：首图作为主 assetPath
    let assetPath = assetPaths[0] || null;

    // --- 视频嵌入 (ADR-044): 优先 addMedia 嵌入，失败时降级为 poster ---
    const hasVideoAsset = originalVideoPaths.length > 0;
    let videoEmbedded = false;

    if (hasVideoAsset && originalVideoPaths.length === 1) {
        // 单视频 Slide：尝试转码+嵌入
        const videoSrc = originalVideoPaths[0];
        const { mp4Path, subtitleLang, posterPath } = convertVideoForPptx(videoSrc, scriptDir);

        if (mp4Path) {
            // 视频 Speaker Notes：追加播放指引
            const videoMeta = [
                '',
                '━━━━━━━━━━━━━━━━━━━━━━━━',
                `🎬 视频素材: ${path.basename(videoSrc)}`,
                visual.duration ? `⏱ 时长: ${visual.duration}` : '',
                subtitleLang ? `📜 字幕: ${subtitleLang}（已烧录硬字幕）` : '📜 字幕: 无',
                visual.timecategory ? `📂 归因: ${visual.timecategory}` : '',
                '💡 提示: 点击 Slide 中央即可播放视频',
                '━━━━━━━━━━━━━━━━━━━━━━━━',
            ].filter(Boolean).join('\n');
            slide.addNotes((speech || '') + videoMeta);

            // 使用专用视频渲染函数
            const ctx = { pres, slide, theme, visual, assetPath: posterPath, assetPaths: [posterPath].filter(Boolean), mp4Path };
            renderVideoSlide(ctx);
            videoEmbedded = true;
        }
    }

    if (!videoEmbedded) {
        // 非视频 Slide 或视频转码失败 → 走原有逻辑
        if (speech) slide.addNotes(speech);

        // 视频资产降级为 poster（兼容旧行为）
        assetPaths = assetPaths.map(ap => {
            if (isVideoAsset(ap)) {
                const poster = extractPosterFrame(ap, scriptDir);
                if (poster) return poster;
                console.warn(`   ⚠️  [Video] 跳过无法生成 poster 的视频: ${path.basename(ap)}`);
                return null;
            }
            return ap;
        }).filter(Boolean);
        assetPath = assetPaths[0] || null;

        // 若是视频但转码失败，在 Notes 中追加警告
        if (hasVideoAsset && !videoEmbedded) {
            const fallbackNote = '\n\n⚠️ 本页包含视频素材但转码失败，已显示为静态截图。\n请使用 H5 课件预览查看完整视频。';
            slide.addNotes((speech || '') + fallbackNote);
        }

        // 分发渲染（assetPaths 供多图布局使用）
        const ctx = { pres, slide, theme, visual, assetPath, assetPaths };
        const renderer = LAYOUT_MAP[layoutType];
        if (renderer) {
            renderer(ctx);
        } else {
            // O-3: 未知 layout 警告增强 — 帮助脚本作者发现拼写错误
            console.warn(`⚠️  未知 Layout "${visual.layout}" (normalized: "${layoutType}")，回退到 renderSplit`);
            DEFAULT_RENDERER(ctx);
        }
    }

    // --- 注入全局面包屑导航 (方案 A) ---
    // F-10: 使用 constants.NO_BREADCRUMB 集合，新增全幅布局时只需维护 constants.js
    if (!NO_BREADCRUMB.has(layoutType)) {
        renderBreadcrumb(slide, theme, visual);
    }
}

module.exports = { renderSlide };
