#!/usr/bin/env python3
"""彻底清洗 YouTube 自动生成字幕 - 合并渐进式重复"""
import re, sys

def clean_youtube_srt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析所有字幕块
    blocks = re.split(r'\n\n+', content.strip())
    entries = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        time_line = None
        text_lines = []
        for line in lines:
            if '-->' in line:
                time_line = line.strip()
            elif not re.match(r'^\d+$', line.strip()):
                t = line.strip()
                if t:
                    text_lines.append(t)
        if time_line and text_lines:
            text = ' '.join(text_lines)
            # 去掉纯 [音乐] / [Music]
            text = re.sub(r'\[音乐\]\s*', '', text).strip()
            text = re.sub(r'\[Music\]\s*', '', text).strip()
            if text:
                start, end = time_line.split(' --> ')
                entries.append({'start': start.strip(), 'end': end.strip(), 'text': text})
    
    if not entries:
        print(f"⚠️ {input_path}: 无有效字幕")
        return
    
    # 合并策略：提取每个条目的"新增"文本部分
    # YouTube 自动字幕特征：每条 = 上一条尾部 + 新内容
    # 我们用最后一句完整文本作为每段的代表
    
    # 先收集所有唯一的完整句子
    sentences = []
    for e in entries:
        text = e['text']
        # 跳过10ms间隔的渐进帧 (e.g., 06,309 → 06,319)
        if entries.index(e) > 0:
            prev = entries[entries.index(e) - 1]
            if text.startswith(prev['text'][:10]):
                # 这是渐进帧，用更长的版本替换
                if sentences and prev['text'] in sentences[-1]['text']:
                    sentences[-1] = {'start': sentences[-1]['start'], 'end': e['end'], 'text': text}
                    continue
        sentences.append({'start': e['start'], 'end': e['end'], 'text': text})
    
    # 最终去重：如果文本完全被下一条包含，合并
    final = []
    for i, s in enumerate(sentences):
        if i + 1 < len(sentences):
            next_s = sentences[i + 1]
            if next_s['text'].startswith(s['text'][:15]):
                continue  # 跳过，由下一条覆盖
        final.append(s)
    
    # 再做一轮：去除完全重复的文本
    deduped = []
    prev_text = ""
    for s in final:
        if s['text'] != prev_text:
            deduped.append(s)
            prev_text = s['text']
    
    # 输出
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, s in enumerate(deduped, 1):
            f.write(f"{i}\n{s['start']} --> {s['end']}\n{s['text']}\n\n")
    
    print(f"✅ {output_path}: {len(deduped)} 条清洗后字幕")

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        out = arg.replace('.srt', '_final.srt')
        clean_youtube_srt(arg, out)
