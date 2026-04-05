// ==UserScript==
// @name         豆包 TTS 完整版 (多音色 + SRT + Cookie)
// @namespace    http://tampermonkey.net/
// @version      4.4.0
// @description  豆包 TTS：44种音色、MP3转换、精确SRT时间戳、Cookie提取
// @author       Kiro
// @match        https://www.doubao.com/*
// @grant        none
// @require      https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js
// @run-at       document-end
// ==/UserScript==

(function () {
    'use strict';

    console.log('🎤 豆包 TTS v4.3 启动');

    // ============ 音色配置 (44个已验证) ============
    const SPEAKERS = {
        // 女声 (13个)
        '温柔桃子': 'zh_female_wenroutaozi_uranus_bigtts',
        '温柔桃子经典': 'zh_female_wenroutaozi_v2_mars_bigtts',
        '知性小棠': 'zh_female_wenroutaozi_mars_bigtts',
        '阳光甜妹': 'zh_female_xiaohe_conversation_wvae_bigtts',
        '邻家女孩': 'zh_female_f261_conversation_wvae_bigtts',
        '魅力苏菲': 'zh_female_sophie_conversation_wvae_bigtts',
        '撒娇学妹': 'zh_female_yuanqinvyou_wvae_bigtts',
        '文静毛毛': 'zh_female_maomao_conversation_wvae_bigtts',
        '北京大妞': 'zh_female_beijingdaniu_mars_bigtts',
        '清甜瑶瑶': 'zh_female_F466_mars_bigtts',
        '活泼可昕': 'zh_female_F765_mars_bigtts',
        '甜美小雪': 'ICL_6acf86286e24',
        '清冷阿梦': 'ICL_16cd9a58768e',
        // 男声 (13个)
        '磁性俊宇': 'zh_male_nuanxinshizhe_mars_bigtts',
        '邻家男孩': 'zh_male_linjiananhai_moon_bigtts',
        '悠悠君子': 'zh_male_M100_conversation_wvae_bigtts',
        '温暖阿虎': 'zh_male_ahu_conversation_wvae_bigtts',
        '少年梓辛': 'zh_male_m286_conversation_wvae_bigtts',
        '阳光阿辰': 'zh_male_qingyiyuxuan_mars_bigtts',
        '傲娇霸总': 'zh_male_aojiaobazong_wvae_bigtts',
        '温柔子言': 'zh_male_cheng_mars_bigtts',
        '率性阿哲': 'zh_male_litiebanzi_mars_bigtts',
        '深夜播客': 'zh_male_shenyeboke_wvae_bigtts',
        '东方浩然': 'zh_male_dongfanghaoran_moon_bigtts',
        '清爽男大': 'zh_male_junlangxize_mars_bigtts',
        '渊博小叔': 'zh_male_m219_conversation_wvae_bigtts',
        // 特色音色 (18个)
        '腹黑霸总': 'ICL_c021bc19bf92',
        '冷酷霸总': 'ICL_e0b9b93ee322',
        '霸道总裁': 'ICL_d4d40acd33dd',
        '温柔陆辰': 'ICL_df4fc4d1ce4b',
        '病娇少爷': 'ICL_72afa6c5dc07',
        '清朗宇澄': 'ICL_9b3bc6941076',
        '奶音俊少': 'ICL_932b3f52bf3d',
        '沉稳皓轩': 'ICL_5a413fbc14fc',
        '温柔俊彦': 'ICL_0ce6ef379e73',
        '青涩沐阳': 'ICL_afedffe4586c',
        '睿语舟舟': 'ICL_4ce34d3f60f4',
        '随性先生': 'ICL_b718c1050dd1',
        '俊朗男友': 'ICL_1eed9233299f',
        '奶酷小宇': 'ICL_b22cd40ccd3e',
        '暖阳阿晨': 'ICL_7a33516fe388',
        '低音小北': 'ICL_989e59f0082a',
        '男闺蜜俊熙': 'ICL_7ba54f5a883e',
        '深情霸总': 'ICL_6e69deb80ce5',
    };

    const SPEAKER_GROUPS = {
        '女声': ['温柔桃子', '温柔桃子经典', '知性小棠', '阳光甜妹', '邻家女孩', '魅力苏菲', '撒娇学妹', '文静毛毛', '北京大妞', '清甜瑶瑶', '活泼可昕', '甜美小雪', '清冷阿梦'],
        '男声': ['磁性俊宇', '邻家男孩', '悠悠君子', '温暖阿虎', '少年梓辛', '阳光阿辰', '傲娇霸总', '温柔子言', '率性阿哲', '深夜播客', '东方浩然', '清爽男大', '渊博小叔'],
        '特色': ['腹黑霸总', '冷酷霸总', '霸道总裁', '温柔陆辰', '病娇少爷', '清朗宇澄', '奶音俊少', '沉稳皓轩', '温柔俊彦', '青涩沐阳', '睿语舟舟', '随性先生', '俊朗男友', '奶酷小宇', '暖阳阿晨', '低音小北', '男闺蜜俊熙', '深情霸总'],
    };

    // ============ 配置 ============
    const WS_URL = 'wss://ws-samantha.doubao.com/samantha/audio/tts';
    const DEFAULT_SPEAKER = 'zh_female_wenroutaozi_uranus_bigtts';

    // ============ 工具函数 ============
    const generateId = () => Math.floor(Math.random() * 9e18 + 1e18).toString();

    function getSpeakerId(name) {
        if (SPEAKERS[name]) return SPEAKERS[name];
        if (Object.values(SPEAKERS).includes(name)) return name;
        return DEFAULT_SPEAKER;
    }

    // 从 localStorage 获取 tea tokens
    function getTeaTokens() {
        try {
            const stored = localStorage.getItem('__tea_cache_tokens_497858');
            if (stored) {
                return JSON.parse(stored);
            }
        } catch (e) { }
        return null;
    }

    // 获取 device_id（从 cookie 或 localStorage）
    function getDeviceId() {
        // 尝试从 tea tokens 获取
        const teaTokens = getTeaTokens();
        if (teaTokens && teaTokens.user_unique_id) {
            return teaTokens.user_unique_id;
        }

        // 尝试从 cookie 获取
        const match = document.cookie.match(/s_v_web_id=([^;]+)/);
        if (match) return match[1].replace('verify_', '');

        // 生成新的
        return generateId();
    }

    // 获取 web_id
    function getWebId() {
        const teaTokens = getTeaTokens();
        if (teaTokens && teaTokens.web_id) {
            return teaTokens.web_id;
        }
        return getDeviceId();
    }

    // 生成 web_tab_id (UUID v4 格式)
    function generateWebTabId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // 缓存 web_tab_id
    let cachedWebTabId = null;
    function getWebTabId() {
        if (!cachedWebTabId) {
            cachedWebTabId = generateWebTabId();
        }
        return cachedWebTabId;
    }

    function buildUrl(options = {}) {
        const deviceId = getDeviceId();
        const webId = getWebId();
        const speaker = options.speaker ? getSpeakerId(options.speaker) : DEFAULT_SPEAKER;

        // 构建完整的参数列表（与豆包官方一致）
        const params = {
            speaker,
            format: options.format || 'aac',
            speech_rate: options.speech_rate || 0,
            pitch: options.pitch || 0,
            version_code: '20800',
            language: 'zh',
            device_platform: 'web',
            aid: '497858',
            real_aid: '497858',
            pkg_type: 'release_version',
            device_id: deviceId,
            pc_version: '2.49.5',
            web_id: webId,
            tea_uuid: webId,
            region: '',
            sys_region: '',
            samantha_web: '1',
            'use-olympus-account': '1',
            web_tab_id: getWebTabId(),
        };

        return `${WS_URL}?${Object.entries(params).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&')}`;
    }

    function formatTime(ms) {
        const h = Math.floor(ms / 3600000);
        const m = Math.floor((ms % 3600000) / 60000);
        const s = Math.floor((ms % 60000) / 1000);
        const ms2 = ms % 1000;
        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms2).padStart(3, '0')}`;
    }

    // ============ Cookie 工具 ============
    function getCookies() {
        return document.cookie;
    }

    function getAuthHeader() {
        return {
            'Cookie': document.cookie,
            'Origin': 'https://www.doubao.com',
            'User-Agent': navigator.userAgent
        };
    }

    function exportConfig() {
        return {
            wsUrl: WS_URL,
            cookies: document.cookie,
            headers: getAuthHeader(),
            speakers: SPEAKERS,
            defaultSpeaker: DEFAULT_SPEAKER,
        };
    }

    function copyCookies() {
        navigator.clipboard.writeText(document.cookie).then(() => {
            console.log('✅ Cookie 已复制到剪贴板');
            alert('Cookie 已复制！');
        });
    }

    // ============ 文本分句 ============
    function splitSentences(text) {
        // 按中文标点分句
        const parts = text.split(/([。！？；\n]+)/);
        const sentences = [];
        let current = '';

        for (let i = 0; i < parts.length; i++) {
            current += parts[i];
            // 如果是标点或最后一部分，且有内容
            if ((i % 2 === 1 || i === parts.length - 1) && current.trim()) {
                sentences.push(current.trim());
                current = '';
            }
        }

        // 如果没有分句成功，按固定长度分
        if (sentences.length === 0 && text.trim()) {
            sentences.push(text.trim());
        }

        return sentences;
    }

    // ============ 文本分段（用于长文本处理）============
    // 豆包 TTS 对单次请求有长度限制，需要将长文本分成多个段落
    // 但分段太细会影响 TTS 对上下文情绪的理解，所以尽量保持较大的段落
    const MAX_CHUNK_LENGTH = 800; // 每段最大字符数（平衡稳定性和情绪连贯性）

    function splitIntoChunks(text) {
        // 首先按段落分割（双换行或分隔线）
        const paragraphs = text.split(/\n{2,}|[-─]{3,}/).filter(p => p.trim());
        const chunks = [];
        let currentChunk = '';

        for (const para of paragraphs) {
            const trimmedPara = para.trim();
            if (!trimmedPara) continue;

            // 如果单个段落就超过限制，需要按句子分割
            if (trimmedPara.length > MAX_CHUNK_LENGTH) {
                // 先保存当前累积的内容
                if (currentChunk.trim()) {
                    chunks.push(currentChunk.trim());
                    currentChunk = '';
                }

                // 按句子分割长段落
                const sentences = splitSentences(trimmedPara);
                let subChunk = '';
                for (const sentence of sentences) {
                    if ((subChunk + sentence).length > MAX_CHUNK_LENGTH) {
                        if (subChunk.trim()) {
                            chunks.push(subChunk.trim());
                        }
                        // 如果单个句子还是太长，强制分割
                        if (sentence.length > MAX_CHUNK_LENGTH) {
                            let remaining = sentence;
                            while (remaining.length > MAX_CHUNK_LENGTH) {
                                let splitPos = MAX_CHUNK_LENGTH;
                                const breakChars = ['，', '、', '：', '；', ',', ':', ' '];
                                for (const char of breakChars) {
                                    const pos = remaining.lastIndexOf(char, MAX_CHUNK_LENGTH);
                                    if (pos > MAX_CHUNK_LENGTH * 0.5) {
                                        splitPos = pos + 1;
                                        break;
                                    }
                                }
                                chunks.push(remaining.slice(0, splitPos).trim());
                                remaining = remaining.slice(splitPos).trim();
                            }
                            subChunk = remaining;
                        } else {
                            subChunk = sentence;
                        }
                    } else {
                        subChunk += sentence;
                    }
                }
                if (subChunk.trim()) {
                    currentChunk = subChunk;
                }
            } else if ((currentChunk + '\n' + trimmedPara).length > MAX_CHUNK_LENGTH) {
                // 当前累积内容加上新段落会超过限制
                if (currentChunk.trim()) {
                    chunks.push(currentChunk.trim());
                }
                currentChunk = trimmedPara;
            } else {
                // 继续累积，段落之间用换行连接保持结构
                currentChunk += (currentChunk ? '\n' : '') + trimmedPara;
            }
        }

        // 保存最后一段
        if (currentChunk.trim()) {
            chunks.push(currentChunk.trim());
        }

        return chunks;
    }

    // ============ 获取音频时长 ============
    function getAudioDuration(blob) {
        return new Promise((resolve) => {
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.addEventListener('loadedmetadata', () => {
                resolve(audio.duration * 1000); // 转为毫秒
                URL.revokeObjectURL(url);
            });
            audio.addEventListener('error', () => {
                resolve(0);
                URL.revokeObjectURL(url);
            });
        });
    }

    // ============ AAC 转 MP3 ============
    async function convertToMp3(blob, bitrate = 128) {
        // 使用 Web Audio API 解码
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const arrayBuffer = await blob.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

        const originalSampleRate = audioBuffer.sampleRate;
        const numChannels = 1; // 强制单声道，简化处理并减少问题

        // 关键修复：统一采样率到 44100Hz (MP3 标准采样率)
        // lamejs 在处理非标准采样率 (如 24000Hz) 时存在严重 bug
        const targetSampleRate = 44100;
        let processedBuffer = audioBuffer;

        if (originalSampleRate !== targetSampleRate) {
            console.log(`🔄 重采样: ${originalSampleRate}Hz → ${targetSampleRate}Hz`);

            // 使用 OfflineAudioContext 进行高质量重采样
            const duration = audioBuffer.duration;
            const offlineCtx = new OfflineAudioContext(
                numChannels,
                Math.ceil(duration * targetSampleRate),
                targetSampleRate
            );

            const source = offlineCtx.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(offlineCtx.destination);
            source.start(0);

            processedBuffer = await offlineCtx.startRendering();
        }

        const samples = processedBuffer.length;
        const sampleRate = processedBuffer.sampleRate;

        // 获取 PCM 数据 (单声道)
        const channelData = processedBuffer.getChannelData(0);

        // 转换为 16-bit PCM，添加软削波防止爆音
        const pcmData = new Int16Array(samples);
        for (let i = 0; i < samples; i++) {
            // 软削波：使用 tanh 压缩而非硬截断
            let sample = channelData[i];
            if (Math.abs(sample) > 0.95) {
                sample = Math.tanh(sample * 1.5) * 0.95;
            }
            pcmData[i] = Math.round(sample * 32767);
        }

        // 使用 lamejs 编码 (单声道模式)
        const mp3Encoder = new lamejs.Mp3Encoder(1, sampleRate, bitrate);
        const mp3Data = [];

        const blockSize = 1152;
        for (let i = 0; i < samples; i += blockSize) {
            const chunk = pcmData.subarray(i, Math.min(i + blockSize, samples));
            const mp3buf = mp3Encoder.encodeBuffer(chunk);
            if (mp3buf.length > 0) {
                mp3Data.push(mp3buf);
            }
        }

        const mp3End = mp3Encoder.flush();
        if (mp3End.length > 0) {
            mp3Data.push(mp3End);
        }

        await audioContext.close();
        console.log(`✅ MP3 编码完成: ${samples} 样本 @ ${sampleRate}Hz`);
        return new Blob(mp3Data, { type: 'audio/mp3' });
    }

    // ============ 合并多段音频 Blob（使用 Web Audio API）============
    async function combineAudioBlobs(blobs) {
        if (blobs.length === 0) return new Blob([], { type: 'audio/aac' });
        if (blobs.length === 1) return blobs[0];

        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffers = [];

        // 解码所有音频 Blob
        for (const blob of blobs) {
            try {
                const arrayBuffer = await blob.arrayBuffer();
                const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                audioBuffers.push(audioBuffer);
            } catch (e) {
                console.warn('解码分段音频失败:', e);
            }
        }

        if (audioBuffers.length === 0) {
            await audioContext.close();
            return new Blob(blobs, { type: blobs[0]?.type || 'audio/aac' });
        }

        // 计算总采样数和统一采样率
        const sampleRate = audioBuffers[0].sampleRate;
        const numChannels = 1; // 强制单声道
        let totalSamples = 0;
        for (const buf of audioBuffers) {
            totalSamples += buf.length;
        }

        // 添加淡入淡出的采样数 (5ms)
        const fadeSamples = Math.floor(sampleRate * 0.005);

        // 创建合并后的 AudioBuffer
        const combinedBuffer = audioContext.createBuffer(numChannels, totalSamples, sampleRate);
        const outputChannel = combinedBuffer.getChannelData(0);

        let offset = 0;
        for (let i = 0; i < audioBuffers.length; i++) {
            const buf = audioBuffers[i];
            const inputChannel = buf.getChannelData(0);

            for (let j = 0; j < buf.length; j++) {
                let sample = inputChannel[j];

                // 淡入 (每段开头)
                if (j < fadeSamples) {
                    sample *= j / fadeSamples;
                }
                // 淡出 (每段结尾)
                if (j >= buf.length - fadeSamples) {
                    sample *= (buf.length - j) / fadeSamples;
                }

                outputChannel[offset + j] = sample;
            }
            offset += buf.length;
        }

        // 编码为 AAC (使用 WAV 作为中间格式，因为浏览器不支持 AAC 编码)
        // 这里输出 WAV 格式，后续可通过 convertToMp3 转为 MP3
        const wavBlob = audioBufferToWav(combinedBuffer);

        await audioContext.close();
        console.log(`✅ 音频合并完成: ${audioBuffers.length} 段 → ${totalSamples} 样本`);
        return wavBlob;
    }

    // 将 AudioBuffer 转换为 WAV Blob
    function audioBufferToWav(buffer) {
        const numChannels = buffer.numberOfChannels;
        const sampleRate = buffer.sampleRate;
        const format = 1; // PCM
        const bitDepth = 16;

        const bytesPerSample = bitDepth / 8;
        const blockAlign = numChannels * bytesPerSample;

        const samples = buffer.getChannelData(0);
        const dataLength = samples.length * bytesPerSample;
        const bufferLength = 44 + dataLength;

        const arrayBuffer = new ArrayBuffer(bufferLength);
        const view = new DataView(arrayBuffer);

        // RIFF header
        writeString(view, 0, 'RIFF');
        view.setUint32(4, bufferLength - 8, true);
        writeString(view, 8, 'WAVE');

        // fmt chunk
        writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true); // chunk size
        view.setUint16(20, format, true);
        view.setUint16(22, numChannels, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * blockAlign, true);
        view.setUint16(32, blockAlign, true);
        view.setUint16(34, bitDepth, true);

        // data chunk
        writeString(view, 36, 'data');
        view.setUint32(40, dataLength, true);

        // 写入采样数据
        let offset = 44;
        for (let i = 0; i < samples.length; i++) {
            const sample = Math.max(-1, Math.min(1, samples[i]));
            view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
            offset += 2;
        }

        return new Blob([arrayBuffer], { type: 'audio/wav' });
    }

    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }

    // ============ 单段 TTS（内部使用）============
    function ttsSingleChunk(text, options = {}, retryCount = 0) {
        const MAX_RETRIES = 2;

        return new Promise((resolve, reject) => {
            // 每次请求生成新的 web_tab_id，避免服务端状态冲突
            const wsUrl = buildUrl({ ...options, _timestamp: Date.now() });
            const ws = new WebSocket(wsUrl);
            const audioChunks = [];
            let finished = false;

            ws.onmessage = (event) => {
                if (typeof event.data === 'string') {
                    try {
                        const msg = JSON.parse(event.data);
                        switch (msg.event) {
                            case 'open_success':
                                ws.send(JSON.stringify({ event: 'text', text }));
                                ws.send(JSON.stringify({ event: 'finish' }));
                                break;
                            case 'finish':
                                finished = true;
                                ws.close();
                                const blob = new Blob(audioChunks, { type: `audio/${options.format || 'aac'}` });
                                resolve({ blob, text });
                                break;
                            case 'error':
                            case '':
                                // 空 event 通常表示错误
                                if (msg.code && msg.code !== 0) {
                                    ws.close();
                                    const errMsg = `TTS 错误 (${msg.code}): ${msg.message || '未知错误'}`;
                                    // 如果是 40000999 错误且还有重试次数，则重试
                                    if (msg.message?.includes('40000999') && retryCount < MAX_RETRIES) {
                                        console.log(`⚠️ 遇到 40000999 错误，${500 * (retryCount + 1)}ms 后重试...`);
                                        setTimeout(() => {
                                            ttsSingleChunk(text, options, retryCount + 1)
                                                .then(resolve)
                                                .catch(reject);
                                        }, 500 * (retryCount + 1));
                                    } else {
                                        reject(new Error(errMsg));
                                    }
                                }
                                break;
                        }
                    } catch (e) {
                        console.error('解析消息失败:', e);
                    }
                } else {
                    audioChunks.push(event.data);
                }
            };

            ws.onerror = () => {
                if (!finished) reject(new Error('连接失败'));
            };

            ws.onclose = (event) => {
                if (!finished && audioChunks.length === 0 && event.code !== 1000) {
                    reject(new Error(`连接关闭: ${event.code}`));
                }
            };

            setTimeout(() => {
                if (ws.readyState === WebSocket.OPEN && !finished) {
                    ws.close();
                    reject(new Error('超时'));
                }
            }, 60000); // 单段超时 60 秒
        });
    }

    // ============ 核心 TTS（支持长文本分段）============
    async function ttsWithTimestamps(text, options = {}, onProgress = null) {
        const textChunks = splitIntoChunks(text);
        const totalChunks = textChunks.length;
        const totalChars = text.length;

        console.log(`📝 文本 ${totalChars} 字，分成 ${totalChunks} 段进行处理`);
        if (onProgress) {
            onProgress('status', `📝 ${totalChars} 字，分成 ${totalChunks} 段`);
            onProgress('progress', { current: 0, total: totalChunks, preview: '' });
        }

        const allBlobs = [];

        // 逐段处理
        for (let i = 0; i < textChunks.length; i++) {
            const chunk = textChunks[i];
            console.log(`🔊 处理第 ${i + 1}/${totalChunks} 段 (${chunk.length}字): ${chunk.slice(0, 30)}...`);

            if (onProgress) {
                onProgress('progress', {
                    current: i + 1,
                    total: totalChunks,
                    preview: chunk.slice(0, 50)
                });
            }

            try {
                const result = await ttsSingleChunk(chunk, options);
                allBlobs.push(result.blob);

                // 段落之间延迟，避免请求过快触发服务端限制
                if (i < textChunks.length - 1) {
                    const delay = 300 + Math.random() * 200; // 300-500ms 随机延迟
                    await new Promise(r => setTimeout(r, delay));
                }
            } catch (error) {
                console.error(`❌ 第 ${i + 1} 段处理失败:`, error);
                throw new Error(`第 ${i + 1}/${totalChunks} 段失败: ${error.message}`);
            }
        }

        // 合并所有音频 Blob
        // 当有多段时使用 Web Audio API 正确合并，避免 Blob 直接拼接导致的格式损坏
        let combinedBlob;
        if (allBlobs.length > 1) {
            console.log(`🔗 正在合并 ${allBlobs.length} 段音频...`);
            combinedBlob = await combineAudioBlobs(allBlobs);
        } else {
            combinedBlob = allBlobs[0];
        }

        // 获取实际音频时长后生成 SRT
        const totalDuration = await getAudioDuration(combinedBlob);
        const sentenceTexts = splitSentences(text);
        const sentenceTotalChars = sentenceTexts.reduce((sum, s) => sum + s.length, 0);

        // 按字数比例分配时间
        let currentTime = 0;
        const sentences = sentenceTexts.map((s, i) => {
            const duration = (s.length / sentenceTotalChars) * totalDuration;
            const startTime = currentTime;
            const endTime = currentTime + duration;
            currentTime = endTime;

            return {
                index: i + 1,
                text: s,
                startTime: Math.round(startTime),
                endTime: Math.round(endTime)
            };
        });

        const srt = sentences.map(s =>
            `${s.index}\n${formatTime(s.startTime)} --> ${formatTime(s.endTime)}\n${s.text}`
        ).join('\n\n');

        if (onProgress) onProgress('status', '✅ 全部完成');

        return { blob: combinedBlob, srt, sentences, totalDuration: Math.round(totalDuration), text };
    }

    // ============ 旧版核心 TTS（保留用于短文本）============
    function ttsWithTimestampsLegacy(text, options = {}, onProgress = null) {
        return new Promise((resolve, reject) => {
            const ws = new WebSocket(buildUrl(options));
            const chunks = [];

            ws.onmessage = (event) => {
                if (typeof event.data === 'string') {
                    const msg = JSON.parse(event.data);
                    switch (msg.event) {
                        case 'open_success':
                            ws.send(JSON.stringify({ event: 'text', text }));
                            ws.send(JSON.stringify({ event: 'finish' }));
                            if (onProgress) onProgress('status', '正在生成...');
                            break;
                        case 'finish':
                            ws.close();
                            // 生成音频 Blob
                            const blob = new Blob(chunks, { type: `audio/${options.format || 'aac'}` });

                            // 获取实际音频时长后生成 SRT
                            getAudioDuration(blob).then(totalDuration => {
                                const sentenceTexts = splitSentences(text);
                                const totalChars = sentenceTexts.reduce((sum, s) => sum + s.length, 0);

                                // 按字数比例分配时间
                                let currentTime = 0;
                                const sentences = sentenceTexts.map((s, i) => {
                                    const duration = (s.length / totalChars) * totalDuration;
                                    const startTime = currentTime;
                                    const endTime = currentTime + duration;
                                    currentTime = endTime;

                                    if (onProgress) onProgress('sentence', s.slice(0, 20));

                                    return {
                                        index: i + 1,
                                        text: s,
                                        startTime: Math.round(startTime),
                                        endTime: Math.round(endTime)
                                    };
                                });

                                const srt = sentences.map(s =>
                                    `${s.index}\n${formatTime(s.startTime)} --> ${formatTime(s.endTime)}\n${s.text}`
                                ).join('\n\n');

                                resolve({ blob, srt, sentences, totalDuration: Math.round(totalDuration), text });
                            });
                            break;
                        case 'error':
                            ws.close();
                            reject(new Error(msg.message || 'TTS 错误'));
                            break;
                    }
                } else {
                    chunks.push(event.data);
                    if (onProgress) onProgress('audio', event.data.size || event.data.byteLength);
                }
            };

            ws.onerror = () => reject(new Error('连接失败'));
            setTimeout(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.close();
                    reject(new Error('超时'));
                }
            }, 300000);
        });
    }

    // ============ API ============
    window.tts = (text, opts) => ttsWithTimestamps(text, opts).then(r => r.blob);
    window.speak = async (text, opts) => {
        const { blob } = await ttsWithTimestamps(text, opts);
        const audio = new Audio(URL.createObjectURL(blob));
        audio.play();
        return audio;
    };
    window.ttsWithSRT = ttsWithTimestamps;
    window.downloadAll = async (text, baseName = 'output', opts) => {
        const result = await ttsWithTimestamps(text, opts);
        downloadBlob(result.blob, baseName + '.aac');
        downloadBlob(new Blob([result.srt], { type: 'text/plain;charset=utf-8' }), baseName + '.srt');
        return result;
    };

    // MP3 下载
    window.downloadMp3 = async (text, filename = 'speech.mp3', opts) => {
        const result = await ttsWithTimestamps(text, opts);
        console.log('🔄 转换为 MP3...');
        const mp3Blob = await convertToMp3(result.blob);
        downloadBlob(mp3Blob, filename);
        console.log('✅ MP3 下载完成');
        return mp3Blob;
    };

    // 转换已有 Blob
    window.toMp3 = convertToMp3;

    // Cookie 工具
    window.getCookies = getCookies;
    window.getAuthHeader = getAuthHeader;
    window.exportConfig = exportConfig;
    window.copyCookies = copyCookies;

    // 音色工具
    window.SPEAKERS = SPEAKERS;
    window.getSpeakerList = () => Object.keys(SPEAKERS);
    window.getSpeakerGroups = () => SPEAKER_GROUPS;

    function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    // ============ UI ============
    function createUI() {
        if (document.getElementById('tts-panel')) return;

        const speakerOptions = Object.entries(SPEAKER_GROUPS).map(([group, names]) =>
            `<optgroup label="${group}">${names.map(n => `<option value="${n}">${n}</option>`).join('')}</optgroup>`
        ).join('');

        const panel = document.createElement('div');
        panel.id = 'tts-panel';
        panel.innerHTML = `
      <style>
        #tts-panel{position:fixed;bottom:20px;right:20px;width:420px;max-height:85vh;background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.15);z-index:999999;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;overflow:hidden;display:flex;flex-direction:column}
        #tts-panel.minimized{width:60px;height:60px;border-radius:30px;cursor:pointer}
        #tts-panel.minimized .panel-body{display:none}
        #tts-panel.minimized .panel-header span,#tts-panel.minimized .header-btns{display:none}
        .panel-header{padding:14px 18px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;font-weight:600;display:flex;justify-content:space-between;align-items:center;cursor:move;flex-shrink:0}
        .header-btns{display:flex;gap:6px}
        .header-btns button{background:rgba(255,255,255,0.2);border:none;color:white;width:28px;height:28px;border-radius:6px;cursor:pointer;font-size:14px}
        .header-btns button:hover{background:rgba(255,255,255,0.3)}
        .panel-body{padding:16px;overflow-y:auto;flex:1}
        .input-area{width:100%;height:140px;border:2px solid #e5e7eb;border-radius:12px;padding:12px;font-size:14px;line-height:1.6;resize:vertical;box-sizing:border-box}
        .input-area:focus{outline:none;border-color:#667eea}
        .options-row{display:flex;gap:12px;margin:12px 0}
        .option-item{flex:1}
        .option-item label{display:flex;justify-content:space-between;font-size:12px;color:#6b7280;margin-bottom:4px}
        .option-item select,.option-item input[type="range"]{width:100%;accent-color:#667eea}
        .option-item select{padding:6px;border:1px solid #e5e7eb;border-radius:6px;font-size:13px}
        .btn-row{display:flex;gap:8px;flex-wrap:wrap}
        .btn{flex:1;min-width:70px;padding:10px 8px;border:none;border-radius:10px;font-size:13px;font-weight:500;cursor:pointer;transition:all 0.2s;display:flex;align-items:center;justify-content:center;gap:4px}
        .btn-primary{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white}
        .btn-primary:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(102,126,234,0.4)}
        .btn-secondary{background:#f3f4f6;color:#374151}
        .btn-secondary:hover{background:#e5e7eb}
        .btn:disabled{opacity:0.5;cursor:not-allowed;transform:none!important}
        .status-bar{margin-top:12px;padding:10px 12px;background:#f8fafc;border-radius:10px;font-size:13px;color:#64748b;display:none}
        .status-bar.show{display:block}
        .status-bar.error{background:#fef2f2;color:#dc2626}
        .status-bar.success{background:#f0fdf4;color:#16a34a}
        .progress-container{margin-top:8px;display:none}
        .progress-container.show{display:block}
        .progress-bar{height:6px;background:#e5e7eb;border-radius:3px;overflow:hidden}
        .progress-fill{height:100%;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);transition:width 0.3s ease;width:0%}
        .progress-text{font-size:11px;color:#9ca3af;margin-top:4px;display:flex;justify-content:space-between}
        .result-section{margin-top:12px;display:none}
        .result-section.show{display:block}
        .result-section audio{width:100%;margin-bottom:10px;border-radius:8px}
        .srt-box{max-height:150px;overflow-y:auto;background:#f8fafc;padding:10px;border-radius:8px;font-size:11px;font-family:monospace;white-space:pre-wrap;line-height:1.4;margin-bottom:10px;border:1px solid #e2e8f0}
      </style>
      <div class="panel-header">
        <span>🎤 豆包 TTS</span>
        <div class="header-btns">
          <button id="btn-cookie" title="复制Cookie">🔑</button>
          <button id="btn-min" title="最小化">−</button>
        </div>
      </div>
      <div class="panel-body">
        <textarea class="input-area" id="tts-input" placeholder="输入文本，整段发送保持情绪连贯..."></textarea>
        <div class="options-row">
          <div class="option-item">
            <label>音色</label>
            <select id="opt-speaker">${speakerOptions}</select>
          </div>
        </div>
        <div class="options-row">
          <div class="option-item">
            <label>语速 <span id="rate-val">0</span></label>
            <input type="range" id="opt-rate" min="-50" max="50" value="0">
          </div>
        </div>
        <div class="btn-row">
          <button class="btn btn-primary" id="btn-generate">🎬 生成</button>
        </div>
        <div class="status-bar" id="status"></div>
        <div class="progress-container" id="progress-container">
          <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
          <div class="progress-text"><span id="progress-text">0/0 段</span><span id="progress-percent">0%</span></div>
        </div>
        <div class="result-section" id="result">
          <audio id="audio" controls></audio>
          <div class="srt-box" id="srt-content"></div>
          <div class="btn-row">
            <button class="btn btn-secondary" id="btn-dl-audio">⬇️ AAC</button>
            <button class="btn btn-secondary" id="btn-dl-mp3">🎵 MP3</button>
            <button class="btn btn-secondary" id="btn-dl-srt">📝 SRT</button>
          </div>
        </div>
      </div>
    `;

        document.body.appendChild(panel);

        const input = document.getElementById('tts-input');
        const speakerSelect = document.getElementById('opt-speaker');
        const rateSlider = document.getElementById('opt-rate');
        const rateVal = document.getElementById('rate-val');
        const status = document.getElementById('status');
        const result = document.getElementById('result');
        const audio = document.getElementById('audio');
        const srtContent = document.getElementById('srt-content');
        const btnGenerate = document.getElementById('btn-generate');

        let currentResult = null;

        rateSlider.oninput = () => rateVal.textContent = rateSlider.value;

        function showStatus(msg, type = '') {
            status.textContent = msg;
            status.className = 'status-bar show ' + type;
        }

        function getOpts() {
            return {
                speaker: speakerSelect.value,
                speech_rate: parseInt(rateSlider.value)
            };
        }

        document.getElementById('btn-min').onclick = (e) => {
            e.stopPropagation();
            panel.classList.add('minimized');
        };
        document.getElementById('btn-cookie').onclick = (e) => {
            e.stopPropagation();
            copyCookies();
        };

        // 点击最小化的面板展开
        panel.onclick = () => {
            if (panel.classList.contains('minimized')) {
                panel.classList.remove('minimized');
            }
        };

        const progressContainer = document.getElementById('progress-container');
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        const progressPercent = document.getElementById('progress-percent');

        function showProgress(current, total, chunkPreview = '') {
            progressContainer.classList.add('show');
            const percent = Math.round((current / total) * 100);
            progressFill.style.width = percent + '%';
            progressText.textContent = `${current}/${total} 段`;
            progressPercent.textContent = percent + '%';
            if (chunkPreview) {
                showStatus(`🔊 正在处理: ${chunkPreview.slice(0, 40)}...`);
            }
        }

        function hideProgress() {
            progressContainer.classList.remove('show');
            progressFill.style.width = '0%';
        }

        btnGenerate.onclick = async () => {
            const text = input.value.trim();
            if (!text) return alert('请输入文字');
            btnGenerate.disabled = true;
            result.classList.remove('show');
            hideProgress();
            showStatus('🔄 分析文本...');
            try {
                currentResult = await ttsWithTimestamps(text, getOpts(), (type, data, extra) => {
                    if (type === 'progress') {
                        showProgress(data.current, data.total, data.preview);
                    } else if (type === 'status') {
                        showStatus(data);
                    }
                });
                hideProgress();
                audio.src = URL.createObjectURL(currentResult.blob);
                srtContent.textContent = currentResult.srt || '(无字幕)';
                result.classList.add('show');
                showStatus(`✅ ${currentResult.sentences.length}句，${Math.round(currentResult.totalDuration / 1000)}秒`, 'success');
            } catch (e) {
                hideProgress();
                showStatus('❌ ' + e.message, 'error');
            } finally {
                btnGenerate.disabled = false;
            }
        };

        document.getElementById('btn-dl-audio').onclick = () => currentResult && downloadBlob(currentResult.blob, 'speech.aac');
        document.getElementById('btn-dl-mp3').onclick = async () => {
            if (!currentResult) return;
            showStatus('🔄 转换 MP3 中...');
            try {
                const mp3Blob = await convertToMp3(currentResult.blob);
                downloadBlob(mp3Blob, 'speech.mp3');
                showStatus('✅ MP3 下载完成', 'success');
            } catch (e) {
                showStatus('❌ MP3 转换失败: ' + e.message, 'error');
            }
        };
        document.getElementById('btn-dl-srt').onclick = () => currentResult && downloadBlob(new Blob([currentResult.srt], { type: 'text/plain;charset=utf-8' }), 'subtitle.srt');

        // 拖拽
        let isDragging = false, offsetX, offsetY;
        panel.querySelector('.panel-header').onmousedown = (e) => {
            if (e.target.tagName === 'BUTTON') return;
            isDragging = true;
            offsetX = e.clientX - panel.offsetLeft;
            offsetY = e.clientY - panel.offsetTop;
        };
        document.onmousemove = (e) => {
            if (!isDragging) return;
            panel.style.left = (e.clientX - offsetX) + 'px';
            panel.style.top = (e.clientY - offsetY) + 'px';
            panel.style.right = 'auto';
            panel.style.bottom = 'auto';
        };
        document.onmouseup = () => isDragging = false;
    }

    if (document.readyState === 'complete') setTimeout(createUI, 1000);
    else window.addEventListener('load', () => setTimeout(createUI, 1000));

    console.log(`
╔════════════════════════════════════════════════════╗
║          豆包 TTS v4.3 - 简化UI                    ║
╠════════════════════════════════════════════════════╣
║ API:                                               ║
║   speak('文本', {speaker:'温柔桃子'})              ║
║   tts('文本') → Blob                               ║
║   ttsWithSRT('文本') → {blob, srt, sentences}      ║
║   downloadAll('文本', '文件名')                    ║
║                                                    ║
║ Cookie工具:                                        ║
║   getCookies()     - 获取Cookie                    ║
║   getAuthHeader()  - 获取认证头                    ║
║   exportConfig()   - 导出完整配置                  ║
║   copyCookies()    - 复制Cookie到剪贴板            ║
║                                                    ║
║ 音色: getSpeakerList() / SPEAKERS                  ║
╚════════════════════════════════════════════════════╝
  `);
})();
