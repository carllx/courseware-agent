const fs = require('fs');
const path = require('path');

const srcDir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src';
const slidesDir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/public/slides';

const files = fs.readdirSync(srcDir).filter(f => f.startsWith('M') && f.endsWith('.md')).sort();

for (const file of files) {
    const filepath = path.join(srcDir, file);
    const content = fs.readFileSync(filepath, 'utf8');
    const blocks = content.split('> [VISUAL]');
    
    for (let i = 1; i < blocks.length; i++) {
        const block = blocks[i];
        if (!block.includes('no_ai_flag: true')) {
            let slideId = '';
            let scene = '';
            const lines = block.split('\n');
            for (const line of lines) {
                if (line.startsWith('> **Slide**:')) slideId = line.split(':')[1].trim();
                if (line.startsWith('> **Scene**:')) scene = line.substring(line.indexOf(':') + 1).trim();
            }
            
            // check file size
            const imagePath = path.join(slidesDir, slideId + '.png');
            let size = -1;
            if (fs.existsSync(imagePath)) {
                size = fs.statSync(imagePath).size;
            }
            
            if (size < 10000) { // arbitrary small size for placeholder
                console.log(`- **${file}** | \`${slideId}\`\n  - 描述: ${scene}\n  - 文件大小: ${size} bytes`);
            }
        }
    }
}
