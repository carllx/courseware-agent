import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

/**
 * CoursePage — 课程周次列表页
 *
 * 展示某门课程的所有讲次卡片，包含 slides/段落数量、
 * 视觉完成度、音频/字幕状态。点击进入单讲预览。
 */
export default function CoursePage() {
  const { courseId } = useParams()
  const [manifest, setManifest] = useState(null)
  const [course, setCourse] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/courses/manifest.json')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(data => {
        setManifest(data)
        // P1 #3: 支持按 id / dirName / name 容错匹配
        const decoded = decodeURIComponent(courseId)
        const found = data.courses.find(c =>
          c.id === decoded || c.dirName === decoded || c.name === decoded
        )
        if (!found) {
          setError(`未找到课程: ${decoded}`)
          return
        }
        setCourse(found)
        document.title = `${found.name} — 课件预览`

        // 注入课程主题
        if (found.theme) {
          const root = document.documentElement
          Object.entries(found.theme).forEach(([key, value]) => {
            if (typeof value !== 'string') return
            root.style.setProperty(`--theme-${key}`, value)
          })
          if (found.theme.isDark) {
            root.style.setProperty('--theme-overlay-subtle', 'rgba(255,255,255,0.08)')
            root.style.setProperty('--theme-overlay-hover', 'rgba(255,255,255,0.04)')
          }
        }
      })
      .catch(err => setError(err.message))
  }, [courseId])

  if (error) {
    return (
      <div className="course-page">
        <div className="dashboard-error">
          <h2>⚠️ {error}</h2>
          <Link to="/" className="back-link">← 返回首页</Link>
        </div>
      </div>
    )
  }

  if (!course) {
    return (
      <div className="course-page">
        <div className="loading">
          <div className="loading-spinner" />
          <p>加载课程数据...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="course-page">
      <header className="course-page-header">
        <Link to="/" className="back-link">← 全部课程</Link>
        <h1 className="course-page-title">{course.name}</h1>
        <p className="course-page-meta">
          {course.semester && <span>{course.semester}</span>}
          {' · '}
          {course.weeks.length} 讲
          {course.structureType === 'phasic' && ' · 阶段制'}
        </p>
      </header>

      <main className="week-grid">
        {course.weeks.map((week, idx) => (
          <WeekCard
            key={week.script}
            week={week}
            index={idx}
            courseId={courseId}
            theme={course.theme}
          />
        ))}
      </main>
    </div>
  )
}

/**
 * WeekCard — 周次卡片
 */
function WeekCard({ week, index, courseId, theme }) {
  const primaryColor = theme?.primary || '#6c63ff'

  // 生成失败的讲次
  if (week.error) {
    return (
      <div className="week-card week-card-error">
        <div className="week-card-number" style={{ background: '#ef4444' }}>
          {index + 1}
        </div>
        <div className="week-card-body">
          <h3 className="week-card-title">{formatScriptName(week.script)}</h3>
          <p className="week-card-error-msg">❌ {week.error}</p>
        </div>
      </div>
    )
  }

  // 解析视觉覆盖
  let visualPercent = 0
  let visualLabel = '0/0'
  if (week.visualCoverage) {
    const [covered, total] = week.visualCoverage.split('/').map(Number)
    visualPercent = total > 0 ? Math.round((covered / total) * 100) : 0
    visualLabel = week.visualCoverage
  }

  // P1 #5: Emoji 图标配 tooltip 说明
  const statusIcon = visualPercent === 100 ? '✅' :
                     visualPercent > 50 ? '🔶' :
                     visualPercent > 0 ? '⚠️' : '📝'
  const statusTooltip = visualPercent === 100 ? '视觉素材已完整' :
                        visualPercent > 50 ? '视觉素材部分完成' :
                        visualPercent > 0 ? '视觉素材较少' : '尚无视觉素材'

  return (
    <Link
      to={`/${courseId}/${week.script}`}
      className="week-card"
      style={{ '--card-primary': primaryColor }}
    >
      <div className="week-card-number" style={{ background: primaryColor }}>
        {index + 1}
      </div>
      <div className="week-card-body">
        <h3 className="week-card-title">{formatScriptName(week.script)}</h3>
        <div className="week-card-stats">
          <span className="week-stat" title={statusTooltip}>{statusIcon} 图片 {visualLabel}</span>
          <span className="week-stat" title="幻灯片数量">📑 {week.slides} slides</span>
          <span className="week-stat week-stat-extra" title="文本段落数">📝 {week.paragraphs} 段</span>
          {week.sections > 0 && <span className="week-stat week-stat-extra" title="教学模块数">📦 {week.sections} 模块</span>}
        </div>
        <div className="week-card-badges">
          {week.hasAudio && <span className="badge badge-audio" title="含音频资源">🔊 音频</span>}
          {week.hasSrt && <span className="badge badge-srt" title="含字幕文件">📜 字幕</span>}
        </div>

        {/* 视觉覆盖率进度条 */}
        <div className="week-progress">
          <div className={`progress-bar${visualPercent === 0 ? ' progress-bar-empty' : ''}`}>
            <div className="progress-fill" style={{
              width: `${visualPercent}%`,
              background: primaryColor,
            }} />
          </div>
          <span className="progress-label">{visualPercent === 0 ? '尚无素材' : `${visualPercent}%`}</span>
        </div>
      </div>
    </Link>
  )
}

/**
 * 格式化脚本文件名为可读标题
 * W01_交互体系概论基础 → 交互体系概论基础
 * W01_Visual_Perception → Visual Perception
 */
function formatScriptName(name) {
  // 移除 W01_ 或 S01_ 前缀
  const stripped = name.replace(/^[WS]\d+_/, '')
  // 替换下划线为空格
  return stripped.replace(/_/g, ' ')
}
