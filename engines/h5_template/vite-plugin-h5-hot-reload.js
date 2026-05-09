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

  // V-08 fix: 插件初始化时一次性解析 FFmpeg 路径，避免每次请求都做磁盘 IO
  const FFMPEG_CMD = fs.existsSync('/opt/homebrew/bin/ffmpeg') ? '/opt/homebrew/bin/ffmpeg' : 'ffmpeg'

  let server = null
  let workspaceRoot = null
  const pendingTimers = new Map()
  let isRebuilding = false  // 防止并发重建

  return {
    name: 'h5-hot-reload',

    handleHotUpdate({ file }) {
      // UX优化支柱 1：拦截底层 full-reload 刷新，实现无痕换药
      // 拦截 public/ 下所有由 Python 引擎重建的 JSON（含 courses/*.json 和 slides.json）
      if (file.endsWith('.json') && file.includes('/public/')) {
        return []
      }
      // 拦截 weeks/ 下直接修改的源 .md 变更
      if (file.endsWith('.md') && file.includes('/weeks/')) {
        return []
      }
    },

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

      // ============ TTS 段落音频本地持久化中间件 ============

      /**
       * POST /api/tts/save — 保存 TTS 段落音频到本地文件系统
       *
       * 二进制协议：前 4 字节为 JSON header 长度（大端），后续 header JSON + audio binary
       * 存储策略 (SSOT)：源文件保持豆包原始格式 (.aac)，格式压缩仅在 SSG 构建时执行。
       * 写入: {workspace}/{courseId}/weeks/{weekName}/tts/{fp}.aac
       * 更新: {workspace}/{courseId}/weeks/{weekName}/tts/manifest.json
       */
      viteServer.middlewares.use('/api/tts/save', async (req, res) => {
        if (req.method !== 'POST') {
          res.statusCode = 405
          res.end(JSON.stringify({ error: 'Method not allowed' }))
          return
        }

        try {
          const chunks = []
          for await (const chunk of req) chunks.push(chunk)
          const body = Buffer.concat(chunks)

          const headerLen = body.readUInt32BE(0)
          const headerJson = body.slice(4, 4 + headerLen).toString('utf-8')
          const meta = JSON.parse(headerJson)
          const audioBuffer = body.slice(4 + headerLen)

          const { courseId, weekName, fp, durationMs } = meta
          if (!courseId || !weekName || !fp || audioBuffer.length === 0) {
            res.statusCode = 400
            res.end(JSON.stringify({ error: '缺少必要字段' }))
            return
          }

          const ttsDir = path.join(workspaceRoot, courseId, 'weeks', weekName, 'tts')
          fs.mkdirSync(ttsDir, { recursive: true })

          // SSOT: 直接写入原始二进制，保持豆包输出的 AAC 格式
          const filePath = path.join(ttsDir, `${fp}.aac`)
          fs.writeFileSync(filePath, audioBuffer)

          // 更新 manifest.json
          const manifestPath = path.join(ttsDir, 'manifest.json')
          let manifest = { version: 1, courseId, weekName, segments: {} }
          if (fs.existsSync(manifestPath)) {
            try { manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8')) } catch {}
          }
          manifest.segments[fp] = {
            durationMs: durationMs || 0,
            size: audioBuffer.length,
            cachedAt: Date.now(),
          }
          fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2))

          console.log(`  \x1b[32m[tts:save]\x1b[0m 💾 ${courseId}/${weekName}/tts/${fp}.aac (${(audioBuffer.length / 1024).toFixed(1)}KB)`)

          res.statusCode = 200
          res.setHeader('Content-Type', 'application/json')
          res.end(JSON.stringify({ ok: true, path: filePath, size: audioBuffer.length }))
        } catch (err) {
          console.error(`  \x1b[31m[tts:save]\x1b[0m ❌ ${err.message}`)
          res.statusCode = 500
          res.end(JSON.stringify({ error: err.message }))
        }
      })

      /**
       * GET /api/tts/manifest?course=X&week=Y — 返回指定 week 的 TTS manifest
       */
      viteServer.middlewares.use('/api/tts/manifest', (req, res) => {
        if (req.method !== 'GET') { res.statusCode = 405; res.end(); return }

        const url = new URL(req.url, 'http://localhost')
        const courseId = url.searchParams.get('course')
        const weekName = url.searchParams.get('week')

        if (!courseId || !weekName) {
          res.statusCode = 400
          res.end(JSON.stringify({ error: '需要 course 和 week 参数' }))
          return
        }

        const manifestPath = path.join(workspaceRoot, courseId, 'weeks', weekName, 'tts', 'manifest.json')

        res.setHeader('Content-Type', 'application/json')
        if (fs.existsSync(manifestPath)) {
          try {
            const data = fs.readFileSync(manifestPath, 'utf-8')
            res.end(data)
          } catch {
            res.end(JSON.stringify({ version: 1, segments: {} }))
          }
        } else {
          res.end(JSON.stringify({ version: 1, segments: {} }))
        }
      })

      /**
       * GET /api/validate/trigger?course=X&week=Y — 尝试并立即执行 P1 验证管线并返回成功状态
       */
      viteServer.middlewares.use('/api/validate/trigger', (req, res) => {
        const url = new URL(req.url, 'http://localhost')
        const courseId = url.searchParams.get('course')
        const weekName = url.searchParams.get('week')

        if (!courseId || !weekName) {
          res.statusCode = 400
          res.end(JSON.stringify({ error: '需要 course 和 week 参数' }))
          return
        }

        // 异步运行管线，会自行通过 WebSocket 发送 h5:validation 事件
        runValidationPipeline(courseId, weekName)
        
        res.setHeader('Content-Type', 'application/json')
        res.end(JSON.stringify({ ok: true, message: '已经触发验证流水线，请等待 WebSocket 下发结果' }))
      })

      /**
       * 静态代理：/courses/{courseId}/weeks/{weekName}/tts/{fp}.{mp3|aac}
       * V-01 fix: 支持双后缀回退，mp3 优先，aac 兜底（兼容 1857 个已有 .aac 文件）
       */
      viteServer.middlewares.use((req, res, next) => {
        const ttsMatch = req.url?.match(/^\/courses\/([^/]+)\/weeks\/([^/]+)\/tts\/([^/]+)\.(mp3|aac)$/)
        if (!ttsMatch) return next()

        const [, courseId, weekName, baseName, requestedExt] = ttsMatch.map(decodeURIComponent)
        const ttsDir = path.join(workspaceRoot, courseId, 'weeks', weekName, 'tts')

        // 双后缀回退：优先请求的后缀，然后尝试另一个
        const candidates = requestedExt === 'mp3'
          ? [`${baseName}.mp3`, `${baseName}.aac`]
          : [`${baseName}.aac`, `${baseName}.mp3`]

        for (const candidate of candidates) {
          const filePath = path.join(ttsDir, candidate)
          if (fs.existsSync(filePath)) {
            const mimeType = candidate.endsWith('.mp3') ? 'audio/mpeg' : 'audio/aac'
            res.setHeader('Content-Type', mimeType)
            res.setHeader('Cache-Control', 'public, max-age=3600')
            fs.createReadStream(filePath).pipe(res)
            return
          }
        }

        res.statusCode = 404
        res.end()
      })

      console.log(`  \x1b[36m[h5-hot-reload]\x1b[0m 💾 TTS 本地持久化已启用 (SSOT: 原始 AAC 存储, SSG 构建时转码 MP3)`)
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

        // ===== P1 管线：异步验证（不阻塞 P0 渲染）=====
        runValidationPipeline(courseDir, weekName)
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

  /**
   * P1 管线：异步执行 validate_runner.py，通过 h5:validation 推送结果
   * 独立于 P0 渲染，不影响热重载响应速度
   */
  function runValidationPipeline(courseDir, weekName) {
    // 从 weekName 中提取周次编号 (W03_xxx → 3)
    const weekMatch = weekName.match(/^W(\d+)/)
    const weekArg = weekMatch ? ['--week', String(parseInt(weekMatch[1], 10))] : []

    const validatorScript = path.join(
      workspaceRoot, '.agent', 'skills', 'validation_suite', 'scripts', 'validate_runner.py'
    )

    if (!fs.existsSync(validatorScript)) {
      console.log(`  \x1b[33m[h5:validation]\x1b[0m ⚠️  validate_runner.py 未找到，跳过验证`)
      return
    }

    const validationStart = Date.now()
    console.log(`  \x1b[35m[h5:validation]\x1b[0m 🔍 启动 P1 验证...`)

    const vProc = spawn(PYTHON, [
      validatorScript,
      '--course', courseDir,
      '--skip-spec',  // 快速模式：跳过 spec 检查减少延迟
      ...weekArg,
    ], {
      cwd: workspaceRoot,
      stdio: ['ignore', 'pipe', 'pipe'],
    })

    let vStdout = '', vStderr = ''
    vProc.stdout.on('data', (d) => { vStdout += d.toString() })
    vProc.stderr.on('data', (d) => { vStderr += d.toString() })

    vProc.on('close', (vCode) => {
      const vElapsed = Date.now() - validationStart

      try {
        const result = JSON.parse(vStdout)
        console.log(`  \x1b[35m[h5:validation]\x1b[0m ✅ 完成 (${vElapsed}ms) gate=${result.gateLevel}`)

        server.ws.send({
          type: 'custom',
          event: 'h5:validation',
          data: { ...result, elapsed: vElapsed },
        })
      } catch (e) {
        console.error(`  \x1b[31m[h5:validation]\x1b[0m ❌ JSON 解析失败 (${vElapsed}ms)`)
        if (vStderr) console.error(`  ${vStderr.slice(0, 200)}`)
      }
    })

    vProc.on('error', (err) => {
      console.error(`  \x1b[31m[h5:validation]\x1b[0m ❌ 启动失败: ${err.message}`)
    })
  }
}
