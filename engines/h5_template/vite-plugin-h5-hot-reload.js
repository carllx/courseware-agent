/**
 * vite-plugin-h5-hot-reload.js
 *
 * H5 逐字稿热重载插件 — 监听 Markdown 源文件变化，自动重建 JSON 并通知浏览器。
 *
 * 信息流：
 *   Ctrl+S (.md) → chokidar → debounce 500ms → Python --rebuild-week → 覆写 JSON
 *   → server.ws.send('h5:reload') → React re-fetch → UI 自动刷新
 *
 * 环境变量：
 *   H5_WATCH_MODE=fragment  使用片段模式（仅单模块，更快但丢失整周上下文）
 *   H5_PYTHON=/path/to/python  指定 Python 解释器路径
 *   H5_DEBOUNCE=800  自定义防抖时间（毫秒）
 */

import { spawn } from 'child_process'
import path from 'path'
import fs from 'fs'

export default function h5HotReload(options = {}) {
  const PYTHON = process.env.H5_PYTHON || options.python || '/opt/anaconda3/envs/mybase/bin/python'
  const DEBOUNCE_MS = parseInt(process.env.H5_DEBOUNCE, 10) || options.debounce || 500

  let server = null
  let workspaceRoot = null
  const pendingTimers = new Map()
  let isRebuilding = false  // 防止并发重建

  return {
    name: 'h5-hot-reload',

    configureServer(viteServer) {
      server = viteServer

      // 推算 workspace 根目录: build/h5_preview → ../../
      workspaceRoot = path.resolve(viteServer.config.root, '..', '..')

      // 发现所有课程目录（含 course.yaml 的子目录）
      const courseDirs = discoverCourseDirs(workspaceRoot)
      if (courseDirs.length === 0) {
        console.log('[h5-hot-reload] ⚠️  未发现课程目录，热重载已禁用')
        return
      }

      // 将每个课程的 weeks/ 目录加入 Vite 的 chokidar watcher
      for (const dir of courseDirs) {
        const weeksDir = path.join(dir, 'weeks')
        if (fs.existsSync(weeksDir)) {
          viteServer.watcher.add(weeksDir)
        }
      }

      // 监听变更事件
      viteServer.watcher.on('change', (filePath) => {
        if (!shouldHandle(filePath)) return

        // 防抖：连续保存时只触发最后一次
        if (pendingTimers.has(filePath)) {
          clearTimeout(pendingTimers.get(filePath))
        }
        pendingTimers.set(filePath, setTimeout(() => {
          pendingTimers.delete(filePath)
          handleFileChange(filePath)
        }, DEBOUNCE_MS))
      })

      // 启动日志
      console.log('')
      console.log(`  \x1b[36m[h5-hot-reload]\x1b[0m 🔌 已激活 — 监听 ${courseDirs.length} 门课程`)
      courseDirs.forEach(d => {
        console.log(`  \x1b[36m[h5-hot-reload]\x1b[0m    📂 ${path.basename(d)}`)
      })
      console.log(`  \x1b[36m[h5-hot-reload]\x1b[0m    防抖: ${DEBOUNCE_MS}ms | Python: ${path.basename(PYTHON)}`)
      console.log('')
    },
  }

  /**
   * 扫描 workspace 下所有含 course.yaml 的目录
   */
  function discoverCourseDirs(root) {
    try {
      return fs.readdirSync(root, { withFileTypes: true })
        .filter(d => d.isDirectory() && fs.existsSync(path.join(root, d.name, 'course.yaml')))
        .map(d => path.join(root, d.name))
    } catch {
      return []
    }
  }

  /**
   * 判断文件变更是否应触发热重载
   * 仅处理 <course>/weeks/<week>/src/*.md 的变更
   */
  function shouldHandle(filePath) {
    if (!filePath.endsWith('.md')) return false
    const rel = path.relative(workspaceRoot, filePath)
    // 匹配: <课程名>/weeks/<教学周>/src/<模块>.md
    return /^[^/]+\/weeks\/[^/]+\/src\/[^/]+\.md$/.test(rel)
  }

  /**
   * 处理文件变更：调用 Python 引擎重建，通过 WebSocket 通知前端
   */
  function handleFileChange(filePath) {
    if (isRebuilding) {
      console.log(`  \x1b[33m[h5-hot-reload]\x1b[0m ⏳ 上一次重建尚未完成，跳过`)
      return
    }

    const relToWorkspace = path.relative(workspaceRoot, filePath)
    const parts = relToWorkspace.split(path.sep)
    const courseDir = parts[0]
    const weekName = parts[2]  // e.g. W01_Visual_Perception
    const moduleName = path.basename(filePath, '.md')

    const mode = process.env.H5_WATCH_MODE || 'week'
    console.log(`  \x1b[36m[h5-hot-reload]\x1b[0m 🔬 ${courseDir}/${weekName}/${moduleName}`)

    let args
    if (mode === 'fragment') {
      args = [
        path.join(workspaceRoot, 'engines', 'generate_course_h5.py'),
        courseDir, '--fragment', filePath,
      ]
    } else {
      // 默认: 整周重建（生成 LessonViewer 兼容的完整教学周 JSON）
      args = [
        path.join(workspaceRoot, 'engines', 'generate_course_h5.py'),
        courseDir, '--rebuild-week', filePath,
      ]
    }

    isRebuilding = true
    const startTime = Date.now()

    const proc = spawn(PYTHON, args, {
      cwd: workspaceRoot,
      stdio: ['ignore', 'pipe', 'pipe'],
    })

    let stdout = '', stderr = ''
    proc.stdout.on('data', (d) => { stdout += d.toString() })
    proc.stderr.on('data', (d) => { stderr += d.toString() })

    proc.on('close', (code) => {
      isRebuilding = false
      const elapsed = Date.now() - startTime

      if (code === 0) {
        console.log(`  \x1b[32m[h5-hot-reload]\x1b[0m ✅ 完成 (${elapsed}ms)`)
        // 输出关键信息行
        stdout.split('\n')
          .filter(l => l.includes('📖') || l.includes('🗺️') || l.includes('🎉'))
          .forEach(l => console.log(`  \x1b[2m${l.trim()}\x1b[0m`))

        server.ws.send({
          type: 'custom',
          event: 'h5:reload',
          data: { courseDir, weekName, moduleName, mode, elapsed },
        })
      } else {
        const errorMsg = (stderr || stdout).slice(0, 500)
        console.error(`  \x1b[31m[h5-hot-reload]\x1b[0m ❌ 失败 (${elapsed}ms):`)
        console.error(`  ${errorMsg.split('\n').slice(0, 5).join('\n  ')}`)

        server.ws.send({
          type: 'custom',
          event: 'h5:error',
          data: { courseDir, moduleName, error: errorMsg },
        })
      }
    })

    proc.on('error', (err) => {
      isRebuilding = false
      console.error(`  \x1b[31m[h5-hot-reload]\x1b[0m ❌ Python 进程启动失败: ${err.message}`)
      server.ws.send({
        type: 'custom',
        event: 'h5:error',
        data: { courseDir, moduleName, error: `Python 进程启动失败: ${err.message}` },
      })
    })
  }
}
