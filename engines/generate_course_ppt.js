/**
 * generate_course_ppt.js — 通用 PPT 生成器主入口 (Workspace 级)
 * 
 * 用法:
 *   node engines/generate_course_ppt.js <课程目录> <脚本相对路径>
 * 
 * 示例:
 *   node engines/generate_course_ppt.js 信息可视化 weeks/W01_Visual_Perception/script.md
 *   node engines/generate_course_ppt.js 实习指导 scripts/S01_Mobilization.md
 */
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");
const { loadTheme, defaultTheme } = require('./utils/ppt_theme');
const { parseScript } = require('./utils/ppt_parser');
const { renderSlide } = require('./utils/ppt_layouts');

// 1. 获取参数
const courseDir = process.argv[2];
const scriptRelPath = process.argv[3];

// 解析可选 --brand 参数（如 --brand nfu）
let brandName = null;
const brandIdx = process.argv.indexOf('--brand');
if (brandIdx !== -1 && process.argv[brandIdx + 1]) {
    brandName = process.argv[brandIdx + 1].toLowerCase();
}

if (!courseDir || !scriptRelPath) {
    console.error("❌ 用法: node engines/generate_course_ppt.js <课程目录> <脚本路径> [--brand nfu]");
    console.error("   示例: node engines/generate_course_ppt.js 信息可视化 weeks/W01_Visual_Perception/script.md");
    console.error("   品牌: node engines/generate_course_ppt.js 交互产品开发 weeks/W01/package.yaml --brand nfu");
    process.exit(1);
}

// 2. 路径解析 — CWD 应为 workspace 根目录
const CWD = process.cwd();
const coursePath = path.resolve(CWD, courseDir);
let scriptPath = path.resolve(coursePath, scriptRelPath);
let scriptDir = path.dirname(scriptPath);
let scriptName = path.basename(scriptPath, '.md');

// 兼容 V5 架构：如果用户传入 script.md 但不存在，尝试寻找 package.yaml
if (!fs.existsSync(scriptPath)) {
    if (scriptPath.endsWith('script.md')) {
        const yamlAlt = scriptPath.replace('script.md', 'package.yaml');
        if (fs.existsSync(yamlAlt)) {
            scriptPath = yamlAlt;
            scriptName = path.basename(scriptPath, '.yaml');
            // scriptDir 保持为 package.yaml 所在目录（而非 .build/ 子目录）
            scriptDir = path.dirname(scriptPath);
        }
    }
}

if (!fs.existsSync(scriptPath)) {
    console.error(`❌ 脚本/配置不存在: ${scriptPath}`);
    process.exit(1);
}

console.log(`📌 课程: ${courseDir}`);
console.log(`📖 源文件: ${path.basename(scriptPath)}`);

let actualScriptPath = scriptPath;
const isYaml = scriptPath.endsWith('.yaml') || scriptPath.endsWith('.yml');

if (isYaml) {
    // V5 架构：自动调用 dumptext 编译 yaml
    const buildDir = path.join(scriptDir, '.build');
    const compiledPath = path.join(buildDir, 'compiled.md');
    const srcDir = path.join(scriptDir, 'src');
    
    let needsRecompile = !fs.existsSync(compiledPath);
    if (!needsRecompile) {
        const compiledMtime = fs.statSync(compiledPath).mtimeMs;
        if (fs.statSync(scriptPath).mtimeMs > compiledMtime) needsRecompile = true;
        if (!needsRecompile && fs.existsSync(srcDir)) {
            needsRecompile = fs.readdirSync(srcDir)
                .filter(f => f.endsWith('.md'))
                .some(f => fs.statSync(path.join(srcDir, f)).mtimeMs > compiledMtime);
        }
    }
    
    if (needsRecompile) {
        console.log(`🧩 [V5] 检测到源码更新，正在编译 ${path.basename(scriptPath)} -> .build/compiled.md...`);
        try {
            execSync(`python engines/dumptext.py "${scriptPath}" --mode full`, { stdio: 'inherit', cwd: CWD });
        } catch (e) {
            console.error(`❌ V5 yaml 编译失败`, e.message);
        }
    }
    actualScriptPath = fs.existsSync(compiledPath) ? compiledPath : scriptPath;
} else {
    // V4 兼容：检测 script.md 是否含 <!-- include: --> 指令
    const scriptContent = fs.readFileSync(scriptPath, 'utf-8');
    if (/<!--\s*include:\s*.+?\s*-->/.test(scriptContent)) {
        const compiledPath = scriptPath.replace(/\.md$/, '_compiled.md');
        let needsRecompile = !fs.existsSync(compiledPath)
            || fs.statSync(scriptPath).mtimeMs > fs.statSync(compiledPath).mtimeMs
            || (() => {
                const segDir = path.join(scriptDir, '_segments');
                if (!fs.existsSync(segDir)) return false;
                const compiledMtime = fs.statSync(compiledPath).mtimeMs;
                return fs.readdirSync(segDir)
                    .filter(f => f.endsWith('.md'))
                    .some(f => fs.statSync(path.join(segDir, f)).mtimeMs > compiledMtime);
            })();

    if (needsRecompile) {
        console.log('🔄 检测到分片架构，自动编译...');
        try {
            execSync(
                `python3 "${path.resolve(CWD, 'engines/dumptext.py')}" "${scriptPath}" --mode full --output "${compiledPath}"`,
                { stdio: 'inherit' }
            );
        } catch (e) {
            console.error('❌ 分片编译失败:', e.message);
            process.exit(1);
        }
    } else {
        console.log('✅ 使用已缓存的编译产物: _compiled.md');
    }
    actualScriptPath = compiledPath;
}
// 闭合最外层的 isYaml 的 else 分支
}

