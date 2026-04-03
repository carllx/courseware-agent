/**
 * Layout_List — 列表卡片布局
 * 标题 + 列表项
 */
export default function Layout_List({ slide }) {
  return (
    <>
      {slide.heading && <div className="slide-heading">{slide.heading}</div>}
      <div className="slide-body" style={{ flexDirection: 'column' }}>
        {slide.resolvedImage ? (
          <div style={{ flex: '0 0 40%', display: 'flex' }}>
            <img className="slide-image" src={slide.resolvedImage} alt="" />
          </div>
        ) : null}
        <div style={{ flex: 1, overflow: 'auto' }}>
          {slide.list && slide.list.length > 0 ? (
            <ul className="slide-list">
              {slide.list.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          ) : (
            <div className="greybox">
              <span className="greybox-label">List</span>
              <span className="greybox-text">{slide.scene || '等待列表内容'}</span>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
