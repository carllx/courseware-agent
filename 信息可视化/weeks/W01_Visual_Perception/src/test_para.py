import sys, re
sys.path.insert(0, '/Users/yamlam/Downloads/2025-2026-2 课程/.agent/skills/validation_suite/scripts')
from validate_script_length import _analyze_paragraphs, TETRAGRAPH_WHITELIST

def block_is_tag(line):
    return line.startswith("[") or line.startswith("<!--")

def get_paras(text):
    WINDOW_SIZE = 5
    raw_sentences = re.split(r'[。！？]', text)
    raw_sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 5]
    paragraphs = []
    for idx in range(0, len(raw_sentences), WINDOW_SIZE):
        window = '。'.join(raw_sentences[idx:idx + WINDOW_SIZE])
        if len(window) > 30:
            paragraphs.append(window)
    return paragraphs

# Inspect what strings matched tetragraphs in a text
def inspect_tetragraphs(para):
    para_cn = re.sub(r'[^\u4e00-\u9fff]', '', para)
    if len(para_cn) >= 4:
        seen = set()
        for j in range(len(para_cn) - 3):
            quad = para_cn[j:j+4]
            if quad not in seen and quad not in TETRAGRAPH_WHITELIST:
                seen.add(quad)
        chains = re.findall(r'[\u4e00-\u9fff]{4}[、，][\u4e00-\u9fff]{4}', para)
        return chains
    return []

from validate_script_length import analyze_modules
for fname in ['M04_格式塔原则_大脑的"找规律"强迫症.md', 'M05_范式革命_Vibe_Coding_与生成的艺术.md']:
    print(f"\n--- {fname} ---")
    mods = analyze_modules(fname, 180)
    for mod in mods:
        text = mod['section_text']
        res = _analyze_paragraphs(text)
        if res['has_structural_degen']:
            print(f"Mod '{mod['name']}' has issues: {res['para_issues']}")
            paras = get_paras(text)
            for issue in res['para_issues']:
                idx = issue[0] - 1
                if idx < len(paras):
                    p_text = paras[idx]
                    chains = inspect_tetragraphs(p_text)
                    print(f"  P{issue[0]}: {p_text[:60]}... => Chains found: {chains}")

