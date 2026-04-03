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

if (!courseDir || !scriptRelPath) {
    console.error("❌ 用法: node engines/generate_course_ppt.js <课程目录> <脚本路径>");
    console.error("   示例: node engines/generate_course_ppt.js 信息可视化 weeks/W01_Visual_Perception/script.md");
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

slides.forEach((slide, i) => {
    try {
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

// 6. 保存
const outputDir = path.resolve(coursePath, 'build', 'presentations');
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
const outputPath = path.resolve(outputDir, `${scriptName}_Presentation_Gen.pptx`);

pres.writeFile({ fileName: outputPath })
    .then(() => {
        console.log(`\n🎉 保存成功: ${path.relative(CWD, outputPath)}`);
        console.log(`   Slide 数: ${slides.length}`);
    })
    .catch(err => console.error("❌ 保存失败:", err));
