
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Configuration
SOURCE_DIR = Path("/Users/yamlam/Downloads/2025-2026-2 课程/实习指导/knowledge/repository")
TARGET_DIR = Path("/Users/yamlam/Downloads/2025-2026-2 课程/实习指导/knowledge/library")

def ensure_pandoc():
    """Check if pandoc is available."""
    if not shutil.which("pandoc"):
        print("Error: pandoc is not installed or not in PATH.")
        return False
    return True

def convert_doc_to_docx(doc_path, temp_dir):
    """Convert .doc to .docx using textutil (macOS only)."""
    docx_path = temp_dir / (doc_path.stem + ".docx")
    try:
        subprocess.run(
            ["textutil", "-convert", "docx", "-output", str(docx_path), str(doc_path)],
            check=True,
            capture_output=True
        )
        return docx_path
    except subprocess.CalledProcessError as e:
        print(f"  [Error] textutil failed for {doc_path.name}: {e}")
        return None

def convert_docx_to_md(docx_path, output_md_path):
    """Convert .docx to .md using pandoc."""
    try:
        # Using sophisticated pandoc options for better markdown
        subprocess.run(
            [
                "pandoc",
                "-f", "docx",
                "-t", "markdown_github-raw_html", # GitHub flavored markdown, less raw HTML
                "--wrap=none", # Don't hard wrap lines
                "--extract-media=.", # Extract images if any (relative to output)
                "-o", str(output_md_path),
                str(docx_path)
            ],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [Error] pandoc failed for {docx_path.name}: {e}")
        return False

def process_file(file_path, target_root):
    """Process a single file."""
    relative_path = file_path.relative_to(SOURCE_DIR)
    target_path = target_root / relative_path.parent / (file_path.stem + ".md")
    
    # Ensure target directory exists
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing: {relative_path}")

    if file_path.suffix.lower() == ".docx":
        # Direct conversion
        if convert_docx_to_md(file_path, target_path):
            print(f"  -> Created {target_path.name}")
            
    elif file_path.suffix.lower() == ".doc":
        # Intermediate conversion
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            temp_docx = convert_doc_to_docx(file_path, temp_path)
            if temp_docx and temp_docx.exists():
                if convert_docx_to_md(temp_docx, target_path):
                    print(f"  -> Created {target_path.name}")
            else:
                print(f"  [Skip] Could not convert .doc to intermediate .docx")

def main():
    if not ensure_pandoc():
        return

    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print("-" * 40)

    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} does not exist.")
        return

    # Walk through the directory
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = Path(root) / file
            if file_path.name.startswith("~$") or file_path.name.startswith("."):
                continue # Skip temporary/hidden files
                
            if file_path.suffix.lower() in [".doc", ".docx"]:
                process_file(file_path, TARGET_DIR)

    print("-" * 40)
    print("Conversion complete.")

if __name__ == "__main__":
    main()
