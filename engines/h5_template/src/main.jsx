import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter, Routes, Route } from 'react-router-dom'
import { ValidationProvider } from './contexts/ValidationContext'
import { ProgressProvider } from './contexts/ProgressContext'
import Dashboard from './pages/Dashboard'
import CoursePage from './pages/CoursePage'
import LessonViewer from './pages/LessonViewer'
import './styles/tokens.css'
import './styles/layout.css'

/**
 * 主入口 — v2.1 统一 H5 预览平台
 *
 * 路由结构：
 *   /                        → Dashboard (全课程总览)
 *   /:courseId                → CoursePage (周次列表)
 *   /:courseId/:scriptName    → LessonViewer (单讲预览)
 *
 * ARC-04: ProgressProvider 提供跨会话学习进度持久化
 */
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ProgressProvider>
      <ValidationProvider>
        <HashRouter>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/:courseId" element={<CoursePage />} />
            <Route path="/:courseId/:scriptName" element={<LessonViewer />} />
          </Routes>
        </HashRouter>
      </ValidationProvider>
    </ProgressProvider>
  </React.StrictMode>,
)
