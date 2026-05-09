const fs = require('fs');
const path = require('path');

const srcDir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src';
const slidesDir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/public/slides';

const files = fs.readdirSync(srcDir).filter(f => f.startsWith('M') && f.endsWith('.md')).sort();

let remaining = [];
for (const file of files) {
    const filepath = path.join(srcDir, file);
    const content = fs.readFileSync(filepath, 'utf8');
    const blocks = content.split('> [VISUAL]');
    
    for (let i = 1; i < blocks.length; i++) {
        const block = blocks[i];
        if (!block.includes('no_ai_flag')) {
            let slideId = '';
            let scene = '';
            const lines = block.split('\n');
            for (const line of lines) {
                if (line.includes('**Slide**:')) slideId = line.split(':')[1].trim();
                if (line.includes('**Scene**:')) scene = line.substring(line.indexOf(':') + 1).trim();
            }
            
            const imagePath = path.join(slidesDir, slideId + '.png');
            let size = -1;
            if (fs.existsSync(imagePath)) size = fs.statSync(imagePath).size;
            
            if (size < 10000) {
                remaining.push(`- **${file}** | \`${slideId}\` (缺失)\n  > Scene: ${scene}`);
            }
        }
    }
}
console.log(remaining.join('\n\n'));
console.log(`\n总计剩余未生成或仅为占位符的 AI 素材数量: ${remaining.length} 张`);
