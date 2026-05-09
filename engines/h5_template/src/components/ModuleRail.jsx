import { useRef, useEffect, useState } from 'react'
import { useProgress } from '../contexts/ProgressContext'
import '../styles/module-rail.css'

/**
 * ModuleRail — ARC-02: 底部模块级导航条
 *
 * 替代原 NavigationBar：以 H2 模块为单位展示导航，
 * 每个模块 Tab 带有独立色相标记和完成度指示。
 *
 * 与旧 API 向后兼容：仍接收 sections + currentIdx + onSwitch。
 * 新增消费 manifest.modules 元数据提供视觉增强。
 */
export default function ModuleRail({ sections = [], modules = [], currentIdx, onSwitch, courseId, scriptName }) {
  const scrollRef = useRef(null)
  const [overflow, setOverflow] = useState({ left: false, right: false })
  const progress = useProgress()

  const checkOverflow = () => {
    const el = scrollRef.current
    if (!el) return
    setOverflow({
      left: el.scrollLeft > 4,
      right: el.scrollLeft + el.clientWidth < el.scrollWidth - 4,
    })
  }

  useEffect(() => {
    checkOverflow()
    const el = scrollRef.current
    if (!el) return
    el.addEventListener('scroll', checkOverflow, { passive: true })
    window.addEventListener('resize', checkOverflow)
    return () => {
      el.removeEventListener('scroll', checkOverflow)
      window.removeEventListener('resize', checkOverflow)
    }
  }, [sections])

  useEffect(() => {
    const el = scrollRef.current
    if (!el) return
    const activeTab = el.querySelector('.module-tab.active')
    if (activeTab) {
      activeTab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' })
    }
    setTimeout(checkOverflow, 300)
  }, [currentIdx])

  // 是否有 modules 元数据可用
  const hasModules = modules.length > 0

  return (
    <div className={`module-rail-wrapper${overflow.left ? ' has-overflow-left' : ''}${overflow.right ? ' has-overflow-right' : ''}`}>
      <nav className="module-rail" ref={scrollRef}>
        {sections.map((sec, idx) => {
          const mod = hasModules ? modules[idx] : null
          const isActive = idx === currentIdx
          const isRead = progress?.isRead?.(courseId, scriptName, sec.id)

          // 模块色相 → HSL 强调色
          const hue = mod?.colorHue ?? 210
          const accentColor = `hsl(${hue}, 60%, 55%)`

          return (
            <button
              key={sec.id}
              className={`module-tab ${isActive ? 'active' : ''} ${isRead && !isActive ? 'read' : ''}`}
              style={{ '--tab-accent': accentColor }}
              onClick={() => onSwitch(idx)}
              title={mod?.transitionHint || sec.title}
            >
              {/* 模块色相指示条 */}
              <span className="module-tab-accent" />

              {/* 图标 + 标题 */}
              <span className="module-tab-content">
                {mod?.heroIcon && (
                  <span className="module-tab-icon">{mod.heroIcon}</span>
                )}
                <span className="module-tab-label">
                  {mod ? _shortTitle(sec.title) : sec.title}
                </span>
              </span>

              {/* 已读标记 */}
              {isRead && !isActive && (
                <span className="module-tab-check">✓</span>
              )}
            </button>
          )
        })}
      </nav>
    </div>
  )
}

/**
 * 缩短模块标题用于 Tab 显示
 */
function _shortTitle(title) {
  // 移除 "Module N: " 前缀
  let s = title.replace(/^Module\s*\d+\s*[:：]\s*/i, '')
  // 移除时长标注
  s = s.replace(/\s*\(\d+\s*分钟\)\s*$/, '')
  // 移除 Markdown 加粗
  s = s.replace(/\*\*/g, '')
  // 截断
  if (s.length > 16) s = s.slice(0, 16) + '…'
  return s
}
