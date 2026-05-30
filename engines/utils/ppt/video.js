/**
 * ppt/video.js — 视频安全着陆系统
 *
 * ADR-042 跨端兼容层 → ADR-044 PPT 原生嵌入升级
 *
 * 负责视频类型判断、首帧 poster 提取（含播放按钮叠加）、
 * 以及 PPTX 兼容 MP4 格式转码（含 VTT 硬字幕烧录）。
 */
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const { VIDEO_EXTS } = require('./constants');

// ============================================================
// 视频类型判断
// ============================================================

/**
 * 判断资产路径是否为视频文件
 * @param {string} assetPath - 资产路径
 * @returns {boolean}
 */
function isVideoAsset(assetPath) {
    if (!assetPath) return false;
    const ext = path.extname(assetPath).toLowerCase();
    return VIDEO_EXTS.includes(ext);
}

// ============================================================
// Poster 提取
// ============================================================

/**
 * 使用 ffmpeg 从视频中提取首帧，叠加半透明播放按钮，生成 poster 图片。
 *
 * 缓存策略：poster 存放于 scriptDir/.build/_video_posters/，
 * 仅在 poster 不存在或视频文件更新时重新提取。
 *
 * @param {string} videoPath - 视频文件的绝对路径
 * @param {string} scriptDir - 脚本所在目录（用于确定缓存位置）
 * @returns {string|null} poster 图片的绝对路径，失败时返回 null
 */
function extractPosterFrame(videoPath, scriptDir) {
    const videoName = path.basename(videoPath, path.extname(videoPath));
    const cacheDir = path.resolve(scriptDir, '.build', '_video_posters');
    const posterPath = path.resolve(cacheDir, `${videoName}_poster.png`);

    // 缓存命中检查
    if (fs.existsSync(posterPath)) {
        try {
            const videoMtime = fs.statSync(videoPath).mtimeMs;
            const posterMtime = fs.statSync(posterPath).mtimeMs;
            if (posterMtime > videoMtime) {
                return posterPath; // 缓存有效
            }
        } catch (e) {
            // 忽略 stat 错误，重新生成
        }
    }

    // 确保缓存目录存在
    if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, { recursive: true });
    }

    // 检查是否存在同名的手工 poster 文件（如 Dropbox_MVP_poster.png）
    const manualPoster = path.resolve(path.dirname(videoPath), `${videoName}_poster.png`);
    if (fs.existsSync(manualPoster)) {
        console.log(`   🖼️  [Video] 使用手工 poster: ${path.basename(manualPoster)}`);
        fs.copyFileSync(manualPoster, posterPath);
        return posterPath;
    }

    // 使用 ffmpeg 提取首帧（3秒处，或视频开头）
    const ffmpegBin = '/opt/homebrew/bin/ffmpeg';
    const tmpRaw = path.resolve(cacheDir, `${videoName}_raw.png`);

    try {
        // 尝试在 3 秒处提取，如果视频不足 3 秒则用首帧
        execSync(
            `${ffmpegBin} -y -ss 00:00:03 -i "${videoPath}" -vframes 1 -q:v 2 "${tmpRaw}" 2>/dev/null` +
            ` || ${ffmpegBin} -y -i "${videoPath}" -vframes 1 -q:v 2 "${tmpRaw}" 2>/dev/null`,
            { stdio: 'pipe', timeout: 15000 }
        );

        if (!fs.existsSync(tmpRaw)) {
            console.warn(`   ⚠️  [Video] ffmpeg 首帧提取失败: ${path.basename(videoPath)}`);
            return null;
        }

        // 叠加半透明播放按钮三角形 (使用 ffmpeg drawbox + 文字绘制播放符号)
        execSync(
            `${ffmpegBin} -y -i "${tmpRaw}" ` +
            `-vf "drawbox=x=iw/2-40:y=ih/2-40:w=80:h=80:color=black@0.5:t=fill, ` +
            `drawtext=text='▶':fontsize=48:fontcolor=white@0.9:x=(w-tw)/2:y=(h-th)/2" ` +
            `"${posterPath}" 2>/dev/null`,
            { stdio: 'pipe', timeout: 10000 }
        );

        // 如果叠加失败，退化为使用原始首帧
        if (!fs.existsSync(posterPath)) {
            fs.renameSync(tmpRaw, posterPath);
        } else {
            // 清理临时文件
            try { fs.unlinkSync(tmpRaw); } catch (e) { /* 忽略 */ }
        }

        console.log(`   🎬→🖼️  [Video] 提取 poster: ${path.basename(videoPath)} → ${path.basename(posterPath)}`);
        return posterPath;
    } catch (e) {
        console.warn(`   ⚠️  [Video] poster 生成失败 (${path.basename(videoPath)}): ${e.message}`);
        // 清理可能的残留文件
        try { if (fs.existsSync(tmpRaw)) fs.unlinkSync(tmpRaw); } catch (e2) { /* 忽略 */ }
        return null;
    }
}

// ============================================================
// PPTX 兼容 MP4 转码
// ============================================================

