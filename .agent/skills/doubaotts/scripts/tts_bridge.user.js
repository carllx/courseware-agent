// ==UserScript==
// @name         H5 TTS 凭证 & 提取桥接器
// @namespace    http://tampermonkey.net/
// @version      2.0.0
// @description  将豆包 TTS 能力通过 postMessage 桥接到 H5 课件预览引擎
// @author       Kiro
// @match        https://www.doubao.com/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

/**
 * 工作原理:
 *
 *  [凭证模式]
 *    H5 通过 window.open() 打开 doubao.com → 本脚本自动推送凭证
 *
 *  [提取模式] ← 核心
 *    H5 发送 postMessage {type:'h5_tts_extract', fp, text, speaker}
 *    → 本脚本调用原版 userscript 的 window.ttsSingleChunk() 提取音频
 *    → 将 ArrayBuffer 通过 postMessage (Transferable) 回传 H5
 *    所有 TTS 操作在 doubao.com 域内完成，无跨域问题。
 *
 *  [心跳模式]
 *    H5 定期发送 ping → 本脚本回复 pong → 确认弹窗仍然活跃
 *
 * 安全策略:
 *   - 仅响应来自 localhost / 127.0.0.1 的请求
 *   - 不修改原版 userscript（仅调用其全局 API）
 */

