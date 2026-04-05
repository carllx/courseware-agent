/**
 * doubao-tts.js — 豆包 TTS 桥接引擎（H5 端）
 *
 * 核心策略：
 *   H5 不直连豆包 WebSocket（会被 Origin 拒绝），
 *   而是通过 doubao.com 弹窗中的桥接脚本 (tts_bridge.user.js) 中继。
 *
 * 数据流:
 *   H5 ──postMessage──→ doubao.com 弹窗
 *                        bridge 调用原版 userscript 的 ttsSingleChunk()
 *   H5 ←──postMessage── 返回 ArrayBuffer (Transferable, 零拷贝)
 *   H5 将 ArrayBuffer → Blob → IndexedDB 缓存
 */

// ============ 音色配置（44个音色与分组）============
const SPEAKERS = {
  // 女声 (13个)
  '温柔桃子': 'zh_female_wenroutaozi_uranus_bigtts',
  '温柔桃子经典': 'zh_female_wenroutaozi_v2_mars_bigtts',
  '知性小棠': 'zh_female_wenroutaozi_mars_bigtts',
  '阳光甜妹': 'zh_female_xiaohe_conversation_wvae_bigtts',
  '邻家女孩': 'zh_female_f261_conversation_wvae_bigtts',
  '魅力苏菲': 'zh_female_sophie_conversation_wvae_bigtts',
  '撒娇学妹': 'zh_female_yuanqinvyou_wvae_bigtts',
  '文静毛毛': 'zh_female_maomao_conversation_wvae_bigtts',
  '北京大妞': 'zh_female_beijingdaniu_mars_bigtts',
  '清甜瑶瑶': 'zh_female_F466_mars_bigtts',
  '活泼可昕': 'zh_female_F765_mars_bigtts',
  '甜美小雪': 'ICL_6acf86286e24',
  '清冷阿梦': 'ICL_16cd9a58768e',
  // 男声 (13个)
  '磁性俊宇': 'zh_male_nuanxinshizhe_mars_bigtts',
  '邻家男孩': 'zh_male_linjiananhai_moon_bigtts',
  '悠悠君子': 'zh_male_M100_conversation_wvae_bigtts',
  '温暖阿虎': 'zh_male_ahu_conversation_wvae_bigtts',
  '少年梓辛': 'zh_male_m286_conversation_wvae_bigtts',
  '阳光阿辰': 'zh_male_qingyiyuxuan_mars_bigtts',
  '傲娇霸总': 'zh_male_aojiaobazong_wvae_bigtts',
  '温柔子言': 'zh_male_cheng_mars_bigtts',
  '率性阿哲': 'zh_male_litiebanzi_mars_bigtts',
  '深夜播客': 'zh_male_shenyeboke_wvae_bigtts',
  '东方浩然': 'zh_male_dongfanghaoran_moon_bigtts',
  '清爽男大': 'zh_male_junlangxize_mars_bigtts',
  '渊博小叔': 'zh_male_m219_conversation_wvae_bigtts',
  // 特色音色 (18个)
  '腹黑霸总': 'ICL_c021bc19bf92',
  '冷酷霸总': 'ICL_e0b9b93ee322',
  '霸道总裁': 'ICL_d4d40acd33dd',
  '温柔陆辰': 'ICL_df4fc4d1ce4b',
  '病娇少爷': 'ICL_72afa6c5dc07',
  '清朗宇澄': 'ICL_9b3bc6941076',
  '奶音俊少': 'ICL_932b3f52bf3d',
  '沉稳皓轩': 'ICL_5a413fbc14fc',
  '温柔俊彦': 'ICL_0ce6ef379e73',
  '青涩沐阳': 'ICL_afedffe4586c',
  '睿语舟舟': 'ICL_4ce34d3f60f4',
  '随性先生': 'ICL_b718c1050dd1',
  '俊朗男友': 'ICL_1eed9233299f',
  '奶酷小宇': 'ICL_b22cd40ccd3e',
  '暖阳阿晨': 'ICL_7a33516fe388',
  '低音小北': 'ICL_989e59f0082a',
  '男闺蜜俊熙': 'ICL_7ba54f5a883e',
  '深情霸总': 'ICL_6e69deb80ce5',
}

const SPEAKER_GROUPS = {
  '女声': ['温柔桃子', '温柔桃子经典', '知性小棠', '阳光甜妹', '邻家女孩', '魅力苏菲', '撒娇学妹', '文静毛毛', '北京大妞', '清甜瑶瑶', '活泼可昕', '甜美小雪', '清冷阿梦'],
  '男声': ['磁性俊宇', '邻家男孩', '悠悠君子', '温暖阿虎', '少年梓辛', '阳光阿辰', '傲娇霸总', '温柔子言', '率性阿哲', '深夜播客', '东方浩然', '清爽男大', '渊博小叔'],
  '特色': ['腹黑霸总', '冷酷霸总', '霸道总裁', '温柔陆辰', '病娇少爷', '清朗宇澄', '奶音俊少', '沉稳皓轩', '温柔俊彦', '青涩沐阳', '睿语舟舟', '随性先生', '俊朗男友', '奶酷小宇', '暖阳阿晨', '低音小北', '男闺蜜俊熙', '深情霸总'],
}

