import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_Diagram — 图表/逻辑图布局
 * 严格遵照学术极简规范：左文右图（文包含编号，图为结构化表达）
 */
export default function Layout_Diagram({ slide }) {
  const hasList = slide.parsedList && slide.parsedList.length > 0;

  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className="h5-slide-body h5-layout-editorial-split h5-layout-editorial-split--reverse">
        {/* 左侧文字/编号逻辑节点 */}
        <div className="h5-split-content">
          {hasList ? (
            <EditorialList items={slide.parsedList} variant="numbered" />
          ) : (
            (slide.text || slide.scene) && (
              <p className="h5-split-scene">
                {slide.text || slide.scene}
              </p>
            )
          )}
        </div>

        {/* 右侧逻辑图 */}
        <AssetPlaceholder 
          slide={slide} 
          proportion={slide.scene && !slide.resolvedImage ? '100%' : '55%'} 
        />
      </div>
    </>
  )
}