// 3. 加载主题 (visual_system.yaml)
// 按优先级搜索全局题库与课程目录内的配置文件
const yaml = require("js-yaml");
let globalThemePath = null;
const courseYamlPath = path.resolve(coursePath, 'course.yaml');
if (fs.existsSync(courseYamlPath)) {
    try {
        const courseConfig = yaml.load(fs.readFileSync(courseYamlPath, 'utf8'));
        const themeRef = courseConfig?.agent?.standards?.visual_system || "";
        if (themeRef.startsWith("@theme:")) {
            const themeName = themeRef.replace("@theme:", "");
            globalThemePath = path.resolve(CWD, '.agent', 'styles', `theme_${themeName}.yaml`);
        }
    } catch (e) {
        console.warn(`⚠️ 解析 course.yaml 主题配置失败: ${e.message}`);
    }
}

const potentialPaths = [
    ...(globalThemePath ? [globalThemePath] : []),
    path.resolve(coursePath, 'visual_system.yaml'),
    path.resolve(coursePath, 'styles/visual_system.yaml'),
];

let themePath = potentialPaths.find(p => fs.existsSync(p));
let theme;

if (themePath) {
    console.log(`🎨 加载主题: ${themePath}`);
    try {
        theme = loadTheme(themePath);
        console.log(`   颜色 keys: ${Object.keys(theme.C).join(', ')}`);
        console.log(`   字体: title=${theme.FONT.title}, body=${theme.FONT.body}`);
    } catch (e) {
        console.warn(`⚠️  主题加载失败: ${e.message}，使用默认低保真主题`);
        theme = defaultTheme();
    }
} else {
    console.log(`ℹ️  未找到 visual_system.yaml（搜索路径: ${potentialPaths.map(p => path.relative(CWD, p)).join(', ')}）`);
    console.log(`   使用默认低保真主题`);
    theme = defaultTheme();
}

// 品牌三色覆盖：当 --brand nfu 时，用 NFU 强调色叠加主题 primary/secondary/tertiary
if (brandName === 'nfu') {
    const nfuThemePath = path.resolve(CWD, '.agent', 'skills', 'pptx-nfu-branded', 'resources', 'nfu_theme.yaml');
    if (fs.existsSync(nfuThemePath)) {
        try {
            const nfuRaw = yaml.load(fs.readFileSync(nfuThemePath, 'utf-8'));
            const nfuPalette = nfuRaw?.palette || {};
            // 映射：accent1(蓝) → primary, accent4(绿) → secondary, accent2(橙) → tertiary
            const brandOverrides = {
                primary: nfuPalette.accent1,
                secondary: nfuPalette.accent4,
                tertiary: nfuPalette.accent2,
            };
            for (const [key, val] of Object.entries(brandOverrides)) {
                if (val) {
                    theme.C[key] = val.replace('#', '');
                }
            }
            console.log(`🎨 [Brand] NFU 品牌三色已覆盖 → primary: #${theme.C.primary}, secondary: #${theme.C.secondary}, tertiary: #${theme.C.tertiary}`);
        } catch (e) {
            console.warn(`⚠️  NFU 品牌主题加载失败: ${e.message}，保持原有配色`);
        }
    } else {
        console.warn(`⚠️  找不到 NFU 品牌主题: ${path.relative(CWD, nfuThemePath)}`);
    }
} else if (brandName) {
    console.warn(`⚠️  未知品牌 "${brandName}"，当前仅支持 --brand nfu`);
}

