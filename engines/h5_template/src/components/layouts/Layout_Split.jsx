import AssetPlaceholder from '../primitives/AssetPlaceholder'
import EditorialList from '../primitives/EditorialList'

/**
 * Layout_Split — 左右分屏布局
 * 
 * 三种模式：
 * 1. 双图模式 (resolvedImages >= 2): 左右各一张图，标题居上
 * 2. 单图+列表模式 (有 list): 左图 55% + 右侧要点列表
 * 3. 单图+文本模式 (默认): 左图 55% + 右侧描述文字
 */
export default function Layout_Split({ slide }) {
  const hasList = slide.parsedList && slide.parsedList.length > 0;
  const hasMultiImages = slide.resolvedImages && slide.resolvedImages.length >= 2;

  // ── 双图 Split 模式 ──
  if (hasMultiImages) {
    return (
      <>
        {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
        {slide.text && <div className="h5-split-title-bar">{slide.text}</div>}
        <div className="h5-slide-body h5-layout-split-dual">
          {slide.resolvedImages.slice(0, 2).map((img, i) => (
            <div className="h5-split-dual-pane" key={i}>
              <img
                className="slide-image"
                src={img}
                alt={`${slide.heading || slide.text || ''} ${i + 1}`}
              />
            </div>
          ))}
        </div>
      </>
    )
  }

  // ── 单图模式（原有逻辑） ──
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
