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
export default function TextPanel({ paragraphs = [], activeParagraphIdx = -1, onParagraphSelect, slides = [] }) {
  const paraRefs = useRef([])
  const contentRef = useRef(null)
  const tts = useTtsSegments()

  // ── 选区守卫 ──
  const hasUserSelection = useRef(false)

  useEffect(() => {
    const onSelectionChange = () => {
      const sel = window.getSelection()
      hasUserSelection.current = !!(sel && sel.toString().trim().length > 0)
    }
    document.addEventListener('selectionchange', onSelectionChange)
    return () => document.removeEventListener('selectionchange', onSelectionChange)
  }, [])

  // 当 activeParagraphIdx 变化时，自动滚动到对应段落
  useEffect(() => {
    if (hasUserSelection.current) return
    if (activeParagraphIdx >= 0 && paraRefs.current[activeParagraphIdx]) {
      paraRefs.current[activeParagraphIdx].scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      })
    }
  }, [activeParagraphIdx])

  // 预计算 paragraphIdx → slideIdx 映射
  const slideDividerMap = useMemo(() => {
    const map = new Map()
    slides.forEach((slide, idx) => {
      if (slide.paragraphStart != null) {
        map.set(slide.paragraphStart, { idx, heading: slide.heading, total: slides.length })
      }
    })
    return map
  }, [slides])



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

  // 当前面包屑信息
  const breadcrumbInfo = useMemo(() => {
    if (slides.length === 0) return null
    return {
      total: slides.length,
    }
  }, [slides])

  if (!paragraphs.length) {
    return (
      <aside className="text-panel">
        <div className="text-panel-header">逐字稿</div>
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
      <div className="text-panel-header">
        {breadcrumbInfo ? (
          <span className="text-panel-breadcrumb">
            <span className="breadcrumb-label">逐字稿</span>
            <span className="breadcrumb-sep">›</span>
            <span className="breadcrumb-slide">
              Slide Count: {breadcrumbInfo.total}
            </span>
            {breadcrumbInfo.heading && (
              <>
                <span className="breadcrumb-sep">›</span>
                <span className="breadcrumb-heading">{breadcrumbInfo.heading}</span>
              </>
            )}
          </span>
        ) : '逐字稿'}
      </div>

      <TtsToolbar paragraphs={paragraphs} />

      <div className="text-panel-body">


        <div className="text-panel-content" ref={contentRef}>
          {paragraphs.map((para, i) => {
            const dividerInfo = slideDividerMap.get(i)
            return (
              <div key={para._fp || i}>
                {dividerInfo && (
                  <div className="slide-divider">
                    <span className="slide-divider-badge">Slide {dividerInfo.idx + 1}/{dividerInfo.total}</span>
                    {dividerInfo.heading && (
                      <span className="slide-divider-title">{dividerInfo.heading}</span>
                    )}
                  </div>
                )}
                <ParagraphBlock
                  para={para}
                  paraIndex={i}
                  isActive={i === activeParagraphIdx}
                  ttsStatus={tts?.segmentMap[i]?.status || 'missing'}
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
const ParagraphBlock = memo(forwardRef(function ParagraphBlock({ para, paraIndex, isActive, ttsStatus, onClick }, ref) {
  const activeClass = isActive ? ' active' : ''
  const hasTts = para.ttsFp && !para.ttsFp.startsWith('00000000')
  const hasLocator = para.srcPath && para.srcLStart != null

  // 活动块
  if (para.type === 'activity') {
    return (
      <div className={`paragraph activity${activeClass}`} ref={ref} data-para-active={isActive} data-scqa-role={para.scqaRole} data-tts-status={ttsStatus} onClick={onClick}>
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
      <div className={`paragraph tech-note${activeClass}`} ref={ref} data-para-active={isActive} data-scqa-role={para.scqaRole} data-tts-status={ttsStatus} onClick={onClick}>
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
    const isLandmark = para.scqaRole === 'c' && ['CASE STUDY', 'WARNING', 'STORY TIME'].includes(para.tag.toUpperCase());
    return (
      <div className={`paragraph tagged ${tagClass}${activeClass}`} ref={ref} data-para-active={isActive} data-scqa-role={para.scqaRole} data-tts-status={ttsStatus} onClick={onClick}>
        <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
        <div className="para-content">
          <div className={`tag-label ${isLandmark ? 'landmark-badge' : ''}`}>
             {isLandmark ? `💥 ${para.tag}` : para.tag}
          </div>
          <div>{formatText(para.text)}</div>
        </div>
      </div>
    )
  }

  // 普通演讲段落
  return (
    <div className={`paragraph speech${activeClass}`} ref={ref} data-para-active={isActive} data-scqa-role={para.scqaRole} data-tts-status={ttsStatus} onClick={onClick}>
      <ParaGutter paraIndex={paraIndex} para={para} hasTts={hasTts} hasLocator={hasLocator} />
      <div className="para-content">
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
