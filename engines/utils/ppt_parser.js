/**
 * ppt_parser.js — Markdown 脚本解析器
 *
 * 解析 Markdown 脚本，提取 [VISUAL] 块的结构化数据（Layout, Asset, List 等）
 * 以及对应的演讲稿 (Speech/Notes)。
 *
 * 修复记录:
 * - 跳过 YAML Frontmatter
 * - 过滤 [TECH NOTE] / [WARNING] 等参考型标签
 * - [ACTIVITY] 块 → 生成 _activity 类型 Slide（含 Type/Duration/Desc 字段）
 * - 口头型标签（STORY TIME / CASE STUDY 等）→ 生成 _oral_tag 类型 Slide
 * - 支持行内单行 [ACTIVITY] Type: QA | Duration: 1min | Desc: ... 格式
 * - 过滤 [STAGE NOTE] / [!INFO] 等非演讲内容
 * - 修复 isMetaLine 误吞正文
 * - 新增 Caption / Quote 字段解析
 * - [TEACHING MOMENT] 分流路由（阶段 1）：
 *     无标题 → 幕后导演提示，静默丢弃（防止投屏给学生）
 *     有标题 → 保留为 _oral_tag Slide（教学金句）
 */
const fs = require('fs');

/**
 * 从原始 Asset 值中提取纯净路径。
 * 支持 MD 语法 ![alt](path)、反引号、双引号、../ 前缀。
 * @param {string} raw - 原始资产路径字符串
 * @returns {string} 清洗后的纯净相对路径
 */
function normalizeAssetPath(raw) {
    if (!raw) return '';
    let s = raw.trim();
    // 剥离 MD 图片/链接语法 ![alt](path) 或 [text](path)
    const mdMatch = s.match(/^!?\[.*?\]\((.+?)\)$/);
    if (mdMatch) s = mdMatch[1].trim();
    // 剥离反引号
    if (s.startsWith('`') && s.endsWith('`')) s = s.slice(1, -1);
    // 剥离双引号
    if (s.startsWith('"') && s.endsWith('"')) s = s.slice(1, -1);
    // 剥离前导 ../
    s = s.replace(/^(\.\.\/)+/, '');
    return s.trim();
}

/**
 * 解析 Markdown 脚本文件
 * @param {string} filePath - 脚本绝对路径
 * @returns {Array<{ visual: Object, speech: string }>} Slides 数组
 */
