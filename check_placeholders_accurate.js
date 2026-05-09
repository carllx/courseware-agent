const fs = require('fs');
const path = require('path');

const srcDir = '/Users/yamlam/Downloads/2025-2026-2 课程/交互产品开发/weeks/W02_Cognitive_Friction/src';

const files = fs.readdirSync(srcDir).filter(f => f.startsWith('M') && f.endsWith('.md')).sort();

let count = 0;
for (const file of files) {
    const filepath = path.join(srcDir, file);
    const content = fs.readFileSync(filepath, 'utf8');
    const blocks = content.split('> [VISUAL]');
    
    for (let i = 1; i < blocks.length; i++) {
        const block = blocks[i];
        // match both '**no_ai_flag**: true' and 'no_ai_flag: true'
        if (!block.match(/no_ai_flag\*?:\s*true/)) {
            let slideId = '';
            let scene = '';
            const lines = block.split('\n');
            for (const line of lines) {
                if (line.includes('**Slide**:')) slideId = line.split(':')[1].trim();
                if (line.includes('**Scene**:')) scene = line.substring(line.indexOf(':') + 1).trim();
            }
            console.log(`- **${file}** | \`${slideId}\`\n  > Scene: ${scene}`);
            count++;
        }
    }
}
console.log(`\nTotal AI Visuals needed: ${count}`);
