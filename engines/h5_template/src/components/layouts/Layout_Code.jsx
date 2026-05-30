import React from 'react';
import '../../styles/h5-layouts.css';

const Layout_Code = ({ slide, theme }) => {
  const { assetContent, assetType, heading } = slide;

  return (
    <div className="h5-layout-code" style={theme ? { '--theme-bgDark': theme.bgDark } : {}}>
      {heading && <div className="h5-slide-heading">{heading}</div>}
      <div className="h5-slide-body" style={{ padding: heading ? '0' : undefined }}>
        <div className="h5-code-terminal">
          <div className="h5-code-terminal-header">
            <div className="h5-code-terminal-dot h5-code-terminal-dot--red"></div>
            <div className="h5-code-terminal-dot h5-code-terminal-dot--yellow"></div>
            <div className="h5-code-terminal-dot h5-code-terminal-dot--green"></div>
            <div className="h5-code-terminal-lang">{assetType || 'text'}</div>
          </div>
          <pre className="h5-code-terminal-body">
            {assetContent}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default Layout_Code;
