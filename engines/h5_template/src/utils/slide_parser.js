/**
 * slide_parser.js
 * 与 ppt_layouts.js 保持一致的解析逻辑，用于在 H5 侧处理未被提前解析的字符串数据。
 */

/**
 * 解析 List 字符串为数组
 * 支持 "A / B / C" 或 "A · B · C" 或 "A, B, C" 格式
 */
export function parseListString(list) {
  if (Array.isArray(list)) return list
  if (typeof list !== 'string') return []
  // 尝试按 / 或 · 分隔符拆分
  const bySep = list.split(/\s*[\/·]\s*/).map(s => s.trim()).filter(Boolean)
  if (bySep.length > 1) return bySep
  // 尝试按 "数字." 分隔（如 "1.粗鲁 2.强迫人..."）
  const byNum = list.split(/(?=\d+\.)/).map(s => s.replace(/^\d+\.\s*/, '').trim()).filter(Boolean)
  if (byNum.length > 1) return byNum
  // 尝试按逗号拆分
  const byComma = list.split(/[,，、]/).map(s => s.trim()).filter(Boolean)
  if (byComma.length > 1) return byComma
  return [list]
}

/**
 * 解析 Comparison 数据
 * 支持 "正面: A/B/C vs 反面: D/E/F" 格式
 * 
 * 如果无法解析出 vs，则返回 null，后续退化为 Grid 或普通 List。
 */
export function parseComparisonData(list) {
  if (typeof list !== 'string') return null
  const vsMatch = list.match(/^(.+?)\s+vs\s+(.+)$/i)
  if (!vsMatch) return null

  function parseSide(str) {
    const colonMatch = str.match(/^([^:]+):\s*(.+)$/)
    if (colonMatch) {
      return {
        label: colonMatch[1].trim(),
        items: colonMatch[2].split(/[\/,，、]/).map(s => s.trim()).filter(Boolean),
      }
    }
    return { label: '', items: str.split(/[\/,，、]/).map(s => s.trim()).filter(Boolean) }
  }

  return { left: parseSide(vsMatch[1]), right: parseSide(vsMatch[2]) }
}
