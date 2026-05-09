export default function AssetPlaceholder({ slide, proportion = '55%', customStyle = {} }) {
  const isBroken = !slide.resolvedImage;
  
  if (slide.resolvedImage) {
    const isVideo = slide.resolvedImage.match(/\.(mp4|webm|ogg)$/i);
    
    let vttZh, vttEn;
    if (isVideo) {
      vttZh = slide.resolvedImage.replace(/\.(mp4|webm|ogg)$/i, '.zh-Hant.vtt');
      vttEn = slide.resolvedImage.replace(/\.(mp4|webm|ogg)$/i, '.en.vtt');
    }

    return (
      <div className="h5-asset-box" style={{ flex: `0 0 ${proportion}`, ...customStyle }}>
        {isVideo ? (
          <video 
            className="slide-video-player"
            src={slide.resolvedImage} 
            controls 
            preload="metadata"
            style={{ width: '100%', height: '100%', objectFit: 'contain', outline: 'none', borderRadius: '4px' }}
          >
            <track kind="captions" src={vttZh} srcLang="zh-Hant" label="繁体中文" default />
            <track kind="captions" src={vttEn} srcLang="en" label="English" />
          </video>
        ) : (
          <img className="slide-image" src={slide.resolvedImage} alt={slide.heading || ''} />
        )}
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
