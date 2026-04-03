import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import SlideFactory from '../components/SlideFactory'
import TextPanel from '../components/TextPanel'
import NavigationBar from '../components/NavigationBar'
import AudioPlayer from '../components/AudioPlayer'

/**
 * LessonViewer — 单讲预览器
 *
 * 从原 App.jsx 重构而来，现在通过路由参数
 * /:courseId/:scriptName 加载对应的分讲 JSON。
 *
 * 功能保持不变：幻灯片 + 文本面板 + 音频联动。
 */
export default function LessonViewer() {
  const { courseId, scriptName } = useParams()
  const [manifest, setManifest] = useState(null)
  const [error, setError] = useState(null)
  const [currentSectionIdx, setCurrentSectionIdx] = useState(0)
  const [currentSlideIdx, setCurrentSlideIdx] = useState(0)

  // === 联动状态 ===
  const [srtCues, setSrtCues] = useState([])
  const [activeParagraphIdx, setActiveParagraphIdx] = useState(-1)
  const [seekToTime, setSeekToTime] = useState(null)
  const isAudioDriving = useRef(false)
  const [hotReloadToast, setHotReloadToast] = useState(null)

  // === HMR 热重载监听 ===
  useEffect(() => {
    if (!import.meta.hot) return

    const handleReload = (data) => {
      console.log('[h5-hot-reload] 收到重载通知', data)
      const jsonUrl = `/courses/${courseId}/${scriptName}.json`
      fetch(jsonUrl + '?t=' + Date.now())
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`)
          return res.json()
        })
        .then(newData => {
          setManifest(newData)
          // 注入主题（热重载时也需要刷新）
          if (newData.theme) {
            const root = document.documentElement
            Object.entries(newData.theme).forEach(([key, value]) => {
              if (typeof value !== 'string') return
              root.style.setProperty(`--theme-${key}`, value)
            })
          }
          document.title = `${newData.script} — ${newData.course}`
          // Toast 提示
          const label = data.elapsed ? `${data.elapsed}ms` : ''
          setHotReloadToast(`🔄 已自动刷新 ${label}`)
          setTimeout(() => setHotReloadToast(null), 2500)
        })
        .catch(err => {
          console.error('[h5-hot-reload] Re-fetch 失败:', err)
        })
    }

    const handleError = (data) => {
      console.warn('[h5-hot-reload] 重建出错:', data.error?.slice(0, 200))
      setHotReloadToast(`❌ 重建失败: ${data.moduleName || '未知模块'}`)
      setTimeout(() => setHotReloadToast(null), 5000)
    }

    import.meta.hot.on('h5:reload', handleReload)
    import.meta.hot.on('h5:error', handleError)
  }, [courseId, scriptName])

  // === 热重载后的位置钳位（防止 section/slide 越界）===
  useEffect(() => {
    if (!manifest) return
    const maxSection = Math.max(0, manifest.sections.length - 1)
    setCurrentSectionIdx(prev => prev > maxSection ? maxSection : prev)
  }, [manifest])

  useEffect(() => {
    if (!manifest) return
    const section = manifest.sections[currentSectionIdx]
    if (!section) return
    const maxSlide = Math.max(0, (section.slides?.length || 1) - 1)
    setCurrentSlideIdx(prev => prev > maxSlide ? maxSlide : prev)
  }, [manifest, currentSectionIdx])

  // 加载数据
  useEffect(() => {
    // 重置状态
    setManifest(null)
    setError(null)
    setCurrentSectionIdx(0)
    setCurrentSlideIdx(0)
    setSrtCues([])
    setActiveParagraphIdx(-1)
    setSeekToTime(null)

    const jsonUrl = `/courses/${courseId}/${scriptName}.json`
    fetch(jsonUrl)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(data => {
        setManifest(data)
        // P0 #2: 自动跳到首个有 slides 的模块，避免首屏空白
        const firstWithSlides = data.sections.findIndex(s => s.slides && s.slides.length > 0)
        if (firstWithSlides > 0) {
          setCurrentSectionIdx(firstWithSlides)
        }
        // 注入 CSS 变量
        if (data.theme) {
          const root = document.documentElement
          Object.entries(data.theme).forEach(([key, value]) => {
            if (typeof value !== 'string') return
            root.style.setProperty(`--theme-${key}`, value)
          })
          if (data.theme.isDark) {
            root.style.setProperty('--theme-overlay-subtle', 'rgba(255,255,255,0.08)')
            root.style.setProperty('--theme-overlay-hover', 'rgba(255,255,255,0.04)')
            root.style.setProperty('--theme-overlay-divider', 'rgba(255,255,255,0.1)')
          }
          document.title = `${data.script} — ${data.course}`
        }
      })
      .catch(err => setError(err.message))
  }, [courseId, scriptName])

  // 键盘导航
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!manifest) return
      const section = manifest.sections[currentSectionIdx]
      if (!section) return

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault()
        if (currentSlideIdx < section.slides.length - 1) {
          setCurrentSlideIdx(prev => prev + 1)
        } else if (currentSectionIdx < manifest.sections.length - 1) {
          setCurrentSectionIdx(prev => prev + 1)
          setCurrentSlideIdx(0)
        }
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault()
        if (currentSlideIdx > 0) {
          setCurrentSlideIdx(prev => prev - 1)
        } else if (currentSectionIdx > 0) {
          setCurrentSectionIdx(prev => prev - 1)
          const prevSection = manifest.sections[currentSectionIdx - 1]
          setCurrentSlideIdx(Math.max(0, prevSection.slides.length - 1))
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [manifest, currentSectionIdx, currentSlideIdx])

  // === 联动回调 ===
  const handleSubtitlesLoaded = useCallback((cues) => {
    setSrtCues(cues)
  }, [])

  const handleAudioTimeUpdate = useCallback((time, subIdx) => {
    if (!manifest || srtCues.length === 0 || subIdx < 0) return
    const section = manifest.sections[currentSectionIdx]
    if (!section) return

    const paraIdx = section.paragraphs.findIndex(p => p.srtCueIdx === subIdx)
    if (paraIdx >= 0) {
      setActiveParagraphIdx(paraIdx)
      const slides = section.slides
      if (slides.length > 0) {
        let matchedSlide = 0
        for (let i = 0; i < slides.length; i++) {
          if (slides[i].paragraphStart != null && slides[i].paragraphStart <= paraIdx) {
            matchedSlide = i
          }
        }
        isAudioDriving.current = true
        setCurrentSlideIdx(matchedSlide)
        setTimeout(() => { isAudioDriving.current = false }, 100)
      }
    }
  }, [manifest, currentSectionIdx, srtCues])

  const handleSeekToSrtCue = useCallback((srtCueIdx) => {
    if (srtCues[srtCueIdx]) {
      setSeekToTime(srtCues[srtCueIdx].start)
    }
  }, [srtCues])

  const handleParagraphSelect = useCallback((paraIdx, srtCueIdx) => {
    if (srtCueIdx != null && srtCues[srtCueIdx]) {
      setSeekToTime(srtCues[srtCueIdx].start)
      return
    }
    
    // 如果没有音频同步（纯图文模式），点击段落可以切换到对应的 Slide
    const section = manifest?.sections[currentSectionIdx]
    if (section && section.slides) {
      let targetSlideIdx = 0
      for (let i = 0; i < section.slides.length; i++) {
        if (section.slides[i].paragraphStart != null && section.slides[i].paragraphStart <= paraIdx) {
          targetSlideIdx = i
        }
      }
      setTimeout(() => {
        setCurrentSlideIdx(targetSlideIdx)
        setActiveParagraphIdx(paraIdx)
      }, 0)
    }
  }, [manifest, currentSectionIdx, srtCues])

  const switchSlide = (idx) => {
    setCurrentSlideIdx(idx)
    if (!isAudioDriving.current && manifest) {
      const section = manifest.sections[currentSectionIdx]
      const paraStart = section?.slides[idx]?.paragraphStart
      if (paraStart != null) {
        setActiveParagraphIdx(paraStart)
        const para = section.paragraphs[paraStart]
        if (para?.srtCueIdx != null && srtCues[para.srtCueIdx]) {
          setSeekToTime(srtCues[para.srtCueIdx].start)
        }
      }
    }
  }

  const switchSection = (idx) => {
    setCurrentSectionIdx(idx)
    setCurrentSlideIdx(0)
    setActiveParagraphIdx(-1)
    if (manifest && srtCues.length > 0) {
      const targetSection = manifest.sections[idx]
      if (targetSection?.firstSrtCueIdx != null && srtCues[targetSection.firstSrtCueIdx]) {
        setSeekToTime(srtCues[targetSection.firstSrtCueIdx].start)
      }
    }
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="dashboard-error">
          <h2>⚠️ 加载失败</h2>
          <p>无法加载 <code>{scriptName}</code></p>
          <p className="error-hint">{error}</p>
          <Link to={`/${courseId}`} className="back-link">← 返回课程</Link>
        </div>
      </div>
    )
  }

  if (!manifest) {
    return (
      <div className="app-container">
        <div className="loading">
          <div className="loading-spinner" />
          <p>加载课件数据...</p>
        </div>
      </div>
    )
  }

  const currentSection = manifest.sections[currentSectionIdx]
  const currentSlide = currentSection?.slides[currentSlideIdx]
  const totalSlides = currentSection?.slides.length || 0
  const hasAudio = manifest.media?.audio

  // 修正音频 URL 路径（多课程模式下需前缀 courseId）
  const audioSrc = hasAudio ? `/courses/${courseId}/${manifest.media.audio}` : null
  const srtSrc = manifest.media?.srt ? `/courses/${courseId}/${manifest.media.srt}` : null

  return (
    <div className="app-container">
      {/* 顶栏 */}
      <header className="app-header">
        <Link to={`/${courseId}`} className="header-back-link">← {manifest.course}</Link>
        <div className="script-title">{manifest.script}</div>
        {hasAudio && <span className="audio-badge">🔊 音频</span>}
      </header>

      {/* 音频播放器 */}
      {hasAudio && (
        <AudioPlayer
          audioSrc={audioSrc}
          srtSrc={srtSrc}
          onTimeUpdate={handleAudioTimeUpdate}
          onSubtitlesLoaded={handleSubtitlesLoaded}
          seekToTime={seekToTime}
          onSubtitleClick={handleSeekToSrtCue}
        />
      )}

      {/* 主内容区 */}
      <main className="main-content">
        <div className="slide-area">
          <div className="slide-viewport">
            {currentSlide ? (
              <SlideFactory slide={currentSlide} courseId={courseId} />
            ) : (
              <div className="empty-state empty-state-enhanced">
                <div className="empty-state-icon">📑</div>
                <p className="empty-state-title">本模块暂无幻灯片</p>
                <p className="empty-state-hint">请选择下方模块查看幻灯片内容</p>
              </div>
            )}
          </div>

          {totalSlides > 0 && (
            <div className="slide-nav">
              <button
                className="slide-nav-btn"
                disabled={currentSlideIdx === 0}
                onClick={() => switchSlide(currentSlideIdx - 1)}
              >
                ◀
              </button>
              <div className="slide-dots">
                {currentSection.slides.map((s, i) => (
                  <button
                    key={s.id}
                    className={`slide-dot ${i === currentSlideIdx ? 'active' : ''}`}
                    onClick={() => switchSlide(i)}
                    title={s.heading || s.id}
                  />
                ))}
              </div>
              <span className="slide-counter">{currentSlideIdx + 1} / {totalSlides}</span>
              <button
                className="slide-nav-btn"
                disabled={currentSlideIdx === totalSlides - 1}
                onClick={() => switchSlide(currentSlideIdx + 1)}
              >
                ▶
              </button>
            </div>
          )}
        </div>

        <TextPanel
          paragraphs={currentSection?.paragraphs || []}
          activeParagraphIdx={activeParagraphIdx}
          onParagraphClick={handleSeekToSrtCue}
          onParagraphSelect={handleParagraphSelect}
          slides={currentSection?.slides || []}
        />
      </main>

      {/* 底部模块导航 */}
      <NavigationBar
        sections={manifest.sections}
        currentIdx={currentSectionIdx}
        onSwitch={switchSection}
      />

      {/* 热重载 Toast */}
      {hotReloadToast && (
        <div style={{
          position: 'fixed', bottom: '1rem', right: '1rem',
          background: hotReloadToast.startsWith('❌')
            ? 'rgba(180,40,40,0.9)' : 'rgba(0,0,0,0.8)',
          color: '#fff', padding: '0.5rem 1rem', borderRadius: '0.5rem',
          fontSize: '0.85rem', zIndex: 9999, backdropFilter: 'blur(8px)',
          animation: 'fadeIn 0.3s ease', boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        }}>
          {hotReloadToast}
        </div>
      )}
    </div>
  )
}