/**
 * 将视频转换为 PPTX 可嵌入的 MP4 格式（含可选 VTT 硬字幕烧录）。
 *
 * 处理流程：
 *   1. 检测同名 .zh-Hant.vtt / .en.vtt 字幕文件
 *   2. 若源为 .webm 或存在字幕 → ffmpeg 转码/烧录 → 输出 .mp4
 *   3. 若源已是 .mp4 且无字幕 → 直接返回原路径
 *
 * 缓存策略：产物存放于 scriptDir/.build/_video_pptx/，
 * 仅在源视频或字幕文件更新时重新转码。
 *
 * @param {string} videoPath - 视频文件的绝对路径
 * @param {string} scriptDir - 脚本所在目录
 * @returns {{ mp4Path: string|null, subtitleLang: string|null, posterPath: string|null }}
 */
function convertVideoForPptx(videoPath, scriptDir) {
    const videoName = path.basename(videoPath, path.extname(videoPath));
    const videoDir = path.dirname(videoPath);
    const videoExt = path.extname(videoPath).toLowerCase();
    const cacheDir = path.resolve(scriptDir, '.build', '_video_pptx');
    const mp4Output = path.resolve(cacheDir, `${videoName}.mp4`);
    const ffmpegBin = '/opt/homebrew/bin/ffmpeg';

    // 检测同名字幕文件（优先中文，回退英文）
    let vttPath = null;
    let subtitleLang = null;
    const vttCandidates = [
        { path: path.resolve(videoDir, `${videoName}.zh-Hant.vtt`), lang: 'zh-Hant' },
        { path: path.resolve(videoDir, `${videoName}.zh.vtt`), lang: 'zh' },
        { path: path.resolve(videoDir, `${videoName}.en.vtt`), lang: 'en' },
        { path: path.resolve(videoDir, `${videoName}.srt`), lang: 'srt' },
    ];
    for (const cand of vttCandidates) {
        if (fs.existsSync(cand.path)) {
            vttPath = cand.path;
            subtitleLang = cand.lang;
            break;
        }
    }

    // 若源已是 MP4 且无字幕需要烧录 → 直接返回原路径
    if (videoExt === '.mp4' && !vttPath) {
        return { mp4Path: videoPath, subtitleLang: null, posterPath: null };
    }

    // 确保缓存目录存在
    if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, { recursive: true });
    }

    // 缓存命中检查 — 源视频和字幕都未更新时跳过
    if (fs.existsSync(mp4Output)) {
        try {
            const outMtime = fs.statSync(mp4Output).mtimeMs;
            const srcMtime = fs.statSync(videoPath).mtimeMs;
            const vttMtime = vttPath ? fs.statSync(vttPath).mtimeMs : 0;
            if (outMtime > srcMtime && outMtime > vttMtime) {
                console.log(`   ✅ [Video→PPTX] 缓存命中: ${videoName}.mp4`);
                // 同时生成/复用 poster 用于 addMedia cover
                const posterPath = extractPosterFrame(videoPath, scriptDir);
                return { mp4Path: mp4Output, subtitleLang, posterPath };
            }
        } catch (e) { /* 忽略 stat 错误，重新转码 */ }
    }

    // 构建 ffmpeg 命令
    let cmd;
    if (vttPath) {
        // 带字幕烧录的转码
        // 注意：subtitles 滤镜需要对路径中的特殊字符进行转义
        const escapedVtt = vttPath.replace(/'/g, "'\\\\\\''").replace(/:/g, '\\\\:');
        cmd = `${ffmpegBin} -y -i "${videoPath}" ` +
            `-vf "subtitles='${escapedVtt}':force_style='FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,MarginV=25'" ` +
            `-c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k ` +
            `"${mp4Output}" 2>&1`;
        console.log(`   🎬→📦 [Video→PPTX] 转码+硬字幕(${subtitleLang}): ${path.basename(videoPath)}`);
    } else {
        // 纯格式转码（WebM → MP4）
        cmd = `${ffmpegBin} -y -i "${videoPath}" ` +
            `-c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k ` +
            `"${mp4Output}" 2>&1`;
        console.log(`   🎬→📦 [Video→PPTX] 格式转码: ${path.basename(videoPath)} → MP4`);
    }

    try {
        execSync(cmd, { stdio: 'pipe', timeout: 120000 }); // 2 分钟超时
        if (!fs.existsSync(mp4Output)) {
            console.warn(`   ⚠️  [Video→PPTX] 转码产物未生成: ${videoName}.mp4`);
            return { mp4Path: null, subtitleLang: null, posterPath: null };
        }
        const sizeMB = (fs.statSync(mp4Output).size / 1024 / 1024).toFixed(1);
        console.log(`   ✅ [Video→PPTX] 转码完成: ${videoName}.mp4 (${sizeMB} MB)`);
        // 提取 poster 用于 addMedia cover
        const posterPath = extractPosterFrame(videoPath, scriptDir);
        return { mp4Path: mp4Output, subtitleLang, posterPath };
    } catch (e) {
        console.warn(`   ⚠️  [Video→PPTX] 转码失败 (${path.basename(videoPath)}): ${e.message?.substring(0, 200)}`);
        return { mp4Path: null, subtitleLang: null, posterPath: null };
    }
}

module.exports = {
    isVideoAsset,
    extractPosterFrame,
    convertVideoForPptx,
};
