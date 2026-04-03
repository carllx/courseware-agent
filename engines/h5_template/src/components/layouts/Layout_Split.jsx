/**
 * Layout_Split — 左右分屏布局
 * 左侧图片/灰盒，右侧 heading + scene 描述
 */
export default function Layout_Split({ slide }) {
  return (
    <>
      {slide.heading && <div className="slide-heading">{slide.heading}</div>}
      <div className="slide-body" style={{ gap: 0 }}>
        {/* 左侧：图片或灰盒 */}
        <div style={{ flex: '0 0 55%', display: 'flex' }}>
          {slide.resolvedImage ? (
            <img className="slide-image" src={slide.resolvedImage} alt={slide.heading || ''} />
          ) : (
            <div className="greybox">
              <span className="greybox-label">Split · 视觉</span>
              <span className="greybox-text">{slide.scene || '等待素材'}</span>
              {slide.assetExpected && (
                <span className="greybox-asset">📂 {slide.assetExpected}</span>
              )}
            </div>
          )}
        </div>
        {/* 右侧：列表或描述 */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '12px 16px' }}>
          {slide.list && slide.list.length > 0 ? (
            <ul className="slide-list">
              {slide.list.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          ) : (
            slide.scene && (
              <p style={{ fontSize: '13px', color: 'var(--theme-textSecondary)', lineHeight: 1.6 }}>
                {slide.scene}
              </p>
            )
          )}
        </div>
      </div>
    </>
  )
}
