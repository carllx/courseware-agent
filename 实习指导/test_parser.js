const { parseScript } = require('./delivery/utils/ppt_parser');
const path = require('path');

const scriptPath = path.resolve(__dirname, 'scripts/S01_Mobilization.md');
console.log(`解析脚本: ${scriptPath}`);

try {
    const slides = parseScript(scriptPath);
    console.log(`\n共解析出 ${slides.length} 张 Slide`);

    slides.forEach((s, i) => {
        console.log(`\n--- Slide ${i + 1} ---`);
        console.log(`Visual:`, s.visual);
        console.log(`Speech Length: ${s.speech.length} chars`);
        console.log(`Speech Preview: ${s.speech.slice(0, 50).replace(/\n/g, ' ')}...`);
    });
} catch (err) {
    console.error("解析失败:", err);
}
