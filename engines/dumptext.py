import sys
import os
import re
import argparse
import yaml

def extract_oot(content):
    """
    Extract ONLY spoken text for Out-Of-Text (Teleprompter) mode.
    Strips out YAML frontmatter, HTML comments, headers, and metadata lines.
    Preserves:
    - Normal paragraphs
    - Quotes (> ) if they are not metadata
    - Lists
    """
    lines = content.splitlines()
    oot_lines = []
    
    in_frontmatter = False
    in_visual_block = False
    in_tag_block = False
    in_oral_tag_block = False
    
    # Metadata markers to ignore
    META_KEYS = ['role', 'stage', 'duration', 'type', 'desc', 'mode']
    ORAL_TAGS = ['STORY TIME', 'PHILOSOPHY', 'CASE STUDY', 'LIFE CONNECT', 'DID YOU KNOW', 'TEACHING MOMENT']
    
    re_visual = re.compile(r'^>\s*\[VISUAL\]', re.I)
    re_activity = re.compile(r'^>\s*\[ACTIVITY\]', re.I)
    re_tag_start = re.compile(r'^>\s*\[(TECH NOTE|WARNING|DID YOU KNOW|STORY TIME|PHILOSOPHY|CASE STUDY|LIFE CONNECT|TEACHING MOMENT)[:\]]', re.I)
    re_stage_note = re.compile(r'^>\s*\[STAGE NOTE', re.I)
    re_info_block = re.compile(r'^>\s*\[!INFO\]', re.I)
    re_quote = re.compile(r'^>\s?(.*)')
    
    def is_meta_line(text):
        m = re.match(r'^\*\*(\w+)\*\*:\s', text.strip())
        if m and m.group(1).lower() in META_KEYS:
            return True
        return False
        
    def should_ignore(line):
        stripped = line.strip()
        if stripped.startswith('#'): return True
        if stripped.startswith('---') and not in_frontmatter: return True
        if stripped.startswith('<!--'): return True
        if stripped == '[SPEECH]': return True
        if stripped.startswith('## Self-Verification'): return True
        if stripped.startswith('- ['): return True
        return False
        
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Handle Frontmatter
        if i == 0 and stripped == '---':
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == '---':
                in_frontmatter = False
            continue
            
        # Block Handling
        if re_visual.match(stripped):
            in_visual_block = True
            in_tag_block = False
            in_oral_tag_block = False
            continue
        if re_activity.match(stripped) or re_stage_note.match(stripped) or re_info_block.match(stripped):
            in_tag_block = True
            in_visual_block = False
            in_oral_tag_block = False
            continue
            
        tag_match = re_tag_start.match(stripped)
        if tag_match:
            tag_name = tag_match.group(1).upper()
            if tag_name in ORAL_TAGS:
                in_oral_tag_block = True
                in_tag_block = False
            else:
                in_tag_block = True
                in_oral_tag_block = False
            in_visual_block = False
            continue
            
        # Closing a block quote
        if (in_visual_block or in_tag_block or in_oral_tag_block) and not stripped.startswith('>'):
            in_visual_block = False
            in_tag_block = False
            in_oral_tag_block = False
            
        if in_visual_block or in_tag_block:
            continue
            
        if should_ignore(stripped):
            continue
            
        # Process Speech
        if stripped == '':
            oot_lines.append('')
            continue
            
        quote_match = re_quote.match(stripped)
        text_to_save = line
        
        if quote_match:
            text = quote_match.group(1).strip()
            if is_meta_line(text):
                continue
            if re.match(r'^\[[A-Z _!]+\]$', text):
                continue
            text_to_save = text
            
        # Clean formatting
        text_to_save = re.sub(r'\*\*(.*?)\*\*', r'\1', text_to_save)
        text_to_save = re.sub(r'\*(.*?)\*', r'\1', text_to_save)
        text_to_save = re.sub(r'`(.*?)`', r'\1', text_to_save)
        text_to_save = re.sub(r'^\s*[\-\*]\s+', '• ', text_to_save)
        text_to_save = re.sub(r'\*\*\(Pause:.*?\)\*\*', r'', text_to_save)
        text_to_save = re.sub(r'\(Pause:.*?\)', r'', text_to_save)
        
        if text_to_save.strip() or stripped == '':
            oot_lines.append(text_to_save)

    result = '\n'.join(oot_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


def dump_script(main_script_path, mode='full', segments=None, output_path=None):
    if not os.path.exists(main_script_path):
        print(f"❌ Error: Script file not found at {main_script_path}")
        sys.exit(1)
        
    script_dir = os.path.dirname(os.path.abspath(main_script_path))
    
    segment_filter = None
    if segments:
        segment_filter = [s.strip() for s in segments.split(',')]
        
    is_yaml = main_script_path.endswith('.yaml') or main_script_path.endswith('.yml')

    compiled_content = ""
    
    if is_yaml:
        with open(main_script_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
            
        segment_list = config.get('segments', [])
        parts = []
        for seg in segment_list:
            # seg 可能是 dict (如 {"id": "M01", "src": "src/M01.md"}) 或纯字符串路径
            rel_path = seg.get('src') if isinstance(seg, dict) else str(seg)
            if not rel_path:
                continue
            
            if segment_filter:
                basename = os.path.basename(rel_path)
                keep = False
                for s in segment_filter:
                    if re.match(rf'^{re.escape(s)}[_.]', basename):
                        keep = True
                        break
                if not keep:
                    continue
                    
            include_path = os.path.join(script_dir, rel_path)
            if os.path.exists(include_path):
                with open(include_path, 'r', encoding='utf-8') as segment_file:
                    seg_content = segment_file.read()
                    # Markdown segments might still optionally contain nested includes
                    def replace_nested(m):
                        np = os.path.join(script_dir, m.group(1).strip())
                        if os.path.exists(np):
                            with open(np, 'r', encoding='utf-8') as nested_f:
                                return nested_f.read()
                        print(f"⚠️ Warning: Could not find nested segment {np}")
                        return m.group(0)
                        
                    seg_content = re.sub(r"<!--\s*include:\s*(.+?)\s*-->", replace_nested, seg_content)
                    parts.append(f"\n<!-- ### BEGIN {rel_path} ### -->\n" + seg_content + f"\n<!-- ### END {rel_path} ### -->\n")
            else:
                print(f"⚠️ Warning: Could not find segment {include_path}")
        compiled_content = "".join(parts)

    else:
        # 兼容旧的 script.md 处理逻辑
        with open(main_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        def replace_include(match):
            rel_path = match.group(1).strip()
            include_path = os.path.join(script_dir, rel_path)
            
            if segment_filter:
                basename = os.path.basename(rel_path)
                keep = False
                for s in segment_filter:
                    if re.match(rf'^{re.escape(s)}[_.]', basename):
                        keep = True
                        break
                if not keep:
                    return ""
                    
            if os.path.exists(include_path):
                with open(include_path, 'r', encoding='utf-8') as segment_file:
                    seg_content = segment_file.read()
                    seg_content = re.sub(r"<!--\s*include:\s*(.+?)\s*-->", replace_include, seg_content)
                    return f"\n<!-- ### BEGIN {rel_path} ### -->\n" + seg_content + f"\n<!-- ### END {rel_path} ### -->\n"
            else:
                print(f"⚠️ Warning: Could not find segment {include_path}")
                return match.group(0)

        compiled_content = re.sub(r"<!--\s*include:\s*(.+?)\s*-->", replace_include, content)
    
    if mode == 'oot':
        compiled_content = extract_oot(compiled_content)
        ext_target = "transcript.oot.txt" if is_yaml else "script.oot.txt"
    else:
        ext_target = "compiled.md" if is_yaml else "script_compiled.md"
    
    if output_path is None:
        if is_yaml:
            # YAML V5 架构：强制输出到 .build/ 目录
            build_dir = os.path.join(script_dir, ".build")
            os.makedirs(build_dir, exist_ok=True)
            output_path = os.path.join(build_dir, ext_target)
        else:
            # 旧架构
            filename, _ = os.path.splitext(main_script_path)
            # 如果结尾是 script，就不用再加 script 前缀了
            output_path = os.path.join(script_dir, ext_target)
        
    # 差异检测：仅在内容实际变化时写入，避免不必要的 mtime 更新
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            existing = f.read()
        if existing == compiled_content:
            print(f"✅ 内容无变化，跳过写入 ({mode} mode). {output_path}")
            return
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(compiled_content)
        
    print(f"✅ Compilation complete ({mode} mode). Saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Course script flattening and dumping tool.")
    parser.add_argument("script", help="Path to main script.md file")
    parser.add_argument("--mode", choices=['full', 'oot', 'compile'], default='full', help="Output mode. 'oot' extracts speech only.")
    parser.add_argument("--segments", help="Comma-separated segments to include, e.g. M01,M02. If omitted, includes all.", default=None)
    parser.add_argument("--output", help="Optional output path.", default=None)
    
    args = parser.parse_args()
    dump_mode = 'full' if args.mode == 'compile' else args.mode
    dump_script(args.script, dump_mode, args.segments, args.output)