function parseScript(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split(/\r?\n/);
    const slides = [];

    let currentSlide = null;
    let inVisualBlock = false;
    let inTagBlock = false;      // 参考型标签引用块内（TECH NOTE / WARNING）
    let inOralTagBlock = false;  // 口头型标签引用块内（STORY TIME 等，ADR 022）
    let inActivityBlock = false; // ACTIVITY 引用块内
    let currentKey = null;       // 当前正在收集的多行字段 (如 List)
    let buffer = [];             // Speech buffer
    let lineIdx = 0;
    let lastHeading = '';        // 最近的 ### 标题行（用于 visual.heading）
    let currentH2 = '';          // 追踪模块上下文
    let currentH3 = '';          // 追踪断言上下文
    let currentH4 = '';          // 追踪指令上下文

    // 正则定义
    const RE_VISUAL_START = /^>\s*\[VISUAL\]/i;
    // 口头叙事型标签（ADR 022）：内容合并到当前 Slide 的 Speaker Notes（不独立成页）
    const ORAL_TAGS = new Set(['STORY TIME', 'PHILOSOPHY', 'CASE STUDY', 'LIFE CONNECT', 'DID YOU KNOW', 'TEACHING MOMENT']);
    const RE_TAG_START = /^>\s*\[(TECH NOTE|WARNING|DID YOU KNOW|STORY TIME|PHILOSOPHY|CASE STUDY|LIFE CONNECT|TEACHING MOMENT)[:\]]/i;
    // 匹配标签行并提取标签名和可选标题（冒号后内容）
    const RE_TAG_WITH_TITLE = /^>\s*\[([A-Z][A-Z ]+?)(?::\s*(.+?))?\]\s*$/i;
    const RE_ACTIVITY_START = /^>\s*\[ACTIVITY\]/i;
    // 行内单行 ACTIVITY 格式：> [ACTIVITY] Type: QA | Duration: 1min | Desc: ...
    const RE_ACTIVITY_INLINE = /^>\s*\[ACTIVITY\]\s+(.+)$/i;
    const RE_STAGE_NOTE = /^>\s*\[STAGE NOTE/i;
    const RE_INFO_BLOCK = /^>\s*\[!INFO\]/i;
    const RE_KEY_VAL = /^>\s*(?:\*\s+)?\*\*([\w][\w ]*\w|\w+)\*\*:\s*(.+)$/; // > **Key**: / > **Asset 1**: 等含空格键名
    const RE_KEY_ONLY = /^>\s*(?:\*\s+)?\*\*([\w][\w ]*\w|\w+)\*\*:\s*$/;    // > **Key**: (Starts list)
    const RE_LIST_ITEM = /^>\s+(?:[\*\-\+]|\d+\.)\s+(.*)$/; // > * Item OR > 1. Item
    const RE_QUOTE_LINE = /^>\s?(.*)/;
    const RE_FRONTMATTER = /^---\s*$/;
    // 资产类键名正则（Asset / Asset 1 / Asset 2 / Resource）
    const RE_ASSET_KEY = /^asset(\s*\d+)?$/i;
    const RE_RESOURCE_KEY = /^resource$/i;

    // 1. 跳过 YAML Frontmatter
    if (lines[0] && lines[0].trim() === '---') {
        lineIdx = 1;
        while (lineIdx < lines.length && lines[lineIdx].trim() !== '---') {
            lineIdx++;
        }
        if (lineIdx < lines.length) lineIdx++; // 跳过结束的 ---
    }

    for (let i = lineIdx; i < lines.length; i++) {
        const line = lines[i];
        const trim = line.trim();

        const h2Match = trim.match(/^##(?!#)\s+(.+)$/);
        if (h2Match) { currentH2 = h2Match[1].trim(); currentH3 = ''; currentH4 = ''; }

        const h3Match = trim.match(/^###\s+(.+)$/);
        if (h3Match) {
            // H3 标题是章节边界：将之前累积的 speech buffer flush 到当前 slide，
            // 确保 H3 之后的正文归属到下一个 VISUAL 的 slide 中，而非"向后粘连"到前一页。
            if (currentSlide && buffer.length > 0) {
                currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
                slides.push(currentSlide);
                currentSlide = null;
                buffer = [];
            }
            currentH3 = h3Match[1].trim(); lastHeading = currentH3; currentH4 = '';
        }

        const h4Match = trim.match(/^####\s+(.+)$/);
        if (h4Match) { currentH4 = h4Match[1].trim(); }

        // === [VISUAL] 块开始 ===
        if (trim.match(RE_VISUAL_START)) {
            // 保存上一张 Slide
            if (currentSlide) {
                currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
                slides.push(currentSlide);
                buffer = []; // 仅在成功保存时 reset，否则保留（H3 flush 后的文字带入新 slide）
            }
            // 初始化新 Slide，附加最近的结构地图及标题
            currentSlide = { 
                visual: { 
                    heading: lastHeading || '', 
                    h2: currentH2,
                    h3: currentH3,
                    h4: currentH4,
                    assets: [] 
                }, 
                speech: "" 
            };
            inVisualBlock = true;
            inTagBlock = false;
            inOralTagBlock = false;
            inActivityBlock = false;
            currentKey = null;
            lastHeading = ''; // 消费后重置，避免同一标题被多个 VISUAL 块复用
            continue;
        }

        // === [ACTIVITY] 块开始 → 生成 _activity Slide ===
        const activityInlineMatch = trim.match(RE_ACTIVITY_INLINE);
        if (activityInlineMatch) {
            // 行内单行 ACTIVITY 格式：> [ACTIVITY] Type: QA | Duration: 1min | Desc: ...
            if (currentSlide) {
                currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
                slides.push(currentSlide);
            }
            const fields = parseInlineActivity(activityInlineMatch[1]);
            currentSlide = {
                visual: {
                    layout: '_activity',
                    heading: lastHeading || '',
                    h2: currentH2, h3: currentH3, h4: currentH4,
                    activityType: fields.type || 'Activity',
                    activityDuration: fields.duration || '',
                    activityDesc: fields.desc || '',
                    assets: []
                },
                speech: fields.desc || ''
            };
            buffer = [];
            // 行内格式无后续引用行，直接保存并重置
            slides.push(currentSlide);
            currentSlide = null;
            inActivityBlock = false;
            inVisualBlock = false;
            inTagBlock = false;
            inOralTagBlock = false;
            currentKey = null;
            continue;
        }
        if (trim.match(RE_ACTIVITY_START)) {
            // 多行 ACTIVITY 块：保存当前 Slide → 创建 _activity Slide
            if (currentSlide) {
                currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
                slides.push(currentSlide);
            }
            currentSlide = {
                visual: {
                    layout: '_activity',
                    heading: lastHeading || '',
                    h2: currentH2, h3: currentH3, h4: currentH4,
                    activityType: '',
                    activityDuration: '',
                    activityDesc: '',
                    assets: []
                },
                speech: ''
            };
            buffer = [];
            inActivityBlock = true;
            inVisualBlock = false;
            inTagBlock = false;
            inOralTagBlock = false;
            currentKey = null;
            continue;
        }

        // === 知识标签块开始 (TECH NOTE / WARNING / CASE STUDY 等) ===
        // 设计原则：只有 [VISUAL] 和 [ACTIVITY] 才创建新 Slide。
        // 口头标签（CASE STUDY / STORY TIME / TEACHING MOMENT 等）和参考标签（TECH NOTE / WARNING）
        // 的内容统一合并到当前 Slide 的 Speaker Notes 中，不独立成页。
        const tagMatch = trim.match(RE_TAG_START);
        if (tagMatch) {
            const tagName = tagMatch[1].toUpperCase();

            // 提取标签标题（冒号后内容，用于 Notes 中的结构标记）
            const titleMatch = trim.match(RE_TAG_WITH_TITLE);
            const tagTitle = titleMatch ? (titleMatch[2] || '').trim() : '';

            // 在 Notes 中插入标签类型标记，便于教师识别内容来源
            const isOral = ORAL_TAGS.has(tagName);
            const icon = isOral ? '' : '📎 ';
            const label = tagTitle ? `${tagName}: ${tagTitle}` : tagName;
            buffer.push(`\n[${icon}${label}]`);

            inOralTagBlock = true;
            inVisualBlock = false;
            inActivityBlock = false;
            inTagBlock = false;
            currentKey = null;
            continue;
        }

        // === [STAGE NOTE] / [!INFO] 行 ===
        if (trim.match(RE_STAGE_NOTE) || trim.match(RE_INFO_BLOCK)) {
            inTagBlock = true; // 也视为非 Speech 的引用块
            inVisualBlock = false;
            inActivityBlock = false;
            continue;
        }

        // === 在 [VISUAL] 块内 ===
        if (inVisualBlock) {
            if (!trim.startsWith('>')) {
                // 引用块结束，Visual 结束
                inVisualBlock = false;
                currentKey = null;

                // Look-Ahead 探测 Markdown 代码块或表格
                let lookIdx = i;
                let emptyCount = 0;
                while (lookIdx < lines.length) {
                    if (lines[lookIdx].trim() === '') {
                        emptyCount++;
                        if (emptyCount > 1) break;
                        lookIdx++;
                    } else {
                        break;
                    }
                }
                if (lookIdx < lines.length) {
                    const lineLook = lines[lookIdx].trim();
                    const codeM = lineLook.match(/^```(\w*)/);
                    const tableM = lineLook.match(/^\|.+\|$/);
                    
                    let assetContent = null;
                    let assetType = null;
                    
                    if (codeM) {
                        const lang = codeM[1].trim();
                        assetType = lang ? lang : 'code';
                        lookIdx++;
                        const innerCode = [];
                        while (lookIdx < lines.length && !lines[lookIdx].trim().startsWith('```')) {
                            innerCode.push(lines[lookIdx].replace(/\r$/, ''));
                            lookIdx++;
                        }
                        assetContent = innerCode.join('\n');
                        if (lookIdx < lines.length) lookIdx++;
                    } else if (tableM) {
                        assetType = 'table';
                        const tableLines = [];
                        while (lookIdx < lines.length && lines[lookIdx].trim().match(/^\|.+\|$/)) {
                            tableLines.push(lines[lookIdx].replace(/\r$/, ''));
                            lookIdx++;
                        }
                        assetContent = tableLines.join('\n');
                    }
                    
                    if (assetContent !== null) {
                        currentSlide.visual.assetContent = assetContent;
                        currentSlide.visual.assetType = assetType;
                        currentSlide.visual.assets = [];
                        currentSlide.visual.asset = '';
                        if (!currentSlide.visual.layout) {
                            if (assetType === 'mermaid') currentSlide.visual.layout = 'Diagram';
                            else if (assetType === 'table') currentSlide.visual.layout = 'Table';
                            else currentSlide.visual.layout = 'Code';
                        }
                        i = lookIdx - 1;
                        continue;
                    }
                }

                // 当前行可能是空行或 Speech 的开始
                if (trim !== '' && !trim.startsWith('<!--')) {
                    if (!isMetaLine(trim)) buffer.push(trim);
                }
                continue;
            }

            // 解析 Key-Value
            const mKV = trim.match(RE_KEY_VAL);
            if (mKV) {
                const rawKey = mKV[1].trim();
                const k = rawKey.toLowerCase();
                let v = mKV[2].trim();

                // 如果 Value 为空，说明是多行 List 的开始
                if (!v) {
                    currentSlide.visual[k] = []; // 初始化数组
                    currentKey = k;
                    continue;
                }

                // 去除行内代码反引号
                if (v.startsWith('`') && v.endsWith('`')) v = v.slice(1, -1);
                // 去除引号
                if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1);

                // 判断是否为资产类键（Asset / Asset 1 / Resource）
                const isAssetKey = RE_ASSET_KEY.test(rawKey) || RE_RESOURCE_KEY.test(rawKey);
                if (isAssetKey) {
                    const cleanPath = normalizeAssetPath(v);
                    if (cleanPath) {
                        currentSlide.visual.assets.push(cleanPath);
                    }
                    // 向后兼容：首个 asset 写入 visual.asset
                    if (!currentSlide.visual.asset) {
                        currentSlide.visual.asset = cleanPath;
                    }
                } else if (k === 'preview') {
                    // Preview 字段：静默跳过，不存入 visual 对象
                } else {
                    currentSlide.visual[k] = v;
                }
                currentKey = null; // 结束上一个多行 Key
                continue;
            }

            // 解析 Key Only (开始多行 List)
            const mKO = trim.match(RE_KEY_ONLY);
            if (mKO) {
                const k = mKO[1].toLowerCase();
                currentSlide.visual[k] = []; // 初始化数组
                currentKey = k;
                continue;
            }

            // 解析 List Item (仅当有 currentKey 时)
            if (currentKey) {
                const mList = trim.match(RE_LIST_ITEM);
                if (mList) {
                    let itemText = mList[1].trim();
                    // 去掉引号
                    if (itemText.startsWith('"') && itemText.endsWith('"')) {
                        itemText = itemText.slice(1, -1);
                    }
                    // 尝试解析结构化 Item: **Key**: Value
                    const itemKV = itemText.match(/^\*\*([^\*]+)\*\*:\s*(.*)/);
                    if (itemKV) {
                        currentSlide.visual[currentKey].push({ title: itemKV[1], desc: itemKV[2] });
                    } else {
                        currentSlide.visual[currentKey].push(itemText);
                    }
                    continue;
                }
            }

            // 其他引用行，忽略
            continue;
        }

        // === 在标签块内（口头型 + 参考型）→ 内容追加到当前 Slide 的 Notes ===
        if (inOralTagBlock) {
            if (!trim.startsWith('>')) {
                // 引用块结束，标签内容已在 buffer 中，继续正常 speech 收集
                inOralTagBlock = false;
                // 当前行可能是后续正文
                if (trim !== '' && !trim.startsWith('<!--')) {
                    if (!isMetaLine(trim) && !shouldIgnoreLine(trim)) {
                        buffer.push(line);
                    }
                }
            } else {
                // 标签内的引用行 → 提取内容追加到 buffer
                const mQuote = line.match(RE_QUOTE_LINE);
                if (mQuote) {
                    let text = mQuote[1];
                    if (!isMetaLine(text) && !text.match(/^\s*\[[A-Z _!]+\]\s*$/)) {
                        buffer.push(text);
                    }
                }
            }
            continue;
        }

        // === 在 [ACTIVITY] 块内 → 收集字段到 _activity Slide ===
        if (inActivityBlock) {
            if (!trim.startsWith('>')) {
                // 引用块结束 → 保存 _activity Slide
                inActivityBlock = false;
                if (currentSlide && currentSlide.visual.layout === '_activity') {
                    currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
                    slides.push(currentSlide);
                    currentSlide = null;
                    buffer = [];
                }
            } else {
                // 解析 ACTIVITY 块内的 Key-Value 字段
                if (currentSlide && currentSlide.visual.layout === '_activity') {
                    const mQuote = line.match(RE_QUOTE_LINE);
                    if (mQuote) {
                        let text = mQuote[1].trim();
                        // 尝试提取 **Key**: Value 格式
                        const kvMatch = text.match(/^\*\*([\w]+)\*\*:\s*(.+)$/);
                        if (kvMatch) {
                            const key = kvMatch[1].toLowerCase();
                            let val = kvMatch[2].trim();
                            if (val.startsWith('`') && val.endsWith('`')) val = val.slice(1, -1);
                            if (key === 'type') currentSlide.visual.activityType = val;
                            else if (key === 'duration') currentSlide.visual.activityDuration = val;
                            else if (key === 'desc') currentSlide.visual.activityDesc = val;
                            // Quiz 子类型专属字段
                            else if (key === 'q') currentSlide.visual.quizQuestion = val;
                            else if (key === 'options') currentSlide.visual.quizOptions = val;
                            else if (key === 'answer') currentSlide.visual.quizAnswer = val;
                            else if (key === 'explain') currentSlide.visual.quizExplain = val;
                        } else if (!isMetaLine(text) && !text.match(/^\s*\[[A-Z _!]+\]\s*$/)) {
                            // 非元数据行 → 写入 speech（活动步骤说明）
                            buffer.push(text);
                        }
                    }
                }
            }
            continue;
        }

        // === 在参考型标签块内（TECH NOTE / WARNING）===
        if (inTagBlock) {
            if (!trim.startsWith('>')) {
                // 引用块结束
                inTagBlock = false;
                // 当前行可能是 Speech
                if (currentSlide && !shouldIgnoreLine(trim)) {
                    buffer.push(line);
                }
            }
            // 引用块内的行全部丢弃，不写入 Speech
            continue;
        }

        // === 收集 Speech (非任何特殊块) ===
        // 即使 currentSlide 为 null（H3 章节切换后），也继续积累 buffer，
        // 待下一个 VISUAL 创建新 slide 时自动携带。
        {
            if (shouldIgnoreLine(trim)) continue;

            // 如果是引用行 (> ...)，提取内容
            const mQuote = line.match(RE_QUOTE_LINE);
            if (mQuote) {
                let text = mQuote[1];
                // 忽略 metadata 行 (> **Role**: ...)
                if (isMetaLine(text)) continue;
                // 忽略独立标签行 (> [TAG])
                if (text.match(/^\s*\[[A-Z _!]+\]\s*$/)) continue;

                buffer.push(text);
            } else {
                buffer.push(line);
            }
        }
    }

    // 保存最后一张
    if (currentSlide) {
        currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
        slides.push(currentSlide);
    }

    return slides;
}

// 辅助函数：判断是否忽略该行
function shouldIgnoreLine(trim) {
    if (trim === '') return false; // 保留段落空行
    if (trim.startsWith('#')) return true; // 标题
    if (trim.startsWith('---')) return true; // 分隔线
    if (trim.startsWith('<!--')) return true; // HTML 注释
    if (trim === '[SPEECH]') return true; // 单独的 [SPEECH] 标记
    if (trim.startsWith('## Self-Verification')) return true; // 脚本末尾校验块
    if (trim.startsWith('- [')) return true; // 校验清单项
    return false;
}

// 辅助函数：判断是否为元数据行 — 仅匹配已知的 meta 关键字
const META_KEYS = new Set(['role', 'stage', 'duration', 'type', 'desc', 'mode']);
function isMetaLine(text) {
    const m = text.trim().match(/^\*\*(\w+)\*\*:\s/);
    if (!m) return false;
    return META_KEYS.has(m[1].toLowerCase());
}

/**
 * 清洗演讲稿文本，移除 Markdown 标记但保留结构
 */
function cleanSpeech(text) {
    if (!text) return "";
    return text
        // 移除加粗 **text** -> text
        .replace(/\*\*(.*?)\*\*/g, '$1')
        // 移除斜体 *text* -> text
        .replace(/\*(.*?)\*/g, '$1')
        // 移除行内代码 `text` -> text
        .replace(/`(.*?)`/g, '$1')
        // 规范化列表符号
        .replace(/^\s*[\-\*]\s+/gm, '• ')
        // 移除 Pause 标记
        .replace(/\*\*\(Pause:.*?\)\*\*/g, '')
        .replace(/\(Pause:.*?\)/g, '')
        // 移除多余的空行 (超过2个换行 -> 2个)
        .replace(/\n{3,}/g, '\n\n')
        .trim();
}

/**
 * 解析行内单行 ACTIVITY 格式的字段
 * 输入示例: "Type: QA | Duration: 1min | Desc: 提问互动：..."
 * @param {string} inlineStr - 行内字段字符串
 * @returns {{ type: string, duration: string, desc: string }}
 */
function parseInlineActivity(inlineStr) {
    const result = { type: '', duration: '', desc: '' };
    if (!inlineStr) return result;
    // 按 | 分隔
    const parts = inlineStr.split(/\s*\|\s*/);
    for (const part of parts) {
        const m = part.match(/^(\w+)\s*[:：]\s*(.+)$/);
        if (m) {
            const key = m[1].toLowerCase();
            let val = m[2].trim();
            if (val.startsWith('`') && val.endsWith('`')) val = val.slice(1, -1);
            if (key === 'type') result.type = val;
            else if (key === 'duration') result.duration = val;
            else if (key === 'desc') result.desc = val;
        }
    }
    return result;
}

module.exports = { parseScript, cleanSpeech };
