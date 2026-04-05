/**
 * DurationGauge — 模块时长/字数微型指示器（极简胶囊版）
 *
 * 嵌入 NavigationBar 的 tab 中，以紧凑文字胶囊显示填充率。
 * 第一性原理极简重构：去除干扰性的警报颜色和数字混排，用隐喻样式传达状态。
 */
import '../styles/craft-room.css'

export default function DurationGauge({ section }) {
  if (!section) return null

  const minutes = section.estimatedMinutes
  const fillRatio = section.fillRatio
  const budget = section.budgetChars

  // 无口述内容的模块（如纯活动模块）不显示
  if (minutes == null || minutes === 0) return null

  // 有 budget 时根据填充率决定展示方式
  if (budget && budget > 0 && fillRatio != null) {
    const percent = Math.min(Math.round(fillRatio * 100), 150)
    
    // 基于极简原则的三态隐喻计算
    const isUnderBudget = fillRatio < 0.8
    const isOverBudget = fillRatio > 1.2
    
    let statusClass = 'healthy'
    let hint = '进度健康'
    if (isUnderBudget) {
      statusClass = 'under-budget'
      hint = '内容单薄，请补充案例或讨论'
    } else if (isOverBudget) {
      statusClass = 'over-budget'
      hint = '信息过载，建议精简描述'
    }

    return (
      <span
        className={`gauge-capsule ${statusClass}`}
        title={`口述 ${section.oralCharCount} 字 / 预算 ${budget} 字 (${percent}%)\n💡 建议: ${hint}`}
      >
        {minutes}m
      </span>
    )
  }

  // 无 budget 时仅显示时长，归类为 healthy
  return (
    <span className="gauge-capsule healthy" title={`口述 ${section.oralCharCount} 字 (无硬性预算)`}>
      {minutes}m
    </span>
  )
}
