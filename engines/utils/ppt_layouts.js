/**
 * ppt_layouts.js — 通用 PPT 布局引擎 v2
 * 
 * 包含各种布局的渲染逻辑。
 * 
 * v2 升级记录:
 * - renderSplit 反转为左文右图（对齐 Output 版专用脚本效果）
 * - 新增 renderComparison 双栏对比布局
 * - 新增 renderCTA 暗色收尾页
 * - renderTitle 升级为暗色全幅封面
 * - renderGrid 添加卡片阴影 + 顶部色条
 * - renderList 添加编号圆形样式
 * - renderDiagram 改为左文右图
 */
const path = require('path');
const fs = require('fs');
const { imageSize: sizeOf } = require('image-size');
const { execSync } = require('child_process');

// ============================================================
// 视频安全着陆系统 (ADR-042 跨端兼容层 → ADR-044 PPT 原生嵌入升级)
// ============================================================

/**
 * 支持的视频扩展名列表
 */
const VIDEO_EXTS = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv'];

/**
 * 判断资产路径是否为视频文件
 */
function isVideoAsset(assetPath) {
    if (!assetPath) return false;
    const ext = path.extname(assetPath).toLowerCase();
    return VIDEO_EXTS.includes(ext);
}

/**
 * 使用 ffmpeg 从视频中提取首帧，叠加半透明播放按钮，生成 poster 图片。
 * 
 * 缓存策略：poster 存放于 scriptDir/.build/_video_posters/，
 * 仅在 poster 不存在或视频文件更新时重新提取。
 * 
 * @param {string} videoPath - 视频文件的绝对路径
 * @param {string} scriptDir - 脚本所在目录（用于确定缓存位置）
 * @returns {string|null} poster 图片的绝对路径，失败时返回 null
 */
function extractPosterFrame(videoPath, scriptDir) {
    const videoName = path.basename(videoPath, path.extname(videoPath));
    const cacheDir = path.resolve(scriptDir, '.build', '_video_posters');
    const posterPath = path.resolve(cacheDir, `${videoName}_poster.png`);

    // 缓存命中检查
    if (fs.existsSync(posterPath)) {
        try {
            const videoMtime = fs.statSync(videoPath).mtimeMs;
            const posterMtime = fs.statSync(posterPath).mtimeMs;
            if (posterMtime > videoMtime) {
                return posterPath; // 缓存有效
            }
        } catch (e) {
            // 忽略 stat 错误，重新生成
        }
    }

    // 确保缓存目录存在
    if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, { recursive: true });
    }

    // 检查是否存在同名的手工 poster 文件（如 Dropbox_MVP_poster.png）
    const manualPoster = path.resolve(path.dirname(videoPath), `${videoName}_poster.png`);
    if (fs.existsSync(manualPoster)) {
        console.log(`   🖼️  [Video] 使用手工 poster: ${path.basename(manualPoster)}`);
        fs.copyFileSync(manualPoster, posterPath);
        return posterPath;
    }

    // 使用 ffmpeg 提取首帧（10秒处，或视频开头）
    const ffmpegBin = '/opt/homebrew/bin/ffmpeg';
    const tmpRaw = path.resolve(cacheDir, `${videoName}_raw.png`);

    try {
        // 尝试在 10 秒处提取，如果视频不足 10 秒则用首帧
        execSync(
            `${ffmpegBin} -y -ss 00:00:03 -i "${videoPath}" -vframes 1 -q:v 2 "${tmpRaw}" 2>/dev/null` +
            ` || ${ffmpegBin} -y -i "${videoPath}" -vframes 1 -q:v 2 "${tmpRaw}" 2>/dev/null`,
            { stdio: 'pipe', timeout: 15000 }
        );

        if (!fs.existsSync(tmpRaw)) {
            console.warn(`   ⚠️  [Video] ffmpeg 首帧提取失败: ${path.basename(videoPath)}`);
            return null;
        }

        // 叠加半透明播放按钮三角形 (使用 ffmpeg drawtext 或 overlay)
        // 简化方案：使用 ffmpeg 的 drawbox + 文字绘制播放符号
        execSync(
            `${ffmpegBin} -y -i "${tmpRaw}" ` +
            `-vf "drawbox=x=iw/2-40:y=ih/2-40:w=80:h=80:color=black@0.5:t=fill, ` +
            `drawtext=text='▶':fontsize=48:fontcolor=white@0.9:x=(w-tw)/2:y=(h-th)/2" ` +
            `"${posterPath}" 2>/dev/null`,
            { stdio: 'pipe', timeout: 10000 }
        );

        // 如果叠加失败，退化为使用原始首帧
        if (!fs.existsSync(posterPath)) {
            fs.renameSync(tmpRaw, posterPath);
        } else {
            // 清理临时文件
            try { fs.unlinkSync(tmpRaw); } catch (e) { /* 忽略 */ }
        }

        console.log(`   🎬→🖼️  [Video] 提取 poster: ${path.basename(videoPath)} → ${path.basename(posterPath)}`);
        return posterPath;
    } catch (e) {
        console.warn(`   ⚠️  [Video] poster 生成失败 (${path.basename(videoPath)}): ${e.message}`);
        // 清理可能的残留文件
        try { if (fs.existsSync(tmpRaw)) fs.unlinkSync(tmpRaw); } catch (e2) { /* 忽略 */ }
        return null;
    }
}

