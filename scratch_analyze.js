const fs = require('fs');
const path = require('path');

function getWordCount(text) {
    text = text.replace(/<[^>]+>/g, '');
    text = text.replace(/\[.*?\]\(.*?\)/g, '');
    text = text.replace(/[*_#`]/g, '');
    
    const cjkMatches = text.match(/[\u4e00-\u9fff]/g);
    const cjkCount = cjkMatches ? cjkMatches.length : 0;
    
    const engMatches = text.match(/\b[a-zA-Z]+\b/g);
    const engCount = engMatches ? engMatches.length : 0;
    
    return cjkCount + engCount;
}

function analyzeFile(filepath) {
    const content = fs.readFileSync(filepath, 'utf8');
    const visualBlocks = content.split(/>\s*\[VISUAL\]/);
    const gaps = [];
    
    if (visualBlocks.length > 1) {
        for (let i = 1; i < visualBlocks.length; i++) {
            let segment = visualBlocks[i];
            
            // Remove ALL blockquote lines (> ...) since they are metadata, labels, or ACTIVITY
            // We only want the SPEECH text (normal markdown paragraphs)
            const speechLines = segment.split('\n').filter(line => !line.trim().startsWith('>'));
            const speechText = speechLines.join('\n');
            
            gaps.push(getWordCount(speechText));
        }
    }
    return gaps;
}

function findMdFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            findMdFiles(fullPath, fileList);
        } else if (file.endsWith('.md') && fullPath.includes('/src/')) {
            fileList.push(fullPath);
        }
    }
    return fileList;
}

const baseDir = '/Users/yamlam/Downloads/2025-2026-2 课程';
let allFiles = [];
try {
    const courses = ['交互产品开发', '信息可视化'];
    for (const course of courses) {
        const weeksDir = path.join(baseDir, course, 'weeks');
        if (fs.existsSync(weeksDir)) {
            allFiles = allFiles.concat(findMdFiles(weeksDir));
        }
    }
} catch (e) {
    console.error(e);
}

let totalGaps = [];
for (const file of allFiles) {
    totalGaps = totalGaps.concat(analyzeFile(file));
}

const bins = {
    '<=150': 0,
    '151-250': 0,
    '251-360': 0,
    '>360': 0
};

for (const g of totalGaps) {
    if (g <= 150) bins['<=150']++;
    else if (g <= 250) bins['151-250']++;
    else if (g <= 360) bins['251-360']++;
    else bins['>360']++;
}

console.log("Regression Analysis of Visual Gaps (Speech Only):");
console.log(`Total gaps analyzed: ${totalGaps.length}`);
const total = totalGaps.length;
for (const [k, v] of Object.entries(bins)) {
    console.log(`Gap ${k} words: ${v} (${total ? (v/total*100).toFixed(1) : 0}%)`);
}
