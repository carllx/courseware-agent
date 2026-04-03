import { useState, useEffect, useCallback, useRef } from 'react'
import SlideFactory from './components/SlideFactory'
import TextPanel from './components/TextPanel'
import NavigationBar from './components/NavigationBar'
import AudioPlayer from './components/AudioPlayer'

function App() {
  const [manifest, setManifest] = useState(null)
  const [currentSectionIdx, setCurrentSectionIdx] = useState(0)
  const [currentSlideIdx, setCurrentSlideIdx] = useState(0)

  // === 联动状态 ===
  const [srtCues, setSrtCues] = useState([])            // SRT 全量 cue 列表
  const [activeParagraphIdx, setActiveParagraphIdx] = useState(-1)  // 当前高亮段落
  const [seekToTime, setSeekToTime] = useState(null)     // 外部 seek 控制
  const isAudioDriving = useRef(false)                   // 防止 audio→slide 触发 slide→text 循环
  const [hotReloadToast, setHotReloadToast] = useState(null)

  // === HMR 热重载监听 ===
  useEffect(() => {
    if (!import.meta.hot) return

    const handleReload = (data) => {
      console.log('[h5-hot-reload] 收到重载通知', data)
      fetch('/slides.json?t=' + Date.now())
        .then(res => res.json())
        .then(newData => {
          setManifest(newData)
          if (newData.theme) {
            const root = document.documentElement
            Object.entries(newData.theme).forEach(([key, value]) => {
              if (typeof value !== 'string') return
              root.style.setProperty(`--theme-${key}`, value)
            })
          }
          document.title = `${newData.script} — ${newData.course}`
          const label = data.elapsed ? `${data.elapsed}ms` : ''
          setHotReloadToast(`🔄 已自动刷新 ${label}`)
          setTimeout(() => setHotReloadToast(null), 2500)
        })
        .catch(err => console.error('[h5-hot-reload] Re-fetch 失败:', err))
    }

    const handleError = (data) => {
      setHotReloadToast(`❌ 重建失败: ${data.moduleName || '未知'}`)
      setTimeout(() => setHotReloadToast(null), 5000)
    }

    import.meta.hot.on('h5:reload', handleReload)
    import.meta.hot.on('h5:error', handleError)
  }, [])

  // === 热重载位置钳位 ===
  useEffect(() => {
    if (!manifest) return
    const max = Math.max(0, manifest.sections.length - 1)
    setCurrentSectionIdx(prev => prev > max ? max : prev)
  }, [manifest])

  useEffect(() => {
    if (!manifest) return
    const section = manifest.sections[currentSectionIdx]
    if (!section) return
    const max = Math.max(0, (section.slides?.length || 1) - 1)
    setCurrentSlideIdx(prev => prev > max ? max : prev)
  }, [manifest, currentSectionIdx])

  // 加载数据
  useEffect(() => {
    fetch('/slides.json')
      .then(res => res.json())
      .then(data => {
        setManifest(data)
        // 注入 CSS 变量
        if (data.theme) {
          const root = document.documentElement
          Object.entries(data.theme).forEach(([key, value]) => {
            // 跳过非字符串值（如 isDark 布尔值）
            if (typeof value !== 'string') return
            root.style.setProperty(`--theme-${key}`, value)
          })
          // Phase 4: 暗色模式自适应 overlay 方向
          if (data.theme.isDark) {
            root.style.setProperty('--theme-overlay-subtle', 'rgba(255,255,255,0.08)')
            root.style.setProperty('--theme-overlay-hover', 'rgba(255,255,255,0.04)')
            root.style.setProperty('--theme-overlay-divider', 'rgba(255,255,255,0.1)')
          }
          document.title = `${data.script} — ${data.course}`
        }
      })
      .catch(err => console.error("加载 slides.json 失败:", err))
  }, [])

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

  // === 联动回调 A: SRT 加载完成 ===
  const handleSubtitlesLoaded = useCallback((cues) => {
    setSrtCues(cues)
  }, [])

  // === 联动回调 B: Audio → Slide + Text (V1 + V2 修复) ===
  const handleAudioTimeUpdate = useCallback((time, subIdx) => {
    if (!manifest || srtCues.length === 0 || subIdx < 0) return

    const section = manifest.sections[currentSectionIdx]
    if (!section) return

    // 通过 srtCueIdx 找到当前段落
    const paraIdx = section.paragraphs.findIndex(p => p.srtCueIdx === subIdx)
    if (paraIdx >= 0) {
      // V2: Audio → Text 高亮
      setActiveParagraphIdx(paraIdx)

      // V1: Audio → Slide 自动翻页
      // 找到 paragraphStart <= paraIdx 的最后一个 slide
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
        // 短暂延迟后重置标志
        setTimeout(() => { isAudioDriving.current = false }, 100)
      }
    }
  }, [manifest, currentSectionIdx, srtCues])

  // === 联动 E: 通用 SRT Cue Seek（字幕点击 / 段落点击共用）===
  const handleSeekToSrtCue = useCallback((srtCueIdx) => {
    if (srtCues[srtCueIdx]) {
      setSeekToTime(srtCues[srtCueIdx].start)
    }
  }, [srtCues])

  // === 联动 C: Slide 手动切换 → Text + Audio (V4→V6 修复) ===
  const switchSlide = (idx) => {
    setCurrentSlideIdx(idx)

    // 仅在非音频驱动时执行 slide→text→audio 同步
    if (!isAudioDriving.current && manifest) {
      const section = manifest.sections[currentSectionIdx]
      const paraStart = section?.slides[idx]?.paragraphStart
      if (paraStart != null) {
        setActiveParagraphIdx(paraStart)
        // Audio-first: slide 点击也同步音频
        const para = section.paragraphs[paraStart]
        if (para?.srtCueIdx != null && srtCues[para.srtCueIdx]) {
          setSeekToTime(srtCues[para.srtCueIdx].start)
        }
      }
    }
  }

  // === 联动 D: Nav → Section + Audio seek (V5 修复) ===
  const switchSection = (idx) => {
    setCurrentSectionIdx(idx)
    setCurrentSlideIdx(0)
    setActiveParagraphIdx(-1) // 重置高亮

    // V5: 跳转音频到目标 section 的起始时间
    if (manifest && srtCues.length > 0) {
      const targetSection = manifest.sections[idx]
      if (targetSection?.firstSrtCueIdx != null && srtCues[targetSection.firstSrtCueIdx]) {
        setSeekToTime(srtCues[targetSection.firstSrtCueIdx].start)
      }
    }
  }

  if (!manifest) {
    return (
      <div className="loading">
        <div className="loading-spinner" />
        <p>加载课件数据...</p>
      </div>
    )
  }

  const currentSection = manifest.sections[currentSectionIdx]
  const currentSlide = currentSection?.slides[currentSlideIdx]
  const totalSlides = currentSection?.slides.length || 0

  const hasAudio = manifest.media?.audio

  return (
    <div className="app-container">
      {/* 顶栏 */}
      <header className="app-header">
        <div className="course-title">{manifest.course}</div>
        <div className="script-title">{manifest.script}</div>
        {hasAudio && <span className="audio-badge">🔊 音频</span>}
      </header>

      {/* 音频播放器（仅在有音频时显示） */}
      {hasAudio && (
        <AudioPlayer
          audioSrc={`/${manifest.media.audio}`}
          srtSrc={manifest.media.srt ? `/${manifest.media.srt}` : null}
          onTimeUpdate={handleAudioTimeUpdate}
          onSubtitlesLoaded={handleSubtitlesLoaded}
          seekToTime={seekToTime}
          onSubtitleClick={handleSeekToSrtCue}
        />
      )}

      {/* 主内容区：左侧幻灯片 + 右侧文本 */}
      <main className="main-content">
        {/* 幻灯片区域 */}
        <div className="slide-area">
          <div className="slide-viewport">
            {currentSlide ? (
              <SlideFactory slide={currentSlide} />
            ) : (
              <div className="empty-state">
                <p>本模块暂无幻灯片</p>
              </div>
            )}
          </div>

          {/* 幻灯片导航条 */}
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

        {/* 文本面板 */}
        <TextPanel
          paragraphs={currentSection?.paragraphs || []}
          activeParagraphIdx={activeParagraphIdx}
          onParagraphClick={handleSeekToSrtCue}
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

export default App

