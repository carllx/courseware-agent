#!/bin/zsh

# Convert Markdown to EPUB using pandoc and pandoc-crossref
# Requires: pandoc, pandoc-crossref

INPUT_MD=${1}
OUTPUT_EPUB=${2}
COVER_IMAGE=${3:-""}
TITLE=${4:-"Generated EPUB"}

PANDOC_CMD=(
  pandoc
  --from markdown
  --to epub3
  --metadata title="${TITLE}"
  "${INPUT_MD}"
  --output "${OUTPUT_EPUB}"
  --toc
  --filter pandoc-crossref
)

if [[ -n "${COVER_IMAGE}" ]]; then
  PANDOC_CMD+=("--epub-cover-image=${COVER_IMAGE}")
fi

echo "Running: ${PANDOC_CMD[@]}"
"${PANDOC_CMD[@]}"
