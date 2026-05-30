import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
});

const MermaidRenderer = ({ chart, id }) => {
  const containerRef = useRef(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (chart && containerRef.current) {
      setError(false);
      const renderChart = async () => {
        try {
          // Clear previous
          containerRef.current.innerHTML = '';
          const { svg } = await mermaid.render(`mermaid-${id}`, chart);
          containerRef.current.innerHTML = svg;
        } catch (e) {
          console.error("Mermaid rendering failed", e);
          setError(true);
        }
      };
      renderChart();
    }
  }, [chart, id]);

  if (error) {
    return (
      <div className="h5-asset-box h5-asset-box--placeholder">
        <div className="h5-asset-placeholder-content">
          <span className="h5-asset-label">Mermaid Rendering Error</span>
        </div>
      </div>
    );
  }

  return (
    <div className="h5-mermaid-container" ref={containerRef}></div>
  );
};

export default MermaidRenderer;
