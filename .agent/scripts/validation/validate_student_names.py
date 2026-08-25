#!/usr/bin/env python3
"""
学生姓名合规扫描工具 (Student Name Validation Script)
基于 students_roster.yaml，在 markdown 或 srt 中进行精准与模糊（拼音级）匹配。
提取并标注识别错误的疑似姓名。
"""
import os
import sys
import yaml
import re
import argparse

try:
    import pypinyin
except ImportError:
    print("Warning: pypinyin not installed. Fuzzy phonetic matching will be disabled.")
    pypinyin = None

def load_roster(course_dir):
    roster_path = os.path.join(course_dir, 'students_roster.yaml')
    if not os.path.exists(roster_path):
        return []
    with open(roster_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('students', [])

def extract_chinese_segments(text):
    """提取连续的中文片段"""
    return re.findall(r'[\u4e00-\u9fa5]+', text)

def compute_phonetic_similarity(target_pinyin, source_pinyin):
    """计算发音相似度 (简化版 Levenshtein 占比)"""
    # 忽略声调
    t_py = [p[0][:-1] if p[0][-1].isdigit() else p[0] for p in target_pinyin]
    s_py = [p[0][:-1] if p[0][-1].isdigit() else p[0] for p in source_pinyin]
    
    match_count = 0
    for tp, sp in zip(t_py, s_py):
        # 容忍平翘舌和鼻音等模糊音
        tp = tp.replace('zh', 'z').replace('ch', 'c').replace('sh', 's').replace('l', 'n')
        sp = sp.replace('zh', 'z').replace('ch', 'c').replace('sh', 's').replace('l', 'n')
        if tp == sp:
            match_count += 1
            
    return match_count / len(t_py)

def validate_names(file_path, students):
    if not os.path.exists(file_path):
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    warnings = []
    
    # 预计算花名册拼音
    student_pinyins = {}
    if pypinyin:
        for s in students:
            name = s['name']
            student_pinyins[name] = pypinyin.pinyin(name, style=pypinyin.NORMAL)
            
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # 提取中文
        segments = extract_chinese_segments(line)
        for seg in segments:
            # 1. 精准匹配（不报错，说明写对了）
            for s in students:
                if s['name'] in seg:
                    # found correct name
                    pass
            
            # 2. 模糊匹配：滑动窗口
            if pypinyin:
                seg_py = pypinyin.pinyin(seg, style=pypinyin.NORMAL)
                for s in students:
                    name_len = len(s['name'])
                    if len(seg) < name_len:
                        continue
                        
                    # 滑动窗口
                    for j in range(len(seg) - name_len + 1):
                        window_py = seg_py[j:j+name_len]
                        target_py = student_pinyins[s['name']]
                        sim = compute_phonetic_similarity(target_py, window_py)
                        
                        if sim >= 0.65: # 相似度阈值
                            suspect_text = seg[j:j+name_len]
                            if suspect_text != s['name']:
                                context = line[:100] # short context
                                warnings.append({
                                    'line': i+1,
                                    'suspect': suspect_text,
                                    'suggest': s['name'],
                                    'context': context,
                                    'confidence': sim
                                })
                                
    return warnings

def main():
    parser = argparse.ArgumentParser(description="Validate student names in text.")
    parser.add_argument("--course", default=".", help="Course root directory")
    parser.add_argument("--week", default=None, help="Week filter (e.g., 1)")
    parser.add_argument("target", nargs='*', help="Specific files to scan")
    args = parser.parse_args()
    
    students = load_roster(args.course)
    if not students:
        print("No students roster found. Skipping name validation.")
        return
        
    files_to_scan = []
    if args.target:
        files_to_scan.extend(args.target)
    else:
        # Default recursive scan in weeks folder if not specified
        weeks_dir = os.path.join(args.course, 'weeks')
        if os.path.exists(weeks_dir):
            for root, dirs, files in os.walk(weeks_dir):
                if args.week and f"W0{args.week}" not in root and f"W{args.week}" not in root:
                    continue
                for f in files:
                    if f.endswith('.md') or f.endswith('.srt'):
                        files_to_scan.append(os.path.join(root, f))
                        
    total_warnings = 0
    for f in files_to_scan:
        warnings = validate_names(f, students)
        if warnings:
            print(f"\\nFile: {f}")
            for w in warnings:
                total_warnings += 1
                conf_str = "High" if w['confidence'] > 0.8 else "Medium"
                print(f"  Line {w['line']}: [NAME_MISMATCH] 疑似将 '{w['suggest']}' 错写为 '{w['suspect']}' (置信度: {conf_str})")
                print(f"  > Context: {w['context']}")
                
    if total_warnings > 0:
        print(f"\\nFound {total_warnings} possible name mismatches.")
        sys.exit(0) # Not failing the build, just warning for human review
    else:
        print("Student names check passed.")

if __name__ == "__main__":
    main()
