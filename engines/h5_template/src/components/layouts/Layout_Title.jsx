/**
 * Layout_Title — 标题/总结/引言布局
 * 居中大标题 + 可选副文本
 */
export default function Layout_Title({ slide }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100%',
      padding: '24px 32px',
      textAlign: 'center',
      background: slide.resolvedImage ? 'none' : 'var(--theme-bgDark)',
      color: slide.resolvedImage ? 'var(--theme-text)' : 'var(--theme-bg)',
      position: 'relative',
    }}>
      {slide.resolvedImage && (
        <img
          src={slide.resolvedImage}
          alt=""
          style={{
            position: 'absolute', inset: 0,
            width: '100%', height: '100%',
            objectFit: 'cover', opacity: 0.3,
          }}
        />
      )}
      <h2 style={{
        fontFamily: 'var(--theme-fontTitleCn)',
        fontSize: '22px',
        fontWeight: 700,
        lineHeight: 1.4,
        position: 'relative',
        zIndex: 1,
      }}>
        {slide.heading || slide.scene || slide.id}
      </h2>
      {slide.list && slide.list.length > 0 && (
        <div style={{
          marginTop: '16px', position: 'relative', zIndex: 1,
          display: 'flex', flexDirection: 'column', gap: '6px', alignItems: 'center',
        }}>
          {slide.list.map((item, i) => (
            <span key={i} style={{
              fontSize: '14px',
              opacity: 0.8,
            }}>
              {item}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}
