/**
 * TtsSegmentContext — 豆包 TTS 段落播放引擎（文件系统持久化模式）
 *
 * 核心能力:
 *   1. 段落级 TTS 提取（通过 doubao.com 弹窗中继）
 *   2. 音频持久化到本地文件系统（通过 Vite 中间件 POST /api/tts/save）
 *   3. 段落播放 / 全段顺序播放
 *   4. manifest.json 批量状态检测（O(1) 判定 ready/missing）
 *
 * V3 架构重构:
 *   - 去除 IndexedDB 依赖，改用文件系统存储 + HTTP 静态服务
 *   - 音频文件存储在 {课程}/weeks/{周次}/tts/{fp}.aac (SSOT: 源文件保持原始格式)
 *   - manifest.json 做批量状态快速检测
 *   - 支持跨浏览器共享 + Netlify 静态部署 (SSG 构建时统一转码为 MP3)
 *   - 保留 V2 的段落索引主键、ref 防 stale closure 等改进
 */
import { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react'
import {
  ttsSingleChunk,
  getAudioDuration,
  combineAudioBlobs,
  loadCredentials,
  saveCredentials,
  clearCredentials as clearStoredCredentials,
  isBridgeAlive,
  closeBridge,
  SPEAKERS,
} from '../utils/doubao-tts'

const TtsSegmentContext = createContext(null)

export function useTtsSegments() {
  return useContext(TtsSegmentContext)
}

// ============ 环境判断 ============
const IS_DEV = import.meta.env.DEV  // Vite 注入：开发态 true，生产构建 false

// ============ 文件系统持久化工具 ============

/**
 * 将音频 Blob 通过 Vite 中间件保存到本地文件系统
 * ⚠️ 仅开发态可用（生产态无 Vite 中间件）
 *
 * 二进制协议: [4B headerLen][headerJSON][audioBytes]
 */
async function saveTtsToFilesystem(courseId, weekName, fp, blob, durationMs) {
  if (!IS_DEV) {
    console.warn('[TTS] saveTtsToFilesystem 仅在开发态可用')
    return { ok: false }
  }

  const header = JSON.stringify({ courseId, weekName, fp, durationMs })
  const headerBuf = new TextEncoder().encode(header)
  const audioBuf = new Uint8Array(await blob.arrayBuffer())

  // 组装二进制包：4字节长度 + header + audio
  const packet = new Uint8Array(4 + headerBuf.length + audioBuf.length)
  const view = new DataView(packet.buffer)
  view.setUint32(0, headerBuf.length) // 大端
  packet.set(headerBuf, 4)
  packet.set(audioBuf, 4 + headerBuf.length)

  const res = await fetch('/api/tts/save', {
    method: 'POST',
    body: packet.buffer,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Unknown' }))
    throw new Error(`保存失败: ${err.error}`)
  }

  return res.json()
}

/**
 * 获取指定 week 的 TTS manifest（批量状态检测）
 *
 * V-05 fix: 双轨环境分离
 *   - 开发态: GET /api/tts/manifest?course=X&week=Y（Vite 中间件）
 *   - 生产态: GET /assets/tts/manifest.json（SSG 构建产物）
 */
async function fetchTtsManifest(courseId, weekName) {
  try {
    const url = IS_DEV
      ? `/api/tts/manifest?course=${encodeURIComponent(courseId)}&week=${encodeURIComponent(weekName)}`
      : `/assets/tts/manifest.json`
    const res = await fetch(url)
    if (!res.ok) return { segments: {} }
    return res.json()
  } catch {
    return { segments: {} }
  }
}

/**
 * 构建 TTS 音频文件的 HTTP URL
 *
 * V-06 fix: 双轨环境分离
 *   - 开发态: /courses/{courseId}/weeks/{weekName}/tts/{fp}.aac (Vite 代理，支持双后缀回退)
 *   - 生产态: 优先使用 staticTtsUrl (by build-ssg.js)，回退到 /assets/tts/{fp}.mp3
 */
function getTtsAudioUrl(courseId, weekName, fp, staticTtsUrl) {
  if (!IS_DEV) {
    // 生产态：SSG 构建时已将音频转码到 /assets/tts/
    return staticTtsUrl || `/assets/tts/${fp}.mp3`
  }
  // 开发态：通过 Vite 代理直接请求原始 .aac
  return `/courses/${encodeURIComponent(courseId)}/weeks/${encodeURIComponent(weekName)}/tts/${fp}.aac`
}

// ============ IndexedDB 迁移工具（一次性导出）============

const IDB_NAME = 'h5_tts_cache'
const IDB_STORE = 'segments'

/**
 * 从 IndexedDB 读取所有缓存条目（用于迁移）
 */
function readAllFromIndexedDB() {
  return new Promise((resolve) => {
    try {
      const req = indexedDB.open(IDB_NAME, 1)
      req.onupgradeneeded = () => {
        // 数据库不存在，无需迁移
        resolve([])
      }
      req.onsuccess = () => {
        const db = req.result
        if (!db.objectStoreNames.contains(IDB_STORE)) {
          resolve([])
          return
        }
        const tx = db.transaction(IDB_STORE, 'readonly')
        const store = tx.objectStore(IDB_STORE)
        const getAll = store.getAll()
        getAll.onsuccess = () => resolve(getAll.result || [])
        getAll.onerror = () => resolve([])
      }
      req.onerror = () => resolve([])
    } catch {
      resolve([])
    }
  })
}

// ============ Provider ============

export function TtsSegmentProvider({ children, courseId, weekName }) {
  /**
   * segmentMap 以段落索引为主键
   * { [paraIndex]: { status, blobUrl, durationMs, text, ttsFp } }
   *   status: 'ready' | 'extracting' | 'missing' | 'error' | 'playing'
   */
  const [segmentMap, setSegmentMap] = useState({})
  const [credentials, setCredentials] = useState(null)
  const [isCredentialValid, setIsCredentialValid] = useState(null)
  const [extractProgress, setExtractProgress] = useState(null)
  const [manifest, setManifest] = useState(null)  // 当前 week 的 TTS manifest
  const isExtracting = useRef(false)
  const audioRef = useRef(null)
  const currentPlayingIdx = useRef(null)
  const isChainPlaying = useRef(false)

  // 使用 ref 持有最新 segmentMap，避免 stale closure
  const segmentMapRef = useRef(segmentMap)
  useEffect(() => { segmentMapRef.current = segmentMap }, [segmentMap])

  // 持有 courseId/weekName 的 ref（供回调使用）
  const courseIdRef = useRef(courseId)
  const weekNameRef = useRef(weekName)
  useEffect(() => { courseIdRef.current = courseId }, [courseId])
  useEffect(() => { weekNameRef.current = weekName }, [weekName])

  // 加载凭证
  useEffect(() => {
    const creds = loadCredentials()
    if (creds) {
      setCredentials(creds)
      setIsCredentialValid(null)
    }
  }, [])

  /**
   * 配置凭证
   */
  const configureCredentials = useCallback(async (config) => {
    saveCredentials(config)
    setCredentials(config)
    setIsCredentialValid(true)
    return true
  }, [])

  /**
   * V3: 从文件系统 manifest 计算段落状态
   *
   * 策略:
   *   1. fetch manifest.json → 获取所有已缓存的 fp 列表
   *   2. 对每个段落，若其 ttsFp 存在于 manifest → status: ready
   *   3. 否则 → status: missing
   *   4. ready 的段落通过 HTTP URL 直接播放，无需预加载 Blob
   */
  const computeStatus = useCallback(async (paragraphs) => {
    const cId = courseIdRef.current
    const wk = weekNameRef.current

    if (!cId || !wk) return {}

    // 获取 manifest（包含所有已缓存段落的 fp + 时长信息）
    const mf = await fetchTtsManifest(cId, wk)
    setManifest(mf)

    const prevMap = segmentMapRef.current
    const newMap = {}

    for (let i = 0; i < paragraphs.length; i++) {
      const para = paragraphs[i]
      const fp = para.ttsFp
      if (!fp || fp.startsWith('00000000')) continue

      // 检查是否正在播放（保留播放状态）
      const prev = prevMap[i]
      if (prev && prev.ttsFp === fp && prev.status === 'playing') {
        newMap[i] = prev
        continue
      }

      // 检查 manifest 中是否存在
      if (mf.segments && mf.segments[fp]) {
        const cached = mf.segments[fp]
        newMap[i] = {
          status: 'ready',
          blobUrl: getTtsAudioUrl(cId, wk, fp, para.staticTtsUrl), // V-06: 生产态使用 staticTtsUrl
          durationMs: cached.durationMs || 0,
          text: para.text,
          ttsFp: fp,
        }
      } else {
        newMap[i] = {
          status: 'missing',
          blobUrl: null,
          durationMs: null,
          text: para.text,
          ttsFp: fp,
        }
      }
    }

    const readyCount = Object.values(newMap).filter(s => s.status === 'ready').length
    const missingCount = Object.values(newMap).filter(s => s.status === 'missing').length
    console.log(`[TTS] computeStatus: ${readyCount} ready, ${missingCount} missing (manifest: ${Object.keys(mf.segments || {}).length} entries)`)

    setSegmentMap(newMap)
    return newMap
  }, [])

  /**
   * V3: 提取单个段落 TTS → 保存到本地文件系统
   */
  const extractSingle = useCallback(async (paraIndex, ttsFp, text) => {
    if (!isBridgeAlive()) throw new Error('桥接弹窗未打开，请先连接豆包')

    const cId = courseIdRef.current
    const wk = weekNameRef.current

    // 标记为 extracting
    setSegmentMap(prev => ({
      ...prev,
      [paraIndex]: { ...prev[paraIndex], status: 'extracting', text, ttsFp },
    }))

    try {
      const result = await ttsSingleChunk(text, {
        fp: ttsFp,
        speaker: credentials?.speaker,
      })

      const durationMs = result.durationMs || await getAudioDuration(result.blob)

      // 保存到文件系统
      await saveTtsToFilesystem(cId, wk, ttsFp, result.blob, durationMs)

      // 更新内存中的 manifest
      setManifest(prev => {
        const updated = { ...prev, segments: { ...(prev?.segments || {}) } }
        updated.segments[ttsFp] = { durationMs, size: result.blob.size, cachedAt: Date.now() }
        return updated
      })

      // 为即时播放创建 blobUrl（后续播放可用 HTTP URL）
      const blobUrl = URL.createObjectURL(result.blob)

      setSegmentMap(prev => ({
        ...prev,
        [paraIndex]: {
          status: 'ready',
          blobUrl, // 首次使用 blobUrl，后续 computeStatus 会切换为 HTTP URL
          durationMs,
          text,
          ttsFp,
        },
      }))

      return { success: true, durationMs }
    } catch (err) {
      setSegmentMap(prev => ({
        ...prev,
        [paraIndex]: {
          ...prev[paraIndex],
          status: 'error',
          errorMsg: err.message,
        },
      }))
      return { success: false, error: err.message }
    }
  }, [credentials])

  /**
   * 批量提取 — 带 try/catch 防永久阻塞
   */
  const extractAll = useCallback(async (paragraphs) => {
    if (!isBridgeAlive() || isExtracting.current) return

    const missingEntries = []
    for (let i = 0; i < paragraphs.length; i++) {
      const fp = paragraphs[i].ttsFp
      if (!fp || fp.startsWith('00000000')) continue
      const seg = segmentMapRef.current[i]
      if (!seg || seg.status === 'missing' || seg.status === 'error') {
        missingEntries.push({ index: i, para: paragraphs[i] })
      }
    }

    if (missingEntries.length === 0) return

    isExtracting.current = true
    const total = missingEntries.length
    let success = 0
    let failed = 0

    try {
      for (let i = 0; i < missingEntries.length; i++) {
        const { index, para } = missingEntries[i]
        setExtractProgress({
          current: i + 1,
          total,
          text: para.text.slice(0, 30) + '...',
        })

        try {
          const result = await extractSingle(index, para.ttsFp, para.text)
          if (result.success) success++
          else failed++
        } catch (err) {
          console.error(`[TTS] 提取异常 (段落 ${index}): ${err.message}`)
          failed++
        }

        // 段间延迟
        if (i < missingEntries.length - 1) {
          const delay = 1000 + Math.random() * 1000
          if ((i + 1) % 20 === 0) {
            await new Promise(r => setTimeout(r, 5000 + Math.random() * 2000))
          } else {
            await new Promise(r => setTimeout(r, delay))
          }
        }
      }
    } finally {
      isExtracting.current = false
      setExtractProgress(null)
    }

    return { success, failed, total }
  }, [credentials, extractSingle])

  /**
   * 播放单个段落 — 使用 HTTP URL 或 blobUrl
   */
  const playSegment = useCallback((paraIndex) => {
    const seg = segmentMapRef.current[paraIndex]
    if (!seg || !seg.blobUrl) return

    // 停止当前播放
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current = null
      if (currentPlayingIdx.current != null) {
        const prevIdx = currentPlayingIdx.current
        setSegmentMap(prev => ({
          ...prev,
          [prevIdx]: {
            ...prev[prevIdx],
            status: 'ready',
          },
        }))
      }
    }

    const audio = new Audio(seg.blobUrl)
    audioRef.current = audio
    currentPlayingIdx.current = paraIndex

    setSegmentMap(prev => ({
      ...prev,
      [paraIndex]: { ...prev[paraIndex], status: 'playing' },
    }))

    audio.onended = () => {
      setSegmentMap(prev => ({
        ...prev,
        [paraIndex]: { ...prev[paraIndex], status: 'ready' },
      }))
      audioRef.current = null
      currentPlayingIdx.current = null
    }

    audio.onerror = () => {
      setSegmentMap(prev => ({
        ...prev,
        [paraIndex]: { ...prev[paraIndex], status: 'ready' },
      }))
      audioRef.current = null
      currentPlayingIdx.current = null
    }

    isChainPlaying.current = false
    audio.play()
  }, [])

  /**
   * 停止播放
   */
  const stopPlayback = useCallback(() => {
    isChainPlaying.current = false
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current = null
    }
    if (currentPlayingIdx.current != null) {
      const idx = currentPlayingIdx.current
      setSegmentMap(prev => ({
        ...prev,
        [idx]: { ...prev[idx], status: 'ready' },
      }))
      currentPlayingIdx.current = null
    }
  }, [])

  /**
   * 从指定段落开始连播
   */
  const playFrom = useCallback((startIndex, paragraphs) => {
    stopPlayback()
    isChainPlaying.current = true

    const playNext = (idx) => {
      if (!isChainPlaying.current) return

      while (idx < paragraphs.length) {
        const fp = paragraphs[idx].ttsFp
        const seg = segmentMapRef.current[idx]
        if (fp && !fp.startsWith('00000000') && seg?.status === 'ready' && seg?.blobUrl) break
        idx++
      }

      if (idx >= paragraphs.length) {
        isChainPlaying.current = false
        return
      }

      const seg = segmentMapRef.current[idx]
      const audio = new Audio(seg.blobUrl)
      audioRef.current = audio
      currentPlayingIdx.current = idx

      setSegmentMap(prev => ({
        ...prev,
        [idx]: { ...prev[idx], status: 'playing' },
      }))

      audio.onended = () => {
        setSegmentMap(prev => ({
          ...prev,
          [idx]: { ...prev[idx], status: 'ready' },
        }))
        audioRef.current = null
        currentPlayingIdx.current = null
        if (isChainPlaying.current) playNext(idx + 1)
      }

      audio.onerror = () => {
        setSegmentMap(prev => ({
          ...prev,
          [idx]: { ...prev[idx], status: 'ready' },
        }))
        audioRef.current = null
        currentPlayingIdx.current = null
        if (isChainPlaying.current) playNext(idx + 1)
      }

      audio.play()
    }

    playNext(startIndex)
    return true
  }, [stopPlayback])

  /**
   * 播放完整模块
   */
  const playAll = useCallback(async (paragraphs) => {
    return playFrom(0, paragraphs)
  }, [playFrom])

  /**
   * 统计信息
   */
  const getStats = useCallback(() => {
    const entries = Object.values(segmentMapRef.current)
    return {
      total: entries.length,
      ready: entries.filter(e => e.status === 'ready').length,
      missing: entries.filter(e => e.status === 'missing').length,
      extracting: entries.filter(e => e.status === 'extracting').length,
      error: entries.filter(e => e.status === 'error').length,
      playing: entries.filter(e => e.status === 'playing').length,
    }
  }, [])

  /**
   * V3: 从 IndexedDB 迁移到文件系统（一次性操作）
   *
   * 遍历 IndexedDB 中的所有条目，逐个 POST 到 /api/tts/save
   * 需要知道 courseId 和 weekName — 从当前上下文获取
   */
  const migrateFromIndexedDB = useCallback(async (onProgress) => {
    const cId = courseIdRef.current
    const wk = weekNameRef.current
    if (!cId || !wk) return { migrated: 0, failed: 0 }

    const entries = await readAllFromIndexedDB()
    if (entries.length === 0) return { migrated: 0, failed: 0 }

    let migrated = 0
    let failed = 0

    for (let i = 0; i < entries.length; i++) {
      const entry = entries[i]
      if (!entry.fp || !entry.blob) continue

      onProgress?.({
        current: i + 1,
        total: entries.length,
        fp: entry.fp,
      })

      try {
        await saveTtsToFilesystem(cId, wk, entry.fp, entry.blob, entry.durationMs || 0)
        migrated++
      } catch (err) {
        console.warn(`[TTS Migration] 迁移失败 ${entry.fp}: ${err.message}`)
        failed++
      }
    }

    console.log(`[TTS Migration] 迁移完成: ${migrated} 成功, ${failed} 失败 (共 ${entries.length})`)
    return { migrated, failed, total: entries.length }
  }, [])

  const value = {
    // 状态
    segmentMap,
    credentials,
    isCredentialValid,
    extractProgress,
    manifest,
    // 凭证管理
    configureCredentials,
    clearCredentials: useCallback(() => {
      clearStoredCredentials()
      closeBridge()
      setCredentials(null)
      setIsCredentialValid(null)
    }, []),
    isBridgeAlive,
    // TTS 操作
    computeStatus,
    extractSingle,
    extractAll,
    // 播放操作
    playSegment,
    stopPlayback,
    playFrom,
    playAll,
    // 迁移
    migrateFromIndexedDB,
    // 工具
    getStats,
    speakers: SPEAKERS,
  }

  return (
    <TtsSegmentContext.Provider value={value}>
      {children}
    </TtsSegmentContext.Provider>
  )
}
