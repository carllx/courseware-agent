import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_Comparison — 对比表布局（空间隔离架构）
 *
 * 策略：图文不重叠，各自保留绝对语义主权。
 *   - 当 image + content 共存时（单图） → 上下分离 Hybrid，上方主图（45% 高度），下方左右横向对比（55% 高度带溢出滚动处理）
 *   - 当 images 存在且 >= 2 时（多图） → 左右纯分形，左栏嵌左图，右栏嵌右图。（防御性前瞻逻辑）
 *   - 仅含 image 无 list 时 → 仍全幅图占位
 *   - 仅含 list 无 image 时 → 正常横向对比
 */
export default function Layout_Comparison({ slide }) {
  const comparisonData = slide.comparisonData
  const parsedList = slide.parsedList || []
  const hasContent = comparisonData || parsedList.length > 0

  // 整理图片数组：如果含有 resolvedImages 数组而且里面有东西就用它，否则用单一的 resolvedImage
  let imgs = []
  if (Array.isArray(slide.resolvedImages) && slide.resolvedImages.length > 0) {
    // 很多原先的逻辑可能会把单数图像路径重复压入数组，所以做个简单的去重
    imgs = Array.from(new Set(slide.resolvedImages.filter(Boolean)))
  } else if (slide.resolvedImage) {
    imgs = [slide.resolvedImage]
  }
  
  // 仅当只有图片没有任何文本 list 时，退回全尺寸背景图片占位图
  if (imgs.length > 0 && !hasContent) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body">
          <AssetPlaceholder slide={{...slide, resolvedImage: imgs[0]}} proportion="100%" />
        </div>
      </>
    )
  }

  // 没有任何有效信息
  if (!hasContent && imgs.length === 0) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body">
          <AssetPlaceholder customStyle={{ flex: 1 }} slide={slide} />
        </div>
      </>
    )
  }

  // 获取左右数据内容
  let leftLabel = '对比项 A', rightLabel = '对比项 B', leftItems = [], rightItems = []
  if (comparisonData) {
    leftLabel = comparisonData.left.label || '对比项 A'
    rightLabel = comparisonData.right.label || '对比项 B'
    leftItems = comparisonData.left.items
    rightItems = comparisonData.right.items
  } else if (hasContent) {
    leftLabel = '左侧'
    rightLabel = '右侧'
    leftItems = parsedList.filter((_, i) => i % 2 === 0)
    rightItems = parsedList.filter((_, i) => i % 2 === 1)
  }

  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      {imgs.length >= 2 ? (
        // --- 方案 A: 拥有 2 张以上图片（双图独立挂载轨道） ---
        <div className="h5-slide-body h5-layout-comparison">
          <ComparisonCol 
            type="positive" label={leftLabel} items={leftItems} 
            innerImage={imgs[0]}
          />
          <ComparisonCol 
            type="negative" label={rightLabel} items={rightItems} 
            innerImage={imgs[1]}
          />
        </div>
      ) : imgs.length === 1 ? (
        // --- 方案 B: 拥有 1 张独立主图（上下分断版式） ---
        <div className="h5-slide-body h5-layout-comparison-hybrid">
          <div className="h5-comparison-hero">
            <AssetPlaceholder slide={{...slide, resolvedImage: imgs[0]}} proportion="100%" />
          </div>
          <div className="h5-comparison-body">
            <ComparisonCol type="positive" label={leftLabel} items={leftItems} />
            <ComparisonCol type="negative" label={rightLabel} items={rightItems} />
          </div>
        </div>
      ) : (
        // --- 方案 C: 无图（纯数据结构原生展示） ---
        <div className="h5-slide-body h5-layout-comparison">
          <ComparisonCol type="positive" label={leftLabel} items={leftItems} />
          <ComparisonCol type="negative" label={rightLabel} items={rightItems} />
        </div>
      )}
    </>
  )
}

function ComparisonCol({ type, label, items, innerImage }) {
  return (
    <div className={`h5-comparison-col h5-comparison-col--${type}`}>
      <div className="h5-comparison-header">
        {label}
      </div>
      {innerImage && (
        <div className="h5-comparison-inner-media">
          <img src={innerImage} alt={label} />
        </div>
      )}
      <div className="h5-comparison-list">
        <EditorialList items={items} variant="numbered" customStyle={{ gap: '8px' }} />
      </div>
    </div>
  )
}
