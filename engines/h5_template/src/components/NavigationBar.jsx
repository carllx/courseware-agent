import { useRef, useEffect, useState } from 'react'

/**
 * NavigationBar — 底部模块导航条
 * P1 #6: 增加滚动指示器（渐变遮罩）
 */
export default function NavigationBar({ sections = [], currentIdx, onSwitch }) {
  const scrollRef = useRef(null)
  const [overflow, setOverflow] = useState({ left: false, right: false })

  // 检测滚动溢出状态
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

  // 当 currentIdx 变化时，自动滚动到激活的 tab
  useEffect(() => {
    const el = scrollRef.current
    if (!el) return
    const activeTab = el.querySelector('.nav-tab.active')
    if (activeTab) {
      activeTab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' })
    }
    // 延迟检测溢出状态（等滚动完成）
    setTimeout(checkOverflow, 300)
  }, [currentIdx])

  return (
    <div className={`nav-bar-wrapper${overflow.left ? ' has-overflow-left' : ''}${overflow.right ? ' has-overflow-right' : ''}`}>
      <nav className="nav-bar" ref={scrollRef}>
        {sections.map((sec, idx) => (
          <button
            key={sec.id}
            className={`nav-tab ${idx === currentIdx ? 'active' : ''}`}
            onClick={() => onSwitch(idx)}
          >
            {sec.title}
            {sec.slides?.length > 0 && (
              <span className="slide-count">{sec.slides.length}</span>
            )}
          </button>
        ))}
      </nav>
    </div>
  )
}
