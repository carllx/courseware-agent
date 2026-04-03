import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * AudioPlayer — 音频播放器 + SRT 字幕同步
 *
 * 当 slides.json 中 media.audio 存在时渲染。
 * 支持播放/暂停、进度条、当前字幕高亮。
 *
 * Props:
 *   audioSrc      — 音频文件 URL
 *   srtSrc        — SRT 字幕文件 URL
 *   onTimeUpdate  — (currentTime, currentSubIdx) => void, 向 App 报告播放状态
 *   onSubtitlesLoaded — (cues[]) => void, SRT 解析完成后传出 cue 列表
 *   seekToTime    — 外部控制：当该值变化时，音频跳转到指定时间（秒）
 */
export default function AudioPlayer({
  audioSrc,
  srtSrc,
  onTimeUpdate: onTimeUpdateProp,
  onSubtitlesLoaded,
  seekToTime,
  onSubtitleClick,
}) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [subtitles, setSubtitles] = useState([])
  const [currentSubIdx, setCurrentSubIdx] = useState(-1)

  // 加载 SRT 字幕
  useEffect(() => {
    if (!srtSrc) return
    fetch(srtSrc)
      .then(res => res.text())
      .then(text => {
        const cues = parseSRT(text)
        setSubtitles(cues)
        // 字幕加载完成后通知 App 层
        onSubtitlesLoaded?.(cues)
      })
      .catch(err => console.warn("SRT 加载失败:", err))
  }, [srtSrc]) // eslint-disable-line react-hooks/exhaustive-deps

  // 外部 seek 控制：当 seekToTime 变化时跳转音频
  useEffect(() => {
    const audio = audioRef.current
    if (audio && seekToTime != null && isFinite(seekToTime)) {
      audio.currentTime = seekToTime
    }
  }, [seekToTime])

  // 时间更新 → 字幕同步 + 向上报告
  const handleTimeUpdate = useCallback(() => {
    const audio = audioRef.current
    if (!audio) return
    const t = audio.currentTime
    setCurrentTime(t)

    // O(log n) 二分查找当前字幕
    if (subtitles.length === 0) return
    let lo = 0, hi = subtitles.length - 1, idx = -1
    while (lo <= hi) {
      const mid = (lo + hi) >> 1
      if (t >= subtitles[mid].start && t <= subtitles[mid].end) {
        idx = mid
        break
      }
      if (t < subtitles[mid].start) hi = mid - 1
      else lo = mid + 1
    }
    setCurrentSubIdx(idx)

    // 向 App 层报告播放进度和当前字幕索引
    onTimeUpdateProp?.(t, idx)
  }, [subtitles, onTimeUpdateProp])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return
    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e) => {
    const audio = audioRef.current
    if (!audio || !duration) return
    const rect = e.currentTarget.getBoundingClientRect()
    const ratio = (e.clientX - rect.left) / rect.width
    audio.currentTime = ratio * duration
  }

  const handleLoadedMetadata = () => {
    const audio = audioRef.current
    if (audio) setDuration(audio.duration)
  }

  const handleEnded = () => {
    setIsPlaying(false)
  }

  const formatTime = (s) => {
    const m = Math.floor(s / 60)
    const sec = Math.floor(s % 60)
    return `${m}:${sec.toString().padStart(2, '0')}`
  }

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={audioSrc}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={handleEnded}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        preload="metadata"
      />

      <button className="audio-play-btn" onClick={togglePlay}>
        {isPlaying ? '⏸' : '▶'}
      </button>

      <div className="audio-progress" onClick={handleSeek}>
        <div className="audio-progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <span className="audio-time">
        {formatTime(currentTime)} / {formatTime(duration)}
      </span>

      {/* 当前字幕行 */}
      {currentSubIdx >= 0 && subtitles[currentSubIdx] && (
        <div
          className="audio-subtitle clickable"
          onClick={() => onSubtitleClick?.(currentSubIdx)}
          title="点击重听当前句"
        >
          {subtitles[currentSubIdx].text}
        </div>
      )}
    </div>
  )
}

/**
 * 解析 SRT 格式字幕
 */
function parseSRT(text) {
  const cues = []
  const blocks = text.trim().split(/\n\s*\n/)
  for (const block of blocks) {
    const lines = block.trim().split('\n')
    if (lines.length < 3) continue

    // 第二行是时间码
    const timeMatch = lines[1].match(
      /(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})/
    )
    if (!timeMatch) continue

    const start = parseInt(timeMatch[1]) * 3600
      + parseInt(timeMatch[2]) * 60
      + parseInt(timeMatch[3])
      + parseInt(timeMatch[4]) / 1000

    const end = parseInt(timeMatch[5]) * 3600
      + parseInt(timeMatch[6]) * 60
      + parseInt(timeMatch[7])
      + parseInt(timeMatch[8]) / 1000

    const text_content = lines.slice(2).join(' ').trim()

    cues.push({ start, end, text: text_content })
  }
  return cues
}
