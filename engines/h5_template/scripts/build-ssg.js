#!/usr/bin/env node
/**
 * build-ssg.js — H5 课件静态发布管线 (SSG Asset Pipeline)
 *
 * 设计原则 (SSOT):
 *   源仓库保持所有资产的原始格式（.aac / .png / .jpg）。
 *   格式转换只在此构建边界发生：
 *     - 图片 → WebP (via sharp)
 *     - 音频 → MP3 单声道 24kHz (via ffmpeg)
 *   转换后的产物写入 dist/，源文件不被修改。
 *
 * 数据流:
 *   1. 扫描 dist/ 下的课程 JSON（由 vite build 从 public/ 复制而来）
 *   2. 解析 JSON 中引用的图片路径 → 从源课程目录读取原始文件 → sharp 转 WebP → dist/assets/media/
 *   3. 解析 JSON 中的 ttsFp → 从源课程 tts/ 目录读取 .aac → ffmpeg 转 MP3 → dist/assets/tts/
 *   4. 重写 JSON 中的路径引用为相对静态路径
 *
 * 用法:
 *   node scripts/build-ssg.js                        # 自动检测 dist/
 *   node scripts/build-ssg.js --workspace /abs/path  # 指定工作区根目录
 */

import fs from 'fs-extra';
import path from 'path';
import sharp from 'sharp';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, '..');
const DIST_DIR = path.join(ROOT_DIR, 'dist');

// 工作区根：默认为 engines/h5_template 的上两级 (即课程工作区根目录)
// 可通过 --workspace 参数覆盖
const WORKSPACE_ARG = process.argv.find((_, i, a) => a[i - 1] === '--workspace');
const WORKSPACE_DIR = WORKSPACE_ARG
  ? path.resolve(WORKSPACE_ARG)
  : path.resolve(ROOT_DIR, '..', '..');

// FFmpeg 路径（一次性解析）
const FFMPEG_CMD = fs.existsSync('/opt/homebrew/bin/ffmpeg') ? '/opt/homebrew/bin/ffmpeg' : 'ffmpeg';

// Sharp 支持的输入格式白名单
const SHARP_SUPPORTED_EXTS = new Set(['.png', '.jpg', '.jpeg', '.tiff', '.webp', '.avif', '.gif']);

// ============ 核心管线 ============

async function run() {
  console.log('🚀 SSG Asset Pipeline 启动');
  console.log(`   工作区: ${WORKSPACE_DIR}`);
  console.log(`   输出目录: ${DIST_DIR}`);

  if (!fs.existsSync(DIST_DIR)) {
    console.error('❌ dist 目录不存在，请先运行 vite build');
    process.exit(1);
  }

  const assetsMediaDir = path.join(DIST_DIR, 'assets', 'media');
  const assetsTtsDir = path.join(DIST_DIR, 'assets', 'tts');
  await fs.ensureDir(assetsMediaDir);
  await fs.ensureDir(assetsTtsDir);

  // 查找 dist 中的所有课程 JSON
  const jsonFiles = findJsonFiles(path.join(DIST_DIR, 'courses'))
    .concat(findJsonFiles(DIST_DIR).filter(f => path.basename(f) === 'slides.json'));

  let imgOptimized = 0;
  let imgSkipped = 0;
  let ttsConverted = 0;
  let ttsSkipped = 0;
  let totalSavedBytes = 0;

  for (const jsonPath of jsonFiles) {
    if (path.basename(jsonPath) === 'manifest.json') continue;

    console.log(`\n📄 ${path.relative(DIST_DIR, jsonPath)}`);
    const data = await fs.readJson(jsonPath);
    let modified = false;

    const courseId = path.basename(path.dirname(jsonPath));

    for (const section of (data.sections || [])) {

      // ──── 图片资产：原始格式 → WebP ────
      for (const slide of (section.slides || [])) {
        const imagesToProcess = slide.images || (slide.image ? [slide.image] : []);
        const newImages = [];

        for (const img of imagesToProcess) {
          const srcAbsPath = path.join(WORKSPACE_DIR, courseId, img);
          if (!fs.existsSync(srcAbsPath)) {
            console.warn(`   ⚠️ 图片不存在: ${img}`);
            newImages.push(img);
            continue;
          }

          const ext = path.extname(img).toLowerCase();

          // V-10 fix: 跳过 Sharp 不支持的格式（如 .svg），直接复制
          if (!SHARP_SUPPORTED_EXTS.has(ext)) {
            // V-07 fix: 用课程ID+路径哈希防止文件名碰撞
            const safeBase = sanitizeAssetName(courseId, img);
            const destPath = path.join(assetsMediaDir, `${safeBase}${ext}`);
            if (!fs.existsSync(destPath)) {
              await fs.copy(srcAbsPath, destPath);
              imgSkipped++;
            }
            newImages.push(`/assets/media/${safeBase}${ext}`);
            modified = true;
            continue;
          }

          // V-07 fix: 生成不碰撞的输出文件名
          const safeBase = sanitizeAssetName(courseId, img);
          const outName = `${safeBase}.webp`;
          const outPath = path.join(assetsMediaDir, outName);

          if (!fs.existsSync(outPath)) {
            try {
              const beforeSize = fs.statSync(srcAbsPath).size;
              await sharp(srcAbsPath).webp({ quality: 80 }).toFile(outPath);
              const afterSize = fs.statSync(outPath).size;
              totalSavedBytes += Math.max(0, beforeSize - afterSize);
              imgOptimized++;
            } catch (err) {
              console.warn(`   ⚠️ Sharp 转换失败 (${img}): ${err.message}，回退为直接复制`);
              await fs.copy(srcAbsPath, path.join(assetsMediaDir, `${safeBase}${ext}`));
              newImages.push(`/assets/media/${safeBase}${ext}`);
              modified = true;
              continue;
            }
          }

          newImages.push(`/assets/media/${outName}`);
          modified = true;
        }

        if (newImages.length > 0) {
          if (slide.image) slide.image = newImages[0];
          slide.images = newImages;
        }
      }

      // ──── TTS 音频：原始 AAC → MP3 (单声道 24kHz) ────
      for (const para of (section.paragraphs || [])) {
        if (!para.ttsFp || para.ttsFp.startsWith('00000000')) continue;

        // 在所有 week 的 tts/ 目录中搜索源文件
        const srcAac = findTtsSource(courseId, para.ttsFp);
        if (!srcAac) {
          ttsSkipped++;
          continue;
        }

        const destMp3 = path.join(assetsTtsDir, `${para.ttsFp}.mp3`);

        if (!fs.existsSync(destMp3)) {
          try {
            await transcodeToMp3(srcAac, destMp3);
            ttsConverted++;
          } catch (err) {
            console.warn(`   ⚠️ FFmpeg 转码失败 (${para.ttsFp}): ${err.message}，回退为直接复制`);
            const destAac = path.join(assetsTtsDir, `${para.ttsFp}.aac`);
            await fs.copy(srcAac, destAac);
          }
        }

        // 重写路径：生产态使用相对的静态路径
        const ext = fs.existsSync(destMp3) ? '.mp3' : '.aac';
        para.staticTtsUrl = `/assets/tts/${para.ttsFp}${ext}`;
        modified = true;
      }
    }

    if (modified) {
      await fs.writeJson(jsonPath, data, { spaces: 2 });
      console.log(`   ✅ JSON 路径已重写 (static)`);
    }
  }

  // 生成静态 TTS manifest（供生产态前端使用）
  const staticManifest = buildStaticManifest(assetsTtsDir);
  await fs.writeJson(path.join(assetsTtsDir, 'manifest.json'), staticManifest);

  // 汇总报告
  console.log(`\n${'─'.repeat(50)}`);
  console.log(`🎉 SSG Pipeline 完成`);
  console.log(`   📸 图片: ${imgOptimized} 张转 WebP, ${imgSkipped} 张直接复制 (节省 ${(totalSavedBytes / 1024 / 1024).toFixed(2)} MB)`);
  console.log(`   🔊 音频: ${ttsConverted} 段转 MP3, ${ttsSkipped} 段缺失 (跳过)`);
}

