/**
 * AnnotationOverlay — Agent 批注层（Phase 3, 修正 V4）
 *
 * 基于段落指纹的语义吸附，将 Agent 批注精确绑定到段落。
 * 指纹失效的批注聚合在 "orphaned" 区域，避免错位贴合。
 *
 * 数据来源：validate_runner.py 未来可通过 h5:annotations WS 推送，
 * 或从 JSON 中预加载静态批注。
 *
 * Props:
 *   annotations - 批注数组 [{ fingerprint, message, type, rule, textPreview }]
 *   paragraphs  - 当前 section 的段落数组
 */
import { useMemo, useState } from 'react'
import { buildFingerprintMap, attachAnnotations } from '../utils/fingerprint'
import '../styles/craft-room.css'

// 批注类型 → 视觉配色
const ANNOTATION_STYLES = {
  TONE_SHIFT: { icon: '🎭', color: '#ff6b6b', label: '语气转折' },
  DEPTH_GAP: { icon: '📐', color: '#ffa502', label: '深度不足' },
  DILUTION: { icon: '💧', color: '#70a1ff', label: '内容稀释' },
  FACTUAL: { icon: '📌', color: '#ff4757', label: '事实校验' },
  SUGGESTION: { icon: '💡', color: '#2ed573', label: '建议' },
  DEFAULT: { icon: '📝', color: '#a29bfe', label: '批注' },
}

export default function AnnotationOverlay({ annotations = [], paragraphs = [] }) {
  const [showOrphaned, setShowOrphaned] = useState(false)

  const result = useMemo(() => {
    if (!annotations.length || !paragraphs.length) {
      return { attached: [], orphaned: [] }
    }
    const fpMap = buildFingerprintMap(paragraphs)
    return attachAnnotations(annotations, fpMap)
  }, [annotations, paragraphs])

  if (!annotations.length) return null

  const { attached, orphaned } = result

  return (
    <div className="annotation-overlay">
      {/* 吸附成功的批注：按段落索引显示标记 */}
      {attached.length > 0 && (
        <div className="annotation-markers">
          {attached.map((anno, i) => {
            const style = ANNOTATION_STYLES[anno.type] || ANNOTATION_STYLES.DEFAULT
            return (
              <div
                key={i}
                className="annotation-marker"
                data-para-idx={anno.paragraphIdx}
                title={`${style.label}: ${anno.message}`}
                style={{ '--anno-color': style.color }}
              >
                <span className="annotation-marker-icon">{style.icon}</span>
                <span className="annotation-marker-text">{anno.message}</span>
                {anno.rule && (
                  <span className="annotation-marker-rule">{anno.rule}</span>
                )}
              </div>
            )
          })}
        </div>
      )}

      {/* 孤立批注区 */}
      {orphaned.length > 0 && (
        <div className="annotation-orphaned">
          <button
            className="annotation-orphaned-toggle"
            onClick={() => setShowOrphaned(!showOrphaned)}
          >
            ⚠️ {orphaned.length} 条批注已失效
            <span className="annotation-orphaned-arrow">
              {showOrphaned ? '▼' : '▶'}
            </span>
          </button>
          {showOrphaned && (
            <div className="annotation-orphaned-list">
              {orphaned.map((anno, i) => {
                const style = ANNOTATION_STYLES[anno.type] || ANNOTATION_STYLES.DEFAULT
                return (
                  <div key={i} className="annotation-orphaned-item">
                    <span>{style.icon}</span>
                    <div>
                      <div className="annotation-orphaned-msg">{anno.message}</div>
                      {anno.textPreview && (
                        <div className="annotation-orphaned-preview">
                          原文: "{anno.textPreview.slice(0, 40)}..."
                        </div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
