import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

/**
 * Dashboard — 全课程总览主页
 *
 * 从 /courses/manifest.json 加载 workspace 级索引，
 * 展示所有课程的卡片概览，包含讲次数量和视觉完成度。
 */
export default function Dashboard() {
  const [manifest, setManifest] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    document.title = '课件预览平台 — H5'
    // 重置主题变量为默认
    const root = document.documentElement
    root.style.setProperty('--theme-bg', '#0f1117')
    root.style.setProperty('--theme-bgSurface', '#1a1d27')
    root.style.setProperty('--theme-bgElevated', '#252836')
    root.style.setProperty('--theme-text', '#e4e6eb')
    root.style.setProperty('--theme-textSecondary', '#8b8fa3')
    root.style.setProperty('--theme-primary', '#6c63ff')
    root.style.setProperty('--theme-border', '#2d3142')

    fetch('/courses/manifest.json')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(data => setManifest(data))
      .catch(err => setError(err.message))
  }, [])

  if (error) {
    return (
      <div className="dashboard">
        <div className="dashboard-error">
          <h2>⚠️ 数据加载失败</h2>
          <p>无法加载 <code>/courses/manifest.json</code></p>
          <p className="error-hint">{error}</p>
          <p className="error-hint">请先运行: <code>python engines/generate_course_h5.py --all</code></p>
        </div>
      </div>
    )
  }

  if (!manifest) {
    return (
      <div className="dashboard">
        <div className="loading">
          <div className="loading-spinner" />
          <p>加载课程数据...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="dashboard-header-content">
          <h1 className="dashboard-title">📚 课件预览平台</h1>
          <p className="dashboard-subtitle">
            {manifest.courses.length} 门课程 ·{' '}
            {manifest.courses.reduce((s, c) => s + c.weeks.length, 0)} 讲
          </p>
        </div>
      </header>

      <main className="dashboard-grid">
        {manifest.courses.map(course => (
          <CourseCard key={course.id} course={course} />
        ))}
      </main>

      <footer className="dashboard-footer">
        <span>生成于 {new Date(manifest.generated).toLocaleString('zh-CN')}</span>
      </footer>
    </div>
  )
}

/**
 * CourseCard — 课程概览卡片
 */
function CourseCard({ course }) {
  const totalWeeks = course.weeks.length
  const errorWeeks = course.weeks.filter(w => w.error).length
  const hasTheme = course.theme

  // 计算视觉完成度
  let totalSlides = 0
  let coveredSlides = 0
  let hasAnyAudio = false

  course.weeks.forEach(w => {
    if (w.error) return
    if (w.visualCoverage) {
      const [covered, total] = w.visualCoverage.split('/').map(Number)
      coveredSlides += covered
      totalSlides += total
    }
    if (w.hasAudio) hasAnyAudio = true
  })

  const visualPercent = totalSlides > 0 ? Math.round((coveredSlides / totalSlides) * 100) : 0

  // 卡片内联主题色
  const cardStyle = hasTheme ? {
    '--card-primary': course.theme.primary,
    '--card-bg': course.theme.isDark ? course.theme.bg : '#1a1d27',
    borderColor: course.theme.primary + '30',
  } : {}

  return (
    <Link to={`/${course.id}`} className="course-card" style={cardStyle}>
      <div className="course-card-header">
        <div
          className="course-card-accent"
          style={{ background: hasTheme ? course.theme.primary : '#6c63ff' }}
        />
        <h2 className="course-card-title">{course.name}</h2>
        <div className="course-card-badges">
          <span className="badge badge-weeks">{totalWeeks} 讲</span>
          {course.structureType === 'phasic' && (
            <span className="badge badge-type">阶段制</span>
          )}
          {hasAnyAudio && <span className="badge badge-audio" title="含音频资源">🔊</span>}
        </div>
      </div>

      <div className="course-card-stats">
        <div className="stat-row">
          <span className="stat-label">视觉覆盖</span>
          <div className="progress-bar">
            <div className="progress-fill" style={{
              width: `${visualPercent}%`,
              background: hasTheme ? course.theme.primary : '#6c63ff',
            }} />
          </div>
          <span className="stat-value">{visualPercent}%</span>
        </div>

        {errorWeeks > 0 && (
          <div className="stat-row error">
            <span className="stat-label">⚠️ 生成异常</span>
            <span className="stat-value">{errorWeeks} 讲</span>
          </div>
        )}
      </div>

      <div className="course-card-footer">
        <span className="card-link-hint">查看详情 →</span>
      </div>
    </Link>
  )
}