/**
 * 将视频转换为 PPTX 可嵌入的 MP4 格式（含可选 VTT 硬字幕烧录）。
 *
 * 处理流程：
 *   1. 检测同名 .zh-Hant.vtt / .en.vtt 字幕文件
 *   2. 若源为 .webm 或存在字幕 → ffmpeg 转码/烧录 → 输出 .mp4
 *   3. 若源已是 .mp4 且无字幕 → 直接返回原路径
 *
 * 缓存策略：产物存放于 scriptDir/.build/_video_pptx/，
 * 仅在源视频或字幕文件更新时重新转码。
 *
 * @param {string} videoPath - 视频文件的绝对路径
 * @param {string} scriptDir - 脚本所在目录
 * @returns {{ mp4Path: string|null, subtitleLang: string|null, posterPath: string|null }}
 */
function convertVideoForPptx(videoPath, scriptDir) {
    const videoName = path.basename(videoPath, path.extname(videoPath));
    const videoDir = path.dirname(videoPath);
    const videoExt = path.extname(videoPath).toLowerCase();
    const cacheDir = path.resolve(scriptDir, '.build', '_video_pptx');
    const mp4Output = path.resolve(cacheDir, `${videoName}.mp4`);
    const ffmpegBin = '/opt/homebrew/bin/ffmpeg';

    // 检测同名字幕文件（优先中文，回退英文）
    let vttPath = null;
    let subtitleLang = null;
    const vttCandidates = [
        { path: path.resolve(videoDir, `${videoName}.zh-Hant.vtt`), lang: 'zh-Hant' },
        { path: path.resolve(videoDir, `${videoName}.zh.vtt`), lang: 'zh' },
        { path: path.resolve(videoDir, `${videoName}.en.vtt`), lang: 'en' },
        { path: path.resolve(videoDir, `${videoName}.srt`), lang: 'srt' },
    ];
    for (const cand of vttCandidates) {
        if (fs.existsSync(cand.path)) {
            vttPath = cand.path;
            subtitleLang = cand.lang;
            break;
        }
    }

    // 若源已是 MP4 且无字幕需要烧录 → 直接返回原路径
    if (videoExt === '.mp4' && !vttPath) {
        return { mp4Path: videoPath, subtitleLang: null, posterPath: null };
    }

    // 确保缓存目录存在
    if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, { recursive: true });
    }

    // 缓存命中检查 — 源视频和字幕都未更新时跳过
    if (fs.existsSync(mp4Output)) {
        try {
            const outMtime = fs.statSync(mp4Output).mtimeMs;
            const srcMtime = fs.statSync(videoPath).mtimeMs;
            const vttMtime = vttPath ? fs.statSync(vttPath).mtimeMs : 0;
            if (outMtime > srcMtime && outMtime > vttMtime) {
                console.log(`   ✅ [Video→PPTX] 缓存命中: ${videoName}.mp4`);
                // 同时生成/复用 poster 用于 addMedia cover
                const posterPath = extractPosterFrame(videoPath, scriptDir);
                return { mp4Path: mp4Output, subtitleLang, posterPath };
            }
        } catch (e) { /* 忽略 stat 错误，重新转码 */ }
    }

    // 构建 ffmpeg 命令
    let cmd;
    if (vttPath) {
        // 带字幕烧录的转码
        // 注意：subtitles 滤镜需要对路径中的特殊字符进行转义
        const escapedVtt = vttPath.replace(/'/g, "'\\\\\\'''").replace(/:/g, '\\\\:');
        cmd = `${ffmpegBin} -y -i "${videoPath}" ` +
            `-vf "subtitles='${escapedVtt}':force_style='FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,MarginV=25'" ` +
            `-c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k ` +
            `"${mp4Output}" 2>&1`;
        console.log(`   🎬→📦 [Video→PPTX] 转码+硬字幕(${subtitleLang}): ${path.basename(videoPath)}`);
    } else {
        // 纯格式转码（WebM → MP4）
        cmd = `${ffmpegBin} -y -i "${videoPath}" ` +
            `-c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k ` +
            `"${mp4Output}" 2>&1`;
        console.log(`   🎬→📦 [Video→PPTX] 格式转码: ${path.basename(videoPath)} → MP4`);
    }

    try {
        execSync(cmd, { stdio: 'pipe', timeout: 120000 }); // 2 分钟超时
        if (!fs.existsSync(mp4Output)) {
            console.warn(`   ⚠️  [Video→PPTX] 转码产物未生成: ${videoName}.mp4`);
            return { mp4Path: null, subtitleLang: null, posterPath: null };
        }
        const sizeMB = (fs.statSync(mp4Output).size / 1024 / 1024).toFixed(1);
        console.log(`   ✅ [Video→PPTX] 转码完成: ${videoName}.mp4 (${sizeMB} MB)`);
        // 提取 poster 用于 addMedia cover
        const posterPath = extractPosterFrame(videoPath, scriptDir);
        return { mp4Path: mp4Output, subtitleLang, posterPath };
    } catch (e) {
        console.warn(`   ⚠️  [Video→PPTX] 转码失败 (${path.basename(videoPath)}): ${e.message?.substring(0, 200)}`);
        return { mp4Path: null, subtitleLang: null, posterPath: null };
    }
}

// 统一常量
const CW = 10.0;  // Slide Width
const CH = 5.625; // Slide Height
const MARGIN = 0.6;

/**
 * Layout → 渲染函数映射表
 */
const LAYOUT_MAP = {
    // --- 正式标签 ---
    'title': 'renderTitle',
    'section': 'renderTitle',
    'agenda': 'renderList',
    'split': 'renderSplit',
    'icons': 'renderList',
    'grid': 'renderGrid',
    'full': 'renderImage',
    'table': 'renderList',
    'comparison': 'renderComparison',
    'dashboard': 'renderGrid',
    'stat': 'renderTitle',
    'timeline': 'renderDiagram',
    'poll': 'renderImage',
    'workshop': 'renderList',
    'quote': 'renderQuote',
    'cta': 'renderCTA',
    'code': 'renderSplit',
    'diagram': 'renderDiagram',
    'image': 'renderImage',
    'screenshot': 'renderImage',
    'list': 'renderList',
    // --- 内部标签（解析器自动生成）---
    '_activity': 'renderActivity',
    '_oral_tag': 'renderOralTag',
};

/**
 * 弃用别名 → 正式标签映射
 */
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
    'Video': 'full',
    'scene': 'image',
    'checklist': 'list',
    'process': 'timeline',
};

const RENDERERS = {
    renderTitle,
    renderSplit,
    renderImage,
    renderDiagram,
    renderList,
    renderGrid,
    renderQuote,
    renderComparison,
    renderCTA,
    renderVideoSlide,
    renderActivity,
    renderOralTag,
};

// ============================================================
// 工厂函数（防止 pptxgenjs 对象变异）
// ============================================================
const cardShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.08 });

/**
 * 安全读取图片宽高比
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

/**
 * 提取幻灯片标题
 * 优先级：headline/text (作者显式指定) > H4 (指令标题) > H3 (断言标题) > sceneSummary(scene)
 */
function extractTitle(visual) {
    // 1. 优先使用 [VISUAL] 块中作者显式指定的标题
    const raw = visual.headline || visual.text || '';
    if (raw) return raw.replace(/^"|"$/g, '').replace(/\\n/g, '\n');
    // 2. 退化为微观行动指令 (H4)
    if (visual.h4) return visual.h4;
    // 3. 退化为宏观断言结构 (H3 / Parser 默认 heading)
    if (visual.h3) return visual.h3;
    if (visual.heading) return visual.heading;
    // 4. 用 Slide 字段作为标题
    if (visual.slide) return visual.slide;
    // 5. 最后 fallback 到 scene 截取
    return sceneSummary(visual.scene);
}

/**
 * 根据标题长度自适应字号
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

/**
 * 安全获取颜色（带 fallback）
 */
function getC(theme, key, fallback) {
    return theme.C[key] || fallback || 'CCCCCC';
}

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

/**
 * 主入口：根据 Layout 类型分发渲染函数
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
        const rendererName = LAYOUT_MAP[layoutType];
        const renderer = rendererName ? RENDERERS[rendererName] : null;
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
        const rendererName = LAYOUT_MAP[layoutType] || 'renderSplit';
        const renderer = RENDERERS[rendererName];
        if (renderer) {
            renderer(ctx);
        } else {
            console.warn(`⚠️  未知渲染函数 ${rendererName}，回退到 renderSplit`);
            renderSplit(ctx);
        }
    }

    // --- 注入全局面包屑导航 (方案 A) ---
    // 对视觉冲击力较强的全幅页面和内部标签页免除面包屑干扰
    if (!['title', 'section', 'cta', 'quote'].includes(layoutType)) {
        renderBreadcrumb(slide, theme, visual);
    }
}

// ============================================================
// Layout Implementations
// ============================================================

/**
 * renderTitle — 暗色全幅封面页
 * 暗底 + 顶部装饰条 + 主标题 + 副标题 + 底部学期信息
 */
function renderTitle(ctx) {
    const { pres, slide, theme, visual } = ctx;
    const C = theme.C;
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

/**
 * renderSplit — 左文右图布局 (v2: 方向修正)
 * 标题在左上、要点/文字在左侧、大图在右侧
 * 
 * v3: 双图 Split 模式 — 当有 ≥2 张图片时，左右各放一张图
 */
function renderSplit(ctx) {
    const { slide, theme, visual, assetPath, assetPaths } = ctx;
    const C = theme.C;
    const F = theme.FONT;

    // ─── 双图 Split 模式 ───
    if (assetPaths && assetPaths.length >= 2) {
        const title = extractTitle(visual);

        // 顶部居中标题
        if (title) {
            slide.addText(title, {
                x: MARGIN, y: 0.35, w: CW - MARGIN * 2, h: 0.55,
                fontSize: adaptiveTitleSize(title), fontFace: F.title, color: getC(theme, 'text_main', '2D2926'),
                bold: true, margin: 0, align: 'center',
            });
        }

        // 左右两张图，各占约 45%
        const imgMaxW = 4.2;
        const imgMaxH = 4.0;
        const imgY0 = 1.1;
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
        const maxW = 4.4;
        const maxH = 4.6;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = 5.2 + (maxW - finalW) / 2;
        const imgY = 0.5 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: imgY, w: finalW, h: finalH });
    }
}

/**
 * renderImage — 居中大图布局
 */
function renderImage(ctx) {
    const { slide, theme, visual, assetPath, assetPaths } = ctx;
    const C = theme.C;
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
        const maxW = 8.0;
        const maxH = 3.8;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = (CW - finalW) / 2;
        const y = 1.1 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
    }

    // 底部说明
    const caption = visual.caption || sceneSummary(visual.scene, 80);
    if (caption) {
        slide.addText(caption, {
            x: MARGIN, y: CH - 0.6, w: CW - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
            align: 'center',
        });
    }
}

/**
 * renderDiagram — 左文右图 + 序号步骤列表
 * v2: 反转为左文右图（与 Split 一致方向）
 */
function renderDiagram(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const C = theme.C;
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
        const maxW = 4.4;
        const maxH = 4.6;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = 5.2 + (maxW - finalW) / 2;
        const y = 0.5 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
    }
}

/**
 * renderList — 编号圆形 + 左图右列表布局
 * v2: 添加编号圆形标记（而非纯 bullet）
 */
function renderList(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const C = theme.C;
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
            const num = String(i + 1).padStart(2, '0');

            // 编号圆形
            slide.addShape(pres.shapes.OVAL, {
                x: MARGIN, y: y + 0.05, w: 0.45, h: 0.45,
                fill: { color: getC(theme, 'primary') },
            });
            slide.addText(num, {
                x: MARGIN, y: y + 0.05, w: 0.45, h: 0.45,
                fontSize: 14, fontFace: F.title, color: getC(theme, 'text_on_dark', 'FFFFFF'),
                align: 'center', valign: 'middle', margin: 0,
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
        const maxW = 4.4;
        const maxH = 4.2;
        const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
        const x = 5.2 + (maxW - finalW) / 2;
        const y = 0.8 + (maxH - finalH) / 2;
        slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
    }
}

/**
 * renderGrid — 卡片网格布局
 * v3: 消除图/卡零和博弈，支持 Editorial Split（左图右卡共生）
 */
function renderGrid(ctx) {
    const { pres, slide, theme, visual, assetPath, assetPaths } = ctx;
    const C = theme.C;
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

        const cardW = (CW - MARGIN * 2 - 0.35 * (cols - 1)) / cols;
        const gridY = 1.1;
        const gridH = CH - gridY - 0.8; 
        const cardH = (gridH - 0.35 * (rows - 1)) / rows;
        const startX = (CW - (cardW * cols + 0.35 * (cols - 1))) / 2;

        const accents = [
            getC(theme, 'primary'),
            getC(theme, 'tertiary', getC(theme, 'warning')),
            getC(theme, 'secondary', getC(theme, 'success')),
            getC(theme, 'primary_light', getC(theme, 'primary')),
        ];

        for (let i = 0; i < count; i++) {
            const col = i % cols;
            const row = Math.floor(i / cols);
            const cx = startX + col * (cardW + 0.35);
            const cy = gridY + row * (cardH + 0.35);

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
        const maxW = 8.0;
        const maxH = 3.8;
        const { w: finalW, h: finalH } = fitImage(ap, maxW, maxH);
        const x = (CW - finalW) / 2;
        const y = 1.1 + (maxH - finalH) / 2;
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

    const cardW = (CW - MARGIN * 2 - 0.35 * (cols - 1)) / cols;
    const gridY = 1.1;
    const gridH = CH - gridY - 0.8;
    // 无 desc 时缩小卡片高度
    const hasDesc = items.some(item => typeof item !== 'string' && item.desc);
    const maxCardH = (gridH - 0.35 * (rows - 1)) / rows;
    const cardH = hasDesc ? maxCardH : Math.min(maxCardH, 1.2);
    const startX = (CW - (cardW * cols + 0.35 * (cols - 1))) / 2;

    // 色调数组
    const accents = [
        getC(theme, 'primary'),
        getC(theme, 'tertiary', getC(theme, 'warning')),
        getC(theme, 'secondary', getC(theme, 'success')),
    ];

    items.forEach((item, i) => {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const cx = startX + col * (cardW + 0.35);
        const cy = gridY + row * (cardH + 0.35);

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
    const C = theme.C;
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

/**
 * renderCTA — 暗色收尾页 (v2 新增)
 * 暗底 + 顶部装饰条 + 总结要点列表 + 水平分隔线 + 课后任务
 */
function renderCTA(ctx) {
    const { pres, slide, theme, visual } = ctx;
    const C = theme.C;
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

/**
 * renderVideoSlide — 视频嵌入专用布局
 * 使用 PptxGenJS addMedia() 嵌入 MP4 视频，poster 作为封面
 */
function renderVideoSlide(ctx) {
    const { pres, slide, theme, visual, assetPath, mp4Path } = ctx;
    const C = theme.C;
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

/**
 * renderQuote — 金句卡片布局
 */
function renderQuote(ctx) {
    const { slide, theme, visual } = ctx;
    const C = theme.C;
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
// 教学标签专用布局（解析器自动生成的内部 Slide 类型）
// ============================================================

/**
 * Activity Type → 图标映射表
 */
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

/**
 * Oral Tag → 图标 + 色调映射表
 */
const ORAL_TAG_STYLE = {
    'STORY TIME':       { icon: '📖', colorKey: 'primary' },
    'CASE STUDY':       { icon: '📋', colorKey: 'secondary' },
    'TEACHING MOMENT':  { icon: '💡', colorKey: 'tertiary' },
    'PHILOSOPHY':       { icon: '🧠', colorKey: 'primary_light' },
    'LIFE CONNECT':     { icon: '🌏', colorKey: 'secondary' },
    'DID YOU KNOW':     { icon: '🔍', colorKey: 'text_muted' },
};

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

    // 活动名称（主标题）
    const actTitle = visual.activityDesc || visual.heading || '课堂活动';
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

module.exports = { renderSlide };
