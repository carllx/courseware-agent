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
    if (Array.isArray(list)) return list;
    if (typeof list !== 'string') return [];
    // 尝试按 / 或 · 分隔符拆分
    const bySep = list.split(/\s*[\/·]\s*/).map(s => s.trim()).filter(Boolean);
    if (bySep.length > 1) return bySep;
    // 尝试按 "数字." 分隔（如 "1.粗鲁 2.强迫人..."）
    const byNum = list.split(/(?=\d+\.)/).map(s => s.replace(/^\d+\.\s*/, '').trim()).filter(Boolean);
    if (byNum.length > 1) return byNum;
    // 尝试按逗号拆分
    const byComma = list.split(/[,，、]/).map(s => s.trim()).filter(Boolean);
    if (byComma.length > 1) return byComma;
    return [list];
}

/**
 * 解析 Comparison 数据
 * 支持 "正面: A/B/C vs 反面: D/E/F" 格式
 */
function parseComparisonData(list) {
    if (typeof list !== 'string') return null;
    const vsMatch = list.match(/^(.+?)\s+vs\s+(.+)$/i);
    if (!vsMatch) return null;

    function parseSide(str) {
        const colonMatch = str.match(/^([^:]+):\s*(.+)$/);
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
 * 优先级：heading (从 ### 标题行提取) > headline > text > sceneSummary(scene)
 */
function extractTitle(visual) {
    // 1. 优先用 Parser 提取的 heading
    if (visual.heading) return visual.heading;
    // 2. 其次是显式的 headline / text 字段
    const raw = visual.headline || visual.text || '';
    if (raw) return raw.replace(/^"|"$/g, '').replace(/\\n/g, '\n');
    // 3. 用 Slide 字段作为标题（脚本中 **Slide**: xxx）
    if (visual.slide) return visual.slide;
    // 4. 最后 fallback 到 scene 截取
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
    if (speech) slide.addNotes(speech);

    // 解析资源路径 — 支持多资产数组
    let assetPaths = [];
    const assetFields = visual.assets || (visual.asset ? [visual.asset] : []);
    const coursePath = path.resolve(scriptDir, '..');

    for (const assetRef of assetFields) {
        const candidates = [
            path.resolve(coursePath, assetRef),
            path.resolve(scriptDir, assetRef),  // weeks/W0X/ 下直接解析（新架构）
            path.resolve(scriptDir, '../visuals/assets', assetRef),
            path.resolve(scriptDir, '../visuals/assets', path.basename(assetRef)),
        ];
        const found = candidates.find(p => fs.existsSync(p)) || null;
        if (found) {
            assetPaths.push(found);
        } else {
            console.warn(`⚠️  Asset not found: ${assetRef}`);
        }
    }

    // 向后兼容：首图作为主 assetPath
    const assetPath = assetPaths[0] || null;

    // 分发渲染（assetPaths 供未来多图布局使用）
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
 */
function renderSplit(ctx) {
    const { slide, theme, visual, assetPath } = ctx;
    const C = theme.C;
    const F = theme.FONT;

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
    } else if (visual.scene) {
        // 场景描述作为正文
        slide.addText(visual.scene, {
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
    const { slide, theme, visual, assetPath } = ctx;
    const C = theme.C;
    const F = theme.FONT;

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
    const { pres, slide, theme, visual, assetPath } = ctx;
    const C = theme.C;
    const F = theme.FONT;

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
    } else if (visual.scene) {
        // Fallback: 用 scene 填充左侧
        slide.addText(visual.scene, {
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
    const { pres, slide, theme, visual, assetPath } = ctx;
    const C = theme.C;
    const F = theme.FONT;

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
 * v2: 添加卡片阴影 + 顶部色条装饰
 */
function renderGrid(ctx) {
    const { pres, slide, theme, visual, assetPath } = ctx;
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

    if (items.length === 0) {
        // 无 list 数据：如果有 asset 则展示居中大图，否则显示 scene 摘要
        if (assetPath) {
            const maxW = 8.0;
            const maxH = 3.8;
            const { w: finalW, h: finalH } = fitImage(assetPath, maxW, maxH);
            const x = (CW - finalW) / 2;
            const y = 1.1 + (maxH - finalH) / 2;
            slide.addImage({ path: assetPath, x: x, y: y, w: finalW, h: finalH });
        } else if (visual.scene) {
            slide.addText(visual.scene, {
                x: MARGIN, y: 1.0, w: CW - MARGIN * 2, h: 3.5,
                fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
                valign: 'top',
            });
        }
        return;
    }

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
 * renderComparison — 双栏对比布局 (v2 新增)
 * 左绿右红的对比列表 + 列头色块 + 底部注释
 */
function renderComparison(ctx) {
    const { pres, slide, theme, visual } = ctx;
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

    const colW = 4.0;
    const colGap = 0.4;
    const lx = MARGIN;
    const rx = MARGIN + colW + colGap;
    const headerY = 1.1;

    // ─── 左列标签（正面 / secondary 绿色）───
    slide.addShape(pres.shapes.RECTANGLE, {
        x: lx, y: headerY, w: colW, h: 0.4,
        fill: { color: getC(theme, 'secondary', getC(theme, 'success', '5B7B6F')) },
    });
    slide.addText(`✓  ${data.left.label || '正面'}`, {
        x: lx, y: headerY, w: colW, h: 0.4,
        fontSize: 14, fontFace: F.title, color: getC(theme, 'text_on_dark', 'FFFFFF'),
        bold: true, align: 'center', valign: 'middle', margin: 0,
    });

    // 左列内容
    let ly = headerY + 0.6;
    data.left.items.forEach(item => {
        if (ly + 0.45 > CH - 0.6) return;
        slide.addText(item, {
            x: lx + 0.2, y: ly, w: colW - 0.4, h: 0.45,
            fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
            bullet: true, valign: 'top',
        });
        ly += 0.5;
    });

    // ─── 右列标签（反面 / primary 红色）───
    slide.addShape(pres.shapes.RECTANGLE, {
        x: rx, y: headerY, w: colW, h: 0.4,
        fill: { color: getC(theme, 'primary', 'B85042') },
    });
    slide.addText(`✗  ${data.right.label || '反面'}`, {
        x: rx, y: headerY, w: colW, h: 0.4,
        fontSize: 14, fontFace: F.title, color: getC(theme, 'text_on_dark', 'FFFFFF'),
        bold: true, align: 'center', valign: 'middle', margin: 0,
    });

    // 右列内容
    let ry = headerY + 0.6;
    data.right.items.forEach(item => {
        if (ry + 0.45 > CH - 0.6) return;
        slide.addText(item, {
            x: rx + 0.2, y: ry, w: colW - 0.4, h: 0.45,
            fontSize: 16, fontFace: F.body, color: getC(theme, 'text_main'),
            bullet: true, valign: 'top',
        });
        ry += 0.5;
    });

    // 底部注释
    if (visual.scene) {
        slide.addText(sceneSummary(visual.scene, 80), {
            x: MARGIN, y: CH - 0.65, w: CW - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: F.body, italic: true, color: getC(theme, 'text_muted'),
            align: 'center',
        });
    }
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

module.exports = { renderSlide };