(function () {
    'use strict';

    const ALLOWED_ORIGINS = [
        /^https?:\/\/localhost(:\d+)?$/,
        /^https?:\/\/127\.0\.0\.1(:\d+)?$/,
    ];

    function isAllowedOrigin(origin) {
        return ALLOWED_ORIGINS.some(re => re.test(origin));
    }

    // ============ 凭证提取（与原版 userscript 获取方式一致）============
    function extractCredentials() {
        let device_id = null;
        let web_id = null;

        try {
            const stored = localStorage.getItem('__tea_cache_tokens_497858');
            if (stored) {
                const tokens = JSON.parse(stored);
                device_id = tokens.user_unique_id || null;
                web_id = tokens.web_id || null;
            }
        } catch (e) { /* ignore */ }

        if (!device_id) {
            const match = document.cookie.match(/s_v_web_id=([^;]+)/);
            if (match) device_id = match[1].replace('verify_', '');
        }

        return {
            device_id: device_id || null,
            web_id: web_id || device_id || null,
        };
    }

    // ============ 等待原版 userscript 加载 ============
    function waitForUserscript(timeout = 15000) {
        return new Promise((resolve) => {
            if (typeof window.ttsSingleChunk === 'function' ||
                typeof window.tts === 'function') {
                resolve(true);
                return;
            }

            const start = Date.now();
            const timer = setInterval(() => {
                if (typeof window.ttsSingleChunk === 'function' ||
                    typeof window.tts === 'function') {
                    clearInterval(timer);
                    resolve(true);
                } else if (Date.now() - start > timeout) {
                    clearInterval(timer);
                    resolve(false);
                }
            }, 300);
        });
    }

    // ============ 核心消息处理 ============
    window.addEventListener('message', async (event) => {
        if (!isAllowedOrigin(event.origin)) return;

        const { type } = event.data || {};

        switch (type) {
            // -- 凭证请求 --
            case 'h5_tts_request_credentials': {
                const creds = extractCredentials();
                event.source.postMessage({
                    type: 'h5_tts_credentials',
                    ...creds,
                    hasUserscript: typeof window.ttsSingleChunk === 'function' || typeof window.tts === 'function',
                    timestamp: Date.now(),
                    source: 'doubao_bridge_v2',
                }, event.origin);
                break;
            }

            // -- TTS 提取请求 --
            case 'h5_tts_extract': {
                const { fp, text, speaker, requestId } = event.data;
                console.log(`🎤 [Bridge] 提取: ${fp} (${text?.length}字)`);

                // 检测可用的 TTS 函数
                // 优先级：ttsSingleChunk（直接返回 {blob}） > tts（返回 Blob）
                const hasSingleChunk = typeof window.ttsSingleChunk === 'function';
                const hasTts = typeof window.tts === 'function';

                if (!hasSingleChunk && !hasTts) {
                    console.error('  ❌ [Bridge] 原版 TTS userscript 未加载');
                    event.source.postMessage({
                        type: 'h5_tts_extract_result',
                        fp,
                        requestId,
                        success: false,
                        error: '原版 TTS userscript 未加载（window.tts 和 window.ttsSingleChunk 均不存在）',
                    }, event.origin);
                    break;
                }

                try {
                    let blob;

                    if (hasSingleChunk) {
                        // 路径 A：ttsSingleChunk 返回 {blob, text}
                        const result = await window.ttsSingleChunk(text, { speaker });
                        blob = result.blob;
                    } else {
                        // 路径 B：window.tts 返回 Blob（原版 userscript 的标准 API）
                        console.log('  📡 [Bridge] 使用 window.tts() 回退路径');
                        blob = await window.tts(text, { speaker });
                    }

                    if (!blob || !(blob instanceof Blob)) {
                        throw new Error('TTS 返回值不是有效的 Blob');
                    }

                    const arrayBuffer = await blob.arrayBuffer();

                    // 获取时长
                    let durationMs = 0;
                    try {
                        durationMs = await getAudioDurationLocal(blob);
                    } catch { /* ignore */ }

                    // 通过 Transferable 传输 ArrayBuffer（零拷贝）
                    event.source.postMessage({
                        type: 'h5_tts_extract_result',
                        fp,
                        requestId,
                        success: true,
                        audioBuffer: arrayBuffer,
                        mimeType: blob.type || 'audio/aac',
                        durationMs,
                    }, event.origin, [arrayBuffer]); // Transferable!

                    console.log(`  ✅ [Bridge] ${fp} 完成 (${arrayBuffer.byteLength} bytes)`);

                } catch (error) {
                    console.error(`  ❌ [Bridge] ${fp}: ${error.message}`);
                    event.source.postMessage({
                        type: 'h5_tts_extract_result',
                        fp,
                        requestId,
                        success: false,
                        error: error.message,
                    }, event.origin);
                }
                break;
            }

            // -- 心跳 --
            case 'h5_tts_ping': {
                event.source.postMessage({
                    type: 'h5_tts_pong',
                    hasUserscript: typeof window.ttsSingleChunk === 'function' || typeof window.tts === 'function',
                    timestamp: Date.now(),
                }, event.origin);
                break;
            }
        }
    });

    // ============ 主动推送凭证给 opener ============
    async function tryAutoSend() {
        if (!window.opener) return;

        await waitForUserscript();
        const creds = extractCredentials();
        if (!creds.device_id) return;

        // V-01 安全修复：使用白名单校验替代 '*' 通配符
        // 跨域场景下无法读取 opener.location.origin，
        // 但可以逐个尝试白名单中的 origin 推送
        const candidateOrigins = [
            'http://localhost:5173',   // Vite dev server 默认端口
            'http://localhost:5174',   // Vite 备用端口
            'http://localhost:3000',   // 其他常见开发端口
            'http://127.0.0.1:5173',
        ];

        const payload = {
            type: 'h5_tts_credentials',
            ...creds,
            hasUserscript: typeof window.ttsSingleChunk === 'function' || typeof window.tts === 'function',
            timestamp: Date.now(),
            source: 'doubao_bridge_v2',
        };

        // 向所有候选 origin 推送（只有实际匹配的 opener 会接收到）
        for (const origin of candidateOrigins) {
            try {
                window.opener.postMessage(payload, origin);
            } catch { /* origin 不匹配时会静默失败 */ }
        }

        console.log(`🔑 [Bridge] 凭证已推送到 opener (尝试 ${candidateOrigins.length} 个候选 origin)`);
        showBridgeNotice('✅ 已连接 H5 课件预览 — 请勿关闭此页面');
    }

    // ============ 音频时长获取（本地实现，不依赖原版） ============
    function getAudioDurationLocal(blob) {
        return new Promise((resolve) => {
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.addEventListener('loadedmetadata', () => {
                resolve(audio.duration * 1000);
                URL.revokeObjectURL(url);
            });
            audio.addEventListener('error', () => {
                resolve(0);
                URL.revokeObjectURL(url);
            });
        });
    }

    // ============ UI 提示 ============
    function showBridgeNotice(text) {
        // 移除旧提示
        const old = document.getElementById('tts-bridge-notice');
        if (old) old.remove();

        const notice = document.createElement('div');
        notice.id = 'tts-bridge-notice';
        notice.style.cssText = `
            position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
            background: linear-gradient(135deg, #4C8C64, #2d6b3f);
            color: white; padding: 10px 20px; border-radius: 10px;
            font-size: 13px; font-weight: 600; z-index: 999999;
            box-shadow: 0 6px 24px rgba(76, 140, 100, 0.35);
            animation: bridgeFadeIn 0.3s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        `;
        notice.textContent = text;
        document.body.appendChild(notice);

        if (!document.getElementById('tts-bridge-style')) {
            const style = document.createElement('style');
            style.id = 'tts-bridge-style';
            style.textContent = `
                @keyframes bridgeFadeIn {
                    from { opacity: 0; transform: translateX(-50%) translateY(-12px); }
                    to   { opacity: 1; transform: translateX(-50%) translateY(0); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // 启动
    setTimeout(tryAutoSend, 2000);
    console.log('🌉 [TTS Bridge v2.0] 已启动 — 凭证 + 提取中继');
})();
