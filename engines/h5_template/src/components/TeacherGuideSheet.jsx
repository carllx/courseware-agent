import React from 'react'
import '../styles/teacher-guide.css'

export default function TeacherGuideSheet({ isOpen, targetIdx, stat, onClose, onNavigate }) {
  if (!isOpen || !stat) return null

  const { temp, totalChars } = stat

  // 映射文案与主题
  let title = "平顺过渡区"
  let suggestion = "保持当前的节奏，清晰传达概念，无需过多额外渲染。"
  let icon = "📝"
  let themeClass = "theme-neutral"

  if (temp === "hot") {
    title = "高点情绪池"
    suggestion = "🚀 推荐脱稿抛出互动问题，或分享行业案例，拉高课堂沉浸感。"
    icon = "🔥"
    themeClass = "theme-hot"
  } else if (temp === "cold") {
    title = "硬核知识消化期"
    suggestion = "📉 干货密集区域，建议放慢语速，辅以板书拆解关键逻辑。"
    icon = "🧊"
    themeClass = "theme-cold"
  }

  // 估算讲解时长 (按每分钟 200 字，约 3.3 字/秒计算。基础缓冲 10 秒)
  const estSeconds = Math.max(10, Math.round((totalChars || 0) / 3.3))
  const formatTime = (secs) => {
    if (secs < 60) return `${secs} 秒`
    const m = Math.floor(secs / 60)
    const s = secs % 60
    return `${m} 分 ${s} 秒`
  }

  return (
    <div className="teacher-guide-overlay" onClick={onClose}>
      <div className={`teacher-guide-sheet ${themeClass}`} onClick={e => e.stopPropagation()}>
        <div className="sheet-handle" onClick={onClose}></div>
        
        <div className="sheet-header">
          <div className="sheet-icon">{icon}</div>
          <div className="sheet-title-group">
            <h3 className="sheet-title">{title}</h3>
            <span className="sheet-time-badge">
              <span>⏳ 预计时长:</span>
              <strong>{formatTime(estSeconds)}</strong>
            </span>
          </div>
        </div>
        
        <div className="sheet-body">
          <p className="sheet-suggestion">{suggestion}</p>
          <div className="sheet-stats">
            <span className="stat-item">字数负载: <strong>{totalChars || 0} 字</strong></span>
            <span className="stat-item">当前段落流属性: <strong>{temp.toUpperCase()}</strong></span>
          </div>
        </div>

        <div className="sheet-actions">
          <button className="sheet-btn sheet-btn-secondary" onClick={onClose}>
            关闭预览
          </button>
          <button className="sheet-btn sheet-btn-primary" onClick={onNavigate}>
            导播：同步大图展示此页
          </button>
        </div>
      </div>
    </div>
  )
}
