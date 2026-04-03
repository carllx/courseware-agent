/**
 * Layout_Grid — 网格布局
 * 标题 + 列表项以网格形式排列
 */
export default function Layout_Grid({ slide }) {
  return (
    <>
      {slide.heading && <div className="slide-heading">{slide.heading}</div>}
      <div className="slide-body" style={{ flexWrap: 'wrap', padding: '12px', gap: '8px', alignContent: 'start' }}>
        {slide.resolvedImage ? (
          <img className="slide-image" src={slide.resolvedImage} alt="" />
        ) : slide.list && slide.list.length > 0 ? (
          slide.list.map((item, i) => (
            <div key={i} style={{
              flex: '1 1 calc(50% - 8px)',
              minWidth: '140px',
              padding: '12px',
              background: 'var(--theme-bgElevated)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '13px',
              lineHeight: 1.5,
              borderLeft: '3px solid var(--theme-primary)',
            }}>
              {item}
            </div>
          ))
        ) : (
          <div className="greybox">
            <span className="greybox-label">Grid</span>
            <span className="greybox-text">{slide.scene || '等待网格内容'}</span>
          </div>
        )}
      </div>
    </>
  )
}