// ============ 辅助函数 ============

/**
 * V-07 fix: 生成不碰撞的资产文件名
 * 策略：courseId + 去路径分隔符的相对路径哈希 → 短前缀 + 原始 basename
 */
function sanitizeAssetName(courseId, relPath) {
  const base = path.basename(relPath, path.extname(relPath));
  // 从相对路径中提取周次信息（如有）
  const weekMatch = relPath.match(/W\d+[^/]*/);
  const weekPrefix = weekMatch ? weekMatch[0] : '';
  // 拼装：courseId 前4字符 + 周次 + 原始文件名
  const prefix = courseId.slice(0, 4).replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '');
  return `${prefix}_${weekPrefix}_${base}`.replace(/_{2,}/g, '_');
}

/**
 * 在工作区中搜索 TTS 源文件 (.aac 或 .mp3)
 */
function findTtsSource(courseId, fp) {
  const courseDir = path.join(WORKSPACE_DIR, courseId);
  const weeksDir = path.join(courseDir, 'weeks');

  if (!fs.existsSync(weeksDir)) return null;

  for (const week of fs.readdirSync(weeksDir)) {
    const ttsDir = path.join(weeksDir, week, 'tts');
    if (!fs.existsSync(ttsDir)) continue;

    // 优先 .aac (源格式)，然后 .mp3 (可能已被手动转换过)
    for (const ext of ['.aac', '.mp3']) {
      const candidate = path.join(ttsDir, `${fp}${ext}`);
      if (fs.existsSync(candidate)) return candidate;
    }
  }

  return null;
}

/**
 * FFmpeg 转码：任意音频 → MP3 单声道 24kHz VBR
 */
function transcodeToMp3(inputPath, outputPath) {
  return new Promise((resolve, reject) => {
    const proc = spawn(FFMPEG_CMD, [
      '-y',
      '-i', inputPath,
      '-ac', '1',            // 单声道
      '-ar', '24000',        // 24kHz
      '-c:a', 'libmp3lame',
      '-q:a', '5',           // VBR 质量（语音适配）
      outputPath,
    ]);

    let stderr = '';
    proc.stderr.on('data', (d) => { stderr += d.toString(); });
    proc.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exit ${code}: ${stderr.slice(-300)}`));
    });
    proc.on('error', reject);
  });
}

/**
 * 构建静态 TTS manifest（遍历 dist/assets/tts/ 下的所有音频文件）
 */
function buildStaticManifest(ttsDir) {
  const segments = {};
  if (fs.existsSync(ttsDir)) {
    for (const f of fs.readdirSync(ttsDir)) {
      const m = f.match(/^(.+)\.(mp3|aac)$/);
      if (m) {
        const stat = fs.statSync(path.join(ttsDir, f));
        segments[m[1]] = {
          format: m[2],
          size: stat.size,
          static: true,
        };
      }
    }
  }
  return { version: 1, segments };
}

/**
 * 递归查找 JSON 文件
 */
function findJsonFiles(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;
  for (const file of fs.readdirSync(dir)) {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      findJsonFiles(filePath, fileList);
    } else if (file.endsWith('.json')) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

run().catch((err) => {
  console.error('❌ SSG Pipeline 致命错误:', err);
  process.exit(1);
});
