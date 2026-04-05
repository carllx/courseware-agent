export default function AssetPlaceholder({ slide, proportion = '55%', customStyle = {} }) {
  const isBroken = !slide.resolvedImage;
  
  if (slide.resolvedImage) {
    return (
      <div className="h5-asset-box" style={{ flex: `0 0 ${proportion}`, ...customStyle }}>
        <img className="slide-image" src={slide.resolvedImage} alt={slide.heading || ''} />
      </div>
    );
  }

  return (
    <div className="h5-asset-box h5-asset-box--placeholder" style={{ flex: `0 0 ${proportion}`, ...customStyle }}>
      <div className="h5-asset-placeholder-content">
        <span className="h5-asset-label">{slide.layout || 'Asset'} · 视觉</span>
        <span className="h5-asset-desc">{slide.scene || '等待视觉素材...'}</span>
        {slide.assetExpected && (
          <span className="h5-asset-path">📂 {slide.assetExpected}</span>
        )}
      </div>
    </div>
  );
}
