/**
 * HealthDot — 全局健康状态指示灯
 *
 * 遍历 manifest.sections 统计断链 slide 数和空模块数，
 * 显示为 🟢🟡🔴 圆点。点击弹出详情 Popover。
 */
import { useState, useMemo, useRef, useEffect } from 'react'
import '../styles/craft-room.css'

export default function HealthDot({ manifest }) {
  const [showPopover, setShowPopover] = useState(false)
  const popoverRef = useRef(null)

  // 点击外部关闭
  useEffect(() => {
    if (!showPopover) return
    const handleClickOutside = (e) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target)) {
        setShowPopover(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [showPopover])

  const stats = useMemo(() => {
    if (!manifest?.sections) return null

    let brokenSlides = 0
    let totalSlides = 0
    let emptyModules = 0
    let underfilledModules = 0
    const issues = []

    manifest.sections.forEach((sec, idx) => {
      // 空模块
      if (!sec.paragraphs || sec.paragraphs.length === 0) {
        emptyModules++
        issues.push({ type: 'empty', module: sec.title, idx })
      }

      // 字数不足
      if (sec.fillRatio != null && sec.fillRatio < 0.8) {
        underfilledModules++
        issues.push({
          type: 'underfilled',
          module: sec.title,
          idx,
          fillRatio: sec.fillRatio,
          oralCharCount: sec.oralCharCount,
          budgetChars: sec.budgetChars,
        })
      }

      // 断链 slides
      if (sec.slides) {
        sec.slides.forEach(slide => {
          totalSlides++
          if (slide.assetExpected && !slide.image) {
            brokenSlides++
            issues.push({ type: 'broken', module: sec.title, slideId: slide.id, idx })
          }
        })
      }
    })

    return { brokenSlides, totalSlides, emptyModules, underfilledModules, issues }
  }, [manifest])

  if (!stats) return null

  // 健康度判定
  let color, label
  if (stats.emptyModules > 0 || stats.underfilledModules > 0) {
    color = 'red'
    label = '需要关注'
  } else if (stats.brokenSlides > 0) {
    color = 'yellow'
    label = '图片待补'
  } else {
    color = 'green'
    label = '健康'
  }

  return (
    <div className="health-dot-container" ref={popoverRef}>
      <button
        className={`health-dot health-dot--${color}`}
        onClick={() => setShowPopover(prev => !prev)}
        title={label}
      >
        <span className="health-dot-pulse" />
      </button>

      {showPopover && (
        <div className="health-popover">
          <div className="health-popover-header">
            <span className={`health-status health-status--${color}`}>
              {color === 'green' ? '✅' : color === 'yellow' ? '🟡' : '🔴'} {label}
            </span>
          </div>
          <div className="health-popover-body">
            <div className="health-stat-row">
              <span>📊 总 Slides</span>
              <span>{stats.totalSlides}</span>
            </div>
            {stats.brokenSlides > 0 && (
              <div className="health-stat-row warning">
                <span>🔗 断链 Slides</span>
                <span>{stats.brokenSlides}</span>
              </div>
            )}
            {stats.underfilledModules > 0 && (
              <div className="health-stat-row error">
                <span>📝 字数不足模块</span>
                <span>{stats.underfilledModules}</span>
              </div>
            )}
            {stats.emptyModules > 0 && (
              <div className="health-stat-row error">
                <span>📭 空模块</span>
                <span>{stats.emptyModules}</span>
              </div>
            )}
          </div>
          {stats.issues.length > 0 && (
            <div className="health-popover-issues">
              {stats.issues.slice(0, 8).map((issue, i) => (
                <div key={i} className="health-issue">
                  {issue.type === 'broken' && (
                    <span>🔗 <strong>{issue.slideId}</strong> — {issue.module}</span>
                  )}
                  {issue.type === 'underfilled' && (
                    <span>📝 {issue.module} — {issue.oralCharCount}/{issue.budgetChars} ({Math.round(issue.fillRatio * 100)}%)</span>
                  )}
                  {issue.type === 'empty' && (
                    <span>📭 {issue.module} — 无内容</span>
                  )}
                </div>
              ))}
              {stats.issues.length > 8 && (
                <div className="health-issue muted">
                  ...还有 {stats.issues.length - 8} 项
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
