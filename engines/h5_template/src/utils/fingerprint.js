/**
 * fingerprint.js — 段落指纹引擎（修正 V4）
 *
 * 使用段落前 N 个字符的简单哈希生成指纹，
 * 替代行号绑定，解决内容增删导致的批注漂移问题。
 *
 * 设计决策：
 * - 使用 DJB2 哈希（纯前端，无需 crypto 模块）
 * - 取段落前 50 个非空白字符作为特征
 * - 输出 8 位十六进制指纹
 */

const FINGERPRINT_CHARS = 50

/**
 * 计算段落文本指纹
 * @param {string} text 段落全文
 * @returns {string} 8 位十六进制指纹
 */
export function computeFingerprint(text) {
  if (!text) return '00000000'

  // 提取前 N 个非空白字符
  const chars = text.replace(/\s+/g, '').slice(0, FINGERPRINT_CHARS)
  if (!chars) return '00000000'

  // DJB2 哈希
  let hash = 5381
  for (let i = 0; i < chars.length; i++) {
    hash = ((hash << 5) + hash + chars.charCodeAt(i)) >>> 0
  }

  return hash.toString(16).padStart(8, '0')
}

/**
 * 为段落数组批量生成指纹映射
 * @param {Array} paragraphs 段落数组
 * @returns {Map<string, number>} fingerprint → paragraphIndex
 */
export function buildFingerprintMap(paragraphs) {
  const map = new Map()
  paragraphs.forEach((para, idx) => {
    const fp = computeFingerprint(para.text)
    // 冲突时保留第一个匹配（通常不会冲突）
    if (!map.has(fp)) {
      map.set(fp, idx)
    }
  })
  return map
}

/**
 * 将批注吸附到当前段落
 * @param {Array} annotations 批注数组 [{ fingerprint, message, type, ... }]
 * @param {Map} fingerprintMap 段落指纹映射
 * @returns {{ attached: Array, orphaned: Array }}
 */
export function attachAnnotations(annotations, fingerprintMap) {
  const attached = []
  const orphaned = []

  for (const anno of annotations) {
    if (!anno.fingerprint) {
      orphaned.push(anno)
      continue
    }

    const paraIdx = fingerprintMap.get(anno.fingerprint)
    if (paraIdx != null) {
      attached.push({ ...anno, paragraphIdx: paraIdx })
    } else {
      orphaned.push({ ...anno, reason: 'fingerprint_mismatch' })
    }
  }

  return { attached, orphaned }
}


// ============================================================
// TTS 段落指纹 — 基于完整文本内容 hash（不截断）
// ============================================================

/**
 * 计算 TTS 专用段落指纹
 * 与展示用指纹不同，TTS 指纹使用完整文本以精确感知任何变更。
 * @param {string} text 段落全文
 * @returns {string} 8 位十六进制指纹
 */
export function computeTtsFingerprint(text) {
  if (!text) return '00000000'
  // 标准化：去除首尾空白、折叠连续空白
  const normalized = text.trim().replace(/\s+/g, ' ')
  if (!normalized) return '00000000'

  let hash = 5381
  for (let i = 0; i < normalized.length; i++) {
    hash = ((hash << 5) + hash + normalized.charCodeAt(i)) >>> 0
  }
  // V-04: 附加文本长度，增强抗碰撞性（与 Python 端 _compute_tts_fingerprint 一致）
  return hash.toString(16).padStart(8, '0') + '_' + normalized.length
}

/**
 * 中文分句（与 userscript splitSentences 保持一致）
 * @param {string} text 段落全文
 * @returns {string[]} 句子数组
 */
export function splitSentences(text) {
  if (!text) return []
  const parts = text.split(/([。！？；\n]+)/)
  const sentences = []
  let current = ''

  for (let i = 0; i < parts.length; i++) {
    current += parts[i]
    if ((i % 2 === 1 || i === parts.length - 1) && current.trim()) {
      sentences.push(current.trim())
      current = ''
    }
  }

  if (sentences.length === 0 && text.trim()) {
    sentences.push(text.trim())
  }
  return sentences
}
