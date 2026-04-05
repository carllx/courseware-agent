/**
 * ValidationContext — H5 Craft-room 验证数据的单一事实来源
 *
 * 管理 h5:validation WebSocket 事件推送的验证结果。
 * 内置"心流保护期"（修正 V2 State Thrashing）：
 *   - 频繁收到 h5:reload 时标记 isInFlow=true
 *   - isInFlow 期间验证 UI 冻结+淡化，不干扰创作心流
 *   - 停止编辑 2 秒后渐入最新验证数据
 */
import { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react'

const ValidationContext = createContext(null)

const FLOW_TIMEOUT_MS = 2000  // 停止编辑后多久恢复验证 UI

export function ValidationProvider({ children }) {
  // 验证数据（h5:validation 事件 payload）
  const [validation, setValidation] = useState(null)
  // 心流保护状态
  const [isInFlow, setIsInFlow] = useState(false)
  // 内部缓冲：在心流期间缓存最新验证数据，退出心流后应用
  const pendingRef = useRef(null)
  const flowTimerRef = useRef(null)
  const reloadTimerRef = useRef(null)

  /**
   * 当收到 h5:reload 时调用 — 标记进入心流
   */
  const onReload = useCallback(() => {
    setIsInFlow(true)

    // 重置心流超时计时器
    if (reloadTimerRef.current) {
      clearTimeout(reloadTimerRef.current)
    }
    reloadTimerRef.current = setTimeout(() => {
      setIsInFlow(false)
      // 退出心流时，如果有待应用的验证数据，立即应用
      if (pendingRef.current) {
        setValidation(pendingRef.current)
        pendingRef.current = null
      }
    }, FLOW_TIMEOUT_MS)
  }, [])

  /**
   * 当收到 h5:validation 时调用 — 更新验证数据
   * 心流期间缓冲数据，退出后自动应用
   */
  const onValidation = useCallback((data) => {
    if (isInFlow) {
      // 心流中：缓冲数据，不立即更新 UI
      pendingRef.current = data
    } else {
      setValidation(data)
      pendingRef.current = null
    }
  }, [isInFlow])

  // 清理
  useEffect(() => {
    return () => {
      if (reloadTimerRef.current) clearTimeout(reloadTimerRef.current)
      if (flowTimerRef.current) clearTimeout(flowTimerRef.current)
    }
  }, [])

  const value = {
    validation,
    isInFlow,
    onReload,
    onValidation,
    gateLevel: validation?.gateLevel ?? 0,
  }

  return (
    <ValidationContext.Provider value={value}>
      {children}
    </ValidationContext.Provider>
  )
}

export function useValidation() {
  const ctx = useContext(ValidationContext)
  if (!ctx) {
    throw new Error('useValidation 必须在 ValidationProvider 内使用')
  }
  return ctx
}

export default ValidationContext
