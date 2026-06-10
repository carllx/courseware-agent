#!/usr/bin/env python3
import json
import os
import re
import hashlib
from pathlib import Path
import sys

def get_id(node_type, label):
    hash_obj = hashlib.md5(f"{node_type}_{label}".encode('utf-8'))
    return f"{node_type}_{hash_obj.hexdigest()[:8]}"

def extract_chunk_id(filename):
    match = re.search(r'_chunk_(\d+)_', filename)
    if match:
        return int(match.group(1))
    return -1

def main():
    if len(sys.argv) < 3:
        print("Usage: python local_graph_extractor.py <slices_dir> <output_graph.json>")
        sys.exit(1)
        
    slices_dir = Path(sys.argv[1])
    out_file = Path(sys.argv[2])
    
    files_data = []
    
    for md_file in slices_dir.glob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        label = h1_match.group(1).strip() if h1_match else md_file.stem.replace('_', ' ')
        
        # Clean label for matching
        label_clean = re.sub(r'[^a-zA-Z0-9\s]', '', label).strip()
        
        chunk_num = extract_chunk_id(md_file.name)
        
        files_data.append({
            "path": md_file,
            "filename": md_file.name,
            "content": content,
            "label": label,
            "label_clean": label_clean,
            "chunk_num": chunk_num,
            "id": get_id("file", label)
        })
        
    # Sort by chunk num
    files_data.sort(key=lambda x: x["chunk_num"])
    
    nodes = {}
    links = []
    
    # 1. Create nodes
    for data in files_data:
        nodes[data["id"]] = {
            "id": data["id"],
            "label": data["label"],
            "file_type": "concept",
            "source_file": data["filename"],
            "description": "Primary concept extracted from chunk"
        }
        
    # 2. Sequential Links
    for i in range(len(files_data) - 1):
        if files_data[i]["chunk_num"] != -1 and files_data[i+1]["chunk_num"] != -1:
            links.append({
                "source": files_data[i]["id"],
                "target": files_data[i+1]["id"],
                "relation": "follows",
                "confidence": "AST",
                "confidence_score": 1.0,
                "source_file": files_data[i+1]["filename"]
            })
            
    # 3. Cross-reference Links
    # To avoid O(N^2) being too slow, we can just do basic substring checks
    # Only use labels > 5 chars to avoid noise
    valid_labels = [d for d in files_data if len(d["label_clean"]) > 5]
    
    for data in files_data:
        text = data["content"]
        for target in valid_labels:
            if target["id"] == data["id"]:
                continue
            # simple substring search (case-insensitive)
            if target["label_clean"].lower() in text.lower():
                links.append({
                    "source": data["id"],
                    "target": target["id"],
                    "relation": "references",
                    "confidence": "AST",
                    "confidence_score": 0.8,
                    "source_file": data["filename"]
                })
                
    graph_data = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": list(nodes.values()),
        "links": links
    }
    
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
    print(f"[+] Processed {len(files_data)} slices. Extracted {len(nodes)} nodes and {len(links)} edges.")
    print(f"[+] Graph saved to {out_file}")

if __name__ == "__main__":
    main()
