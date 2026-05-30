import AssetPlaceholder from '../primitives/AssetPlaceholder'

/**
 * Layout_Flow — 流程/时间线步进器布局
 *
 * 用纯 CSS 垂直步进器（Stepper）恢复 flow 布局的时序方向性，
 * 替代之前 flow → timeline → Layout_Diagram 的语义断裂路径。
 *
 * 渲染逻辑：
 *   1. heading → 顶部标题栏
 *   2. parsedList → 垂直步进器（节点 + 连接线 + 序号圆点）
 *   3. resolvedImage → 右侧辅助配图（如有）
 *   4. 无 list 时退化为图 + 文字描述
 */
export default function Layout_Flow({ slide }) {
  const hasList = slide.parsedList && slide.parsedList.length > 0
  const hasAsset = !!slide.resolvedImage || !!slide.assetContent

  // 无 list 时退化为简单的图文展示
  if (!hasList) {
    return (
      <>
        {(slide.text || slide.heading) && <div className="h5-slide-heading">{slide.text || slide.heading}</div>}
        <div className="h5-slide-body h5-layout-editorial-split h5-layout-editorial-split--reverse">
          <div className="h5-split-content">
            {(slide.scene) && (
              <p className="h5-split-scene">{slide.scene}</p>
            )}
          </div>
          <AssetPlaceholder
            slide={slide}
            proportion={slide.scene && !hasAsset ? '100%' : '55%'}
          />
        </div>
      </>
    )
  }

  return (
    <>
      {(slide.text || slide.heading) && <div className="h5-slide-heading">{slide.text || slide.heading}</div>}
      <div className={`h5-slide-body h5-layout-flow${hasAsset ? '' : ' h5-layout-flow--full'}`}>
        {/* 左侧：垂直步进器 */}
        <div className="h5-flow-stepper">
          {slide.parsedList.map((item, i) => {
            const itemTitle = typeof item === 'string' ? item : item.title
            const itemDesc = typeof item === 'string' ? '' : (item.desc || '')
            const isLast = i === slide.parsedList.length - 1

            return (
              <div key={i} className={`h5-flow-step${isLast ? ' h5-flow-step--last' : ''}`}>
                <div className="h5-flow-step-marker"></div>
                <div className="h5-flow-step-content">
                  <div className="h5-flow-step-title">{itemTitle}</div>
                  {itemDesc && <div className="h5-flow-step-desc">{itemDesc}</div>}
                </div>
              </div>
            )
          })}
        </div>

        {/* 右侧：辅助配图（如有） */}
        {hasImage && (
          <AssetPlaceholder slide={slide} proportion="35%" />
        )}
      </div>
    </>
  )
}