// 4. 解析脚本（使用编译后的路径，对单体脚本透明兼容）
console.log(`\n📖 解析 ${scriptName}...`);
const slides = parseScript(actualScriptPath);
console.log(`✅ 发现 ${slides.length} 张 Slide`);

// 输出 Slide 清单
slides.forEach((s, i) => {
    const layout = s.visual.layout || '(未指定)';
    const slideId = s.visual.slide || '(无ID)';
    const speechLen = s.speech ? s.speech.length : 0;
    console.log(`   ${i + 1}. [${layout}] ${slideId} — Notes: ${speechLen} 字符`);
});

// 5. 生成 PPT
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Course PPT Generator";
pres.title = scriptName;

let lastSeenH2 = null;
let lastSeenH3 = null;

slides.forEach((slide, i) => {
    try {
        if (slide.visual) {
            let h2Changed = false;
            
            // H2 跳变检测：插入重装模块章封面
            if (slide.visual.h2) {
                if (lastSeenH2 !== null && slide.visual.h2 !== lastSeenH2) {
                    h2Changed = true;
                    // 生成超大模块过渡页
                    const trSlide = pres.addSlide();
                    trSlide.background = { color: theme.C.bg_dark || theme.C.bg_base || '1A1A1A' };
                    
                    // 中间巨型模块标
                    trSlide.addText(slide.visual.h2, {
                        x: 0.5, y: 2.2, w: 9.0, h: 1.2,
                        fontSize: 48, fontFace: theme.FONT.title, color: theme.C.text_on_dark || 'FFFFFF',
                        align: 'center', bold: true, margin: 0,
                    });
                }
                lastSeenH2 = slide.visual.h2;
            }

            // H3 跳变检测：在未处于刚插入 H2 封面的情况下，插入轻装断言过渡
            if (slide.visual.h3) {
                if (lastSeenH3 !== null && slide.visual.h3 !== lastSeenH3) {
                    if (!h2Changed) {
                        const trSlide = pres.addSlide();
                        trSlide.background = { color: theme.C.bg_dark || theme.C.bg_base || '1A1A1A' };
                        
                        // 顶部辅助线
                        trSlide.addShape(pres.shapes.RECTANGLE, {
                            x: 0, y: 0, w: 10.0, h: 0.08,
                            fill: { color: theme.C.primary || 'B85042' },
                        });
                        
                        // 模块归属 (H2)
                        if (slide.visual.h2) {
                            trSlide.addText(slide.visual.h2, {
                                x: 0.8, y: 2.0, w: 8.4, h: 0.5,
                                fontSize: 16, fontFace: theme.FONT.body, color: theme.C.primary_light || theme.C.primary || 'EEAA88',
                                align: 'left', italic: true
                            });
                        }
                        
                        // 核心断言 (H3)
                        trSlide.addText(slide.visual.h3, {
                            x: 0.8, y: 2.5, w: 8.4, h: 1.5,
                            fontSize: 34, fontFace: theme.FONT.title, color: theme.C.text_on_dark || 'FFFFFF',
                            align: 'left', bold: true, margin: 0,
                        });
                    }
                }
                lastSeenH3 = slide.visual.h3;
            }
            
            // 纯文字资产降级策略：Mermaid 图表 -> 网络图片
            if (slide.visual.assetType === 'mermaid' && slide.visual.assetContent) {
                const b64 = Buffer.from(slide.visual.assetContent).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
                const url = `https://mermaid.ink/img/${b64}`;
                // 统一输出目录提前创建，或者写在临时目录
                const mmdDir = path.resolve(coursePath, 'build', 'artifacts', '_intermediate');
                if (!fs.existsSync(mmdDir)) fs.mkdirSync(mmdDir, { recursive: true });
                const imgPath = path.resolve(mmdDir, `mermaid_slide_${i}.png`);
                
                if (!fs.existsSync(imgPath)) {
                    console.log(`   🌊 [Mermaid] 下载远端图表...`);
                    try {
                        execSync(`curl -sL "${url}" -o "${imgPath}"`, { timeout: 15000 });
                        if (fs.existsSync(imgPath) && fs.statSync(imgPath).size > 0) {
                            slide.visual.assets = [imgPath];
                            slide.visual.asset = imgPath;
                        } else {
                            console.warn(`   ⚠️  [Mermaid] 下载失败，图片为空`);
                        }
                    } catch(e) {
                        console.warn(`   ⚠️  [Mermaid] 网络异常: ${e.message}`);
                    }
                } else {
                    slide.visual.assets = [imgPath];
                    slide.visual.asset = imgPath;
                }
            }
        }

        renderSlide(pres, slide, theme, scriptDir);
    } catch (err) {
        console.error(`❌ 渲染 Slide ${i + 1} 失败 (${slide.visual.layout}):`, err.message);
        // 生成错误占位页
        const s = pres.addSlide();
        s.background = { color: 'FF0000' };
        s.addText(`Error: Slide ${i + 1}`, { x: 1, y: 1, w: 8, h: 1, color: 'FFFFFF', fontSize: 24 });
        s.addText(err.message, { x: 1, y: 2.5, w: 8, h: 2, color: 'FFFFFF', fontSize: 14 });
    }
});