const DEFAULT_SPEAKER = 'zh_female_wenroutaozi_uranus_bigtts'

// ============ 凭证管理 ============
const STORAGE_KEY = 'h5_doubao_tts_config'

export function saveCredentials(config) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    device_id: config.device_id,
    web_id: config.web_id,
    speaker: config.speaker || '温柔桃子',
    hasUserscript: config.hasUserscript || false,
    savedAt: new Date().toISOString(),
  }))
}

export function loadCredentials() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch { return null }
}

export function clearCredentials() {
  localStorage.removeItem(STORAGE_KEY)
}

// ============ 弹窗管理 ============

let bridgePopup = null
let pendingRequests = new Map() // requestId → {resolve, reject, timer}
let requestIdCounter = 0

/**
 * 获取或打开桥接弹窗
 */
function getBridgePopup() {
  if (bridgePopup && !bridgePopup.closed) return bridgePopup
  return null
}

/**
 * 打开豆包弹窗并等待凭证 + 桥接就绪
 */
export function openDoubaoAndGetCredentials(onStatus = () => {}) {
  return new Promise((resolve) => {
    onStatus('🔗 正在打开豆包...')

    bridgePopup = window.open(
      'https://www.doubao.com/chat/',
      'doubao_tts_bridge',
      'width=500,height=400,left=100,top=100'
    )

    if (!bridgePopup) {
      onStatus('❌ 弹窗被拦截，请允许弹窗后重试')
      resolve(null)
      return
    }

    onStatus('⏳ 等待桥接脚本...')
    let resolved = false

    const handleMessage = (event) => {
      if (event.data?.type === 'h5_tts_credentials') {
        resolved = true
        window.removeEventListener('message', handleMessage)
        clearInterval(pollTimer)

        const creds = {
          device_id: event.data.device_id,
          web_id: event.data.web_id,
          hasUserscript: event.data.hasUserscript,
        }

        onStatus(creds.hasUserscript
          ? '✅ 已连接！TTS 引擎就绪'
          : '⚠️ 凭证已获取，但原版 TTS 脚本未检测到')

        // 不关闭弹窗！保持作为提取中继
        resolve(creds)
      } else if (event.data?.type === 'h5_tts_credentials_error') {
        resolved = true
        window.removeEventListener('message', handleMessage)
        clearInterval(pollTimer)
        onStatus(`❌ ${event.data.error}`)
        resolve(null)
      }
    }

    window.addEventListener('message', handleMessage)

    // 主动轮询请求凭证（V-01 补丁：桥接在跨域下无法自动推送，需要 H5 主动请求）
    const pollTimer = setInterval(() => {
      if (resolved || !bridgePopup || bridgePopup.closed) {
        clearInterval(pollTimer)
        return
      }
      try {
        bridgePopup.postMessage(
          { type: 'h5_tts_request_credentials' },
          'https://www.doubao.com'
        )
      } catch { /* ignore */ }
    }, 2000) // 每 2 秒请求一次

    // 超时
    setTimeout(() => {
      if (!resolved) {
        resolved = true
        window.removeEventListener('message', handleMessage)
        clearInterval(pollTimer)
        onStatus('⏰ 超时。请确保已安装 TTS 桥接脚本 (tts_bridge.user.js)')
        resolve(null)
      }
    }, 30000)

    // 弹窗被关闭
    const checkClosed = setInterval(() => {
      if (bridgePopup?.closed && !resolved) {
        resolved = true
        clearInterval(checkClosed)
        clearInterval(pollTimer)
        window.removeEventListener('message', handleMessage)
        onStatus('弹窗已关闭（需要保持打开以提取 TTS）')
        resolve(null)
      }
      if (resolved) clearInterval(checkClosed)
    }, 500)
  })
}

/**
 * 检查桥接弹窗是否活跃
 */
export function isBridgeAlive() {
  return bridgePopup && !bridgePopup.closed
}

/**
 * 关闭桥接弹窗
 */
export function closeBridge() {
  if (bridgePopup && !bridgePopup.closed) {
    bridgePopup.close()
  }
  bridgePopup = null
}

// ============ 消息路由（接收 bridge 的响应）============

