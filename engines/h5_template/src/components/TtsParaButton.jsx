/**
 * TtsParaButton — 段落级 TTS 播放/提取按钮
 *
 *   🔊 ready      → 点击播放
 *   ⏸  playing    → 点击停止
 *   ○  missing    → 点击提取（如果有凭证）
 *   ⟳  extracting → 提取中（动画）
 *   ✕  error      → 点击重试
 *
 * V2: 接收 paraIndex 替代旧的纯 ttsFp 主键（V-06 修复）
 */
import { memo, useCallback } from 'react'
import { useTtsSegments } from '../contexts/TtsSegmentContext'
import '../styles/tts-para-button.css'

const STATUS_CONFIG = {
  ready:      { icon: '🔊', title: '点击播放', className: 'tts-ready' },
  playing:    { icon: '⏸',  title: '点击停止', className: 'tts-playing' },
  missing:    { icon: '○',   title: '点击提取语音', className: 'tts-missing' },
  extracting: { icon: '⟳',  title: '提取中...', className: 'tts-extracting' },
  error:      { icon: '✕',   title: '提取失败，点击重试', className: 'tts-error' },
}

function TtsParaButton({ paraIndex, ttsFp, text }) {
  const tts = useTtsSegments()

  const handleClick = useCallback((e) => {
    e.stopPropagation()
    if (!tts) return

    const seg = tts.segmentMap[paraIndex]
    if (!seg) {
      // 不在 map 中 → 尝试提取
      if (tts.credentials && text && ttsFp) {
        tts.extractSingle(paraIndex, ttsFp, text)
      }
      return
    }

    switch (seg.status) {
      case 'playing':
        tts.stopPlayback()
        break
      case 'ready':
        tts.playSegment(paraIndex)
        break
      case 'missing':
      case 'error':
        if (tts.credentials && (seg.text || text) && (seg.ttsFp || ttsFp)) {
          tts.extractSingle(paraIndex, seg.ttsFp || ttsFp, seg.text || text)
        }
        break
      case 'extracting':
        // 不操作
        break
    }
  }, [tts, paraIndex, ttsFp, text])

  if (!tts || !ttsFp || ttsFp.startsWith('00000000') || paraIndex == null) return null

  const seg = tts.segmentMap[paraIndex]
  const status = seg?.status || 'missing'
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.missing
  const isClickable = status !== 'extracting'

  return (
    <button
      className={`tts-para-btn ${config.className}`}
      title={status === 'error' ? `${config.title}: ${seg?.errorMsg || ''}` : config.title}
      onClick={handleClick}
      disabled={!isClickable}
      aria-label={config.title}
    >
      {config.icon}
    </button>
  )
}

export default memo(TtsParaButton)