// 6. 保存 — 统一命名规范: <课程>_<周次>_<产物类型>.pptx
// 从 scriptDir 推导 weekId（取 package.yaml 所在目录名）
const weekDirName = path.basename(scriptDir);
// 判断该目录名是否匹配 weeks/WXX_xxx 模式
const weekMatch = weekDirName.match(/^(W\d+)_(.+)$/);
const weekId = weekMatch ? weekDirName : scriptName; // fallback 到旧命名

// 统一输出目录: build/artifacts/<weekId>/
const artifactsDir = path.resolve(coursePath, 'build', 'artifacts', weekId);
const intermediateDir = path.resolve(coursePath, 'build', 'artifacts', '_intermediate');
if (!fs.existsSync(artifactsDir)) fs.mkdirSync(artifactsDir, { recursive: true });
if (!fs.existsSync(intermediateDir)) fs.mkdirSync(intermediateDir, { recursive: true });

// 旧版 build/presentations/ 同时保留（向后兼容）
const legacyDir = path.resolve(coursePath, 'build', 'presentations');
if (!fs.existsSync(legacyDir)) fs.mkdirSync(legacyDir, { recursive: true });

// 裸 PPT 按统一命名写入 _intermediate/
const rawFileName = `${courseDir}_${weekId}_Presentation.pptx`;
const rawOutputPath = path.resolve(intermediateDir, rawFileName);

pres.writeFile({ fileName: rawOutputPath })
    .then(() => {
        console.log(`\n🎉 裸 PPT 保存成功: ${path.relative(CWD, rawOutputPath)}`);
        console.log(`   Slide 数: ${slides.length}`);

        // 自动调用 NFU 品牌注入管线
        const brandedFileName = `${courseDir}_${weekId}_Branded.pptx`;
        const brandedOutputPath = path.resolve(artifactsDir, brandedFileName);
        const courseYamlPath = path.resolve(coursePath, 'course.yaml');
        const injectScript = path.resolve(CWD, '.agent', 'skills', 'pptx-nfu-branded', 'scripts', 'inject_branding.py');
        const pythonBin = '/opt/anaconda3/envs/mybase/bin/python';

        // 推导周次编号（从目录名提取 W01 之类的数字部分）
        const weekNum = weekMatch ? weekMatch[1].replace('W0', '').replace('W', '') : null;

        if (fs.existsSync(injectScript) && fs.existsSync(courseYamlPath)) {
            console.log(`\n🏫 [NFU] 自动注入品牌封装...`);
            const brandCmd = [
                pythonBin, `"${injectScript}"`,
                `--input "${rawOutputPath}"`,
                `--output "${brandedOutputPath}"`,
                `--course-yaml "${courseYamlPath}"`,
            ];
            if (weekNum) brandCmd.push(`--week ${weekNum}`);

            try {
                execSync(brandCmd.join(' '), { stdio: 'inherit', cwd: CWD });
                console.log(`\n✅ 品牌成品: ${path.relative(CWD, brandedOutputPath)}`);

                // 同时在旧版目录放一份符号链接（向后兼容）
                const legacyLink = path.resolve(legacyDir, brandedFileName);
                try {
                    if (fs.existsSync(legacyLink)) fs.unlinkSync(legacyLink);
                    fs.copyFileSync(brandedOutputPath, legacyLink);
                } catch (e) {
                    // 符号链接失败不影响主流程
                }
            } catch (e) {
                console.warn(`⚠️  品牌注入失败: ${e.message}`);
                console.warn(`   裸 PPT 仍可使用: ${path.relative(CWD, rawOutputPath)}`);
                // 将裸 PPT 复制到 artifacts 作为降级产物
                fs.copyFileSync(rawOutputPath, path.resolve(artifactsDir, rawFileName));
            }
        } else {
            console.log(`\nℹ️  未找到 NFU 品牌注入脚本或 course.yaml，跳过品牌封装`);
            console.log(`   裸 PPT 已保存: ${path.relative(CWD, rawOutputPath)}`);
            // 将裸 PPT 也复制到 artifacts 目录
            fs.copyFileSync(rawOutputPath, path.resolve(artifactsDir, rawFileName));
        }
    })
    .catch(err => console.error("❌ 保存失败:", err));
