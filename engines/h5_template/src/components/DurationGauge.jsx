/**
 * DurationGauge — 模块时长/字数微型指示器（极简胶囊版）
 *
 * 嵌入 NavigationBar 的 tab 中，以紧凑文字胶囊显示填充率。
 * 第一性原理极简重构：去除干扰性的警报颜色和数字混排，用隐喻样式传达状态。
 */
import '../styles/craft-room.css'

export default function DurationGauge({ section }) {
  if (!section) return null

  const minutes = section.estimatedMinutes || 0
  const actMinutes = section.activityMinutes || 0
  const fillRatio = section.fillRatio
  const budget = section.budgetChars

  // 无口述且无实践内容的模块不显示
  if (minutes === 0 && actMinutes === 0) return null

  let overloadClass = ''
  let statusClass = 'healthy'
  let hint = '进度健康'

  // 防倦怠预警：如果连续讲述超过 15 分钟且该模块没有插入任何实践互动
  if (minutes > 15 && actMinutes === 0) {
    overloadClass = ' overload-alert'
    hint = '单口讲述过长，建议插入 ACTIVITY'
  }

  // 有 budget 时根据填充率决定基底展示方式
  if (budget && budget > 0 && fillRatio != null) {
    const percent = Math.min(Math.round(fillRatio * 100), 150)
    
    // 基于极简原则的推断
    const isUnderBudget = fillRatio < 0.8
    const isOverBudget = fillRatio > 1.2
    
    if (isUnderBudget) {
      statusClass = 'under-budget'
      hint = hint === '进度健康' ? '内容单薄，请补充案例或讨论' : hint
    } else if (isOverBudget) {
      statusClass = 'over-budget'
      hint = hint === '进度健康' ? '信息过载，建议精简描述' : hint
    }

    return (
      <span
        className={`gauge-capsule ${statusClass}${overloadClass}`}
        title={`口述 ${section.oralCharCount} 字 / 预算 ${budget} 字 (${percent}%)\n💡 建议: ${hint}`}
      >
        🗣️ {minutes}m {actMinutes > 0 ? `| 🛠️ ${actMinutes}m` : ''}
      </span>
    )
  }

  // 无 budget 时
  return (
    <span className={`gauge-capsule healthy${overloadClass}`} title={`口述 ${section.oralCharCount} 字 (无硬性预算)\n💡 建议: ${hint}`}>
      🗣️ {minutes}m {actMinutes > 0 ? `| 🛠️ ${actMinutes}m` : ''}
    </span>
  )
}
