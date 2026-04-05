import AssetPlaceholder from '../primitives/AssetPlaceholder'

/**
 * Layout_Grid — 网格卡片矩阵布局
 * 带有 Subtle 阴影和强调色描边的信息卡片阵列
 */
export default function Layout_Grid({ slide }) {
  const items = slide.parsedList || []
  
  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className="h5-slide-body h5-layout-grid">
        {slide.resolvedImage ? (
          <AssetPlaceholder slide={slide} proportion="100%" />
        ) : items && items.length > 0 ? (
          items.map((item, i) => {
            const itemTitle = typeof item === 'string' ? item : item.title;
            const itemDesc = typeof item === 'string' ? '' : item.desc;
            
            return (
              <div key={i} className="h5-grid-card">
                {itemTitle && <div className="h5-grid-card-title">{itemTitle}</div>}
                {itemDesc && <div className="h5-grid-card-desc">{itemDesc}</div>}
              </div>
            )
          })
        ) : (
          <AssetPlaceholder customStyle={{ flex: 1 }} slide={slide} />
        )}
      </div>
    </>
  )
}
