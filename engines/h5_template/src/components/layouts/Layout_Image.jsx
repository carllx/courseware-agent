import AssetPlaceholder from '../primitives/AssetPlaceholder'

/**
 * Layout_Image — 全屏图片布局
 * 纯图片展示，带标题容错
 */
export default function Layout_Image({ slide }) {
  return (
    <>
      {slide.heading && <div className="h5-slide-heading">{slide.heading}</div>}
      <div className="h5-slide-body">
        <AssetPlaceholder slide={slide} proportion="100%" />
      </div>
    </>
  )
}
