/**
 * ValidationOverlay — 验证数据可视化覆盖层
 *
 * Phase 2 核心组件：将 ValidationContext 中的验证结果
 * 以紧凑的侧边抽屉形式呈现，内置心流保护的视觉反馈。
 *
 * 功能：
 * - 字数验证结果（模块级填充率热力图）
 * - 视觉断链列表（含 VSCode 直跳）
 * - 门控信息（gateLevel 2 时隐藏视觉检查）
 * - 心流保护淡化动画
 */
import { useState, useMemo } from 'react'
import { useValidation } from '../contexts/ValidationContext'
import '../styles/craft-room.css'

export default function ValidationOverlay() {
  const { validation, isInFlow, gateLevel } = useValidation()
  const [isOpen, setIsOpen] = useState(false)

  if (!validation) return null

  const { validators } = validation
  const lengthData = validators?.length
  const visualsData = validators?.visuals

  // 汇总统计
  const stats = useMemo(() => {
    if (!lengthData) return null
    const modules = lengthData.modules || []
    const underfilledCount = modules.filter(m => m.fillRatio != null && m.fillRatio < 0.8).length
    const draftCount = modules.filter(m => m.isDraft).length
    const tagDeficitCount = modules.filter(m => m.tagDeficit > 0).length
    const missingVisuals = visualsData?.summary?.missing || 0

    return { underfilledCount, draftCount, tagDeficitCount, missingVisuals, modules }
  }, [lengthData, visualsData])

  if (!stats) return null

  // 无问题时不显示
  const totalIssues = stats.underfilledCount + stats.draftCount + stats.missingVisuals
  if (totalIssues === 0 && !isOpen) return null

  return (
    <div
      className={`validation-overlay ${isOpen ? 'open' : 'collapsed'}`}
      style={{
        opacity: isInFlow ? 0.15 : 1,
        pointerEvents: isInFlow ? 'none' : 'auto',
        transition: 'opacity 300ms ease-in',
      }}
    >
      {/* 折叠态：仅显示问题计数 */}
      {!isOpen && (
        <button
          className="validation-toggle"
          onClick={() => setIsOpen(true)}
          title="展开验证详情"
        >
          <span className="validation-toggle-icon">🔍</span>
          <span className="validation-toggle-count">{totalIssues}</span>
        </button>
      )}

      {/* 展开态：验证详情面板 */}
      {isOpen && (
        <div className="validation-panel">
          <div className="validation-panel-header">
            <span>🔍 验证详情</span>
            <button
              className="validation-close"
              onClick={() => setIsOpen(false)}
            >×</button>
          </div>

          {/* 门控提示 */}
          {gateLevel >= 2 && (
            <div className="validation-gate-warning">
              ⚠️ 字数严重不足，视觉检查已折叠
            </div>
          )}

          {/* 字数验证 */}
          {lengthData && (
            <div className="validation-section">
              <div className="validation-section-title">📝 字数验证</div>
              {stats.modules.map((mod, i) => {
                if (mod.fillRatio == null) return null
                const percent = Math.round(mod.fillRatio * 100)
                const status = mod.fillRatio >= 1.0 ? 'ok' : mod.fillRatio >= 0.8 ? 'warn' : 'fail'
                return (
                  <div key={i} className={`validation-module-row ${status}`}>
                    <span className="validation-module-name" title={mod.module}>
                      {mod.module.length > 25 ? mod.module.slice(0, 23) + '..' : mod.module}
                    </span>
                    <div className="validation-mini-bar">
                      <div
                        className={`validation-mini-fill ${status}`}
                        style={{ width: `${Math.min(percent, 100)}%` }}
                      />
                    </div>
                    <span className={`validation-percent ${status}`}>{percent}%</span>
                  </div>
                )
              })}
              {stats.tagDeficitCount > 0 && (
                <div className="validation-hint">
                  🏷️ {stats.tagDeficitCount} 个模块标签密度不足
                </div>
              )}
            </div>
          )}

          {/* 视觉断链（门控 2 时折叠） */}
          {visualsData && gateLevel < 2 && (
            <div className="validation-section">
              <div className="validation-section-title">🔗 视觉素材</div>
              {visualsData.missing?.length > 0 ? (
                visualsData.missing.map((m, i) => (
                  <div key={i} className="validation-missing-row">
                    <span className="validation-slide-id">{m.slideId}</span>
                    <button
                      className="validation-jump"
                      onClick={() => {
                        // Antigravity 直跳到 VISUAL 块
                        if (m.file && m.line) {
                          // 推算绝对路径并跳转
                          const ideUri = `antigravity://file${m.file}:${m.line}`
                          window.open(ideUri, '_self')
                        }
                      }}
                      title={`${m.file}:L${m.line}`}
                    >📍</button>
                  </div>
                ))
              ) : (
                <div className="validation-ok">✅ 素材完整</div>
              )}
            </div>
          )}

          {/* 验证耗时 */}
          {validation.elapsed && (
            <div className="validation-footer">
              验证耗时 {validation.elapsed}ms · gate={gateLevel}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
