import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter, Routes, Route } from 'react-router-dom'
import { ValidationProvider } from './contexts/ValidationContext'
import Dashboard from './pages/Dashboard'
import CoursePage from './pages/CoursePage'
import LessonViewer from './pages/LessonViewer'
import './styles/tokens.css'
import './styles/layout.css'

/**
 * 主入口 — v2.0 统一 H5 预览平台
 *
 * 路由结构：
 *   /                        → Dashboard (全课程总览)
 *   /:courseId                → CoursePage (周次列表)
 *   /:courseId/:scriptName    → LessonViewer (单讲预览)
 */
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ValidationProvider>
      <HashRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/:courseId" element={<CoursePage />} />
          <Route path="/:courseId/:scriptName" element={<LessonViewer />} />
        </Routes>
      </HashRouter>
    </ValidationProvider>
  </React.StrictMode>,
)
