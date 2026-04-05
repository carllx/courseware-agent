/**
 * Layout_Title — 标题/总结/引言布局
 * 居中大标题 + 可选副文本，极简留白风格
 */
export default function Layout_Title({ slide }) {
  return (
    <div className={`h5-layout-title ${slide.resolvedImage ? 'h5-layout-title--with-bg' : ''}`}>
      {slide.resolvedImage && (
        <img
          src={slide.resolvedImage}
          alt=""
          className="h5-layout-title-bg"
        />
      )}
      <h2 className="h5-layout-title-heading">
        {slide.heading || slide.text || slide.scene || slide.id}
      </h2>
      {slide.parsedList && slide.parsedList.length > 0 && (
        <div className="h5-layout-title-subtext-container">
          {slide.parsedList.map((item, i) => {
            const itemText = typeof item === 'string' ? item : item.title;
            return (
              <span key={i} className="h5-layout-title-subtext">
                {itemText}
              </span>
            )
          })}
        </div>
      )}
    </div>
  )
}
