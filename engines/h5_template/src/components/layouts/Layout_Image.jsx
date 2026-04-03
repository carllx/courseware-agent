/**
 * Layout_Image — 全屏图片布局
 * 纯图片展示，带标题
 *
 * C5 降级: 无图片时显示场景描述和预期素材路径
 */
export default function Layout_Image({ slide }) {
  return (
    <>
      {slide.heading && <div className="slide-heading">{slide.heading}</div>}
      <div className="slide-body">
        {slide.resolvedImage ? (
          <img className="slide-image" src={slide.resolvedImage} alt={slide.heading || ''} />
        ) : (
          <div className="greybox">
            <span className="greybox-label">{slide.layout || 'Image'}</span>
            <span className="greybox-text">{slide.scene || '等待图片素材'}</span>
            {slide.assetExpected && (
              <span className="greybox-asset">📂 {slide.assetExpected}</span>
            )}
          </div>
        )}
      </div>
    </>
  )
}
