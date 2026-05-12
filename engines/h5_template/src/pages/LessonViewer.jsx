import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import { useParams, Link, useSearchParams } from 'react-router-dom'
import SlideFactory from '../components/SlideFactory'
import TextPanel from '../components/TextPanel'
import OutlineSidebar from '../components/OutlineSidebar'
import TeacherGuideSheet from '../components/TeacherGuideSheet'
import ModuleRail from '../components/ModuleRail'


import AnnotationOverlay from '../components/AnnotationOverlay'
import { useValidation } from '../contexts/ValidationContext'
import { useProgress } from '../contexts/ProgressContext'
import { TtsSegmentProvider, useTtsSegments } from '../contexts/TtsSegmentContext'
import '../styles/craft-room.css'

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

  return (
    <TtsSegmentProvider courseId={courseId} weekName={scriptName}>
      <LessonViewerInner courseId={courseId} scriptName={scriptName} />
    </TtsSegmentProvider>
  )
}

function LessonViewerInner({ courseId, scriptName }) {
  const [manifest, setManifest] = useState(null)
  const [error, setError] = useState(null)
  const [currentSectionIdx, setCurrentSectionIdx] = useState(0)
  const [currentSlideIdx, setCurrentSlideIdx] = useState(0)

  // === 联动状态 ===
  const [activeParagraphIdx, setActiveParagraphIdx] = useState(-1)
  const [hotReloadToast, setHotReloadToast] = useState(null)
  
  // === Mobile Drawer UI ===
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false)

  // === Feature C: Teacher Guide ===
  const [teacherSheetTarget, setTeacherSheetTarget] = useState(null)

  // 🩹 Fix-2: 用户主动导航守卫 — 防止 TTS 播放同步 useEffect 覆写用户意图
  const userNavigatingRef = useRef(false)

  // === P1 验证上下文 ===
  const { onReload, onValidation, isInFlow } = useValidation()

  // === ARC-04: 学习进度 ===
  const progressCtx = useProgress()

  // === ARC-03: URL query params 深链接 ===
  const [searchParams, setSearchParams] = useSearchParams()

  const isTeacherMode = searchParams.get('mode') === 'teacher'

  // === P0: 教师/学生模式切换 ===
  const toggleMode = useCallback(() => {
    const newParams = new URLSearchParams(searchParams)
    if (isTeacherMode) {
      newParams.delete('mode')
    } else {
      newParams.set('mode', 'teacher')
    }
    setSearchParams(newParams, { replace: true })
  }, [isTeacherMode, searchParams, setSearchParams])

  // === P3: Touch Swipe 翻页手势 ===
  const touchStartRef = useRef(null)
  const handleTouchStart = useCallback((e) => {
    touchStartRef.current = { x: e.touches[0].clientX, y: e.touches[0].clientY }
  }, [])
  const handleTouchEnd = useCallback((e) => {
    if (!touchStartRef.current || !manifest) return
    const dx = e.changedTouches[0].clientX - touchStartRef.current.x
    const dy = e.changedTouches[0].clientY - touchStartRef.current.y
    touchStartRef.current = null
    // 仅在水平滑动距离 > 50px 且大于垂直距离时触发（防止与滚动冲突）
    if (Math.abs(dx) < 50 || Math.abs(dx) < Math.abs(dy)) return
    const section = manifest.sections[currentSectionIdx]
    if (!section) return
    if (dx < 0 && currentSlideIdx < (section.slides?.length || 1) - 1) {
      switchSlide(currentSlideIdx + 1)
    } else if (dx > 0 && currentSlideIdx > 0) {
      switchSlide(currentSlideIdx - 1)
    }
  }, [manifest, currentSectionIdx, currentSlideIdx])

  // === TTS 段落缓存 ===
  const ttsCtx = useTtsSegments()

  // === HMR 热重载监听 ===
  useEffect(() => {
    if (!import.meta.hot) return

    const handleReload = (data) => {
      console.log('[h5-hot-reload] 收到重载通知', data)
      // P1: 标记进入心流保护期
      onReload()
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

    const handleValidation = (data) => {
      console.log('[h5:validation] 收到验证结果', data.gateLevel, `${data.elapsed}ms`)
      onValidation(data)
    }

    import.meta.hot.on('h5:reload', handleReload)
    import.meta.hot.on('h5:error', handleError)
    import.meta.hot.on('h5:validation', handleValidation)

    // 漏洞修复：清理旧监听器，防止 courseId/scriptName 变化时多重触发
    return () => {
      import.meta.hot.off('h5:reload', handleReload)
      import.meta.hot.off('h5:error', handleError)
      import.meta.hot.off('h5:validation', handleValidation)
    }
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

  // === TTS: section 切换时计算段落缓存状态 ===
  useEffect(() => {
    if (!manifest || !ttsCtx?.computeStatus) return
    const section = manifest.sections[currentSectionIdx]
    if (section?.paragraphs) {
      ttsCtx.computeStatus(section.paragraphs)
    }
  }, [manifest, currentSectionIdx, ttsCtx?.computeStatus]) // eslint-disable-line react-hooks/exhaustive-deps

  // === 同步 TTS 播放状态到当前高亮段落 ===
  useEffect(() => {
    if (!ttsCtx) return
    // 🩹 Fix-2: 用户主动导航期间，跳过 TTS 播放状态同步，防止覆写劫持
    if (userNavigatingRef.current) return
    
    // 找到当前正在播放的段落
    let playingIdx = null
    const keys = Object.keys(ttsCtx.segmentMap)
    for (let k of keys) {
      if (ttsCtx.segmentMap[k].status === 'playing') {
        playingIdx = Number(k)
        break
      }
    }

    if (playingIdx !== null && playingIdx !== activeParagraphIdx) {
      setActiveParagraphIdx(playingIdx)
      
      // 同步 Slide
      const section = manifest?.sections[currentSectionIdx]
      if (section?.slides?.length > 0) {
        let targetSlideIdx = 0
        for (let i = 0; i < section.slides.length; i++) {
          if (section.slides[i].paragraphStart != null && section.slides[i].paragraphStart <= playingIdx) {
            targetSlideIdx = i
          }
        }
        setCurrentSlideIdx(targetSlideIdx)
      }
    }
  }, [ttsCtx?.segmentMap, manifest, currentSectionIdx, activeParagraphIdx])

  // 加载数据
  useEffect(() => {
    // 重置状态
    setManifest(null)
    setError(null)

    // UX 优化支柱 2：恢复位置优先级 → ARC-03 query params > sessionStorage > 默认值
    const qm = searchParams.get('m')
    const qs = searchParams.get('s')
    if (qm != null) {
      // ARC-03: URL 深链接优先
      setCurrentSectionIdx(parseInt(qm) || 0)
      setCurrentSlideIdx(parseInt(qs) || 0)
    } else {
      const savedPos = sessionStorage.getItem(`h5-pos-${courseId}-${scriptName}`)
      if (savedPos) {
        try {
          const { section, slide } = JSON.parse(savedPos)
          setCurrentSectionIdx(section || 0)
          setCurrentSlideIdx(slide || 0)
        } catch (e) {
          setCurrentSectionIdx(0)
          setCurrentSlideIdx(0)
        }
      } else {
        setCurrentSectionIdx(0)
        setCurrentSlideIdx(0)
      }
    }

    setActiveParagraphIdx(-1)

    const jsonUrl = `/courses/${courseId}/${scriptName}.json`
    fetch(jsonUrl)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(data => {
        setManifest(data)
        // P0 #2: 如果没有记忆锚点，且没有 URL 强制参数，才自动跳到首个有 slides 的模块，避免首屏空白
        const savedPos = window.sessionStorage.getItem(`h5-pos-${courseId}-${scriptName}`)
        const qm = searchParams.get('m')
        if (!savedPos && qm == null) {
          const firstWithSlides = data.sections.findIndex(s => s.slides && s.slides.length > 0)
          if (firstWithSlides > 0) {
            setCurrentSectionIdx(firstWithSlides)
          }
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

  // === UX 优化支柱 2：写入记忆锚点 ===
  useEffect(() => {
    if (manifest) {
      sessionStorage.setItem(`h5-pos-${courseId}-${scriptName}`, JSON.stringify({
        section: currentSectionIdx,
        slide: currentSlideIdx
      }))
      // ARC-03: 同步 URL query params（保留 mode 参数）
      const newParams = new URLSearchParams(searchParams)
      newParams.set('m', String(currentSectionIdx))
      newParams.set('s', String(currentSlideIdx))
      setSearchParams(newParams, { replace: true })
    }
  }, [currentSectionIdx, currentSlideIdx, courseId, scriptName, manifest])

  // === P5: 教师模式防息屏 (Screen Wake Lock API) ===
  useEffect(() => {
    if (!isTeacherMode) return
    let wakeLock = null
    const requestWakeLock = async () => {
      try {
        if ('wakeLock' in navigator) {
          wakeLock = await navigator.wakeLock.request('screen')
        }
      } catch (e) { /* 静默降级：不支持或用户拒绝 */ }
    }
    requestWakeLock()
    // 页面重新可见时重新请求（浏览器后台会释放 lock）
    const onVisibility = () => {
      if (document.visibilityState === 'visible') requestWakeLock()
    }
    document.addEventListener('visibilitychange', onVisibility)
    return () => {
      wakeLock?.release()
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [isTeacherMode])

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
  const handleParagraphSelect = useCallback((paraIdx) => {
    const section = manifest?.sections[currentSectionIdx]
    
    // 1. 如果段落 TTS 已就绪，触发连播
    if (ttsCtx?.segmentMap[paraIdx]?.status === 'ready') {
      ttsCtx.playFrom(paraIdx, section.paragraphs)
      return
    }
    
    // 2. 否则，点击段落仅切换到对应的 Slide
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
  }, [manifest, currentSectionIdx, ttsCtx])

  // SSOT Scroll Spy 无声更新 (仅更新高亮和幻灯片，不触发 TTS 播放)
  const handleParagraphView = useCallback((paraIdx) => {
    setActiveParagraphIdx(paraIdx)
    const section = manifest?.sections[currentSectionIdx]
    if (section && section.slides) {
      let targetSlideIdx = 0
      for (let i = 0; i < section.slides.length; i++) {
        if (section.slides[i].paragraphStart != null && section.slides[i].paragraphStart <= paraIdx) {
          targetSlideIdx = i
        }
      }
      setCurrentSlideIdx(targetSlideIdx)
    }
  }, [manifest, currentSectionIdx])

  const switchSlide = (idx) => {
    setCurrentSlideIdx(idx)
    setMobileDrawerOpen(false)
    if (manifest) {
      const section = manifest.sections[currentSectionIdx]
      const paraStart = section?.slides[idx]?.paragraphStart
      if (paraStart != null) {
        setActiveParagraphIdx(paraStart)
      }
    }
  }

  const switchSection = (idx) => {
    // 🩹 Fix-1a: 切换模块前必须停止 TTS 播放，防止跨模块状态污染
    if (ttsCtx) ttsCtx.stopPlayback()
    userNavigatingRef.current = true
    setTimeout(() => { userNavigatingRef.current = false }, 500)
    setCurrentSectionIdx(idx)
    setCurrentSlideIdx(0)
    setActiveParagraphIdx(-1)
    setMobileDrawerOpen(false)
    // ARC-04: 标记当前 section 为已读
    if (manifest && progressCtx?.markRead) {
      const sec = manifest.sections[idx]
      if (sec) progressCtx.markRead(courseId, scriptName, sec.id)
    }
  }

  // ARC-01 v2: 段落锚点导航（OutlineSidebar H3 子节点击专用）
  const navigateToParagraph = useCallback((paraIdx) => {
    const section = manifest?.sections[currentSectionIdx]
    if (!section) return

    // 🩹 Fix-1b: 跳转子节前停止 TTS 连播，防止 useEffect 覆写用户导航
    if (ttsCtx) ttsCtx.stopPlayback()
    userNavigatingRef.current = true
    setTimeout(() => { userNavigatingRef.current = false }, 500)

    // 1. 高亮目标段落
    setActiveParagraphIdx(paraIdx)

    // 2. runtime 动态推算包含该段落的 slide
    if (section.slides?.length > 0) {
      let bestSlide = 0
      for (let i = 0; i < section.slides.length; i++) {
        if (section.slides[i].paragraphStart != null
          && section.slides[i].paragraphStart <= paraIdx) {
          bestSlide = i
        }
      }
      setCurrentSlideIdx(bestSlide)
    }

    // 3. 关闭移动端 drawer
    setMobileDrawerOpen(false)
  }, [manifest, currentSectionIdx, ttsCtx])

  // ── 备课辅助：计算每个 Slide 的温度与字数（必须在条件 return 之前，遵守 Hooks 规则）──
  const currentSection = manifest?.sections[currentSectionIdx] ?? null
  const slideStats = useMemo(() => {
    if (!currentSection || !currentSection.slides || !currentSection.paragraphs) return []
    const paras = currentSection.paragraphs
    return currentSection.slides.map((s, i) => {
      const startIdx = s.paragraphStart != null ? s.paragraphStart : 0
      let nextSlideStartIdx = paras.length
      if (i + 1 < currentSection.slides.length && currentSection.slides[i+1].paragraphStart != null) {
        nextSlideStartIdx = currentSection.slides[i+1].paragraphStart
      }
      
      let totalChars = 0
      let hotChars = 0
      let coldChars = 0

      for (let j = startIdx; j < nextSlideStartIdx; j++) {
        const p = paras[j]
        if (!p) continue
        const count = p.cnCharCount || 0
        totalChars += count
        if (p.temperature === 'hot') hotChars += count
        else if (p.temperature === 'cold') coldChars += count
      }

      let temp = 'neutral'
      if (hotChars > 0 && hotChars >= coldChars) temp = 'hot'
      else if (coldChars > 0) temp = 'cold'

      return { temp, totalChars }
    })
  }, [currentSection])

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

  const currentSlide = currentSection?.slides?.[currentSlideIdx]
  const totalSlides = currentSection?.slides?.length || 0

  return (
    <div className={`app-container ${isTeacherMode ? 'layout-mode-teacher' : 'layout-mode-student'}`}
         onTouchStart={handleTouchStart}
         onTouchEnd={handleTouchEnd}
    >
      {/* 顶栏 */}
      <header className="app-header">
        <button 
          className="mobile-drawer-toggle" 
          onClick={() => setMobileDrawerOpen(true)}
          title="展开目录"
          aria-label="展开章节目录"
        >
          ☰
        </button>
        <Link to={`/${courseId}`} className="header-back-link">← {manifest.course}</Link>
        <div className="script-title" title={manifest.script}>{manifest.script}</div>
        <div className="header-right">
          {/* P4: 教师版迷你进度指示器 */}
          {isTeacherMode && totalSlides > 0 && (
            <span className="teacher-progress-badge">
              <span className="teacher-progress-bar">
                <span className="teacher-progress-fill" style={{ width: `${((currentSlideIdx + 1) / totalSlides) * 100}%` }} />
              </span>
              <span className="teacher-progress-text">{currentSlideIdx + 1}/{totalSlides}</span>
            </span>
          )}
          {/* P0: 教师/学生模式切换 */}
          <button
            className="mode-toggle-btn"
            onClick={toggleMode}
            title={isTeacherMode ? '切换到学生浏览模式' : '切换到教师提词器模式'}
          >
            {isTeacherMode ? '📖 学生版' : '🎓 教师版'}
          </button>
        </div>
      </header>



      {/* 主内容区 */}
      <main className="main-content">
        <OutlineSidebar
          manifest={manifest}
          currentSectionIdx={currentSectionIdx}
          activeParagraphIdx={activeParagraphIdx}
          onSwitchSection={switchSection}
          onNavigateToParagraph={navigateToParagraph}
          courseId={courseId}
          scriptName={scriptName}
          mobileDrawerOpen={mobileDrawerOpen}
          onCloseMobileDrawer={() => setMobileDrawerOpen(false)}
        />

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
                {currentSection.slides.map((s, i) => {
                  const stat = slideStats[i] || { temp: 'neutral', totalChars: 0 }
                  // 字数映射宽度：每 20 字 1px，最小 6px，最大 32px
                  let dynamicWidth = Math.max(6, Math.min(32, Math.floor(stat.totalChars / 20)))
                  // 对于 0 字的赋予最小 6px
                  if (stat.totalChars === 0) dynamicWidth = 6
                  
                  return (
                    <button
                      key={s.id}
                      className={`slide-dot temp-${stat.temp} ${i === currentSlideIdx ? 'active' : ''}`}
                      onClick={() => {
                        if (isTeacherMode) {
                          setTeacherSheetTarget(i)
                        } else {
                          switchSlide(i)
                        }
                      }}
                      title={`${s.heading || s.id}\n字数: ${stat.totalChars}`}
                      style={{ width: `${dynamicWidth}px` }}
                    />
                  )
                })}
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

        {/* P2: 教师版快速模块切换导航条 */}
        {isTeacherMode && manifest.sections.length > 1 && (
          <ModuleRail
            sections={manifest.sections}
            modules={manifest.modules || []}
            currentIdx={currentSectionIdx}
            onSwitch={switchSection}
            courseId={courseId}
            scriptName={scriptName}
          />
        )}

        <TextPanel
          paragraphs={currentSection?.paragraphs || []}
          allSections={manifest?.sections || []}
          activeParagraphIdx={activeParagraphIdx}
          onParagraphSelect={handleParagraphSelect}
          onParagraphView={handleParagraphView}
          slides={currentSection?.slides || []}
          subSections={currentSection?.subSections || []}
        />
      </main>

      {/* Phase 3: Agent 批注层（基于指纹的语义吸附） */}
      <AnnotationOverlay
        annotations={manifest.annotations || []}
        paragraphs={currentSection?.paragraphs || []}
      />

      {/* Feature C: 教师导览提词器 */}
      <TeacherGuideSheet
        isOpen={teacherSheetTarget !== null}
        targetIdx={teacherSheetTarget}
        stat={teacherSheetTarget !== null ? slideStats[teacherSheetTarget] : null}
        onClose={() => setTeacherSheetTarget(null)}
        onNavigate={() => {
          switchSlide(teacherSheetTarget)
          setTeacherSheetTarget(null)
        }}
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
