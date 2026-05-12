import { useRef, useEffect, useMemo, useState, useCallback, memo, forwardRef } from 'react'
import TtsParaButton from './TtsParaButton'
import TtsToolbar from './TtsToolbar'
import { useTtsSegments } from '../contexts/TtsSegmentContext'
import '../styles/text-panel.css'

/**
 * TextPanel — 逐字稿文本面板（UX V2 重构）
 *
 * 改进:
 *   1. 动态面包屑替代静态 "逐字稿" 标题
 *   2. 右侧 Scroll-spy 轨道提供全局结构感
 *   3. 段落操作收纳到统一的 Action Gutter
 */
export default function TextPanel({ paragraphs = [], allSections = [], activeParagraphIdx = -1, onParagraphSelect, onParagraphView, slides = [], subSections = [] }) {
  const paraRefs = useRef([])
  const wrapperRefs = useRef([])
  const contentRef = useRef(null)
  const flashTimeoutRef = useRef(null)
  const tts = useTtsSegments()

  // ── 状态守卫 ──
  const hasUserSelection = useRef(false)
  const isAutoScrolling = useRef(false)

  // ── 检视模式 (Cloak Mode) ──
  const [cloakMode, setCloakMode] = useState(false)

  useEffect(() => {
    const onSelectionChange = () => {
      const sel = window.getSelection()
      hasUserSelection.current = !!(sel && sel.toString().trim().length > 0)
    }
    document.addEventListener('selectionchange', onSelectionChange)
    return () => document.removeEventListener('selectionchange', onSelectionChange)
  }, [])

  // ── 结构映射（必须在 useEffect 之前声明，避免 TDZ 引用错误） ──
  
  // 预计算 paragraphIdx → Array<SlideInfo> 映射，避免幻灯片挤占段落被覆写
  const slideDividerMap = useMemo(() => {
    const map = new Map()
    slides.forEach((slide, idx) => {
      if (slide.paragraphStart != null) {
        const arr = map.get(slide.paragraphStart) || []
        arr.push({ idx, heading: slide.heading, total: slides.length })
        map.set(slide.paragraphStart, arr)
      }
    })
    return map
  }, [slides])

  // 预计算 paragraphIdx → SubSection 映射，用于插入 H3 切割符
  const subSectionDividerMap = useMemo(() => {
    const map = new Map()
    if (subSections) {
      subSections.forEach((sub, idx) => {
        if (sub.startParagraph != null) {
          map.set(sub.startParagraph, sub)
        }
      })
    }
    return map
  }, [subSections])

  // 预计算 paragraphIdx → H4 子节点映射，用于插入 H4 切割符
  const h4DividerMap = useMemo(() => {
    const map = new Map()
    if (subSections) {
      subSections.forEach((sub) => {
        if (sub.children && sub.children.length > 0) {
          sub.children.forEach((child) => {
             if (child.startParagraph != null) {
                map.set(child.startParagraph, child)
             }
          })
        }
      })
    }
    return map
  }, [subSections])

  // 推断当前活动的子节（逻辑同 OutlineSidebar）
  const activeSubIdx = useMemo(() => {
    let subIdx = -1
    const effectiveParaIdx = activeParagraphIdx >= 0 ? activeParagraphIdx : 0
    if (subSections && subSections.length > 0) {
      for (let i = 0; i < subSections.length; i++) {
        if (subSections[i].startParagraph <= effectiveParaIdx) {
          subIdx = i
        }
      }
    }
    return subIdx
  }, [subSections, activeParagraphIdx])

  // 推断当前活动的 H4 子节
  const activeH4Idx = useMemo(() => {
    let h4Idx = -1
    const effectiveParaIdx = activeParagraphIdx >= 0 ? activeParagraphIdx : 0
    if (activeSubIdx >= 0 && subSections && subSections[activeSubIdx]?.children) {
      const children = subSections[activeSubIdx].children
      for (let i = 0; i < children.length; i++) {
        if (children[i].startParagraph <= effectiveParaIdx) {
          h4Idx = i
        }
      }
    }
    return h4Idx
  }, [subSections, activeSubIdx, activeParagraphIdx])

  // 当 activeParagraphIdx 变化时，智能滚动到对应位置
  // 方案 A: 若目标段落位于 H3 子节起点 -> 滚动到节标题 + 闪烁高亮
  useEffect(() => {
    if (hasUserSelection.current) return
    if (activeParagraphIdx >= 0 && paraRefs.current[activeParagraphIdx]) {
      isAutoScrolling.current = true

      const hasSubDivider = subSectionDividerMap.has(activeParagraphIdx)
      const scrollTarget = hasSubDivider
        ? (wrapperRefs.current[activeParagraphIdx] || paraRefs.current[activeParagraphIdx])
        : paraRefs.current[activeParagraphIdx]

      scrollTarget.scrollIntoView({
        behavior: 'smooth',
        block: hasSubDivider ? 'start' : 'center',
      })

      if (hasSubDivider && wrapperRefs.current[activeParagraphIdx]) {
        const dividerEl = wrapperRefs.current[activeParagraphIdx].querySelector('.transcript-section-divider')
        if (dividerEl) {
          dividerEl.classList.remove('flash')
          void dividerEl.offsetWidth
          dividerEl.classList.add('flash')
          if (flashTimeoutRef.current) clearTimeout(flashTimeoutRef.current)
          flashTimeoutRef.current = setTimeout(() => {
            dividerEl.classList.remove('flash')
          }, 1800)
        }
      }

      setTimeout(() => { isAutoScrolling.current = false }, 800)
    }
  }, [activeParagraphIdx, subSectionDividerMap])



  // ── Scroll Spy 视口联动 ──
  useEffect(() => {
    const container = contentRef.current?.parentElement
    if (!container || !onParagraphView) return

    let timeout
    const handleScroll = () => {
      // 若处于用户选词、系统自动滚动过程，则挂起触发机制
      if (hasUserSelection.current || isAutoScrolling.current) return
      
      if (timeout) clearTimeout(timeout)
      timeout = setTimeout(() => {
         const containerRect = container.getBoundingClientRect()
         // 检测锚点设为视口上方 40% 处
         const centerTargetY = containerRect.top + containerRect.height * 0.4
         let closestIdx = -1
         let minDistance = Infinity

         paraRefs.current.forEach((el, idx) => {
           if (!el) return
           const rect = el.getBoundingClientRect()
           const elCenterY = rect.top + rect.height / 2
           const distance = Math.abs(elCenterY - centerTargetY)
           if (distance < minDistance) {
             minDistance = distance
             closestIdx = idx
           }
         })

         if (closestIdx !== -1 && minDistance < containerRect.height / 2) {
            if (activeParagraphIdx !== closestIdx) {
               onParagraphView(closestIdx)
            }
         }
      }, 150)
    }

    container.addEventListener('scroll', handleScroll, { passive: true })
    return () => container.removeEventListener('scroll', handleScroll)
  }, [activeParagraphIdx, onParagraphView])

  // 稳定的段落 onClick 回调
  const handleClick = useCallback((i) => {
    const selection = window.getSelection()
    if (selection && selection.toString().trim().length > 0) {
      return
    }
    if (onParagraphSelect) {
      onParagraphSelect(i)
    }
  }, [onParagraphSelect])

  // 动态面包屑信息
  const breadcrumbInfo = useMemo(() => {
    if (slides.length === 0 && (!subSections || subSections.length === 0)) return null
    const baseInfo = { total: slides.length, heading: '', subHeading: '' }
    if (subSections && subSections.length > 0 && activeSubIdx >= 0) {
      const currentSub = subSections[activeSubIdx]
      baseInfo.heading = currentSub.title
      if (activeH4Idx >= 0 && currentSub.children && currentSub.children[activeH4Idx]) {
        baseInfo.subHeading = currentSub.children[activeH4Idx].title
      }
    }
    return baseInfo
  }, [slides, subSections, activeSubIdx, activeH4Idx])

  if (!paragraphs.length) {
    return (
      <aside className="text-panel">
        <div className="text-panel-header">
          <span>逐字稿</span>
        </div>
        <div className="text-panel-content">
          <p className="empty-state" style={{ height: 'auto', padding: '2rem' }}>
            本模块暂无文本内容
          </p>
        </div>
      </aside>
    )
  }

  return (
    <aside className="text-panel">
      {/* 动态面包屑头部 */}
      <div className="text-panel-header" style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
        {breadcrumbInfo ? (
          <span className="text-panel-breadcrumb">
            <span className="breadcrumb-label">逐字稿</span>
            {breadcrumbInfo.heading && (
              <>
                <span className="breadcrumb-sep">›</span>
                <span className="breadcrumb-heading">{breadcrumbInfo.heading}</span>
              </>
            )}
            {breadcrumbInfo.subHeading && (
              <>
                <span className="breadcrumb-sep">›</span>
                <span className="breadcrumb-subheading">{breadcrumbInfo.subHeading}</span>
              </>
            )}
            {breadcrumbInfo.total > 0 && (
              <>
                <span className="breadcrumb-sep">|</span>
                <span className="breadcrumb-slide">
                  {breadcrumbInfo.total} Slides
                </span>
              </>
            )}
          </span>
        ) : <span>逐字稿</span>}
        
        {/* 检视模式 Toggle */}
        <button 
          className={`cloak-toggle-btn ${cloakMode ? 'active' : ''}`}
          onClick={() => setCloakMode(!cloakMode)}
          title="记忆检视模式：隐藏正文，显示锚词"
          style={{
            background: cloakMode ? 'var(--theme-primary)' : 'transparent',
            color: cloakMode ? 'white' : 'var(--theme-textMuted)',
            border: `1px solid ${cloakMode ? 'var(--theme-primary)' : 'var(--theme-overlay-divider)'}`,
            borderRadius: '4px',
            padding: '2px 8px',
            fontSize: '11px',
            cursor: 'pointer',
            transition: 'all 0.2s',
            fontWeight: 600,
          }}
        >
          {cloakMode ? '👁️ 检视中' : '👁️ 记忆检视'}
        </button>
      </div>

      <TtsToolbar paragraphs={paragraphs} allSections={allSections} />

      <div className="text-panel-body">


        <div className={`text-panel-content ${cloakMode ? 'cloaked' : ''}`} ref={contentRef}>
          {paragraphs.map((para, i) => {
            const subDivider = subSectionDividerMap.get(i)
            const h4Divider = h4DividerMap.get(i)
            const slideDividers = slideDividerMap.get(i)
            
            return (
              <div key={para._fp || i} ref={el => (wrapperRefs.current[i] = el)}>
                {/* 1. 先渲染 H3 逻辑节点（结构骨架） */}
                {subDivider && (
                  <div className="transcript-section-divider">
                     <span className="section-divider-icon">🔖</span>
                     <span className="section-divider-title">{subDivider.title}</span>
                  </div>
                )}
                
                {/* 1.5. 渲染 H4 逻辑节点（内联/扁平化锚点） */}
                {h4Divider && (
                  <div className="transcript-h4-divider">
                     <span className="h4-divider-dot"></span>
                     <span className="h4-divider-title">{h4Divider.title}</span>
                  </div>
                )}
                
                {/* 2. 再渲染 物理节点 (Slide Dividers)，支持多 Slides 并排避免截断 */}
                {slideDividers && slideDividers.length > 0 && (
                  <div className="slide-divider-group">
                    {slideDividers.map((dividerInfo, dIdx) => (
                      <div key={dIdx} className="slide-divider">
                        <span className="slide-divider-badge">Slide {dividerInfo.idx + 1}/{dividerInfo.total}</span>
                        {dividerInfo.heading && (
                          <span className="slide-divider-title">{dividerInfo.heading}</span>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* 3. 最后渲染段落块 */}
                <ParagraphBlock
                  para={para}
                  paraIndex={i}
                  isActive={i === activeParagraphIdx}
                  ttsStatus={tts?.segmentMap[i]?.status || 'missing'}
                  isCloaked={cloakMode}
                  ref={el => (paraRefs.current[i] = el)}
                  onClick={() => handleClick(i)}
                />
              </div>
            )
          })}
        </div>
      </div>
    </aside>
  )
}

/**
 * ParagraphBlock — 单个段落渲染块（Action Gutter 版）
 *
 * 布局: [Gutter (TTS + 定位)] [内容区]
 * Gutter 区域常驻显示，提供效率优先的 Craft Room 体验。
 */
const ParagraphBlock = memo(forwardRef(function ParagraphBlock({ para, paraIndex, isActive, ttsStatus, isCloaked, onClick }, ref) {
  const [revealed, setRevealed] = useState(false)
  const activeClass = isActive ? ' active' : ''
  const revealedClass = revealed ? ' revealed' : ''
  const hasTts = para.ttsFp && !para.ttsFp.startsWith('00000000')
  const hasLocator = para.srcPath && para.srcLStart != null

  const handleParaClick = (e) => {
    // 检视模式下的防误触拦截：首击只显式，不触发系统关联动画与语音
    if (isCloaked && !revealed) {
      setRevealed(true)
      return
    }
    
    // 如果已经显式，或在正常模式下，才触发正常的选中播放/同步滚动
    setRevealed(!revealed)
    if (onClick) onClick(e)
  }

  // 活动块
  if (para.type === 'activity') {
    // Quiz 专用渲染 — 结构化题目卡片
    if (para.activityType === 'Quiz' && para.quizQuestion) {
      return (
        <div className={`paragraph activity quiz${activeClass}${revealedClass}`} ref={ref} data-para-active={isActive} data-temp={para.temperature} data-tts-status={ttsStatus} onClick={handleParaClick}>
          <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
          <div className="para-content">
            <div className="activity-header">
              <span className="activity-badge quiz-badge">📝 测验</span>
              {para.duration && (
                <span className="activity-duration">⏱ {para.duration}</span>
              )}
            </div>
            {para.desc && <div className="activity-desc">{para.desc}</div>}
            <div className="quiz-question">{para.quizQuestion}</div>
            <div className="quiz-options">
              {(para.quizOptions || []).map((opt, idx) => (
                <div key={idx} className="quiz-option">{opt}</div>
              ))}
            </div>
            <QuizReveal answer={para.quizAnswer} explain={para.quizExplain} />
          </div>
        </div>
      )
    }
    // 通用 activity 渲染（Practice / QA / Workshop 等）
    return (
      <div className={`paragraph activity${activeClass}${revealedClass}`} ref={ref} data-para-active={isActive} data-temp={para.temperature} data-tts-status={ttsStatus} onClick={handleParaClick}>
        <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
        <div className="para-content">
          <div className="activity-header">
            <span className="activity-badge">
              {para.activityType || '实践'}
            </span>
            {para.duration && (
              <span className="activity-duration">⏱ {para.duration}</span>
            )}
          </div>
          {para.desc && <div className="activity-desc">{para.desc}</div>}
          <div>{formatText(para.text)}</div>
        </div>
      </div>
    )
  }

  // 技术注释
  if (para.type === 'tech_note') {
    return (
      <div className={`paragraph tech-note${activeClass}${revealedClass}`} ref={ref} data-para-active={isActive} data-temp={para.temperature} data-tts-status={ttsStatus} onClick={handleParaClick}>
        <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
        <div className="para-content">
          <div className="tag-label">{para.tag || 'TECH NOTE'}</div>
          <div>{formatText(para.text)}</div>
        </div>
      </div>
    )
  }

  // 口头标签（case study / story time 等）
  if (para.tag) {
    const tagClass = para.type.replace(/\s+/g, '_')
    const isLandmark = para.temperature === 'hot' && ['CASE STUDY', 'WARNING', 'STORY TIME'].includes(para.tag.toUpperCase());
    return (
      <div className={`paragraph tagged ${tagClass}${activeClass}${revealedClass}`} ref={ref} data-para-active={isActive} data-temp={para.temperature} data-tts-status={ttsStatus} onClick={handleParaClick}>
        <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
        <div className="para-content">
          <div className={`tag-label ${isLandmark ? 'landmark-badge' : ''}`}>
             {isLandmark ? `💥 ${para.tag}` : para.tag}
          </div>
          {para.anchorWord && (
            <div className="anchor-chip-container">
              <span className="anchor-chip">{para.anchorWord}</span>
            </div>
          )}
          <div>{formatText(para.text)}</div>
        </div>
      </div>
    )
  }

  // 普通演讲段落
  return (
    <div className={`paragraph speech${activeClass}${revealedClass}`} ref={ref} data-para-active={isActive} data-temp={para.temperature} data-tts-status={ttsStatus} onClick={handleParaClick}>
      <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
      <div className="para-content">
        {para.anchorWord && (
          <div className="anchor-chip-container">
            <span className="anchor-chip">{para.anchorWord}</span>
          </div>
        )}
        {formatText(para.text)}
      </div>
    </div>
  )
}), (prevProps, nextProps) => {
  // 自定义比较：当用户有活跃选区时，忽略 isActive 变化以保护选词
  if (prevProps.para === nextProps.para && prevProps.onClick === nextProps.onClick && prevProps.ttsStatus === nextProps.ttsStatus) {
    const sel = window.getSelection()
    if (sel && sel.toString().trim().length > 0) {
      return true
    }
  }
  return prevProps.para === nextProps.para
      && prevProps.isActive === nextProps.isActive
      && prevProps.ttsStatus === nextProps.ttsStatus
      && prevProps.onClick === nextProps.onClick
})

/**
 * ParaGutter — 段落左侧操作匣
 *
 * 常驻显示 TTS 按钮 + IDE 定位按钮。
 * 通过视觉层级区分：TTS 状态是主信息，定位是辅助。
 */
function ParaGutter({ paraIndex, para, hasTts, hasLocator }) {
  if (!hasTts && !hasLocator) return <div className="para-gutter empty" />

  return (
    <div className="para-gutter">
      {hasTts && (
        <TtsParaButton paraIndex={paraIndex} ttsFp={para.ttsFp} text={para.text} />
      )}
      {hasLocator && (
        <LocatorButton para={para} />
      )}
    </div>
  )
}

/**
 * LocatorButton — IDE 跳转 + 链接复制（原 CopyButton 重命名）
 */
function LocatorButton({ para }) {
  const [copied, setCopied] = useState(false)

  const handleJump = (e) => {
    e.stopPropagation()
    const ideUri = `antigravity://file${para.srcPath}:${para.srcLStart}`
    window.open(ideUri, '_self')
  }

  const handleCopy = (e) => {
    e.stopPropagation()
    e.preventDefault()
    const fileName = para.srcPath.split('/').pop() || '源文件'
    const copyText = `📍 修正建议 - [${fileName}](file://${para.srcPath}#L${para.srcLStart}-L${para.srcLEnd})`
    navigator.clipboard.writeText(copyText).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <button
      className={`locator-btn ${copied ? 'copied' : ''}`}
      title={`点击跳转 Antigravity · 右键复制链接\n${para.srcPath.split('/').pop()}:L${para.srcLStart}`}
      onClick={handleJump}
      onContextMenu={handleCopy}
    >
      {copied ? '✔' : '📍'}
    </button>
  )
}

/**
 * QuizReveal — Quiz 答案折叠区（MVP V1）
 *
 * 点击按钮展开/收起答案与解析。
 * 不做选项交互判定，仅作信息展示。
 */
function QuizReveal({ answer, explain }) {
  const [open, setOpen] = useState(false)
  if (!answer) return null
  return (
    <div className="quiz-reveal">
      <button className="quiz-reveal-btn" onClick={(e) => { e.stopPropagation(); setOpen(!open) }}>
        {open ? '🔽 收起答案' : '👉 查看答案与解析'}
      </button>
      {open && (
        <div className="quiz-reveal-content">
          <div className="quiz-answer">✅ 正确答案：{answer}</div>
          {explain && <div className="quiz-explain">{explain}</div>}
        </div>
      )}
    </div>
  )
}

/**
 * 简单的 Markdown → React 文本格式化
 */
function formatText(text) {
  if (!text) return null

  return text.split('\n\n').map((paragraph, i) => {
    const parts = paragraph.split(/(\*\*.*?\*\*)/).map((part, j) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={j}>{part.slice(2, -2)}</strong>
      }
      return part
    })

    const stableKey = `${i}_${paragraph.slice(0, 32)}`
    return <p key={stableKey} style={{ marginBottom: '0.75em' }}>{parts}</p>
  })
}
