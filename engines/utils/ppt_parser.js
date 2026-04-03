/**
 * ppt_parser.js — Markdown 脚本解析器
 *
 * 解析 Markdown 脚本，提取 [VISUAL] 块的结构化数据（Layout, Asset, List 等）
 * 以及对应的演讲稿 (Speech/Notes)。
 *
 * 修复记录:
 * - 跳过 YAML Frontmatter
 * - 过滤 [TECH NOTE] / [WARNING] / [CASE STUDY] 等知识标签
 * - 过滤 [ACTIVITY] 块
 * - 过滤 [STAGE NOTE] / [!INFO] 等非演讲内容
 * - 修复 isMetaLine 误吞正文
 * - 新增 Caption / Quote 字段解析
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

    // 正则定义
    const RE_VISUAL_START = /^>\s*\[VISUAL\]/i;
    // 口头叙事型标签（ADR 022）：内容写入 Speaker Notes
    const ORAL_TAGS = new Set(['STORY TIME', 'PHILOSOPHY', 'CASE STUDY', 'LIFE CONNECT', 'DID YOU KNOW', 'TEACHING MOMENT']);
    const RE_TAG_START = /^>\s*\[(TECH NOTE|WARNING|DID YOU KNOW|STORY TIME|PHILOSOPHY|CASE STUDY|LIFE CONNECT|TEACHING MOMENT)[:\]]/i;
    const RE_ACTIVITY_START = /^>\s*\[ACTIVITY\]/i;
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

        // === 追踪 ### 标题行（用于提取 visual.heading）===
        const headingMatch = trim.match(/^###\s+(?:\d+\.\d+\s+)?(.+)$/);
        if (headingMatch) {
            lastHeading = headingMatch[1].trim();
        }

        // === [VISUAL] 块开始 ===
        if (trim.match(RE_VISUAL_START)) {
            // 保存上一张 Slide
            if (currentSlide) {
                currentSlide.speech = cleanSpeech(buffer.join('\n').trim());
                slides.push(currentSlide);
            }
            // 初始化新 Slide，附加最近的 ### 标题
            currentSlide = { visual: { heading: lastHeading || '', assets: [] }, speech: "" };
            buffer = [];
            inVisualBlock = true;
            inTagBlock = false;
            inOralTagBlock = false;
            inActivityBlock = false;
            currentKey = null;
            lastHeading = ''; // 消费后重置，避免同一标题被多个 VISUAL 块复用
            continue;
        }

        // === [ACTIVITY] 块开始 ===
        if (trim.match(RE_ACTIVITY_START)) {
            inActivityBlock = true;
            inVisualBlock = false;
            inTagBlock = false;
            inOralTagBlock = false;
            currentKey = null;
            continue;
        }

        // === 知识标签块开始 (TECH NOTE / WARNING / CASE STUDY 等) ===
        const tagMatch = trim.match(RE_TAG_START);
        if (tagMatch) {
            const tagName = tagMatch[1].toUpperCase();
            if (ORAL_TAGS.has(tagName)) {
                // 口头型标签：内容写入 Speech Notes
                inOralTagBlock = true;
            } else {
                // 参考型标签（TECH NOTE / WARNING）：内容丢弃
                inTagBlock = true;
            }
            inVisualBlock = false;
            inActivityBlock = false;
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

        // === 在口头型标签块内（STORY TIME 等）===
        if (inOralTagBlock) {
            if (!trim.startsWith('>')) {
                // 引用块结束
                inOralTagBlock = false;
                // 当前行可能是 Speech
                if (currentSlide && !shouldIgnoreLine(trim)) {
                    buffer.push(line);
                }
            } else {
                // 口头型标签内的行写入 Speech Notes
                if (currentSlide) {
                    const mQuote = line.match(RE_QUOTE_LINE);
                    if (mQuote) {
                        let text = mQuote[1];
                        if (!isMetaLine(text) && !text.match(/^\s*\[[A-Z _!]+\]\s*$/)) {
                            buffer.push(text);
                        }
                    }
                }
            }
            continue;
        }

        // === 在 [ACTIVITY] 或参考型标签块内 ===
        if (inActivityBlock || inTagBlock) {
            if (!trim.startsWith('>')) {
                // 引用块结束
                inActivityBlock = false;
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
        if (currentSlide) {
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

module.exports = { parseScript, cleanSpeech };
