/**
 * slide_parser.js
 * 与 ppt_layouts.js 保持一致的解析逻辑，用于在 H5 侧处理未被提前解析的字符串数据。
 */

export function parseListString(list) {
  // 1. 若 SSG 已预处理为数组，跳过拆分直接进入冒号解析
  if (Array.isArray(list)) {
    return list.map(item => _parseColonPair(item));
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
 * 内部辅助：仅执行冒号键值对解析（不做拆分）
 * 当 SSG 已预处理为数组时使用，避免二次拆分破坏内容
 */
function _parseColonPair(item) {
  if (typeof item !== 'string') return item;
  const colonMatch = item.match(/^([^:：]+)[:：]\s*(.+)$/);
  if (colonMatch) {
    return {
      title: colonMatch[1].trim(),
      desc: colonMatch[2].trim()
    };
  }
  return item;
}

/**
 * 解析 Comparison 数据
 * 支持 "正面: A/B/C vs 反面: D/E/F" 格式
 * 
 * 如果无法解析出 vs，则返回 null，后续退化为 Grid 或普通 List。
 */
export function parseComparisonData(list) {
  // 字符串路径：原有逻辑
  if (typeof list === 'string') {
    return _parseComparisonString(list)
  }

  // 数组路径：Python SSG 已预处理为 Array
  if (Array.isArray(list) && list.length > 0) {
    // 策略 1: 在数组元素中查找包含 "vs" 的条目
    for (const item of list) {
      if (typeof item === 'string') {
        const result = _parseComparisonString(item)
        if (result) return result
      }
    }

    // 策略 2: 尝试从所有元素的拼接文本中提取 vs 结构
    const joined = list.filter(s => typeof s === 'string').join(' ')
    const joinedResult = _parseComparisonString(joined)
    if (joinedResult) return joinedResult

    // 策略 3: 检查是否有 "label: items" 格式的成对条目（如 "正面体验: A, B" / "负面体验: C, D"）
    // 同时匹配英文冒号 : 和中文冒号 ：
    if (list.length >= 2) {
      const colonRe = /^[^:：]+[：:]\s*.+/
      const sides = list.filter(s => typeof s === 'string' && colonRe.test(s))
      if (sides.length >= 2) {
        const parseSide = (str) => {
          const m = str.match(/^([^:：]+)[：:]\s*(.+)$/)
          if (m) return { label: m[1].trim(), items: m[2].split(/[\/,，、]/).map(s => s.trim()).filter(Boolean) }
          return { label: '', items: [str] }
        }
        return { left: parseSide(sides[0]), right: parseSide(sides[1]) }
      }
    }
  }

  return null
}

/**
 * 内部辅助：从字符串中解析 "A vs B" 对比结构
 */
function _parseComparisonString(str) {
  if (typeof str !== 'string') return null
  const vsMatch = str.match(/^(.+?)(?:\s+vs\s+|\s*\|\s*)(.+)$/i)
  if (!vsMatch) return null

  function parseSide(s) {
    const colonMatch = s.match(/^([^:：]+)[:：]\s*(.+)$/)
    if (colonMatch) {
      return {
        label: colonMatch[1].trim(),
        items: colonMatch[2].split(/[\/,，、]/).map(t => t.trim()).filter(Boolean),
      }
    }
    return { label: '', items: s.split(/[\/,，、]/).map(t => t.trim()).filter(Boolean) }
  }

  return { left: parseSide(vsMatch[1]), right: parseSide(vsMatch[2]) }
}
