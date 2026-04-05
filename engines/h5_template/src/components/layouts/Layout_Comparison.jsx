import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_Comparison — 对比表布局
 * 严谨的双栏对比布局
 */
export default function Layout_Comparison({ slide }) {
  // 如果有图片，优先全幅展现（用于设计稿对比图等场景）
  if (slide.resolvedImage) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body">
          <AssetPlaceholder slide={slide} proportion="100%" />
        </div>
      </>
    )
  }

  // 从数据代理层获取已清洗对比数据或回退的列表数据
  const comparisonData = slide.comparisonData
  const parsedList = slide.parsedList || []
  const hasData = comparisonData || parsedList.length > 0

  // 无任何内容时显示占位符
  if (!hasData) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body">
          <AssetPlaceholder slide={slide} proportion="100%" />
        </div>
      </>
    )
  }

  // 回退渲染逻辑：没有明确的 left/right 则均分普通列表
  if (!comparisonData) {
    const leftItems = parsedList.filter((_, i) => i % 2 === 0)
    const rightItems = parsedList.filter((_, i) => i % 2 === 1)
    
    return (
      <ComparisonView 
        heading={slide.heading}
        leftLabel="左侧" rightLabel="右侧"
        leftItems={leftItems} rightItems={rightItems}
      />
    )
  }

  // 渲染高保真对比图
  const { left, right } = comparisonData
  return (
    <ComparisonView 
      heading={slide.heading}
      leftLabel={left.label || '正方'} rightLabel={right.label || '反方'}
      leftItems={left.items} rightItems={right.items}
    />
  )
}

function ComparisonView({ heading, leftLabel, rightLabel, leftItems, rightItems }) {
  return (
    <>
      {heading && <div className="h5-slide-heading">{heading}</div>}
      <div className="h5-slide-body h5-layout-comparison">
        {/* 左栏（正面、绿色基调） */}
        <div className="h5-comparison-col h5-comparison-col--positive">
          <div className="h5-comparison-header">
            <span className="h5-comparison-icon">✓</span> {leftLabel}
          </div>
          <div className="h5-comparison-list">
            <EditorialList items={leftItems} variant="numbered" customStyle={{ gap: '8px' }} />
          </div>
        </div>
        
        {/* 右栏（反面、红色基调） */}
        <div className="h5-comparison-col h5-comparison-col--negative">
          <div className="h5-comparison-header">
            <span className="h5-comparison-icon">✗</span> {rightLabel}
          </div>
          <div className="h5-comparison-list">
            <EditorialList items={rightItems} variant="numbered" customStyle={{ gap: '8px' }} />
          </div>
        </div>
      </div>
    </>
  )
}
