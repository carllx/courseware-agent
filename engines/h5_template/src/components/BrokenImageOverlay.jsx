/**
 * BrokenImageOverlay — 断链幻灯片警示覆盖层
 *
 * 当 slide 声明了 assetExpected 但实际 image 为 null 时，
 * 在幻灯片上叠加斑马纹 + 缺失路径提示。
 */
import { useState } from 'react'
import '../styles/craft-room.css'

export default function BrokenImageOverlay({ expected }) {
  const [copied, setCopied] = useState(false)

  // 从 expected 中提取显示文本
  const displayPath = Array.isArray(expected)
    ? expected[0] || '未知路径'
    : expected || '未知路径'

  const handleCopy = (e) => {
    e.stopPropagation()
    navigator.clipboard.writeText(displayPath).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <div className="broken-image-overlay">
      <div className="broken-image-icon">🔗</div>
      <div className="broken-image-label">图片缺失</div>
      <div className="broken-image-path" title={displayPath}>
        {displayPath}
      </div>
      <button
        className="broken-image-copy"
        onClick={handleCopy}
        title="复制期望路径"
      >
        {copied ? '✔ 已复制' : '📋 复制路径'}
      </button>
    </div>
  )
}
