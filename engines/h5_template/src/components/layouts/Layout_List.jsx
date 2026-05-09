import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_List — 列表卡片布局
 * 标题 + 可选图片配图的垂直列表项
 */
export default function Layout_List({ slide }) {
  const items = slide.parsedList || []
  const hasList = items.length > 0
  const hasImage = !!slide.resolvedImage
  
  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className={`h5-slide-body ${hasImage && hasList ? 'h5-layout-editorial-split' : 'h5-layout-list-wrapper'}`}>
        {hasImage && (
          <AssetPlaceholder 
            slide={slide} 
            proportion={hasList ? '45%' : '100%'} 
          />
        )}
        <div className={hasImage && hasList ? 'h5-split-content' : 'h5-list-container'}>
          {hasList ? (
            <EditorialList items={items} variant="numbered" />
          ) : (
            /* 当没有解析出列表时，且没有图片时才抛出占位符 */
            !hasImage && (
              <div className="h5-asset-box h5-asset-box--placeholder" style={{ flex: 1 }}>
                <span className="h5-asset-label">List</span>
                <span className="h5-asset-desc">{slide.scene || '等待列表数据'}</span>
              </div>
            )
          )}
        </div>
      </div>
    </>
  )
}
