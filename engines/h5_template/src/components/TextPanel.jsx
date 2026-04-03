import { useRef, useEffect, useMemo, useState } from 'react'

/**
 * TextPanel — 逐字稿文本面板
 * 
 * 将 PPT 中不可见的 Speaker Notes 以可阅读的形式呈现。
 * 支持 speech、oral tags（case study 等）、tech note、activity 等多种段落类型。
 *
 * Props:
 *   paragraphs        — 段落数组
 *   activeParagraphIdx — 当前高亮的段落索引（section 内），-1 表示无高亮
 *   onParagraphClick   — (srtCueIdx) => void, 点击段落时触发音频 seek
 *   slides             — 当前 section 的 slides 数组，用于渲染分隔线
 */
export default function TextPanel({ paragraphs = [], activeParagraphIdx = -1, onParagraphClick, onParagraphSelect, slides = [] }) {
  const paraRefs = useRef([])

  // 当 activeParagraphIdx 变化时，自动滚动到对应段落
  useEffect(() => {
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
      <div className="text-panel-header">逐字稿</div>
      <div className="text-panel-content">
        {paragraphs.map((para, i) => {
          const dividerInfo = slideDividerMap.get(i)
          return (
            <div key={i}>
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
                isActive={i === activeParagraphIdx}
                ref={el => (paraRefs.current[i] = el)}
                onClick={() => {
                  const selection = window.getSelection()
                  if (selection && selection.toString().trim().length > 0) {
                    return // 忽略拖拽选择引发的点击
                  }
                  if (onParagraphSelect) {
                    onParagraphSelect(i, para.srtCueIdx)
                  } else if (onParagraphClick && para.srtCueIdx != null) {
                    onParagraphClick(para.srtCueIdx)
                  }
                }}
              />
            </div>
          )
        })}
      </div>
    </aside>
  )
}

import { forwardRef } from 'react'

const ParagraphBlock = forwardRef(function ParagraphBlock({ para, isActive, onClick }, ref) {
  const activeClass = isActive ? ' active' : ''

  // 活动块
  if (para.type === 'activity') {
    return (
      <div className={`paragraph activity${activeClass}`} ref={ref} data-para-active={isActive} onClick={onClick} style={{ position: 'relative' }}>
        <CopyButton para={para} />
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
    )
  }

  // 技术注释（参考型标签）
  if (para.type === 'tech_note') {
    return (
      <div className={`paragraph tech-note${activeClass}`} ref={ref} data-para-active={isActive} onClick={onClick} style={{ position: 'relative' }}>
        <CopyButton para={para} />
        <div className="tag-label">{para.tag || 'TECH NOTE'}</div>
        <div>{formatText(para.text)}</div>
      </div>
    )
  }

  // 口头标签（case study / story time 等）
  if (para.tag) {
    const tagClass = para.type.replace(/\s+/g, '_')
    return (
      <div className={`paragraph tagged ${tagClass}${activeClass}`} ref={ref} data-para-active={isActive} onClick={onClick} style={{ position: 'relative' }}>
        <CopyButton para={para} />
        <div className="tag-label">{para.tag}</div>
        <div>{formatText(para.text)}</div>
      </div>
    )
  }

  // 普通演讲段落
  return (
    <div className={`paragraph speech${activeClass}`} ref={ref} data-para-active={isActive} onClick={onClick} style={{ position: 'relative' }}>
      <CopyButton para={para} />
      {formatText(para.text)}
    </div>
  )
})

function CopyButton({ para }) {
  const [copied, setCopied] = useState(false)

  if (!para.srcPath || para.srcLStart == null) return null

  const handleCopy = (e) => {
    e.stopPropagation()
    const fileName = para.srcPath.split('/').pop() || '源文件'
    const copyText = `📍 修正建议 - [${fileName}](file://${para.srcPath}#L${para.srcLStart}-L${para.srcLEnd})`
    navigator.clipboard.writeText(copyText).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <button
      className="copy-locator-btn"
      title="复制定位地址至剪贴板供 Agent 修改使用"
      onClick={handleCopy}
      style={{
        position: 'absolute',
        right: '0.25rem',
        top: '0.25rem',
        background: 'transparent',
        border: 'none',
        cursor: 'pointer',
        opacity: copied ? 0.8 : 0.05,
        fontSize: '0.9rem',
        padding: '0.2rem',
        transition: 'opacity 0.2s',
      }}
      onMouseEnter={(e) => {
        if (!copied) e.currentTarget.style.opacity = 1;
      }}
      onMouseLeave={(e) => {
        if (!copied) e.currentTarget.style.opacity = 0.05;
      }}
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
    // 处理加粗
    const parts = paragraph.split(/(\*\*.*?\*\*)/).map((part, j) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={j}>{part.slice(2, -2)}</strong>
      }
      return part
    })

    return <p key={i} style={{ marginBottom: '0.75em' }}>{parts}</p>
  })
}