if (typeof window !== 'undefined') {
  window.addEventListener('message', (event) => {
    const { type, requestId } = event.data || {}

    if (type === 'h5_tts_extract_result' && requestId) {
      const pending = pendingRequests.get(requestId)
      if (!pending) return

      pendingRequests.delete(requestId)
      clearTimeout(pending.timer)

      if (event.data.success) {
        pending.resolve({
          blob: new Blob([event.data.audioBuffer], { type: event.data.mimeType || 'audio/aac' }),
          durationMs: event.data.durationMs || 0,
        })
      } else {
        pending.reject(new Error(event.data.error || '提取失败'))
      }
    }
  })
}

// ============ 核心 TTS 提取（通过 bridge 中继）============

/**
 * 通过桥接弹窗提取单段 TTS
 * @param {string} text - 要合成的文本
 * @param {Object} options - {speaker}
 * @returns {Promise<{blob: Blob, durationMs: number}>}
 */
export function ttsSingleChunk(text, options = {}) {
  return new Promise((resolve, reject) => {
    const popup = getBridgePopup()
    if (!popup) {
      reject(new Error('桥接弹窗未打开。请先点击"连接豆包"'))
      return
    }

    const requestId = `tts_${++requestIdCounter}_${Date.now()}`

    // 超时 60 秒
    const timer = setTimeout(() => {
      pendingRequests.delete(requestId)
      reject(new Error('提取超时 (60s)'))
    }, 60000)

    pendingRequests.set(requestId, { resolve, reject, timer })

    // 发送提取请求
    popup.postMessage({
      type: 'h5_tts_extract',
      fp: options.fp || requestId,
      text,
      speaker: options.speaker,
      requestId,
    }, 'https://www.doubao.com')
  })
}

// ============ 音频工具 ============

/**
 * 获取音频 Blob 的时长（毫秒）
 */
export function getAudioDuration(blob) {
  return new Promise((resolve) => {
    const url = URL.createObjectURL(blob)
    const audio = new Audio(url)
    audio.addEventListener('loadedmetadata', () => {
      resolve(audio.duration * 1000)
      URL.revokeObjectURL(url)
    })
    audio.addEventListener('error', () => {
      resolve(0)
      URL.revokeObjectURL(url)
    })
  })
}

/**
 * 合并多段音频 Blob（Web Audio API + 交叉淡化）
 */
export async function combineAudioBlobs(blobs) {
  if (blobs.length === 0) return new Blob([], { type: 'audio/aac' })
  if (blobs.length === 1) return blobs[0]

  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const audioBuffers = []

  for (const blob of blobs) {
    try {
      const arrayBuffer = await blob.arrayBuffer()
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
      audioBuffers.push(audioBuffer)
    } catch (e) {
      console.warn('解码分段音频失败:', e)
    }
  }

  if (audioBuffers.length === 0) {
    await audioContext.close()
    return new Blob(blobs, { type: 'audio/aac' })
  }

  const sampleRate = audioBuffers[0].sampleRate
  let totalSamples = 0
  for (const buf of audioBuffers) totalSamples += buf.length

  const fadeSamples = Math.floor(sampleRate * 0.005)
  const combinedBuffer = audioContext.createBuffer(1, totalSamples, sampleRate)
  const output = combinedBuffer.getChannelData(0)

  let offset = 0
  for (const buf of audioBuffers) {
    const input = buf.getChannelData(0)
    for (let j = 0; j < buf.length; j++) {
      let sample = input[j]
      if (j < fadeSamples) sample *= j / fadeSamples
      if (j >= buf.length - fadeSamples) sample *= (buf.length - j) / fadeSamples
      output[offset + j] = sample
    }
    offset += buf.length
  }

  const wavBlob = audioBufferToWav(combinedBuffer)
  await audioContext.close()
  return wavBlob
}

function audioBufferToWav(buffer) {
  const sampleRate = buffer.sampleRate
  const samples = buffer.getChannelData(0)
  const dataLength = samples.length * 2
  const bufferLength = 44 + dataLength

  const ab = new ArrayBuffer(bufferLength)
  const view = new DataView(ab)

  const writeStr = (off, str) => { for (let i = 0; i < str.length; i++) view.setUint8(off + i, str.charCodeAt(i)) }

  writeStr(0, 'RIFF')
  view.setUint32(4, bufferLength - 8, true)
  writeStr(8, 'WAVE')
  writeStr(12, 'fmt ')
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true)
  view.setUint16(22, 1, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * 2, true)
  view.setUint16(32, 2, true)
  view.setUint16(34, 16, true)
  writeStr(36, 'data')
  view.setUint32(40, dataLength, true)

  let offset = 44
  for (let i = 0; i < samples.length; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true)
    offset += 2
  }

  return new Blob([ab], { type: 'audio/wav' })
}

// ============ 导出 ============
export { SPEAKERS, SPEAKER_GROUPS, DEFAULT_SPEAKER }
