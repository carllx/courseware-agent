/**
 * Layout_Diagram — 图表/流程图布局
 * 全幅图片 + 标题
 */
export default function Layout_Diagram({ slide }) {
  return (
    <>
      {slide.heading && <div className="slide-heading">{slide.heading}</div>}
      <div className="slide-body">
        {slide.resolvedImage ? (
          <img className="slide-image" src={slide.resolvedImage} alt={slide.heading || ''} />
        ) : (
          <div className="greybox">
            <span className="greybox-label">Diagram</span>
            <span className="greybox-text">{slide.scene || '等待图表素材'}</span>
          </div>
        )}
      </div>
    </>
  )
}
