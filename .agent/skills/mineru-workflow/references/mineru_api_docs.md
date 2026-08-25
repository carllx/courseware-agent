# MinerU API Reference and Architecture

## System Architecture

The Mineru Scan System is a local document processing system that relies on the Mineru API for PDF/Image to Markdown conversion, combined with Imgur for image hosting.

- **Backend**: Python FastAPI service running locally (default `http://localhost:8000`).
- **Core Pipeline**:
  1.  **Scanning**: Recurses through a local folder, collecting supported files (`.pdf`, `.jpg`, `.png`). Project name is derived from the parent folder.
  2.  **Uploading**: Uses `MineruClient` to upload files in batches to Mineru.
  3.  **Polling**: Polls the Mineru API for batch status (`waiting` -> `running` -> `done`/`failed`).
  4.  **Downloading**: Downloads the resulting ZIP package and extracts it to `temp_processing/{TaskName}/`.
  5.  **Processing (Imgur)**: Parses `full.md`, extracts local image references, uploads them to Imgur, and replaces them with online URLs.
  6.  **Archiving**: Moves the final Markdown to `outputs/{ProjectName}/{OriginalFileName}.md` preserving the original directory structure using `data_id` mapping.
  7.  **Cleanup**: Deletes intermediate files.

- **Stability & Resume**: Uses `project_state.json` to store `batch_id` and `processed_files` for resuming interrupted tasks. Features exponential backoff for Mineru API and handles Imgur 429 errors.

## API Endpoints

- `POST /api/process/path`
  Trigger a local path processing task.
  ```json
  { "path": "/absolute/path/to/directory_or_file" }
  ```
  Returns:
  ```json
  {
    "status": "success",
    "processed_paths": ["outputs/Project/file.md"],
    "output_dir": "outputs/Project"
  }
  ```

- `POST /api/process/stop`
  Force stop the current task.
  Returns: `{ "status": "success", "message": "Stop signal sent" }`

## Quick Start (User Interface)

Users can launch the system via `start_mac.command` (macOS) or `start_win.bat` (Windows).
The frontend supports Drag & Drop (recursively scanning via `webkitGetAsEntry()`) or absolute path submission.
Output is placed in `outputs/{ProjectName}`.

## Updating Conda Environment for MinerU
To manually update the underlying MinerU environment (from Obsidian notes):
1. `conda activate MinerU`
2. `pip install -U "magic-pdf[full]" --extra-index-url https://wheels.myhloli.com`
3. Download models via `download_models_hf.py` from huggingface_hub.
