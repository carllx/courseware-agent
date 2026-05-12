/**
 * TtsToolbar — TTS 提取 & 播放控制工具栏
 *
 * 功能:
 *   1. 一键连接豆包（自动弹窗获取凭证）
 *   2. 手动输入凭证（回退方案）
 *   3. 一键提取所有 missing 段落
 *   4. 提取进度条
 *   5. 全段连续播放按钮
 *   6. 段落状态统计
 */
import { useState, useCallback, useEffect } from 'react'
import { useTtsSegments } from '../contexts/TtsSegmentContext'
import { openDoubaoAndGetCredentials, isBridgeAlive, SPEAKERS, SPEAKER_GROUPS } from '../utils/doubao-tts'
import '../styles/tts-toolbar.css'

export default function TtsToolbar({ paragraphs = [], allSections = [] }) {
  const tts = useTtsSegments()
  const [showConfig, setShowConfig] = useState(false)
  const [showManual, setShowManual] = useState(false)
  const [deviceId, setDeviceId] = useState('')
  const [webId, setWebId] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [isExtractingAll, setIsExtractingAll] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [isMigrating, setIsMigrating] = useState(false)

  // 初始化凭证表单
  useEffect(() => {
    if (tts?.credentials) {
      setDeviceId(tts.credentials.device_id || '')
      setWebId(tts.credentials.web_id || '')
    }
  }, [tts?.credentials])

  // === 一键连接豆包 ===
  const handleAutoConnect = useCallback(async () => {
    if (!tts || isConnecting) return
    setIsConnecting(true)

    const creds = await openDoubaoAndGetCredentials((status) => {
      setFeedback(status)
    })

    if (creds) {
      // 拿到凭证后自动测试并保存
      setFeedback('⏳ 测试 WebSocket 连接...')
      const valid = await tts.configureCredentials({
        device_id: creds.device_id,
        web_id: creds.web_id,
        speaker: tts?.credentials?.speaker,
      })

      if (valid) {
        setFeedback('✅ 连接成功！豆包 TTS 已就绪')
        setShowConfig(false)
      } else {
        setFeedback('⚠️ 凭证已保存，但 WebSocket 测试未通过')
      }
    }

    setIsConnecting(false)
    setTimeout(() => setFeedback(null), 4000)
  }, [tts, isConnecting])

  // === 手动保存凭证 ===
  const handleSaveConfig = useCallback(async () => {
    if (!tts || !deviceId.trim()) return

    setFeedback('⏳ 测试连接...')
    const valid = await tts.configureCredentials({
      device_id: deviceId.trim(),
      web_id: webId.trim() || deviceId.trim(),
      speaker: tts?.credentials?.speaker,
    })

    if (valid) {
      setFeedback('✅ 连接成功！')
      setShowConfig(false)
      setShowManual(false)
    } else {
      setFeedback('❌ 连接失败，请检查凭证')
    }
    setTimeout(() => setFeedback(null), 3000)
  }, [tts, deviceId, webId])

  // === 一键提取所有 ===
  const handleExtractAll = useCallback(async () => {
    if (!tts || isExtractingAll) return

    if (!tts.credentials) {
      setShowConfig(true)
      return
    }

    setIsExtractingAll(true)
    const result = await tts.extractAll(paragraphs)
    setIsExtractingAll(false)

    if (result) {
      setFeedback(`✅ 完成: ${result.success} 成功, ${result.failed} 失败`)
      setTimeout(() => setFeedback(null), 4000)
    }
  }, [tts, paragraphs, isExtractingAll])

  // === 一键补齐全周 ===
  const handleExtractWeek = useCallback(async () => {
    if (!tts || isExtractingAll) return

    if (!tts.credentials) {
      setShowConfig(true)
      return
    }

    setIsExtractingAll(true)
    const result = await tts.extractWeek(allSections)
    setIsExtractingAll(false)

    if (result) {
      setFeedback(`✅ 全周完成: ${result.success} 成功, ${result.failed} 失败`)
      // 刷新当前 section 状态
      tts.computeStatus(paragraphs)
      setTimeout(() => setFeedback(null), 5000)
    }
  }, [tts, allSections, paragraphs, isExtractingAll])

  // === 完整播放 ===
  const handlePlayAll = useCallback(async () => {
    if (!tts) return
    const ok = await tts.playAll(paragraphs)
    if (!ok) {
      setFeedback('⚠️ 部分段落未提取，请先完成提取')
      setTimeout(() => setFeedback(null), 3000)
    }
  }, [tts, paragraphs])

  if (!tts) return null

  const stats = tts.getStats()
  const weekStats = tts.getWeekStats(allSections)
  const hasCredentials = !!tts.credentials
  const bridgeActive = isBridgeAlive()
  const canExtract = hasCredentials && bridgeActive
  const allReady = stats.total > 0 && stats.ready === stats.total
  const progress = tts.extractProgress
  // 全周统计：排除当前模块的 missing，计算其他模块的缺口
  const weekMissingOther = Math.max(0, weekStats.missing - stats.missing)

  return (
    <div className="tts-toolbar">
      {/* 统计 */}
      <div className="tts-stats">
        {stats.ready > 0 && (
          <span className="tts-stat ready" title="当前模块已缓存">🔊 {stats.ready}</span>
        )}
        {stats.missing > 0 && (
          <span className="tts-stat missing" title="当前模块待提取">○ {stats.missing}</span>
        )}
        {stats.extracting > 0 && (
          <span className="tts-stat extracting" title="提取中">⟳ {stats.extracting}</span>
        )}
        {stats.error > 0 && (
          <span className="tts-stat error" title="失败">✕ {stats.error}</span>
        )}
        {weekStats.total > 0 && weekMissingOther > 0 && (
          <>
            <span className="tts-stat-sep">│</span>
            <span className="tts-stat week-missing" title={`全周其他模块还缺 ${weekMissingOther} 段 TTS`}>📦 全周 ○ {weekStats.missing}</span>
          </>
        )}
        {weekStats.total > 0 && weekStats.missing === 0 && (
          <>
            <span className="tts-stat-sep">│</span>
            <span className="tts-stat week-complete" title="全周 TTS 已完整">✅ 全周完整</span>
          </>
        )}
      </div>

      {/* 操作按钮 */}
      <div className="tts-actions">
        {/* 凭证状态指示 */}
        <button
          className={`tts-action-btn config ${canExtract ? 'connected' : hasCredentials ? 'stale' : ''}`}
          onClick={() => setShowConfig(!showConfig)}
          title={canExtract ? `已连接: ${tts.credentials.device_id?.slice(0, 8)}...` : hasCredentials ? '弹窗已关闭，点击重连' : '连接豆包 TTS'}
        >
          {canExtract ? '🟢' : hasCredentials ? '🟡' : '⚙️'}
        </button>

        {/* 补齐当前模块缺口 */}
        {stats.missing > 0 && canExtract && (
          <button
            className="tts-action-btn extract"
            onClick={handleExtractAll}
            disabled={isExtractingAll}
          >
            {isExtractingAll ? '⟳ 补齐中...' : `🎬 本模块 ${stats.missing} 处`}
          </button>
        )}

        {/* 补齐全周缺口 */}
        {weekStats.missing > 0 && canExtract && !isExtractingAll && (
          <button
            className="tts-action-btn extract week-extract"
            onClick={handleExtractWeek}
            title={`补齐全周所有模块的 ${weekStats.missing} 处 TTS 缺口`}
          >
            📦 全周 {weekStats.missing} 处
          </button>
        )}

        {/* 完整播放 */}
        {allReady && (
          <button
            className="tts-action-btn play-all"
            onClick={handlePlayAll}
            title="播放所有段落"
          >
            ▶ 全部播放
          </button>
        )}

        {/* 停止 */}
        {stats.playing > 0 && (
          <button
            className="tts-action-btn stop"
            onClick={() => tts.stopPlayback()}
          >
            ⏹
          </button>
        )}
      </div>

      {/* 提取进度 */}
      {progress && (
        <div className="tts-progress">
          <span className="tts-progress-text">
            {progress.current}/{progress.total}: {progress.text}
          </span>
          <div className="tts-progress-bar">
            <div
              className="tts-progress-fill"
              style={{ width: `${Math.round(progress.current / progress.total * 100)}%` }}
            />
          </div>
        </div>
      )}

      {/* 凭证配置面板 */}
      {showConfig && (
        <div className="tts-config-panel">
          <div className="tts-config-title">
            豆包 TTS 连接
            <button className="tts-config-close" onClick={() => { setShowConfig(false); setShowManual(false) }}>✕</button>
          </div>

          {/* 一键连接按钮 */}
          <button
            className="tts-action-btn extract tts-connect-btn"
            onClick={handleAutoConnect}
            disabled={isConnecting}
            style={{ width: '100%', padding: '10px', fontSize: '0.8rem' }}
          >
            {isConnecting ? '⏳ 连接中...' : '🔗 一键连接豆包'}
          </button>

          <div className="tts-config-hint">
            点击上方按钮自动打开豆包页面并获取凭证。<br/>
            需要安装 <strong>TTS 桥接脚本</strong> (tts_bridge.user.js)。
          </div>

          {/* 全局音色选择设置 */}
          {tts.credentials && (
            <div className="tts-manual-section" style={{ marginTop: '4px', marginBottom: '12px' }}>
              <div style={{ 
                fontSize: '0.7rem', 
                color: 'var(--theme-textSecondary, #6B635C)', 
                marginBottom: '6px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                fontWeight: '500'
              }}>
                🗣️ 当前音色角色
              </div>
              <select
                className="tts-config-input"
                style={{ 
                  padding: '6px 8px', 
                  appearance: 'auto', 
                  backgroundColor: 'white',
                  fontFamily: 'inherit',
                  cursor: 'pointer',
                  fontWeight: '500',
                  color: 'var(--theme-text, #2D2926)'
                }}
                value={Object.keys(SPEAKERS).find(name => SPEAKERS[name] === tts.credentials.speaker) || '温柔桃子'}
                onChange={(e) => {
                  const newSpeakerName = e.target.value;
                  const newSpeakerCode = SPEAKERS[newSpeakerName];
                  if (newSpeakerCode && newSpeakerCode !== tts.credentials.speaker) {
                    tts.configureCredentials({
                      ...tts.credentials,
                      speaker: newSpeakerCode,
                    });
                    setFeedback(`✅ 音色已切换为【${newSpeakerName}】(旧音频需手动删除后重新提取)`);
                    setTimeout(() => setFeedback(null), 4000);
                  }
                }}
              >
                {Object.entries(SPEAKER_GROUPS).map(([groupName, names]) => (
                  <optgroup key={groupName} label={groupName}>
                    {names.map((name) => (
                      <option key={name} value={name}>{name}</option>
                    ))}
                  </optgroup>
                ))}
              </select>
            </div>
          )}

          {/* 手动输入回退 */}
          <button
            className="tts-manual-toggle"
            onClick={() => setShowManual(!showManual)}
          >
            {showManual ? '▲ 收起手动输入' : '▼ 手动输入凭证'}
          </button>

          {showManual && (
            <div className="tts-manual-section">
              <div className="tts-config-hint">
                在 doubao.com 控制台输入:<br/>
                <code>JSON.parse(localStorage.getItem('__tea_cache_tokens_497858'))</code>
              </div>
              <input
                className="tts-config-input"
                placeholder="device_id (user_unique_id)"
                value={deviceId}
                onChange={e => setDeviceId(e.target.value)}
              />
              <input
                className="tts-config-input"
                placeholder="web_id (可留空)"
                value={webId}
                onChange={e => setWebId(e.target.value)}
              />
              <button
                className="tts-action-btn extract"
                onClick={handleSaveConfig}
                style={{ width: '100%', marginTop: '4px' }}
              >
                🔌 测试并保存
              </button>
            </div>
          )}

          {/* 已连接时显示断开按钮 */}
          {tts.credentials && (
            <button
              className="tts-action-btn config tts-disconnect-btn"
              onClick={() => { tts.clearCredentials(); setDeviceId(''); setWebId('') }}
              style={{ width: '100%', marginTop: '8px', fontSize: '0.65rem' }}
            >
              断开连接 ({tts.credentials.device_id?.slice(0, 12)}...)
            </button>
          )}

          {/* IndexedDB → 本地文件系统迁移 */}
          <button
            className="tts-action-btn extract"
            onClick={async () => {
              if (isMigrating) return
              if (!tts.migrateFromIndexedDB) {
                setFeedback('⚠️ 上下文未更新，请强刷新(Cmd+Shift+R)或重启。')
                return
              }
              setIsMigrating(true)
              setFeedback('⏳ 正在迁移 IndexedDB 缓存到本地...')
              const result = await tts.migrateFromIndexedDB((p) => {
                setFeedback(`⏳ 迁移 ${p.current}/${p.total}: ${p.fp}`)
              })
              setIsMigrating(false)
              if (result.migrated > 0) {
                setFeedback(`✅ 迁移完成: ${result.migrated} 个音频已保存到本地`)
                // 重新计算状态
                tts.computeStatus(paragraphs)
              } else {
                setFeedback('ℹ️ 无需迁移（IndexedDB 为空）')
              }
              setTimeout(() => setFeedback(null), 5000)
            }}
            disabled={isMigrating}
            style={{ width: '100%', marginTop: '8px', fontSize: '0.65rem', border: '1px solid #10b981', color: '#10b981' }}
          >
            {isMigrating ? '⏳ 迁移中...' : '📦 导出 IndexedDB → 本地文件'}
          </button>
        </div>
      )}

      {/* 反馈 */}
      {feedback && (
        <div className="tts-feedback">{feedback}</div>
      )}
    </div>
  )
}
