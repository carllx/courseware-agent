import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_Split — 左右分屏布局
 * 经典学术极简组合：左 55%（或自适应）负责视觉/灰盒，右负责要点或描述。
 */
export default function Layout_Split({ slide }) {
  const hasList = slide.parsedList && slide.parsedList.length > 0;
  
  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className="h5-slide-body h5-layout-editorial-split">
        <AssetPlaceholder 
          slide={slide} 
          proportion={slide.scene && !slide.resolvedImage ? '100%' : '55%'} 
        />
        
        {/* 右侧：列表或描述 */}
        <div className="h5-split-content">
          {hasList ? (
            <EditorialList items={slide.parsedList} variant="bars" />
          ) : (
            (slide.text || slide.scene) && (
              <p className="h5-split-scene">
                {slide.text || slide.scene}
              </p>
            )
          )}
        </div>
      </div>
    </>
  )
}
