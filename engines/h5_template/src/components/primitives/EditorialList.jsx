/**
 * EditorialList
 * A high-fidelity reusable primitive for rendering Academic Minimalist lists
 * Incorporates numbered markers or colored vertical bars to match PPTX aesthetics.
 */
export default function EditorialList({ 
  items, 
  variant = 'numbered', // 'numbered' or 'bars'
  customStyle = {} 
}) {
  if (!items || items.length === 0) return null;

  return (
    <ul className={`h5-editorial-list h5-editorial-list--${variant}`} style={customStyle}>
      {items.map((item, i) => {
        const itemTitle = typeof item === 'string' ? item : item.title;
        const itemDesc = typeof item === 'string' ? '' : (item.desc || '');

        return (
          <li key={i} className="h5-editorial-item">
            {variant === 'numbered' ? (
              <div className="h5-editorial-marker h5-editorial-marker--numbered"></div>
            ) : (
              <div className={`h5-editorial-marker h5-editorial-marker--bar h5-editorial-marker--color-${i % 3}`}></div>
            )}
            <div className="h5-editorial-content">
              <div className="h5-editorial-title">{itemTitle}</div>
              {itemDesc && <div className="h5-editorial-desc">{itemDesc}</div>}
            </div>
          </li>
        );
      })}
    </ul>
  );
}
