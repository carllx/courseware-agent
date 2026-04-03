
import json
import os
import sys

def search_textbook_index(query, base_dir):
    """
    Searches the textbook index for the given query.
    Returns a list of matches.
    """
    index_path = os.path.join(base_dir, "knowledge", "index.json")
    
    if not os.path.exists(index_path):
        return {"error": f"Index not found at {index_path}. Please run indexer.py first."}

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load index: {e}"}

    results = []
    query_lower = query.lower()
    
    # Simple keyword search in titles
    for book_name, book_data in index_data.items():
        for file_entry in book_data.get("files", []):
            file_path = file_entry.get("path")
            for chapter in file_entry.get("chapters", []):
                title = chapter.get("title", "")
                if query_lower in title.lower():
                    results.append({
                        "book": book_name,
                        "chapter": title,
                        "path": file_path,
                        "lines": [chapter.get("start_line"), chapter.get("end_line")]
                    })
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_index.py <query>")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    
    # Determine base_dir (assuming script is in .agent/skills/librarian/scripts)
    # Project root is ../../../../ from here
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, "../../../../../"))
    
    # Adjust if run from different location or structure is different
    # Fallback to current working directory if it looks like project root
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "knowledge", "index.json")):
       base_dir = cwd

    matches = search_textbook_index(query, base_dir)
    # Debug print
    # print(f"DEBUG: base_dir={base_dir}") 
    print(json.dumps(matches, indent=2, ensure_ascii=False))
