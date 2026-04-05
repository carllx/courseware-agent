import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_List — 列表卡片布局
 * 标题 + 可选图片配图的垂直列表项
 */
export default function Layout_List({ slide }) {
  const items = slide.parsedList || []
  
  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className="h5-slide-body h5-layout-list-wrapper">
        <div className="h5-list-container">
          {items.length > 0 ? (
            <EditorialList items={items} variant="numbered" />
          ) : (
            /* 当没有解析出列表时，才回退显示图片或占位符 */
            slide.resolvedImage ? (
              <AssetPlaceholder slide={slide} proportion="100%" customStyle={{ display: 'flex' }} />
            ) : (
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
