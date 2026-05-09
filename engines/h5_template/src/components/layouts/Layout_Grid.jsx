import AssetPlaceholder from '../primitives/AssetPlaceholder'

/**
 * Layout_Grid — 网格卡片矩阵布局（空间隔离架构）
 *
 * 策略：图文不重叠。
 *   - 当 image + items 共存时 → 采用类似 Editorial Split 的左右分割布局：图片 45%，卡片列表 55%（并保持网格特性或收缩为通栏）。
 *     - 若存在多张图片与多个项目数量一致，则融合为图文一体的混合卡片网格。
 *   - 仅有 image 时 → 全尺寸展示图片。
 *   - 仅有 items 时 → 全屏均分网格卡片瀑布流。
 */
export default function Layout_Grid({ slide }) {
  const items = slide.parsedList || []
  const hasItems = items.length > 0
  
  // 获取全部可用图片
  const images = (slide.resolvedImages && slide.resolvedImages.length > 0)
    ? slide.resolvedImages
    : (slide.resolvedImage ? [slide.resolvedImage] : [])
  const hasImage = images.length > 0

  // 1. 无数据无图片
  if (!hasItems && !hasImage) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body">
          <AssetPlaceholder customStyle={{ flex: 1 }} slide={slide} />
        </div>
      </>
    )
  }

  // 2. 只有图片
  if (hasImage && !hasItems) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className={`h5-slide-body ${images.length > 1 ? 'h5-layout-grid' : ''}`} style={images.length > 1 ? { display: 'grid', gap: '1rem', gridTemplateColumns: `repeat(${Math.min(images.length, 3)}, 1fr)`, padding: '16px' } : {}}>
          {images.map((img, i) => (
             <AssetPlaceholder key={i} slide={{...slide, resolvedImage: img}} proportion="100%" />
          ))}
        </div>
      </>
    )
  }

  // 3. 只有卡片数据 (原始经典网格瀑布)
  if (!hasImage && hasItems) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body h5-layout-grid">
          {items.map((item, i) => <GridCard key={i} item={item} />)}
        </div>
      </>
    )
  }

  // 4. 图片与卡片并存
  // 4a. 混合卡片模式: 图片数量与项目数量匹配（且数量>1）
  if (images.length > 1 && images.length === items.length) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        <div className="h5-slide-body h5-layout-grid">
          {items.map((item, i) => (
            <GridCard key={i} item={item} image={images[i]} />
          ))}
        </div>
      </>
    )
  }

  // 4b. 默认 Side-by-side 分形折叠布局
  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className="h5-slide-body h5-layout-grid-split">
        {/* 左侧：专属媒体展区 */}
        <div className="h5-grid-split-media" style={images.length > 1 ? { display: 'flex', flexDirection: 'column', gap: '1rem', overflowY: 'auto' } : {}}>
          {images.map((img, i) => (
            <AssetPlaceholder key={i} slide={{...slide, resolvedImage: img}} proportion="100%" customStyle={images.length > 1 ? { minHeight: '160px', flexShrink: 0 } : {}} />
          ))}
        </div>
        {/* 右侧：纵深滚动的网格列阵 */}
        <div className="h5-grid-split-content">
          <div className="h5-layout-grid h5-layout-grid--compact">
            {items.map((item, i) => <GridCard key={i} item={item} />)}
          </div>
        </div>
      </div>
    </>
  )
}

function GridCard({ item, image }) {
  const itemTitle = typeof item === 'string' ? item : item.title;
  const itemDesc = typeof item === 'string' ? '' : item.desc;

  if (image) {
    return (
      <div className="h5-grid-card" style={{ display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
        <div style={{ width: '100%', height: '140px', flexShrink: 0, background: 'var(--theme-bgDark)' }}>
          <img src={image} alt={itemTitle || ''} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
        </div>
        <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', flex: 1 }}>
          {itemTitle && <div className="h5-grid-card-title">{itemTitle}</div>}
          {itemDesc && <div className="h5-grid-card-desc">{itemDesc}</div>}
        </div>
      </div>
    )
  }

  return (
    <div className="h5-grid-card">
      {itemTitle && <div className="h5-grid-card-title">{itemTitle}</div>}
      {itemDesc && <div className="h5-grid-card-desc">{itemDesc}</div>}
    </div>
  )
}
