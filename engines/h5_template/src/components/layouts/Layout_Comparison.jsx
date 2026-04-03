/**
 * Layout_Comparison — 对比表布局
 * 左右两列对比
 */
export default function Layout_Comparison({ slide }) {
  // 尝试将 List 拆分为左右两组（按 "vs" 或 "/" 分隔）
  const items = slide.list || []

  return (
    <>
      {slide.heading && <div className="slide-heading">{slide.heading}</div>}
      <div className="slide-body">
        {slide.resolvedImage ? (
          <img className="slide-image" src={slide.resolvedImage} alt="" />
        ) : items.length > 0 ? (
          <div style={{
            display: 'flex',
            flex: 1,
            gap: '2px',
            padding: '12px',
          }}>
            {/* 渲染列表为两列 */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div style={{
                fontSize: '12px', fontWeight: 600, color: 'var(--theme-secondary)',
                padding: '4px 8px', textTransform: 'uppercase', letterSpacing: '0.5px'
              }}>
                ✓ 正面
              </div>
              {items.filter((_, i) => i % 2 === 0).map((item, i) => (
                <div key={i} style={{
                  padding: '8px 12px', background: 'rgba(var(--theme-secondaryRgb), 0.06)',
                  borderRadius: '6px', fontSize: '13px', lineHeight: 1.5,
                }}>
                  {item}
                </div>
              ))}
            </div>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div style={{
                fontSize: '12px', fontWeight: 600, color: 'var(--theme-primary)',
                padding: '4px 8px', textTransform: 'uppercase', letterSpacing: '0.5px'
              }}>
                ✗ 反面
              </div>
              {items.filter((_, i) => i % 2 === 1).map((item, i) => (
                <div key={i} style={{
                  padding: '8px 12px', background: 'rgba(var(--theme-primaryRgb), 0.06)',
                  borderRadius: '6px', fontSize: '13px', lineHeight: 1.5,
                }}>
                  {item}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="greybox">
            <span className="greybox-label">Comparison</span>
            <span className="greybox-text">{slide.scene || '等待对比数据'}</span>
          </div>
        )}
      </div>
    </>
  )
}
