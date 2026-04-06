import { createContext, useContext, useState, useCallback } from 'react'

/**
 * ProgressContext — ARC-04: 学习进度持久化上下文
 *
 * 职责：管理模块/小节的阅读进度，持久化到 localStorage。
 * 与 sessionStorage 的记忆锚点（LessonViewer 断点续传）并存：
 *   - sessionStorage: 当前位置（section+slide 索引），标签页生命周期
 *   - localStorage: 完成度数据（哪些已读），跨会话持久
 */
const ProgressContext = createContext(null)

const STORAGE_KEY = 'h5-progress-v1'

function loadProgress() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : {}
  } catch {
    return {}
  }
}

function saveProgress(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch (e) {
    console.warn('[ProgressContext] localStorage 写入失败:', e)
  }
}

export function ProgressProvider({ children }) {
  const [progress, setProgress] = useState(loadProgress)

  // 标记小节已读
  const markRead = useCallback((courseId, scriptName, sectionId) => {
    setProgress(prev => {
      const key = `${courseId}/${scriptName}`
      const next = {
        ...prev,
        [key]: { ...(prev[key] || {}), [sectionId]: { read: true, ts: Date.now() } },
      }
      saveProgress(next)
      return next
    })
  }, [])

  // 查询单个小节是否已读
  const isRead = useCallback((courseId, scriptName, sectionId) => {
    const key = `${courseId}/${scriptName}`
    return !!(progress[key]?.[sectionId]?.read)
  }, [progress])

  // 查询模块完成度（接收该模块下所有 sectionId）
  const getModuleProgress = useCallback((courseId, scriptName, sectionIds) => {
    const key = `${courseId}/${scriptName}`
    const data = progress[key] || {}
    const completed = sectionIds.filter(id => data[id]?.read).length
    const total = sectionIds.length
    return { completed, total, ratio: total > 0 ? completed / total : 0 }
  }, [progress])

  return (
    <ProgressContext.Provider value={{ progress, markRead, isRead, getModuleProgress }}>
      {children}
    </ProgressContext.Provider>
  )
}

export function useProgress() {
  return useContext(ProgressContext)
}
